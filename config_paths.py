"""Centralized path configuration for all research notebooks.

HOW TO USE
----------
Notebooks load this file automatically. Check your data status with:

    python config_paths.py

If anything shows "NOT FOUND", place the dataset at the location shown, or
edit one of the lines below (the LEGACY_PATHS / DATA_DIR section).

EXPECTED STRUCTURE
------------------------
This repo:
    <repo>/data/raw/<logical_dataset_name>/...

Original research structure (used as an automatic fallback, see LEGACY_PATHS):
    C:\\Users\\<user>\\Documents\\Onedrive Kuliah\\Kuliah\\After Lulus Paper\\Data\\...
    C:\\Users\\<user>\\Documents\\Onedrive Kuliah\\Kuliah\\Semester 7\\SEMPRO\\Code\\...

The data folder can be moved anywhere as long as `resolve()` is pointed correctly.
"""

from __future__ import annotations

import glob
import os

# ==========================================================================
# 1. REPO LOCATION
# ==========================================================================
def _find_repo_root(start: str) -> str:
    p = os.path.abspath(start)
    for _ in range(8):
        if os.path.isfile(os.path.join(p, "config_paths.py")):
            return p
        parent = os.path.dirname(p)
        if parent == p:
            break
        p = parent
    return os.path.abspath(start)


REPO_ROOT = os.environ.get("KALIBRASI_REPO", _find_repo_root(os.getcwd()))
DATA_DIR = os.environ.get("KALIBRASI_DATA", os.path.join(REPO_ROOT, "data", "raw"))
OUTPUT_DIR = os.environ.get("KALIBRASI_OUTPUT", os.path.join(REPO_ROOT, "data", "processed"))

# ==========================================================================
# 2. LEGACY PATHS (automatic fallback when data has not been moved to data/raw)
#    Remove this section once all data has been moved to data/raw/.
# ==========================================================================
_ONEDRIVE = r"C:\Users\zaydz\Documents\Onedrive Kuliah\Kuliah"
LEGACY_DATA_DIR = os.path.join(_ONEDRIVE, "After Lulus Paper", "Data")
LEGACY_CODE_DIR = os.path.join(_ONEDRIVE, "Semester 7", "SEMPRO", "Code")

LEGACY_PATHS = {
    "camera_calibration/dataset_kalibrasi_fix_prime_260":
        os.path.join(LEGACY_CODE_DIR, "dataset_kalibrasi_fix_prime_260"),
    "camera_calibration/dataset_kalibrasi_ditambah":
        os.path.join(LEGACY_CODE_DIR, "dataset_kalibrasi_ditambah"),

    "linear_baseline_x":     os.path.join(LEGACY_DATA_DIR, "BASELINE_X_INDIVIDUAL"),
    "linear_baseline_y":     os.path.join(LEGACY_DATA_DIR, "BASELINE_Y_FIX_METHOD"),
    "linear_calibrated_x":   os.path.join(LEGACY_DATA_DIR, "X_LAST_FIX"),
    "linear_calibrated_y":   os.path.join(LEGACY_DATA_DIR, "Y_LAST_FIX"),

    "measurement_error/x_machine_movement":
        os.path.join(LEGACY_DATA_DIR, "systematic_error_x"),
    "measurement_error/y_machine_movement":
        os.path.join(LEGACY_DATA_DIR, "systematic_error_Y"),
    "measurement_error/x_camera_calibration":
        os.path.join(LEGACY_DATA_DIR, "kalibrator_systematic_error_x"),
    "measurement_error/y_camera_calibration":
        os.path.join(LEGACY_DATA_DIR, "kalibrator_systematic_y"),

    "circular_baseline":   os.path.join(LEGACY_DATA_DIR, "Circular Baseline"),
    "circular_calibrated": os.path.join(LEGACY_DATA_DIR, "Circular Kalibrasi"),

    # trajectory video (only present in the Code folder, not copied to After Lulus Paper/Data)
    "video_baseline_x":   os.path.join(LEGACY_CODE_DIR, "BASELINE_JALUR_FINAL_VIDEO", "video"),
    "video_calibrated_x": os.path.join(LEGACY_CODE_DIR, "KALIBRASI_JALUR_FINAL_VIDEO_3", "video"),
    "video_kalibrasi_x":  os.path.join(LEGACY_CODE_DIR, "KALIBRASI_X_VIDEO_BENERAN", "video"),
    "video_baseline_y":   os.path.join(LEGACY_DATA_DIR, "BASELINE_Y_VIDEO_FINAL_BGT_BGT", "video"),
    "video_calibrated_y": os.path.join(LEGACY_DATA_DIR, "KALIBRASI_Y_VIDEO_FINAL_BGT_BGT", "video"),
}


