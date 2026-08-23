#!/usr/bin/env python3
"""Conceptual parametric model for the custom king storage bed."""

from pathlib import Path

from build123d import Align, Box, Compound, Face, Pos, Vector, Wire, export_step, export_stl, extrude, fillet
from checks import Report, volume_of

IN = 25.4


def inches(value: float) -> float:
    return value * IN


def box(length: float, width: float, height: float, x: float, y: float, z: float):
    solid = Box(
        inches(length),
        inches(width),
        inches(height),
        align=(Align.MIN, Align.MIN, Align.MIN),
    )
    return Pos(inches(x), inches(y), inches(z)) * solid


def profile(points: list[tuple[float, float]], y_min: float, y_max: float):
    vertices = [Vector(inches(x), inches(y_min), inches(z)) for x, z in points]
    face = Face(Wire.make_polygon(vertices, close=True))
    return extrude(face, amount=inches(y_max - y_min), dir=(0, 1, 0))


def compound(parts: list):
    return Compound(parts)


# Working side-elevation dimensions. Delivered sleep-system measurements remain authoritative.
MATTRESS_LENGTH = 84.0
MATTRESS_WIDTH = 72.0
MATTRESS_HEIGHT = 11.0
MATTRESS_SIDE_MARGIN = 2.0
MATTRESS_FOOT_MARGIN = 2.0
DECK_HEIGHT = 3.0
FLOOR_CLEARANCE = 5.0
PEDESTAL_HEIGHT = 8.0
HEADBOARD_HEIGHT = 36.0
HEADBOARD_DEPTH = 14.0
HEADBOARD_TOP_DEPTH = 7.0
MATTRESS_OVERLAP = 4.0
OVERALL_LENGTH = HEADBOARD_DEPTH + MATTRESS_LENGTH - MATTRESS_OVERLAP + MATTRESS_FOOT_MARGIN
FRAME_WIDTH = MATTRESS_WIDTH + 2 * MATTRESS_SIDE_MARGIN

# Provisional front-view, pod, and construction dimensions.
PLYWOOD_THICKNESS = 0.75
HEADBOARD_PANEL_THICKNESS = PLYWOOD_THICKNESS
FACE_THICKNESS = PLYWOOD_THICKNESS
DRAWER_FACE_HEIGHT = 6.0
SUPPORT_WIDTH = 3.0
SUPPORT_EDGE_INSET = 2.5
POD_SLIDE_LENGTH = 24.0
POD_END_CAP_THICKNESS = PLYWOOD_THICKNESS
POD_WALL_THICKNESS = PLYWOOD_THICKNESS
POD_CLEARANCE = 0.0625
POD_BODY_WIDTH = POD_SLIDE_LENGTH + POD_END_CAP_THICKNESS + POD_WALL_THICKNESS + 2 * POD_CLEARANCE
POD_EXTENSION = 16.0
POD_SHELF_THICKNESS = PLYWOOD_THICKNESS
POD_RAIL_HEIGHT = 2.0
POD_BOTTOM_Z = FLOOR_CLEARANCE + PEDESTAL_HEIGHT + POD_CLEARANCE
POD_FLOOR_Z = POD_BOTTOM_Z + POD_RAIL_HEIGHT + POD_CLEARANCE
POD_WALL_TOP = 26.0
POD_SLIDE_THICKNESS = 0.375
OCCUPANT_DESIGN_LOAD = 750.0
POWER_FLEX_ADVERTISED_TOTAL_CAPACITY = 850.0

FRAME_Y_MIN = -FRAME_WIDTH / 2
MATTRESS_Y_MIN = -MATTRESS_WIDTH / 2
PEDESTAL_Z = FLOOR_CLEARANCE
PEDESTAL_TOP = PEDESTAL_Z + PEDESTAL_HEIGHT
DECK_Z = PEDESTAL_TOP
MATTRESS_Z = DECK_Z + DECK_HEIGHT
MATTRESS_X = HEADBOARD_DEPTH - MATTRESS_OVERLAP

