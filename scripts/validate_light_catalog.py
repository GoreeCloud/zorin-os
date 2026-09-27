#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "wallpapers.json"
PALETTES = ROOT / "config" / "palettes.json"
EXPECTED_MODE_COUNTS = {"light": 10, "dark": 10, "deep-dark": 10}
EXPECTED_MODE_ORDER = ["light"] * 10 + ["dark"] * 10 + ["deep-dark"] * 10


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    source_catalog = data.get("catalog", [])
    if len(source_catalog) != 30:
        fail(f"Expected 30 source wallpaper entries, found {len(source_catalog)}")

    source_by_id = {item["id"]: item for item in source_catalog}
    if len(source_by_id) != 30:
        fail("Wallpaper source IDs must be unique")

    counts = {
        mode: sum(1 for item in source_catalog if item.get("mode") == mode)
        for mode in EXPECTED_MODE_COUNTS
    }
    if counts != EXPECTED_MODE_COUNTS:
        fail(f"Expected 10 wallpapers in each appearance mode, found {counts}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        rendered = tmp_path / "wallpapers"
        catalog_path = tmp_path / "goreecloud-zorin.xml"

        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_wallpapers.py"),
                "--palette-config",
                str(PALETTES),
                "--output",
                str(rendered),
            ],
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_background_catalog.py"),
                "--manifest",
                str(MANIFEST),
                "--filename-root",
                str(rendered),
                "--output",
                str(catalog_path),
            ],
            check=True,
        )

        nodes = ET.parse(catalog_path).getroot().findall("wallpaper")
        if len(nodes) != 30:
            fail(f"Wallpaper gallery must contain 30 entries, found {len(nodes)}")

        hidden = [node for node in nodes if node.attrib.get("deleted") != "false"]
        if hidden:
            fail(f"All 30 GoreeCloud wallpapers must be visible; found {len(hidden)} hidden entries")

        ordered_modes: list[str] = []
        seen_ids: set[str] = set()
        for node in nodes:
            filename = node.findtext("filename")
            title = node.findtext("name") or ""
            if not filename:
                fail("Wallpaper entry has no filename")
            path = Path(filename)
            if not path.is_file():
                fail(f"Wallpaper file is missing: {path}")
            wallpaper_id = path.stem
            if wallpaper_id in seen_ids:
                fail(f"Duplicate visible wallpaper ID: {wallpaper_id}")
            seen_ids.add(wallpaper_id)
            item = source_by_id.get(wallpaper_id)
            if item is None:
                fail(f"Catalog references unknown wallpaper ID: {wallpaper_id}")
            mode = item["mode"]
            ordered_modes.append(mode)
            expected_label = mode.replace("-", " ").title()
            if expected_label not in title:
                fail(f"Wallpaper title does not expose appearance mode: {title}")

        if seen_ids != set(source_by_id):
            fail("Visible wallpaper IDs differ from the complete 30-wallpaper source catalog")
        if ordered_modes != EXPECTED_MODE_ORDER:
            fail(
                "Wallpaper gallery must remain light-first: 10 Light, then 10 Dark, "
                f"then 10 Deep Dark; got {ordered_modes}"
            )

    print("Light-first wallpaper gallery validation passed: 30 visible (10 Light / 10 Dark / 10 Deep Dark)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
