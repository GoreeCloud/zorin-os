#!/usr/bin/env bash
set -euo pipefail

DEST_ROOT="${THEME_INSTALL_ROOT:-${XDG_DATA_HOME:-$HOME/.local/share}/themes}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

uninstall_variant() {
  local name="$1"
  local destination="$DEST_ROOT/$name"
  local removed="$DEST_ROOT/.goreecloud-removed-$name-$STAMP"

  if [ ! -e "$destination" ]; then
    echo "$name is not installed."
    return
  fi

  if [ ! -f "$destination/.goreecloud-theme" ]; then
    echo "Refusing to remove unmanaged theme directory: $destination" >&2
    exit 1
  fi

  mv "$destination" "$removed"
  echo "Deactivated $name and preserved its files at $removed"
}

uninstall_variant "GoreeCloud-Glaze"
uninstall_variant "GoreeCloud-Glaze-Dark"

echo "The active desktop theme was not changed automatically."
