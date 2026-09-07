# Miniature bed print order and machine estimates

Scale 1:10; 0.25 mm per-side fit; 48 production pieces. Use the illustrated [assembly guide](README.md) and its physical fit gates before printing duplicates.

This print-only bundle includes pre-oriented STL, exact STEP, and single-part binary g-code. Regenerate from `custom-king-storage-bed/miniature/` in the source repository, not by scaling an assembly mesh. No printer upload or start is performed by these scripts.

## Print first

Print the three calibration pieces, one production seam key, and one production headboard pin. Then test one drawer with one side module. Confirm one left pod with the headboard before producing the second pod. Keys, pins, and first articles count toward the production quantities below.

## Complete job list

Each file contains one copy, already oriented. Repeat the job to reach the total quantity. Do not print this entire list before the fit samples pass.

The sleep system uses one each of `base-insert`, `mattress`, `base-raised`, and `mattress-raised`. The head-up pair has a fixed 15.24 mm rise over 60.96 mm (14.036 degrees), matching 6 inches over a 24-inch run at full scale. Keep each mattress with its matching support.

| File | Total copies | Slot / PLA color | Size X x Y x Z, mm | Brim | Time per copy | Filament per copy |
|---|---:|---|---|---:|---|---:|
| [`side-module.bgcode`](build/gcode/side-module.bgcode) | 4 | 3 / silver | 121.6 x 69.2 x 20.3 | 0 mm | 1h 36m 2s | 48.78 g |
| [`center-module.bgcode`](build/gcode/center-module.bgcode) | 2 | 3 / silver | 121.6 x 50.8 x 20.3 | 0 mm | 1h 34m 55s | 45.50 g |
| [`drawer.bgcode`](build/gcode/drawer.bgcode) | 8 | 4 / green | 60.3 x 19.8 x 62.5 | 3 mm | 1h 6m 39s | 14.68 g |
| [`seam-key.bgcode`](build/gcode/seam-key.bgcode) | 13 | 3 / silver | 12.0 x 10.0 x 5.0 | 3 mm | 5m 56s | 0.79 g |
| [`foot.bgcode`](build/gcode/foot.bgcode) | 12 | 3 / silver | 8.9 x 8.9 x 14.1 | 3 mm | 12m 56s | 1.19 g |
| [`headboard-pin.bgcode`](build/gcode/headboard-pin.bgcode) | 2 | 3 / silver | 4.0 x 4.0 x 3.6 | 3 mm | 1m 41s | 0.31 g |
| [`headboard.bgcode`](build/gcode/headboard.bgcode) | 1 | 3 / silver | 58.4 x 188.7 x 24.9 | 3 mm | 3h 27m 0s | 98.33 g |
| [`pod-left.bgcode`](build/gcode/pod-left.bgcode) | 1 | 1 / red | 24.9 x 58.4 x 72.0 | 3 mm | 1h 13m 10s | 9.44 g |
| [`pod-right.bgcode`](build/gcode/pod-right.bgcode) | 1 | 1 / red | 24.9 x 58.4 x 72.0 | 3 mm | 1h 13m 14s | 9.44 g |
| [`base-insert.bgcode`](build/gcode/base-insert.bgcode) | 1 | 2 / blue | 213.4 x 91.1 x 9.5 | 3 mm | 39m 44s | 19.92 g |
| [`mattress.bgcode`](build/gcode/mattress.bgcode) | 1 | 2 / blue | 213.4 x 91.1 x 27.9 | 3 mm | 3h 12m 39s | 112.70 g |
| [`base-raised.bgcode`](build/gcode/base-raised.bgcode) | 1 | 2 / blue | 213.4 x 91.1 x 23.5 | 3 mm | 1h 2m 11s | 30.89 g |
| [`mattress-raised.bgcode`](build/gcode/mattress-raised.bgcode) | 1 | 2 / blue | 213.4 x 43.2 x 91.1 | 3 mm | 7h 20m 14s | 194.82 g |
| [`fit-channels.bgcode`](build/gcode/fit-channels.bgcode) | 1 (sample) | 3 / silver | 82.0 x 32.0 x 7.0 | 0 mm | 19m 11s | 8.42 g |
| [`fit-slider.bgcode`](build/gcode/fit-slider.bgcode) | 1 (sample) | 4 / green | 15.0 x 22.0 x 5.0 | 0 mm | 6m 15s | 1.61 g |
| [`fit-connectors.bgcode`](build/gcode/fit-connectors.bgcode) | 1 (sample) | 3 / silver | 34.0 x 24.0 x 8.0 | 0 mm | 13m 40s | 5.02 g |

**Production totals:** 40h 31m 04s and 904.27 g. **Three calibration pieces:** 0h 39m 06s and 15.05 g, in addition to production totals. The tested key and pin are already included in production totals.

These are PrusaSlicer estimates summed across separate single-copy jobs, not elapsed project time. They exclude loading, unloading, plate cleaning, cooldown, assembly, retries, and failed prints. Batching or changing profiles will change the numbers.

All jobs use 0.15 mm layers, 0.20 mm first layer, four perimeters, 15% gyroid infill, and six top/bottom solid layers, with supports disabled and no in-print tool changes. Slot 5 PETG is unused. Confirm the actual PLA spools match before printing.

Source and g-code SHA-256 hashes are recorded per part in `build/print-summary.json`; packaging refuses mismatches. The STL is the slicing derivative; parametric source lives in the repository.
