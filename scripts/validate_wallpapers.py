#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "wallpapers.json"
PALETTES = ROOT / "config" / "palettes.json"

EXPECTED_CATEGORIES = {
    "Atmosphere",
    "Terrain",
    "Celestial",
    "Architecture",
    "Digital",
}
EXPECTED_MODES = {"light", "dark", "deep-dark"}
EXPECTED_TOTAL = 30
EXPECTED_PER_MODE = 10
EXPECTED_PER_CATEGORY = 6
EXPECTED_FAMILIES_PER_CATEGORY = 2

FORBIDDEN_WALLPAPER_TOKENS = {
    "{{accent}}",
    "{{accent2}}",
    "{{accent_hover}}",
    "{{accent_soft}}",
    "{{soft}}",
    "{{on}}",
    "{{on_accent}}",
    "{{selection}}",
    "{{amber}}",
    "{{atmosphere_amber}}",
    "{{destructive}}",
    "{{destructive_hover}}",
    "{{success}}",
    "{{warning}}",
    "{{information}}",
    "{{focus}}",
}
LEGACY_IDENTITY_TOKENS = {"{{identity_inner}}", "{{identity_viewbox}}", "{{identity_asset_id}}"}


def fail(message: str) -> None:
    raise SystemExit(message)


def validate_safe_svg(path: Path, label: str) -> ET.Element:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{label}: invalid SVG XML: {exc}")
    if not root.tag.endswith("svg"):
        fail(f"{label}: root element is not SVG")
    for element in root.iter():
        local_name = element.tag.rsplit("}", 1)[-1].lower()
        if local_name == "script":
            fail(f"{label}: script content is prohibited")
        for attr, value in element.attrib.items():
            attr_name = attr.rsplit("}", 1)[-1].lower()
            if attr_name == "href" and value.startswith(("http://", "https://", "data:", "file:")):
                fail(f"{label}: external/embedded href is prohibited")
    return root


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    palettes = json.loads(PALETTES.read_text(encoding="utf-8"))
    palette_by_id = {variant["id"]: variant for variant in palettes["variants"]}

    if data.get("schema_version") != 4:
        fail("Wallpaper manifest schema_version must be 4 for the Glaze Originals catalog")

    design = data.get("design_system", {})
    if design.get("name") != "Glaze UI" or design.get("version") != "1.6.0":
        fail("Wallpaper collection must target GLAZE UI V1.6 / 1.6.0")
    if design.get("lifecycle") != "anchor":
        fail("Wallpaper collection must remain pinned to the V1.6 Official Anchor")

    collection = data.get("collection", {})
    catalog = data.get("catalog", [])
    primary = data.get("wallpapers", [])

    if collection.get("total") != EXPECTED_TOTAL or collection.get("minimum_total") != EXPECTED_TOTAL:
        fail("Wallpaper collection total and minimum_total must both be exactly 30")
    if len(catalog) != EXPECTED_TOTAL:
        fail(f"Wallpaper catalog must contain exactly 30 entries, found {len(catalog)}")
    if len(primary) != 3:
        fail("Primary wallpaper compatibility set must contain exactly three entries")

    categories = {item.get("category") for item in catalog}
    if categories != EXPECTED_CATEGORIES:
        fail(f"Wallpaper categories mismatch: {sorted(categories)}")

    category_counts = Counter(item["category"] for item in catalog)
    if any(category_counts[category] != EXPECTED_PER_CATEGORY for category in EXPECTED_CATEGORIES):
        fail(f"Each category must contain exactly 6 variants: {dict(category_counts)}")

    mode_counts = Counter(item["mode"] for item in catalog)
    if any(mode_counts[mode] != EXPECTED_PER_MODE for mode in EXPECTED_MODES):
        fail(f"Each appearance mode must contain exactly 10 wallpapers: {dict(mode_counts)}")

    ids = [item["id"] for item in catalog]
    if len(ids) != len(set(ids)):
        fail("Duplicate wallpaper IDs found")

    family_modes: dict[tuple[str, str], set[str]] = defaultdict(set)
    category_families: dict[str, set[str]] = defaultdict(set)
    active_sources: set[str] = set()

    required = {
        "id", "category", "family", "mode", "theme_id", "file",
        "canvas", "accent", "accent_soft", "atmosphere_amber", "role",
        "art_direction", "source", "generated",
    }

    for item in catalog:
        missing = required - set(item)
        if missing:
            fail(f"{item.get('id', '<unknown>')}: missing keys: {sorted(missing)}")
        if item["mode"] not in EXPECTED_MODES:
            fail(f"{item['id']}: invalid mode {item['mode']}")
        if item["role"] != "glaze-native-environmental-wallpaper":
            fail(f"{item['id']}: wallpaper role must be Glaze-native environmental artwork")
        if item["art_direction"] != "Glaze UI V1.6 environmental illustration":
            fail(f"{item['id']}: unexpected art direction")

        palette = palette_by_id.get(item["theme_id"])
        if palette is None:
            fail(f"{item['id']}: unknown theme_id {item['theme_id']}")
        if item["mode"] != palette["mode"]:
            fail(f"{item['id']}: mode does not match theme palette")

        for key in ("canvas", "accent", "accent_soft", "atmosphere_amber"):
            if item[key] != palette[key]:
                fail(f"{item['id']}: {key} does not match {item['theme_id']}")

        source = ROOT / item["source"]
        if not source.is_file():
            fail(f"{item['id']}: missing repository source {item['source']}")
        if not item.get("generated") or not item["source"].endswith(".svg.in"):
            fail(f"{item['id']}: wallpaper must use a generated .svg.in template")

        template = source.read_text(encoding="utf-8")
        forbidden = sorted(token for token in FORBIDDEN_WALLPAPER_TOKENS if token in template)
        if forbidden:
            fail(
                f"{item['id']}: wallpaper source consumes semantic UI token(s): "
                + ", ".join(forbidden)
            )
        legacy = sorted(token for token in LEGACY_IDENTITY_TOKENS if token in template)
        if legacy:
            fail(
                f"{item['id']}: wallpaper source still depends on legacy logo-derived token(s): "
                + ", ".join(legacy)
            )

        family_modes[(item["category"], item["family"])].add(item["mode"])
        category_families[item["category"]].add(item["family"])
        active_sources.add(item["source"])

    if len(active_sources) != 10:
        fail(f"Wallpaper collection must use exactly 10 distinct compositions, found {len(active_sources)}")

    for category in EXPECTED_CATEGORIES:
        if len(category_families[category]) != EXPECTED_FAMILIES_PER_CATEGORY:
            fail(
                f"{category}: expected exactly two wallpaper families, "
                f"found {sorted(category_families[category])}"
            )

    for key, modes in family_modes.items():
        if modes != EXPECTED_MODES:
            fail(f"{key}: family must provide Light, Dark, and Deep Dark; got {sorted(modes)}")

    primary_ids = {item["id"] for item in primary}
    catalog_ids = set(ids)
    if not primary_ids <= catalog_ids:
        fail("Primary wallpaper entries must also exist in the full catalog")
    if {item["mode"] for item in primary} != EXPECTED_MODES:
        fail("Primary wallpaper set must cover Light, Dark, and Deep Dark")
    if {item["family"] for item in primary} != {"Cirrus"}:
        fail("Primary wallpaper family must be Atmosphere — Cirrus")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        rendered = tmp_path / "rendered"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_wallpapers.py"), "--output", str(rendered)],
            check=True,
        )

        files = sorted(rendered.glob("*.svg"))
        if len(files) != EXPECTED_TOTAL:
            fail(f"Wallpaper renderer must produce exactly 30 SVG files, found {len(files)}")

        for item in catalog:
            path = rendered / f"{item['id']}.svg"
            if not path.is_file():
                fail(f"{item['id']}: rendered wallpaper is missing")
            svg = validate_safe_svg(path, item["id"])
            if svg.attrib.get("width") != "3840" or svg.attrib.get("height") != "2160":
                fail(f"{item['id']}: native size must be 3840x2160")
            if svg.attrib.get("viewBox") != "0 0 3840 2160":
                fail(f"{item['id']}: viewBox must be 0 0 3840 2160")

        catalog_path = tmp_path / "goreecloud-zorin.xml"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_background_catalog.py"),
                "--manifest", str(MANIFEST),
                "--filename-root", str(rendered),
                "--output", str(catalog_path),
            ],
            check=True,
        )
        nodes = ET.parse(catalog_path).getroot().findall("wallpaper")
        if len(nodes) != EXPECTED_TOTAL:
            fail("Generated GNOME background catalog must contain exactly 30 entries")
        hidden = [node for node in nodes if node.attrib.get("deleted") != "false"]
        if hidden:
            fail(f"All 30 Glaze Originals must be visible in Settings; found {len(hidden)} hidden")

    print(
        "Wallpaper collection validation passed: "
        f"30 Glaze-native assets, 5 categories, 10 families, {dict(mode_counts)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
