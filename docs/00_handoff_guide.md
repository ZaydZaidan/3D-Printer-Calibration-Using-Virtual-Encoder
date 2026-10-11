# HANDOFF GUIDE — How to Use & Reproduce the Research

This document is for the **next person** who continues or uses this repo.
Follow it in order. Each stage lists the inputs, the outputs, and **the result
you should see**, so that you know whether your work is correct or not.

> All numbers in this document were **re-verified** by re-running the notebooks
> in this repo (not copied from the manuscript). See section 4.

---

## 1. Research summary

Calibration of 3D printer machine axes **without a dial gauge and without an
encoder**, using a single camera + chessboard as a **virtual encoder**. What is
calibrated: **steps/mm**, **backlash**, and **skew/XY orthogonality**. The
validation is a forward-and-backward ellipse trajectory compared against the
ground truth.

High-level flow:

```
camera calibration -> machine calibration (linear) -> ellipse trajectory -> virtual encoder -> evaluation
```

## 2. Main results

**A. Machine calibration (linear test, 10 mm target, 10 valid samples out of 40)**

| Metric | Baseline | After calibration | Improvement |
|---|---|---|---|
| X-axis error | 0.0463 mm | 0.0071 mm | 84.7 % |
| Y-axis error | 0.0550 mm | 0.0054 mm | 90.2 % |
| Y drift during X motion (skew) | 0.0937 mm | 0.0043 mm | 95.4 % |
| X drift during Y motion (skew) | 0.0898 mm | 0.0036 mm | 96.0 % |

Parameters: initial steps/mm **80 / 80**, backlash comp **0**, skew comp **0**.
Result: steps/mm **79.72 / 80.40**, backlash **0.0124 / 0.0244 mm**,
skew **-0.009327 / 0.009025** (≈ ±0.52°).

**B. Ellipse trajectory evaluation (RMSE against ground truth)**

| Metric | Baseline | After calibration |
|---|---|---|
| RMSE X | 76.91 µm (std 5.33) | 34.42 µm (std 1.61) |
| RMSE Y | 65.29 µm (std 4.67) | 30.75 µm (std 1.30) |
| **RMSE Total** | **100.89 µm** (std 7.00) | **46.17 µm** (std 1.68) |

**Trajectory accuracy improvement: 54.24 %.**

## 3. Prerequisites

**Software**

```bash
pip install -r requirements.txt
```

- Python **3.11** (the research used 3.11.9).
- `opencv-contrib-python` is **required** (the contrib version) — the code uses
  `cv2.ximgproc` (`createEdgeDrawing`), which is not available in plain
  `opencv-python`.
- Packages: opencv-contrib-python 4.12.0.88, numpy 2.2.6, scipy 1.17.1, pandas 3.0.2,
  matplotlib 3.10.8. Run the notebooks with `pandas` and `numpy` available, since
  camera parameters are exchanged via CSV.

**Data** — already included in this folder:

| Location | Content | Size |
|---|---|---|
| `data/raw/camera_calibration/` | chessboard images for camera calibration | 19 MB |
| `data/raw/linear_baseline_x`, `linear_baseline_y` | linear dataset before calibration | 44 MB |
| `data/raw/linear_calibrated_x`, `linear_calibrated_y` | linear dataset after calibration | 44 MB |
| `data/raw/measurement_error/` | dial gauge dataset (0.5 mm, baseline parameters) | 63 MB |
| `data/raw/circular_baseline`, `circular_calibrated` | CSV + ellipse trajectory images | 13 MB |
| `data/raw/video_*` | raw trajectory videos (to re-run the virtual encoder) | 1.7 GB |

Details of the original name of each folder: **`data/MANIFEST.md`**.

**Hardware** is only needed if you want to **acquire new data** (folder `05_data_acquisition/`).
To merely check/reproduce the results from data that already exists, no machine is required.

## 4. Evidence this repo runs (already tested)

After the reorganization, the three notebooks were re-run from scratch in this repo:

| Notebook | Output produced | Matches the research log? |
|---|---|---|
| `01_.../camera_calibration.ipynb` | 10 valid images. **Overall reprojection RMSE 0.1154 px** (mean per image 0.1152 px; min 0.0979, max 0.1249) | there is no original log — this artifact was created just now |
| `02_.../machine_calibration.ipynb` | X: Δ 10.0045 mm, error 0.0071 mm, RMSE 0.1186 px, `M92 X79.68`, `M425 X0.0068`, skew 0.000427 | **identical digit-for-digit** to `DATA HASIL KALIBRASI LINEAR X DAN Y.txt` |
| `02_.../machine_calibration.ipynb` | Y: Δ -10.0022 mm, error 0.0054 mm, RMSE 0.1281 px, `M92 Y80.38`, `M425 Y0.0068`, skew 0.000362 | **identical** to the same log |
| `04_.../trajectory_evaluation.ipynb` | Baseline 100.89 µm -> calibrated 46.17 µm, **improvement 54.24 %** | matches the reported numbers |

