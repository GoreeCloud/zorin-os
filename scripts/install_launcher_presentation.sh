#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
THEME_DEST="$DATA_HOME/themes"
PALETTE_CONFIG="$ROOT/config/palettes.json"
STAMP="$(date +%Y%m%d-%H%M%S)"
RECOVERY_ROOT="$THEME_DEST/.goreecloud-zorin-launcher-recovery/$STAMP"
TEMP_ROOT="$(mktemp -d)"

THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)

cleanup() {
  rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

python3 "$ROOT/scripts/build.py"   --palette-config "$PALETTE_CONFIG"   --output "$TEMP_ROOT/themes"

python3 "$ROOT/scripts/validate_desktop_assets.py" >/dev/null
python3 "$ROOT/scripts/validate_v16_anchor.py" >/dev/null

python3 "$ROOT/scripts/compose_zorin_base.py"   "$TEMP_ROOT/themes"   --palette-config "$PALETTE_CONFIG"

mkdir -p -- "$RECOVERY_ROOT"

updated=0
for theme in "${THEMES[@]}"; do
  source_shell="$TEMP_ROOT/themes/$theme/gnome-shell"
  target_theme="$THEME_DEST/$theme"
  target_shell="$target_theme/gnome-shell"

  if [[ ! -d "$target_theme" ]]; then
    continue
  fi
  if [[ ! -d "$source_shell" ]]; then
    echo "Generated Shell assets are missing for $theme" >&2
    exit 1
  fi

  mkdir -p -- "$RECOVERY_ROOT/$theme"
  if [[ -e "$target_shell" || -L "$target_shell" ]]; then
    mv -- "$target_shell" "$RECOVERY_ROOT/$theme/gnome-shell"
  fi
  cp -a -- "$source_shell" "$target_shell"
  updated=$((updated + 1))
done

if [[ "$updated" -eq 0 ]]; then
  echo "No installed GoreeCloud Shell themes were found under: $THEME_DEST" >&2
  echo "Run ./scripts/install.sh first." >&2
  exit 1
fi

if command -v gsettings >/dev/null 2>&1 &&
   gsettings list-schemas | grep -Fxq 'org.gnome.shell.extensions.user-theme'; then
  current_shell="$(gsettings get org.gnome.shell.extensions.user-theme name 2>/dev/null | tr -d "'" || true)"
  for theme in "${THEMES[@]}"; do
    if [[ "$current_shell" == "$theme" ]]; then
      gsettings set org.gnome.shell.extensions.user-theme name "''"
      sleep 0.35
      gsettings set org.gnome.shell.extensions.user-theme name "'$theme'"
      break
    fi
  done
fi

echo
echo "Updated GoreeCloud launcher/Shell presentation for $updated installed theme variant(s)."
echo "Recovery snapshot:"
echo "  $RECOVERY_ROOT"
echo "Third-party application icon files were not changed."
echo "GTK application theme, icon theme, cursor theme, and wallpaper settings were not changed."
echo
echo "If the open Zorin menu still shows the previous styling, close and reopen it."
echo "On Wayland, log out and back in only if Shell theme caching prevents the change from appearing."
