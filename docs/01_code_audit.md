# Code Audit & Cleanup Plan

Source: `Semester 7/SEMPRO/Code/kalibrasicamera` (+ a few .py files in `Code/`).
Audit date: 12 October 2026.

## 1. Notebooks Used (final)

| Source file | Size | Cell count | Note |
|---|---|---|---|
| `kalibrasicamera/kalibrasisesuaipaper.ipynb` | 3.4 MB | 12 | Paper-aligned pipeline implementation + X & Y firmware recommendations |
| `kalibrasicamera/virtualencodervideo.ipynb` | 766 KB | 12 | Camera calibration (duplicate) + virtual encoder & plots |
| `kalibrasicamera/evaluasilintasan.ipynb` | 40 KB | 5 | Ellipse ground truth + RMSE baseline vs calibrated |

### Other notebooks in the `Code/` folder (not core, but related)

- `KALIBRASI_SESUAI_PAPER_DAN_VIRTUALENCODER_FOTO.ipynb` — photo-based version (not video)
- `VIRTUALENCODER_VIDEOPROCESSING.ipynb` — an earlier version of the video virtual encoder
- `virtualencodervideo copy.ipynb`, `copy 2/3/4.ipynb` — experiment copies
- `tulispaper_kalibrasi.ipynb` — manuscript-writing notebook
- `animasiplot.ipynb`, `datalintasan.ipynb`, `regresibaseline.ipynb`, `debuggingcirle.ipynb`, `CLAHEdanGAUSSIANBLUR.IPYNB`
- Utility scripts: `virtualencoder.py`, `otomasikalibrasi.py`, `otomasilintasan.py`,
  `capturedatasetbiasa.py`, `capturedatasetpengujianfoto.py`, `linescreeningparameter.py`,
  `distorsikamera.py`, `distorsikameravisualisasisim.py`, `cekfps.py`, `plotpergerakancapturedata.py`,
  `alasantetatidaksimetris.py`, `Chessboard_generator.py`, `jalaninrepetierhost.py`

Decision to make: which ones go into the public repo, which are archived.

## 2. Issues Found

### 2.1 Hardcoded absolute paths (biggest blocker)
Every notebook uses the path `C:\Users\zaydz\Documents\Onedrive Kuliah\...` literally,
at least at the following points:

- `FOLDER_PATH` calibration dataset
- `base_path` of the `X_LAST_FIX` / `Y_LAST_FIX` dataset (oriy/fwd/bck triplet)
- `base_path` noise search
- `VIDEO_PATH` (`KALIBRASI_X_VIDEO_BENERAN\video\pose_video_XX.avi`)
- `filename_csv` in the evaluation notebook (`DATA FIX\hasil_fix_banget_baseline_XX.csv`, `JALUR_VIDEO_FINAL_3_XX.csv`)
- `output_plot_name` (`HASIL_KALIBRASI_JALUR_FIX_EVALUASI`, `HASIL_PENGUJIAN_LINTASAN` folders)
- `TARGET_FOLDER` in `cek_frame_folder`

**Fix:** move them into a single configuration cell (`PROJECT_ROOT`, `DATA_DIR`, `OUTPUT_DIR`)
or a `config.py`/`.env` file, then document the expected folder structure in the README.

### 2.2 Duplicated code blocks
- The camera-calibration cells (0-5) in `kalibrasisesuaipaper.ipynb` are **exactly the same** as
  cells 0-5 in `virtualencodervideo.ipynb`.
- `calibrateCamera` + the RMSE computation are also written twice (cell 5 and the comment "Cell 7").
- Cells 8 and 9 in notebook 1 are nearly identical (X vs Y), differing only in target, steps/mm,
  `base_path`, and the visualization file name.
- Notebook 3: cells 0 and 1 are nearly identical (baseline vs calibration), cell 4 merges the two.

**Fix:** turn them into a single `src/` module (e.g. `pipeline.py`: `detect_corners`, `calibrate_camera`,
`pose_from_image`, `evaluate_path`), then have the notebooks just import it. This also directly
answers the "clean code" requirement for the GitHub repo.

### 2.3 Bloated notebook output
`kalibrasisesuaipaper.ipynb` is 3.4 MB because images are stored in the cell outputs.
For the repo, run **Clear All Outputs** before committing, and save execution-output images
only to `figures/`.

### 2.4 Dead lines / duplicate comments
- The `cv2.putText` block from the "font too small" version still exists as a long comment
  in cell 8 of notebook 1.
- `FILE_INDICES = [1,2,3,4,5,6,7,8,9,10]` is immediately overwritten by `FILE_INDICES = [1,2,3]`
  in cell 6 of notebook 2 (the effective value is only 3 videos).
- `sample_idx = 0 if len(image_files) > 7 else 0` (both branches give the same value).
- Bare `try/except` (`except:`) in `intersect_lines` and `optimize_subpixel_gradient`.

### 2.5 Undocumented dependencies
Required: `opencv-contrib-python` (for `cv2.ximgproc`), `numpy`, `scipy`, `pandas`, `matplotlib`.
There is no `requirements.txt` yet. The OpenCV version also affects detection stability,
so it should be pinned in requirements.

### 2.6 No standard repo files yet
There is no `LICENSE`, `.gitignore`, or README yet. Animated `.gif` files of 15-23 MB
should **not** be committed to git (or should go through Git LFS), because they bloat the history.

## 3. Proposed Work Order

1. Copy the 3 final notebooks + the small CSVs into this folder structure (without the large datasets).
2. Extract the repeated blocks into `src/` (`pipeline.py`, `evaluate.py`, `plot.py`).
3. Replace all absolute paths with relative configuration + `config.py`.
4. Remove dead lines, replace the bare `except:` with explicit handling.
5. Clear notebook outputs, save images to `figures/`.
6. Add `requirements.txt`, `LICENSE`, `.gitignore`, and update the README with the final numbers
   (camera-calibration RMSE, trajectory RMSE baseline vs calibrated, percentage improvement).
7. Decide which files in `Code/` go into the repo and which go to `archive/` or `.gitignore`.
8. `git init` in this folder (not inside the old OneDrive), commit, then push to GitHub.

## 4. What Still Needs Filling In (not yet in the code)

Several final numbers are not written in the code (they only appear as print output
when run): the K and D values, the overall reprojection RMSE, the per-trial trajectory RMSE,
and the percentage improvement. These numbers need to be taken from the manuscript or by
re-running the notebooks with the dataset, so that they can be shown in the repo README.