_DATASET_PATTERNS = ("oriy1.png", "pose_video_*.avi", "calib_0000.png", "*.csv")


def _deepen(p: str) -> str:
    """Descend into the subfolder that actually contains the dataset files."""
    if not os.path.isdir(p):
        return p
    for pat in _DATASET_PATTERNS:
        if glob.glob(os.path.join(p, pat)):
            return p
    for pat in _DATASET_PATTERNS:
        nested = glob.glob(os.path.join(p, "**", pat), recursive=True)
        if nested:
            return os.path.dirname(nested[0])
    return p


def _has_data(p: str) -> bool:
    """True if the folder contains dataset files (empty folders do not count)."""
    if not os.path.isdir(p):
        return False
    d = _deepen(p)
    return any(glob.glob(os.path.join(d, pat)) for pat in _DATASET_PATTERNS)


def resolve(name: str) -> str:
    """Dataset folder `name`: look in data/raw first, then fall back to the legacy path.

    A folder that exists but is EMPTY is considered not ready, so it automatically
    falls back to the legacy path. If neither exists, the expected location under
    data/raw is returned so that the error message points to the right place.
    """
    repo_path = os.path.normpath(os.path.join(DATA_DIR, name))
    legacy_path = LEGACY_PATHS.get(name)
    if _has_data(repo_path):
        return _deepen(repo_path)
    if legacy_path and _has_data(legacy_path):
        return _deepen(legacy_path)
    return repo_path


def status(name: str) -> tuple[str, bool]:
    p = resolve(name)
    return p, _has_data(p)


# ==========================================================================
# 3. DATASET PER STAGE
# ==========================================================================
# Stage 1 — camera calibration (needs chessboard images)
CAMERA_CALIB_DATASET = status("camera_calibration/dataset_kalibrasi_fix_prime_260")[0]

# Stage 2 — machine calibration (needs the oriy/fwd/bck triplet)
RUN_MODE = os.environ.get("KALIBRASI_MODE", "calibrated")  # baseline | calibrated | measurement_error

# Machine parameters per mode (values from the research result logs: docs/03)
MODE_PARAMS = {
    "baseline":          {"delta_x": 10.0, "delta_y": -10.0, "steps_x": 80.00, "steps_y": 80.00},
    "calibrated":        {"delta_x": 10.0, "delta_y": -10.0, "steps_x": 79.72, "steps_y": 80.40},
    "measurement_error": {"delta_x": 0.5,  "delta_y": 0.5,   "steps_x": 80.00, "steps_y": 80.00},
}

DATASET_X_BY_MODE = {
    "baseline":          "linear_baseline_x",
    "calibrated":        "linear_calibrated_x",
    "measurement_error": "measurement_error/x_machine_movement",
}
DATASET_Y_BY_MODE = {
    "baseline":          "linear_baseline_y",
    "calibrated":        "linear_calibrated_y",
    "measurement_error": "measurement_error/y_machine_movement",
}

DATASET_X = status(DATASET_X_BY_MODE.get(RUN_MODE, "linear_calibrated_x"))[0]
DATASET_Y = status(DATASET_Y_BY_MODE.get(RUN_MODE, "linear_calibrated_y"))[0]

