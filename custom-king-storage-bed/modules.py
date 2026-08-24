#!/usr/bin/env python3
"""Structural module study for the custom California king storage bed."""

from pathlib import Path

from build123d import Align, Box, Compound, Cylinder, Pos, Rot, export_step, export_stl
from checks import Report
from design import (
    ADAPTER_PANEL_THICKNESS,
    ADAPTER_SUPPORT_RAIL_HEIGHT,
    ADAPTER_SUPPORT_RAIL_WIDTH,
    CENTER_MODULE_WIDTH,
    CHASSIS_DISTRIBUTED_DESIGN_LOAD,
    CHASSIS_EDGE_POINT_LOAD,
    CROSSMEMBER_DEPTH,
    CROSSMEMBER_NOTCH_CLEARANCE,
    CROSSMEMBER_WIDTH,
    CROSSMEMBER_X_RANGES,
    DEFLECTION_LIMIT_RATIO,
    DRAWER_SLIDE_CARRIER_HEIGHT,
    DRAWER_SLIDE_SIDE_CLEARANCE,
    FLOOR_CLEARANCE,
    FACE_THICKNESS,
    FOOT_FASCIA_THICKNESS,
    FRAME_WIDTH as FINISHED_FRAME_WIDTH,
    STRUCTURAL_FRAME_WIDTH as FRAME_WIDTH,
    MODULE_LENGTH,
    LATERAL_RACKING_SCREEN_LOAD,
    OVERALL_LENGTH as FINISHED_LENGTH,
    STRUCTURAL_LENGTH as OVERALL_LENGTH,
    PEDESTAL_HEIGHT,
    PLYWOOD_SCREENING_BENDING_ALLOWABLE,
    PLYWOOD_SCREENING_COMPRESSION_ALLOWABLE,
    PLYWOOD_SCREENING_MODULUS,
    STRUCTURAL_PLYWOOD_THICKNESS as PLYWOOD_THICKNESS,
    SEAM_BOLT_CLEARANCE_DIAMETER,
    SEAM_BOLT_DIAMETER,
    SEAM_BOLT_WASHER_OD,
    SEAM_SOCKET_ENVELOPE_DIAMETER,
    SEAM_BOLT_SCREENING_BEARING_STRESS,
    SERVICE_OPENING_WIDTH,
    SIDE_MODULE_WIDTH,
    STRUCTURAL_SUPPORT_SIZE,
    SUPPORT_CAPTURE_CLEARANCE,
    SUPPORT_CAPTURE_CLEAT_HEIGHT,
    SUPPORT_CAPTURE_CLEAT_WIDTH,
    SUPPORT_PAD_THICKNESS,
    SLEEP_SYSTEM_X,
)

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


def compound(parts: list):
    return Compound(parts)