headboard_profile = [
    (0, PEDESTAL_TOP),
    (0, HEADBOARD_HEIGHT),
    (HEADBOARD_TOP_DEPTH, HEADBOARD_HEIGHT),
    (HEADBOARD_DEPTH, PEDESTAL_TOP),
]
pod_profile = [(1.5, POD_BOTTOM_Z), (1.5, 34.2), (6.5, 34.2), (9, 26), (9, POD_BOTTOM_Z)]
fixed_infill_profile = [(9, PEDESTAL_TOP), (9, 26), (12.5, PEDESTAL_TOP)]

# The full-width headboard is a cabinet. Its center recess accepts the mattress and deck,
# while full-height cavities at each end contain the lateral pull-out pods.
headboard_envelope = profile(headboard_profile, FRAME_Y_MIN, -FRAME_Y_MIN)
center_recess = box(
    HEADBOARD_DEPTH - MATTRESS_X + 1,
    MATTRESS_WIDTH,
    MATTRESS_Z + MATTRESS_HEIGHT - PEDESTAL_TOP,
    MATTRESS_X,
    MATTRESS_Y_MIN,
    PEDESTAL_TOP,
)
left_pod_cavity = profile(pod_profile, FRAME_Y_MIN, FRAME_Y_MIN + POD_BODY_WIDTH)
right_pod_cavity = profile(pod_profile, -FRAME_Y_MIN - POD_BODY_WIDTH, -FRAME_Y_MIN)
left_infill = profile(fixed_infill_profile, FRAME_Y_MIN, FRAME_Y_MIN + FACE_THICKNESS)
right_infill = profile(fixed_infill_profile, -FRAME_Y_MIN - FACE_THICKNESS, -FRAME_Y_MIN)
fixed_infills = [left_infill, right_infill]
rear_opening = box(
    1.6,
    FRAME_WIDTH - 3,
    HEADBOARD_HEIGHT - PEDESTAL_TOP - 2.75,
    -0.05,
    FRAME_Y_MIN + 1.5,
    PEDESTAL_TOP + 0.75,
)
headboard_slope_dx = HEADBOARD_DEPTH - HEADBOARD_TOP_DEPTH
headboard_slope_dz = HEADBOARD_HEIGHT - PEDESTAL_TOP
headboard_slope_length = (headboard_slope_dx**2 + headboard_slope_dz**2) ** 0.5
headboard_slope_x_inset = HEADBOARD_PANEL_THICKNESS * headboard_slope_length / headboard_slope_dz
service_top_z = HEADBOARD_HEIGHT - HEADBOARD_PANEL_THICKNESS
service_bottom_z = PEDESTAL_TOP + HEADBOARD_PANEL_THICKNESS
service_top_x = (
    HEADBOARD_TOP_DEPTH
    + (HEADBOARD_HEIGHT - service_top_z) * headboard_slope_dx / headboard_slope_dz
    - headboard_slope_x_inset
)
service_bottom_x = (
    HEADBOARD_TOP_DEPTH
    + (HEADBOARD_HEIGHT - service_bottom_z) * headboard_slope_dx / headboard_slope_dz
    - headboard_slope_x_inset
)
central_service_profile = [
    (1.5, service_bottom_z),
    (1.5, service_top_z),
    (service_top_x, service_top_z),
    (service_bottom_x, service_bottom_z),
]
central_service_cavity = profile(
    central_service_profile,
    FRAME_Y_MIN + POD_BODY_WIDTH,
    -FRAME_Y_MIN - POD_BODY_WIDTH,
)
service_drop_width = 12.0
service_drop = box(
    3.0,
    service_drop_width,
    HEADBOARD_PANEL_THICKNESS,
    0,
    -service_drop_width / 2,
    PEDESTAL_TOP,
)
headboard_structure = (
    headboard_envelope
    - center_recess
    - left_pod_cavity
    - right_pod_cavity
    - compound(fixed_infills)
    - rear_opening
    - central_service_cavity
    - service_drop
)


