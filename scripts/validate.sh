#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_GTK=0

if [[ "${1:-}" == "--gtk" ]]; then
  RUN_GTK=1
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--gtk]" >&2
  exit 64
fi

python3 -m py_compile \
  "$ROOT/scripts/build.py" \
  "$ROOT/scripts/compose_zorin_base.py"
bash -n "$ROOT/scripts/install.sh"
bash -n "$ROOT/scripts/uninstall.sh"
bash -n "$ROOT/scripts/validate.sh"
bash -n "$ROOT/scripts/diagnose.sh"
bash -n "$ROOT/scripts/trace_gtk4_runtime.sh"
bash -n "$ROOT/scripts/diagnose_settings_css.sh"
bash -n "$ROOT/scripts/wallpaper.sh"

for tool in \
  "$ROOT/scripts/build.py" \
  "$ROOT/scripts/install.sh" \
  "$ROOT/scripts/uninstall.sh" \
  "$ROOT/scripts/validate.sh" \
  "$ROOT/scripts/diagnose.sh" \
  "$ROOT/scripts/trace_gtk4_runtime.sh" \
  "$ROOT/scripts/diagnose_settings_css.sh" \
  "$ROOT/scripts/wallpaper.sh"; do
  if [[ ! -x "$tool" ]]; then
    echo "Expected executable tool is not executable: $tool" >&2
    exit 65
  fi
done

TEMP_ROOT="$(mktemp -d)"
TEMP_HOME="$(mktemp -d)"
cleanup() {
  rm -rf -- "$TEMP_ROOT" "$TEMP_HOME"
}
trap cleanup EXIT

python3 "$ROOT/scripts/build.py" --output "$TEMP_ROOT"

python3 - "$ROOT" "$TEMP_ROOT" <<'PY'
from __future__ import annotations

import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(sys.argv[1])
generated = Path(sys.argv[2])

config = json.loads((root / "config" / "palettes.json").read_text(encoding="utf-8"))
required = {
    "id", "display_name", "mode", "gtk_base_import",
    "canvas", "surface", "elevated", "deep", "text", "muted", "border",
    "accent", "accent_hover", "accent_soft", "on_accent", "selection",
    "destructive", "destructive_hover", "atmosphere_amber",
    "shell_panel", "shell_surface", "shell_elevated", "shell_border",
    "shell_hover", "shell_active", "shell_shadow",
}

ids = []
for variant in config["variants"]:
    missing = required - set(variant)
    if missing:
        raise SystemExit(f"{variant.get('id', '<unknown>')}: missing palette keys: {sorted(missing)}")
    ids.append(variant["id"])

if len(ids) != len(set(ids)):
    raise SystemExit("Duplicate theme IDs found")

