#!/usr/bin/env python3
"""Integrated review assembly for structure, finish, headboard, and sleep system."""

from pathlib import Path

from build123d import Compound, export_step

import bed
import modules
from checks import Report
from design import FRAME_WIDTH, HEADBOARD_HEIGHT, OVERALL_LENGTH, POD_EXTENSION


def compound(parts):
    return Compound(parts)


fixed_headboard_parts = (
    [bed.headboard_structure]
    + bed.wall_cleats
    + bed.pod_module_floors
    + bed.pod_rails
    + bed.fixed_infills
    + bed.fixed_slide_segments
)
fixed_sleep_parts = [bed.deck, bed.mattress]
closed_headboard_parts = fixed_headboard_parts + bed.pods_closed + bed.moving_slide_segments_closed
open_headboard_parts = fixed_headboard_parts + bed.pods_open + bed.moving_slide_segments_open

closed_assembly = compound([modules.assembly] + closed_headboard_parts + fixed_sleep_parts)
open_assembly = compound([modules.assembly] + open_headboard_parts + fixed_sleep_parts)

output = Path(__file__).parent / "build"
export_step(closed_assembly, output / "integrated-bed-closed.step")
export_step(open_assembly, output / "integrated-bed-open.step")

report = Report("integrated custom king storage bed")
report.valid(closed_assembly)
report.valid(open_assembly)
report.bbox(
    closed_assembly,
    (bed.inches(OVERALL_LENGTH), bed.inches(FRAME_WIDTH), bed.inches(HEADBOARD_HEIGHT)),
    tol=0.05,
)
report.bbox(
    open_assembly,
    (
        bed.inches(OVERALL_LENGTH),
        bed.inches(FRAME_WIDTH + 2 * POD_EXTENSION),
        bed.inches(HEADBOARD_HEIGHT),
    ),
    tol=0.05,
)
report.no_interference(modules.assembly, compound(fixed_headboard_parts))
report.no_interference(modules.assembly, compound(bed.pods_closed))
report.no_interference(modules.assembly, compound(bed.pods_open))
report.no_interference(modules.assembly, bed.deck)
report.no_interference(modules.assembly, bed.mattress)
report.note("The integrated assembly replaces the old pedestal abstraction for build-guide and finish-envelope review.")
report.note("Wall-cleat anchorage, lower headboard locating bolts, exact pod hardware, and delivered-base adapter cutouts remain release gates.")
report.done()
