# DATA MANIFEST

Dataset mapping: original name (in `After Lulus Paper/Data/`) -> name in this repo.
All image/video datasets **are not tracked in git** (see `.gitignore`); only the processed
CSVs in `data/processed/` are tracked in git.

## 1. Camera calibration

| Name in repo | Original name | Contents | Size | Git |
|---|---|---|---|---|
| `camera_calibration/dataset_kalibrasi_fix_prime_260/` | `dataset_kalibrasi_fix_prime_260` | 10 `calib_XXXX.png` images + black margin | small | yes |
| `camera_calibration/dataset_kalibrasi_ditambah/` | `dataset_kalibrasi_ditambah` | 97 `oriy/fwd/bck` images | ~20 MB | no |

> Note: the folder name `fix_prime_260` implies 260 images, but it only contains 10.
> Needs confirmation whether this is the dataset that produces the numbers in the manuscript.

## 2. Linear testing (machine calibration) - CONFIRMED by the author

| Name in repo | Original name | Axis | Condition | Files | Size | Git |
|---|---|---|---|---|---|---|
| `linear_baseline_x/` | `BASELINE_X_INDIVIDUAL` | X | baseline | 120 | 22 MB | no |
| `linear_baseline_y/` | `BASELINE_Y_FIX_METHOD` | Y | baseline | 120 | 22 MB | no |
| `linear_calibrated_x/` | `X_LAST_FIX` | X | after calibration | 120 | 22 MB | no |
| `linear_calibrated_y/` | `Y_LAST_FIX` | Y | after calibration | 120 | 21 MB | no |

Each folder contains 40 triplets: `oriy{i}.png`, `fwd{i}.png`, `bck{i}.png` (i = 1..40),
matching `FILE_INDICES = list(range(1, 41))` in the machine calibration notebook.

## 3. Measurement error (previously "systematic error") - RENAME APPROVED by the author

Used to compare this method's reading with a **dial gauge**.
Configuration: all baseline parameters (backlash comp 0, skew comp 0, steps/mm 80),
and the **travel distance reduced to 0.5 mm** (not 10 mm).

| Name in repo | Original name | Contents | Files | Size | Git |
|---|---|---|---|---|---|
| `measurement_error/x_camera_calibration/` | `kalibrator_systematic_error_x` | camera calibration dataset for this session | 54 | 11 MB | no |
| `measurement_error/x_machine_movement/` | `systematic_error_x` | machine movement result for the X axis | 120 | 24 MB | no |
| `measurement_error/y_camera_calibration/` | `kalibrator_systematic_y` | camera calibration dataset for this session | 31 | 5.4 MB | no |
| `measurement_error/y_machine_movement/` | `systematic_error_Y` | machine movement result for the Y axis | 120 | 21 MB | no |
| `measurement_error/x_dial_gauge/` | `Semester 8/.../images/Hasil/Kalibrator_x` | 15 dial gauge photos of the X axis (`orix/fwd/bck` 1-5) + 3 visualization images | 18 | small | no |
| `measurement_error/y_dial_gauge/` | `Semester 8/.../images/Hasil/Kalibrator_y` | 15 dial gauge photos of the Y axis (`oriy/fwd/bck` 1-5) + 3 visualization images | 18 | small | no |

> What produced this dataset: `otomasikalibrasi.py` with `TEST_MODE = 'X+'` / `'Y+'`,
> where `fwd_move = (0.5, 0.0)` / `(0.0, 0.5)` — this is the evidence of the 0.5 mm distance in the code.
> To process it in the machine calibration notebook, select `KALIBRASI_MODE=measurement_error`
> (automatically uses a 0.5 mm target and baseline steps/mm).
>
> `*_camera_calibration/` comes from `otomasikalibrasi.py`; `*_dial_gauge/` are PHOTOS
> of the dial gauge used to compute the measurement error. The comparison result numbers
> are in `data/processed/measurement_error/dial_vs_ve.csv`.

### 3.1 Environmental noise (static capture) - RECOVERED from the working archive

The machine was **not commanded to move**: 24 stills (`calib_0000.png` .. `calib_0023.png`) were
taken at one fixed position and processed with the same detection code as the linear test. With
zero commanded travel, whatever delta remains is environmental noise. The paper figure
`figures/paper/environmental_noise_with_std.png` uses 10 of these 24 stills.

| Name in repo | Original name | Contents | Files | Size | Git |
|---|---|---|---|---|---|
| `noise_static_capture/` | `SEMPRO/Code/ARSIP/pengujian_noise_fix_banget/kalibrasi` | static-capture stills `calib_0000.png`..`calib_0023.png` (**photos only, no video** - the `video/` subfolder is empty by design) | 24 | 4.2 MB | no |

> This dataset existed only inside the working archive `SEMPRO/Code/ARSIP/`; it was copied into
> `data/raw/noise_static_capture/` so that it is not lost.
> `07_paper_figures/verify_environmental_noise.py` reproduces the figure values from it (all 10
> pairs match to 0.00 um). The pair list uses `calib_0019.png` twice, so the figure's 10 points
> come from 9 distinct stills - see `docs/03_results_and_data_locations.md` section 6.4.


## 4. Ellipse path (circular)

