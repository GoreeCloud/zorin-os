#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VARIANTS_DIR="$PACKAGE_DIR/variants"
DEST_ROOT="${THEME_INSTALL_ROOT:-${XDG_DATA_HOME:-$HOME/.local/share}/themes}"
APPEARANCE=""
APPLY_SHELL=0

usage() {
  cat <<'USAGE'
Usage: bash install.sh [--apply light|dark] [--apply-shell]

Installs both GoreeCloud Glaze variants into the current user's theme directory.
No active GTK or Shell theme is changed unless --apply is supplied.
--apply-shell requires --apply and a compatible GNOME User Themes extension.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --apply)
      [ "$#" -ge 2 ] || { echo "Missing value for --apply" >&2; exit 2; }
      APPEARANCE="$2"
      shift 2
      ;;
    --apply-shell)
      APPLY_SHELL=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$APPEARANCE" in
  ""|light|dark) ;;
  *)
    echo "--apply must be light or dark" >&2
    exit 2
    ;;
esac

if [ "$APPLY_SHELL" -eq 1 ] && [ -z "$APPEARANCE" ]; then
  echo "--apply-shell requires --apply light|dark" >&2
  exit 2
fi

mkdir -p "$DEST_ROOT"

install_variant() {
  local name="$1"
  local source="$VARIANTS_DIR/$name"
  local destination="$DEST_ROOT/$name"
  local staging
  local backup
  local stamp

  [ -f "$source/.goreecloud-theme" ] || {
    echo "Refusing to install $name: package marker is missing." >&2
    exit 1
  }

  if [ -e "$destination" ]; then
    if [ ! -f "$destination/.goreecloud-theme" ]; then
      echo "Refusing to replace unmanaged theme directory: $destination" >&2
      exit 1
    fi
    stamp="$(date -u +%Y%m%dT%H%M%SZ)"
    backup="$DEST_ROOT/.goreecloud-backup-$name-$stamp"
    mv "$destination" "$backup"
    echo "Preserved previous managed theme at $backup"
  fi

  staging="$(mktemp -d "$DEST_ROOT/.goreecloud-stage-$name.XXXXXX")"
  cp -a "$source/." "$staging/"
  mv "$staging" "$destination"
  echo "Installed $name -> $destination"
}

install_variant "GoreeCloud-Glaze"
install_variant "GoreeCloud-Glaze-Dark"

if [ -n "$APPEARANCE" ]; then
  if [ "$APPEARANCE" = "dark" ]; then
    ACTIVE_THEME="GoreeCloud-Glaze-Dark"
  else
    ACTIVE_THEME="GoreeCloud-Glaze"
  fi

  if command -v gsettings >/dev/null 2>&1; then
    gsettings set org.gnome.desktop.interface gtk-theme "$ACTIVE_THEME"
    echo "Applied GTK theme: $ACTIVE_THEME"

    if [ "$APPLY_SHELL" -eq 1 ]; then
      if gsettings list-schemas | grep -Fxq 'org.gnome.shell.extensions.user-theme'; then
        gsettings set org.gnome.shell.extensions.user-theme name "$ACTIVE_THEME"
        echo "Applied GNOME Shell theme: $ACTIVE_THEME"
      else
        echo "GNOME User Themes settings schema is unavailable; Shell theme was not changed." >&2
      fi
    fi
  else
    echo "gsettings is unavailable; themes were installed but not applied." >&2
  fi
fi