for theme_id in ids:
    theme_root = generated / theme_id
    marker = theme_root / "gtk-4.0" / ".libadwaita"
    required_files = [
        theme_root / "index.theme",
        theme_root / "gtk-2.0" / "gtkrc",
        theme_root / "gtk-3.0" / "gtk.css",
        theme_root / "gtk-4.0" / "gtk.css",
        marker,
        theme_root / "gnome-shell" / "gnome-shell.css",
    ]
    for path in required_files:
        if not path.is_file():
            raise SystemExit(f"Missing generated file: {path}")

    for path in required_files:
        text = path.read_text(encoding="utf-8")
        if "{{" in text or "}}" in text:
            raise SystemExit(f"Unresolved template marker in {path}")

    gtk2 = (theme_root / "gtk-2.0" / "gtkrc").read_text(encoding="utf-8")
    gtk3 = (theme_root / "gtk-3.0" / "gtk.css").read_text(encoding="utf-8")
    gtk4 = (theme_root / "gtk-4.0" / "gtk.css").read_text(encoding="utf-8")
    shell = (theme_root / "gnome-shell" / "gnome-shell.css").read_text(encoding="utf-8")
    variant = next(v for v in config["variants"] if v["id"] == theme_id)

    for label, css in (("gtk3", gtk3), ("gtk4", gtk4), ("shell", shell)):
        if css.count("{") != css.count("}"):
            raise SystemExit(f"{theme_id}: unbalanced braces in {label} stylesheet")

    if 'include "/usr/share/themes/Adwaita/gtk-2.0/gtkrc"' not in gtk2:
        raise SystemExit(f"{theme_id}: GTK 2 discovery compatibility shim is missing")
    if "resource:///org/gtk/libgtk/theme/Adwaita/" not in gtk3:
        raise SystemExit(f"{theme_id}: GTK 3 standalone compatibility-base import is missing")
    for legacy_name in (
        "theme_fg_color",
        "theme_text_color",
        "theme_bg_color",
        "theme_base_color",
        "theme_selected_bg_color",
        "theme_selected_fg_color",
        "theme_unfocused_bg_color",
        "theme_unfocused_base_color",
        "borders",
        "unfocused_borders",
    ):
        if f"@define-color {legacy_name} " not in gtk3:
            raise SystemExit(
                f"{theme_id}: GTK 3 legacy symbolic color mapping is missing: {legacy_name}"
            )
    if ".nautilus-window .sidebar-row:selected" not in gtk3:
        raise SystemExit(
            f"{theme_id}: exact Nautilus 42.6 selected-sidebar override is missing"
        )

    gtk3_row_pattern = re.compile(
        r"row:selected,\s*row:selected:hover,\s*row:selected:focus\s*\{[^}]*"
        + re.escape("background-color: @gc_selection;"),
        re.S,
    )
    if not gtk3_row_pattern.search(gtk3):
        raise SystemExit(
            f"{theme_id}: GTK 3 generic selected-row state is not mapped to @gc_selection"
        )
    if "row.activatable:selected" not in gtk3:
        raise SystemExit(
            f"{theme_id}: GTK 3 activatable selected-row state coverage is missing"
        )
    gtk3_switch_pattern = re.compile(
        r"switch:checked\s*\{[^}]*"
        + re.escape("background-image: image(@gc_accent);"),
        re.S,
    )
    if not gtk3_switch_pattern.search(gtk3):
        raise SystemExit(
            f"{theme_id}: GTK 3 checked-switch image layer is not mapped to @gc_accent"
        )
    if "switch:checked slider" not in gtk3 or "switch:backdrop:checked slider" not in gtk3:
        raise SystemExit(
            f"{theme_id}: GTK 3 checked-switch slider state coverage is missing"
        )

    if "@define-color window_bg_color" not in gtk4:
        raise SystemExit(f"{theme_id}: GTK 4/libadwaita color-role mapping is missing")
    for expected_selector in (
        "list.navigation-sidebar > row:selected",
        "list.navigation-sidebar > row.activatable:selected",
        "switch:checked:hover",
    ):
        if expected_selector not in gtk4:
            raise SystemExit(
                f"{theme_id}: target GTK 4 selected-state override is missing: {expected_selector}"
            )
    selection_image = f"background-image: image({variant['selection']});"
    if selection_image not in gtk4:
        raise SystemExit(
            f"{theme_id}: GTK 4 selected-row image layer is not mapped to the variant selection token"
        )
    if "background-image: image(@accent_bg_color);" not in gtk4:
        raise SystemExit(
            f"{theme_id}: GTK 4 checked-switch image layer is not mapped to the GoreeCloud accent"
        )
    if "switch:checked > slider" not in gtk4:
        raise SystemExit(
            f"{theme_id}: GTK 4 checked-switch slider override is missing"
        )
    if marker.read_bytes() != b"":
        raise SystemExit(f"{theme_id}: .libadwaita marker must remain empty")
    markers = list(theme_root.rglob(".libadwaita"))
    if markers != [marker]:
        raise SystemExit(f"{theme_id}: unexpected libadwaita marker layout: {markers}")

    index = (theme_root / "index.theme").read_text(encoding="utf-8")
    if f"GtkTheme={theme_id}" not in index:
        raise SystemExit(f"{theme_id}: index.theme does not identify its GTK theme")

palette_by_id = {variant["id"]: variant for variant in config["variants"]}
wallpaper_config_path = root / "config" / "wallpapers.json"
if not wallpaper_config_path.is_file():
    raise SystemExit("Missing wallpaper manifest: config/wallpapers.json")
wallpaper_config = json.loads(wallpaper_config_path.read_text(encoding="utf-8"))
if wallpaper_config.get("design_system", {}).get("version") != config["design_system"]["version"]:
    raise SystemExit("Wallpaper manifest Glaze UI version does not match the theme palette version")
wallpapers = wallpaper_config.get("wallpapers", [])
if len(wallpapers) != 3:
    raise SystemExit("Expected exactly three primary Glaze Originals wallpaper variants")

