<style>
:root { color-scheme: light dark; }
html { scroll-behavior: smooth; }
body { font-size: 17px; }
.container { max-width: 900px; }
.status, .decision, .stop, .check { border-radius: 12px; margin: 1rem 0; padding: 1rem; }
.status { background: #fff4ce; border: 2px solid #b45309; color: #3b2f00; }
.decision { background: #e8f4ff; border-left: 5px solid #2563eb; }
.stop { background: #ffe8e8; border-left: 5px solid #b91c1c; }
.check { background: #e9f9ee; border-left: 5px solid #15803d; }
.phase { border: 1px solid var(--subtle-border); border-radius: 14px; margin: 1.5rem 0; padding: 0 1rem 1rem; }
.phase h2 { margin-top: 1rem; }
.tools { color: var(--muted); font-size: 0.95rem; }
nav ul { display: grid; gap: 0.4rem; grid-template-columns: 1fr; list-style: none; padding: 0; }
nav a, .print-button { align-items: center; background: var(--subtle-bg); border: 1px solid var(--subtle-border); border-radius: 10px; color: var(--text); display: flex; min-height: 44px; padding: 0.65rem 0.8rem; }
.print-button { cursor: pointer; font: inherit; width: 100%; }
table { display: block; max-width: 100%; overflow-x: auto; white-space: nowrap; }
th, td { padding: 0.5rem 0.75rem; }
img { background: #1b1f24; }
@media (min-width: 760px) { nav ul { grid-template-columns: repeat(2, 1fr); } }
@media print {
  :root { color-scheme: light; }
  body { background: white; color: black; font-size: 11pt; }
  .container { max-width: none; padding: 0; }
  nav, .print-button { display: none; }
  .phase { break-inside: avoid; }
  h2, h3 { break-after: avoid; }
  img { box-shadow: none; max-height: 7in; object-fit: contain; }
  a { color: black; text-decoration: none; }
}
</style>

# California King Storage Bed Build Guide

<div class="status"><strong>Design review draft—do not cut the final parts yet.</strong> The lower-chassis concept is promising, but the current CAD is not a cut list. Blocking fit, joinery, finish-envelope, adapter, and hardware details are tracked below and must be closed before their affected cuts.</div>

<button class="print-button" onclick="window.print()">Print or save as PDF</button>

This is the phone-first construction guide for a 96×76-inch modular California king storage bed supporting two Power-Flex 3 halves, a Personal Comfort Rego Flex-Head mattress, eight side drawers, and two pull-out headboard shelves. Instructions are intentionally short; each stage ends with a measurable gate.

<div class="check"><strong>Illustration rule:</strong> Every numbered construction step must have an adjacent image that shows the exact parts, orientation, operation, or verification result. A step is not build-ready while its image is missing, provisional, or based on geometry that differs from the released CAD.</div>

## Quick navigation

<nav>
<ul>
<li><a href="#current-decisions">Current decisions</a></li>
<li><a href="#mistakes-and-blockers-found">Mistakes and blockers</a></li>
<li><a href="#phase-0-freeze-the-room-and-finished-envelope">Phase 0: Measure</a></li>
<li><a href="#phase-1-select-materials-and-prove-the-joinery">Phase 1: Materials</a></li>
<li><a href="#phase-2-correct-the-cad-and-release-the-cut-list">Phase 2: Correct CAD</a></li>
<li><a href="#remaining-construction-sequence">Remaining sequence</a></li>
</ul>
</nav>

## Current decisions

<div class="decision"><strong>Lower chassis:</strong> Build a universal six-module lower chassis before the Power-Flex arrives. Add a removable, replaceable top adapter only after measuring the delivered bases.</div>

<div class="decision"><strong>Floor:</strong> The bed sits on newly leveled LVP. Use fifteen equal-height wood support blocks with nearly full-face, LVP-approved non-staining pads. Do not use small metal leveler feet against the floor. Correct minor variation with captured shims above a support block.</div>

<div class="decision"><strong>Materials:</strong> Use flat, structurally rated 23/32-inch veneer-core plywood for hidden load-bearing parts. Use furniture-grade birch plywood, hardwood edging, and deliberate shadow gaps for every visible surface. Measure actual sheet thickness before sizing joinery.</div>

<div class="decision"><strong>Available tools:</strong> Track saw, table saw, sliding compound miter saw, plunge router, router table, circular saw with guide, jigsaw, drill/driver, drill press, random-orbit sander, brad nailer, pocket-hole jig, parallel or pipe clamps, long straightedge, and squares. Structural joints will use fitted dados or rabbets, glue, and appropriate screws; brads and pocket screws are alignment aids rather than the primary load path. The miter saw is reserved for support blocks, hardwood edging, cleats, trim, and controlled bevels—not plywood panels or long crossmember laminations.</div>

<div class="decision"><strong>Guide format:</strong> Maintain this Markdown source and publish a responsive standalone HTML page with embedded images. The same page includes print CSS for a future PDF.</div>

![Current six-module structural concept. Blue is the head half, green is the foot half, purple is the crossmember system, and brown is the direct support grid.](guide-assets/chassis-overview.png)

## Mistakes and blockers found

### B1. The finished envelope and structural envelope conflict

The structural chassis currently occupies the full 76×96-inch target. Adding 3/4-inch side skins, overlay drawer fronts, or a foot fascia outside it would make the finished bed wider or longer and change the 2-inch mattress reveal.

**Required correction:** Model structural carcasses and finish panels together. Recess the visible panels within the 76×96-inch target or intentionally approve a larger finished envelope before generating a cut list.

### B2. “Five crossmembers” is not a physical cut count

There are five load stations, but the head station is split around the 12-inch service opening. The current geometry therefore needs six physical laminated pieces.

**Required correction:** Name and dimension each physical piece separately in the CAD, cut list, labels, and assembly images.

### B3. The CAD uses impossible perfect-fit notches

The crossmembers and their notches are both exactly 1.500 inches wide. Real 23/32-inch sheets vary, glue adds thickness, and a router template has tolerance.

**Required correction:** Measure both laminations, make a full-thickness test coupon, and encode a small verified assembly clearance. Do not choose the clearance from nominal plywood dimensions.

The currently passing plywood-bearing and bolt-edge screens also use a nominal 0.750-inch thickness. Re-run every thickness-dependent check against the measured structural stock; nominal 23/32-inch material is already about four percent thinner.

### B4. The support-height stack is incomplete

The CAD shows 5-inch-tall support blocks with no floor pad, capture pocket, or shim allowance. Adding those parts would raise the bed unless the block is shortened.

**Required correction:** Select the LVP-safe pad and capture method, then calculate `block + pad + captured shim allowance = 5.000 inches`.

### B5. The removable top adapter does not exist yet

The delivered Power-Flex bearing surfaces, moving hardware, wiring, and legal mounting points are unknown. The current crossmembers are a furniture load path, not a base-support interface.

**Required correction:** Add a removable adapter assembly with replaceable rails or plates. Freeze its geometry only after cycling and measuring both delivered halves.

### B6. Crossmember retention and drawer-slide mounting are not detailed

The crossmembers sit in notches but have no selected hold-down. The eight drawers need real slide mounting faces, clearances, screw locations, removal access, and a sequence that still permits chassis disassembly.

**Required correction:** Select the drawer slides and crossmember hold-down method before drilling. Verify that every bolt and screw remains reachable after removing a drawer.

### B7. The exterior and structural models are still separate

The current finished-bed model still shows the old nine-support pedestal abstraction while the structural model uses fifteen supports and real carcasses.

**Required correction:** Generate the guide and cut list from one integrated assembly so a change to structure, skins, drawers, or headboard cannot silently disagree with another model.

### B8. The headboard is not yet a buildable module set

The exterior shape is modeled, but panel seams, pod cassettes, joinery, chassis attachment, wall clearance, anti-racking guides, and equipment access are not defined.

**Required correction:** Design and carry-test separate left pod, center cabinet, and right pod modules before producing headboard cuts.

### B9. The proof-load procedure is undefined

The calculations are screening checks, not a furniture rating. Racking stiffness, fastener withdrawal, plywood tear-out, pad behavior on LVP, and dynamic use remain unresolved.

**Required correction:** Define a staged proof load, inspection points, stop conditions, and post-load measurements before anyone sleeps on the bed.

## Build sequence

![The build remains reversible until the chassis is square and the delivered Power-Flex halves define the removable adapter.](guide-assets/build-sequence.svg)

<div class="phase">

## Phase 0: Freeze the room and finished envelope

**Tools:** 25-foot tape, laser measure, painter’s tape, level, square, phone camera, cardboard or scrap strips.

1. Choose one permanent wall corner as the room datum. Record every measurement from that corner and the finished floor.
2. Measure room width, usable wall-to-foot length, side walkways, baseboard projection, outlet faceplate, plug projection, register locations, and door swing.
3. Tape a 76×96-inch rectangle on the LVP. Add the 16-inch open-pod sweep on both sides and the planned drawer extension.
4. Carry a rigid 48×28-inch rectangle through the workshop-to-bedroom route. Test every doorway, hallway turn, stair, and ceiling pinch point.
5. Photograph the taped footprint from the head, foot, and both sides with the tape markings visible.
6. Record whether adding finish panels inside the 76×96-inch target leaves acceptable internal space. Do not assume exterior skins can be added outside the current chassis.

<div class="stop"><strong>Stop:</strong> Do not freeze module widths or lengths until the finished 76×96-inch envelope includes skins, fronts, fascia, gaps, and service clearance.</div>

<div class="check"><strong>Pass when:</strong> The taped bed and every open drawer/pod fit the room; a 48×28-inch route template reaches the bedroom; and one dimensioned room sketch uses a single wall datum.</div>

</div>

<div class="phase">

## Phase 1: Select materials and prove the joinery

**Tools:** calipers, straightedge, track saw, table saw, plunge router, guide bushing or pattern bit, drill/driver, drill press, square, clamps.

1. Select the exact structural plywood product. Reject MDF core, particle core, visibly warped sheets, delaminated edges, and sheets with large core voids.
2. Measure each candidate sheet at ten perimeter and field locations. Record minimum, maximum, and typical thickness.
3. Cut two small joint coupons from the real stock: one bottom-to-wall joint and one doubled crossmember with its receiving notch.
4. Use a rabbet or dado sized from the measured stock, not from “3/4 inch.” Keep at least two full outer plies beyond the dado floor.
5. Glue and screw the bottom-to-wall coupon using the planned fastener and pilot hole. After cure, inspect for splitting, stripped threads, rocking, and glue starvation.
6. Laminate the crossmember coupon on a flat caul. After cure, measure its actual thickness at both ends and the middle.
7. Route a test notch from the planned template. The laminated coupon must seat by hand without hammering, remain removable, and show no visible side play.

<div class="stop"><strong>Stop:</strong> Do not route module parts using a nominal 1.500-inch notch or an untested template.</div>

<div class="check"><strong>Pass when:</strong> The chosen sheets are flat, the recorded material properties support the structural screen, the joint coupon stays square, and the crossmember coupon repeatedly seats and removes without damage.</div>

</div>

<div class="phase">

## Phase 2: Correct the CAD and release the cut list

1. Integrate the six structural modules, birch finish skins, overlay drawer fronts, foot fascia, and headboard attachment into one assembly.
2. Keep the finished dimensions at the approved room envelope. Recalculate the structural module widths and lengths around the finish thicknesses and reveal gaps.
3. Replace nominal plywood thicknesses with measured material parameters.
4. Add the verified notch clearance from the coupon test.
5. Model the LVP pad, support-block height, capture pocket, and any top-side shim allowance.
6. Split the five load stations into six named physical crossmember parts.
7. Add crossmember hold-downs, accessible seam-bolt washers, alignment dowels, and tool-clearance envelopes.
8. Add the removable top-adapter envelope without drilling final Power-Flex holes.
9. Export one labeled exploded view per module and one dimensioned drawing per unique panel.
10. Generate a cut list grouped by material, thickness, grain direction, edge treatment, and stage.

<div class="stop"><strong>Stop:</strong> A render is not a cut list. Do not release cuts while any solid is only an unlabeled envelope or any required fastener lacks installation access.</div>

<div class="check"><strong>Pass when:</strong> The integrated CAD stays inside the finished envelope, all assembly clearances are measured, every part has a unique label, and the complete bed can be assembled and disassembled in the modeled order.</div>

</div>

## Remaining construction sequence

The following sections will gain concise instructions and purpose-built images as their blocking design details are resolved:

1. Fabricate and pad the fifteen direct support blocks.
2. Build the two center carcass modules.
3. Build one side carcass as the master, verify it, then repeat the other three.
4. Dry-fit all six modules; square, level, bolt, and rack-test the lower chassis.
5. Laminate, fit, label, and retain the six physical crossmember pieces.
6. Measure the delivered Power-Flex halves through full articulation.
7. Build and install the removable top adapter.
8. Build drawer boxes and install slides while preserving bolt access.
9. Build the three-part headboard and two pod cassettes.
10. Fit birch skins, drawer fronts, foot fascia, edge treatment, and finish.
11. Route accessible power, pump hoses, and articulation-safe cable slack.
12. Perform controlled proof loading and final inspection.

## Guide image plan

Every numbered construction step will include at least one directly adjacent image. The complete image set will use:

- CAD exploded views for part placement and orientation.
- Dimensioned orthographic drawings for cuts, holes, dados, and clearances.
- Close-up joint diagrams for glue, screws, bolts, dowels, slides, and retainers.
- Assembly-state images showing what the bed should look like before continuing.
- Photo-style verification callouts for square, flush, level, accessible, and correctly oriented checks.

Repeated operations may reference one master image only when the released CAD proves the geometry and procedure are identical.
