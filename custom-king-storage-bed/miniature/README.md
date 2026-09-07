# Modular California king miniature

A 1:10, hand-assembled interpretation of the full-size storage bed. The construction model in the parent directory remains unchanged. This kit prioritizes removable modules, usable drawers, and lateral nightstand movement over reproducing miniature plywood hardware.

![Completed miniature with the two mattresses in place.](assets/closed.png)

## Start here

The finished miniature is **243.2 mm long, 193.0 mm wide, and 91.4 mm high** with the nightstands closed. There are 48 production pieces, made from 11 distinct part files, plus three calibration pieces. Print one copy of a file per job and repeat it according to the quantity table. Do not slice an assembly STEP or the colored scene meshes.

The ready-oriented meshes and exact solids are in `build/parts/`. Corresponding single-part printer files are in `build/gcode/`. `build/manifest.json` is the quantity/orientation list; `build/print-summary.json` and `build/slice-reports/` contain the actual slicer settings, material use, printing time, source hashes, and g-code hashes for this build. Rebuild and re-slice together if any source or fit setting changes.

The [generated print plan](print-plan.md) lists measured per-copy and complete-kit slicer estimates. `build/miniature-print-kit.zip` is the portable print-only bundle with this guide, illustrations, oriented STL/STEP files, and binary g-code.

**First prints:** `fit-channels.bgcode`, `fit-slider.bgcode`, `fit-connectors.bgcode`, one `seam-key.bgcode`, and one `headboard-pin.bgcode`. Then print one `side-module` and one `drawer`, and confirm their fit before producing duplicates. The calibration key and pin count toward the final quantities.

## Part quantities and colors

| File stem | Total copies | MMU slot / recorded filament | Orientation already in STL |
|---|---:|---|---|
| `side-module` | 4 | 3 / silver PLA | Floor down, both bays open upward |
| `center-module` | 2 | 3 / silver PLA | Floor down, cavity upward |
| `drawer` | 8 | 4 / green PLA | Open tray upward |
| `seam-key` | 13 | 3 / silver PLA | Broad face down |
| `foot` | 12 | 3 / silver PLA | Pad down, square peg up |
| `headboard-pin` | 2 | 3 / silver PLA | Flat end down |
| `headboard` | 1 | 3 / silver PLA | Broad back down, not upright |
| `pod-left` | 1 | 1 / red PLA | End cap down, tray vertical |
| `pod-right` | 1 | 1 / red PLA | Mirrored end cap down, tray vertical |
| `base-insert` | 2 | 2 / blue PLA | Lattice down, locators up |
| `mattress` | 2 | 2 / blue PLA | Top down, underside recess up |
| `fit-channels` | 1, calibration only | 3 / silver PLA | Flat base down |
| `fit-slider` | 1, calibration only | 4 / green PLA | Flat down |
| `fit-connectors` | 1, calibration only | 3 / silver PLA | Pockets upward |

The two pods are genuinely handed parts: print one of each, not two copies of the left one. The four side modules and eight drawers are interchangeable. All files use just one MMU lane during a print, with no in-print tool changes or wipe tower. Slot 5 is recorded as black PETG and is not used. Confirm the recorded spools still match the printer before printing; do not substitute PETG into the supplied PLA g-code. The render uses a lighter blue tint for the mattresses to distinguish them from the bases; both are assigned the same blue PLA spool.

## Design contract

The frame consists of four identical outside two-drawer modules and two identical center modules, arranged three across and two long. Thirteen top-loaded butterfly keys join the six modules; twelve removable feet preserve the scaled floor clearance. Eight hollow drawers have integrated fronts and finger notches. One removable headboard locates on two square pins, with two end-cap nightstand trays sliding laterally. Two static adjustable-base envelopes support two separate rigid mattress pieces, hollow underneath with a 2.4 mm top skin and internal ribs to reduce material.

The nominal scale is 1:10. Walls, joints, and clearances are designed in millimeters rather than blindly scaled. Handled walls start at 1.8 mm; the wider module end/back walls support the seam pockets. The separate feet and keys are deliberately simplified miniature hardware, not a reproduction of the full-size support count or load path. The foot fascia is omitted, shortening the model by 0.635 mm.

