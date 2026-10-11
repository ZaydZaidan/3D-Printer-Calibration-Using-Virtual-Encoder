# Research Results & Final Data Locations

## 1. Final data locations

> Stated by the author: *"the final data from my research that I used is in
> `Kuliah/After Lulus Paper/Data`"*

**Final reference = `After Lulus Paper/Data/`.** The `Semester 7/SEMPRO/Code/` folder contains
working copies + experiment archives and is **not** used as the reference.

### 1.1 Dataset mapping — CONFIRMED by the author

| Name in repo (new) | Original name | Axis | Condition | Files | Size |
|---|---|---|---|---|---|
| `linear_baseline_x/` | `BASELINE_X_INDIVIDUAL` | X | linear **baseline** | 120 | 22 MB |
| `linear_baseline_y/` | `BASELINE_Y_FIX_METHOD` | Y | linear **baseline** | 120 | 22 MB |
| `linear_calibrated_x/` | `X_LAST_FIX` | X | **after calibration** | 120 | 22 MB |
| `linear_calibrated_y/` | `Y_LAST_FIX` | Y | **after calibration** | 120 | 21 MB |
| `measurement_error/x_camera_calibration/` | `kalibrator_systematic_error_x` | X | camera calibration dataset for the measurement error session | 54 | 11 MB |
| `measurement_error/x_machine_movement/` | `systematic_error_x` | X | machine movement, 0.5 mm, baseline | 120 | 24 MB |
| `measurement_error/y_camera_calibration/` | `kalibrator_systematic_y` | Y | camera calibration dataset for the measurement error session | 31 | 5.4 MB |
| `measurement_error/y_machine_movement/` | `systematic_error_Y` | Y | machine movement, 0.5 mm, baseline | 120 | 21 MB |
| `circular_baseline/` | `Circular Baseline` | XY | ellipse path, baseline | 20 | 4.1 MB |
| `circular_calibrated/` | `Circular Kalibrasi` | XY | ellipse path, calibrated | 33 | 8.2 MB |
| `camera_calibration/dataset_kalibrasi_fix_prime_260/` | `dataset_kalibrasi_fix_prime_260` | - | camera calibration images | 10 | small |
| `camera_calibration/dataset_kalibrasi_ditambah/` | `dataset_kalibrasi_ditambah` | - | additional calibration images | 97 | ~20 MB |

Details + git status per dataset: `data/MANIFEST.md`.

### 1.2 Result file name mapping

| Name in `SEMPRO/Code/` | Name in `After Lulus Paper/Data/` |
|---|---|
| `kalibrasicamera/DATA FIX/hasil_fix_banget_baseline_XX.csv` | `Circular Baseline/hasil_fix_banget_baseline_XX.csv` |
| `kalibrasicamera/JALUR_VIDEO_FINAL_3_XX.csv` | `Circular Kalibrasi/JALUR_VIDEO_FINAL_3_XX.csv` |

Basis: `evaluasilintasan.ipynb` reads both of those name patterns (cell 0 -> baseline, cells 1 & 4 -> calibration).

Both CSVs were produced by the **same code** (`virtualencodervideo`), differing only in
the input video and the output CSV path (stated by the research owner). In the remaining
code, no notebook writes the name `hasil_fix_banget_baseline_*` — all of them only read.
In this repo that difference has been unified through `KALIBRASI_VIDEO` + `KALIBRASI_CSV_PREFIX`
in `config_paths.py`:

| Input video | Output CSV prefix |
|---|---|
| `video_baseline_x` (`BASELINE_JALUR_FINAL_VIDEO`) | `hasil_fix_banget_baseline` |
| `video_calibrated_x` (`KALIBRASI_JALUR_FINAL_VIDEO_3`) | `JALUR_VIDEO_FINAL_3` |

---

## 2. Initial (baseline) and final parameters

`otomasikalibrasi.py` lines 19-26 — **baseline** configuration:

| Parameter | Baseline value |
|---|---|
| `BACKLASH` (compensation) | 0 |
| `SKEW_FACTOR` | 0 |
| `STEPX` | 80 |
| `STEPY` | 80 |

The commented block in lines 10-17 contains the **calibration result** values that were then used:
backlash 0.0133 (X), skew 0.009213, steps/mm 79.72 (X) and 80.40 (Y).

---

## 3. Linear test results (X and Y axes)

Motion target of **10 mm** per axis, 10 valid samples out of 40 trials,
RMSE rejection threshold of 0.2 px.

### 3.1 Baseline

