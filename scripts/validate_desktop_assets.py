#!/usr/bin/env python3
from __future__ import annotations

import json
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "desktop-assets.json"
IMAGE_TYPE = 0xFFFD0002


def fail(message: str) -> None:
    raise SystemExit(message)


def validate_svg(path: Path) -> None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{path}: invalid SVG XML: {exc}")
    if not root.tag.endswith("svg"):
        fail(f"{path}: root element is not SVG")
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1].lower() == "script":
            fail(f"{path}: scripts are prohibited")
        for attr, value in node.attrib.items():
            if attr.rsplit("}", 1)[-1].lower() == "href" and value.startswith(
                ("http:", "https:", "file:", "data:")
            ):
                fail(f"{path}: external resources are prohibited")


def validate_line_only_symbolic(path: Path) -> None:
    """Keep large/places symbolic marks free of enclosed fill geometry."""
    root = ET.parse(path).getroot()
    geometry = []
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        if tag in {"path", "rect", "circle", "ellipse", "polygon", "polyline", "line"}:
            geometry.append(tag)
    if not geometry or any(tag != "line" for tag in geometry):
        fail(f"{path}: symbolic geometry must use line elements only, found {geometry}")
    if any(
        node.attrib.get("fill", "").lower() not in {"", "none"}
        for node in root.iter()
    ):
        fail(f"{path}: symbolic icon must not contain painted fill geometry")


def read_xcursor_frames(path: Path) -> list[dict[str, object]]:
    data = path.read_bytes()
    if len(data) < 16:
        fail(f"{path}: cursor file is too small")
    magic, header_size, version, ntoc = struct.unpack_from("<4sIII", data, 0)
    if magic != b"Xcur" or header_size != 16 or version != 0x00010000:
        fail(f"{path}: invalid Xcursor header")

    frames: list[dict[str, object]] = []
    for index in range(ntoc):
        offset = 16 + index * 12
        if offset + 12 > len(data):
            fail(f"{path}: cursor TOC escapes file")
        type_id, subtype, position = struct.unpack_from("<III", data, offset)
        if type_id != IMAGE_TYPE:
            fail(f"{path}: unsupported cursor TOC type {type_id:#x}")
        if position + 36 > len(data):
            fail(f"{path}: cursor frame position escapes file")
        chunk = struct.unpack_from("<IIIIIIIII", data, position)
        (
            chunk_header,
            chunk_type,
            chunk_subtype,
            chunk_version,
            width,
            height,
            xhot,
            yhot,
            delay,
        ) = chunk
        if chunk_header != 36 or chunk_type != IMAGE_TYPE or chunk_version != 1:
            fail(f"{path}: invalid Xcursor image chunk")
        if chunk_subtype != subtype or width != subtype or height != subtype:
            fail(f"{path}: Xcursor frame dimensions/subtype mismatch")
        if xhot >= width or yhot >= height:
            fail(f"{path}: Xcursor hotspot lies outside image")
        pixel_count = width * height
        end = position + 36 + pixel_count * 4
        if end > len(data):
            fail(f"{path}: cursor pixel payload escapes file")
        pixels = struct.unpack_from(f"<{pixel_count}I", data, position + 36)
        if not any((pixel >> 24) & 0xFF for pixel in pixels):
            fail(f"{path}: cursor frame is fully transparent")
        frames.append(
            {
                "size": subtype,
                "xhot": xhot,
                "yhot": yhot,
                "delay": delay,
                "pixels": pixels,
            }
        )
    return frames


