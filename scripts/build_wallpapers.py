#!/usr/bin/env python3
"""Render the GoreeCloud Zorin wallpaper catalog from Glaze-native SVG templates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PALETTES = ROOT / "config" / "palettes.json"

VARIANT_TOKEN_KEYS = (
    "canvas", "surface", "elevated", "deep", "text", "muted", "border",
)
OPTICAL_TOKEN_KEYS = (
    "frost_white", "crystal_white", "ice_blue", "glacier_blue",
    "clear_sky_blue", "cloud_gray", "slate_gray", "cool_graphite",
    "deep_graphite", "blue_black", "goreecloud_primary_blue",
    "goreecloud_deep_blue",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--palette-config",
        type=Path,
        default=DEFAULT_PALETTES,
        help=(
            "palette contract used for Glaze environmental tokens; defaults to "
            "the canonical GLAZE UI V1.6 Zorin adaptation."
        ),
    )
    return parser.parse_args()


def resolve_input(path: Path) -> Path:
    path = path.expanduser()
    if path.is_absolute():
        return path.resolve()
    return (ROOT / path).resolve()


def mode_label(mode: str) -> str:
    return {"light": "Light", "dark": "Dark", "deep-dark": "Deep Dark"}[mode]


def render_template(template: str, values: dict[str, str], source: Path) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    if "{{" in rendered or "}}" in rendered:
        raise SystemExit(f"Unresolved wallpaper template token in {source}")
    return rendered


def main() -> int:
    args = parse_args()
    manifest = json.loads((ROOT / "config/wallpapers.json").read_text(encoding="utf-8"))
    palette_path = resolve_input(args.palette_config)
    palettes = json.loads(palette_path.read_text(encoding="utf-8"))
    palette_by_id = {variant["id"]: variant for variant in palettes["variants"]}
    optical = palettes.get("optical_references", {})

    missing_optical = [key for key in OPTICAL_TOKEN_KEYS if key not in optical]
    if missing_optical:
        raise SystemExit(
            "Palette contract is missing wallpaper optical reference(s): "
            + ", ".join(missing_optical)
        )

    args.output.mkdir(parents=True, exist_ok=True)
    generated = 0

    for item in manifest["catalog"]:
        if not item.get("generated"):
            raise SystemExit(f"{item['id']}: wallpaper catalog must use generated SVG templates")

        source = ROOT / item["source"]
        if not source.is_file():
            raise SystemExit(f"Missing wallpaper template: {item['source']}")

        palette = palette_by_id.get(item["theme_id"])
        if palette is None:
            raise SystemExit(
                f"{item['id']}: palette contract {palette_path} has no {item['theme_id']} variant"
            )
        if palette.get("mode") != item["mode"]:
            raise SystemExit(
                f"{item['id']}: palette mode {palette.get('mode')} does not match {item['mode']}"
            )

        values = {key: str(palette[key]) for key in VARIANT_TOKEN_KEYS}
        values.update({key: str(optical[key]) for key in OPTICAL_TOKEN_KEYS})
        values["mode_label"] = mode_label(item["mode"])
        values["category"] = str(item["category"])
        values["family"] = str(item["family"])

        template = source.read_text(encoding="utf-8")
        output = args.output / f"{item['id']}.svg"
        output.write_text(render_template(template, values, source), encoding="utf-8")
        generated += 1

    design = palettes.get("design_system", {})
    version = design.get("version", "unknown")
    lifecycle = design.get("lifecycle")
    label = f"Glaze UI {version}"
    if lifecycle:
        label += f" ({lifecycle})"

    print(f"Rendered {generated} Glaze-native wallpapers from {label} in {args.output}")
    print(f"Palette contract: {palette_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
