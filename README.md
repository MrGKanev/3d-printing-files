# 3d-printing-files

Models for the **Elegoo Centauri Carbon** (Orca Slicer), made with [build123d](https://github.com/gumyr/build123d).

## Models

| Model | Description | Material | Size (mm) | Status |
|---|---|---|---|---|
| [Tablet wall mount](models/tablet-wall-mount/) | Samsung Galaxy Tab A11 (8.7"), landscape. The tablet slides in from the top and lifts out freely. The USB-C cable runs behind the plate and exits on the right. | PETG | 242 x 98 x 18 | draft |

## Usage

```
/opt/homebrew/bin/python3.12 -m venv .venv && .venv/bin/pip install build123d   # once
.venv/bin/python tools/build.py   # regenerates the STL files and all READMEs
```

New model: `models/<name>/model.py` (defines `part`) + `info.toml` (copy an existing one), then run `build.py`.
Open the `.stl` in Orca. The README files are generated - don't edit them by hand.
