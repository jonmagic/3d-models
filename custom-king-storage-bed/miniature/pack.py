#!/usr/bin/env python3
"""Package only a complete, current set of individually sliced miniature parts."""

import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def duration(seconds):
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    return f"{hours}h {minutes:02}m {seconds:02}s"


def record_renders():
    manifest = BUILD / "manifest.json"
    record = {"manifest_sha256": digest(manifest), "images": {}}
    for pose in ("closed", "open", "exploded"):
        path = BUILD / pose / "structure-iso.png"
        if path.stat().st_mtime_ns < manifest.stat().st_mtime_ns:
            raise ValueError(f"Render predates the model export: {path}")
        record["images"][pose] = digest(path)
    (BUILD / "render-manifest.json").write_text(json.dumps(record, indent=2)+"\n")


def main():
    manifest = json.loads((BUILD / "manifest.json").read_text())
    report = json.loads((BUILD / "print-summary.json").read_text())
    if set(report["parts"]) != set(manifest["parts"]):
        raise ValueError("Incomplete slicer summary; run ruby slice.rb without part selectors.")
    if report["fit_per_side_mm"] != manifest["fit_per_side_mm"]:
        raise ValueError("Slicer summary uses a different fit setting; re-slice the complete kit.")
    for name in ("model.py", "../design.py"):
        if digest(ROOT / name) != manifest["source_sha256"][name]:
            raise ValueError(f"Source changed since CAD export: {name}; rebuild the kit.")
    if digest(ROOT / "slice.rb") != report["slicer_script_sha256"]:
        raise ValueError("Slicing script changed since this run; re-slice the complete kit.")
    if digest(BUILD / "manifest.json") != report["manifest_sha256"]:
        raise ValueError("Model manifest changed since slicing; re-slice the complete kit.")
    renders = json.loads((BUILD / "render-manifest.json").read_text())
    if renders["manifest_sha256"] != digest(BUILD / "manifest.json"):
        raise ValueError("Assembly renders are from a different model export; run bash build.sh.")
    files = [ROOT / "README.md", BUILD / "manifest.json", BUILD / "print-summary.json"]
    for name, part in manifest["parts"].items():
        sliced = report["parts"][name]
        for key in ("quantity", "slot", "calibration_only"):
            if part[key] != sliced[key]:
                raise ValueError(f"Manifest/slicer mismatch: {name} {key}")
        for suffix, hash_key, directory in (
            ("stl", "stl_sha256", "parts"), ("bgcode", "gcode_sha256", "gcode")):
            path = BUILD / directory / f"{name}.{suffix}"
            if digest(path) != sliced[hash_key]:
                raise ValueError(f"Stale or modified file: {path}; rebuild/re-slice before packaging.")
            files.append(path)
        files.append(BUILD / "parts" / f"{name}.step")
        files.append(BUILD / "slice-reports" / f"{name}.json")
    production = [p for p in report["parts"].values() if not p["calibration_only"]]
    if sum(p["quantity"] for p in production) != manifest["assembly_piece_count"]:
        raise ValueError("Production piece count does not match the assembly.")

    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for pose in ("closed", "open", "exploded"):
        image = BUILD / pose / "structure-iso.png"
        if not image.is_file():
            raise FileNotFoundError(f"Missing {pose} render; run bash build.sh.")
        if digest(image) != renders["images"][pose]:
            raise ValueError(f"Changed {pose} render; run bash build.sh.")
        destination = assets / f"{pose}.png"
        shutil.copyfile(image, destination)
        files.append(destination)

    lines = [
        "# Miniature bed print order and machine estimates",
        "",
        f"Scale 1:10; {report['fit_per_side_mm']:.2f} mm per-side fit; {report['production_piece_count']} production pieces. Use the illustrated [assembly guide](README.md) and its physical fit gates before printing duplicates.",
        "",
        "This print-only bundle includes pre-oriented STL, exact STEP, and single-part binary g-code. Regenerate from `custom-king-storage-bed/miniature/` in the source repository, not by scaling an assembly mesh. No printer upload or start is performed by these scripts.",
        "",
        "## Print first",
        "",
        "Print the three calibration pieces, one production seam key, and one production headboard pin. Then test one drawer with one side module. Confirm one left pod with the headboard before producing the second pod. Keys, pins, and first articles count toward the production quantities below.",
        "",
        "## Complete job list",
        "",
        "Each file contains one copy, already oriented. Repeat the job to reach the total quantity. Do not print this entire list before the fit samples pass.",
        "",
        "The sleep system uses one each of `base-insert`, `mattress`, `base-raised`, and `mattress-raised`. The head-up pair has a fixed 15.24 mm rise over 60.96 mm (14.036 degrees), matching 6 inches over a 24-inch run at full scale. Keep each mattress with its matching support.",
        "",
        "| File | Total copies | Slot / PLA color | Size X x Y x Z, mm | Brim | Time per copy | Filament per copy |",
        "|---|---:|---|---|---:|---|---:|",
    ]
    for name, part in report["parts"].items():
        quantity = f"{part['quantity']} (sample)" if part["calibration_only"] else str(part["quantity"])
        dimensions = " x ".join(f"{value:.1f}" for value in part["size_mm"])
        lines.append(f"| [`{name}.bgcode`](build/gcode/{name}.bgcode) | {quantity} | {part['slot']} / {part['color']} | {dimensions} | {part['brim_mm']} mm | {part['time']} | {part['grams']:.2f} g |")
    lines += [
        "",
        f"**Production totals:** {duration(report['production_seconds'])} and {report['production_grams']:.2f} g. **Three calibration pieces:** {duration(report['calibration_seconds'])} and {report['calibration_grams']:.2f} g, in addition to production totals. The tested key and pin are already included in production totals.",
        "",
        "These are PrusaSlicer estimates summed across separate single-copy jobs, not elapsed project time. They exclude loading, unloading, plate cleaning, cooldown, assembly, retries, and failed prints. Batching or changing profiles will change the numbers.",
        "",
        "All jobs use 0.15 mm layers, 0.20 mm first layer, four perimeters, 15% gyroid infill, and six top/bottom solid layers, with supports disabled and no in-print tool changes. Slot 5 PETG is unused. Confirm the actual PLA spools match before printing.",
        "",
        "Source and g-code SHA-256 hashes are recorded per part in `build/print-summary.json`; packaging refuses mismatches. The STL is the slicing derivative; parametric source lives in the repository.",
        "",
    ]
    plan = ROOT / "print-plan.md"
    plan.write_text("\n".join(lines))
    files.append(plan)
    archive = BUILD / "miniature-print-kit.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, Path("miniature-print-kit") / path.relative_to(ROOT))
    with zipfile.ZipFile(archive) as bundle:
        bad = bundle.testzip()
        if bad:
            raise ValueError(f"ZIP checksum failed for {bad}")
    print(f"Packaged {len(files)} files: {archive}")
    print(f"Production: {duration(report['production_seconds'])}, {report['production_grams']:.2f} g")


if __name__ == "__main__":
    if sys.argv[1:] == ["--record-renders"]:
        record_renders()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit("Usage: python3 pack.py [--record-renders]")