| Metric | X axis | Y axis |
|---|---|---|
| Mean travel of the motion axis | 10.0463 mm (std 0.0072) | -9.9450 mm (std 0.0108) |
| Mean error of the motion axis | **0.0463 mm** | **0.0550 mm** |
| Mean drift of the perpendicular axis | -0.0937 mm (std 0.0089) | -0.0898 mm (std 0.0054) |
| Mean reprojection RMSE | 0.1137 px (std 0.0178) | 0.1178 px (std 0.0190) |
| Rejected / failed samples | 16 of 40 | 28 of 40 |

**Baseline firmware recommendations:**

| | X axis | Y axis |
|---|---|---|
| Initial steps/mm | 80.0000 | 80.0000 |
| New steps/mm | **79.6314** (`M92 X79.63`) | **80.4425** (`M92 Y80.44`) |
| Backlash | 0.0124 mm (`M425 X0.0124`) | 0.0244 mm (`M425 Y0.0244`) |
| Skew | -0.009327 (-0.5344 degrees) | 0.009025 (0.5171 degrees) |

### 3.2 After calibration

Re-run with steps/mm X = 79.72 and Y = 80.40.

| Metric | X axis | Y axis |
|---|---|---|
| Mean travel of the motion axis | 10.0045 mm (std 0.0079) | -10.0022 mm (std 0.0071) |
| Mean error of the motion axis | **0.0071 mm** | **0.0054 mm** |
| Mean drift of the perpendicular axis | 0.0043 mm (std 0.0058) | 0.0036 mm (std 0.0053) |
| Mean reprojection RMSE | 0.1186 px (std 0.0151) | 0.1281 px (std 0.0168) |
| Rejected / failed samples | 9 of 40 | 10 of 40 |

**Follow-up recommendations (residual error):**

| | X axis | Y axis |
|---|---|---|
| Steps/mm at the time | 79.7200 | 80.4000 |
| New steps/mm | 79.6845 | 80.3826 |
| Backlash | 0.0068 mm | 0.0068 mm |
| Skew | 0.000427 -> already square, no compensation | 0.000362 -> already square |

### 3.3 Improvement baseline -> calibrated

| Metric | Baseline | After calibration | Improvement |
|---|---|---|---|
| X axis error | 0.0463 mm | 0.0071 mm | **84.7 %** |
| Y axis error | 0.0550 mm | 0.0054 mm | **90.2 %** |
| Y drift during X motion | 0.0937 mm | 0.0043 mm | **95.4 %** |
| X drift during Y motion | 0.0898 mm | 0.0036 mm | **96.0 %** |

---

## 4. Measurement error (previously named "systematic error")

> Author's statement: *"I calculated the measurement error by comparing
> my method's reading with a dial gauge. now in the folder it's written as systematic
> error. later you just rename the new one to measurement error. it has a calibration dataset
> and systematic error for each axis. the calibration dataset is like the dataset for
> calibrating the camera and the pure systematic error is the result of the machine
> movement from the calibration automation process but the travel distance is reduced to
> 0.5mm and all the parameters use baseline"*

**Purpose:** to validate the absolute accuracy of this method's reading by comparing it
against the **dial gauge** (reference measuring instrument).

**Configuration:** all baseline parameters (backlash comp 0, skew comp 0, steps/mm 80)
with the **travel distance reduced to 0.5 mm**.

**Consequence in the code:** this is why `otomasikalibrasi.py` modes `X+` and `Y+` use
`fwd_move = (0.5, 0.0)` / `(0.0, 0.5)`. When processing this dataset in the machine
calibration notebook, `EXPECTED_DELTA_X` / `EXPECTED_DELTA_Y` **must be changed to 0.5**, not 10.

**New naming:** `systematic_error_*` -> `measurement_error/*`.
`kalibrator_*` = camera calibration dataset for this session; `*_machine_movement` = the
machine movement result.

### 4.1 Comparison results with the dial gauge

Source of the numbers: `After Lulus Paper/code/plotmeasurement.py` (now moved to
`06_measurement_error/plot_measurement_error.py`, its data split into
`data/processed/measurement_error/dial_vs_ve.csv`).

Units are microns. The dial gauge was read constant across 5 iterations, with an instrument accuracy of **±10 µm**.

