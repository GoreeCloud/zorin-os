#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
THEME_DEST="$DATA_HOME/themes"
ICON_DEST="$DATA_HOME/icons"
LEGACY_ICON_DEST="$HOME/.icons"
PALETTE_CONFIG="$ROOT/config/palettes.json"
DESKTOP_ASSET_CONFIG="$ROOT/config/desktop-assets.json"
STAMP="$(date +%Y%m%d-%H%M%S)"
THEME_RECOVERY_ROOT="$THEME_DEST/.goreecloud-zorin-recovery/$STAMP"
ASSET_RECOVERY_ROOT="$ICON_DEST/.goreecloud-zorin-recovery/$STAMP"
LEGACY_RECOVERY_ROOT="$LEGACY_ICON_DEST/.goreecloud-zorin-recovery/$STAMP"
REPLACE_STOCK=0
THEMES=(
  "GoreeCloud-Zorin-Light"
  "GoreeCloud-Zorin-Dark"
  "GoreeCloud-Zorin-DeepDark"
)
ICON_THEME="GoreeCloud-Zorin"
CURSOR_THEME="GoreeCloud-Zorin-Cursors"
CURSOR_RUNTIME_THEME="$(
  python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["cursor_theme"]["runtime_id"])' \
    "$DESKTOP_ASSET_CONFIG"
)"
LIGHT_THEME="GoreeCloud-Zorin-Light"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/install.sh
  ./scripts/install.sh --replace-stock

The install activates the light-first GoreeCloud desktop experience using the
GLAZE UI V1.6 Official Anchor desktop palette: Applications theme, Shell theme, GoreeCloud
icons, GoreeCloud cursors, and the primary light wallpaper. The GNOME
Settings gallery remains light-first rather than light-only: all 30 Glaze
Originals are visible, ordered as 10 Light, 10 Dark, and 10 Deep Dark variants.

--replace-stock additionally moves the exact audited Zorin OS 17.3 stock
wallpaper files/catalogs out of GNOME discovery paths with package-safe dpkg
diversions. Zorin desktop/artwork packages remain installed.
EOF
}

case "${1:-}" in
  "") ;;
  --replace-stock) REPLACE_STOCK=1 ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 64
    ;;