The headboard is trimmed ahead of the sleep system instead of reproducing the provisional four-inch full-size overlap. Each nightstand has a longer hidden guide tail, allowing 40.64 mm of lateral movement with at least 28 mm still engaged. Drawers pull out 35 mm for display. Neither has a captive stop; both can be removed completely and should be supported by hand when open. The two rigid mattresses are a miniature adaptation of the full-size model's single Flex-Head mattress. The base inserts do not articulate.

## Interfaces and print orientation

| Interface | Assembly behavior | Printing strategy |
|---|---|---|
| Module seams | Butterfly keys drop vertically into paired pockets; lift the sleep system off to remove them. | Modules floor-down and open-top; keys broad-face down. |
| Feet | Square pegs enter the module floor from below. | Flat pads down, pegs up. |
| Drawers | Straight sliding fit in open-top bays; integrated fronts seat at the outside edge. | Open trays up, fronts printed as part of the tray. |
| Headboard | Two square pins locate the housing on the head modules; gravity seats it. | Housing back down; two lateral channel roofs bridge 12.5 mm. |
| Nightstands | End-cap trays slide in straight channels; hidden tails retain guidance when open. | End cap down, tray growing vertically. |
| Mattress/base | Four base locators enter the hollow mattress underside inside its perimeter rim. | Bases lattice-down; mattresses top-down, hollow side up. |

Print one part per job initially. All production parts are supplied in their intended print orientation. Assemblies under `build/closed`, `build/open`, and `build/exploded` are for viewing, not slicing.

## Print settings

The supplied jobs target a Prusa MK4 with a 0.4 mm nozzle and MMU3: 0.15 mm layers, 0.20 mm first layer, four perimeters, 15% gyroid infill, and six top/bottom solid layers. Supports and the wipe tower are explicitly disabled; a 3 mm skirt distance and 0.15 mm elephant-foot compensation are specified. The slicer binds perimeter, solid infill, and infill to the listed single lane. The hollow mattresses print top-down: the complete skin prints on the plate first, then the walls and ribs rise from it, so their large internal cavities do not require bridging.

The headboard, both pods, both mattress jobs, base inserts, feet, keys, and pins use a 3 mm outer brim. Remove it without shaving mating surfaces. Other jobs have no brim. Clean the smooth PEI sheet and inspect the first layer. The headboard's printed channel roofs span 12.5 mm; the small horizontal pin pockets span 4.5 mm at the default fit. Check those openings for sagging before inserting a pod or pin. The pod's tall tray prints from its broad end cap, avoiding a long unsupported shelf.

The largest reserved footprints, including skirt/brim allowance, remain within the 250 x 210 mm plate. All components are supplied at their final size in millimeters: **do not use slicer auto-scale or "fit to bed."** The assembled open model may be wider than the build plate; that does not affect separately printed parts.

## Physical fit gate

No printer-specific clearance measurement is assumed. The default is 0.25 mm **per side** (0.50 mm total across a drawer). Print `fit-channels` in silver PLA and `fit-slider` in green PLA first. One, two, and three raised ticks identify channels with 0.20, 0.25, and 0.35 mm per-side clearance. The slider must move freely without forcing; remove first-layer burrs only before comparing.

Print `fit-connectors`, one `seam-key`, and one `headboard-pin` in silver PLA. Keys and pins should insert and withdraw by hand without forcing. Keep the key and pin for the finished kit; these are production parts, not sacrificial coupons.

If the default binds, rebuild with `--fit 0.35`, regenerate g-code, and repeat the connector and first-drawer checks. If all supplied choices bind or are too loose, stop and measure before revising the geometry. Do not print the whole kit before the coupon, one drawer/module, and one pod/housing fit acceptably. A successful CAD run cannot establish actual friction, bridge quality, adhesion, or strength.

## Assembly sequence

![Exploded view showing the removable sleep system, drawers, keys, and headboard.](assets/exploded.png)

