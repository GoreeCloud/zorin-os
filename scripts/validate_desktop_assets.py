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
    if normalization.get("enabled") is not False:
        fail("failed runtime third-party icon wrappers must remain disabled")
    if normalization.get("mode") != "disabled-after-target-visual-failure":
        fail("icon normalization mode must record the target visual failure")
    behavior = normalization.get("behavior", {})
    if behavior.get("runtime_icon_wrappers") is not False:
        fail("runtime third-party icon wrappers must not be generated")
    if behavior.get("modify_desktop_files") or behavior.get("modify_application_packages"):
        fail("icon handling must not modify third-party launchers or packages")
    if behavior.get("preserve_original_identity") is not True:
        fail("third-party original identity preservation must remain required")
    if behavior.get("unresolved_icons_inherit") is not True:
        fail("third-party app icons must continue to inherit when not overridden")

    presentation = icons.get("launcher_presentation", {})
    if presentation.get("enabled") is not True:
        fail("safe launcher tile presentation must remain enabled")
    if presentation.get("mode") != "zorin-menu-grid-app-item":
        fail("launcher presentation must remain on the Zorin Menu grid app-item layer")
    if presentation.get("preserves_original_icon_artwork") is not True:
        fail("launcher presentation must preserve original application artwork")
    if presentation.get("target_selectors") != [".apps-grid .app-item"]:
        fail("launcher presentation must target the verified Zorin Menu app actors")
    if int(presentation.get("padding_px", 0)) != 6:
        fail("Zorin Menu app-item padding must remain 6px")
    if int(presentation.get("spacing_px", 0)) != 6:
        fail("launcher tile spacing must remain 6px")
    if int(presentation.get("radius_px", 0)) != 14:
        fail("Zorin Menu app-item radius must remain 14px")
    if int(presentation.get("focus_ring_px", 0)) < 2:
        fail("launcher tile focus ring must remain at least 2px")

    shell_template = (ROOT / "src" / "gnome-shell" / "gnome-shell.css.in").read_text(
        encoding="utf-8"
    )
    required_shell_fragments = (
        ".overview-tile,\n.grid-search-result {",
        ".apps-grid .app-item {",
        "padding: 6px;",
        "border-radius: 14px;",
        "background-color: {{SHELL_ELEVATED}};",
        "border: 1px solid {{SHELL_BORDER}};",
        "box-shadow: inset 0 0 0 2px {{FOCUS}}, inset 0 1px 0 {{EDGE_LIGHT}};",
        ".calendar-day-base.calendar-today,",
        "background-gradient-start: {{ACCENT}};",
        "background-gradient-end: {{ACCENT}};",
    )
    for fragment in required_shell_fragments:
        if fragment not in shell_template:
            fail(f"launcher presentation CSS is missing required fragment: {fragment}")

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
            if rel in icon_index or (icon_root / rel).exists():
                fail(
                    f"disabled runtime wrappers must not leave an advertised optical directory: {rel}"
                )

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

        # Runtime third-party wrappers are intentionally disabled after
        # representative target visual failure. The base icon theme must keep
        # third-party application artwork on inherited Zorin/Adwaita/hicolor.
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
