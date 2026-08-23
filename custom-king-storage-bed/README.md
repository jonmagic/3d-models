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

## Provisional front-view geometry

The current model uses an 80-inch overall frame/headboard width, a centered 76-inch mattress and deck, 2-inch side pod zones, a recessed 1.5-inch-deep lower central back, and a 1-inch-thick sloped upper panel above the mattress. These values make the approved side elevation physically coherent without allowing the headboard to intersect the tucked mattress. They are not construction dimensions.

The pod faces preserve the five-sided side profile and parallel angled reveal from the approved elevation. The light triangular infill remains fixed; it shares the drawer-front finish but is not part of the moving pod. The model does not yet define drawer boxes, slides, joinery, the pod shelf cavity, wiring, or the Power-Flex articulation envelope.

## Build

```sh
./build.sh
```

The build fails when dimensional, validity, alignment, count, or interference assertions fail.

Outputs:

```text
build/custom-king-storage-bed.step
build/frame.stl
build/fronts.stl
build/deck.stl
build/mattress.stl
build/supports.stl
build/exact/custom-king-storage-bed-{iso,front,right,top}.png
build/colored/frame-{iso,front,right,top}.png
```
