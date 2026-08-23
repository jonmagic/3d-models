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

# Provisional front-view and construction dimensions.
SIDE_MODULE_WIDTH = 2.0
FACE_THICKNESS = 0.25
CENTRAL_BACK_DEPTH = 1.5
UPPER_PANEL_THICKNESS = 1.0
DRAWER_FACE_HEIGHT = 6.0
SUPPORT_WIDTH = 3.0

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

# The center recess is what allows the deck and mattress to tuck behind the visible side modules.
left_module = profile(headboard_profile, FRAME_Y_MIN, MATTRESS_Y_MIN)
right_module = profile(headboard_profile, -MATTRESS_Y_MIN, -FRAME_Y_MIN)
central_lower_back = box(CENTRAL_BACK_DEPTH, MATTRESS_WIDTH, MATTRESS_Z + MATTRESS_HEIGHT - PEDESTAL_TOP, 0, MATTRESS_Y_MIN, PEDESTAL_TOP)
upper_panel_front_bottom = 7 + (HEADBOARD_HEIGHT - (MATTRESS_Z + MATTRESS_HEIGHT)) * (HEADBOARD_DEPTH - 7) / (HEADBOARD_HEIGHT - PEDESTAL_TOP)
central_upper_profile = [
    (7 - UPPER_PANEL_THICKNESS, HEADBOARD_HEIGHT),
    (7, HEADBOARD_HEIGHT),
    (upper_panel_front_bottom, MATTRESS_Z + MATTRESS_HEIGHT),
    (upper_panel_front_bottom - UPPER_PANEL_THICKNESS, MATTRESS_Z + MATTRESS_HEIGHT),
]
central_upper_back = profile(central_upper_profile, MATTRESS_Y_MIN, -MATTRESS_Y_MIN)
central_back = compound([central_lower_back, central_upper_back])

left_pod = profile(pod_profile, FRAME_Y_MIN, FRAME_Y_MIN + FACE_THICKNESS)
right_pod = profile(pod_profile, -FRAME_Y_MIN - FACE_THICKNESS, -FRAME_Y_MIN)
left_infill = profile(fixed_infill_profile, FRAME_Y_MIN, FRAME_Y_MIN + FACE_THICKNESS)
right_infill = profile(fixed_infill_profile, -FRAME_Y_MIN - FACE_THICKNESS, -FRAME_Y_MIN)
pod_faces = [left_pod, right_pod]
fixed_infills = [left_infill, right_infill]
headboard_structure = compound([left_module, right_module]) - compound(pod_faces + fixed_infills)
headboard_structure += central_back

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
front_parts = drawer_faces + pod_faces + fixed_infills
assembly = compound(frame_parts + front_parts + [deck, mattress] + supports)

output = Path(__file__).parent / "build"
output.mkdir(exist_ok=True)
export_step(assembly, output / "custom-king-storage-bed.step")
export_stl(compound(frame_parts), output / "frame.stl")
export_stl(compound(front_parts), output / "fronts.stl")
export_stl(deck, output / "deck.stl")
export_stl(mattress, output / "mattress.stl")
export_stl(compound(supports), output / "supports.stl")

report = Report("custom king storage bed")
report.valid(assembly)
report.bbox(
    assembly,
    (inches(OVERALL_LENGTH), inches(FRAME_WIDTH), inches(HEADBOARD_HEIGHT)),
    tol=0.05,
)
report.dimension(pedestal, "x", inches(OVERALL_LENGTH), tol=0.01)
report.dimension(deck, "x", inches(MATTRESS_LENGTH), tol=0.01)
report.dimension(mattress, "x", inches(MATTRESS_LENGTH), tol=0.05)
report.dimension(mattress, "y", inches(MATTRESS_WIDTH), tol=0.05)
report.dimension(pedestal, "z", inches(PEDESTAL_HEIGHT), tol=0.01)
report.no_interference(mattress, compound([left_module, right_module]))
report.no_interference(deck, compound([left_module, right_module]))
report.no_interference(mattress, central_back)
report.no_interference(deck, central_back)
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
report.note("The 4 in mattress overlap is provisional pending the delivered Power-Flex base articulation envelope.")
report.note("The 80 in frame width, 2 in side pod zones, central back panel, and pod mechanism depth are provisional pending front-view dimensions.")
report.note(f"assembly volume: {volume_of(assembly):.2f} mm^3")
report.done()