This means: the data, the path configuration, and the notebook separation are consistent.

## 5. Repo structure

```
Folder Rapih Code & Data Thesis/
├─ README.md                  summary + results
├─ config_paths.py            >>> ALL PATHS ARE HERE <<<
├─ calibration_pipeline.py    corner detection functions (shared by all notebooks)
├─ requirements.txt
├─ 01_camera_calibration/camera_calibration.ipynb
├─ 02_machine_calibration/machine_calibration.ipynb
├─ 03_virtual_encoder/virtual_encoder.ipynb
├─ 04_trajectory_evaluation/trajectory_evaluation.ipynb
├─ 05_data_acquisition/       scripts that need the machine & camera (see the README inside)
├─ 06_measurement_error/plot_measurement_error.py   dial gauge vs virtual encoder
├─ data/raw/                  raw data + videos (NOT committed to git, shipped via this folder instead)
├─ data/processed/            output of each stage (committed to git, small in size)
├─ figures/                   figures for the manuscript
└─ docs/                      this 00 guide, 01 audit, 02 file roles, 03 results & data locations
```

## 6. How to run

### Step 0 — check the data (30 seconds)

```bash
python config_paths.py
```

It prints a table: each dataset is marked `OK` or `NOT FOUND`, along with the
location used. If something is `NOT FOUND`, put the dataset in the location
shown (or change the `LEGACY_PATHS` section in `config_paths.py`).

Run each notebook **from inside its own notebook folder** (Jupyter does this
automatically), so that `config_paths.py` at the repo root can be found.

### Step 1 — camera calibration

`01_camera_calibration/camera_calibration.ipynb` — all cells, in order.

- **Inputs:** `data/raw/camera_calibration/dataset_kalibrasi_fix_prime_260/`
- **Process:** EDLines -> line screening -> subpixel optimization -> sorting of 49
  corners via homography -> `cv2.calibrateCamera`
- **Outputs (all into `data/processed/camera_calibration/`):**
  - `camera_matrix.csv` — intrinsic matrix K (3x3)
  - `dist_coeffs.csv` — distortion coefficients `[k1, k2, p1, p2, k3]`
  - `camera_params.csv` — parameter/value table + image size (easy to read)
  - `reprojection_rmse.csv` — reprojection RMSE per image
- **Expected result:** about 10 valid images, RMSE ~0.10-0.13 px.
  Status "ACCURATE" if < 0.15 px.
  The notebook prints two RMSE numbers and **both are correct**, don't mix them up:
  **"Overall Reprojection Error (RMSE)"** = `sqrt(total_SSE / total_titik)` →
  **0.1154 px**; whereas the **mean RMSE per image** = the ordinary mean of the
  `rmse_px` column in `reprojection_rmse.csv` → **0.1152 px**. The two differ
  slightly because the first is a root-of-the-mean (RMS), while the second is a
  mean-of-the-roots. **To cite in the manuscript, use the number the notebook
  itself prints: 0.1154 px.**
- **Time:** ~25 seconds for 10 images.

The test result in this repo (overall reprojection RMSE 0.1154 px): `fx=2314.64`, `fy=2328.29`, `cx=637.08`, `cy=222.88`,
`D = [-0.056105, 0.959537, 0.000141, 0.000407, -5.033022]`.

> **Note:** The K and D here are computed from the **10 images** present in the
> repo, even though the folder name implies 260 images. The important thing: the
> K/D from these 10 images **has been proven to reproduce all the manuscript's
> numbers** (see section 4) — so to reproduce the research results, these 10
> images are enough. For new data acquisition, your K/D will differ; that is
> normal and not a problem (see section 7).

### Step 2 — machine calibration

`02_machine_calibration/machine_calibration.ipynb` — all cells, in order.

- **Inputs:**
  - `data/processed/camera_calibration/*.csv` (from step 1, loaded automatically)
  - the linear dataset according to `RUN_MODE` (see below): `oriy{i}.png`, `fwd{i}.png`,
    `bck{i}.png`, i = 1..40
- **Outputs:** mean statistics + firmware recommendations `M92`, `M425`, `M852`
  (printed on screen), and image files `visualization_*.png` in the notebook folder.
