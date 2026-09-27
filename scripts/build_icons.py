#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "desktop-assets.json"
DEFAULT_OUTPUT = ROOT / "build" / "icons"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the GoreeCloud Zorin icon theme.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def svg(body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">\n'
        '  <defs>\n'
        '    <linearGradient id="frost" x1="0" y1="0" x2="0" y2="1">\n'
        '      <stop stop-color="#FBFDFE"/>\n'
        '      <stop offset="1" stop-color="#DCECF6"/>\n'
        '    </linearGradient>\n'
        '  </defs>\n'
        f'{body}\n'
        '</svg>\n'
    )


def folder_icon(glyph: str = "") -> str:
    return svg(
        '  <path d="M6 18c0-3 2-5 5-5h15l5 6h22c3 0 5 2 5 5v26c0 4-3 7-7 7H13c-4 0-7-3-7-7Z" fill="#8FC4E8" opacity=".5"/>\n'
        '  <path d="M6 23h52v27c0 4-3 7-7 7H13c-4 0-7-3-7-7Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/>\n'
        '  <path d="M10 27h44" stroke="#FFFFFF" stroke-width="2" opacity=".9"/>\n'
        + glyph
    )


def symbolic_folder_icon(opened: bool = False) -> str:
    """Large symbolic folder treatment used by Nautilus empty-state views.

    Nautilus' symbolic pipeline can flatten SVG paint into a monochrome mask.
    Even a nominally unfilled closed path can therefore read as a filled gray
    block after recoloring. Build the empty-state mark from independent line
    segments only: there is no enclosed fill geometry for the symbolic loader
    to turn into a muddy silhouette, while the folder remains recognizable at
    large sizes.
    """
    if opened:
        body = (
            '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
            '    <line x1="10" y1="27" x2="10" y2="19" stroke="#8FC4E8" stroke-width="3"/>\n'
            '    <line x1="10" y1="19" x2="27" y2="19" stroke="#8FC4E8" stroke-width="3"/>\n'
            '    <line x1="27" y1="19" x2="34" y2="26" stroke="#8FC4E8" stroke-width="3"/>\n'
            '    <line x1="34" y1="26" x2="54" y2="26" stroke="#8FC4E8" stroke-width="3"/>\n'
            '    <line x1="54" y1="26" x2="54" y2="31" stroke="#8FC4E8" stroke-width="3"/>\n'
            '    <line x1="13" y1="33" x2="57" y2="33" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="57" y1="33" x2="50" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="50" y1="53" x2="9" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="9" y1="53" x2="13" y2="33" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="18" y1="37" x2="48" y2="37" stroke="#DCECF6" stroke-width="2"/>\n'
            '  </g>\n'
        )
    else:
        body = (
            '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
            '    <line x1="10" y1="51" x2="10" y2="19" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="10" y1="19" x2="27" y2="19" stroke="#8FC4E8" stroke-width="3"/>\n'
            '    <line x1="27" y1="19" x2="34" y2="26" stroke="#8FC4E8" stroke-width="3"/>\n'
            '    <line x1="34" y1="26" x2="54" y2="26" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="54" y1="26" x2="54" y2="51" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="10" y1="51" x2="54" y2="51" stroke="#3B82F6" stroke-width="3"/>\n'
            '    <line x1="10" y1="30" x2="54" y2="30" stroke="#8FC4E8" stroke-width="2.5"/>\n'
            '    <line x1="15" y1="23" x2="25" y2="23" stroke="#DCECF6" stroke-width="2"/>\n'
            '  </g>\n'
        )
    return svg(body)


