#!/usr/bin/env python3
from __future__ import annotations

import argparse
import configparser
import json
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "desktop-assets.json"
ICON_NAME_RE = re.compile(r"^[A-Za-z0-9_.+@-]+$")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@dataclass(frozen=True)
class DesktopIcon:
    desktop_id: str
    icon_name: str


@dataclass(frozen=True)
class SourceIcon:
    path: Path
    extension: str
    score: tuple[int, int, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize third-party application icons into the GoreeCloud Zorin "
            "icon theme without modifying application packages or .desktop files."
        )
    )
    parser.add_argument("--theme-root", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--desktop-root", action="append", type=Path, default=[])
    parser.add_argument("--icon-root", action="append", type=Path, default=[])
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def expand(path: str | Path) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(str(path)))).resolve()


def default_desktop_roots() -> list[Path]:
    data_home = expand(os.environ.get("XDG_DATA_HOME", "~/.local/share"))
    return [
        data_home / "applications",
        Path("/usr/local/share/applications"),
        Path("/usr/share/applications"),
        expand("~/.local/share/flatpak/exports/share/applications"),
        Path("/var/lib/flatpak/exports/share/applications"),
        Path("/var/lib/snapd/desktop/applications"),
    ]


def default_icon_roots() -> list[Path]:
    data_home = expand(os.environ.get("XDG_DATA_HOME", "~/.local/share"))
    return [
        data_home / "icons/hicolor",
        Path("/usr/local/share/icons/hicolor"),
        Path("/usr/share/icons/hicolor"),
        data_home / "flatpak/exports/share/icons/hicolor",
        Path("/var/lib/flatpak/exports/share/icons/hicolor"),
        Path("/var/lib/snapd/desktop/icons"),
        Path("/usr/local/share/pixmaps"),
        Path("/usr/share/pixmaps"),
    ]


def desktop_truth(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def desktop_entries(
    roots: list[Path],
    skip_prefixes: tuple[str, ...],
) -> tuple[list[DesktopIcon], list[dict[str, str]]]:
    seen: set[tuple[str, str]] = set()
    entries: list[DesktopIcon] = []
    skipped: list[dict[str, str]] = []

    for root in roots:
        if not root.is_dir():
            continue
        for desktop in sorted(root.glob("*.desktop")):
            parser = configparser.ConfigParser(interpolation=None, strict=False)
            parser.optionxform = str
            try:
                parser.read(desktop, encoding="utf-8")
            except (OSError, UnicodeError, configparser.Error):
                skipped.append({"desktop_id": desktop.name, "status": "unreadable-desktop"})
                continue
            if "Desktop Entry" not in parser:
                continue
            section = parser["Desktop Entry"]
            if section.get("Type", "Application") != "Application":
                continue
            if desktop_truth(section.get("Hidden")) or desktop_truth(section.get("NoDisplay")):
                continue
            icon = (section.get("Icon") or "").strip()
            if not icon:
                skipped.append({"desktop_id": desktop.name, "status": "missing-icon"})
                continue
            if icon.startswith(("/", "./", "../")) or "/" in icon:
                skipped.append({
                    "desktop_id": desktop.name,
                    "icon_name": icon,
                    "status": "path-icon-not-theme-overridable",
                })
                continue
            suffix = Path(icon).suffix.lower()
            icon_name = Path(icon).stem if suffix in {".svg", ".png", ".xpm"} else icon
            if not ICON_NAME_RE.fullmatch(icon_name):
                skipped.append({
                    "desktop_id": desktop.name,
                    "icon_name": icon_name,
                    "status": "unsafe-icon-name",
                })
                continue
            lowered = icon_name.lower()
            if any(lowered.startswith(prefix) for prefix in skip_prefixes):
                skipped.append({
                    "desktop_id": desktop.name,
                    "icon_name": icon_name,
                    "status": "first-party-or-protected-prefix",
                })
                continue
            key = (desktop.name, icon_name)
            if key not in seen:
                seen.add(key)
                entries.append(DesktopIcon(desktop.name, icon_name))
    return entries, skipped


def source_score(path: Path) -> tuple[int, int, str]:
    suffix = path.suffix.lower()
    vector = 0 if suffix == ".svg" else 1
    size_score = 999
    for part in path.parts:
        match = re.fullmatch(r"(\d+)x(\d+)", part)
        if match and match.group(1) == match.group(2):
            size = int(match.group(1))
            size_score = abs(256 - size)
            break
        if part == "scalable":
            size_score = 0
            break
    return (vector, size_score, str(path))


def build_source_index(
    roots: list[Path],
    theme_root: Path,
) -> dict[str, list[SourceIcon]]:
    index: dict[str, list[SourceIcon]] = {}
    theme_root = theme_root.resolve()
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".svg", ".png"}:
                continue
            try:
                resolved = path.resolve()
            except OSError:
                continue
            if resolved == theme_root or theme_root in resolved.parents:
                continue
            name = path.stem
            if not ICON_NAME_RE.fullmatch(name):
                continue
            source = SourceIcon(
                path=resolved,
                extension=path.suffix.lower(),
                score=source_score(path),
            )
            index.setdefault(name, []).append(source)
    for candidates in index.values():
        candidates.sort(key=lambda item: item.score)
    return index