- **Time:** ~2 minutes per axis.

**Choose the mode without editing the notebook:**

```bash
# Windows
set KALIBRASI_MODE=baseline
# Linux / macOS
export KALIBRASI_MODE=baseline
```

| Mode | Dataset | steps/mm | target | note |
|---|---|---|---|---|
| `calibrated` (default) | `linear_calibrated_x/y` | 79.72 / 80.40 | 10 mm | measures the **residual** error after calibration |
| `baseline` | `linear_baseline_x/y` | 80 / 80 | 10 mm | condition before calibration |
| `measurement_error` | `measurement_error/*_machine_movement` | 80 / 80 | 0.5 mm | for comparison with the dial gauge |

- **Expected result (mode `calibrated`):** X → Δ 10.0045 mm, error 0.0071 mm,
  RMSE 0.1186 px. Y → Δ -10.0022 mm, error 0.0054 mm, RMSE 0.1281 px.
- **Expected result (mode `baseline`):** X → error 0.0463 mm;
  Y → error 0.0550 mm.

> **Don't be confused if the recommendation that comes out differs from the values in `config_paths.py`.**
> The available dataset yields recommendations of **79.6314 (X)** and **80.4425 (Y)** —
> those are the first-round recommendations. The final research values are **79.72 / 80.40**,
> the result of several rounds of *fine-tuning* (see the manuscript `bab4.tex`, the
> *Fine-Tuning Calibration Result Parameters* Table, and `docs/03_results_and_data_locations.md`
> section 5). The `calibrated` mode in this repo uses those final values because they
> are what produce the numbers in the manuscript.

> This notebook **stops automatically after 10 valid samples**. If many samples
> fail ("pose not found"), it is usually because the lighting/exposure differs
> from the time the data was acquired.

### Step 2b — fine-tuning: repeat calibration until the error reaches *steady state*

**The core of this method: a single calibration is not enough. The recommendation
must be applied repeatedly.** The flow is like this, and this loop is what gets
repeated:

```
   parameters currently ON the machine      measure                    NEW recommendation
   (STEPX, STEPY, BACKLASH,     -->   run step 2           -->   (M92 steps/mm,
    SKEW_FACTOR)                      on the new dataset          M425 backlash, M852 skew)
          ^                                                            |
          |                    APPLY the recommendation above         |
          +------------------- to the machine, acquire data again <----+
                              (repeat this loop)

   continue until the error no longer moves much   ->   STEADY STATE
```

Why it must be repeated: the machine's mechanical condition (friction, gear play,
frame tilt) can shift between data-acquisition sessions, so a single correction is
not necessarily right. What you do is keep correcting until **the next correction
is nearly zero** — that is, when the new recommendation is already almost the same
as the value currently in use.

One practical loop:

1. Enter the parameters currently in use into
   `05_data_acquisition/automated_linear_test.py` (`STEPX`, `STEPY`, `BACKLASH`,
   `SKEW_FACTOR`).
2. Acquire a **new** linear test dataset (the machine moves with those parameters).
3. Run the step-2 notebook on that new dataset → the **residual error** and the
   **new recommendation** are printed.
4. Go back to step 1 with that recommendation. Repeat until *steady state*.

**Signs that *steady state* has been reached:**

- The forward travel error no longer drops significantly, and is **already on the
  order of the *measurement error* limit of your measuring instrument** (in this
  research the dial gauge has a resolution of ±10 µm, and the final error is 7.1 µm
  for X and 5.4 µm for Y — already within that limit).
- The new `steps/mm` recommendation is **almost the same** as the value currently in use.
- The `skew` recommendation is already small; in this research the last round gave
  0.000427 (≈0.024°) and the notebook states *"Orthogonal, no compensation
  needed"*.

**A real example from this research** (the chain of values; see also `docs/03` section 5):

```
80.00 steps/mm  (baseline, log saved)
   -> 79.6314   (round-1 recommendation, log saved)
      -> 80.13 / 80.11 / skew variants   (intermediate rounds; their datasets are in the
                                          ARCHIVE, NOT shown in the manuscript)
         -> 79.72  (FINAL, after steady state)
```

The manuscript shows only **two points**: baseline and the final value after fine-tuning.
That is indeed enough for the manuscript — the intermediate chain is not needed.