def symbolic_special_folder_icon(kind: str) -> str:
    """Small-place folder symbolics with distinct XDG-directory semantics.

    Nautilus asks for the *-symbolic names in its sidebar. Keep both the folder
    silhouette and the inner semantic glyph line-only so GTK cannot flatten a
    closed shape into a filled block, while Documents/Downloads/Music/Pictures/
    Videos stop looking like five copies of the generic folder.
    """
    glyphs = {
        "documents": (
            '    <line x1="25" y1="35" x2="40" y2="35" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="25" y1="40" x2="40" y2="40" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="25" y1="45" x2="35" y2="45" stroke="#174EA6" stroke-width="2.5"/>\n'
        ),
        "download": (
            '    <line x1="32" y1="34" x2="32" y2="46" stroke="#174EA6" stroke-width="3"/>\n'
            '    <line x1="26" y1="41" x2="32" y2="47" stroke="#174EA6" stroke-width="3"/>\n'
            '    <line x1="38" y1="41" x2="32" y2="47" stroke="#174EA6" stroke-width="3"/>\n'
        ),
        "music": (
            '    <line x1="36" y1="34" x2="36" y2="45" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="36" y1="34" x2="44" y2="32" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="44" y1="32" x2="44" y2="42" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="30" y1="47" x2="36" y2="45" stroke="#174EA6" stroke-width="3"/>\n'
            '    <line x1="38" y1="44" x2="44" y2="42" stroke="#174EA6" stroke-width="3"/>\n'
        ),
        "pictures": (
            '    <line x1="23" y1="46" x2="29" y2="39" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="29" y1="39" x2="34" y2="44" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="34" y1="44" x2="39" y2="38" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="39" y1="38" x2="45" y2="46" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="42" y1="34" x2="45" y2="34" stroke="#8FC4E8" stroke-width="3"/>\n'
        ),
        "videos": (
            '    <line x1="28" y1="35" x2="28" y2="47" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="28" y1="35" x2="40" y2="41" stroke="#174EA6" stroke-width="2.5"/>\n'
            '    <line x1="40" y1="41" x2="28" y2="47" stroke="#174EA6" stroke-width="2.5"/>\n'
        ),
    }
    if kind not in glyphs:
        raise ValueError(f"unsupported symbolic special folder kind: {kind}")
    return svg(
        '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
        '    <line x1="10" y1="51" x2="10" y2="19" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="10" y1="19" x2="27" y2="19" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="27" y1="19" x2="34" y2="26" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="34" y1="26" x2="54" y2="26" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="54" y1="26" x2="54" y2="51" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="10" y1="51" x2="54" y2="51" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="10" y1="30" x2="54" y2="30" stroke="#8FC4E8" stroke-width="2.5"/>\n'
        + glyphs[kind]
        + '  </g>\n'
    )


def symbolic_star_icon() -> str:
    """Nautilus Starred empty-state icon using the same line-only contract."""
    return svg(
        '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
        '    <line x1="32" y1="9" x2="38" y2="24" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="38" y1="24" x2="54" y2="25" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="54" y1="25" x2="42" y2="35" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="42" y1="35" x2="46" y2="51" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="46" y1="51" x2="32" y2="42" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="32" y1="42" x2="18" y2="51" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="18" y1="51" x2="22" y2="35" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="22" y1="35" x2="10" y2="25" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="10" y1="25" x2="26" y2="24" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="26" y1="24" x2="32" y2="9" stroke="#8FC4E8" stroke-width="3"/>\n'
        '  </g>\n'
    )


def symbolic_home_icon() -> str:
    return svg(
        '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
        '    <line x1="10" y1="31" x2="32" y2="12" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="32" y1="12" x2="54" y2="31" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="14" y1="28" x2="14" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="50" y1="28" x2="50" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="14" y1="53" x2="50" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="27" y1="53" x2="27" y2="39" stroke="#3B82F6" stroke-width="2.5"/>\n'
        '    <line x1="27" y1="39" x2="37" y2="39" stroke="#DCECF6" stroke-width="2.5"/>\n'
        '    <line x1="37" y1="39" x2="37" y2="53" stroke="#3B82F6" stroke-width="2.5"/>\n'
        '  </g>\n'
    )


def symbolic_recent_icon() -> str:
    return svg(
        '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
        '    <line x1="32" y1="10" x2="46" y2="15" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="46" y1="15" x2="54" y2="29" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="54" y1="29" x2="49" y2="44" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="49" y1="44" x2="35" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="35" y1="53" x2="20" y2="49" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="20" y1="49" x2="11" y2="35" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="11" y1="35" x2="15" y2="20" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="15" y1="20" x2="32" y2="10" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="32" y1="19" x2="32" y2="33" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="32" y1="33" x2="42" y2="38" stroke="#3B82F6" stroke-width="3"/>\n'
        '  </g>\n'
    )