wallpaper_rendered = generated / "_wallpapers"
subprocess.run(
    [
        sys.executable,
        str(root / "scripts" / "build_wallpapers.py"),
        "--output",
        str(wallpaper_rendered),
    ],
    check=True,
)

wallpaper_ids = set()
wallpaper_modes = set()
for wallpaper in wallpapers:
    required_wallpaper_keys = {
        "id", "mode", "theme_id", "file", "canvas", "accent", "accent_soft",
        "atmosphere_amber", "role", "art_direction", "source", "generated",
    }
    missing = required_wallpaper_keys - set(wallpaper)
    if missing:
        raise SystemExit(f"Wallpaper entry missing keys: {sorted(missing)}")
    if wallpaper["id"] in wallpaper_ids:
        raise SystemExit(f"Duplicate wallpaper ID: {wallpaper['id']}")
    if wallpaper["mode"] in wallpaper_modes:
        raise SystemExit(f"Duplicate wallpaper mode: {wallpaper['mode']}")
    wallpaper_ids.add(wallpaper["id"])
    wallpaper_modes.add(wallpaper["mode"])

    theme_id = wallpaper["theme_id"]
    if theme_id not in palette_by_id:
        raise SystemExit(f"Wallpaper references unknown theme: {theme_id}")
    palette = palette_by_id[theme_id]
    if wallpaper["mode"] != palette["mode"]:
        raise SystemExit(f"Wallpaper mode does not match theme mode: {wallpaper['id']}")
    for key in ("canvas", "accent", "accent_soft", "atmosphere_amber"):
        if wallpaper[key] != palette[key]:
            raise SystemExit(
                f"Wallpaper {wallpaper['id']} {key} does not match {theme_id} palette"
            )

    if wallpaper["generated"] is not True:
        raise SystemExit(f"Primary wallpaper must be generated from a Glaze-native source template: {wallpaper['id']}")
    relative = Path(wallpaper["file"])
    expected_relative = Path("generated") / f"{wallpaper['id']}.svg"
    if relative != expected_relative:
        raise SystemExit(
            f"Wallpaper generated path mismatch for {wallpaper['id']}: {relative}"
        )
    source = root / wallpaper["source"]
    if not source.is_file() or source.suffix != ".in":
        raise SystemExit(
            f"Wallpaper Glaze-native template is missing or invalid: {wallpaper['source']}"
        )

    path = wallpaper_rendered / f"{wallpaper['id']}.svg"
    if not path.is_file():
        raise SystemExit(f"Missing generated wallpaper artwork: {relative}")

    try:
        svg_root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise SystemExit(f"Invalid SVG XML in {relative}: {exc}") from exc
    if not svg_root.tag.endswith("svg"):
        raise SystemExit(f"Wallpaper root is not SVG: {relative}")
    if svg_root.attrib.get("width") != "3840" or svg_root.attrib.get("height") != "2160":
        raise SystemExit(f"Wallpaper does not declare 3840x2160 native size: {relative}")
    if svg_root.attrib.get("viewBox") != "0 0 3840 2160":
        raise SystemExit(f"Wallpaper viewBox is not 0 0 3840 2160: {relative}")

    for element in svg_root.iter():
        local_name = element.tag.rsplit("}", 1)[-1].lower()
        if local_name == "script":
            raise SystemExit(f"Wallpaper contains executable script content: {relative}")
        for attribute, value in element.attrib.items():
            attr_name = attribute.rsplit("}", 1)[-1].lower()
            if attr_name == "href" and (
                value.startswith("http://")
                or value.startswith("https://")
                or value.startswith("data:")
                or value.startswith("file:")
            ):
                raise SystemExit(f"Wallpaper contains an external/embedded href: {relative}")

if wallpaper_modes != {"light", "dark", "deep-dark"}:
    raise SystemExit(f"Unexpected wallpaper mode set: {sorted(wallpaper_modes)}")