def make_pod(side: str):
    if side == "left":
        y_min = FRAME_Y_MIN
        y_max = FRAME_Y_MIN + POD_BODY_WIDTH
        cap_y = y_min
        inner_wall_y = y_max - POD_WALL_THICKNESS
    else:
        y_min = -FRAME_Y_MIN - POD_BODY_WIDTH
        y_max = -FRAME_Y_MIN
        cap_y = y_max - POD_END_CAP_THICKNESS
        inner_wall_y = y_min

    rear_wall_x = 1.5
    front_apron_x = 9 - POD_WALL_THICKNESS
    shelf_x = rear_wall_x
    shelf_depth = 9 - shelf_x

    end_cap = profile(pod_profile, cap_y, cap_y + POD_END_CAP_THICKNESS)
    shelf = box(
        shelf_depth,
        POD_BODY_WIDTH,
        POD_SHELF_THICKNESS,
        shelf_x,
        y_min,
        POD_FLOOR_Z,
    )
    back_wall = box(
        POD_WALL_THICKNESS,
        POD_BODY_WIDTH,
        POD_WALL_TOP - POD_BOTTOM_Z,
        rear_wall_x,
        y_min,
        POD_BOTTOM_Z,
    )
    front_apron = box(
        POD_WALL_THICKNESS,
        POD_BODY_WIDTH,
        POD_FLOOR_Z - POD_BOTTOM_Z,
        front_apron_x,
        y_min,
        POD_BOTTOM_Z,
    )
    inner_wall = box(
        shelf_depth,
        POD_WALL_THICKNESS,
        POD_WALL_TOP - POD_FLOOR_Z,
        shelf_x,
        inner_wall_y,
        POD_FLOOR_Z,
    )
    return end_cap + shelf + back_wall + front_apron + inner_wall


def make_slide_segments(side: str, extension: float):
    if side == "left":
        fixed_y = FRAME_Y_MIN + POD_END_CAP_THICKNESS + POD_CLEARANCE
        moving_y = fixed_y - extension
    else:
        fixed_y = -FRAME_Y_MIN - POD_BODY_WIDTH + POD_WALL_THICKNESS + POD_CLEARANCE
        moving_y = fixed_y + extension

    channel_thickness = POD_SLIDE_THICKNESS / 2
    rail_rear_x = 1.5 + POD_WALL_THICKNESS + POD_SLIDE_THICKNESS
    rail_front_x = 9 - POD_WALL_THICKNESS - POD_SLIDE_THICKNESS
    fixed_segments = [
        box(channel_thickness, POD_SLIDE_LENGTH, POD_RAIL_HEIGHT, rail_rear_x - channel_thickness, fixed_y, POD_BOTTOM_Z),
        box(channel_thickness, POD_SLIDE_LENGTH, POD_RAIL_HEIGHT, rail_front_x, fixed_y, POD_BOTTOM_Z),
    ]
    moving_segments = [
        box(channel_thickness, POD_SLIDE_LENGTH, POD_RAIL_HEIGHT, 1.5 + POD_WALL_THICKNESS, moving_y, POD_BOTTOM_Z),
        box(channel_thickness, POD_SLIDE_LENGTH, POD_RAIL_HEIGHT, rail_front_x + channel_thickness, moving_y, POD_BOTTOM_Z),
    ]
    return fixed_segments, moving_segments


def make_pod_rail(side: str):
    rail_y = (
        FRAME_Y_MIN + POD_END_CAP_THICKNESS + POD_CLEARANCE
        if side == "left"
        else -FRAME_Y_MIN - POD_BODY_WIDTH + POD_WALL_THICKNESS + POD_CLEARANCE
    )
    rail_rear_x = 1.5 + POD_WALL_THICKNESS + POD_SLIDE_THICKNESS
    rail_front_x = 9 - POD_WALL_THICKNESS - POD_SLIDE_THICKNESS
    return box(
        rail_front_x - rail_rear_x,
        POD_SLIDE_LENGTH,
        POD_RAIL_HEIGHT,
        rail_rear_x,
        rail_y,
        POD_BOTTOM_Z,
    )