def symbolic_trash_icon(full: bool = False) -> str:
    body = (
        '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
        '    <line x1="17" y1="19" x2="47" y2="19" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="26" y1="12" x2="38" y2="12" stroke="#8FC4E8" stroke-width="3"/>\n'
        '    <line x1="21" y1="24" x2="23" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="43" y1="24" x2="41" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="23" y1="53" x2="41" y2="53" stroke="#3B82F6" stroke-width="3"/>\n'
        '    <line x1="29" y1="29" x2="29" y2="46" stroke="#DCECF6" stroke-width="2.5"/>\n'
        '    <line x1="35" y1="29" x2="35" y2="46" stroke="#DCECF6" stroke-width="2.5"/>\n'
    )
    if full:
        body += (
            '    <line x1="26" y1="31" x2="38" y2="44" stroke="#3B82F6" stroke-width="2.5"/>\n'
            '    <line x1="38" y1="31" x2="26" y2="44" stroke="#3B82F6" stroke-width="2.5"/>\n'
        )
    body += '  </g>\n'
    return svg(body)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))["icon_theme"]
    theme = args.output.expanduser().resolve() / cfg["id"]
    if theme.exists():
        shutil.rmtree(theme)

    dirs = {
        "places": theme / "scalable" / "places",
        "devices": theme / "scalable" / "devices",
        "apps": theme / "scalable" / "apps",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    normalization = cfg.get("normalization", {})
    optical_sizes = (
        [int(value) for value in normalization.get("optical_sizes", [])]
        if normalization.get("enabled") is True
        else []
    )
    optical_app_dirs = [f"{size}x{size}/apps" for size in optical_sizes]
    for rel in optical_app_dirs:
        (theme / rel).mkdir(parents=True, exist_ok=True)

    inherits = ",".join(cfg["inherits"])
    theme_directories = [
        "scalable/places",
        "scalable/devices",
        "scalable/apps",
        *optical_app_dirs,
    ]
    index = (
        "[Icon Theme]\n"
        f"Name={cfg['name']}\n"
        f"Comment={cfg['comment']}\n"
        f"Inherits={inherits}\n"
        "Example=folder\n"
        f"Directories={','.join(theme_directories)}\n\n"
        "[scalable/places]\nSize=64\nType=Scalable\nMinSize=16\nMaxSize=512\nContext=Places\n\n"
        "[scalable/devices]\nSize=64\nType=Scalable\nMinSize=16\nMaxSize=512\nContext=Devices\n\n"
        "[scalable/apps]\nSize=64\nType=Scalable\nMinSize=16\nMaxSize=512\nContext=Applications\n\n"
    )
    for size, rel in zip(optical_sizes, optical_app_dirs):
        index += (
            f"[{rel}]\n"
            f"Size={size}\n"
            "Type=Fixed\n"
            "Context=Applications\n\n"
        )
    write(theme / "index.theme", index)

    place_icons = {
        "folder": folder_icon(),
        "folder-symbolic": symbolic_folder_icon(),
        "folder-open-symbolic": symbolic_folder_icon(opened=True),
        "folder-documents-symbolic": symbolic_special_folder_icon("documents"),
        "folder-download-symbolic": symbolic_special_folder_icon("download"),
        "folder-music-symbolic": symbolic_special_folder_icon("music"),
        "folder-pictures-symbolic": symbolic_special_folder_icon("pictures"),
        "folder-videos-symbolic": symbolic_special_folder_icon("videos"),
        "starred-symbolic": symbolic_star_icon(),
        "user-home-symbolic": symbolic_home_icon(),
        "document-open-recent-symbolic": symbolic_recent_icon(),
        "user-trash-symbolic": symbolic_trash_icon(),
        "user-trash-full-symbolic": symbolic_trash_icon(full=True),
        "folder-documents": folder_icon('  <path d="M25 32h15v16H25z" fill="#FFFFFF" stroke="#174EA6" stroke-width="1.5"/><path d="M28 36h9M28 40h9M28 44h7" stroke="#3B82F6" stroke-width="1.5" stroke-linecap="round"/>'),
        "folder-download": folder_icon('  <path d="M32 31v13m-6-5 6 6 6-6" fill="none" stroke="#174EA6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'),
        "folder-music": folder_icon('  <path d="M38 31v13c0 4-7 5-7 1 0-3 4-4 7-3V34l9-2v10c0 4-7 5-7 1 0-3 4-4 7-3V29Z" fill="#174EA6"/>'),
        "folder-pictures": folder_icon('  <rect x="23" y="31" width="22" height="16" rx="2" fill="#FFFFFF" stroke="#174EA6" stroke-width="1.5"/><circle cx="39" cy="35" r="2" fill="#3B82F6"/><path d="m25 44 6-6 4 4 3-3 5 5" fill="none" stroke="#3B82F6" stroke-width="2"/>'),
        "folder-videos": folder_icon('  <rect x="24" y="32" width="20" height="15" rx="3" fill="#FFFFFF" stroke="#174EA6" stroke-width="1.5"/><path d="m32 36 7 4-7 4Z" fill="#3B82F6"/>'),
        "user-home": svg('  <path d="M10 31 32 12l22 19v21a5 5 0 0 1-5 5H15a5 5 0 0 1-5-5Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M25 57V39h14v18" fill="#DCECF6" stroke="#174EA6" stroke-width="2"/>'),
        "user-desktop": svg('  <rect x="7" y="10" width="50" height="35" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M23 54h18M28 43v9m8-9v9" stroke="#174EA6" stroke-width="2.5" stroke-linecap="round"/>'),
        "user-trash": svg('  <path d="M18 20h28l-2 36H20Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M15 17h34M26 12h12" stroke="#174EA6" stroke-width="3" stroke-linecap="round"/>'),
        "user-trash-full": svg('  <path d="M18 20h28l-2 36H20Z" fill="#DCECF6" stroke="#3B82F6" stroke-width="2"/><path d="M15 17h34M26 12h12" stroke="#174EA6" stroke-width="3" stroke-linecap="round"/><path d="m25 29 14 17M39 29 25 46" stroke="#3B82F6" stroke-width="2.5"/>'),
    }
    for name, content in place_icons.items():
        write(dirs["places"] / f"{name}.svg", content)

    device_icons = {
        "drive-harddisk": svg('  <rect x="8" y="13" width="48" height="38" rx="8" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M14 39h36" stroke="#8FC4E8" stroke-width="2"/><circle cx="47" cy="45" r="3" fill="#3B82F6"/>'),
        "drive-removable-media": svg('  <rect x="13" y="9" width="38" height="46" rx="8" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><rect x="21" y="16" width="22" height="17" rx="3" fill="#DCECF6" stroke="#174EA6" stroke-width="1.5"/><circle cx="32" cy="45" r="4" fill="#3B82F6"/>'),
        "network-server": svg('  <rect x="9" y="9" width="46" height="18" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><rect x="9" y="37" width="46" height="18" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><circle cx="46" cy="18" r="3" fill="#3B82F6"/><circle cx="46" cy="46" r="3" fill="#3B82F6"/>'),
        "computer": svg('  <rect x="7" y="9" width="50" height="34" rx="5" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M22 55h20M28 43v12m8-12v12" stroke="#174EA6" stroke-width="2.5" stroke-linecap="round"/>'),
        "phone": svg('  <rect x="19" y="5" width="26" height="54" rx="7" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><circle cx="32" cy="52" r="2" fill="#174EA6"/>'),
        "media-flash": svg('  <path d="M23 6h18v12h6v37a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4V18h6Z" fill="url(#frost)" stroke="#3B82F6" stroke-width="2"/><path d="M27 6v12m10-12v12" stroke="#174EA6" stroke-width="2"/>'),
    }
    for name, content in device_icons.items():
        write(dirs["devices"] / f"{name}.svg", content)

    identity = ROOT / cfg["identity_source"]
    if not identity.is_file():
        raise SystemExit(f"Missing canonical GoreeCloud mark: {identity}")
    shutil.copyfile(identity, dirs["apps"] / "start-here.svg")
    shutil.copyfile(identity, dirs["apps"] / "goreecloud.svg")

    print(f"Built GoreeCloud icon theme: {theme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
