#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PALETTES = ROOT / "config" / "palettes.json"

TOKEN_KEYS = (
    "canvas", "surface", "elevated", "deep", "text", "muted", "border",
    "accent", "accent_hover", "accent_soft", "selection", "atmosphere_amber",
    "on_accent",
)

TOKEN_MAP = {
    "accent2": "accent_hover",
    "soft": "accent_soft",
    "amber": "atmosphere_amber",
    "on": "on_accent",
}


def parse_args():
    p = argparse.ArgumentParser(
        description="Render the GoreeCloud Zorin wallpaper catalog from repository source."
    )
    p.add_argument("--output", required=True, type=Path)
    p.add_argument(
        "--palette-config",
        type=Path,
        default=DEFAULT_PALETTES,
        help=(
            "palette contract used for environmental base tokens; defaults to the "
            "canonical GLAZE UI V1.6 desktop adaptation in config/palettes.json."
        ),
    )
    return p.parse_args()


def resolve_input(path: Path) -> Path:
    path = path.expanduser()
    if path.is_absolute():
        return path.resolve()
    return (ROOT / path).resolve()


def mode_label(mode: str) -> str:
    return {"light": "Light", "dark": "Dark", "deep-dark": "Deep Dark"}[mode]


def strip_identity_wrapper(svg_text: str) -> str:
    text = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", svg_text, count=1)
    match = re.fullmatch(r"\s*<svg\b[^>]*>(.*)</svg>\s*", text, flags=re.S)
    if not match:
        raise SystemExit("Canonical identity SVG does not have one parseable outer <svg> wrapper")
    inner = match.group(1)
    inner = re.sub(r"\s*<title\b[^>]*>.*?</title>", "", inner, flags=re.S)
    inner = re.sub(r"\s*<desc\b[^>]*>.*?</desc>", "", inner, flags=re.S)
    return inner.strip()


def identity_values(item: dict, identities: dict) -> dict[str, str]:
    category_map = identities["category_asset"].get(item["category"])
    if not category_map:
        raise SystemExit(f"No canonical identity mapping for category {item['category']}")
    asset_id = category_map.get(item["mode"])
    if not asset_id:
        raise SystemExit(f"No canonical identity mapping for {item['category']} / {item['mode']}")
    asset = identities["assets"].get(asset_id)
    if not asset:
        raise SystemExit(f"Unknown canonical identity asset {asset_id}")
    if asset["identity"] != item["category"]:
        raise SystemExit(
            f"{item['id']}: canonical identity mapping mismatch "
            f"({asset['identity']} != {item['category']})"
        )

    path = ROOT / asset["local_path"]
    if not path.is_file():
        raise SystemExit(f"Missing synchronized canonical identity asset: {asset['local_path']}")
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != asset["sha256"]:
        raise SystemExit(
            f"{item['id']}: synchronized identity checksum mismatch for {asset['local_path']}"
        )
    text = raw.decode("utf-8")
    return {
        "identity_asset_id": asset_id,
        "identity_viewbox": asset["viewBox"],
        "identity_inner": strip_identity_wrapper(text),
    }


def main() -> int:
    args = parse_args()
    manifest = json.loads((ROOT / "config/wallpapers.json").read_text(encoding="utf-8"))
    palette_path = resolve_input(args.palette_config)
    palettes = json.loads(palette_path.read_text(encoding="utf-8"))
    identities = json.loads((ROOT / "config/wallpaper-identities.json").read_text(encoding="utf-8"))
    palette_by_id = {v["id"]: v for v in palettes["variants"]}
    args.output.mkdir(parents=True, exist_ok=True)

    generated = 0
    copied = 0
    for item in manifest["catalog"]:
        out = args.output / f"{item['id']}.svg"
        if not item.get("generated"):
            src = ROOT / item["source"]
            if not src.is_file():
                raise SystemExit(f"Missing wallpaper source: {item['source']}")
            out.write_bytes(src.read_bytes())
            copied += 1
            continue

        src = ROOT / item["source"]
        if not src.is_file():
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
        text = src.read_text(encoding="utf-8")
        values = {key: palette[key] for key in TOKEN_KEYS}
        for template_key, palette_key in TOKEN_MAP.items():
            values[template_key] = palette[palette_key]
        values["mode_label"] = mode_label(item["mode"])
        values.update(identity_values(item, identities))
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        if "{{" in text or "}}" in text:
            raise SystemExit(
                f"Unresolved wallpaper template token in {item['source']} for {item['id']}"
            )
        out.write_text(text, encoding="utf-8")
        generated += 1

    design = palettes.get("design_system", {})
    version = design.get("version", "unknown")
    lifecycle = design.get("lifecycle")
    label = f"Glaze UI {version}"
    if lifecycle:
        label += f" ({lifecycle})"
    print(
        f"Rendered wallpaper catalog from {label}: "
        f"{copied} direct + {generated} generated = {copied + generated}"
    )
    print(f"Palette contract: {palette_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
