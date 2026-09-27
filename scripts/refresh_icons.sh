#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
ICON_THEME="GoreeCloud-Zorin"
THEME_ROOT="$DATA_HOME/icons/$ICON_THEME"
REPORT="$THEME_ROOT/goreecloud-normalization-report.json"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  ./scripts/refresh_icons.sh
  ./scripts/refresh_icons.sh --dry-run

Refreshes GoreeCloud's user-local third-party application icon normalization
without modifying application packages or .desktop files.

--dry-run scans and reports what would be normalized without writing wrappers,
rebuilding the icon cache, or cycling the active icon theme.
EOF
}

case "${1:-}" in
  "") ;;
  --dry-run) DRY_RUN=1 ;;
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

if [[ ! -f "$THEME_ROOT/index.theme" ]]; then
  echo "GoreeCloud icon theme is not installed at: $THEME_ROOT" >&2
  echo "Install the desktop experience first with ./scripts/install.sh" >&2
  exit 1
fi

args=(
  "$ROOT/scripts/normalize_app_icons.py"
  --theme-root "$THEME_ROOT"
)
if [[ "$DRY_RUN" -eq 1 ]]; then
  args+=(--dry-run)
else
  args+=(--report "$REPORT")
fi
python3 "${args[@]}"

if [[ "$DRY_RUN" -eq 1 ]]; then
  exit 0
fi

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f "$THEME_ROOT" >/dev/null 2>&1 || true
fi

if command -v gsettings >/dev/null 2>&1; then
  current="$(gsettings get org.gnome.desktop.interface icon-theme 2>/dev/null | tr -d "'" || true)"
  if [[ "$current" == "$ICON_THEME" ]]; then
    gsettings set org.gnome.desktop.interface icon-theme "'Adwaita'"
    sleep 0.35
    gsettings set org.gnome.desktop.interface icon-theme "'$ICON_THEME'"
  fi
fi

echo "Refreshed GoreeCloud application icon normalization."
echo "Report:"
echo "  $REPORT"