# Stage 3 — virtual encoder: video folder + output CSV filename prefix
VIDEO_DATASET = os.environ.get("KALIBRASI_VIDEO", "video_calibrated_x")
VIDEO_DIR = status(VIDEO_DATASET)[0]
VIDEO_PATTERN = "pose_video_{:02d}.avi"
CSV_PREFIX = os.environ.get("KALIBRASI_CSV_PREFIX", "JALUR_VIDEO_FINAL_3")
FILE_INDICES = list(range(1, 11))

# Stage 4 — trajectory evaluation: baseline vs calibrated CSV
CSV_DIR_BASELINE = status("circular_baseline")[0]
CSV_DIR_CALIBRATED = status("circular_calibrated")[0]
CSV_BASELINE_NAME = "hasil_fix_banget_baseline_{:02d}.csv"
CSV_CALIBRATED_NAME = "JALUR_VIDEO_FINAL_3_{:02d}.csv"

# Output figure folder for the manuscript
FIG_DIR = os.path.join(REPO_ROOT, "figures")

# Manuscript-ready figures: the exact files that are placed in the paper
# (paper plots produced by 07_paper_figures/ and the measurement-error plot)
PAPER_FIG_DIR = os.path.join(REPO_ROOT, "figures", "paper")

# Small CSVs for the manuscript figure cells (already copied to data/processed/virtual_encoder)
CSV_VE_DIR = os.path.join(OUTPUT_DIR, "virtual_encoder")
CSV_NASKAH = {
    "baseline_x":   os.path.join(CSV_VE_DIR, "baseline_x.csv"),
    "baseline_y":   os.path.join(CSV_VE_DIR, "baseline_y.csv"),
    "calibrated_x": os.path.join(CSV_VE_DIR, "calibrated_x.csv"),
    "calibrated_y": os.path.join(CSV_VE_DIR, "calibrated_y.csv"),
    "baseline_x_analysis":   os.path.join(CSV_VE_DIR, "baseline_x_analysis.csv"),
    "calibrated_x_analysis": os.path.join(CSV_VE_DIR, "calibrated_x_analysis.csv"),
}

# Ellipse trajectory parameters (ground truth)
ELLIPSE = {"center_x": 0.0, "center_y": -3.162277, "skala": 10.0, "ratio": 8.0,
           "resolusi_titik": 240, "angle_a": 45, "angle_b": 135}

# Chessboard
CHESSBOARD_SIZE = (7, 7)   # inner corner points
SQUARE_SIZE_MM = 20.0


def diagnose() -> None:
    """Print a status table of all required datasets."""
    print(f"REPO_ROOT  : {REPO_ROOT}")
    print(f"DATA_DIR   : {DATA_DIR}  (exists: {os.path.isdir(DATA_DIR)})")
    print(f"OUTPUT_DIR : {OUTPUT_DIR}")
    print(f"RUN_MODE   : {RUN_MODE}")
    print()
    print(f"{'stage':8s} {'dataset name':46s} {'status':16s} location")
    print("-" * 120)
    rows = [
        ("stage 1", "camera_calibration/dataset_kalibrasi_fix_prime_260"),
        ("stage 2", DATASET_X_BY_MODE.get(RUN_MODE, "")),
        ("stage 2", DATASET_Y_BY_MODE.get(RUN_MODE, "")),
        ("stage 3", VIDEO_DATASET),
        ("stage 4", "circular_baseline"),
        ("stage 4", "circular_calibrated"),
    ]
    for tahap, name in rows:
        if not name:
            continue
        p, ok = status(name)
        n = len(glob.glob(os.path.join(p, "*"))) if ok else 0
        print(f"{tahap:8s} {name:46s} {'OK' if ok else 'NOT FOUND':16s} "
              f"{p}" + (f"  ({n} files)" if ok else ""))
    print()
    print("Legacy paths used as fallback:")
    for k, v in LEGACY_PATHS.items():
        print(f"  [{'x' if os.path.isdir(v) else ' '}] {k:46s} {v}")


if __name__ == "__main__":
    diagnose()
