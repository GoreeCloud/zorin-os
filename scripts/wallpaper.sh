#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/config/wallpapers.json"
PALETTE_CONFIG="${GOREECLOUD_PALETTE_CONFIG:-$ROOT/config/palettes.json}"
DEST_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/backgrounds/GoreeCloud-Zorin"
CATALOG_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-background-properties"
CATALOG_FILE="$CATALOG_DIR/goreecloud-zorin.xml"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/goreecloud-zorin/wallpaper"
SCHEMA="org.gnome.desktop.background"
DEFAULT_MODE="light"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/wallpaper.sh install
  ./scripts/wallpaper.sh list
  ./scripts/wallpaper.sh apply default|current|light|dark|deep-dark|WALLPAPER_ID
  ./scripts/wallpaper.sh restore
  ./scripts/wallpaper.sh status
  ./scripts/wallpaper.sh replace-stock plan|apply|status|restore|finalize

The GoreeCloud gallery is light-first, not light-only. GNOME Settings exposes
all 24 wallpapers: the eight Light variants first, followed by eight Dark and
eight Deep Dark variants. The default applied wallpaper remains Light.

The default installed wallpaper palette is the GoreeCloud Zorin adaptation of GLAZE UI V1.6 / 1.6.0 Official Anchor.

replace-stock keeps Zorin packages installed and diverts only the exact audited
stock wallpaper/catalog files out of GNOME discovery paths.
EOF
}

detect_mode() {
  local theme
  theme="$(gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null | tr -d "'" || true)"
  case "$theme" in
    GoreeCloud-Zorin-Light) printf '%s\n' "light" ;;
    GoreeCloud-Zorin-Dark) printf '%s\n' "dark" ;;
    GoreeCloud-Zorin-DeepDark) printf '%s\n' "deep-dark" ;;
    *) printf '%s\n' "$DEFAULT_MODE" ;;
  esac
}

primary_id_for_mode() {
  python3 - "$MANIFEST" "$1" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
mode=sys.argv[2]
matches=[w["id"] for w in data["wallpapers"] if w["mode"] == mode]
if len(matches) != 1:
    raise SystemExit(f"Expected one primary wallpaper for {mode}; found {len(matches)}")
print(matches[0])
PY
}

file_for_id() {
  python3 - "$MANIFEST" "$1" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
wallpaper_id=sys.argv[2]
matches=[w for w in data["catalog"] if w["id"] == wallpaper_id]
if len(matches) != 1:
    raise SystemExit(f"Unknown or duplicate wallpaper ID: {wallpaper_id}")
print(matches[0]["id"] + ".svg")
PY
}

schema_has_key() {
  gsettings list-keys "$SCHEMA" 2>/dev/null | grep -Fxq -- "$1"
}

install_wallpapers() {
  python3 "$ROOT/scripts/validate_wallpapers.py" >/dev/null
  mkdir -p -- "$DEST_DIR" "$CATALOG_DIR"

  find "$DEST_DIR" -maxdepth 1 -type f -name '*.svg' -delete

  local temp_dir
  temp_dir="$(mktemp -d)"
  trap 'rm -rf -- "$temp_dir"' RETURN
  python3 "$ROOT/scripts/build_wallpapers.py" \
    --palette-config "$PALETTE_CONFIG" \
    --output "$temp_dir" >/dev/null

  while IFS= read -r wallpaper_id; do
    [[ -n "$wallpaper_id" ]] || continue
    cp -f -- "$temp_dir/$wallpaper_id.svg" "$DEST_DIR/$wallpaper_id.svg"
  done < <(python3 - "$MANIFEST" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
for item in data["catalog"]:
    print(item["id"])
PY
)

  python3 "$ROOT/scripts/build_background_catalog.py" \
    --manifest "$MANIFEST" \
    --filename-root "$DEST_DIR" \
    --output "$CATALOG_FILE" \
    --mode light >/dev/null

  rm -rf -- "$temp_dir"
  trap - RETURN
  printf 'Installed GoreeCloud wallpaper source set to:\n  %s\n' "$DEST_DIR"
  printf 'Installed Light-only GNOME background catalog (8 visible; 16 compatibility derivatives hidden) to:\n  %s\n' "$CATALOG_FILE"
}

backup_settings() {
  mkdir -p -- "$STATE_DIR"
  local stamp snapshot
  stamp="$(date +%Y%m%d-%H%M%S)"
  snapshot="$STATE_DIR/settings-$stamp.txt"
  : > "$snapshot"
  for key in picture-uri picture-uri-dark picture-options primary-color secondary-color color-shading-type; do
    if schema_has_key "$key"; then
      printf '%s\t%s\n' "$key" "$(gsettings get "$SCHEMA" "$key")" >> "$snapshot"
    fi
  done
  printf '%s\n' "$snapshot"
}

