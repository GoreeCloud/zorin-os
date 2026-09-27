#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
ICON_DEST="$DATA_HOME/icons"
LEGACY_ICON_DEST="$HOME/.icons"
ICON_THEME="GoreeCloud-Zorin"
STAMP="$(date +%Y%m%d-%H%M%S)"
RECOVERY_ROOT="$ICON_DEST/.goreecloud-zorin-recovery/$STAMP"
TEMP_ROOT="$(mktemp -d)"

cleanup() {
  rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

python3 "$ROOT/scripts/build_icons.py" --output "$TEMP_ROOT/icons"
python3 "$ROOT/scripts/validate_desktop_assets.py" >/dev/null

mkdir -p -- "$ICON_DEST"
target="$ICON_DEST/$ICON_THEME"
backed_up=0
if [[ -e "$target" || -L "$target" ]]; then
  mkdir -p -- "$RECOVERY_ROOT"
  mv -- "$target" "$RECOVERY_ROOT/$ICON_THEME"
  backed_up=1
fi
cp -a -- "$TEMP_ROOT/icons/$ICON_THEME" "$target"

REPORT="$target/goreecloud-normalization-report.json"
python3 "$ROOT/scripts/normalize_app_icons.py" \
  --theme-root "$target" \
  --report "$REPORT"

if [[ "$LEGACY_ICON_DEST" != "$ICON_DEST" ]]; then
  mkdir -p -- "$LEGACY_ICON_DEST"
  legacy="$LEGACY_ICON_DEST/$ICON_THEME"
  if [[ -e "$legacy" || -L "$legacy" ]]; then
    if [[ -L "$legacy" && "$(readlink -- "$legacy")" == "$target" ]]; then
      rm -f -- "$legacy"
    else
      mkdir -p -- "$RECOVERY_ROOT/legacy"
      mv -- "$legacy" "$RECOVERY_ROOT/legacy/$ICON_THEME"
    fi
  fi
  ln -s -- "$target" "$legacy"
fi

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f "$target" >/dev/null 2>&1 || true
fi

if command -v gsettings >/dev/null 2>&1; then
  current="$(gsettings get org.gnome.desktop.interface icon-theme 2>/dev/null | tr -d "'" || true)"
  if [[ "$current" == "$ICON_THEME" ]]; then
    gsettings set org.gnome.desktop.interface icon-theme "'Adwaita'"
    sleep 0.35
  fi
  gsettings set org.gnome.desktop.interface icon-theme "'$ICON_THEME'"
fi

echo
echo "Installed GoreeCloud icon theme:"
echo "  $target"
echo "Third-party app normalization report:"
echo "  $REPORT"
if [[ "$backed_up" -eq 1 ]]; then
  echo "Previous GoreeCloud icon theme preserved at:"
  echo "  $RECOVERY_ROOT/$ICON_THEME"
fi
echo "GTK/Shell themes, cursor theme, and wallpaper settings were not changed."
