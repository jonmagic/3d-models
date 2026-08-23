# Custom California king storage bed

A conceptual build123d model for the California king storage bed around a Personal Comfort Rego Flex-Head mattress and Power-Flex 3 adjustable base.

`bed.py` is the parametric source of truth. It exports an exact STEP assembly plus separate STL groups for colored review renders. Generated files live under `build/` and are ignored.

`modules.py` is the structural-chassis study. It replaces the pedestal envelope with six transportable carcass modules, five removable laminated crossmembers, eight midpoint through-bolts, and fifteen direct wood supports. Shared dimensions live in `design.py`.

## Working side-elevation geometry

| Dimension | Value |
|---|---:|
| Pedestal length | 96 in |
| Frame width | 76 in |
| Mattress | 72 × 84 × 11 in |
| Power-Flex deck envelope | Two 36 × 84 × 3 in halves, provisional |
| Floor clearance | 5 in |
| Pedestal height | 8 in |
| Mattress top | 27 in |
| Headboard top | 36 in |
| Headboard footprint | 14 in |
| Mattress overlap behind side pod | 4 in, provisional |
| Base drawer faces | Four per long side |

The frame preserves a 2-inch reveal along each mattress side and across the foot. Nine supports form a three-by-three load grid at the head, midpoint, and foot across left, center, and right load paths. The head and foot supports are splayed; the midpoint supports are rectangular. The outer supports and foot ends use a consistent 2.5-inch perimeter inset. The center row supports the seam between the two Power-Flex halves and reduces crossmember spans. Final support dimensions, crossmembers, joinery, leveling feet, and load capacity still require structural design.

The 96-inch wall-to-foot target depends on the provisional 4-inch tuck: 14 inches of headboard depth plus 84 inches of mattress minus 4 inches of overlap plus a 2-inch foot reveal. Removing the tuck produces a 100-inch bed before adding any required wall gap. The new target matches the existing bed’s approximate 96-inch footprint, but that does not establish the room’s measured maximum or leave room for an additional wall gap. Actual clear floor length and full-articulation wallward travel must be measured before freezing this dimension.

## Sleep-system compatibility

Personal Comfort confirms that the current Power-Flex 3 is platform-ready and can rest flat on an existing frame with its legs removed. The Flex-Head California King uses two independently powered halves. Each half has its own control box, power supply, and cord; an optional sync cable can connect the control boxes. The model therefore represents two provisional 36 × 84-inch deck solids, but their exact footprint and 3-inch no-leg height remain envelopes rather than fabrication dimensions.

The manufacturer does not publish the exact support pattern, underside motor/control-box protrusion map, minimum wall clearance, horizontal travel during articulation, cord lengths, or service clearances. Manuals warn that the head can be too close to a wall and require tubing and wiring to remain clear of moving parts. The removable platform layout, 4-inch headboard overlap, rigid clearances, and cable paths cannot be frozen until the delivered halves are identified by law label and measured through their full articulation range.

### Load margin

The required occupant load is 750 pounds: approximately 500 pounds for the two primary sleepers plus another 250 pounds when the children are on the bed. Personal Comfort advertises an 850-pound total distributed capacity for the Power-Flex 3, including mattress, occupants, and bedding. That leaves only 100 pounds for the Rego mattress and bedding. The mattress weight is not verified, and one current Power-Flex manual inconsistently states a 750-pound structural limit while its warranty language references 850 pounds. This is an accepted design-margin risk for the concept, not verified manufacturer compatibility.

The furniture chassis carries a different and larger load: occupants, mattress, bedding, both Power-Flex halves, and the furniture’s supported components. Children climbing or dropping onto the bed also create dynamic loads above the static total. Nine legs reduce spans but do not establish capacity. Crossmembers, connections, center-seam support, leg bearing, floor contact, racking resistance, and an appropriate structural safety margin must be calculated or independently reviewed before construction.