esac
[[ $# -le 1 ]] || { usage >&2; exit 64; }

TEMP_ROOT="$(mktemp -d)"
cleanup() {
  rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

python3 "$ROOT/scripts/build.py" \
  --palette-config "$PALETTE_CONFIG" \
  --output "$TEMP_ROOT/themes"
python3 "$ROOT/scripts/build_icons.py" --output "$TEMP_ROOT/icons"
python3 "$ROOT/scripts/build_cursors.py" --output "$TEMP_ROOT/cursors"
python3 "$ROOT/scripts/validate_desktop_assets.py" >/dev/null
python3 "$ROOT/scripts/validate_v16_anchor.py" >/dev/null
python3 "$ROOT/scripts/validate_light_catalog.py" >/dev/null

# Zorin OS 17.3's GTK 3, GTK 4, and Shell themes contain extensive
# platform-specific selectors and assets. Compose the generated GoreeCloud
# semantic overrides on top of the exact verified local Zorin 17.3 base before
# touching an existing installed GoreeCloud theme. Use the same V1.6 palette
# contract so native selected/checked states cannot fall back to V1.1 teal.
python3 "$ROOT/scripts/compose_zorin_base.py" \
  "$TEMP_ROOT/themes" \
  --palette-config "$PALETTE_CONFIG"

mkdir -p -- "$THEME_DEST" "$ICON_DEST"

theme_backed_up=0
for theme in "${THEMES[@]}"; do
  target="$THEME_DEST/$theme"
  if [[ -e "$target" || -L "$target" ]]; then
    mkdir -p -- "$THEME_RECOVERY_ROOT"
    mv -- "$target" "$THEME_RECOVERY_ROOT/$theme"
    theme_backed_up=1
  fi
  cp -a -- "$TEMP_ROOT/themes/$theme" "$target"
done

asset_backed_up=0
for asset in "$ICON_THEME" "$CURSOR_THEME"; do
  target="$ICON_DEST/$asset"
  if [[ -e "$target" || -L "$target" ]]; then
    mkdir -p -- "$ASSET_RECOVERY_ROOT"
    mv -- "$target" "$ASSET_RECOVERY_ROOT/$asset"
    asset_backed_up=1
  fi
done
cp -a -- "$TEMP_ROOT/icons/$ICON_THEME" "$ICON_DEST/$ICON_THEME"
cp -a -- "$TEMP_ROOT/cursors/$CURSOR_THEME" "$ICON_DEST/$CURSOR_THEME"

# Mutter/Xcursor consumers can keep the bytes for a cursor theme cached by
# theme identifier even after that directory is replaced in place. The cursor
# design contract therefore carries a revisioned runtime identifier while the
# canonical product asset remains GoreeCloud-Zorin-Cursors. Point the runtime
# identifier at the canonical installed bytes so a design-revision change is a
# real settings identity change without duplicating the cursor payload.
if [[ "$CURSOR_RUNTIME_THEME" != "$CURSOR_THEME" ]]; then
  runtime_target="$ICON_DEST/$CURSOR_RUNTIME_THEME"
  if [[ -e "$runtime_target" || -L "$runtime_target" ]]; then
    if [[ -L "$runtime_target" && "$(readlink -- "$runtime_target")" == "$ICON_DEST/$CURSOR_THEME" ]]; then
      rm -f -- "$runtime_target"
    else
      mkdir -p -- "$ASSET_RECOVERY_ROOT"
      mv -- "$runtime_target" "$ASSET_RECOVERY_ROOT/$CURSOR_RUNTIME_THEME"
      asset_backed_up=1
    fi
  fi
  ln -s -- "$ICON_DEST/$CURSOR_THEME" "$runtime_target"
fi

# Zorin's documented third-party icon/cursor location is
# ~/.local/share/icons. Some GTK/theme enumeration paths and older tools also
# consult ~/.icons. Keep compatibility links there so Zorin Appearance and
# legacy consumers resolve the same canonical installation without duplicating
# theme bytes. The revisioned cursor runtime identity is included for the same
# discovery reason.
legacy_backed_up=0
if [[ "$LEGACY_ICON_DEST" != "$ICON_DEST" ]]; then
  mkdir -p -- "$LEGACY_ICON_DEST"
  legacy_assets=("$ICON_THEME" "$CURSOR_THEME")
  if [[ "$CURSOR_RUNTIME_THEME" != "$CURSOR_THEME" ]]; then
    legacy_assets+=("$CURSOR_RUNTIME_THEME")
  fi
  for asset in "${legacy_assets[@]}"; do
    legacy="$LEGACY_ICON_DEST/$asset"
    if [[ -e "$legacy" || -L "$legacy" ]]; then
      if [[ -L "$legacy" && "$(readlink -- "$legacy")" == "$ICON_DEST/$asset" ]]; then
        rm -f -- "$legacy"
      else
        mkdir -p -- "$LEGACY_RECOVERY_ROOT"
        mv -- "$legacy" "$LEGACY_RECOVERY_ROOT/$asset"
        legacy_backed_up=1
      fi
    fi
    ln -s -- "$ICON_DEST/$asset" "$legacy"
  done
fi

for required in \
  "$ICON_DEST/$ICON_THEME/index.theme" \
  "$ICON_DEST/$CURSOR_THEME/index.theme" \
  "$ICON_DEST/$CURSOR_THEME/cursors/left_ptr" \
  "$ICON_DEST/$CURSOR_RUNTIME_THEME/cursors/left_ptr"; do
  if [[ ! -e "$required" ]]; then
    echo "Installed desktop asset is missing: $required" >&2
    exit 1
  fi
done

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f "$ICON_DEST/$ICON_THEME" >/dev/null 2>&1 || true
fi

cycle_setting_if_same() {
  local schema="$1"
  local key="$2"
  local target="$3"
  local fallback="$4"
  local current

  current="$(gsettings get "$schema" "$key" 2>/dev/null | tr -d "'" || true)"
  if [[ "$current" == "$target" ]]; then
    gsettings set "$schema" "$key" "'$fallback'"
    # Do not immediately overwrite the fallback. GNOME settings observers can
    # coalesce back-to-back dconf changes and never process the intermediate
    # identity, leaving an old in-memory theme or cursor payload resident.
    sleep 0.35
  fi
  gsettings set "$schema" "$key" "'$target'"
}

activate_light_experience() {
  if ! command -v gsettings >/dev/null 2>&1; then
    return 0
  fi

  # Reinstalling a theme under the same name does not reliably make already
  # running GTK/Shell consumers reload the changed CSS or icons. Cycle through
  # a safe fallback only when the target is already selected, then restore the
  # GoreeCloud values. Cursor design revisions use a revisioned runtime theme
  # identity so Mutter/Xcursor cannot resolve the new design through the prior
  # GoreeCloud cursor cache key.
  cycle_setting_if_same org.gnome.desktop.interface gtk-theme "$LIGHT_THEME" "Adwaita"
  cycle_setting_if_same org.gnome.desktop.interface icon-theme "$ICON_THEME" "Adwaita"
  cycle_setting_if_same org.gnome.desktop.interface cursor-theme "$CURSOR_RUNTIME_THEME" "Adwaita"

  if gsettings list-schemas | grep -Fxq 'org.gnome.shell.extensions.user-theme'; then
    current_shell_theme="$(gsettings get org.gnome.shell.extensions.user-theme name 2>/dev/null | tr -d "'" || true)"
    if [[ "$current_shell_theme" == "$LIGHT_THEME" ]]; then
      gsettings set org.gnome.shell.extensions.user-theme name "''"
      # Give the Shell extension a chance to process the first settings change
      # before restoring the same theme name; otherwise rapid dconf updates can
      # leave the previous stylesheet resident for the rest of the session.
      sleep 0.25
    fi
    gsettings set org.gnome.shell.extensions.user-theme name "'$LIGHT_THEME'"
  fi

  if gsettings list-keys org.gnome.desktop.interface 2>/dev/null | grep -Fxq 'color-scheme'; then
    gsettings set org.gnome.desktop.interface color-scheme "'default'"
  fi

  active_gtk="$(gsettings get org.gnome.desktop.interface gtk-theme | tr -d "'" || true)"
  active_icons="$(gsettings get org.gnome.desktop.interface icon-theme | tr -d "'" || true)"
  active_cursor="$(gsettings get org.gnome.desktop.interface cursor-theme | tr -d "'" || true)"
  if [[ "$active_gtk" != "$LIGHT_THEME" ]]; then
    echo "Failed to activate GTK theme: expected $LIGHT_THEME, got $active_gtk" >&2
    exit 1
  fi
  if [[ "$active_icons" != "$ICON_THEME" ]]; then
    echo "Failed to activate icon theme: expected $ICON_THEME, got $active_icons" >&2
    exit 1
  fi
  if [[ "$active_cursor" != "$CURSOR_RUNTIME_THEME" ]]; then
    echo "Failed to activate cursor theme: expected $CURSOR_RUNTIME_THEME, got $active_cursor" >&2
    exit 1
  fi
}

activate_light_experience
GOREECLOUD_PALETTE_CONFIG="$PALETTE_CONFIG" "$ROOT/scripts/wallpaper.sh" apply default

if [[ "$REPLACE_STOCK" -eq 1 ]]; then
  "$ROOT/scripts/system_wallpapers.sh" plan
  sudo "$ROOT/scripts/system_wallpapers.sh" apply
fi

echo
echo "Installed and activated GoreeCloud desktop assets:"
echo "  Design:         GLAZE UI V1.6 / 1.6.0 Official Anchor (downstream Development)"
echo "  Applications:   $LIGHT_THEME"
echo "  Shell:          $LIGHT_THEME"
echo "  Icons:          $ICON_THEME"
echo "  Cursor asset:   $CURSOR_THEME"
echo "  Cursor runtime: $CURSOR_RUNTIME_THEME"
echo "  Wallpaper:      primary GoreeCloud light wallpaper"
echo "  Gallery:        30 visible (10 Light / 10 Dark / 10 Deep Dark), Light first"
echo "  Live refresh:   GTK, icons, cursor, and Shell settings were re-emitted; cursor revisions use a cache-busting runtime identity"
echo
echo "Theme directory:"
echo "  $THEME_DEST"
echo "Icon/cursor directory:"
echo "  $ICON_DEST"
if [[ "$LEGACY_ICON_DEST" != "$ICON_DEST" ]]; then
  echo "Compatibility discovery links:"
  echo "  $LEGACY_ICON_DEST/$ICON_THEME"
  echo "  $LEGACY_ICON_DEST/$CURSOR_THEME"
  if [[ "$CURSOR_RUNTIME_THEME" != "$CURSOR_THEME" ]]; then
    echo "  $LEGACY_ICON_DEST/$CURSOR_RUNTIME_THEME"
  fi
fi

if [[ "$theme_backed_up" -eq 1 ]]; then
  echo "Previous GoreeCloud theme folders were preserved at:"
  echo "  $THEME_RECOVERY_ROOT"
fi
if [[ "$asset_backed_up" -eq 1 ]]; then
  echo "Previous GoreeCloud icon/cursor folders were preserved at:"
  echo "  $ASSET_RECOVERY_ROOT"
fi
if [[ "$legacy_backed_up" -eq 1 ]]; then
  echo "Previous legacy icon/cursor entries were preserved at:"
  echo "  $LEGACY_RECOVERY_ROOT"
fi

if pgrep -f 'zorin-appearance' >/dev/null 2>&1; then
  echo "Zorin Appearance was already open while desktop assets changed; reopen it to refresh its theme lists."
fi

if [[ "$REPLACE_STOCK" -eq 1 ]]; then
  echo "The audited Zorin stock wallpaper files/catalogs were diverted out of GNOME discovery paths."
  echo "Zorin desktop/artwork packages remain installed."
  echo "Recovery remains available through:"
  echo "  ./scripts/wallpaper.sh replace-stock restore"
else
  echo "The complete GoreeCloud wallpaper catalog is installed user-locally."
  echo "To replace the audited Zorin stock wallpaper gallery later:"
  echo "  ./scripts/wallpaper.sh replace-stock apply"
fi
