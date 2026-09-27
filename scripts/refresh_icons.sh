#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
GoreeCloud third-party runtime icon normalization is currently disabled.

The first wrapper implementation failed representative Zorin OS 17.3 visual
acceptance because original third-party artwork did not render reliably inside
the generated wrappers. The safe GoreeCloud icon theme now inherits original
third-party application artwork instead.

Use this to reinstall the safe base icon theme:
  bash ./scripts/install_icons.sh
EOF
