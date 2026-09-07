# 3D Models

Parametric models I've designed for printing, plus a few downloads I've modified. Everything
here is written for a **Prusa MK4 with a 0.4 mm nozzle**, mostly sliced in PrusaSlicer, and
mostly printed in PLA or PETG.

The source of truth is the parametric `.scad` or build123d `.py` file. Meshes, STEP exports, and g-code are build output and are
gitignored — run the project's `build.sh` to regenerate them.

## Projects

| Project | What it is |
|---|---|
| [`custom-king-storage-bed/`](custom-king-storage-bed) | A build123d model of a king storage bed with an adjustable-base envelope, eight drawer faces, and sliding headboard pod geometry. |
| [`custom-king-storage-bed/miniature/`](custom-king-storage-bed/miniature) | A 1:10 printable assembly kit with functional drawers, sliding nightstands, fit coupons, two mattress pieces, and an illustrated print/assembly guide. |
| [`cousin-camp-2026/`](cousin-camp-2026) | A parametric crown/diadem/tiara engine sized to a measured head circumference, and a five-finger piano keyboard designed as a two-colour press-fit assembly. |
| `tornado.scad` | A spiral with a turn-based thickness profile and a reinforced bridge joint. |

## Why parametric

Most printable crowns are a fixed mesh you rescale, and rescaling assumes a circular head.
Heads are ellipses, so a ring sized to circumference ÷ π comes out too short front-to-back
to go on at all. `cousin-camp-2026` exists because solving the ellipse from a tape
measurement is the only version that fits. That is the general pattern here: model the
constraint, not the object.

## Building

OpenSCAD projects require [OpenSCAD](https://openscad.org). The build123d bed project uses the shared `cad` and `scad` skills under `~/.agents/skills`. Each project has its own `build.sh`:

```bash
cd cousin-camp-2026
./build.sh
```

Set `OPENSCAD_BIN` if OpenSCAD is not at `/opt/homebrew/bin/openscad`.

## A note on personal data

Several of these were gifts sized to specific people. Names and body measurements are kept
out of this repository — projects read them from untracked `*.local.sh` files and fall back
to placeholder values, so a fresh clone builds without them. See
[`cousin-camp-2026/README.md`](cousin-camp-2026/README.md#recipients).

## License

[ISC](LICENSE) © 2026 Jonathan Hoyt
