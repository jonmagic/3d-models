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


# Settled side-elevation dimensions.
OVERALL_LENGTH = 90.0
FRAME_WIDTH = 80.0
MATTRESS_LENGTH = 80.0
MATTRESS_WIDTH = 76.0
MATTRESS_HEIGHT = 11.0
DECK_HEIGHT = 3.0
FLOOR_CLEARANCE = 5.0
PEDESTAL_HEIGHT = 8.0
HEADBOARD_HEIGHT = 36.0
HEADBOARD_DEPTH = 14.0
MATTRESS_OVERLAP = 4.0

# Provisional front-view, pod, and construction dimensions.
FACE_THICKNESS = 0.25
DRAWER_FACE_HEIGHT = 6.0
SUPPORT_WIDTH = 3.0
POD_BODY_WIDTH = 18.0
POD_EXTENSION = 16.0
POD_END_CAP_THICKNESS = 0.75
POD_WALL_THICKNESS = 0.75
POD_SHELF_THICKNESS = 0.75
POD_SHELF_TOP = 26.0

FRAME_Y_MIN = -FRAME_WIDTH / 2
MATTRESS_Y_MIN = -MATTRESS_WIDTH / 2
PEDESTAL_Z = FLOOR_CLEARANCE
PEDESTAL_TOP = PEDESTAL_Z + PEDESTAL_HEIGHT
DECK_Z = PEDESTAL_TOP
MATTRESS_Z = DECK_Z + DECK_HEIGHT
MATTRESS_X = HEADBOARD_DEPTH - MATTRESS_OVERLAP

headboard_profile = [(0, PEDESTAL_TOP), (0, HEADBOARD_HEIGHT), (7, HEADBOARD_HEIGHT), (HEADBOARD_DEPTH, PEDESTAL_TOP)]
pod_profile = [(1.5, 14.5), (1.5, 34.2), (6.5, 34.2), (9, 26), (9, 14.5)]
fixed_infill_profile = [(9, 14.5), (9, 26), (12.5, 14.5)]

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
headboard_structure = headboard_envelope - center_recess - left_pod_cavity - right_pod_cavity - compound(fixed_infills)


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

    end_cap = profile(pod_profile, cap_y, cap_y + POD_END_CAP_THICKNESS)
    shelf = box(
        9 - 1.5,
        POD_BODY_WIDTH,
        POD_SHELF_THICKNESS,
        1.5,
        y_min,
        POD_SHELF_TOP - POD_SHELF_THICKNESS,
    )
    back_wall = box(
        POD_WALL_THICKNESS,
        POD_BODY_WIDTH,
        POD_SHELF_TOP - 14.5,
        1.5,
        y_min,
        14.5,
    )
    inner_wall = box(
        9 - 1.5,
        POD_WALL_THICKNESS,
        POD_SHELF_TOP - 14.5,
        1.5,
        inner_wall_y,
        14.5,
    )
    return end_cap + shelf + back_wall + inner_wall


left_pod_closed = make_pod("left")
right_pod_closed = make_pod("right")
left_pod_open = Pos(0, -inches(POD_EXTENSION), 0) * left_pod_closed
right_pod_open = Pos(0, inches(POD_EXTENSION), 0) * right_pod_closed
pods_closed = [left_pod_closed, right_pod_closed]
pods_open = [left_pod_open, right_pod_open]

pedestal = box(OVERALL_LENGTH, FRAME_WIDTH, PEDESTAL_HEIGHT, 0, FRAME_Y_MIN, PEDESTAL_Z)
drawer_gap = 1.2
drawer_width = 20.1
drawer_step = 22.5
drawer_faces = []
for index in range(4):
    x = drawer_gap + index * drawer_step
    drawer_faces.append(box(drawer_width, FACE_THICKNESS, DRAWER_FACE_HEIGHT, x, FRAME_Y_MIN, PEDESTAL_Z + 1))
    drawer_faces.append(box(drawer_width, FACE_THICKNESS, DRAWER_FACE_HEIGHT, x, -FRAME_Y_MIN - FACE_THICKNESS, PEDESTAL_Z + 1))
pedestal_structure = pedestal - compound(drawer_faces)