| Panel | Dial gauge | Virtual Encoder (5 iterations) | MAE | std |
|---|---|---|---|---|
| X Forward | 505.0 | 504.9 / 507.0 / 494.7 / 497.0 / 502.3 | 4.62 | 4.32 |
| Y Forward | 480.0 | 480.1 / 481.6 / 498.6 / 489.4 / 493.0 | 8.54 | 7.77 |
| X Backward | 10.0 | 11.2 / 5.1 / 16.8 / 17.8 / 15.8 | 5.30 | 2.54 |
| Y Backward | 20.0 | 4.9 / 23.0 / 24.7 / 11.5 / 15.9 | 7.08 | 4.94 |
| **Combined X** | | (10 measurements) | **4.96** | 3.36 |
| **Combined Y** | | (10 measurements) | **7.81** | 6.18 |

MAE = mean |VE - dial|, the same as the "Mean Diff" label in the manuscript figure legend.
The 5-8 µm difference is within the dial gauge resolution (±10 µm), so this method is consistent
with the reference measuring instrument.

### 4.2 Related files

| File | Contents |
|---|---|
| `data/processed/measurement_error/dial_vs_ve.csv` | 20 rows: axis, frame, iteration, dial_um, dial_err_um, ve_um, abs_diff_um |
| `data/raw/measurement_error/x_dial_gauge/` | 15 dial gauge photos of the X axis (`orix/fwd/bck` 1-5) + 3 visualization images |
| `data/raw/measurement_error/y_dial_gauge/` | 15 dial gauge photos of the Y axis (`oriy/fwd/bck` 1-5) + 3 visualization images |
| `figures/paper/1_4_position_comparison_combined.png` | manuscript figure, 4 panels |

---

## 5. Provenance of the calibration values — ANSWERED: these are the result of *fine-tuning*, not a copy error

**The question that was previously open:** the values used in the code (79.72 / 80.40 / 0.0133 /
0.009213) are not the same as those recommended by the baseline log (79.6314 / 80.4425 /
0.0124 / 0.009025). Which is correct?

**Answer:** both are correct and genuinely different. The baseline log records the **baseline
values as well as the first round's recommendation**, whereas the code contains the **final
values after fine-tuning**. The manuscript **deliberately presents only those two points**
(baseline and final); the chain of iterations in between is not included in the manuscript —
so nothing is missing from the manuscript, and nothing is wrong in the code.

The authoritative source is in the manuscript: Table *"Fine Tuning Calibration Result Parameters"*
(`tab:parameter_final_kalibrasi`, `mainmatter/bab4.tex` lines 695-716):

| Parameter | Final value (manuscript) | Equivalent in code |
|---|---|---|
| `STEPX` | 79,72 steps/mm | `STEPX = 79.72` |
| `STEPY` | 80,40 steps/mm | `STEPY = 80.40` |
| `BACKLASH_X` | 13,3 µm | `BACKLASH_X = 0.0133` mm |
| `BACKLASH_Y` | 31,4 µm | `BACKLASH_Y = 0.0244 + 0.0070` = 0.0314 mm |
| `SKEW_X_ON_Y` | -9,2 µm/mm | `SKEW_X_ON_Y = -0.009200` |
| `SKEW_Y_ON_X` | 9,213 µm/mm | `SKEW_Y_ON_X = 0.009213` |

The manuscript (bab4.tex line 693) explains the stages: after steps/mm and backlash
are applied, **fine-tuning** is performed by repeatedly updating the parameters based on
the recommendation equations until the machine reaches *steady-state*.

### 5.1 Working artifacts from the fine-tuning iterations in the ARCHIVE (outside the manuscript, explanatory only)

The intermediate iterations are not shown in the manuscript, but the **datasets still exist** in
`SEMPRO/Code/ARSIP` (dated 5 May 2026). This is what explains the origin of the final numbers
79.72 / 80.40 — not guesses, but the trace of runs that were actually performed:

| ARCHIVE folder | Files | Implies |
|---|---|---|
| `kalibrasi_x_step80.11_skew0_5_may_2026` | 87 | steps 80.11, skew 0 |
| `kalibrasi_x_step80.11_skew+0.0128_5_may_2026` | 93 | steps 80.11, skew +0.0128 |
| `kalibrasi_x_step80.11_skew-0.0123_...`, `skew-0.0128_...` | — | steps 80.11, negative skew |
| `kalibrasi_x_stepdoang_8013_5_may_2026` | 61 | test of steps 80.13 only |
| `kalibrasi_x_skewfactorx2_5_may_2026` | 60 | test of skew factor 2x |
| `dataset_setelah_kalibrasi_step_x_1`, `_x_2`, `_y_1`..`_y_4` | — | steps iterations per axis |
| `KALIBRASI_X_STEPBACK_1_FIX_METHOD`, `STEPBACK_2_FIX_METHOD` | 120 | *stepback* iterations |
| `KALIBRASI_X_SKEW_1_FIX`, `SKEW_2_FIX`, `KALIBRASI_Y_SKEW_1_FIX` | 120 | skew iterations |
| `dataset_jalur_setelah_kalibrasi_step_backlash_skew_feedrate_{500,1000,2000,3000}` | — | feedrate test |
| `X_LAST_FIX/KALIBRASI_X_FINETUNING/kalibrasi` | 120 | last fine-tuning data |