The Rego California King uses two air chambers and two hoses that exit at the mattress head. Personal Comfort instructs placing the air-control unit under the head of the mattress. A 12-inch-wide service drop now connects the open central headboard cavity through its 3/4-inch floor and into the wall-side center notch. This establishes a hose and cable route but does not establish a pump location. No pump shelf or ventilated enclosure is modeled. Pump dimensions, hose length, bend radius, port orientation, cord length, ventilation clearance, and noise are not published.

The system needs accessible power distribution for two Power-Flex supplies, the Rego pump, and any pod/CPAP equipment. No power strip, transformer, surge protector, or cord junction may be permanently buried in the furniture. The measured wall outlet begins approximately 3–4 inches above the floor, reaches approximately 10 inches at the top, and is approximately 32 inches from one bed edge. Its exact side, faceplate dimensions, plug projection, and circuit loading remain to be recorded.

Before construction dimensions are frozen:

- Photograph each Power-Flex law label and identify the applicable OEM/manual.
- Measure both base halves, their no-leg height, center seam, underside protrusions, retainer hardware, cords, control boxes, USB/lighting locations, and optional sync cable.
- Cycle both halves through full articulation away from the wall and measure every wallward, footward, upward, and downward excursion.
- Repeat at candidate wall gaps to establish the minimum nonbinding clearance.
- Measure clear floor length from the wall to the required foot-side walkway limit; do not treat the existing 96-inch bed as the room maximum.
- Measure room width, clear aisle on both sides, and every door, register, nightstand, or other obstruction within the 108-inch open-pod sweep.
- Confirm clearance for each base drawer at full extension and for moving around an open pod.
- Record the doorway, hallway, stair, and turn dimensions that constrain module size and disassembly.
- Measure the delivered pump, both hose exits, hose length and bend radius, pump cord and ports, and observed ventilation/noise needs.
- Record the outlet’s exact lateral edge reference, faceplate bounds, plug projection, and available circuit.
- Resolve base retention on the platform and reserve a hose slack loop that remains clear through full head articulation.