apply_wallpaper() {
  local selection="$1" mode wallpaper_id file
  case "$selection" in
    default)
      wallpaper_id="$(primary_id_for_mode "$DEFAULT_MODE")"
      ;;
    current)
      mode="$(detect_mode)"
      wallpaper_id="$(primary_id_for_mode "$mode")"
      ;;
    light|dark|deep-dark)
      wallpaper_id="$(primary_id_for_mode "$selection")"
      ;;
    *)
      wallpaper_id="$selection"
      ;;
  esac

  file="$(file_for_id "$wallpaper_id")"
  command -v gsettings >/dev/null 2>&1 || {
    echo "gsettings is required to apply a wallpaper." >&2
    exit 69
  }

  install_wallpapers >/dev/null
  local snapshot uri target
  snapshot="$(backup_settings)"
  target="$DEST_DIR/$file"
  uri="$(python3 - "$target" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve().as_uri())
PY
)"

  gsettings set "$SCHEMA" picture-uri "'$uri'"
  if schema_has_key picture-uri-dark; then
    gsettings set "$SCHEMA" picture-uri-dark "'$uri'"
  fi
  if schema_has_key picture-options; then
    gsettings set "$SCHEMA" picture-options "'zoom'"
  fi

  printf 'Applied GoreeCloud wallpaper %s:\n  %s\n' "$wallpaper_id" "$target"
  printf 'Previous GNOME background settings were preserved at:\n  %s\n' "$snapshot"
}

restore_wallpaper() {
  command -v gsettings >/dev/null 2>&1 || {
    echo "gsettings is required to restore wallpaper settings." >&2
    exit 69
  }

  local snapshot
  snapshot="$(find "$STATE_DIR" -maxdepth 1 -type f -name 'settings-*.txt' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -n1 | cut -d' ' -f2- || true)"
  if [[ -z "$snapshot" || ! -f "$snapshot" ]]; then
    echo "No GoreeCloud wallpaper settings snapshot is available to restore." >&2
    exit 1
  fi

  while IFS=$'\t' read -r key value; do
    [[ -n "$key" ]] || continue
    if schema_has_key "$key"; then
      gsettings set "$SCHEMA" "$key" "$value"
    fi
  done < "$snapshot"

  printf 'Restored GNOME background settings from:\n  %s\n' "$snapshot"
}

list_wallpapers() {
  python3 - "$MANIFEST" <<'PY'
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))
mode_order={"light": 0, "dark": 1, "deep-dark": 2}
category_order={name: i for i, name in enumerate(data["collection"]["categories"])}
items=sorted(
    data["catalog"],
    key=lambda item: (
        mode_order.get(item["mode"], 99),
        category_order.get(item["category"], 99),
        item["family"],
        item["id"],
    ),
)
current=None
for item in items:
    if item["mode"] != current:
        current=item["mode"]
        print(f"\n{current.replace('-', ' ').title()}")
    print(f"  {item['id']:<38} {item['category']} — {item['family']}")
print("\nGallery order: 8 Light, 8 Dark, 8 Deep Dark")
PY
}

show_status() {
  printf 'GoreeCloud wallpaper asset directory:\n  %s\n' "$DEST_DIR"
  if [[ -d "$DEST_DIR" ]]; then
    find "$DEST_DIR" -maxdepth 1 -type f -name '*.svg' -print | sort
  fi
  printf '\nUser background catalog:\n  %s\n' "$CATALOG_FILE"
  if command -v gsettings >/dev/null 2>&1; then
    printf '\nCurrent GNOME background settings:\n'
    for key in picture-uri picture-uri-dark picture-options; do
      if schema_has_key "$key"; then
        printf '%-18s %s\n' "$key" "$(gsettings get "$SCHEMA" "$key")"
      fi
    done
  fi
}

replace_stock() {
  local action="$1"
  case "$action" in
    plan|status)
      "$ROOT/scripts/system_wallpapers.sh" "$action"
      ;;
    apply)
      apply_wallpaper default
      sudo "$ROOT/scripts/system_wallpapers.sh" apply
      ;;
    restore|finalize)
      sudo "$ROOT/scripts/system_wallpapers.sh" "$action"
      ;;
    *)
      usage >&2
      exit 64
      ;;
  esac
}

case "${1:-}" in
  install)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    install_wallpapers
    ;;
  list)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    list_wallpapers
    ;;
  apply)
    [[ $# -eq 2 ]] || { usage >&2; exit 64; }
    apply_wallpaper "$2"
    ;;
  restore)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    restore_wallpaper
    ;;
  status)
    [[ $# -eq 1 ]] || { usage >&2; exit 64; }
    show_status
    ;;
  replace-stock)
    [[ $# -eq 2 ]] || { usage >&2; exit 64; }
    replace_stock "$2"
    ;;
  *)
    usage >&2
    exit 64
    ;;
esac