def seam_bolt_hole(y: float):
    cylinder = Cylinder(
        inches(SEAM_BOLT_CLEARANCE_DIAMETER / 2),
        inches(2.5),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return Pos(inches(MODULE_LENGTH), inches(y), inches(SEAM_BOLT_Z)) * Rot(0, 90, 0) * cylinder


FRAME_Y_MIN = -FRAME_WIDTH / 2
PEDESTAL_Z = FLOOR_CLEARANCE
PEDESTAL_TOP = PEDESTAL_Z + PEDESTAL_HEIGHT
CROSSMEMBER_BOTTOM_Z = PEDESTAL_TOP - CROSSMEMBER_DEPTH
CARCASS_BOTTOM_Z = PEDESTAL_Z + PLYWOOD_THICKNESS
LOWER_BULKHEAD_HEIGHT = CROSSMEMBER_BOTTOM_Z - CARCASS_BOTTOM_Z
OUTER_TOP_RAIL_DEPTH = 1.5
OUTER_TOP_RAIL_WIDTH = 1.5
DRAWER_ENVELOPE_DEPTH = 24.0
DRAWER_ENVELOPE_SIDE_CLEARANCE = DRAWER_SLIDE_SIDE_CLEARANCE
DRAWER_ENVELOPE_VERTICAL_CLEARANCE = 0.25
DRAWER_ENVELOPE_HEIGHT = (
    PEDESTAL_TOP
    - OUTER_TOP_RAIL_DEPTH
    - CARCASS_BOTTOM_Z
    - 2 * DRAWER_ENVELOPE_VERTICAL_CLEARANCE
)
LEFT_MODULE_Y = FRAME_Y_MIN
CENTER_MODULE_Y = -CENTER_MODULE_WIDTH / 2
RIGHT_MODULE_Y = CENTER_MODULE_WIDTH / 2
FINISHED_FRAME_Y_MIN = -FINISHED_FRAME_WIDTH / 2
OUTER_SUPPORT_CENTER_Y = FRAME_WIDTH / 2 - 4.0
DRAWER_FRONT_EDGE_GAP = 0.125
DRAWER_FRONT_BOTTOM_Z = PEDESTAL_Z + 1.125
DRAWER_FRONT_HEIGHT = PEDESTAL_HEIGHT - 2.25
SUPPORT_CAPTURE_MARGIN = SUPPORT_CAPTURE_CLEARANCE + SUPPORT_CAPTURE_CLEAT_WIDTH


SEAM_BOLT_Z = CARCASS_BOTTOM_Z + LOWER_BULKHEAD_HEIGHT / 2
SEAM_BOLT_Y_POSITIONS = (
    LEFT_MODULE_Y + 3.0,
    LEFT_MODULE_Y + SIDE_MODULE_WIDTH / 2,
    LEFT_MODULE_Y + SIDE_MODULE_WIDTH - 3.0,
    CENTER_MODULE_Y + 2.0,
    CENTER_MODULE_Y + CENTER_MODULE_WIDTH - 2.0,
    RIGHT_MODULE_Y + 3.0,
    RIGHT_MODULE_Y + SIDE_MODULE_WIDTH / 2,
    RIGHT_MODULE_Y + SIDE_MODULE_WIDTH - 3.0,
)
seam_bolt_holes = [seam_bolt_hole(y) for y in SEAM_BOLT_Y_POSITIONS]
seam_bolt_hole_compound = compound(seam_bolt_holes)


def relevant_crossmember_ranges(x_min: float, x_max: float):
    return [(start, end) for start, end in CROSSMEMBER_X_RANGES if end > x_min and start < x_max]


def notch_for_crossmembers(part, x_min: float, x_max: float, y_min: float, y_max: float):
    notches = [
        box(
            end - start + CROSSMEMBER_NOTCH_CLEARANCE,
            y_max - y_min,
            CROSSMEMBER_DEPTH,
            start - CROSSMEMBER_NOTCH_CLEARANCE / 2,
            y_min,
            CROSSMEMBER_BOTTOM_Z,
        )
        for start, end in relevant_crossmember_ranges(x_min, x_max)
    ]
    return part - compound(notches)


def module_bulkhead_xs(half: str):
    x_min = 0.0 if half == "head" else MODULE_LENGTH
    if half == "head":
        return (
            SUPPORT_CAPTURE_MARGIN,
            x_min + MODULE_LENGTH / 2 - PLYWOOD_THICKNESS / 2,
            x_min + MODULE_LENGTH - PLYWOOD_THICKNESS,
        )
    return (
        x_min,
        x_min + MODULE_LENGTH / 2 - PLYWOOD_THICKNESS / 2,
        OVERALL_LENGTH - SUPPORT_CAPTURE_MARGIN - PLYWOOD_THICKNESS,
    )


def drawer_bay_x_ranges(x_min: float):
    crossmember_ranges = relevant_crossmember_ranges(x_min, x_min + MODULE_LENGTH)
    return (
        (crossmember_ranges[0][1], crossmember_ranges[1][0]),
        (crossmember_ranges[1][1], crossmember_ranges[2][0]),
    )


def make_side_module(side: str, half: str):
    x_min = 0.0 if half == "head" else MODULE_LENGTH
    y_min = LEFT_MODULE_Y if side == "left" else RIGHT_MODULE_Y
    inner_wall_y = (
        y_min + SIDE_MODULE_WIDTH - PLYWOOD_THICKNESS
        if side == "left"
        else y_min
    )
    outer_rail_y = y_min if side == "left" else y_min + SIDE_MODULE_WIDTH - OUTER_TOP_RAIL_WIDTH

    bottom = box(MODULE_LENGTH, SIDE_MODULE_WIDTH, PLYWOOD_THICKNESS, x_min, y_min, PEDESTAL_Z)
    inner_wall = box(
        MODULE_LENGTH,
        PLYWOOD_THICKNESS,
        PEDESTAL_HEIGHT - PLYWOOD_THICKNESS,
        x_min,
        inner_wall_y,
        CARCASS_BOTTOM_Z,
    )
    inner_wall = notch_for_crossmembers(
        inner_wall,
        x_min,
        x_min + MODULE_LENGTH,
        inner_wall_y,
        inner_wall_y + PLYWOOD_THICKNESS,
    )
    outer_top_rail = box(
        MODULE_LENGTH,
        OUTER_TOP_RAIL_WIDTH,
        OUTER_TOP_RAIL_DEPTH,
        x_min,
        outer_rail_y,
        PEDESTAL_TOP - OUTER_TOP_RAIL_DEPTH,
    )
    outer_top_rail = notch_for_crossmembers(
        outer_top_rail,
        x_min,
        x_min + MODULE_LENGTH,
        outer_rail_y,
        outer_rail_y + OUTER_TOP_RAIL_WIDTH,
    )
    bulkheads = [
        box(
            PLYWOOD_THICKNESS,
            SIDE_MODULE_WIDTH,
            LOWER_BULKHEAD_HEIGHT,
            x,
            y_min,
            CARCASS_BOTTOM_Z,
        )
        for x in module_bulkhead_xs(half)
    ]
    slide_carriers = []
    for bay_start, bay_end in drawer_bay_x_ranges(x_min):
        slide_carriers.extend(
            [
                box(
                    PLYWOOD_THICKNESS,
                    SIDE_MODULE_WIDTH,
                    DRAWER_SLIDE_CARRIER_HEIGHT,
                    bay_start,
                    y_min,
                    CROSSMEMBER_BOTTOM_Z,
                ),
                box(
                    PLYWOOD_THICKNESS,
                    SIDE_MODULE_WIDTH,
                    DRAWER_SLIDE_CARRIER_HEIGHT,
                    bay_end - PLYWOOD_THICKNESS,
                    y_min,
                    CROSSMEMBER_BOTTOM_Z,
                ),
            ]
        )
    return compound([bottom, inner_wall, outer_top_rail] + bulkheads + slide_carriers) - seam_bolt_hole_compound


def service_bulkhead(x: float):
    opening_min = -SERVICE_OPENING_WIDTH / 2
    opening_max = SERVICE_OPENING_WIDTH / 2
    return compound(
        [
            box(
                PLYWOOD_THICKNESS,
                opening_min - CENTER_MODULE_Y,
                LOWER_BULKHEAD_HEIGHT,
                x,
                CENTER_MODULE_Y,
                CARCASS_BOTTOM_Z,
            ),
            box(
                PLYWOOD_THICKNESS,
                CENTER_MODULE_Y + CENTER_MODULE_WIDTH - opening_max,
                LOWER_BULKHEAD_HEIGHT,
                x,
                opening_max,
                CARCASS_BOTTOM_Z,
            ),
        ]
    )


def make_center_module(half: str):
    x_min = 0.0 if half == "head" else MODULE_LENGTH
    bottom = box(MODULE_LENGTH, CENTER_MODULE_WIDTH, PLYWOOD_THICKNESS, x_min, CENTER_MODULE_Y, PEDESTAL_Z)
    if half == "head":
        bottom = bottom - box(
            3.0,
            SERVICE_OPENING_WIDTH,
            PLYWOOD_THICKNESS,
            0,
            -SERVICE_OPENING_WIDTH / 2,
            PEDESTAL_Z,
        )

    side_walls = []
    for y in (CENTER_MODULE_Y, -CENTER_MODULE_Y - PLYWOOD_THICKNESS):
        wall = box(
            MODULE_LENGTH,
            PLYWOOD_THICKNESS,
            PEDESTAL_HEIGHT - PLYWOOD_THICKNESS,
            x_min,
            y,
            CARCASS_BOTTOM_Z,
        )
        side_walls.append(
            notch_for_crossmembers(
                wall,
                x_min,
                x_min + MODULE_LENGTH,
                y,
                y + PLYWOOD_THICKNESS,
            )
        )

    beam_x = 3.4 if half == "head" else x_min
    center_beam = box(
        x_min + MODULE_LENGTH - beam_x,
        2 * PLYWOOD_THICKNESS,
        PEDESTAL_HEIGHT - PLYWOOD_THICKNESS,
        beam_x,
        -PLYWOOD_THICKNESS,
        CARCASS_BOTTOM_Z,
    )
    center_beam = notch_for_crossmembers(
        center_beam,
        x_min,
        x_min + MODULE_LENGTH,
        -PLYWOOD_THICKNESS,
        PLYWOOD_THICKNESS,
    )
    bulkheads = [service_bulkhead(x) for x in module_bulkhead_xs(half)]
    return compound([bottom, center_beam] + side_walls + bulkheads) - seam_bolt_hole_compound


def make_crossmembers():
    members = []
    for index, (x_min, x_max) in enumerate(CROSSMEMBER_X_RANGES):
        if index == 0:
            members.extend(
                [
                    box(
                        x_max - x_min,
                        FRAME_WIDTH / 2 - SERVICE_OPENING_WIDTH / 2,
                        CROSSMEMBER_DEPTH,
                        x_min,
                        FRAME_Y_MIN,
                        CROSSMEMBER_BOTTOM_Z,
                    ),
                    box(
                        x_max - x_min,
                        FRAME_WIDTH / 2 - SERVICE_OPENING_WIDTH / 2,
                        CROSSMEMBER_DEPTH,
                        x_min,
                        SERVICE_OPENING_WIDTH / 2,
                        CROSSMEMBER_BOTTOM_Z,
                    ),
                ]
            )
        else:
            members.append(
                box(
                    x_max - x_min,
                    FRAME_WIDTH,
                    CROSSMEMBER_DEPTH,
                    x_min,
                    FRAME_Y_MIN,
                    CROSSMEMBER_BOTTOM_Z,
                )
            )
    return members


def make_drawer_envelopes():
    envelopes = []
    for half in ("head", "foot"):
        x_min = 0.0 if half == "head" else MODULE_LENGTH
        for bay_start, bay_end in drawer_bay_x_ranges(x_min):
            x_start = bay_start + PLYWOOD_THICKNESS + DRAWER_ENVELOPE_SIDE_CLEARANCE
            x_end = bay_end - PLYWOOD_THICKNESS - DRAWER_ENVELOPE_SIDE_CLEARANCE
            envelopes.append(
                box(
                    x_end - x_start,
                    DRAWER_ENVELOPE_DEPTH,
                    DRAWER_ENVELOPE_HEIGHT,
                    x_start,
                    LEFT_MODULE_Y,
                    CARCASS_BOTTOM_Z + DRAWER_ENVELOPE_VERTICAL_CLEARANCE,
                )
            )
            envelopes.append(
                box(
                    x_end - x_start,
                    DRAWER_ENVELOPE_DEPTH,
                    DRAWER_ENVELOPE_HEIGHT,
                    x_start,
                    RIGHT_MODULE_Y + SIDE_MODULE_WIDTH - DRAWER_ENVELOPE_DEPTH,
                    CARCASS_BOTTOM_Z + DRAWER_ENVELOPE_VERTICAL_CLEARANCE,
                )
            )
    return envelopes


def make_finish_faces(drawer_envelopes):
    faces = [
        box(
            FOOT_FASCIA_THICKNESS,
            FINISHED_FRAME_WIDTH,
            PEDESTAL_HEIGHT,
            OVERALL_LENGTH,
            FINISHED_FRAME_Y_MIN,
            PEDESTAL_Z,
        )
    ]
    for side in ("left", "right"):
        y = FINISHED_FRAME_Y_MIN if side == "left" else FRAME_WIDTH / 2
        faces.extend(
            [
                box(OVERALL_LENGTH, FACE_THICKNESS, 1.0, 0, y, PEDESTAL_Z),
                box(OVERALL_LENGTH, FACE_THICKNESS, 1.0, 0, y, PEDESTAL_TOP - 1.0),
            ]
        )
    for index, envelope in enumerate(drawer_envelopes):
        bounds = envelope.bounding_box()
        x_min = bounds.min.X / IN - (DRAWER_ENVELOPE_SIDE_CLEARANCE - DRAWER_FRONT_EDGE_GAP)
        x_max = bounds.max.X / IN + (DRAWER_ENVELOPE_SIDE_CLEARANCE - DRAWER_FRONT_EDGE_GAP)
        is_left = index % 2 == 0
        y = FINISHED_FRAME_Y_MIN if is_left else FRAME_WIDTH / 2
        faces.append(
            box(
                x_max - x_min,
                FACE_THICKNESS,
                DRAWER_FRONT_HEIGHT,
                x_min,
                y,
                DRAWER_FRONT_BOTTOM_Z,
            )
        )
    return faces


def make_adapter_envelopes():
    return [
        box(
            84.0,
            36.0,
            ADAPTER_PANEL_THICKNESS,
            SLEEP_SYSTEM_X,
            -36.0,
            PEDESTAL_TOP,
        ),
        box(
            84.0,
            36.0,
            ADAPTER_PANEL_THICKNESS,
            SLEEP_SYSTEM_X,
            0.0,
            PEDESTAL_TOP,
        ),
    ]


def make_adapter_support_rails():
    rails = []
    for (_, previous_end), (next_start, _) in zip(CROSSMEMBER_X_RANGES, CROSSMEMBER_X_RANGES[1:]):
        gap = next_start - previous_end
        for y in (
            FRAME_Y_MIN + OUTER_TOP_RAIL_WIDTH,
            FRAME_WIDTH / 2 - OUTER_TOP_RAIL_WIDTH - ADAPTER_SUPPORT_RAIL_WIDTH,
        ):
            rails.append(
                box(
                    gap,
                    ADAPTER_SUPPORT_RAIL_WIDTH,
                    ADAPTER_SUPPORT_RAIL_HEIGHT,
                    previous_end,
                    y,
                    PEDESTAL_TOP - ADAPTER_SUPPORT_RAIL_HEIGHT,
                )
            )
    return rails


supports = []
support_records = []
for index, (x_min, x_max) in enumerate(CROSSMEMBER_X_RANGES):
    crossmember_center_x = (x_min + x_max) / 2
    default_support_x = min(
        max(crossmember_center_x - STRUCTURAL_SUPPORT_SIZE / 2, SUPPORT_CAPTURE_MARGIN),
        OVERALL_LENGTH - STRUCTURAL_SUPPORT_SIZE - SUPPORT_CAPTURE_MARGIN,
    )
    support_center_ys = (
        (-OUTER_SUPPORT_CENTER_Y, -8.0, 0.0, 8.0, OUTER_SUPPORT_CENTER_Y)
        if index == 0
        else (-OUTER_SUPPORT_CENTER_Y, 0.0, OUTER_SUPPORT_CENTER_Y)
    )
    for support_center_y in support_center_ys:
        support_x = 3.0 + SUPPORT_CAPTURE_MARGIN if index == 0 and support_center_y == 0 else default_support_x
        supports.append(
            box(
                STRUCTURAL_SUPPORT_SIZE,
                STRUCTURAL_SUPPORT_SIZE,
                FLOOR_CLEARANCE - SUPPORT_PAD_THICKNESS,
                support_x,
                support_center_y - STRUCTURAL_SUPPORT_SIZE / 2,
                SUPPORT_PAD_THICKNESS,
            )
        )
        support_records.append((index, support_center_y, support_x))

support_pads = [
    box(
        STRUCTURAL_SUPPORT_SIZE,
        STRUCTURAL_SUPPORT_SIZE,
        SUPPORT_PAD_THICKNESS,
        support_x,
        support_center_y - STRUCTURAL_SUPPORT_SIZE / 2,
        0,
    )
    for _, support_center_y, support_x in support_records
]
support_capture_cleats = []
for _, support_center_y, support_x in support_records:
    support_y = support_center_y - STRUCTURAL_SUPPORT_SIZE / 2
    for cleat_y in (
        support_y - SUPPORT_CAPTURE_CLEARANCE - SUPPORT_CAPTURE_CLEAT_WIDTH,
        support_y + STRUCTURAL_SUPPORT_SIZE + SUPPORT_CAPTURE_CLEARANCE,
    ):
        support_capture_cleats.append(
            box(
                STRUCTURAL_SUPPORT_SIZE,
                SUPPORT_CAPTURE_CLEAT_WIDTH,
                SUPPORT_CAPTURE_CLEAT_HEIGHT,
                support_x,
                cleat_y,
                PEDESTAL_Z - SUPPORT_CAPTURE_CLEAT_HEIGHT,
            )
        )
    for cleat_x in (
        support_x - SUPPORT_CAPTURE_CLEARANCE - SUPPORT_CAPTURE_CLEAT_WIDTH,
        support_x + STRUCTURAL_SUPPORT_SIZE + SUPPORT_CAPTURE_CLEARANCE,
    ):
        support_capture_cleats.append(
            box(
                SUPPORT_CAPTURE_CLEAT_WIDTH,
                STRUCTURAL_SUPPORT_SIZE,
                SUPPORT_CAPTURE_CLEAT_HEIGHT,
                cleat_x,
                support_y,
                PEDESTAL_Z - SUPPORT_CAPTURE_CLEAT_HEIGHT,
            )
        )

left_head = make_side_module("left", "head")
center_head = make_center_module("head")
right_head = make_side_module("right", "head")
left_foot = make_side_module("left", "foot")
center_foot = make_center_module("foot")
right_foot = make_side_module("right", "foot")
head_modules = [left_head, center_head, right_head]
foot_modules = [left_foot, center_foot, right_foot]
modules = head_modules + foot_modules
crossmembers = make_crossmembers()
drawer_envelopes = make_drawer_envelopes()
finish_faces = make_finish_faces(drawer_envelopes)
adapter_envelopes = make_adapter_envelopes()
adapter_support_rails = make_adapter_support_rails()
structural_assembly = compound(
    modules + crossmembers + supports + support_pads + support_capture_cleats + adapter_support_rails
)
assembly = compound(
    modules
    + crossmembers
    + supports
    + support_pads
    + support_capture_cleats
    + adapter_support_rails
    + finish_faces
    + adapter_envelopes
)

output = Path(__file__).parent / "build" / "modules"
output.mkdir(parents=True, exist_ok=True)
export_step(assembly, output / "structural-modules.step")
export_stl(compound(head_modules), output / "head-modules.stl")
export_stl(compound(foot_modules), output / "foot-modules.stl")
export_stl(compound(crossmembers), output / "crossmembers.stl")
export_stl(compound(supports), output / "supports.stl")
export_stl(compound(support_pads), output / "support-pads.stl")
export_stl(compound(support_capture_cleats), output / "support-capture-cleats.stl")
export_stl(compound(finish_faces), output / "finish-faces.stl")
export_stl(compound(adapter_envelopes), output / "adapter-envelopes.stl")
export_stl(compound(adapter_support_rails), output / "adapter-support-rails.stl")
export_stl(compound(drawer_envelopes), output / "drawer-envelopes.stl")
export_stl(seam_bolt_hole_compound, output / "seam-bolt-envelopes.stl")

# Screening check for one crossmember span under the distributed station load and edge point load.
crossmember_span = OUTER_SUPPORT_CENTER_Y
section_inertia = CROSSMEMBER_WIDTH * CROSSMEMBER_DEPTH**3 / 12
section_modulus = CROSSMEMBER_WIDTH * CROSSMEMBER_DEPTH**2 / 6
crossmember_station_load = CHASSIS_DISTRIBUTED_DESIGN_LOAD / len(CROSSMEMBER_X_RANGES)
uniform_line_load = crossmember_station_load / FRAME_WIDTH
combined_moment = (
    CHASSIS_EDGE_POINT_LOAD * crossmember_span / 4
    + uniform_line_load * crossmember_span**2 / 8
)
combined_stress = combined_moment / section_modulus
combined_deflection = (
    CHASSIS_EDGE_POINT_LOAD
    * crossmember_span**3
    / (48 * PLYWOOD_SCREENING_MODULUS * section_inertia)
    + 5
    * uniform_line_load
    * crossmember_span**4
    / (384 * PLYWOOD_SCREENING_MODULUS * section_inertia)
)
deflection_limit = crossmember_span / DEFLECTION_LIMIT_RATIO
edge_cantilever = FRAME_WIDTH / 2 - crossmember_span
edge_point_near_support_reaction = (
    CHASSIS_EDGE_POINT_LOAD * (crossmember_span + edge_cantilever) / crossmember_span
)
worst_support_load = crossmember_station_load / 3 + edge_point_near_support_reaction
bulkhead_bearing_area = PLYWOOD_THICKNESS * STRUCTURAL_SUPPORT_SIZE
bulkhead_compression_stress = worst_support_load / bulkhead_bearing_area
floor_bearing_pressure = worst_support_load / STRUCTURAL_SUPPORT_SIZE**2
seam_bolt_vertical_edge_distance = LOWER_BULKHEAD_HEIGHT / 2
center_seam_bolt_capacity = (
    2
    * SEAM_BOLT_SCREENING_BEARING_STRESS
    * PLYWOOD_THICKNESS
    * SEAM_BOLT_DIAMETER
)

report = Report("modular structural chassis")
report.valid(assembly)
report.bbox(
    assembly,
    (
        inches(FINISHED_LENGTH),
        inches(FINISHED_FRAME_WIDTH),
        inches(PEDESTAL_TOP + ADAPTER_PANEL_THICKNESS),
    ),
    tol=0.05,
)
report.bbox(
    structural_assembly,
    (inches(OVERALL_LENGTH), inches(FRAME_WIDTH), inches(PEDESTAL_TOP)),
    tol=0.05,
)
for module in modules:
    report.valid(module)
report.bbox(left_head, (inches(MODULE_LENGTH), inches(SIDE_MODULE_WIDTH), inches(PEDESTAL_HEIGHT)), tol=0.05)
report.bbox(center_head, (inches(MODULE_LENGTH), inches(CENTER_MODULE_WIDTH), inches(PEDESTAL_HEIGHT)), tol=0.05)
report.no_interference(compound(head_modules), compound(foot_modules))
report.no_interference(left_head, center_head)
report.no_interference(center_head, right_head)
report.no_interference(left_foot, center_foot)
report.no_interference(center_foot, right_foot)
report.no_interference(compound(crossmembers), compound(modules))
report.no_interference(compound(drawer_envelopes), compound(modules + crossmembers))
report.no_interference(compound(supports), compound(modules + crossmembers))
report.no_interference(compound(support_pads), compound(supports + modules))
report.no_interference(compound(support_capture_cleats), compound(supports + modules))
report.no_interference(compound(adapter_support_rails), compound(modules + crossmembers + drawer_envelopes))
report.no_interference(compound(finish_faces), compound(modules + crossmembers))
report.no_interference(compound(adapter_envelopes), compound(modules + crossmembers + finish_faces))
report.no_interference(seam_bolt_hole_compound, compound(modules + crossmembers))
report.solid_count(compound(supports), 17)
report.solid_count(compound(support_pads), 17)
report.solid_count(compound(support_capture_cleats), 68)
report.solid_count(compound(adapter_support_rails), 8)
report.solid_count(compound(finish_faces), 13)
report.solid_count(compound(adapter_envelopes), 2)
minimum_drawer_width = min(
    (envelope.bounding_box().max.X - envelope.bounding_box().min.X) / IN
    for envelope in drawer_envelopes
)
minimum_drawer_depth = min(
    (envelope.bounding_box().max.Y - envelope.bounding_box().min.Y) / IN
    for envelope in drawer_envelopes
)
minimum_drawer_height = min(
    (envelope.bounding_box().max.Z - envelope.bounding_box().min.Z) / IN
    for envelope in drawer_envelopes
)
station_a_support_span = OUTER_SUPPORT_CENTER_Y - 8.0
for station_index, support_center_y, support_x in support_records:
    crossmember_x_min, crossmember_x_max = CROSSMEMBER_X_RANGES[station_index]
    support_x_max = support_x + STRUCTURAL_SUPPORT_SIZE
    if station_index == 0 and support_center_y == 0:
        beam_overlap = support_x_max - max(support_x, 3.4)
        report._record(
            beam_overlap > 0 and support_x - SUPPORT_CAPTURE_MARGIN >= 3.0,
            f"center-head support overlaps the center beam by {beam_overlap:.2f} in and keeps its head capture cleat beyond the 3 in service notch",
        )
    else:
        overlap = min(support_x_max, crossmember_x_max) - max(support_x, crossmember_x_min)
        report._record(
            overlap > 0,
            f"station {station_index + 1} support at Y={support_center_y:.0f} in overlaps its crossmember by {overlap:.2f} in",
        )
report._record(
    station_a_support_span <= crossmember_span,
    f"each split station-A member has a {station_a_support_span:.2f} in support-center span <= the screened {crossmember_span:.2f} in B-E span",
)
report._record(
    CROSSMEMBER_BOTTOM_Z - (SEAM_BOLT_Z + SEAM_SOCKET_ENVELOPE_DIAMETER / 2) >= 0,
    f"a {SEAM_SOCKET_ENVELOPE_DIAMETER:.2f} in socket envelope clears the raised slide-carrier webs by {CROSSMEMBER_BOTTOM_Z - (SEAM_BOLT_Z + SEAM_SOCKET_ENVELOPE_DIAMETER / 2):.3f} in",
)
report._record(
    module_bulkhead_xs("head")[0] >= SUPPORT_CAPTURE_MARGIN
    and module_bulkhead_xs("head")[0] + PLYWOOD_THICKNESS <= SUPPORT_CAPTURE_MARGIN + STRUCTURAL_SUPPORT_SIZE
    and module_bulkhead_xs("foot")[-1] >= OVERALL_LENGTH - STRUCTURAL_SUPPORT_SIZE - SUPPORT_CAPTURE_MARGIN
    and module_bulkhead_xs("foot")[-1] + PLYWOOD_THICKNESS <= OVERALL_LENGTH - SUPPORT_CAPTURE_MARGIN,
    "head and foot end bulkheads bear within the captured end-support footprints",
)
report._record(
    minimum_drawer_width >= 19.25 - 1e-6
    and minimum_drawer_depth >= DRAWER_ENVELOPE_DEPTH - 1e-6
    and minimum_drawer_height >= DRAWER_ENVELOPE_HEIGHT - 1e-6,
    f"eight drawer envelopes preserve at least {minimum_drawer_width:.2f} x {minimum_drawer_depth:.2f} x {minimum_drawer_height:.2f} in",
)
report._record(
    combined_stress <= PLYWOOD_SCREENING_BENDING_ALLOWABLE,
    f"combined crossmember bending stress {combined_stress:.0f} psi <= {PLYWOOD_SCREENING_BENDING_ALLOWABLE:.0f} psi screening limit",
)
report._record(
    combined_deflection <= deflection_limit,
    f"combined crossmember deflection {combined_deflection:.4f} in <= L/{DEFLECTION_LIMIT_RATIO:.0f} ({deflection_limit:.4f} in)",
)
report._record(
    bulkhead_compression_stress <= PLYWOOD_SCREENING_COMPRESSION_ALLOWABLE,
    f"worst bulkhead compression {bulkhead_compression_stress:.0f} psi <= {PLYWOOD_SCREENING_COMPRESSION_ALLOWABLE:.0f} psi screening limit",
)
report._record(
    center_seam_bolt_capacity >= LATERAL_RACKING_SCREEN_LOAD,
    f"two-bolt center seam bearing screen {center_seam_bolt_capacity:.0f} lb >= {LATERAL_RACKING_SCREEN_LOAD:.0f} lb lateral screen",
)
report._record(
    seam_bolt_vertical_edge_distance >= 2 * SEAM_BOLT_DIAMETER,
    f"seam-bolt vertical center-to-edge distance {seam_bolt_vertical_edge_distance:.3f} in >= 2d ({2 * SEAM_BOLT_DIAMETER:.3f} in)",
)
report._record(
    LOWER_BULKHEAD_HEIGHT - SEAM_BOLT_WASHER_OD >= 0.5,
    f"{SEAM_BOLT_WASHER_OD:.2f} in washer leaves {(LOWER_BULKHEAD_HEIGHT - SEAM_BOLT_WASHER_OD) / 2:.3f} in to each bulkhead edge",
)
report.note(f"Distributed screening load: {CHASSIS_DISTRIBUTED_DESIGN_LOAD:.0f} lb, averaging {crossmember_station_load:.0f} lb across five directly supported crossmember stations.")
report.note(f"Crossmember bending uses the conservative {crossmember_span:.2f} in span from stations B-E with the bulkhead treated only as local bearing; those members are continuous over three supports, while each split station-A member bears on two supports.")
report.note("The 500 lb edge case uses midspan placement for member bending and a 4 in cantilever reaction for support bearing.")
report.note(f"Seventeen {STRUCTURAL_SUPPORT_SIZE:.1f} in square wood supports retain their full footprint on {SUPPORT_PAD_THICKNESS:.4f} in provisional LVP-safe pads; station A has two supports under each split crossmember plus one under the center beam.")
report.note("The seam screen checks plywood bearing only; bolt grade, washer size, tear-out, repeated assembly, and crossmember-to-module fasteners remain unresolved.")
report.note("Plywood grade, lamination quality, racking stiffness, edge-load uplift restraint, adjustable levelers, floor finish, and proof loading are not yet verified.")
report.note(f"Eight provisional drawer envelopes preserve {DRAWER_ENVELOPE_DEPTH:.0f} in depth and {DRAWER_ENVELOPE_HEIGHT:.2f} in internal height before drawer-box and slide clearances.")
report.note("The two 1/4 in Power-Flex adapter panels are cutout envelopes, not released parts; their bearing lattices, no-go openings, backing blocks, and mounting holes require the delivered halves.")
report.done()
