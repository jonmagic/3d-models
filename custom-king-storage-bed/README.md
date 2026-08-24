# Custom California king storage bed

Parametric build123d models and an illustrated construction guide for a modular California king storage bed around two Personal Comfort Power-Flex adjustable-base halves and a Rego Flex-Head mattress.

## Current geometry

| Dimension | Value |
|---|---:|
| Finished bed | 96 × 76 in |
| Hidden structural chassis | 95.75 × 74.5 in |
| Mattress | 72 × 84 × 11 in |
| Power-Flex envelope | Two 36 × 84 × 3 in halves, provisional |
| Floor clearance | 5 in |
| Furniture chassis | 8 in |
| Removable adapter | 1/4 in blank, field cut after delivery |
| Provisional mattress top | 27.25 in |
| Headboard top | 36 in |
| Mattress overlap behind headboard | 4 in, provisional |
| Drawers | Eight, four per long side |

The finished dimensions include 3/4-inch side finish faces and a 1/4-inch foot fascia. Hidden module dimensions are calculated inside that envelope: four side modules are 47.875 × 27.25 inches and two center modules are 47.875 × 20 inches.

## Models

- `design.py` contains shared dimensions, material assumptions, load cases, and sleep-system geometry.
- `modules.py` generates the six structural modules, six physical crossmember pieces at five load stations, seventeen supports and pads, four-sided support capture, independent drawer-slide carriers, longitudinal adapter-support rails, finish faces, drawer envelopes, seam-bolt holes, and two removable adapter blank envelopes.
- `bed.py` generates the wall-anchored headboard, pod module floors and pull-out concepts, Power-Flex envelopes, mattress, and the retired pedestal concept retained for comparison.
- `integrated.py` combines the real modular chassis from `modules.py` with the headboard, pods, Power-Flex envelopes, and mattress from `bed.py`. This is the assembly used for finished-envelope review.
- `guide-images.py` generates the twenty dimensioned SVG construction diagrams from the same shared parameters.

Generated CAD and render files live under `build/` and are ignored. The guide diagrams under `guide-assets/steps/` and the standalone HTML under `docs/` are committed.

## Structural concept

The lower chassis is six transportable plywood carcasses arranged three across and two long. Four side modules hold two drawers each. Two center modules carry the split-base seam and preserve a 12-inch service route at the wall.

Five crossmember stations are directly supported. Station A uses supports at Y = -33.25, -8, 0, +8, and +33.25 inches: the two split members each bear on an outer and inner support while the center support carries the wall-side center beam. Stations B–E use supports at Y = -33.25, 0, and +33.25 inches, producing seventeen supports total. The head station is split around the service opening, so the physical cut count is six crossmember pieces. Each member is laminated from two measured 23/32-inch plywood strips for a nominal 1.4375-inch width and 5.5-inch depth. Receiving notches start with 1/32-inch modeled clearance, but final router templates must follow a full-thickness coupon made from the purchased sheets.

The supports are 3.5-inch-square wood blocks shortened by the selected pad thickness so the floor-to-module stack remains exactly 5 inches. Each support retains its full footprint on a nearly full-face, non-staining pad approved for the installed LVP. Four underside cleats capture each block in both axes while leaving it removable. Minor leveling corrections use captured shims above a support, never point levelers against the LVP.

At the 47.875-inch module seam, paired plywood bulkheads clamp together with eight provisional 3/8-inch through-bolts: three per side pair and two through the center pair outside the service route. The working washer OD is 1.25 inches, leaving 0.266 inch to each edge of the 1.78125-inch lower bulkhead. The current screen covers plywood bearing and bolt edge distance, not final connection behavior, tear-out, or repeated assembly. Crossmember retention is a release gate: the rejected A21Z detail requires screws that protrude through this plywood geometry, so a removable hardwood keeper system using broad faces and backed machine or through-bolt hardware must be proven at full scale.

Each drawer uses a raised, full-depth fixed carrier web rather than a removable crossmember as its mounting face. Every bay preserves at least a 19.34 × 24 × 5.28-inch envelope before the selected slide clearances and drawer-box construction are applied. A modeled 1-inch socket envelope passes beneath the carriers with 0.391 inch of vertical clearance so all midpoint seam bolts remain serviceable after drawer removal.