deck = box(MATTRESS_LENGTH, MATTRESS_WIDTH, DECK_HEIGHT, MATTRESS_X, MATTRESS_Y_MIN, DECK_Z)
mattress = box(MATTRESS_LENGTH, MATTRESS_WIDTH, MATTRESS_HEIGHT, MATTRESS_X, MATTRESS_Y_MIN, MATTRESS_Z)
mattress = fillet(mattress.edges(), radius=inches(1.0))

head_leg_profile = [(1.4, 0), (3, FLOOR_CLEARANCE), (6.2, FLOOR_CLEARANCE), (5, 0)]
foot_leg_profile = [(84, FLOOR_CLEARANCE), (82.8, FLOOR_CLEARANCE), (84, 0), (87.6, 0)]
supports = []
for y_min in (FRAME_Y_MIN, -FRAME_Y_MIN - SUPPORT_WIDTH):
    supports.append(profile(head_leg_profile, y_min, y_min + SUPPORT_WIDTH))
    supports.append(profile(foot_leg_profile, y_min, y_min + SUPPORT_WIDTH))
    supports.append(box(3.2, SUPPORT_WIDTH, FLOOR_CLEARANCE, 43.4, y_min, 0))

frame_parts = [pedestal_structure, headboard_structure]
fixed_front_parts = drawer_faces + fixed_infills
fixed_parts = frame_parts + fixed_front_parts + [deck, mattress] + supports
closed_assembly = compound(fixed_parts + pods_closed)
open_assembly = compound(fixed_parts + pods_open)

output = Path(__file__).parent / "build"
output.mkdir(exist_ok=True)
export_step(closed_assembly, output / "custom-king-storage-bed.step")
export_step(closed_assembly, output / "custom-king-storage-bed-closed.step")
export_step(open_assembly, output / "custom-king-storage-bed-open.step")
export_stl(compound(frame_parts), output / "frame.stl")
export_stl(compound(fixed_front_parts), output / "fixed-fronts.stl")
export_stl(compound(pods_closed), output / "pods-closed.stl")
export_stl(compound(pods_open), output / "pods-open.stl")
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
report.dimension(mattress, "x", inches(MATTRESS_LENGTH), tol=0.05)
report.dimension(mattress, "y", inches(MATTRESS_WIDTH), tol=0.05)
report.dimension(pedestal, "z", inches(PEDESTAL_HEIGHT), tol=0.01)
report.no_interference(mattress, headboard_structure)
report.no_interference(deck, headboard_structure)
report.no_interference(compound(pods_closed), headboard_structure)
report.no_interference(compound(pods_open), headboard_structure)
report.dimension(left_pod_closed, "y", inches(POD_BODY_WIDTH), tol=0.01)
report._record(
    abs(mattress.bounding_box().max.X - pedestal.bounding_box().max.X) <= 0.01,
    "mattress, deck, and pedestal foot edges align",
)
report._record(
    abs(mattress.bounding_box().min.X - inches(MATTRESS_X)) <= 0.01,
    f"mattress starts {MATTRESS_X:.1f} in from wall for {MATTRESS_OVERLAP:.1f} in overlap",
)
report._record(
    len(drawer_faces) == 8,
    "eight base drawer faces modeled",
)
report._record(
    abs(left_pod_open.bounding_box().min.Y - left_pod_closed.bounding_box().min.Y + inches(POD_EXTENSION)) <= 0.01
    and abs(right_pod_open.bounding_box().max.Y - right_pod_closed.bounding_box().max.Y - inches(POD_EXTENSION)) <= 0.01,
    f"both pods extend {POD_EXTENSION:.1f} in laterally",
)
report._record(
    len(pods_closed) == 2,
    "two lateral headboard pods modeled",
)
report.note("The 4 in mattress overlap is provisional pending the delivered Power-Flex base articulation envelope.")
report.note("The 80 in frame width, 18 in pod bodies, 16 in extension, 26 in shelf height, and pod mechanism are provisional pending front-view dimensions and hardware selection.")
report.note(f"closed assembly volume: {volume_of(closed_assembly):.2f} mm^3")
report.done()
