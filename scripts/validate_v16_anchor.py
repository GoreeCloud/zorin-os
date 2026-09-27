#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTES = ROOT / "config" / "palettes.json"
EXPECTED_MODES = {"light", "dark", "deep-dark"}
EXPECTED_UPSTREAM_SOURCE = "a7180679ea851389e0f3004515f9a25f420e716d"
EXPECTED_QUALIFICATION_ANCHOR = "c7509c79256b04b0aa67cb9dd0737d7588e0ae4a"
REQUIRED = {
    "id", "display_name", "mode", "gtk_base_import", "canvas", "surface",
    "elevated", "deep", "text", "muted", "border", "accent", "accent_hover",
    "accent_soft", "focus", "on_accent", "selection", "success", "on_success",
    "warning", "on_warning", "information", "on_information", "destructive",
    "destructive_hover", "atmosphere_amber", "frost", "edge_light",
    "atmosphere", "shell_panel", "shell_surface", "shell_elevated",
    "shell_border", "shell_hover", "shell_active", "shell_shadow",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def srgb_channel(value: int) -> float:
    c = value / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def luminance(value: str) -> float:
    if len(value) != 7 or not value.startswith("#"):
        fail(f"Contrast validation requires #RRGGBB, got {value!r}")
    rgb = [int(value[i:i + 2], 16) for i in (1, 3, 5)]
    r, g, b = (srgb_channel(channel) for channel in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def require_contrast(label: str, foreground: str, background: str, minimum: float) -> None:
    ratio = contrast(foreground, background)
    if ratio < minimum:
        fail(f"{label}: contrast {ratio:.2f} < {minimum:.1f}")


def main() -> int:
    data = json.loads(PALETTES.read_text(encoding="utf-8"))
    design = data.get("design_system", {})
    contract = data.get("desktop_contract", {})

    if data.get("schema_version") != 1:
        fail("Canonical palette schema_version must be 1")
    if design.get("name") != "Glaze UI" or design.get("version") != "1.6.0":
        fail("Canonical desktop palette must target GLAZE UI V1.6 / 1.6.0")
    if design.get("lifecycle") != "anchor" or design.get("consumer_eligible") is not True:
        fail("Canonical palette must record the consumer-eligible V1.6 Official Anchor")
    if design.get("upstream_repository") != "GoreeCloud/glaze-ui":
        fail("Canonical palette must identify GoreeCloud/glaze-ui as upstream authority")
    if design.get("upstream_release_tag") != "v1.6.0":
        fail("Canonical palette must pin upstream release tag v1.6.0")
    if design.get("upstream_accepted_release_source") != EXPECTED_UPSTREAM_SOURCE:
        fail("Canonical palette upstream accepted-release source pin changed unexpectedly")
    if design.get("upstream_source_qualification_anchor") != EXPECTED_QUALIFICATION_ANCHOR:
        fail("Canonical palette upstream qualification anchor changed unexpectedly")
    if design.get("target") != "Zorin OS 17.3":
        fail("Canonical palette must remain scoped to the verified Zorin OS 17.3 target")

    expected_contract = {
        "reading_surfaces": "solid",
        "transient_chrome": "bounded-glaze-with-solid-fallback",
        "unsupported_backdrop_fallback": "solid-or-raised",
        "reduced_transparency_fallback": "solid-or-raised",
        "performance_degradation": "reduce-backdrop-before-hierarchy",
        "focus_ring_minimum_px": 2,
        "pointer_compact_minimum_px": 32,
        "coarse_interactive_minimum_px": 44,
        "color_only_status_allowed": False,
        "nested_backdrop_stacks_allowed": False,
    }
    for key, expected in expected_contract.items():
        if contract.get(key) != expected:
            fail(f"desktop_contract.{key} must be {expected!r}, got {contract.get(key)!r}")

    variants = data.get("variants", [])
    if len(variants) != 3:
        fail("Canonical palette must define exactly three Zorin appearance variants")
    if {variant.get("mode") for variant in variants} != EXPECTED_MODES:
        fail("Canonical palette must define Light, Dark, and Deep Dark")

    for variant in variants:
        mode = variant["mode"]
        missing = REQUIRED - set(variant)
        if missing:
            fail(f"{variant.get('id', mode)}: missing V1.6 desktop tokens: {sorted(missing)}")

        require_contrast(f"{variant['id']} primary text/canvas", variant["text"], variant["canvas"], 7.0)
        require_contrast(f"{variant['id']} muted text/canvas", variant["muted"], variant["canvas"], 4.5)
        require_contrast(f"{variant['id']} on-accent/accent", variant["on_accent"], variant["accent"], 4.5)
        require_contrast(f"{variant['id']} focus/canvas", variant["focus"], variant["canvas"], 3.0)
        require_contrast(f"{variant['id']} selected text/selection", variant["text"], variant["selection"], 4.5)
        require_contrast(f"{variant['id']} success foreground", variant["on_success"], variant["success"], 4.5)
        require_contrast(f"{variant['id']} warning foreground", variant["on_warning"], variant["warning"], 4.5)
        require_contrast(f"{variant['id']} information foreground", variant["on_information"], variant["information"], 4.5)

    wallpapers = json.loads((ROOT / "config" / "wallpapers.json").read_text(encoding="utf-8"))
    wallpaper_design = wallpapers.get("design_system", {})
    if wallpaper_design.get("version") != "1.6.0" or wallpaper_design.get("lifecycle") != "anchor":
        fail("Wallpaper manifest must target the same V1.6 Anchor desktop contract")
    if wallpaper_design.get("upstream_accepted_release_source") != EXPECTED_UPSTREAM_SOURCE:
        fail("Wallpaper manifest upstream source pin does not match the theme palette")

    palette_by_id = {variant["id"]: variant for variant in variants}
    for collection_name in ("wallpapers", "catalog"):
        for wallpaper in wallpapers.get(collection_name, []):
            palette = palette_by_id.get(wallpaper.get("theme_id"))
            if palette is None:
                fail(f"{collection_name}: unknown theme_id {wallpaper.get('theme_id')!r}")
            if wallpaper.get("mode") != palette["mode"]:
                fail(f"{wallpaper.get('id')}: wallpaper mode does not match theme mode")
            for key in ("canvas", "accent", "accent_soft", "atmosphere_amber"):
                if wallpaper.get(key) != palette[key]:
                    fail(f"{wallpaper.get('id')}: {key} does not match canonical V1.6 palette")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        theme_output = tmp_path / "themes"
        wallpaper_output = tmp_path / "wallpapers"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build.py"),
                "--palette-config",
                str(PALETTES),
                "--output",
                str(theme_output),
            ],
            check=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_wallpapers.py"),
                "--palette-config",
                str(PALETTES),
                "--output",
                str(wallpaper_output),
            ],
            check=True,
        )

        index_files = list(theme_output.glob("*/index.theme"))
        if len(index_files) != 3:
            fail("V1.6 Anchor build did not render all three theme variants")
        for index_file in index_files:
            generated_metadata = index_file.read_text(encoding="utf-8")
            if "Glaze UI 1.6.0" not in generated_metadata:
                fail(f"{index_file.parent.name}: generated metadata does not identify Glaze UI 1.6.0")
            if "Glaze UI 1.2.0" in generated_metadata:
                fail(f"{index_file.parent.name}: generated metadata contains stale V1.2 labeling")

        if len(list(wallpaper_output.glob("*.svg"))) < 20:
            fail("V1.6 Anchor build did not render the complete wallpaper catalog")

    print("GLAZE UI V1.6 Anchor desktop contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
