#!/usr/bin/env bash
# Regenerate every mesh for the Cousin Camp 2026 headpieces.
#
# STLs and gcode are gitignored, so this script is how you get them back.
# Gems must build before the crowns, because assembly.scad imports the real
# exported gem STLs rather than modelling a second idealised copy.
set -euo pipefail
cd "$(dirname "$0")"
OPENSCAD="${OPENSCAD_BIN:-/opt/homebrew/bin/openscad}"
mkdir -p out

# Who a piece is for, and the size of their head, is personal information and
# does not belong in a public repository. These are placeholder sizes. Put the
# real ones in recipients.local.sh, which is untracked:
#
#   HEADPIECES=(crown:545:one diadem:560:two tiara:505:three)
#   LABEL="NAME"
#
# Each entry is design : head circumference in mm : output slug. The slug is
# optional and defaults to the design name.
HEADPIECES=(crown:550 diadem:570 tiara:500)
LABEL="PIANO"
# shellcheck source=/dev/null
[ -f recipients.local.sh ] && . ./recipients.local.sh

for g in 9:9 8:8 7:7 14:10 10:13 7:4.5; do
    w="${g%%:*}"; h="${g##*:}"
    "$OPENSCAD" -o "out/gem-${w}x${h}.stl" -D "gem_w=$w" -D "gem_h=$h" -D '$fn=64' gem.scad
done

for c in "${HEADPIECES[@]}"; do
    IFS=: read -r d circ slug <<< "$c"
    slug="${slug:-$d}"
    "$OPENSCAD" -o "out/crown-$slug.stl" -D "design=\"$d\"" -D "head_circ=$circ" -D '$fn=96' crown.scad
    "$OPENSCAD" -o "out/gems-$slug.stl"  -D "design=\"$d\"" gemplate.scad
done

for pt in chassis keys; do
    "$OPENSCAD" -o "out/piano-$pt.stl" \
        -D "part=\"$pt\"" -D "label=\"$LABEL\"" -D '$fn=64' piano.scad
done

# PETG chassis: same model, looser press fit. The keys are PLA in both versions,
# so there is no PETG key plate to build.
"$OPENSCAD" -o "out/piano-chassis-petg.stl" \
    -D 'part="chassis"' -D 'material="PETG"' -D "label=\"$LABEL\"" -D '$fn=64' piano.scad