### 5.2 Why this still needs to be recorded in the repo

Someone who derives the calibration themselves from the **stored baseline dataset** will
get **79.6314**, not 79.72. That is **not** an error: 79.6314 is the first
round's recommendation, whereas 79.72 is the final result after several rounds of fine-tuning.
This repo uses 79.72 / 80.40 because that is what produces the numbers in the manuscript
(proven: the `calibrated` mode reproduces the log identically).

The full chain: `80.00` (baseline) -> 79.6314 (round 1 recommendation, stored log)
-> iterations in the ARCHIVE (80.13 / 80.11 / skew variants; **not in the manuscript**) -> **79.72**
(final, manuscript + code). The manuscript shows only the endpoints, and that is enough
for the manuscript; this note exists solely so readers of the repo don't think 79.6314 is wrong.

## 6. What is not yet in the repo

The intrinsic matrix `K` and distortion coefficients `D` have never been saved as a file —
only printed on screen. The split notebook
(`01_camera_calibration/camera_calibration.ipynb`) now exports them to
`output/camera_params.npz` so they can be referenced and used by the machine calibration notebook.

## 6. Data-consistency verification (carried out while preparing this repo)

Everything below was checked by **re-running the code**, not by reading the documentation.

### 6.1 Machine calibration — the repo reproduces the manuscript numbers

| Quantity | Log / manuscript | Re-run from this repo |
|---|---|---|
| X travel, error | 10.0045 mm, 0.0071 mm | identical |
| X steps/mm recommendation | `M92 X79.68` | identical |
| Y travel, error | −10.0022 mm, 0.0054 mm | identical |
| Y steps/mm recommendation | `M92 Y80.38` | identical |

### 6.2 Trajectory evaluation — the repo reproduces the manuscript numbers

Re-running the evaluation gives RMSE total 100.89 um (baseline) -> 46.17 um (calibrated), i.e. a
54.24 % improvement, matching `tab:perbandingan_evaluasi_rmse` (100.9 um -> 46.17 um).

### 6.3 The paper figures are built from the manuscript tables

The data arrays hard-coded in `07_paper_figures/plot_axis_iterations.py` reproduce the thesis
tables exactly (`bab4.tex` lines 585-597 baseline, 809-820 calibrated), and so does
`plot_trajectory_rmse.py`. `plot_environmental_noise.py` was audited by re-deriving its values
from the raw stills with `07_paper_figures/verify_environmental_noise.py`: all 10 pairs match to
0.00 um.

### 6.4 KNOWN INCONSISTENCY: on axis X the noise figure and the noise table disagree

Both come from the same 10 deltas, but they use two different definitions:

| Quantity | Manuscript table + prose (`tab:statistik_noise_lingkungan`) | Paper figure (`environmental_noise_with_std`) |
|---|---|---|
| X | 1.6 um (SD 2.5) | MAE 2.58 um (SD 1.49) |
| Y | 4.9 um (SD 3.3) | MAE 4.97 um (SD 3.40) |

Cause: the manuscript value is the magnitude of the mean of the **signed** deltas
(|mean(delta)| = 1.57 um on X) with the **population** standard deviation (ddof = 0) — exactly
what the notebook's `FIND NOISE` cell prints. The figure instead draws the mean of the
**absolute** deltas (mean(|delta|) = 2.58 um on X) with the sample standard deviation.
On axis Y every delta is negative, so the two definitions nearly coincide (4.94 vs 4.96 um);
on axis X the signs are mixed, so they differ by about 1 um (65 %).

Two further notes on the same experiment:

- The table column is labelled "mean absolute error", but what was computed is the magnitude of
  a signed mean — so the label does not describe the number.
- The figure's 10 points come from **9 distinct stills**, because `calib_0019.png` appears twice
  in the pair list of the original cell (pairs 2 and 9). This is why elements 2 and 9 of both
  plotted arrays are identical.

Nothing was changed inside `plot_environmental_noise.py`: the figure still shows exactly what was
plotted for the manuscript. Table and figure need to be brought into agreement by the author —
either report mean(|delta|) in the table, or relabel the table column and update the figure.