def validate_svg_source(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f"invalid-svg:{exc}") from exc
    for node in root.iter():
        local = node.tag.rsplit("}", 1)[-1].lower()
        if local in {"script", "foreignobject"}:
            raise ValueError(f"unsafe-svg-element:{local}")
        for attr, value in node.attrib.items():
            attr_name = attr.rsplit("}", 1)[-1].lower()
            if attr_name in {"href", "src"} and str(value).strip().lower().startswith(
                ("http:", "https:", "file:", "data:", "//")
            ):
                raise ValueError("unsafe-svg-resource")
    return data


def validate_png_source(path: Path) -> bytes:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("invalid-png-signature")
    if len(data) < 32:
        raise ValueError("invalid-png-size")
    return data


def load_source(path: Path) -> bytes:
    if path.suffix.lower() == ".svg":
        return validate_svg_source(path)
    if path.suffix.lower() == ".png":
        return validate_png_source(path)
    raise ValueError("unsupported-format")


def normalized_svg(
    source_rel: str,
    canvas: int,
    presentation_inset: int,
    content_inset: int,
    plate_radius: int,
    palette: dict[str, str],
) -> str:
    plate_size = canvas - presentation_inset * 2
    content_size = canvas - content_inset * 2
    shadow_y = max(1, canvas // 128)
    outline_width = max(1, canvas // 96)
    highlight_width = max(1, canvas // 128)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{canvas}" height="{canvas}" viewBox="0 0 {canvas} {canvas}">
  <title>Glaze-normalized third-party application icon</title>
  <desc>Original application identity preserved inside a GoreeCloud Glaze presentation plate.</desc>
  <defs>
    <linearGradient id="gcPlate" x1="0" y1="0" x2="0" y2="1">
      <stop stop-color="{palette["plate_top"]}"/>
      <stop offset="1" stop-color="{palette["plate_bottom"]}"/>
    </linearGradient>
  </defs>
  <rect x="{presentation_inset}" y="{presentation_inset + shadow_y}" width="{plate_size}" height="{plate_size}" rx="{plate_radius}" fill="{palette["shadow"]}" opacity="{palette["shadow_opacity"]}"/>
  <rect x="{presentation_inset}" y="{presentation_inset}" width="{plate_size}" height="{plate_size}" rx="{plate_radius}" fill="url(#gcPlate)" stroke="{palette["outline"]}" stroke-width="{outline_width}" stroke-opacity="{palette["outline_opacity"]}"/>
  <rect x="{presentation_inset + highlight_width}" y="{presentation_inset + highlight_width}" width="{plate_size - highlight_width * 2}" height="{plate_size - highlight_width * 2}" rx="{max(1, plate_radius - highlight_width)}" fill="none" stroke="{palette["highlight"]}" stroke-width="{highlight_width}" stroke-opacity="{palette["highlight_opacity"]}"/>
  <image x="{content_inset}" y="{content_inset}" width="{content_size}" height="{content_size}" preserveAspectRatio="xMidYMid meet" href="{source_rel}" xlink:href="{source_rel}"/>
</svg>
'''


def target_directories(
    theme_root: Path,
    sizes: list[int],
) -> list[tuple[Path, int]]:
    targets: list[tuple[Path, int]] = [(theme_root / "scalable/apps", 1024)]
    for size in sizes:
        targets.append((theme_root / f"{size}x{size}/apps", size))
    return targets


def scale_value(value: int, canvas: int, target: int) -> int:
    return max(1, round(value * target / canvas))


def write_wrapper_set(
    theme_root: Path,
    icon_name: str,
    source: SourceIcon,
    source_bytes: bytes,
    config: dict[str, object],
    dry_run: bool,
) -> int:
    sizes = [int(v) for v in config["optical_sizes"]]
    canvas = int(config["canvas"])
    presentation_inset = int(config["presentation_inset"])
    content_inset = int(config["content_inset"])
    plate_radius = int(config["plate_radius"])
    palette = dict(config["palette"])

    source_dir = theme_root / "scalable/apps/.goreecloud-source"
    source_name = f"{icon_name}{source.extension}"
    source_path = source_dir / source_name
    wrapper_count = 0

    if not dry_run:
        source_dir.mkdir(parents=True, exist_ok=True)
        source_path.write_bytes(source_bytes)

    for directory, target_canvas in target_directories(theme_root, sizes):
        if target_canvas == 1024:
            rel = ".goreecloud-source/" + source_name
            p_inset = presentation_inset
            c_inset = content_inset
            radius = plate_radius
        else:
            rel = os.path.relpath(source_path, directory).replace(os.sep, "/")
            p_inset = scale_value(presentation_inset, canvas, target_canvas)
            compact_adjust = -max(0, round(target_canvas * 0.025)) if target_canvas <= 32 else 0
            c_inset = max(
                p_inset + 1,
                scale_value(content_inset, canvas, target_canvas) + compact_adjust,
            )
            radius = scale_value(plate_radius, canvas, target_canvas)

        content = normalized_svg(
            rel,
            target_canvas,
            p_inset,
            c_inset,
            radius,
            palette,
        )
        if not dry_run:
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"{icon_name}.svg").write_text(content, encoding="utf-8")
        wrapper_count += 1
    return wrapper_count


def main() -> int:
    args = parse_args()
    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    normalization = cfg["icon_theme"].get("normalization", {})
    if not normalization.get("enabled"):
        raise SystemExit("Icon normalization is disabled by config")

    theme_root = args.theme_root.expanduser().resolve()
    if not (theme_root / "index.theme").is_file():
        raise SystemExit(f"Icon theme root is missing index.theme: {theme_root}")

    desktop_roots = [expand(p) for p in args.desktop_root] or default_desktop_roots()
    icon_roots = [expand(p) for p in args.icon_root] or default_icon_roots()
    skip_prefixes = tuple(
        str(v).lower() for v in normalization.get("skip_prefixes", [])
    )
    protected_names = {
        str(v) for v in normalization.get("protected_icon_names", [])
    }

    entries, skipped = desktop_entries(desktop_roots, skip_prefixes)
    source_index = build_source_index(icon_roots, theme_root)
    app_dir = theme_root / "scalable/apps"

    normalized: list[dict[str, str]] = []
    unresolved: list[dict[str, str]] = []
    seen_names: set[str] = set()
    wrapper_total = 0

    for entry in entries:
        if entry.icon_name in seen_names:
            continue
        seen_names.add(entry.icon_name)
        if (
            entry.icon_name in protected_names
            or (app_dir / f"{entry.icon_name}.svg").exists()
        ):
            skipped.append({
                "desktop_id": entry.desktop_id,
                "icon_name": entry.icon_name,
                "status": "protected-or-first-party-override",
            })
            continue

        candidates = source_index.get(entry.icon_name, [])
        source = candidates[0] if candidates else None
        if source is None:
            unresolved.append({
                "desktop_id": entry.desktop_id,
                "icon_name": entry.icon_name,
                "status": "source-not-found",
            })
            continue
        try:
            source_bytes = load_source(source.path)
        except (OSError, ValueError) as exc:
            unresolved.append({
                "desktop_id": entry.desktop_id,
                "icon_name": entry.icon_name,
                "status": f"source-rejected:{exc}",
            })
            continue

        wrapper_total += write_wrapper_set(
            theme_root,
            entry.icon_name,
            source,
            source_bytes,
            normalization,
            args.dry_run,
        )
        normalized.append({
            "desktop_id": entry.desktop_id,
            "icon_name": entry.icon_name,
            "source_file": source.path.name,
            "source_format": source.extension.lstrip("."),
            "status": "normalized",
        })

    report = {
        "schema_version": 1,
        "mode": normalization.get("mode"),
        "normalized_icon_names": len(normalized),
        "generated_wrappers": wrapper_total,
        "unresolved_icon_names": len(unresolved),
        "skipped_entries": len(skipped),
        "normalized": normalized,
        "unresolved": unresolved,
        "skipped": skipped,
    }
    report_path = args.report or (
        theme_root / "goreecloud-normalization-report.json"
    )
    if not args.dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )

    print(
        "GoreeCloud icon normalization: "
        f"{len(normalized)} icon names normalized, "
        f"{len(unresolved)} unresolved, {len(skipped)} skipped"
    )
    if normalized:
        print(
            "Normalized examples: "
            + ", ".join(item["icon_name"] for item in normalized[:12])
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