| Name in repo | Original name | Contents | Size | Git |
|---|---|---|---|---|
| `circular_baseline/` | `Circular Baseline` | `hasil_fix_banget_baseline_XX.csv` + PNG | 4.1 MB | CSV yes, PNG no |
| `circular_calibrated/` | `Circular Kalibrasi` | `JALUR_VIDEO_FINAL_3_XX.csv` + PNG | 8.2 MB | CSV yes, PNG no |

The raw videos (not tracked in git), according to the research owner's explanation:

| Folder in repo | Original name | Contents | Files | Size |
|---|---|---|---|---|
| `video_baseline_x/` | `BASELINE_JALUR_FINAL_VIDEO` | test video of the **circular baseline** | 21 | 970 MB |
| `video_calibrated_x/` | `KALIBRASI_JALUR_FINAL_VIDEO_3` | test video of the **calibrated circular** result | 11 | 547 MB |
| `video_kalibrasi_x/` | `KALIBRASI_X_VIDEO_BENERAN` | X-axis video (manuscript figure) | 3 | 100 MB |
| `video_baseline_y/` | `BASELINE_Y_VIDEO_FINAL_BGT_BGT` | baseline Y-axis video | 1 | 34 MB |
| `video_calibrated_y/` | `KALIBRASI_Y_VIDEO_FINAL_BGT_BGT` | calibrated Y-axis video | 1 | 38 MB |

Total 37 files / 1.7 GB. **No need to reprocess** to reproduce the research
results — the path CSVs already exist in `circular_baseline/` and `circular_calibrated/`.
(`HASIL_PENGUJIAN_LINTASAN` is not copied because its contents are evaluation images, not videos.)

## 5. Processed outputs (tracked in git)

| File | Contents | Size |
|---|---|---|
| `processed/camera_calibration/camera_matrix.csv` | 3x3 intrinsic matrix K | small |
| `processed/camera_calibration/dist_coeffs.csv` | 1x5 distortion coefficients | small |
| `processed/camera_calibration/camera_params.csv` | parameter/value table + image size | small |
| `processed/camera_calibration/reprojection_rmse.csv` | reprojection RMSE per image | small |
| `processed/virtual_encoder/*.csv` | path CSVs for the manuscript figures | small |
| `processed/measurement_error/dial_vs_ve.csv` | 20 rows comparing dial gauge vs VE | small |

## 6. Duplicates in `SEMPRO/Code/`

The folders `systematic_error_x`, `systematic_error_Y`, `kalibrator_systematic_error_x`,
`kalibrator_systematic_y`, `X_LAST_FIX`, `Y_LAST_FIX`, `X_LAST`, `Y_LAST`,
`BASELINE_X_FIX_METHOD`, `BASELINE_Y_FIX_METHOD`, `KALIBRASI_X_SKEW_1_FIX`,
`KALIBRASI_X_STEPBACK_1_FIX_METHOD`, `KALIBRASI_Y_STEPBACK_1_FIX_METHOD` all
have copies in `After Lulus Paper/Data/`. **Final reference = `After Lulus Paper/Data/`**;
the ones in `Code/` are considered working archives.

---

## 7. Raw data download (for handoff)

The git repo deliberately does **not** include the large raw data.

**Google Drive link:** https://drive.google.com/drive/folders/1-t_4XDX1aLUvNeTrkfXd1f1-iWcVR9tP?usp=sharing

(a folder named `raw`, containing the entire contents of `data/raw/`). Download it, then place the contents according to
the "name in repo" column above.

| Package | Contents | Size | Link |
|---|---|---|---|
| Path videos | 5 `video_*` folders (37 files) | 1.7 GB | [https://drive.google.com/drive/folders/1-t_4XDX1aLUvNeTrkfXd1f1-iWcVR9tP?usp=sharing](https://drive.google.com/drive/folders/1-t_4XDX1aLUvNeTrkfXd1f1-iWcVR9tP?usp=sharing) |
| Images + raw CSV | `camera_calibration/`, `linear_*`, `measurement_error/`, `noise_static_capture/` (24 stills), `circular_*` | 187 MB | included in the Drive folder above |

**How to use:** download, extract, then place the contents **directly inside** `data/raw/`
so that the structure becomes `data/raw/linear_baseline_x/...`,
`data/raw/video_baseline_x/...`, and so on. Verify with:

```bash
python config_paths.py
```

All lines must have the status `OK`. If any is `NOT FOUND`, its location will be
shown in the last column.

**Check the completeness of the video package** (so that no file is left behind when uploading):

| Folder | Original name | Must contain |
|---|---|---|
| `video_baseline_x/` | `BASELINE_JALUR_FINAL_VIDEO` | 21 files `pose_video_01..21.avi` |
| `video_calibrated_x/` | `KALIBRASI_JALUR_FINAL_VIDEO_3` | 11 files (`pose_video_01..10.avi` + `pose_video_01 - KALIBRASI.avi`) |
| `video_kalibrasi_x/` | `KALIBRASI_X_VIDEO_BENERAN` | 3 files |
| `video_baseline_y/` | `BASELINE_Y_VIDEO_FINAL_BGT_BGT` | 1 file |
| `video_calibrated_y/` | `KALIBRASI_Y_VIDEO_FINAL_BGT_BGT` | 1 file |
