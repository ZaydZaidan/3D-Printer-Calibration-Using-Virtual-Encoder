# Role of Each File — Confirmation Results

Filled in gradually as the author pointed out which files are actually used.
Status: **confirmed** = stated directly by the author; **suspected** = inferred from the
code contents/dataset names; **pending** = awaiting identification.

---

## 1. `capturedatasetbiasa.py` — CONFIRMED

**Role:** only for **capturing the chessboard photo dataset** as material for camera calibration.
Goal: to obtain the **camera intrinsic matrix and distortion coefficients** (camera profiling).

Author's statement:

> "Back then I used the one called capturedatasetbiasa to capture the chessboard dataset images
> for camera calibration. I only used the f key to capture photos."

| Key | Function in code | Used? |
|---|---|---|
| `f` | Save to `dataset_sesi_<timestamp>/kalibrasi/calib_XXXX.png` | **YES** |
| `g` | Record video `pose_video_XX.avi` | **NO** |
| `q` | Quit | yes |

Consequence: all the video logic in this file (`vid_counter`, `VideoWriter`) is irrelevant.
The video dataset comes from `otomasilintasan.py` — see section 3.

Usage chain:

```
capturedatasetbiasa.py (f key)             -> calib_XXXX.png
        v
camera_calibration.ipynb (formerly kalibrasisesuaipaper.ipynb cells 0-5)
        -> K (intrinsic) + D (distortion) + reprojection RMSE
        v
reused by the virtual encoder for per-frame solvePnP
```

## 2. `otomasikalibrasi.py` — CONFIRMED

**Role:** captures the **linear test** dataset for machine calibration. Run **twice**:

| Run | Parameters | Resulting dataset | Processing notebook |
|---|---|---|---|
| Baseline | backlash 0, skew 0, steps/mm 80 (X and Y) | `BASELINE_X_INDIVIDUAL` (X), `BASELINE_Y_FIX_METHOD` (Y) | `machine_calibration.ipynb` X / Y cells |
| After calibration | steps/mm 79.72 (X) / 80.40 (Y) | `X_LAST_FIX` (X), `Y_LAST_FIX` (Y) | same, change `base_path` + `CURRENT_STEPS_MM` |
| Measurement error | all baseline, **0.5 mm travel distance** | `systematic_error_x`, `systematic_error_Y` | compare with the dial gauge |

The parameter values are read directly in the code, lines 10-26:
the commented-out block (lines 10-17) holds the **calibration-result** values, the active block
(lines 19-26) holds the **baseline** values.

`fwd_move` per mode determines the travel distance:
`X+`/`Y+` = **0.5 mm** (used for the measurement error),
`X-`/`Y-` = 10 mm (normal linear test, and the value that matches
`EXPECTED_DELTA = 10` in the notebook).

**Output:** `dataset_<Xpos|Xneg|Ypos|Yneg>_sesi_<timestamp>/kalibrasi/`
containing `oriy{i}.png`, `fwd{i}.png`, `bck{i}.png` (i = 1..40).

## 3. `otomasilintasan.py` — CONFIRMED

**Role:** runs the **elliptical trajectory** on the machine while recording video, used twice
(baseline parameters, then the calibration-result parameters).

- The calibration parameters are on lines 15-21 (`BACKLASH_X`, `BACKLASH_Y`, `SKEW_X_ON_Y`,
  `SKEW_Y_ON_X`, `STEPX`, `STEPY`) — these are the values fed in from the
  `machine_calibration.ipynb` recommendation.
