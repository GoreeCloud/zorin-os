#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LIGHT="GoreeCloud-Glaze"
DARK="GoreeCloud-Glaze-Dark"
THEME_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/themes"

print_value() {
  local label="$1"
  shift
  printf '%-34s %s\n' "$label" "$*"
}

echo "GoreeCloud Glaze native preflight"
echo "================================"

if [ -r /etc/os-release ]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  print_value "Operating system:" "${PRETTY_NAME:-unknown}"
  print_value "Version ID:" "${VERSION_ID:-unknown}"
  print_value "Codename:" "${VERSION_CODENAME:-unknown}"
fi

if command -v gnome-shell >/dev/null 2>&1; then
  print_value "GNOME Shell:" "$(gnome-shell --version 2>/dev/null || true)"
else
  print_value "GNOME Shell:" "not found"
fi

if command -v gsettings >/dev/null 2>&1; then
  print_value "Current GTK theme:" "$(gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null || echo unavailable)"
  print_value "Color scheme:" "$(gsettings get org.gnome.desktop.interface color-scheme 2>/dev/null || echo unavailable)"
  if gsettings list-schemas | grep -Fxq 'org.gnome.shell.extensions.user-theme'; then
    print_value "User Themes schema:" "available"
    print_value "Current Shell theme:" "$(gsettings get org.gnome.shell.extensions.user-theme name 2>/dev/null || echo unavailable)"
  else
    print_value "User Themes schema:" "unavailable"
  fi
else
  print_value "gsettings:" "not found"
fi

if command -v dpkg-query >/dev/null 2>&1; then
  for pkg in libgtk-3-0 libgtk-4-1 libadwaita-1-0; do
    version="$(dpkg-query -W -f='${Version}' "$pkg" 2>/dev/null || true)"
    print_value "$pkg:" "${version:-not installed}"
  done
fi

for theme in "$LIGHT" "$DARK"; do
  if [ -f "$THEME_ROOT/$theme/.goreecloud-theme" ]; then
    print_value "$theme installed:" "yes"
  else
    print_value "$theme installed:" "no"
  fi
done

for variant in "$ROOT/variants/$LIGHT" "$ROOT/variants/$DARK"; do
  [ -s "$variant/gtk-3.0/gtk.css" ] || { echo "Missing GTK 3 source: $variant" >&2; exit 1; }
  [ -s "$variant/gtk-3.0/gtk-dark.css" ] || { echo "Missing GTK 3 dark source: $variant" >&2; exit 1; }
  [ -s "$variant/gtk-4.0/gtk.css" ] || { echo "Missing GTK 4 source: $variant" >&2; exit 1; }
  [ -s "$variant/gtk-4.0/gtk-dark.css" ] || { echo "Missing GTK 4 dark source: $variant" >&2; exit 1; }
  [ -s "$variant/gnome-shell/gnome-shell.css" ] || { echo "Missing Shell source: $variant" >&2; exit 1; }
done

echo
echo "Preflight passed. This is environment/source evidence only."
echo "It does not establish rendered, accessibility, Shell, libadwaita, Stable, or production acceptance."
