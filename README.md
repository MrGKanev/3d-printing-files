# 3d-printing-files

Models for the **Elegoo Centauri Carbon** (Orca Slicer), made with [build123d](https://github.com/gumyr/build123d).

## Models

| Model | Version | Description | Material | Size (mm) | Status |
|---|---|---|---|---|---|
| [Tablet wall mount](models/tablet-wall-mount/) | 0.4 | Samsung Galaxy Tab A11 (8.7"), landscape. Two-part wall mount: plate + press-fit cover (no small screws). The USB-C cable runs through the plate and out a channel on the back. Extra room around the power/volume buttons. | PETG | plate 244 x 158 x 14; cover 244 x 158 x 10 | draft |

## Usage

```
/opt/homebrew/bin/python3.12 -m venv .venv && .venv/bin/pip install build123d   # once
.venv/bin/python tools/build.py   # regenerates the STL files and all READMEs
```

New model: `models/<name>/model.py` (defines `part`) + `info.toml` (copy an existing one), then run `build.py`.
Open the `.stl` in Orca. The README files are generated - don't edit them by hand.
