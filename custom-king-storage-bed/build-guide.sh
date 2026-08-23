#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$PROJECT_DIR/.." && pwd)"
D2_BIN="${D2_BIN:-d2}"
GUIDE_CONVERTER="${GUIDE_CONVERTER:-$HOME/.agents/skills/markdown-to-standalone-html/scripts/markdown_to_standalone_html.rb}"
GUIDE_TEMPLATE="${GUIDE_TEMPLATE:-$HOME/.agents/skills/markdown-to-standalone-html/assets/template.html}"

"$D2_BIN" --pad=40 --layout=dagre \
  "$PROJECT_DIR/guide-assets/build-sequence.d2" \
  "$PROJECT_DIR/guide-assets/build-sequence.svg"

CHASSIS_RENDER="$PROJECT_DIR/build/modules/colored-structure/head-modules-iso.png"
CHASSIS_GUIDE_IMAGE="$PROJECT_DIR/guide-assets/chassis-overview.png"
if [[ -f "$CHASSIS_RENDER" ]]; then
  cp "$CHASSIS_RENDER" "$CHASSIS_GUIDE_IMAGE"
elif [[ ! -f "$CHASSIS_GUIDE_IMAGE" ]]; then
  printf 'Missing chassis overview. Run ./build.sh before ./build-guide.sh.\n' >&2
  exit 1
fi

ruby "$GUIDE_CONVERTER" \
  "$PROJECT_DIR/build-guide.md" \
  --title "California King Storage Bed Build Guide" \
  --template "$GUIDE_TEMPLATE" \
  --out "$REPO_DIR/docs/custom-king-storage-bed/index.html"

ruby "$PROJECT_DIR/guide-freshness.rb" stamp