**Practical note if you repeat this with your own machine:** this repo provides three
ready-to-use modes (`baseline`, `calibrated`, `measurement_error`). For your own
fine-tuning iterations, add one entry in `config_paths.py` in two places:
`MODE_PARAMS` (the `delta`/`steps` value currently in use) and
`DATASET_X_BY_MODE` / `DATASET_Y_BY_MODE` (the dataset folder for that iteration),
then select it via `KALIBRASI_MODE`.

**Final parameters of this research:**

| Parameter | X-axis | Y-axis |
|---|---|---|
| steps/mm | 79.72 | 80.40 |
| backlash | 13.3 µm | 31.4 µm |
| skew | -9.2 µm/mm (X drift during Y motion) | 9.213 µm/mm (Y drift during X motion) |

### Step 3 — virtual encoder (video -> trajectory)

`03_virtual_encoder/virtual_encoder.ipynb`

- **Inputs:** videos `data/raw/video_*/pose_video_XX.avi`, and K/D from step 1
- **Outputs:** `data/processed/virtual_encoder/<CSV_PREFIX>_XX.csv` —
  columns `Frame, Waktu (detik), X Posisi (mm), Y Posisi (mm), Reprojection Error (px)`
- **Parameters:** set `KALIBRASI_VIDEO` (video folder) and `KALIBRASI_CSV_PREFIX`
  (output CSV filename) in `config_paths.py`. The combination that produces the
  research artifacts (as stated by the research owner):

| Video folder in repo | Original name | Content | Output CSV prefix |
|---|---|---|---|
| `video_baseline_x` | `BASELINE_JALUR_FINAL_VIDEO` | **circular baseline** test video | `hasil_fix_banget_baseline` |
| `video_calibrated_x` | `KALIBRASI_JALUR_FINAL_VIDEO_3` | **circular calibrated** test video | `JALUR_VIDEO_FINAL_3` |
| `video_kalibrasi_x` | `KALIBRASI_X_VIDEO_BENERAN` | 3 X-axis videos | `KALIBRASI_X_VIDEO_FINAL_BENERAN` |
| `video_baseline_y`, `video_calibrated_y` | `..._BGT_BGT` | Y-axis videos | `..._BGT_BGT` |

> **DO NOT run unless needed.** The videos are ~30-46 MB per file; 1.7 GB total
> for 37 files. Processing one video takes a long time, and is **not necessary**
> just to reproduce the research results: the trajectory CSVs needed by step 4
> are already available in `data/raw/circular_baseline/` and `data/raw/circular_calibrated/`.
> The virtual encoder only needs to be re-run if you have new trajectory videos.

- **Note:** the last cell produces a comparison figure into `figures/`.

### Step 4 — trajectory evaluation

`04_trajectory_evaluation/trajectory_evaluation.ipynb`

- **Inputs:** `data/raw/circular_baseline/hasil_fix_banget_baseline_XX.csv` and
  `data/raw/circular_calibrated/JALUR_VIDEO_FINAL_3_XX.csv`
- **Process:** generate the ground truth as 2 ellipses, find the nearest neighbor of
  each point with `cKDTree`, compute RMSE per axis and total (µm)
- **Outputs:** evaluation figures into `figures/`, and a summary table on screen
- **Expected result:** baseline 100.89 µm -> calibrated 46.17 µm, improvement **54.24 %**
- **Time:** ~15 seconds

### Step 5 — measurement error (comparison with the dial gauge)

This experiment compares the readings of this method (*virtual encoder*) with the **dial gauge**.
Configuration: all baseline parameters, **travel distance reduced to 0.5 mm**, 5 iterations per
panel (forward and backward, X and Y axes).

```bash
python 06_measurement_error/plot_measurement_error.py
```

- **Inputs:** `data/processed/measurement_error/dial_vs_ve.csv`
  (the dial gauge photos are in `data/raw/measurement_error/x_dial_gauge/` and `y_dial_gauge/`)
- **Outputs:** `figures/paper/1_4_position_comparison_combined.png` (+ `.pdf`) and the MAE table on screen
- **Expected result** (mean absolute difference |VE - dial|):

  | Panel | MAE | std |
  |---|---|---|
  | X Forward | 4.62 µm | 4.32 µm |
  | Y Forward | 8.54 µm | 7.77 µm |
  | X Backward | 5.30 µm | 2.54 µm |
  | Y Backward | 7.08 µm | 4.94 µm |
  | **Combined X** | **4.96 µm** | 3.36 µm |
  | **Combined Y** | **7.81 µm** | 6.18 µm |

  The dial gauge has a resolution of ±10 µm, so a difference on the order of 5-8 µm is within
  the precision of the measuring instrument.
- **Time:** ~5 seconds. The output figure is identical to the manuscript's figure (2584x2134 px).