def validate_xcursor(
    path: Path,
    expected_sizes: set[int],
    frames_per_size: int = 1,
    animated: bool = False,
) -> None:
    frames = read_xcursor_frames(path)
    expected_count = len(expected_sizes) * frames_per_size
    if len(frames) != expected_count:
        fail(
            f"{path}: expected {expected_count} cursor frames, "
            f"found {len(frames)}"
        )

    counts = Counter(int(frame["size"]) for frame in frames)
    if set(counts) != expected_sizes:
        fail(f"{path}: cursor frame sizes differ: {sorted(counts)}")
    for size in expected_sizes:
        if counts[size] != frames_per_size:
            fail(
                f"{path}: expected {frames_per_size} frame(s) at {size}px, "
                f"found {counts[size]}"
            )

    for frame in frames:
        delay = int(frame["delay"])
        if animated and delay <= 0:
            fail(f"{path}: animated cursor frame is missing a positive delay")
        if not animated and delay != 0:
            fail(f"{path}: static cursor frame unexpectedly has delay {delay}")


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def validate_primary_pointer_palette(
    path: Path,
    frost: tuple[int, int, int],
    graphite: tuple[int, int, int],
    blue: tuple[int, int, int],
) -> None:
    frames = read_xcursor_frames(path)
    frame = min(frames, key=lambda item: int(item["size"]))
    frost_count = 0
    graphite_count = 0
    blue_count = 0
    visible = 0
    for pixel in frame["pixels"]:
        alpha = (int(pixel) >> 24) & 0xFF
        if alpha < 160:
            continue
        visible += 1
        color = (
            (int(pixel) >> 16) & 0xFF,
            (int(pixel) >> 8) & 0xFF,
            int(pixel) & 0xFF,
        )
        if color == frost:
            frost_count += 1
        elif color == graphite:
            graphite_count += 1
        elif color == blue:
            blue_count += 1

    if visible < 20:
        fail(f"{path}: primary pointer has too little visible geometry")
    if frost_count < 8 or graphite_count < 8:
        fail(
            f"{path}: primary pointer must retain both Frost fill and "
            "Graphite outline"
        )
    if blue_count:
        fail(
            f"{path}: primary pointer must stay neutral; GoreeCloud Blue is "
            "reserved for activity/action accents"
        )


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    if config.get("schema_version") != 2:
        fail("desktop asset schema_version must be 2")
    if config.get("design_direction") != "light-first":
        fail("desktop assets must preserve the light-first product direction")

    icons = config["icon_theme"]
    cursors = config["cursor_theme"]
    if icons["id"] != "GoreeCloud-Zorin":
        fail("icon theme ID changed unexpectedly")
    if cursors["id"] != "GoreeCloud-Zorin-Cursors":
        fail("cursor theme ID changed unexpectedly")

    normalization = icons.get("normalization", {})
    if not normalization.get("enabled"):
        fail("third-party app icon normalization must remain enabled")
    if normalization.get("mode") != "glaze-plate-preserve-third-party-identity":
        fail("unexpected third-party icon normalization mode")
    if int(normalization.get("canvas", 0)) != 1024:
        fail("icon normalization canvas must remain 1024")
    if int(normalization.get("presentation_inset", -1)) != 64:
        fail("icon normalization must preserve the Glaze 64px presentation inset")
    if int(normalization.get("safe_area_inset", -1)) != 128:
        fail("icon normalization must preserve the Glaze 128px safe-area inset")
    content_inset = int(normalization.get("content_inset", -1))
    core_inset = int(normalization.get("core_identity_inset", -1))
    if not 128 <= content_inset <= core_inset == 224:
        fail("normalized third-party identity must stay between safe and core Glaze zones")
    if [int(value) for value in normalization.get("optical_sizes", [])] != [24, 32, 48, 64]:
        fail("icon normalization optical-size ladder must remain 24/32/48/64")
    behavior = normalization.get("behavior", {})
    if behavior.get("modify_desktop_files") or behavior.get("modify_application_packages"):
        fail("icon normalization must not modify third-party launchers or packages")
    if behavior.get("preserve_original_identity") is not True:
        fail("third-party icon normalization must preserve original identity")
    if behavior.get("unresolved_icons_inherit") is not True:
        fail("unresolved third-party icons must fall back to inherited themes")

    design_revision = int(cursors.get("design_revision", 0))
    expected_runtime_id = f"{cursors['id']}-r{design_revision}"
    if cursors.get("runtime_id") != expected_runtime_id:
        fail(
            "cursor runtime_id must track design_revision for target-device "
            f"cache busting: expected {expected_runtime_id}"
        )

    supersample = int(cursors.get("supersample", 1))
    if supersample < 4:
        fail("cursor rendering must use at least 4x supersampling")
    animation_frames = int(cursors.get("animation_frames", 1))
    animation_delay = int(cursors.get("animation_delay_ms", 0))
    if animation_frames < 6:
        fail("cursor activity animation must contain at least 6 frames")
    if not 35 <= animation_delay <= 100:
        fail("cursor activity animation delay must remain between 35ms and 100ms")

    expected_sizes = {int(value) for value in cursors["sizes"]}
    if not {24, 32, 48, 64}.issubset(expected_sizes):
        fail("cursor size ladder must cover 24px, 32px, 48px, and 64px")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        icon_out = tmp_path / "icons"
        cursor_out = tmp_path / "cursors"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_icons.py"),
                "--output",
                str(icon_out),
            ],
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_cursors.py"),
                "--output",
                str(cursor_out),
            ],
            check=True,
        )

        icon_root = icon_out / icons["id"]
        cursor_root = cursor_out / cursors["id"]
        if not (icon_root / "index.theme").is_file():
            fail("generated icon theme is missing index.theme")
        if not (cursor_root / "index.theme").is_file():
            fail("generated cursor theme is missing index.theme")

        icon_index = (icon_root / "index.theme").read_text(encoding="utf-8")
        for inherit in icons["inherits"]:
            if inherit not in icon_index:
                fail(f"generated icon theme does not inherit {inherit}")
        for size in normalization["optical_sizes"]:
            rel = f"{size}x{size}/apps"
            if rel not in icon_index:
                fail(f"generated icon theme does not advertise {rel}")
            if not (icon_root / rel).is_dir():
                fail(f"generated icon theme is missing optical directory {rel}")

        svgs = sorted(icon_root.rglob("*.svg"))
        if len(svgs) < int(icons["minimum_generated_icons"]):
            fail(f"generated icon theme contains only {len(svgs)} SVG icons")
        for path in svgs:
            validate_svg(path)

        for required_symbolic in (
            "folder-symbolic.svg",
            "folder-open-symbolic.svg",
            "folder-documents-symbolic.svg",
            "folder-download-symbolic.svg",
            "folder-music-symbolic.svg",
            "folder-pictures-symbolic.svg",
            "folder-videos-symbolic.svg",
            "starred-symbolic.svg",
            "user-home-symbolic.svg",
            "document-open-recent-symbolic.svg",
            "user-trash-symbolic.svg",
            "user-trash-full-symbolic.svg",
        ):
            symbolic_path = (
                icon_root / "scalable" / "places" / required_symbolic
            )
            if not symbolic_path.is_file():
                fail(f"generated icon theme is missing {required_symbolic}")
            validate_line_only_symbolic(symbolic_path)

        identity = ROOT / icons["identity_source"]
        if (
            icon_root / "scalable" / "apps" / "start-here.svg"
        ).read_bytes() != identity.read_bytes():
            fail("start-here icon does not preserve the canonical GoreeCloud mark")

        normalizer = ROOT / "scripts" / "normalize_app_icons.py"
        if not normalizer.is_file():
            fail("missing runtime app icon normalizer")

        fixture_desktop = tmp_path / "desktop-fixture"
        fixture_icons = tmp_path / "hicolor-fixture" / "scalable" / "apps"
        fixture_desktop.mkdir(parents=True)
        fixture_icons.mkdir(parents=True)
        (fixture_desktop / "thirdparty.desktop").write_text(
            "[Desktop Entry]\nType=Application\nName=Third Party\nIcon=thirdparty-test\n",
            encoding="utf-8",
        )
        (fixture_desktop / "goreecloud.desktop").write_text(
            "[Desktop Entry]\nType=Application\nName=GoreeCloud Test\nIcon=goreecloud-test\n",
            encoding="utf-8",
        )
        (fixture_icons / "thirdparty-test.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<circle cx="32" cy="32" r="24" fill="#8844CC"/></svg>',
            encoding="utf-8",
        )
        normalization_report = tmp_path / "normalization-report.json"
        subprocess.run(
            [
                sys.executable,
                str(normalizer),
                "--theme-root",
                str(icon_root),
                "--desktop-root",
                str(fixture_desktop),
                "--icon-root",
                str(tmp_path / "hicolor-fixture"),
                "--report",
                str(normalization_report),
            ],
            check=True,
        )
        report = json.loads(normalization_report.read_text(encoding="utf-8"))
        if report.get("normalized_icon_names") != 1:
            fail("runtime icon normalizer must normalize the safe third-party fixture")
        normalized_names = {
            item.get("icon_name") for item in report.get("normalized", [])
        }
        if normalized_names != {"thirdparty-test"}:
            fail(f"unexpected normalized fixture set: {normalized_names}")
        skipped_names = {
            item.get("icon_name") for item in report.get("skipped", [])
        }
        if "goreecloud-test" not in skipped_names:
            fail("runtime icon normalizer must preserve first-party GoreeCloud identity")

        wrapper_paths = [
            icon_root / "scalable" / "apps" / "thirdparty-test.svg",
            *[
                icon_root / f"{size}x{size}" / "apps" / "thirdparty-test.svg"
                for size in normalization["optical_sizes"]
            ],
        ]
        for wrapper in wrapper_paths:
            if not wrapper.is_file():
                fail(f"runtime icon normalizer is missing wrapper: {wrapper}")
            root = ET.parse(wrapper).getroot()
            images = [
                node for node in root.iter()
                if node.tag.rsplit("}", 1)[-1].lower() == "image"
            ]
            if len(images) != 1:
                fail(f"{wrapper}: normalized wrapper must contain one source image")
            href = images[0].attrib.get("href") or images[0].attrib.get(
                "{http://www.w3.org/1999/xlink}href"
            )
            if not href or href.startswith(("http:", "https:", "file:", "data:", "/")):
                fail(f"{wrapper}: normalized wrapper must reference only a local relative source")
            source = (wrapper.parent / href).resolve()
            icon_root_resolved = icon_root.resolve()
            if source != icon_root_resolved and icon_root_resolved not in source.parents:
                fail(f"{wrapper}: normalized source escapes the icon theme")
            if not source.is_file():
                fail(f"{wrapper}: normalized source file is missing")

        animated_names = set(cursors.get("animated_cursor_names", []))
        cursor_dir = cursor_root / "cursors"
        for name in cursors["required_cursor_names"]:
            path = cursor_dir / name
            if not path.is_file():
                fail(f"generated cursor theme is missing required cursor: {name}")
            animated = name in animated_names
            validate_xcursor(
                path,
                expected_sizes,
                frames_per_size=animation_frames if animated else 1,
                animated=animated,
            )

        palette = cursors["palette"]
        validate_primary_pointer_palette(
            cursor_dir / "left_ptr",
            frost=rgb(palette["frost"]),
            graphite=rgb(palette["graphite"]),
            blue=rgb(palette["primary_blue"]),
        )

    print("GoreeCloud icon and cursor theme validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