left_pod_closed = make_pod("left")
right_pod_closed = make_pod("right")
left_pod_open = Pos(0, -inches(POD_EXTENSION), 0) * left_pod_closed
right_pod_open = Pos(0, inches(POD_EXTENSION), 0) * right_pod_closed
pods_closed = [left_pod_closed, right_pod_closed]
pods_open = [left_pod_open, right_pod_open]
left_fixed_slides, left_moving_slides_closed = make_slide_segments("left", 0)
right_fixed_slides, right_moving_slides_closed = make_slide_segments("right", 0)
_, left_moving_slides_open = make_slide_segments("left", POD_EXTENSION)
_, right_moving_slides_open = make_slide_segments("right", POD_EXTENSION)
fixed_slide_segments = left_fixed_slides + right_fixed_slides
moving_slide_segments_closed = left_moving_slides_closed + right_moving_slides_closed
moving_slide_segments_open = left_moving_slides_open + right_moving_slides_open
pod_rails = [make_pod_rail("left"), make_pod_rail("right")]

wall_service_chase_depth = 3.0
wall_service_chase_width = FRAME_WIDTH - 2 * POD_BODY_WIDTH
wall_service_chase = box(
    wall_service_chase_depth,
    wall_service_chase_width,
    PEDESTAL_HEIGHT,
    0,
    -wall_service_chase_width / 2,
    PEDESTAL_Z,
)
pedestal = box(OVERALL_LENGTH, FRAME_WIDTH, PEDESTAL_HEIGHT, 0, FRAME_Y_MIN, PEDESTAL_Z)
pedestal = pedestal - wall_service_chase
drawer_end_gap = 1.2
drawer_face_gap = 2.4
drawer_width = (OVERALL_LENGTH - 2 * drawer_end_gap - 3 * drawer_face_gap) / 4
drawer_step = drawer_width + drawer_face_gap
drawer_faces = []
for index in range(4):
    x = drawer_end_gap + index * drawer_step
    drawer_faces.append(box(drawer_width, FACE_THICKNESS, DRAWER_FACE_HEIGHT, x, FRAME_Y_MIN, PEDESTAL_Z + 1))
    drawer_faces.append(box(drawer_width, FACE_THICKNESS, DRAWER_FACE_HEIGHT, x, -FRAME_Y_MIN - FACE_THICKNESS, PEDESTAL_Z + 1))
pedestal_structure = pedestal - compound(drawer_faces)

deck_halves = [
    box(MATTRESS_LENGTH, MATTRESS_WIDTH / 2, DECK_HEIGHT, MATTRESS_X, MATTRESS_Y_MIN, DECK_Z),
    box(MATTRESS_LENGTH, MATTRESS_WIDTH / 2, DECK_HEIGHT, MATTRESS_X, 0, DECK_Z),
]
deck = compound(deck_halves)
mattress = box(MATTRESS_LENGTH, MATTRESS_WIDTH, MATTRESS_HEIGHT, MATTRESS_X, MATTRESS_Y_MIN, MATTRESS_Z)
mattress = fillet(mattress.edges(), radius=inches(1.0))

head_leg_profile = [(1.4, 0), (3, FLOOR_CLEARANCE), (6.2, FLOOR_CLEARANCE), (5, 0)]
center_head_leg_profile = [(3.4, 0), (5, FLOOR_CLEARANCE), (8.2, FLOOR_CLEARANCE), (7, 0)]
foot_leg_profile = [
    (OVERALL_LENGTH - 6, FLOOR_CLEARANCE),
    (OVERALL_LENGTH - 7.2, FLOOR_CLEARANCE),
    (OVERALL_LENGTH - 6, 0),
    (OVERALL_LENGTH - SUPPORT_EDGE_INSET, 0),
]
supports = []
for y_min in (
    FRAME_Y_MIN + SUPPORT_EDGE_INSET,
    -SUPPORT_WIDTH / 2,
    -FRAME_Y_MIN - SUPPORT_EDGE_INSET - SUPPORT_WIDTH,
):
    supports.append(
        profile(
            center_head_leg_profile if y_min == -SUPPORT_WIDTH / 2 else head_leg_profile,
            y_min,
            y_min + SUPPORT_WIDTH,
        )
    )
    supports.append(profile(foot_leg_profile, y_min, y_min + SUPPORT_WIDTH))
    supports.append(box(3.2, SUPPORT_WIDTH, FLOOR_CLEARANCE, OVERALL_LENGTH / 2 - 1.6, y_min, 0))