1. **Prepare the parts.** Remove brims, strings, and first-layer burrs. Keep all small parts in a tray. Do not force a tight pin or key: return to the fit gate instead of splitting the receiving wall.
2. **Fit two feet beneath each chassis module.** The square peg enters the matching opening in the module floor. The flat pad sits on the table. These are locating fits, not snap-locks.
3. **Arrange the six chassis modules.** At each end, place one center module between two side modules. Rotate the right-side units 180 degrees on the table so their drawer openings face outward. Bring the two three-module rows together lengthwise.
4. **Install thirteen seam keys from above.** Use two keys along each side-to-center seam: four such seams use eight keys. Across the midpoint seam, use two keys in the left pair, one in the center pair, and two in the right pair: five more. Keys sit flush or slightly recessed. Unused pockets around the outside are intentional consequences of the interchangeable module design.
5. **Insert the eight drawers.** Keep the open side up and finger-notch front facing out. Push each front gently against the outside edge. They should slide by hand; the 35 mm open display position leaves useful support under the tray.
6. **Fit the headboard.** The headboard is at the end nearest the mattress head, with its broad flat back facing away from the bed and its sloping front facing the foot. Put one square pin in each of the two corresponding module-top holes, then lower the housing onto them. The housing rests on the chassis, not on the pins.
7. **Insert the handed nightstands.** Feed each long tray tail into its side channel while keeping the tray open upward. The red end cap continues the headboard's slope when closed. Pull outward no more than about 41 mm for display; support it by hand because there is no captive end stop.
8. **Place the two blue base inserts.** Their long edges run head-to-foot. Place their head edges 25.4 mm from the back end of the chassis, just ahead of the headboard. Center them with 5.08 mm side margins and a 0.6 mm gap between halves; the foot margin is about 4.45 mm. They rest on the module tops without fasteners.
9. **Seat the two mattresses.** Turn them top-up, recess-down, and lower each over the four small locator tabs on its own base. The two pieces remain independently removable.

```text
                    HEADBOARD
             left pod <     > right pod
             +-----------+--------+-----------+
             | side: 2   | center | side: 2   |
             | drawers   |        | drawers   |
             +-----------+--------+-----------+
             | side: 2   | center | side: 2   |
             | drawers   |        | drawers   |
             +-----------+--------+-----------+
                       FOOT
```

![Open display position with side drawers and headboard nightstands extended.](assets/open.png)

To disassemble, lift off the mattresses and bases, remove the headboard and trays, and extract the seam keys. The key's 2.4 mm hole accepts a small hook or bent paperclip for lifting; do not pry against the thin pocket edges. Support the feet when picking up a module because they are intentionally removable.

## Build

Requires the existing build123d environment and the local `cad`, `scad`, and `3d-printer` skill tools used by the parent project.

```sh
bash build.sh
ruby slice.rb
python3 pack.py
```

After measuring coupons, use `bash build.sh --fit 0.35` (or `--fit 0.20`) instead of the first command, then re-slice and repackage. A partial first-article run is also available:

```sh
ruby slice.rb fit-channels fit-slider fit-connectors seam-key headboard-pin
```

`model.py` imports only shared scalar dimensions from `../design.py`. It creates new miniature solids, checks topology, piece count, walls, oriented build-volume limits, assembly collisions, and moving interfaces, then exports individual STEP/STL files and a quantity/color manifest. Build outputs are ignored by git and reproducible from source.

`slice.rb` rejects repaired/non-watertight meshes, checks oriented bed margin, reads the recorded filament state, and verifies the actual printer model, material, layer height, support setting, and active MMU lane in each binary g-code file. It does not change shared printer profiles. A partial named-part run invalidates aggregate totals; run it without names to regenerate the complete report. Per-copy slicer time includes each separate job's overhead, so batching later will produce different totals.

`pack.py` produces the generated print plan, copies the three reviewed assembly illustrations into `assets/`, and creates the portable ZIP. It refuses source, manifest, or g-code mismatches rather than bundling stale toolpaths. Use the source repository for regeneration; the ZIP intentionally contains printable output rather than the development environment.

The inspection loop is CAD assertions, mesh checks, open/closed/exploded renders, slicer output, then physical coupons and first articles. Do not estimate design duration or staffing unless explicitly requested. Slicer-reported printing times describe machine output, not a delivery estimate.

## Scope and handling

This is a desk/display assembly, not a structural prototype or a child's toy. Feet, keys, and pins are small loose parts. Keep them away from young children and pets. Support the chassis when moving the model; do not lift it by the headboard, mattresses, or extended nightstands. No magnets, glue, metal hardware, printer upload, or automatic print start is required.
