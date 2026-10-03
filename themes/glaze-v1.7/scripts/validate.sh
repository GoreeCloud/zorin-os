#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
METADATA="$ROOT/metadata/theme.json"
LIGHT="$ROOT/variants/GoreeCloud-Glaze"
DARK="$ROOT/variants/GoreeCloud-Glaze-Dark"

required_files=(
  "$METADATA"
  "$ROOT/README.md"
  "$LIGHT/index.theme"
  "$LIGHT/.goreecloud-theme"
  "$LIGHT/gtk-3.0/gtk.css"
  "$LIGHT/gtk-4.0/gtk.css"
  "$LIGHT/gnome-shell/gnome-shell.css"
  "$DARK/index.theme"
  "$DARK/.goreecloud-theme"
  "$DARK/gtk-3.0/gtk.css"
  "$DARK/gtk-4.0/gtk.css"
  "$DARK/gnome-shell/gnome-shell.css"
  "$ROOT/scripts/install.sh"
  "$ROOT/scripts/uninstall.sh"
)

for file in "${required_files[@]}"; do
  [ -s "$file" ] || { echo "Missing or empty required file: $file" >&2; exit 1; }
done

bash -n "$ROOT/scripts/install.sh"
bash -n "$ROOT/scripts/uninstall.sh"
bash -n "$ROOT/scripts/validate.sh"

python3 - "$METADATA" "$LIGHT" "$DARK" <<'PY'
import json
import pathlib
import sys

metadata_path = pathlib.Path(sys.argv[1])
light = pathlib.Path(sys.argv[2])
dark = pathlib.Path(sys.argv[3])

data = json.loads(metadata_path.read_text(encoding="utf-8"))
assert data["id"] == "com.goreecloud.zorin.theme.glaze-v1-7"
assert data["version"] == "0.1.0-dev.1"
assert data["lifecycle"] == "development"

glaze = data["designSystem"]
assert glaze["product"] == "Glaze V1.7"
assert glaze["version"] == "1.7.0"
assert glaze["lifecycle"] == "anchor"
assert glaze["consumerAcceptance"] == "pending"
assert glaze["verifiedRepositoryRevision"] == "1a5756daed2294155be2e9972b24f580f6222b7b"
assert glaze["sourceQualificationAnchor"] == "7c4ded83d7a8725165bb6a55dfb175667cc9589e"
assert glaze["retainedDev47Included"] is False
assert glaze["section48Included"] is False

expected = {
    light / "gtk-3.0" / "gtk.css": [
        "#EEF3F9", "#172033", "#366CF6", "#244FC6", "#B42318",
        "rgba(54,108,246,0.18)",
    ],
    dark / "gtk-3.0" / "gtk.css": [
        "#0D1119", "#F3F6FB", "#7AA2FF", "#A9C2FF", "#FF8A80",
        "rgba(122,162,255,0.24)",
    ],
}

for path, tokens in expected.items():
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: missing Glaze token {token}"
    assert "backdrop-filter" not in text
    assert text.count("{") == text.count("}"), f"{path}: unbalanced braces"

for variant in (light, dark):
    gtk3 = (variant / "gtk-3.0" / "gtk.css").read_bytes()
    gtk4 = (variant / "gtk-4.0" / "gtk.css").read_bytes()
    assert gtk3 == gtk4, f"{variant.name}: GTK3/GTK4 semantic source drift"
    shell = (variant / "gnome-shell" / "gnome-shell.css").read_text(encoding="utf-8")
    assert shell.count("{") == shell.count("}"), f"{variant.name}: shell CSS braces"
    assert "backdrop-filter" not in shell
    marker = (variant / ".goreecloud-theme").read_text(encoding="utf-8")
    assert f"id={variant.name}" in marker

print("Metadata and semantic CSS checks passed.")
PY

TEST_ROOT="$(mktemp -d)"
THEME_INSTALL_ROOT="$TEST_ROOT/themes" bash "$ROOT/scripts/install.sh"

for variant in GoreeCloud-Glaze GoreeCloud-Glaze-Dark; do
  [ -f "$TEST_ROOT/themes/$variant/.goreecloud-theme" ] || {
    echo "Installer failed to place $variant marker" >&2
    exit 1
  }
done

THEME_INSTALL_ROOT="$TEST_ROOT/themes" bash "$ROOT/scripts/uninstall.sh"

for variant in GoreeCloud-Glaze GoreeCloud-Glaze-Dark; do
  [ ! -e "$TEST_ROOT/themes/$variant" ] || {
    echo "Uninstaller left active directory for $variant" >&2
    exit 1
  }
done

echo "GoreeCloud Glaze V1.7 theme validation passed."