composer = (root / "scripts" / "compose_zorin_base.py").read_text(encoding="utf-8")
for expected in (
    'TARGET_PACKAGE_VERSION = "4.2.2"',
    '"GoreeCloud-Zorin-Light": "ZorinBlue-Light"',
    '"GoreeCloud-Zorin-Dark": "ZorinBlue-Dark"',
    '"GoreeCloud-Zorin-DeepDark": "ZorinBlue-Dark"',
    "bc06ff2fac92e56951b8f4141b8324acc1e38db783ec3a0b3cf438e8c87d9fe6",
    "71e9d93ad1e58f75e52bb7b724fa38409961368b5d9edda4c3b921fac6e44604",
    "b29cfbaa713955b14517798e2c15a67184136d9913944c1d0cf22fce0d1b3e0c",
    "90ffa76c872443d1549f09c814be8c22d68169a0dfb19e0508339e3613add77d",
    "3d94563d7c680be4ac0632b95bb0c205954377488c774a653d8655dbc2ca0823",
    "e36202095055bda8de6f225227a91911623775aa0896c24b8568c0d52982f8d7",
    'shutil.copytree(base_theme / "gtk-3.0"',
    "strip_standalone_gtk3_import",
):
    if expected not in composer:
        raise SystemExit(f"Target Zorin 17.3 base-composition evidence is missing: {expected}")

secret_patterns = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]+['\"]"),
]
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts or "build" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for pattern in secret_patterns:
        if pattern.search(text):
            raise SystemExit(f"Potential reusable secret material detected in {path}")

print("Static theme and wallpaper validation passed")
PY

if [[ "$RUN_GTK" -eq 1 ]]; then
  command -v xvfb-run >/dev/null || {
    echo "xvfb-run is required for --gtk validation" >&2
    exit 69
  }

  mkdir -p "$TEMP_HOME/.local/share/themes"
  cp -a "$TEMP_ROOT"/GoreeCloud-Zorin-* "$TEMP_HOME/.local/share/themes/"

  for theme in GoreeCloud-Zorin-Light GoreeCloud-Zorin-Dark GoreeCloud-Zorin-DeepDark; do
    echo "GTK 3 smoke-load: $theme"
    HOME="$TEMP_HOME" \
    GTK_THEME="$theme" \
    THEME_CSS="$TEMP_ROOT/$theme/gtk-3.0/gtk.css" \
    NO_AT_BRIDGE=1 \
    xvfb-run -a python3 - <<'PY'
import os

import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

errors = []
provider = Gtk.CssProvider()
provider.connect(
    "parsing-error",
    lambda _provider, _section, error: errors.append(str(error)),
)
provider.load_from_path(os.environ["THEME_CSS"])
if errors:
    raise SystemExit("GTK 3 CSS parsing failed: " + " | ".join(errors))

screen = Gdk.Screen.get_default()
if screen is None:
    raise SystemExit("GTK 3 smoke-load could not acquire an Xvfb screen")
Gtk.StyleContext.add_provider_for_screen(
    screen,
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER,
)

window = Gtk.Window()
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
box.set_border_width(12)
box.pack_start(Gtk.Entry(), False, False, 0)
box.pack_start(Gtk.Button(label="GoreeCloud"), False, False, 0)
box.pack_start(Gtk.Switch(), False, False, 0)
window.add(box)
window.show_all()
while Gtk.events_pending():
    Gtk.main_iteration()
window.destroy()
PY

    echo "GTK 4/libadwaita smoke-load: $theme"
    HOME="$TEMP_HOME" \
    THEME_CSS="$TEMP_ROOT/$theme/gtk-4.0/gtk.css" \
    NO_AT_BRIDGE=1 \
    xvfb-run -a python3 - <<'PY'
import os

import gi
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gdk, GLib, Gtk

Adw.init()
errors = []
provider = Gtk.CssProvider()
provider.connect(
    "parsing-error",
    lambda _provider, _section, error: errors.append(str(error)),
)
provider.load_from_path(os.environ["THEME_CSS"])
if errors:
    raise SystemExit("GTK 4 CSS parsing failed: " + " | ".join(errors))

display = Gdk.Display.get_default()
if display is None:
    raise SystemExit("GTK 4 smoke-load could not acquire an Xvfb display")
Gtk.StyleContext.add_provider_for_display(
    display,
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER,
)

window = Adw.Window()
box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
box.set_margin_top(12)
box.set_margin_bottom(12)
box.set_margin_start(12)
box.set_margin_end(12)
box.append(Gtk.Entry())
box.append(Gtk.Button(label="GoreeCloud"))
box.append(Gtk.Switch())
window.set_content(box)
window.present()
context = GLib.MainContext.default()
while context.pending():
    context.iteration(False)
window.close()
PY
  done
fi

echo "Validation completed successfully"
