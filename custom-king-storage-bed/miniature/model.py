#!/usr/bin/env python3
"""Printable 1:10 interpretation; never scales the construction meshes."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.util
import json
import math
from pathlib import Path

from build123d import (
    Align, Axis, Box, Compound, Cylinder, Face, Plane, Pos, Rot, Vector, Wire,
    export_step, export_stl, extrude, fillet, mirror,
)
from checks import Report, volume_of

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("full_size_design", ROOT.parent / "design.py")
full = importlib.util.module_from_spec(spec)
spec.loader.exec_module(full)

SCALE = 10
MM = 25.4 / SCALE
L = full.MODULE_LENGTH * MM
SIDE = full.SIDE_MODULE_WIDTH * MM
CENTER = full.CENTER_MODULE_WIDTH * MM
HEIGHT = full.PEDESTAL_HEIGHT * MM
GROUND = full.FLOOR_CLEARANCE * MM
WIDTH = full.FRAME_WIDTH * MM
LENGTH = full.OVERALL_LENGTH * MM
SIDE_INSET = full.FACE_THICKNESS * MM
WALL = 1.8
COLLAR = 8.4
DIVIDER = 2.0
KEY_HEIGHT = 5.0
PIN_SIZE = 4.0
PIN_HEIGHT = 3.6
HOLE_DEPTH = 2.25
DRAWER_TRAVEL = 35.0
POD_TRAVEL = full.POD_EXTENSION * MM
POD_LENGTH = 72.0
CAP = 1.9
CHANNEL_X = (3.0, 20.0)
CHANNEL_Z = (4.5, 17.0)
HB_HEIGHT = (full.HEADBOARD_HEIGHT - full.FLOOR_CLEARANCE - full.PEDESTAL_HEIGHT) * MM
SLEEP_X = full.SLEEP_SYSTEM_X * MM
HB_DEPTH = SLEEP_X - 0.5
MATTRESS_LENGTH = full.MATTRESS_LENGTH * MM
MATTRESS_GAP = 0.6
HALF_WIDTH = (full.MATTRESS_WIDTH * MM - MATTRESS_GAP) / 2
MATTRESS_HEIGHT = full.MATTRESS_HEIGHT * MM
BASE_HEIGHT = (full.DECK_HEIGHT + full.ADAPTER_PANEL_THICKNESS) * MM
TOP = GROUND + HEIGHT
PAD = full.STRUCTURAL_SUPPORT_SIZE * MM
LOCATOR_HEIGHT = 1.2
RECESS_DEPTH = 1.8
MATTRESS_SKIN = 2.4
EPS = 0.01


def box(x, y, z, at=(0, 0, 0)):
    return Pos(*at) * Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


def prism(points, height):
    wire = Wire.make_polygon([Vector(x, y, 0) for x, y in points], close=True)
    return extrude(Face(wire), amount=height)


def rounded_box(x, y, z, radius=1.0):
    return fillet(box(x, y, z).edges().filter_by(Axis.Z), radius)


def normalized(shape):
    b = shape.bounding_box()
    return Pos(-b.min.X, -b.min.Y, -b.min.Z) * shape


def bowtie(height=KEY_HEIGHT, allowance=0.0):
    a = allowance
    return prism([
        (-6-a, -5-a), (0, -3-a), (6+a, -5-a),
        (6+a, 5+a), (0, 3+a), (-6-a, 5+a),
    ], height)


def pin_hole(x, y, z, fit):
    return box(PIN_SIZE + 2*fit, PIN_SIZE + 2*fit, HOLE_DEPTH + EPS,
               (x-PIN_SIZE/2-fit, y-PIN_SIZE/2-fit, z))


def sockets(width, side, fit):
    result = []
    end_ys = (12.0, width-12.0) if side else (width/2,)
    for x in (0.0, L):
        result.extend((x, y, 0) for y in end_ys)
    edges = (width,) if side else (0.0, width)
    for y in edges:
        result.extend((x, y, 90) for x in (L/3, 2*L/3))
    return [
        Pos(x, y, HEIGHT-KEY_HEIGHT-fit) * Rot(0, 0, angle)
        * bowtie(KEY_HEIGHT+fit+EPS, fit)
        for x, y, angle in result
    ]


def make_module(width, side, fit):
    result = box(L, width, HEIGHT)
    if side:
        opening = (L-2*COLLAR-DIVIDER)/2
        for x in (COLLAR, COLLAR+opening+DIVIDER):
            result -= box(opening, width-COLLAR+EPS, HEIGHT,
                          (x, -EPS, WALL))
    else:
        result -= box(L-2*COLLAR, width-2*COLLAR, HEIGHT,
                      (COLLAR, COLLAR, WALL))
    for pocket in sockets(width, side, fit):
        result -= pocket
    for x in (12.0, L-12.0):
        result -= box(PIN_SIZE+2*fit, PIN_SIZE+2*fit, WALL+EPS,
                      (x-PIN_SIZE/2-fit, width/2-PIN_SIZE/2-fit, -EPS))
    if side:
        for x in (COLLAR/2, L-COLLAR/2):
            result -= pin_hole(x, 25.0, HEIGHT-HOLE_DEPTH, fit)
    return result


def make_drawer(fit):
    opening = (L-2*COLLAR-DIVIDER)/2
    w, d, h = opening-2*fit, SIDE-COLLAR-fit, 13.4
    tray = box(w, d, h) - box(w-2*WALL, d-2*WALL, h,
                              (WALL, WALL, WALL))
    front = box(w+2.0, SIDE_INSET, 15.5, (-1.0, -SIDE_INSET, 0))
    front -= box(10, SIDE_INSET+2*EPS, 3.6+EPS,
                 (w/2-5, -SIDE_INSET-EPS, 11.9))
    return tray + front


def headboard_profile():
    bottom = full.HEADBOARD_DEPTH * MM
    top = full.HEADBOARD_TOP_DEPTH * MM
    transition = HB_HEIGHT * (bottom-HB_DEPTH) / (bottom-top)
    return [(0, 0), (HB_DEPTH, 0), (HB_DEPTH, transition),
            (top, HB_HEIGHT), (0, HB_HEIGHT)]


def headboard_solid(y, width):
    wire = Wire.make_polygon([Vector(x, y, z) for x, z in headboard_profile()], close=True)
    return extrude(Face(wire), amount=width, dir=(0, 1, 0))


def make_headboard(fit):
    body = headboard_solid(CAP+fit, WIDTH-2*(CAP+fit))
    for y in (-EPS, WIDTH-POD_LENGTH-fit):
        body -= box(CHANNEL_X[1]-CHANNEL_X[0], POD_LENGTH+fit+EPS,
                    CHANNEL_Z[1]-CHANNEL_Z[0], (CHANNEL_X[0], y, CHANNEL_Z[0]))
    for y in (SIDE_INSET+25, WIDTH-SIDE_INSET-25):
        body -= pin_hole(COLLAR/2, y, -EPS, fit)
    return body


def make_pod(fit):
    x = CHANNEL_X[0]+fit
    z = CHANNEL_Z[0]+fit
    w = CHANNEL_X[1]-CHANNEL_X[0]-2*fit
    h = CHANNEL_Z[1]-CHANNEL_Z[0]-2*fit
    body = box(w, POD_LENGTH-CAP, h, (x, CAP, z))
    body -= box(w-2*WALL, POD_LENGTH-CAP-WALL+EPS, h,
                (x+WALL, CAP-EPS, z+WALL))
    # A long hidden tail retains 29 mm of guidance at the 40.64 mm open pose.
    return headboard_solid(0, CAP) + body


def make_foot():
    base = rounded_box(PAD, PAD, GROUND, 0.8)
    return base + box(PIN_SIZE, PIN_SIZE, 1.4,
                      ((PAD-PIN_SIZE)/2, (PAD-PIN_SIZE)/2, GROUND))


def make_key():
    return bowtie() - Pos(0, 0, -EPS)*Cylinder(
        1.2, KEY_HEIGHT+2*EPS, align=(Align.CENTER, Align.CENTER, Align.MIN))


def make_base():
    outer = rounded_box(MATTRESS_LENGTH, HALF_WIDTH, BASE_HEIGHT, 2.5)
    inner = Pos(WALL, WALL, -EPS) * rounded_box(
        MATTRESS_LENGTH-2*WALL, HALF_WIDTH-2*WALL, BASE_HEIGHT+2*EPS, 0.7)
    result = outer-inner
    for x in (MATTRESS_LENGTH/3, 2*MATTRESS_LENGTH/3):
        result += box(2*WALL, HALF_WIDTH, BASE_HEIGHT, (x-WALL, 0, 0))
    # Four short vertical locators enter the mattress's open underside recess.
    for x in (6.0, MATTRESS_LENGTH-26.0):
        for y in (2.5, HALF_WIDTH-4.3):
            pad_y = 0 if y == 2.5 else HALF_WIDTH-4.3
            result += box(20.0, 4.3, BASE_HEIGHT, (x, pad_y, 0))
            result += box(20.0, WALL, LOCATOR_HEIGHT, (x, y, BASE_HEIGHT))
    return result


def make_mattress(fit):
    outer = rounded_box(MATTRESS_LENGTH, HALF_WIDTH, MATTRESS_HEIGHT, 2.5)
    inset = 2.5-fit
    recess = box(MATTRESS_LENGTH-2*inset, HALF_WIDTH-2*inset, MATTRESS_HEIGHT-MATTRESS_SKIN+EPS,
                 (inset, inset, -EPS))
    result = outer-recess
    # Printed top-down: the full skin is on the plate first, then the ribs rise.
    for x in (MATTRESS_LENGTH/3, 2*MATTRESS_LENGTH/3):
        result += box(WALL, HALF_WIDTH-2*inset, MATTRESS_HEIGHT-RECESS_DEPTH,
                      (x-WALL/2, inset, RECESS_DEPTH))
    result += box(MATTRESS_LENGTH-2*inset, WALL, MATTRESS_HEIGHT-RECESS_DEPTH,
                  (inset, HALF_WIDTH/2-WALL/2, RECESS_DEPTH))
    return result


def make_coupon(fit):
    base = box(82, 32, WALL)
    for i, gap in enumerate((0.20, 0.25, 0.35)):
        x = 2+i*27
        # Same open-top sliding interface as a drawer; count 1/2/3 raised ticks.
        rails = box(23, 16, 7, (x, 2, 0))
        rails -= box(15+2*gap, 16+EPS, 7,
                     (x+(23-15-2*gap)/2, 2-EPS, WALL))
        base += rails
        for tick in range(i+1):
            base += box(1.2, 3, 0.6, (x+tick*2.4, 20, WALL))
    return base


def make_connector_coupon(fit):
    body = box(34, 24, 8)
    body -= Pos(10, 12, 8-KEY_HEIGHT-fit) * bowtie(KEY_HEIGHT+fit+EPS, fit)
    body -= pin_hole(26, 12, 8-HOLE_DEPTH, fit)
    return body


@dataclass
class Part:
    shape: object
    quantity: int
    slot: int
    orientation: tuple = (0, 0, 0)
    purpose: str = ""

    def printable(self):
        return normalized(Rot(*self.orientation) * self.shape)


def parts(fit):
    return {
        "side-module": Part(make_module(SIDE, True, fit), 4, 3, purpose="Open top up; outer drawer openings face out."),
        "center-module": Part(make_module(CENTER, False, fit), 2, 3, purpose="Open top up."),
        "drawer": Part(make_drawer(fit), 8, 4, purpose="Tray opening up; front and finger notch are integral."),
        "seam-key": Part(make_key(), 13, 3, purpose="Flat down; top-loaded seam key with a 2.4 mm extraction hole."),
        "foot": Part(make_foot(), 12, 3, purpose="Pad down, locating peg up."),
        "headboard-pin": Part(box(PIN_SIZE, PIN_SIZE, PIN_HEIGHT), 2, 3, purpose="One pin at each headboard locating hole."),
        "headboard": Part(make_headboard(fit), 1, 3, (0, -90, 0), "Back flat on the plate; channel roofs bridge 12.5 mm."),
        "pod-left": Part(make_pod(fit), 1, 1, (90, 0, 0), "Left end cap flat down; tray grows vertically."),
        "pod-right": Part(mirror(make_pod(fit), about=Plane.XZ), 1, 1, (-90, 0, 0), "Mirrored right end cap flat down; tray grows vertically."),
        "base-insert": Part(make_base(), 2, 2, purpose="Lattice down; four mattress locators up. Static envelope only."),
        "mattress": Part(make_mattress(fit), 2, 2, (180, 0, 0), "Top face down; hollow ribbed underside up."),
        "fit-channels": Part(make_coupon(fit), 1, 3, purpose="Calibration only: one/two/three ticks = 0.20/0.25/0.35 mm per side."),
        "fit-slider": Part(box(15, 22, 5), 1, 4, purpose="Calibration only; flat down, slide by the protruding end."),
        "fit-connectors": Part(make_connector_coupon(fit), 1, 3, purpose="Calibration only; test one production key and one pin."),
    }


def module_locations():
    for half in range(2):
        x = half*L
        yield f"left-{half}", "side-module", Pos(x, SIDE_INSET, GROUND), SIDE
        yield f"center-{half}", "center-module", Pos(x, SIDE_INSET+SIDE, GROUND), CENTER
        yield f"right-{half}", "side-module", Pos(x+L, WIDTH-SIDE_INSET, GROUND)*Rot(0, 0, 180), SIDE


def assembly(kit, fit, opened=False, exploded=False):
    objects = []

    def add(name, part, pose, group):
        objects.append((name, pose*part, group))

    opening = (L-2*COLLAR-DIVIDER)/2
    for label, kind, pose, width in module_locations():
        add(label, kit[kind].shape, pose, "structure")
        for i, x in enumerate((12, L-12)):
            add(f"foot-{label}-{i}", kit["foot"].shape,
                pose*Pos(x-PAD/2, width/2-PAD/2, -GROUND), "structure")
        if kind == "side-module":
            for i, x in enumerate((COLLAR, COLLAR+opening+DIVIDER)):
                slide = -DRAWER_TRAVEL if opened or exploded else 0
                if exploded:
                    slide = -SIDE-15
                add(f"drawer-{label}-{i}", kit["drawer"].shape,
                    pose*Pos(x+fit, slide, WALL+fit), "drawers")
    key_z = TOP-KEY_HEIGHT + (18 if exploded else 0)
    for y in (SIDE_INSET+SIDE, SIDE_INSET+SIDE+CENTER):
        for half in range(2):
            for x in (half*L+L/3, half*L+2*L/3):
                add(f"key-y-{x}-{y}", kit["seam-key"].shape,
                    Pos(x, y, key_z)*Rot(0, 0, 90), "structure")
    for y in (SIDE_INSET+12, SIDE_INSET+SIDE-12,
              SIDE_INSET+SIDE+CENTER/2, WIDTH-SIDE_INSET-12, WIDTH-SIDE_INSET-SIDE+12):
        add(f"key-x-{y}", kit["seam-key"].shape, Pos(L, y, key_z), "structure")
    hb_lift = 38 if exploded else 0
    add("headboard", kit["headboard"].shape, Pos(0, 0, TOP+hb_lift), "headboard")
    for y in (SIDE_INSET+25, WIDTH-SIDE_INSET-25):
        add(f"headboard-pin-{y}", kit["headboard-pin"].shape,
            Pos(COLLAR/2-PIN_SIZE/2, y-PIN_SIZE/2, TOP-PIN_HEIGHT/2), "structure")
    travel = POD_TRAVEL if opened else (POD_LENGTH+12 if exploded else 0)
    add("pod-left", kit["pod-left"].shape, Pos(0, -travel, TOP+hb_lift), "pods")
    add("pod-right", kit["pod-right"].shape,
        Pos(0, WIDTH+travel, TOP+hb_lift), "pods")
    for i, y in enumerate((full.MATTRESS_SIDE_MARGIN*MM, full.MATTRESS_SIDE_MARGIN*MM+HALF_WIDTH+MATTRESS_GAP)):
        add(f"base-{i}", kit["base-insert"].shape,
            Pos(SLEEP_X, y, TOP+(65 if exploded else 0)), "bases")
        add(f"mattress-{i}", kit["mattress"].shape,
            Pos(SLEEP_X, y, TOP+BASE_HEIGHT+(110 if exploded else 0)), "mattresses")
    return objects


def bboxes_overlap(a, b):
    aa, bb = a.bounding_box(), b.bounding_box()
    return all(min(getattr(aa.max, c), getattr(bb.max, c))-max(getattr(aa.min, c), getattr(bb.min, c)) > 1e-5
               for c in ("X", "Y", "Z"))


def validate(kit, fit):
    for name, part in kit.items():
        r = Report(name)
        r.valid(part.shape)
        r.solid_count(part.shape, 1)
        printable = part.printable()
        size = printable.bounding_box().size
        r._record(size.X <= 240 and size.Y <= 200 and size.Z <= 210,
                  f"print orientation fits 240 x 200 x 210 mm margin envelope: {size}")
        if name not in ("fit-channels",):
            minimum = {"foot": 1.4, "base-insert": LOCATOR_HEIGHT}.get(name, WALL)
            r.min_wall(part.shape, minimum-0.02, samples=3)
            if name in ("foot", "base-insert"):
                r.note("The lower ray threshold is the intentional short locator height, not a thin handled wall.")
        r.done()
    r = Report("assembly and interfaces")
    closed = assembly(kit, fit)
    opened = assembly(kit, fit, opened=True)
    r._record(len(closed) == 48, f"48 physical pieces, got {len(closed)}")
    combined = Compound([shape for _, shape, _ in closed])
    r.dimension(combined, "x", L*2, tol=0.05)
    r.dimension(combined, "y", WIDTH, tol=0.05)
    r.dimension(combined, "z", full.HEADBOARD_HEIGHT*MM, tol=0.05)
    for label, objects in (("closed", closed), ("open", opened)):
        collisions = []
        for i, (a_name, a, _) in enumerate(objects):
            for b_name, b, _ in objects[i+1:]:
                if bboxes_overlap(a, b) and volume_of(a.intersect(b)) > 0.001:
                    collisions.append(f"{a_name}/{b_name}")
        r._record(not collisions, f"{label}: no part interference; collisions={collisions}")
    drawer = kit["drawer"].shape
    opening = (L-2*COLLAR-DIVIDER)/2
    for x in (COLLAR, COLLAR+opening+DIVIDER):
        # Swept envelope includes every position, not only two end poses.
        sweep = extrude(Face(Wire.make_polygon([
            Vector(-1, 0, 0), Vector(opening-2*fit+1, 0, 0),
            Vector(opening-2*fit+1, 0, 15.5), Vector(-1, 0, 15.5),
        ], close=True)), amount=DRAWER_TRAVEL, dir=(0, -1, 0))
        r.no_interference(Pos(x+fit, 0, WALL+fit)*sweep, kit["side-module"].shape)
        for travel in (0, DRAWER_TRAVEL/2, DRAWER_TRAVEL):
            r.no_interference(Pos(x+fit, -travel, WALL+fit)*drawer, kit["side-module"].shape)
    for travel in (0, POD_TRAVEL/4, POD_TRAVEL/2, 3*POD_TRAVEL/4, POD_TRAVEL):
        r.no_interference(Pos(0, -travel, 0)*kit["pod-left"].shape, kit["headboard"].shape)
        r.no_interference(Pos(0, WIDTH+travel, 0)*kit["pod-right"].shape, kit["headboard"].shape)
    pod_sweep = box(CHANNEL_X[1]-CHANNEL_X[0]-2*fit, POD_LENGTH-CAP+POD_TRAVEL,
                    CHANNEL_Z[1]-CHANNEL_Z[0]-2*fit,
                    (CHANNEL_X[0]+fit, CAP-POD_TRAVEL, CHANNEL_Z[0]+fit))
    r.no_interference(pod_sweep, kit["headboard"].shape)
    r._record(POD_LENGTH-POD_TRAVEL-(CAP+fit) >= 28, "Open pod retains at least 28 mm of guide engagement.")
    r._record(COLLAR-6-fit >= WALL, "Seam socket retains at least 1.8 mm collar wall.")
    r.clearance(kit["headboard"].shape, kit["pod-left"].shape, minimum=fit-0.01)
    bottom_skin = kit["mattress"].printable().intersect(
        box(MATTRESS_LENGTH, HALF_WIDTH, MATTRESS_SKIN))
    skin_volume = (MATTRESS_LENGTH*HALF_WIDTH-(4-math.pi)*2.5**2)*MATTRESS_SKIN
    r.volume(bottom_skin, skin_volume, tol_pct=0.01)
    r.note("The mattress skin is printed directly on the plate before its vertical ribs; it is not a bridged roof.")
    r.note("Base inserts are static envelopes; mattress split and non-telescoping pod tails are miniature adaptations.")
    r.note("No captive drawer/pod stops: open poses are display limits, not mechanical stops.")
    r.note("Physical fit, adhesion, bridge finish, and sliding friction require the included coupons and first articles.")
    r.done()


def export(kit, fit, output):
    output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "scale": SCALE, "fit_per_side_mm": fit, "parts": {}, "assembly_piece_count": 48,
        "source_sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                          for name in ("model.py", "../design.py")},
    }
    for name, part in kit.items():
        oriented = part.printable()
        step = output / "parts" / f"{name}.step"
        step.parent.mkdir(exist_ok=True)
        export_step(oriented, step)
        export_stl(oriented, step.with_suffix(".stl"), tolerance=0.01, angular_tolerance=0.1)
        b = oriented.bounding_box().size
        manifest["parts"][name] = {
            "quantity": part.quantity, "slot": part.slot, "material": "PLA",
            "size_mm": [round(b.X, 3), round(b.Y, 3), round(b.Z, 3)],
            "volume_mm3": round(oriented.volume, 3), "orientation": part.purpose,
            "calibration_only": name.startswith("fit-"),
        }
    for state in ("closed", "open", "exploded"):
        items = assembly(kit, fit, opened=state == "open", exploded=state == "exploded")
        folder = output / state
        folder.mkdir(exist_ok=True)
        export_step(Compound([s for _, s, _ in items]), folder / "assembly.step")
        for group in ("structure", "drawers", "headboard", "pods", "bases", "mattresses"):
            export_stl(Compound([s for _, s, g in items if g == group]), folder / f"{group}.stl",
                       tolerance=0.01, angular_tolerance=0.1)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(f"Exported kit to {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fit", type=float, choices=(0.20, 0.25, 0.35), default=0.25,
                        help="Clearance per side, in mm; choose after physical coupon testing.")
    parser.add_argument("--out", type=Path, default=ROOT / "build")
    args = parser.parse_args()
    kit = parts(args.fit)
    validate(kit, args.fit)
    export(kit, args.fit, args.out.resolve())


if __name__ == "__main__":
    main()
