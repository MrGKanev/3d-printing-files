"""Slices every STL with the Orca CLI and writes ready-to-open Orca projects (.3mf) next to them.

Usage: .venv/bin/python tools/slice.py   (run tools/build.py first; needs OrcaSlicer.app)
Profile: Elegoo Centauri Carbon 0.4, 0.20mm Strength, Elegoo PETG; 4 walls, 15% gyroid.
"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORCA = "/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer"
SYS = Path.home() / "Library/Application Support/ElegooSlicer/system/Elegoo"  # unpacked Elegoo profiles (OrcaSlicer packs its own copy into .opc)
SETTINGS = f"{SYS}/machine/ECC/Elegoo Centauri Carbon 0.4 nozzle.json;{SYS}/process/ECC/0.20mm Strength @Elegoo CC 0.4 nozzle.json"
FILAMENT = f"{SYS}/filament/ECC/Elegoo PETG @ECC.json"

for stl in sorted((ROOT / "models").glob("*/*-*.stl")):
    out = Path(tempfile.mkdtemp())  # Orca writes the 3mf, gcode and stats here
    subprocess.run([ORCA, "--arrange", "1", "--slice", "0", "--curr-bed-type", "Textured PEI Plate", "--wall-loops", "4", "--sparse-infill-density", "15%",
                    "--sparse-infill-pattern", "gyroid", "--export-statistics", "--load-settings", SETTINGS,
                    "--load-filaments", FILAMENT, "--outputdir", str(out), "--export-3mf", stl.with_suffix(".3mf").name,
                    str(stl)], check=True, capture_output=True)
    (out / stl.with_suffix(".3mf").name).replace(stl.with_suffix(".3mf"))
    s = json.loads(next(out.glob("*.statistics.json")).read_text())["summary"]
    print(f"{stl.stem}: {s['time'] / 3600:.1f} h, {s['weight']:.0f} g")