- `TOTAL_ITERASI = 10` -> 10 videos per session.
- `precompute_ellipse_commands()` generates the ellipse gcode (see section 5).
- In `cnc_worker_thread`, line 235, the `STEPX`/`STEPY` values are sent as `M92`.
- **Output:** `dataset_otomatis_sesi_<timestamp>/video/pose_video_XX.avi`
  (the `dataset_otomatis_sesi_` prefix is this file's marker, distinguishing it from the other capture file).

> Note: this file stores only the **calibration-result** configuration. The baseline
> configuration is not stored in the code, only recorded in its dataset.

## 4. `virtualencodervideo copy 2.ipynb` — CONFIRMED (a link in the chain that was initially missed)

**Role:** converts the **calibration-result** trajectory video into a trajectory CSV.
Not merely an experiment copy — it is part of the final chain.

- Cell 6: `VIDEO_PATH = ...\KALIBRASI_JALUR_FINAL_VIDEO_3\video\pose_video_XX.avi`
- `CSV_OUTPUT_PATH = f"JALUR_VIDEO_FINAL_3_{video_index:02d}.csv"` -> read by
  `evaluasilintasan.ipynb`.

Full chain:

```
otomasilintasan.py -> KALIBRASI_JALUR_FINAL_VIDEO_3/video/pose_video_XX.avi
        v
virtualencodervideo copy 2.ipynb (cell 6)
        -> JALUR_VIDEO_FINAL_3_XX.csv
        v
evaluasilintasan.ipynb (cells 1 & 4)
```

For the baseline, the same path ends at `hasil_fix_banget_baseline_XX.csv`
(source: `BASELINE_JALUR_FINAL_VIDEO`), but **no notebook in the folder writes
that file name** — possibly the result of a manual rename. Needs confirmation.

## 5. Conceptual note: on "extrinsics"

In this pipeline there is **no single fixed extrinsic matrix** (camera -> machine transform):

- `cv2.calibrateCamera()` returns `rvecs`/`tvecs`, which are the **board pose relative to the
  camera for each calibration image** (used to compute the RMSE), not a fixed transform.
- Machine calibration and the virtual encoder recompute the pose **per image/frame** with
  `cv2.solvePnP`. The trajectory is obtained from the **difference** of each `tvec` against the
  `tvec` of the origin frame.

A safe sentence for the manuscript/repo: camera calibration yields the **intrinsics (K) and
distortion coefficients (D)**; the position is obtained **per frame** through `solvePnP` and
expressed **relative** to the initial frame.

## 6. Anomalies & open questions

1. `dataset_kalibrasi_fix_prime_260` contains only **10 images** even though its name implies 260,
   yet the notebook uses it as `FOLDER_PATH`.
2. `dataset_kalibrasi_ditambah` (97 files, `oriy/fwd/bck` pattern) — which part uses it?
   Candidates: `PLOT_GABUNGAN_X_DITAMBAHDATASET.png`, `JALUR_DATASET_DITAMBAH_01.csv`.
3. Inconsistent FPS in `capturedatasetbiasa.py`: line 29 requests 60 FPS, line 109's
   `VideoWriter` uses 120.0 FPS. No impact (the `g` key is unused) but it should be fixed
   before release.
4. The on-screen overlay in both capture scripts writes `"REC 120FPS"` as a hardcoded string.

## 7. Status of all files

| # | File | Status | Role |
|---|---|---|---|
| 17 | `capturedatasetbiasa.py` | confirmed | Chessboard image acquisition for camera calibration (`f` key) |
| 16 | `otomasikalibrasi.py` | confirmed | Linear test dataset acquisition (baseline / after calibration / measurement error) |
| 15 | `otomasilintasan.py` | confirmed | Run the elliptical trajectory + record video; baseline and calibrated parameters |
| 9 | `kalibrasicamera\virtualencodervideo copy 2.ipynb` | confirmed | Calibrated trajectory video -> `JALUR_VIDEO_FINAL_3_XX.csv` |
| 1 | `kalibrasicamera\kalibrasisesuaipaper.ipynb` | confirmed | Split into `camera_calibration.ipynb` + `machine_calibration.ipynb` |
| 2 | `kalibrasicamera\virtualencodervideo.ipynb` | confirmed | Virtual encoder (video -> trajectory) |
| 11 | `kalibrasicamera\evaluasilintasan.ipynb` | confirmed | Trajectory RMSE evaluation vs ground truth |
| 18 | `capturedatasetpengujianfoto.py` | not used (suspected) | `oriy/fwd/bck` triplet acquisition; but the author cites `otomasikalibrasi.py` as the one used |
| — | `After Lulus Paper/code/plotmeasurement.py` | confirmed | Dial gauge vs virtual encoder comparison (measurement error). Moved to `06_measurement_error/plot_measurement_error.py` |
| — | `After Lulus Paper/code/plotdatabaselinedankalibrasi.py` | confirmed | Per-iteration X/Y MAE figures. Copied to `07_paper_figures/plot_axis_iterations.py`; its 12 data arrays match the thesis tables exactly |
| — | `After Lulus Paper/code/plotdatabaselinedankalibrasitrajektori.py` | confirmed | Trajectory RMSE figures. Copied to `07_paper_figures/plot_trajectory_rmse.py`; its 9 data arrays match the thesis tables exactly |
| — | `After Lulus Paper/code/plotnoiselingkungan.py` | confirmed | Environmental noise figure. Copied to `07_paper_figures/plot_environmental_noise.py`; values re-derived from the raw stills (`07_paper_figures/verify_environmental_noise.py`) |
| — | `Semester 8/.../images/Hasil/Kalibrator_x`, `Kalibrator_y` | confirmed | 15 dial gauge photos per axis (5 `ori/fwd/bck` triplets) for the measurement error experiment |
| — | 22 other files | pending | Awaiting author identification |

## 8. Note: two trajectory-CSV paths from one script

The **calibrated** side (`JALUR_VIDEO_FINAL_3_XX.csv`) is clearly produced by
`virtualencodervideo copy 2.ipynb` cell 6. The **baseline** side
(`hasil_fix_banget_baseline_XX.csv`), according to the research owner, is produced by the
**same code**, differing only in the input video and the output CSV path.

A search across all notebooks in `SEMPRO/Code/` confirms that no other notebook
**writes** the name `hasil_fix_banget_baseline_*` — they all only read it.
So that explanation is consistent with the code; the only thing not saved is the version
of the script with the modified output path.

In this repo the two are unified through `config_paths.py`: `KALIBRASI_VIDEO`
(video folder) + `KALIBRASI_CSV_PREFIX` (output CSV file name).
