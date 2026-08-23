#!/usr/bin/env python3
"""Structural module study for the custom California king storage bed."""

from pathlib import Path

from build123d import Align, Box, Compound, Face, Pos, Vector, Wire, export_step, export_stl, extrude
from checks import Report
from design import (
    CENTER_MODULE_WIDTH,
    CHASSIS_DISTRIBUTED_DESIGN_LOAD,
    CHASSIS_EDGE_POINT_LOAD,
    CROSSMEMBER_DEPTH,
    CROSSMEMBER_WIDTH,
    CROSSMEMBER_X_RANGES,
    DEFLECTION_LIMIT_RATIO,
    FLOOR_CLEARANCE,
    FRAME_WIDTH,
    MODULE_LENGTH,
    OVERALL_LENGTH,
    PEDESTAL_HEIGHT,
    PLYWOOD_SCREENING_BENDING_ALLOWABLE,
    PLYWOOD_SCREENING_MODULUS,
    PLYWOOD_THICKNESS,
    SERVICE_OPENING_WIDTH,
    SIDE_MODULE_WIDTH,
    SPLICE_PLATE_HEIGHT,
    SPLICE_PLATE_LENGTH,
    SPLICE_PLATE_THICKNESS,
    SUPPORT_EDGE_INSET,
    SUPPORT_WIDTH,
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


def profile(points: list[tuple[float, float]], y_min: float, y_max: float):
    vertices = [Vector(inches(x), inches(y_min), inches(z)) for x, z in points]
    face = Face(Wire.make_polygon(vertices, close=True))
    return extrude(face, amount=inches(y_max - y_min), dir=(0, 1, 0))


def compound(parts: list):
    return Compound(parts)


FRAME_Y_MIN = -FRAME_WIDTH / 2
PEDESTAL_Z = FLOOR_CLEARANCE
PEDESTAL_TOP = PEDESTAL_Z + PEDESTAL_HEIGHT
CROSSMEMBER_BOTTOM_Z = PEDESTAL_TOP - CROSSMEMBER_DEPTH
CARCASS_BOTTOM_Z = PEDESTAL_Z + PLYWOOD_THICKNESS
LOWER_BULKHEAD_HEIGHT = CROSSMEMBER_BOTTOM_Z - CARCASS_BOTTOM_Z
OUTER_TOP_RAIL_DEPTH = 1.5
OUTER_TOP_RAIL_WIDTH = 1.5
DRAWER_ENVELOPE_DEPTH = 24.0
DRAWER_ENVELOPE_SIDE_CLEARANCE = 0.5
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


def splice_plate_z():
    return CARCASS_BOTTOM_Z + (LOWER_BULKHEAD_HEIGHT - SPLICE_PLATE_HEIGHT) / 2


def side_splice_plate_y(side: str):
    if side == "left":
        return LEFT_MODULE_Y + SIDE_MODULE_WIDTH - PLYWOOD_THICKNESS - SPLICE_PLATE_THICKNESS
    return RIGHT_MODULE_Y + PLYWOOD_THICKNESS


def relevant_crossmember_ranges(x_min: float, x_max: float):
    return [(start, end) for start, end in CROSSMEMBER_X_RANGES if end > x_min and start < x_max]


def notch_for_crossmembers(part, x_min: float, x_max: float, y_min: float, y_max: float):
    notches = [
        box(
            end - start,
            y_max - y_min,
            CROSSMEMBER_DEPTH,
            start,
            y_min,
            CROSSMEMBER_BOTTOM_Z,
        )
        for start, end in relevant_crossmember_ranges(x_min, x_max)
    ]
    return part - compound(notches)


def module_bulkhead_xs(half: str):
    x_min = 0.0 if half == "head" else MODULE_LENGTH
    return (
        x_min,
        x_min + MODULE_LENGTH / 2 - PLYWOOD_THICKNESS / 2,
        x_min + MODULE_LENGTH - PLYWOOD_THICKNESS,
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
    plate_pocket = box(
        SPLICE_PLATE_LENGTH,
        SPLICE_PLATE_THICKNESS,
        SPLICE_PLATE_HEIGHT,
        MODULE_LENGTH - SPLICE_PLATE_LENGTH / 2,
        side_splice_plate_y(side),
        splice_plate_z(),
    )
    bulkheads = [bulkhead - plate_pocket for bulkhead in bulkheads]
    return compound([bottom, inner_wall, outer_top_rail] + bulkheads)


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
    return compound([bottom, center_beam] + side_walls + bulkheads)


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


def make_splice_plates():
    x = MODULE_LENGTH - SPLICE_PLATE_LENGTH / 2
    z = splice_plate_z()
    return [
        box(
            SPLICE_PLATE_LENGTH,
            SPLICE_PLATE_THICKNESS,
            SPLICE_PLATE_HEIGHT,
            x,
            side_splice_plate_y("left"),
            z,
        ),
        box(
            SPLICE_PLATE_LENGTH,
            SPLICE_PLATE_THICKNESS,
            SPLICE_PLATE_HEIGHT,
            x,
            PLYWOOD_THICKNESS,
            z,
        ),
        box(
            SPLICE_PLATE_LENGTH,
            SPLICE_PLATE_THICKNESS,
            SPLICE_PLATE_HEIGHT,
            x,
            side_splice_plate_y("right"),
            z,
        ),
    ]


def make_drawer_envelopes():
    envelopes = []
    for half in ("head", "foot"):
        x_min = 0.0 if half == "head" else MODULE_LENGTH
        crossmember_ranges = relevant_crossmember_ranges(x_min, x_min + MODULE_LENGTH)
        x_ranges = (
            (
                crossmember_ranges[0][1] + DRAWER_ENVELOPE_SIDE_CLEARANCE,
                crossmember_ranges[1][0] - DRAWER_ENVELOPE_SIDE_CLEARANCE,
            ),
            (
                crossmember_ranges[1][1] + DRAWER_ENVELOPE_SIDE_CLEARANCE,
                crossmember_ranges[2][0] - DRAWER_ENVELOPE_SIDE_CLEARANCE,
            ),
        )
        for x_start, x_end in x_ranges:
            envelopes.append(
                box(
                    x_end - x_start,
                    DRAWER_ENVELOPE_DEPTH,
                    DRAWER_ENVELOPE_HEIGHT,
                    x_start,
                    LEFT_MODULE_Y + PLYWOOD_THICKNESS,
                    CARCASS_BOTTOM_Z + DRAWER_ENVELOPE_VERTICAL_CLEARANCE,
                )
            )
            envelopes.append(
                box(
                    x_end - x_start,
                    DRAWER_ENVELOPE_DEPTH,
                    DRAWER_ENVELOPE_HEIGHT,
                    x_start,
                    RIGHT_MODULE_Y + SIDE_MODULE_WIDTH - PLYWOOD_THICKNESS - DRAWER_ENVELOPE_DEPTH,
                    CARCASS_BOTTOM_Z + DRAWER_ENVELOPE_VERTICAL_CLEARANCE,
                )
            )
    return envelopes


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
splice_plates = make_splice_plates()
drawer_envelopes = make_drawer_envelopes()
assembly = compound(modules + crossmembers + splice_plates + supports)

output = Path(__file__).parent / "build" / "modules"
output.mkdir(parents=True, exist_ok=True)
export_step(assembly, output / "structural-modules.step")
export_stl(compound(head_modules), output / "head-modules.stl")
export_stl(compound(foot_modules), output / "foot-modules.stl")
export_stl(compound(crossmembers), output / "crossmembers.stl")
export_stl(compound(splice_plates), output / "splice-plates.stl")
export_stl(compound(supports), output / "supports.stl")
export_stl(compound(drawer_envelopes), output / "drawer-envelopes.stl")

# Screening check for the crossmember segment spanning the 12-inch center service opening.
service_span = SERVICE_OPENING_WIDTH
section_inertia = CROSSMEMBER_WIDTH * CROSSMEMBER_DEPTH**3 / 12
section_modulus = CROSSMEMBER_WIDTH * CROSSMEMBER_DEPTH**2 / 6
point_moment = CHASSIS_EDGE_POINT_LOAD * service_span / 4
point_stress = point_moment / section_modulus
point_deflection = (
    CHASSIS_EDGE_POINT_LOAD
    * service_span**3
    / (48 * PLYWOOD_SCREENING_MODULUS * section_inertia)
)
deflection_limit = service_span / DEFLECTION_LIMIT_RATIO
average_crossmember_load = CHASSIS_DISTRIBUTED_DESIGN_LOAD / len(CROSSMEMBER_X_RANGES)

report = Report("modular structural chassis")
report.valid(assembly)
report.bbox(
    assembly,
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
report.no_interference(compound(splice_plates), compound(modules + crossmembers))
report.no_interference(compound(drawer_envelopes), compound(modules + crossmembers + splice_plates))
report.no_interference(compound(supports), compound(modules + crossmembers + splice_plates))
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
report._record(
    minimum_drawer_width >= 20.75 - 1e-6
    and minimum_drawer_depth >= DRAWER_ENVELOPE_DEPTH - 1e-6
    and minimum_drawer_height >= DRAWER_ENVELOPE_HEIGHT - 1e-6,
    f"eight drawer envelopes preserve at least {minimum_drawer_width:.2f} x {minimum_drawer_depth:.2f} x {minimum_drawer_height:.2f} in",
)
report._record(
    point_stress <= PLYWOOD_SCREENING_BENDING_ALLOWABLE,
    f"500 lb service-opening point-load bending stress {point_stress:.0f} psi <= {PLYWOOD_SCREENING_BENDING_ALLOWABLE:.0f} psi screening limit",
)
report._record(
    point_deflection <= deflection_limit,
    f"500 lb service-opening point-load deflection {point_deflection:.4f} in <= L/{DEFLECTION_LIMIT_RATIO:.0f} ({deflection_limit:.4f} in)",
)
report.note(f"Distributed screening load: {CHASSIS_DISTRIBUTED_DESIGN_LOAD:.0f} lb, averaging {average_crossmember_load:.0f} lb across five crossmember stations.")
report.note("The bending checks cover only the laminated crossmember over the 12 in center service opening.")
report.note("No longitudinal span, drawer-division reaction, or load transfer from the crossmembers to the three leg rows has been calculated yet.")
report.note("Plywood grade, lamination quality, bulkhead buckling, fasteners, splice plates, racking, feet, and floor bearing are not yet verified.")
report.note(f"Eight provisional drawer envelopes preserve {DRAWER_ENVELOPE_DEPTH:.0f} in depth and {DRAWER_ENVELOPE_HEIGHT:.2f} in internal height before drawer-box and slide clearances.")
report.note("Power-Flex bearing locations and allowable chassis spans remain unknown until the delivered halves are measured.")
report.done()
