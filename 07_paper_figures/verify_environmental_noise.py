"""Reproduce the environmental-noise numbers used by plot_environmental_noise.py.

Why this file exists
--------------------
`plot_environmental_noise.py` plots a hard-coded array of 10 position deltas
(delta_x / delta_y in um). This script re-derives those deltas from the raw
captures so the figure can be audited instead of taken on trust.

Method (identical to the historical `FIND NOISE` notebook cell)
---------------------------------------------------------------
One static capture sequence, 24 photos, machine not commanded to move.
`calib_0000.png` is the anchor; each image in PAIRS is compared with it.
For both images the chessboard pose is estimated with the same pipeline used by
the calibration notebooks (EDLines -> initial corners -> sub-pixel refinement ->
robust sorting -> solvePnP), and the delta is the difference of the absoloute
translation components:

    delta_x = |tvec_x(image)| - |tvec_x(anchor|     [mm] -> um
    delta_y = |tvec_y(image)| - |tvec_y(anchor)|    [mm] -> um

A static machine should give delta = 0; whatever remains is the environmental
noise of the measurement chain.

Usage
-----
    python verify_environmental_noise.py [path/to/folder/with/calib_XXXX.png]

Default folder: ../data/raw/noise_static_capture (raw data is not tracked by git;
see README.md and data/MANIFEST.md for the download link).

Note on PAIR NUMBERS
--------------------
PAIRS reproduces the original notebook list verbatim, including the fact that
`calib_0019.png` is used TWICE (pairs 2 and 9). The published figure therefore
contains 10 data points coming from 9 distinct captures; elements 2 and 9 of
both arrays are identical, which is what makes this duplication detectable.
"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir))
sys.path.insert(0, REPO)

from calibration_pipeline import (  # noqa: E402
    detect_edlines_raw, get_initial_corners_strict_paper,
    optimize_subpixel_gradient, sort_corners_robust_paper,
)

CAM_DIR = os.path.join(REPO, "data", "processed", "camera_calibration")
DEFAULT_DIR = os.path.join(REPO, "data", "raw", "noise_static_capture")

CHESSBOARD_SIZE = (7, 7)
SQUARE_SIZE = 20.0          # mm, same target as the rest of the project
EXPECTED_PTS = CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1]

# Verbatim from the historical notebook cell: anchor calib_0000.png vs each of these
PAIR_NUMBERS = [11, 19, 13, 4, 18, 6, 7, 8, 19, 10]

# Hard-coded values in plot_environmental_noise.py (um)
FIGURE_DELTA_X = np.array([-4.8, -2.1, -4.0, 1.1, 1.2, 0.6, -4.6, -3.1, -2.1, 2.2])
FIGURE_DELTA_Y = np.array([-4.1, -6.7, -5.1, -3.0, -11.1, 0.1, -1.1, -8.7, -6.7, -3.1])


def load_camera_params():
    K = np.loadtxt(os.path.join(CAM_DIR, "camera_matrix.csv"), delimiter=",").astype(np.float64)
    D = np.loadtxt(os.path.join(CAM_DIR, "dist_coeffs.csv"), delimiter=",").astype(np.float64)
    return K, D.reshape(-1, 1)


def get_pose_from_image(image_path, K, D, objp):
    """Pose of one chessboard image. Returns (tvec, reprojection_rmse_px) or (None, None)."""
    if not os.path.exists(image_path):
        return None, None
    gray = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    initial_corners, _ = get_initial_corners_strict_paper(gray, detect_edlines_raw(gray))
    if initial_corners is None or len(initial_corners) < EXPECTED_PTS:
        return None, None
    refined = optimize_subpixel_gradient(gray, initial_corners)
    sorted_corners = sort_corners_robust_paper(refined, gray, CHESSBOARD_SIZE)
    if sorted_corners is None:
        return None, None
    corners_final = sorted_corners.reshape(-1, 1, 2)
    success, rvec, tvec = cv2.solvePnP(objp, corners_final, K, D)
    if not success:
        return None, None
    imgpts2, _ = cv2.projectPoints(objp, rvec, tvec, K, D)
    norm_l2 = cv2.norm(corners_final, imgpts2, cv2.NORM_L2)
    return tvec, np.sqrt((norm_l2 ** 2) / len(imgpts2))


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    if not os.path.isdir(folder):
        print(f"NOT FOUND: no image folder at\n    {folder}\n"
              "The static-capture dataset is raw data and is not tracked by git.\n"
              "Download it (see the link in README.md), or pass the folder as an argument:\n"
              "    python verify_environmental_noise.py D:/somewhere/calib_XXXX.png/")
        return 1

    K, D = load_camera_params()
    objp = np.zeros((EXPECTED_PTS, 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2) * SQUARE_SIZE

    anchor = os.path.join(folder, "calib_0000.png")
    print(f"images in dataset : {len([f for f in os.listdir(folder) if f.endswith('.png')])}")
    print(f"anchor            : calib_0000.png")
    print(f"pairs compared    : {len(PAIR_NUMBERS)} "
          f"({len(set(PAIR_NUMBERS))} distinct images - calib_0019 is used twice)\n")

    t_anchor, rmse_anchor = get_pose_from_image(anchor, K, D, objp)
    if t_anchor is None:
        print("FAILED: the anchor image could not be processed.")
        return 1

    print(f"{'pair':>4}  {'image':16s}  {'dX (um)':>9}  {'dY (um)':>9}   rmse px")
    dx_list, dy_list = [], []
    for i, n in enumerate(PAIR_NUMBERS, 1):
        t, rmse = get_pose_from_image(os.path.join(folder, f"calib_{n:04d}.png"), K, D, objp)
        if t is None:
            print(f"{i:>4}  calib_{n:04d}.png      [FAILED]")
            continue
        dx = (abs(t[0][0]) - abs(t_anchor[0][0])) * 1000.0
        dy = (abs(t[1][0]) - abs(t_anchor[1][0])) * 1000.0
        dx_list.append(dx)
        dy_list.append(dy)
        print(f"{i:>4}  calib_{n:04d}.png  {dx:9.2f}  {dy:9.2f}   {rmse:.4f}")

    if len(dx_list) != len(FIGURE_DELTA_X):
        print(f"\nonly {len(dx_list)} pairs were processed, cannot compare with the figure arrays.")
        return 1

    rec_x, rec_y = np.array(dx_list), np.array(dy_list)
    print("\nComparison with the hard-coded arrays in plot_environmental_noise.py")
    for name, rec, published in (("X", rec_x, FIGURE_DELTA_X), ("Y", rec_y, FIGURE_DELTA_Y)):
        worst = np.abs(np.round(rec, 1) - published).max()
        print(f"  axis {name}: reconstructed {np.round(rec, 2)}")
        print(f"          published     {published}")
        print(f"          max deviation {worst:.2f} um -> {'MATCH' if worst <= 0.05 else 'MISMATCH'}")

    print("\nTwo different statistics computed from these same deltas")
    print("  mean(delta)  = what the calibration notebook prints and what the thesis table")
    print("                 reports (labelled 'mean absolute error', which it is not):")
    print(f"      X = {abs(rec_x.mean()):.2f} um   SD(ddof=0) = {rec_x.std():.2f}")
    print(f"      Y = {abs(rec_y.mean()):.2f} um   SD(ddof=0) = {rec_y.std():.2f}")
    print("  mean(|delta|) = the true MAE, and what the figure draws:")
    print(f"      X = {np.abs(rec_x).mean():.2f} um   SD(ddof=1) = {np.abs(rec_x).std(ddof=1):.2f}")
    print(f"      Y = {np.abs(rec_y).mean():.2f} um   SD(ddof=1) = {np.abs(rec_y).std(ddof=1):.2f}")
    print("\nBecause the X deltas have mixed signs, |mean| and mean|.| differ for X (about")
    print("1.6 vs 2.6 um) while for Y all deltas are negative so both agree (about 4.9 um).")
    print("See docs/03_results_and_data_locations.md, 'Data-consistency verification'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