frame_parts = [pedestal_structure, headboard_structure] + pod_rails
fixed_front_parts = drawer_faces + fixed_infills
fixed_parts = frame_parts + fixed_front_parts + [deck, mattress] + supports + fixed_slide_segments
closed_assembly = compound(fixed_parts + pods_closed + moving_slide_segments_closed)
open_assembly = compound(fixed_parts + pods_open + moving_slide_segments_open)

output = Path(__file__).parent / "build"
output.mkdir(exist_ok=True)
export_step(closed_assembly, output / "custom-king-storage-bed.step")
export_step(closed_assembly, output / "custom-king-storage-bed-closed.step")
export_step(open_assembly, output / "custom-king-storage-bed-open.step")
export_stl(compound(frame_parts), output / "frame.stl")
export_stl(compound(fixed_front_parts), output / "fixed-fronts.stl")
export_stl(compound(pods_closed), output / "pods-closed.stl")
export_stl(compound(pods_open), output / "pods-open.stl")
export_stl(compound(fixed_slide_segments + moving_slide_segments_closed), output / "slide-envelopes-closed.stl")
export_stl(compound(fixed_slide_segments + moving_slide_segments_open), output / "slide-envelopes-open.stl")
export_stl(deck, output / "deck.stl")
export_stl(mattress, output / "mattress.stl")
export_stl(compound(supports), output / "supports.stl")