Primary references: [Power-Flex 3 product](https://personalcomfortbed.com/products/power-flex-3), [platform-ready definition](https://hs.personalcomfortbed.com/knowledge-base/what-does-22zero-clearance22-or-22platform-ready22-mean), [Power-Flex manuals](https://hs.personalcomfortbed.com/knowledge-base/owners-manuals-for-adjustable-power-bases), [Personal Comfort mattress owner’s manual](https://cdn.shopify.com/s/files/1/0740/4345/7831/files/personal-comfort-owners-manual-2023.pdf), and [Rejuvenation-series assembly manual](https://cdn.shopify.com/s/files/1/0740/4345/7831/files/Personal-Comfort-Rejuvenation-Series-Instructions-and-Owners-Manual-202203.pdf).

## Headboard cabinet and pull-out pods

The headboard is one full-width sloped cabinet. A centered lower recess allows the 72-inch mattress and Power-Flex deck to tuck 4 inches behind the visible side profile without intersecting the cabinet.

Each end of the headboard stores a 25.625-inch-deep lateral pod sized for a 24-inch drawer slide, a 3/4-inch outer end cap, a 3/4-inch inner retaining wall, and 1/16-inch stops at both ends. Each pod has a five-sided outer cap, a shelf approximately 15 1/8 inches above the floor, a tall back wall, a nominally 2-inch front skirt below the shelf, and an inner retaining wall. The usable edge facing the foot of the bed is open above that short skirt, so the pod functions as a shelf rather than a drawer. In the open configuration each pod slides 16 inches beyond its side of the bed while 9.625 inches remain inside the headboard.

A solid 2-inch-tall fixed rail runs laterally inside each pod cavity. The current clearance envelope raises it 1/16 inch above the cabinet floor; the final design needs a real shim or mounting detail. One slide mounts vertically on each long face of that rail. The moving members attach to the inside of the pod’s 2-inch front skirt and tall back wall, with the shelf spanning across their tops. The slide envelopes are 24 inches long, 2 inches tall, and 3/8 inch thick based on the approximate hardware dimensions; they preserve the slides’ normal side-mount orientation but are not exact hardware models. The model reserves 1/16 inch between the moving pod and the pedestal, between the shelf and fixed rail, and at the slide travel stops. A 22-inch slide can use the same arrangement with a shorter rail. The same slide family is intended for the eight base drawers, but their boxes and hardware are not modeled yet.

The tall outer pod cap creates a large overturning moment if someone leans or sits on an extended pod. Final hardware must be selected and tested for the resulting moment and dynamic load, not only a vertical pound rating. An upper anti-rack guide or second support point may be required.

The wall-facing back of the headboard is mostly open so the bed can be pulled forward for access to adjustable-base power, CPAP, and charging cables. Narrow side stiles plus top and bottom rails preserve the cabinet frame, and the central interior is hollow rather than modeled as a solid block. The continuous bed-facing headboard skin remains intact above the mattress and is modeled as 3/4-inch plywood, including the sloped face.

The left and right drawer chassis continue to the headboard. Only the approximately 24.75-inch-wide center service bay stops 3 inches short of the wall. If the measured 32-inch outlet offset were referenced to an edge of the planned 76-inch frame, it would sit about 6 inches from center inside this notch. This keeps the outlet approximately 3–10 inches above the floor from being trapped behind the 5–13-inch-high pedestal while preserving the visible side carcasses and head-end drawer fronts. The center head leg begins beyond the 3-inch notch. Final outlet position must be remeasured from a permanent wall reference; faceplate, plug, cord, and circuit dimensions also remain to be recorded.

Personal Comfort instructs placing the Rego air-control unit under the head of the mattress. The two air hoses exit at the mattress head, so the open central headboard cavity is reserved as a hose and cable path down to an under-head service bay rather than treating the headboard as the confirmed pump location. Pump dimensions, hose lengths, port orientation, and ventilation clearance are not published and must be measured from the delivered unit.

The light triangular infill remains fixed to the cabinet and does not move with the pod. The pod depth, extension, shelf height, walls, and slide mechanism are provisional pending equipment envelopes and final hardware selection.

## Working material system

Use 3/4-inch furniture-grade plywood as the default carcass, headboard-skin, shelf, partition, and drawer-front thickness unless a structural calculation or hardware interface requires something different. Birch veneer is the current finish candidate. The exact plywood core, veneer grade, exposed-edge treatment, hardwood trim, joinery, and finish are not selected yet. The present pedestal remains an exterior-envelope abstraction; it must be converted into actual 3/4-inch panel carcasses and structural members before producing a cut list.

## Modular structural chassis

The working chassis is divided into six 48-inch-long modules arranged three across and two long. The four side modules are 28 inches wide and provide two drawer bays each. The two 20-inch-wide center modules carry the split-base seam and preserve service space. Head and foot modules meet at the 48-inch midpoint above the middle support row.

Each side module currently includes a 3/4-inch bottom, an inner longitudinal wall, a shallow outer top rail, and three lower transverse bulkheads at the end, drawer-divider, and midpoint interfaces. Eight explicit drawer-box envelopes preserve two openings per side module; each currently reserves 24 inches of depth, at least 20.75 inches of width, and approximately 5.25 inches of internal height before drawer-box and slide clearances. The center modules include bottom panels, outer walls, a doubled center beam, and service-opening bulkheads. The head-center bottom and beam preserve the existing 12-inch outlet and cable route.

Five removable 1.5 × 5.5-inch laminated plywood crossmembers drop into notches at the head, drawer divisions, midpoint, and foot. They bridge left, center, and right modules while resting directly over the transverse bulkheads. The head crossmember is split around the 12-inch service opening. Each crossmember station has three hidden 3.5-inch-square wood supports beneath its left, center, and right load paths, for fifteen supports total. This removes the need for a long steel rail: loads travel from the adjustable base into a laminated crossmember, through a plywood bulkhead and bottom, and almost directly into a support.

At the 48-inch module seam, the paired plywood end bulkheads clamp directly together with eight provisional 3/8-inch through-bolts: three through each side-module pair and two through the center pair outside its service opening. The model includes 7/16-inch clearance holes. The 5.5-inch crossmember depth leaves a 1.75-inch lower bulkhead and 0.875-inch vertical bolt center-to-edge distance, which passes the study's minimum 2d geometry check but still needs tear-out testing in the selected plywood. Large washers or purchased load-spreading hardware, bolt grade, alignment dowels, edge tear-out, and repeated-assembly durability still require selection and testing; no fabricated steel plate is required.

The intended shop work uses ordinary woodworking tools. Break down 3/4-inch plywood with a track saw or table saw, cut the repeated crossmember notches with a router and template, laminate each crossmember from two plywood strips with glue and clamps, and drill the module-seam and leveling-foot holes with a handheld drill or drill press. The support blocks can be cut from ordinary 4×4 stock or laminated from plywood offcuts. Metalwork is limited to installing purchased bolts, washers, alignment dowels, threaded inserts, adjustable levelers, and crossmember hold-down screws; nothing requires cutting or welding steel.

The assembly order is:

1. Build the six plywood carcass modules with glued rabbets or dados and screws appropriate to the selected plywood.
2. Make the five removable laminated crossmembers from the same routed template.
3. Position and level the fifteen support blocks in five rows of three.
4. Set the six modules on the supports and align their midpoint bulkheads with dowels.
5. Clamp each head/foot module pair together with the eight midpoint through-bolts.
6. Drop the five crossmembers into their matching notches and secure them to purchased wood cleats or other face-grain hold-down blocks.
7. Fit the delivered Power-Flex halves, add their measured retention hardware, and route power, air hoses, and service wiring.
8. Install the side skins, drawer faces, foot face, and modular headboard last so the structural fasteners remain serviceable.

The structural screening combines a 2,000-pound distributed chassis load with a 500-pound concentrated edge load on one 34-inch crossmember span. The crossmember is conservatively treated as a simple span, while the shallow plywood bulkhead is treated only as local bearing. For member bending, the point load is placed at midspan; for support and floor bearing, it is placed at the actual 4-inch edge cantilever, producing an approximately 692-pound near-support reaction. The study checks bending stress, L/360 deflection, local plywood bulkhead compression, and a conservative plywood-bearing capacity for the two-bolt center seam against a provisional 250-pound lateral screen equal to 12.5% of the distributed vertical load. Direct supports under all five crossmember stations eliminate the previous unscreened longitudinal span between three leg rows.

The full-depth inner longitudinal plywood walls provide the primary module shear panels. The five crossmembers captured in routed notches tie the three module columns together, and the midpoint bolts clamp the head and foot shear panels together. That is a defined racking path, not a completed racking-stiffness calculation. Edge-load uplift restraint, hold-down cleat sizing, fastener withdrawal, and repetitive motion remain unresolved.

This still does not establish a bed rating. Plywood grade and orientation, glue-lamination quality, bolt grade and tear-out, crossmember fasteners, racking stiffness, adjustable levelers, the actual floor finish, and controlled proof loading remain unresolved.

The Power-Flex support interface also remains provisional. The five crossmember stations are a furniture load path, not confirmation that the adjustable bases may bridge those spaces. Additional bearing rails or slats and field-located bolt plates must follow the delivered bases' stationary chassis, factory mounting points, and permitted support pattern.

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
build/modules/structural-modules.step
build/modules/{head-modules,foot-modules,crossmembers,seam-bolt-envelopes,drawer-envelopes,supports}.stl
build/modules/{exact,colored-structure,colored-drawers}/*.png
build/exact-{closed,open}/*.png
build/colored-{closed,open}/*.png
```
