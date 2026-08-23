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

Each end of the headboard stores a 24.75-inch-deep lateral pod sized for a 24-inch drawer slide plus the 3/4-inch outer end cap. Each pod has a five-sided outer cap, a bottom shelf 14.5 inches above the floor, a rear wall, a shallow front apron, and an inner retaining wall. In the open configuration each pod slides 16 inches beyond its side of the bed while 8.75 inches remain inside the headboard, making the drawer bottom function like a compact nightstand shelf for a CPAP and charging stand.

Two vertically oriented slide envelopes run behind the rear wall and front apron of each pod. The envelopes are 24 inches long, 2 inches tall, and 3/8 inch thick based on the approximate hardware dimensions; they reserve clearance and show the mounting concept but are not exact hardware models. A localized rear mounting strip and the continuous front cabinet rail provide the fixed mounting surfaces. A 22-inch slide can use the same arrangement with shorter mounting blocks. The same slide family is intended for the eight base drawers, but their boxes and hardware are not modeled yet.

The wall-facing back of the headboard is mostly open so the bed can be pulled forward for access to adjustable-base power, CPAP, and charging cables. Narrow side stiles plus top and bottom rails preserve the cabinet frame. Localized horizontal strips remain behind the rear slide of each pod; the rest of the back is open rather than covered by a full panel.

The light triangular infill remains fixed to the cabinet and does not move with the pod. The pod depth, extension, shelf height, walls, and slide mechanism are provisional pending equipment envelopes and final hardware selection.

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
build/slide-envelopes-closed.stl
build/slide-envelopes-open.stl
build/deck.stl
build/mattress.stl
build/supports.stl
build/exact-{closed,open}/*.png
build/colored-{closed,open}/*.png
```
