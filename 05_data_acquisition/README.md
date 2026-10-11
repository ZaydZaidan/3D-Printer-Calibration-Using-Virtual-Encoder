# 05 — Acquisition Scripts (requires machine & camera)

The scripts in this folder **can only be run with hardware**: a 3D printer connected
over serial + a camera. These scripts **populate** `data/raw/`, they do not process it.
Their contents are identical to the original research code (contents unchanged, only the
file names).

| File | Role | Lines that MUST be adjusted |
|---|---|---|
| `generate_chessboard.py` | Print the A4 calibration board (8x8 squares of 20 mm + 3 marker circles) | - |
| `capture_camera_calibration.py` | Capture chessboard images for camera calibration (`f` key) | line 23 `cv2.VideoCapture(1)` (camera index), line 29 FPS, line 41 exposure |
| `automated_linear_test.py` | `oriy`/`fwd`/`bck` linear movement 40x for machine calibration | line 19 `PORT` (e.g. `COM10`), lines 21-26 `BACKLASH`/`SKEW_FACTOR`/`STEPX`/`STEPY`, line 30 `TEST_MODE` |
| `automated_ellipse_path.py` | Run the ellipse path + record video | line 12 `PORT`, lines 15-21 calibration parameters, line 23 `TOTAL_ITERASI`, line 322 camera index |

Machine prerequisites:

- RepRap/Marlin firmware that accepts `M92`, `M425`, `M852`, `G28`, `G1`, `M400`, `G4`.
- **Monochrome** 1280x720 camera (the research used OV9281). The scripts force grayscale.
- Exposure locked manually (`AUTO_EXPOSURE=1`, `EXPOSURE=-7`) so lighting stays stable.

Acquisition flow per session:

```
capture_camera_calibration.py   -> dataset_sesi_<timestamp>/kalibrasi/calib_XXXX.png
automated_linear_test.py        -> dataset_<Xpos|Xneg|Ypos|Yneg>_sesi_<ts>/kalibrasi/oriy,fwd,bck{i}.png
automated_ellipse_path.py       -> dataset_otomatis_sesi_<timestamp>/video/pose_video_XX.avi
```

When finished, move the results to `data/raw/` according to `data/MANIFEST.md`.

> The original `automated_linear_test.py` script used a travel distance of **10 mm** for
> modes `X-`/`Y-` and **0.5 mm** for modes `X+`/`Y+` (the latter is used for the
> measurement error / dial gauge experiment).
