#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
CAD_BIN="${CAD_BIN:-$HOME/.agents/skills/cad/scripts/cad}"
RENDER_BIN="${RENDER_BIN:-$HOME/.agents/skills/scad/scripts/render}"

if [[ $# -ne 0 && ! ( $# -eq 2 && "$1" == "--fit" ) ]]; then
  echo "Usage: bash build.sh [--fit 0.20|0.25|0.35]" >&2
  exit 2
fi
"$CAD_BIN" run "$PROJECT_DIR/model.py" "$@"
for state in closed open exploded; do
  "$RENDER_BIN" \
    "$PROJECT_DIR/build/$state/structure.stl:silver" \
    "$PROJECT_DIR/build/$state/drawers.stl:seagreen" \
    "$PROJECT_DIR/build/$state/headboard.stl:silver" \
    "$PROJECT_DIR/build/$state/pods.stl:firebrick" \
    "$PROJECT_DIR/build/$state/bases.stl:royalblue" \
    "$PROJECT_DIR/build/$state/mattresses.stl:lightblue" \
    --views iso,top,front --out "$PROJECT_DIR/build/$state"
done
python3 "$PROJECT_DIR/pack.py" --record-renders
