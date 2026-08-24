#!/usr/bin/env bash
set -euo pipefail

CAD_BIN="${CAD_BIN:-$HOME/.agents/skills/cad/scripts/cad}"
RENDER_BIN="${RENDER_BIN:-$HOME/.agents/skills/scad/scripts/render}"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

"$CAD_BIN" run "$(dirname "$0")/bed.py"
"$CAD_BIN" run "$(dirname "$0")/modules.py"
"$CAD_BIN" run "$(dirname "$0")/integrated.py"
"$RENDER_BIN" "$PROJECT_DIR/build/custom-king-storage-bed-closed.step" --views iso,front,right,top --out "$PROJECT_DIR/build/exact-closed"
"$RENDER_BIN" "$PROJECT_DIR/build/custom-king-storage-bed-open.step" --views iso,front,right,top --out "$PROJECT_DIR/build/exact-open"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/frame.stl:brown" \
  "$PROJECT_DIR/build/fixed-fronts.stl:burlywood" \
  "$PROJECT_DIR/build/pods-closed.stl:tan" \
  "$PROJECT_DIR/build/slide-envelopes-closed.stl:silver" \
  "$PROJECT_DIR/build/deck.stl:slategray" \
  "$PROJECT_DIR/build/mattress.stl:white" \
  "$PROJECT_DIR/build/supports.stl:saddlebrown" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/colored-closed"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/frame.stl:brown" \
  "$PROJECT_DIR/build/fixed-fronts.stl:burlywood" \
  "$PROJECT_DIR/build/pods-open.stl:tan" \
  "$PROJECT_DIR/build/slide-envelopes-open.stl:silver" \
  "$PROJECT_DIR/build/deck.stl:slategray" \
  "$PROJECT_DIR/build/mattress.stl:white" \
  "$PROJECT_DIR/build/supports.stl:saddlebrown" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/colored-open"
"$RENDER_BIN" "$PROJECT_DIR/build/modules/structural-modules.step" --views iso,front,right,top --out "$PROJECT_DIR/build/modules/exact"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/modules/head-modules.stl:lightblue" \
  "$PROJECT_DIR/build/modules/foot-modules.stl:lightgreen" \
  "$PROJECT_DIR/build/modules/crossmembers.stl:mediumpurple" \
  "$PROJECT_DIR/build/modules/seam-bolt-envelopes.stl:silver" \
  "$PROJECT_DIR/build/modules/supports.stl:saddlebrown" \
  "$PROJECT_DIR/build/modules/support-pads.stl:dimgray" \
  "$PROJECT_DIR/build/modules/support-capture-cleats.stl:peru" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/modules/colored-structure"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/modules/head-modules.stl:lightblue" \
  "$PROJECT_DIR/build/modules/foot-modules.stl:lightgreen" \
  "$PROJECT_DIR/build/modules/crossmembers.stl:mediumpurple" \
  "$PROJECT_DIR/build/modules/seam-bolt-envelopes.stl:silver" \
  "$PROJECT_DIR/build/modules/drawer-envelopes.stl:tan" \
  "$PROJECT_DIR/build/modules/supports.stl:saddlebrown" \
  "$PROJECT_DIR/build/modules/support-pads.stl:dimgray" \
  "$PROJECT_DIR/build/modules/support-capture-cleats.stl:peru" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/modules/colored-drawers"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/modules/head-modules.stl:lightblue" \
  "$PROJECT_DIR/build/modules/foot-modules.stl:lightgreen" \
  "$PROJECT_DIR/build/modules/crossmembers.stl:mediumpurple" \
  "$PROJECT_DIR/build/modules/finish-faces.stl:burlywood" \
  "$PROJECT_DIR/build/modules/adapter-envelopes.stl:slategray" \
  "$PROJECT_DIR/build/modules/adapter-support-rails.stl:peru" \
  "$PROJECT_DIR/build/modules/supports.stl:saddlebrown" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/modules/colored-finished"
"$RENDER_BIN" "$PROJECT_DIR/build/integrated-bed-closed.step" --views iso,front,right,top --out "$PROJECT_DIR/build/integrated-exact-closed"
"$RENDER_BIN" "$PROJECT_DIR/build/integrated-bed-open.step" --views iso,front,right,top --out "$PROJECT_DIR/build/integrated-exact-open"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/modules/head-modules.stl:lightblue" \
  "$PROJECT_DIR/build/modules/foot-modules.stl:lightgreen" \
  "$PROJECT_DIR/build/modules/crossmembers.stl:mediumpurple" \
  "$PROJECT_DIR/build/modules/finish-faces.stl:burlywood" \
  "$PROJECT_DIR/build/modules/adapter-envelopes.stl:slategray" \
  "$PROJECT_DIR/build/modules/adapter-support-rails.stl:peru" \
  "$PROJECT_DIR/build/modules/supports.stl:saddlebrown" \
  "$PROJECT_DIR/build/headboard.stl:brown" \
  "$PROJECT_DIR/build/wall-cleat.stl:peru" \
  "$PROJECT_DIR/build/fixed-infills.stl:burlywood" \
  "$PROJECT_DIR/build/pod-rails.stl:saddlebrown" \
  "$PROJECT_DIR/build/pod-module-floors.stl:burlywood" \
  "$PROJECT_DIR/build/pods-closed.stl:tan" \
  "$PROJECT_DIR/build/slide-envelopes-closed.stl:silver" \
  "$PROJECT_DIR/build/deck.stl:slategray" \
  "$PROJECT_DIR/build/mattress.stl:white" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/integrated-colored-closed"
"$RENDER_BIN" \
  "$PROJECT_DIR/build/modules/head-modules.stl:lightblue" \
  "$PROJECT_DIR/build/modules/foot-modules.stl:lightgreen" \
  "$PROJECT_DIR/build/modules/crossmembers.stl:mediumpurple" \
  "$PROJECT_DIR/build/modules/finish-faces.stl:burlywood" \
  "$PROJECT_DIR/build/modules/adapter-envelopes.stl:slategray" \
  "$PROJECT_DIR/build/modules/adapter-support-rails.stl:peru" \
  "$PROJECT_DIR/build/modules/supports.stl:saddlebrown" \
  "$PROJECT_DIR/build/headboard.stl:brown" \
  "$PROJECT_DIR/build/wall-cleat.stl:peru" \
  "$PROJECT_DIR/build/fixed-infills.stl:burlywood" \
  "$PROJECT_DIR/build/pod-rails.stl:saddlebrown" \
  "$PROJECT_DIR/build/pod-module-floors.stl:burlywood" \
  "$PROJECT_DIR/build/pods-open.stl:tan" \
  "$PROJECT_DIR/build/slide-envelopes-open.stl:silver" \
  "$PROJECT_DIR/build/deck.stl:slategray" \
  "$PROJECT_DIR/build/mattress.stl:white" \
  --views iso,front,right,top \
  --out "$PROJECT_DIR/build/integrated-colored-open"
