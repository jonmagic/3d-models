# Custom king storage bed

A conceptual build123d model for the king storage bed around a Personal Comfort Rego Flex-Head mattress and Power-Flex 3 adjustable base.

`bed.py` is the parametric source of truth. It exports an exact STEP assembly plus separate STL groups for colored review renders. Generated files live under `build/` and are ignored.

## Settled side-elevation geometry

| Dimension | Value |
|---|---:|
| Pedestal length | 90 in |
| Mattress | 76 × 80 × 11 in |
| Power-Flex deck envelope | 76 × 80 × 3 in |
| Floor clearance | 5 in |
| Pedestal height | 8 in |
| Mattress top | 27 in |
| Headboard top | 36 in |
| Headboard footprint | 14 in |
| Mattress overlap behind side pod | 4 in, provisional |
| Base drawer faces | Four per long side |

The mattress, deck, and pedestal foot edges align. The outer supports are splayed and the center supports are rectangular.

## Headboard cabinet and pull-out pods

The headboard is one full-width sloped cabinet. A centered lower recess allows the 76-inch mattress and Power-Flex deck to tuck 4 inches behind the visible side profile without intersecting the cabinet.

An 18-inch-wide pod is stored laterally inside each end of the headboard. Each pod has a five-sided outer cap, a 26-inch-high shelf, a rear wall, and an inner retaining wall. In the open configuration each pod slides 16 inches beyond its side of the bed while 2 inches remain captured in the headboard, making the exposed shelf function like a compact nightstand for a CPAP and charging stand.

The light triangular infill remains fixed to the cabinet and does not move with the pod. The pod width, extension, shelf height, walls, and slide mechanism are provisional pending front-view dimensions, equipment envelopes, and hardware selection.

## Build

```sh
./build.sh
```

The build fails when dimensional, validity, alignment, count, or interference assertions fail.

Outputs:

```text
build/custom-king-storage-bed.step
build/custom-king-storage-bed-closed.step
build/custom-king-storage-bed-open.step
build/frame.stl
build/fixed-fronts.stl
build/pods-closed.stl
build/pods-open.stl
build/deck.stl
build/mattress.stl
build/supports.stl
build/exact-{closed,open}/*.png
build/colored-{closed,open}/*.png
```