The structural screen uses a 2,000-pound distributed chassis load plus a 500-pound concentrated edge load. The current model reports 676 psi crossmember bending stress against a 1,000 psi screening limit, 0.0235-inch deflection against an L/360 limit of 0.0924 inch, and 276 psi worst local bulkhead compression against a 300 psi screen. These calculations are design screens, not a furniture rating. Material qualification, connection tests, racking tests, and controlled proof loading remain mandatory.

## Power-Flex adapter

The universal lower chassis can be built before the adjustable bases arrive. Two replaceable 1/4-inch 36 × 84-inch adapter blanks sit between the furniture and the Power-Flex halves. After delivery, each base is measured through full articulation. Stationary bearing lines, moving no-go zones, motors, controls, wiring, and factory mounting points are transferred to its adapter blank. The blank is then cut into an open lattice, with replaceable backing added only at verified factory mounting points.

The 1/4-inch lattice is a template and locator, not a structural bridge. Every delivered base-bearing line requires continuous support beneath it. Eight modeled outer longitudinal rails cover the current planning envelope; additional field-fitted rails must be removable between crossmember stations wherever the delivered underside map requires them.

The adapter is intentionally not a released cut part. Do not drill or modify a Power-Flex chassis unless its applicable manufacturer documentation expressly authorizes the exact hole or threaded socket. The 1/4-inch adapter raises the provisional mattress top from 27 to 27.25 inches.

Personal Comfort describes the Power-Flex 3 as platform-ready with its legs removed, but exact underside geometry and permitted retention details are not published. The delivered law labels and applicable manuals are authoritative.

## Load compatibility warning

The required occupant load is 750 pounds: approximately 500 pounds for the two primary sleepers plus another 250 pounds when the children are on the bed. Personal Comfort publishes an 850-pound Power-Flex capacity without stating whether it applies to one half or the paired sleep surface, or which loads it includes. An evenly shared occupant comparison is approximately 375 pounds per half before mattress and bedding loads, but that is not a manufacturer rating. Written manufacturer interpretation, delivered labels and manuals, and the actual mattress weight remain required. This is a product-compatibility risk independent of the furniture chassis screen.

## Headboard and pods

The headboard is full width and divides into a left pod module, center cabinet, and right pod module for transport. A removable two-part wall cleat anchored to verified framing is the primary gravity and pod-overturning path; lower chassis bolts locate the headboard but are not the primary anti-tip restraint. The wall-facing back remains serviceable. A 12-inch central route carries the two mattress air hoses, two adjustable-base power systems, and pump connections without burying power strips or service connections. The current product page says paired bases synchronize without a cable.

Each side pod pulls laterally from the headboard and becomes a small shelf for CPAP equipment and charging. The working hardware is one pair of Accuride 9308-E16 side-mount slides per pod: 16-inch full travel, 3-inch height, 0.75-inch side space, non-disconnect, and lock-in/lock-out. This corrects the previous non-buildable 24 × 2 × 0.375-inch envelope while preserving the desired 16-inch extension. Each fixed rail bears on a dedicated 3/4-inch pod-module floor and requires through-bolted reinforced backing checked for downward and uplift reactions. The final pod cassette still requires an upper anti-rack guide, positive travel stops, a full-size mockup, load testing, and an explicit no-sitting/no-climbing limitation.

The wall-cleat anchors, pod rail connections, crossmember keepers, complete furniture connections, and proof-load target require qualified review. The proof-load review must include the building floor structure, not only the furniture and LVP.

## Build and guide

```sh
./build.sh
./build-guide.sh
ruby guide-freshness.rb check
```

`build.sh` validates the exterior concept, modular chassis, and integrated assembly, then renders exact and colored views. `build-guide.sh` regenerates the D2 sequence, twenty SVG construction diagrams, integrated overview, standalone embedded-image HTML, and freshness stamp.

Primary outputs:

```text
build/integrated-bed-{closed,open}.step
build/modules/structural-modules.step
build/integrated-{exact,colored}-{closed,open}/*.png
build/modules/{exact,colored-structure,colored-drawers,colored-finished}/*.png
guide-assets/steps/*.svg
docs/custom-king-storage-bed/index.html
```

The Markdown guide is the editable source. Every numbered construction step has an adjacent generated illustration and a measurable pass gate. Browser print CSS supports saving the same guide as a PDF.