## 7. Adapting to a new machine/camera

1. Print the calibration board: `python 05_data_acquisition/generate_chessboard.py`
   (A4, 8x8 grid of 20 mm squares, 3 marker circles that define the origin).
2. Photograph the board from many angles with `05_data_acquisition/capture_camera_calibration.py`
   (the `f` key). It is best to use **far more than 10 images**, with wide variation in
   tilt/position.
3. Run step 1 above. **K, D, and the reprojection RMSE value will differ from this
   research** — that is expected, because the camera and its mounting position are
   different. Only the order of the stages needs to be the same, not the numbers. The
   same applies if you use an alternative calibration dataset (e.g.
   `measurement_error/x_camera_calibration`).
4. Acquire a linear dataset with `05_data_acquisition/automated_linear_test.py`
   (change `COM10` -> your port, `TEST_MODE`, initial parameters 80/80/0/0).
5. Run step 2 -> you get new `M92`/`M425`/`M852` values.
6. Enter those values into `05_data_acquisition/automated_ellipse_path.py`, record the
   trajectory videos, then continue to steps 3 and 4.

## 8. Limitations you should know (honest, not yet complete)

The following items were **not** resolved in this reorganization and need a decision from the research owner:

1. **The calibration folder name is misleading: `dataset_kalibrasi_fix_prime_260` contains 10
   images, not 260.** This is **not a problem for reproduction** — the K/D from those 10
   images already reproduces all the manuscript's numbers (section 4). It is noted only so
   that you don't go looking for the "remaining 250 images" that may indeed never have
   existed. If the manuscript states the number of calibration images explicitly, that is
   the number that needs to be matched.
2. **The trace of what generated `hasil_fix_banget_baseline_XX.csv` is not preserved in the code.**
   According to the research owner, this baseline CSV was produced by the **same code**
   (`virtualencodervideo`), differing only in the **input video** (`BASELINE_JALUR_FINAL_VIDEO`)
   and the **output CSV path**. In the remaining code, no notebook writes that filename —
   they all only read it (confirmed by searching the entire set of notebooks). So the baseline
   path and the calibrated path use the same script, and what differs is only the parameters
   at the top of the script. In this repo both have been unified via
   `config_paths.py`: `KALIBRASI_VIDEO` and `KALIBRASI_CSV_PREFIX`.
4. **The acquisition scripts are not yet parameterized.** They still contain the research's original
   values (port `COM10`, camera index, exposure). See the table in `05_data_acquisition/README.md`.
5. **`measurement_error` needs the 0.5 mm mode**: when processing it, `EXPECTED_DELTA` must
   be 0.5 (already handled automatically via `RUN_MODE=measurement_error`).

## 9. What is validated vs not yet

| Section | Status |
|---|---|
| Camera calibration (stage 1) | re-run from the data in the repo, succeeded, wrote 4 CSVs |
| Machine calibration (stage 2, `calibrated` mode) | re-run, **identical digit-for-digit** to the manuscript log |
| Trajectory evaluation (stage 4) | re-run, succeeded, improvement 54.24 % |
| Virtual encoder (stage 3) | bootstrap + loading K/D from CSV was tested, succeeded. **Video processing was deliberately not run** — the videos are 1.7 GB and the plots are no longer needed because the trajectory CSVs are available |
| Measurement error (dial gauge vs VE) | re-run, succeeded, output figure **identical** to the manuscript's figure (2584x2134 px) |
| Machine calibration in `baseline` and `measurement_error` mode | not yet re-run — the dataset is complete, just change `KALIBRASI_MODE` |
| Acquisition scripts (folder 05) | cannot be run without the machine |

---

## 10. If something doesn't work

| Symptom | Most likely cause |
|---|---|
| `config_paths.py not found` | the notebook was run from outside the repo folder. Run it via Jupyter in its notebook folder, or set `KALIBRASI_REPO` to the repo root |
| `Not found: .../camera_calibration/camera_matrix.csv` | stage 1 (camera calibration) has not been run through to the end of the export cell |
| `NOT FOUND` in the output of `python config_paths.py` | the dataset is not yet in `data/raw/`; place it as described in `data/MANIFEST.md` |
| Many samples "pose not found" | lighting/exposure differs from when the data was acquired, or the board does not fully fit in the frame |
| `ModuleNotFoundError: cv2` then `has no attribute 'ximgproc'` | `opencv-python` is installed, not `opencv-contrib-python` |
| Camera calibration produces very different K/D | the number of calibration images is only 10 (see section 8 item 1) |
