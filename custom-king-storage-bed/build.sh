#!/usr/bin/env bash
set -euo pipefail

CAD_BIN="${CAD_BIN:-$HOME/.agents/skills/cad/scripts/cad}"
RENDER_BIN="${RENDER_BIN:-$HOME/.agents/skills/scad/scripts/render}"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

"$CAD_BIN" run "$(dirname "$0")/bed.py"
"$RENDER_BIN" "$PROJECT_DIR/build/custom-king-storage-bed.step" --views iso,front,right,top --out "$PROJECT_DIR/build/exact"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/frame.stl:brown" \
  "$PROJECT_DIR/build/fronts.stl:burlywood" \
  "$PROJECT_DIR/build/deck.stl:slategray" \
  "$PROJECT_DIR/build/mattress.stl:white" \
  "$PROJECT_DIR/build/supports.stl:saddlebrown" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/colored"