report = Report("custom king storage bed")
report.valid(closed_assembly)
report.valid(open_assembly)
report.bbox(
    closed_assembly,
    (inches(OVERALL_LENGTH), inches(FRAME_WIDTH), inches(HEADBOARD_HEIGHT)),
    tol=0.05,
)
report.bbox(
    open_assembly,
    (inches(OVERALL_LENGTH), inches(FRAME_WIDTH + 2 * POD_EXTENSION), inches(HEADBOARD_HEIGHT)),
    tol=0.05,
)
report.dimension(pedestal, "x", inches(OVERALL_LENGTH), tol=0.01)
report.dimension(deck, "x", inches(MATTRESS_LENGTH), tol=0.01)
report.solid_count(deck, 2)
report.dimension(mattress, "x", inches(MATTRESS_LENGTH), tol=0.05)
report.dimension(mattress, "y", inches(MATTRESS_WIDTH), tol=0.05)
report.dimension(pedestal, "z", inches(PEDESTAL_HEIGHT), tol=0.01)
report.no_interference(mattress, headboard_structure)
report.no_interference(deck, headboard_structure)
report.no_interference(compound(pods_closed), headboard_structure)
report.no_interference(compound(pods_open), headboard_structure)
report.no_interference(compound(fixed_slide_segments), compound(pods_closed))
report.no_interference(compound(fixed_slide_segments), compound(pods_open))
report.no_interference(compound(fixed_slide_segments), headboard_structure)
report.no_interference(compound(pod_rails), headboard_structure)
report.no_interference(compound(moving_slide_segments_closed), headboard_structure)
report.no_interference(compound(moving_slide_segments_open), headboard_structure)
report.no_interference(compound(pod_rails), compound(pods_closed))
report.no_interference(compound(pod_rails), compound(pods_open))
report.clearance(compound(pod_rails), compound(pods_closed), minimum=inches(POD_CLEARANCE))
report.clearance(compound(pod_rails), compound(pods_open), minimum=inches(POD_CLEARANCE))
report.no_interference(compound(pods_closed), pedestal_structure)
report.no_interference(compound(pods_open), pedestal_structure)
report.clearance(compound(pods_closed), pedestal_structure, minimum=inches(POD_CLEARANCE))
report.clearance(compound(pods_open), pedestal_structure, minimum=inches(POD_CLEARANCE))
report.no_interference(
    box(
        1.4,
        28,
        HEADBOARD_HEIGHT - PEDESTAL_TOP - 3,
        0.05,
        -14,
        PEDESTAL_TOP + 1,
    ),
    compound(frame_parts + supports),
)
report.no_interference(
    box(
        wall_service_chase_depth,
        wall_service_chase_width,
        7,
        0,
        -wall_service_chase_width / 2,
        3,
    ),
    compound(frame_parts + supports),
)
report.no_interference(
    box(
        1.4,
        service_drop_width,
        HEADBOARD_HEIGHT - 5,
        0.05,
        -service_drop_width / 2,
        3,
    ),
    compound(frame_parts + supports),
)
report.dimension(left_pod_closed, "y", inches(POD_BODY_WIDTH), tol=0.01)
report._record(
    abs(pedestal.bounding_box().max.X - mattress.bounding_box().max.X - inches(MATTRESS_FOOT_MARGIN)) <= 0.01
    and abs(pedestal.bounding_box().max.X - deck.bounding_box().max.X - inches(MATTRESS_FOOT_MARGIN)) <= 0.01,
    f"mattress and deck preserve a {MATTRESS_FOOT_MARGIN:.1f} in foot lip",
)
report._record(
    abs(mattress.bounding_box().min.X - inches(MATTRESS_X)) <= 0.01,
    f"mattress starts {MATTRESS_X:.1f} in from wall for {MATTRESS_OVERLAP:.1f} in overlap",
)
report.solid_count(compound(drawer_faces), 8)
report.solid_count(compound(supports), 9)
report._record(
    abs(compound(supports).bounding_box().min.Y - inches(FRAME_Y_MIN + SUPPORT_EDGE_INSET)) <= 0.01
    and abs(compound(supports).bounding_box().max.Y - inches(-FRAME_Y_MIN - SUPPORT_EDGE_INSET)) <= 0.01
    and abs(compound(supports).bounding_box().max.X - inches(OVERALL_LENGTH - SUPPORT_EDGE_INSET)) <= 0.01,
    f"outer and foot supports use a consistent {SUPPORT_EDGE_INSET:.1f} in edge inset",
)
report._record(
    abs(left_pod_open.bounding_box().min.Y - left_pod_closed.bounding_box().min.Y + inches(POD_EXTENSION)) <= 0.01
    and abs(right_pod_open.bounding_box().max.Y - right_pod_closed.bounding_box().max.Y - inches(POD_EXTENSION)) <= 0.01,
    f"both pods extend {POD_EXTENSION:.1f} in laterally",
)
report.solid_count(compound(pods_closed), 2)
report.solid_count(compound(pod_rails), 2)
report.note("The 4 in mattress overlap is provisional pending the delivered Power-Flex base articulation envelope.")
report.note("The 72 x 84 x 3 in California King Power-Flex envelope is provisional; exact half dimensions, underside protrusions, support pattern, and wall travel are not published.")
report.note("Two independent Power-Flex halves require two accessible power-supply and cord routes plus optional sync-cable routing.")
report.note(f"LOAD MARGIN: {OCCUPANT_DESIGN_LOAD:.0f} lb of occupants leaves only {POWER_FLEX_ADVERTISED_TOTAL_CAPACITY - OCCUPANT_DESIGN_LOAD:.0f} lb under the advertised Power-Flex total capacity for the mattress and bedding.")
report.note("The furniture chassis must also carry both base halves and dynamic loading; the nine-leg layout is not a structural capacity calculation.")
report.note(f"Length budget: {HEADBOARD_DEPTH:.0f} in headboard + {MATTRESS_LENGTH:.0f} in mattress - {MATTRESS_OVERLAP:.0f} in tuck + {MATTRESS_FOOT_MARGIN:.0f} in foot lip = {OVERALL_LENGTH:.0f} in; zero-tuck fallback is {HEADBOARD_DEPTH + MATTRESS_LENGTH + MATTRESS_FOOT_MARGIN:.0f} in.")
report.note("Pump location, base retention, room side clearances, and pod overturning resistance remain unresolved.")
report.note("The pod slide geometry is a 24 x 2 x 0.375 in clearance envelope, not an exact hardware model.")
report.note("The 76 in frame width, 25.625 in pod bodies, 16 in extension, 15.125 in pod shelf height, and pod mechanism are provisional pending front-view dimensions and hardware selection.")
report.note(f"closed assembly volume: {volume_of(closed_assembly):.2f} mm^3")
report.done()
