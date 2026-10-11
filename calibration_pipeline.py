"""Pipeline deteksi sudut papan catur "sesuai paper".

Diekstrak dari kode penelitian asli tanpa mengubah isinya. Fungsi-fungsi ini dipakai
bersama oleh:
  - 01_camera_calibration_paper/kalibrasi_kamera.ipynb  (kalibrasi kamera)
  - 02_machine_calibration/kalibrasi_mesin.ipynb        (kalibrasi mesin)
  - 03_virtual_encoder/...                              (virtual encoder)

Tahapan: EDLines -> line screening -> subpixel -> pengurutan sudut via homografi.

Memerlukan opencv-contrib (cv2.ximgproc).
"""

import cv2
import numpy as np
from scipy.spatial import distance

__all__ = ["detect_edlines_raw", "calculate_angle", "fit_line_gradient", "intersect_lines", "get_initial_corners_strict_paper", "optimize_subpixel_gradient", "sort_corners_robust_paper"]

def detect_edlines_raw(gray):
    ed = cv2.ximgproc.createEdgeDrawing()
    ed.detectEdges(gray) 
    lines = ed.detectLines()
    return lines.reshape(-1, 4) if lines is not None else []


def calculate_angle(x1, y1, x2, y2):
    angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    if angle < 0: angle += 180
    return angle


def fit_line_gradient(gray, line, h=4, n=20):
    x1, y1, x2, y2 = line
    vx, vy = x2 - x1, y2 - y1
    length = np.hypot(vx, vy)
    if length == 0: return None
    vx, vy = vx / length, vy / length
    nx, ny = -vy, vx 
    min_x, max_x = max(0, int(min(x1, x2) - h)), min(gray.shape[1]-1, int(max(x1, x2) + h))
    min_y, max_y = max(0, int(min(y1, y2) - h)), min(gray.shape[0]-1, int(max(y1, y2) + h))
    roi = gray[min_y:max_y+1, min_x:max_x+1]
    gx, gy = cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=3), cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.hypot(gx, gy)
    points = []
    for i in range(roi.shape[0]):
        for j in range(roi.shape[1]):
            px, py = min_x + j, min_y + i
            if abs(nx*(px - x1) + ny*(py - y1)) <= h:
                points.append((grad_mag[i, j], px, py))
    points.sort(key=lambda item: item[0], reverse=True)
    top_points = points[:n]
    if len(top_points) < 2: return None
    pts_arr = np.array([[pt[1], pt[2]] for pt in top_points], dtype=np.float32)
    vx_f, vy_f, x0_f, y0_f = cv2.fitLine(pts_arr, cv2.DIST_L2, 0, 0.01, 0.01)
    return (vx_f[0], vy_f[0], x0_f[0], y0_f[0])


def intersect_lines(lines_params):
    A, B = [], []
    for vx, vy, x0, y0 in lines_params:
        A.append([-vy, vx])
        B.append(-vy * x0 + vx * y0)
    try:
        res, _, _, _ = np.linalg.lstsq(np.array(A), np.array(B), rcond=None)
        return res.flatten()
    except: return None


def get_initial_corners_strict_paper(gray, lines, r_thresh=10.0, L_thresh=15.0, theta_thr=8.0):
    raw_corners, valid_lines = [], []
    if lines is None or len(lines) < 3: return [], []
    endpoints = [{'id': i, 'pt': l[:2], 'line': l} for i, l in enumerate(lines)] + \
                [{'id': i, 'pt': l[2:], 'line': l} for i, l in enumerate(lines)]
    for i in range(len(lines)):
        for pt in [lines[i][:2], lines[i][2:]]:
            neighbors = [ep for ep in endpoints if ep['id'] != i and distance.euclidean(pt, ep['pt']) < r_thresh]
            group_lines = []
            if len(neighbors) >= 3:
                four_lines = [lines[i]] + [n['line'] for n in neighbors[:3]]
                if all(np.linalg.norm(l[:2] - l[2:]) > L_thresh for l in four_lines):
                    angles = [calculate_angle(*l) for l in four_lines]
                    if sum(1 for a in range(4) for b in range(a + 1, 4) if min(abs(angles[a] - angles[b]), abs(abs(angles[a] - angles[b]) - 180)) < theta_thr) >= 2:
                        group_lines = four_lines
            elif len(neighbors) == 2:
                three_lines = [lines[i]] + [n['line'] for n in neighbors[:2]]
                if all(np.linalg.norm(l[:2] - l[2:]) > L_thresh for l in three_lines):
                    angles = [calculate_angle(*l) for l in three_lines]
                    if any(min(abs(angles[a] - angles[b]), abs(abs(angles[a] - angles[b]) - 180)) < theta_thr for a in range(3) for b in range(a+1, 3)):
                        group_lines = three_lines
            if group_lines:
                fitted = [fit_line_gradient(gray, gl) for gl in group_lines]
                fitted = [p for p in fitted if p is not None]
                if len(fitted) >= 2:
                    isect = intersect_lines(fitted)
                    if isect is not None:
                        raw_corners.append(isect)
                        valid_lines.extend(group_lines)
    if not raw_corners: return [], []
    corners = np.array(raw_corners, dtype=np.float32)
    filt = []
    for p in corners:
        if len(filt) == 0 or np.min(np.linalg.norm(np.array(filt) - p, axis=1)) > 15.0: filt.append(p)
    return np.array(filt), np.unique(np.array(valid_lines), axis=0) if valid_lines else []


def optimize_subpixel_gradient(gray, corners, win_size=5):
    if corners is None or len(corners) == 0: return None
    opt = []
    for p in corners:
        x, y = int(p[0]), int(p[1])
        if x-win_size < 0 or y-win_size < 0 or x+win_size >= gray.shape[1] or y+win_size >= gray.shape[0]:
            opt.append(p); continue
        roi = gray[y-win_size:y+win_size, x-win_size:x+win_size]
        gx, gy = cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=3), cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=3)
        sum_ggT, sum_ggTq = np.zeros((2, 2)), np.zeros((2, 1))
        for i in range(roi.shape[0]):
            for j in range(roi.shape[1]):
                g = np.array([[gx[i, j]], [gy[i, j]]])
                q = np.array([[x - win_size + j], [y - win_size + i]])
                sum_ggT += g @ g.T; sum_ggTq += (g @ g.T) @ q
        try: opt.append((np.linalg.inv(sum_ggT) @ sum_ggTq).flatten())
        except: opt.append(p)
    return np.array(opt, dtype=np.float32)


def sort_corners_robust_paper(corners, gray_img, grid_size):
    if corners is None or len(corners) < (grid_size[0] * grid_size[1]):
        return None

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    enhanced = clahe.apply(gray_img)
    
    ed = cv2.ximgproc.createEdgeDrawing()
    ed.detectEdges(enhanced)
    ellipses = ed.detectEllipses()
    
    candidates = []
    if ellipses is not None:
        candidates = [[e[0], e[1]] for e in ellipses[0]]
    
    if len(candidates) < 3:
        circles_hough = cv2.HoughCircles(cv2.GaussianBlur(enhanced, (5,5), 0), 
                                         cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                                         param1=50, param2=25, minRadius=5, maxRadius=30)
        if circles_hough is not None:
            candidates.extend(circles_hough[0][:, :2].tolist())

    if len(candidates) < 3:
        return None

    # --- 1. Filter 49 Titik Terdekat dengan Pusat (Buang Noise Background) ---
    candidate_scores = []
    for center in candidates:
        center_pt = np.array(center)
        dist_sum = np.sum(np.linalg.norm(corners - center_pt, axis=1))
        candidate_scores.append((dist_sum, center))
    
    candidate_scores.sort(key=lambda x: x[0])
    top3 = np.array([x[1] for x in candidate_scores[:3]])

    # Cari origin tengah kasar untuk filter jarak
    origin_approx = np.mean(top3, axis=0) 
    dists_to_origin = np.linalg.norm(corners - origin_approx, axis=1)
    
    m_expected = grid_size[0] * grid_size[1]
    true_corners = corners[np.argsort(dists_to_origin)[:m_expected]]

    # --- 2. KUNCI PERBAIKAN: Identifikasi 4 Sudut Berdasarkan Koordinat Gambar ---
    # Kita paksa mencari ujung berdasarkan sumbu X dan Y dari gambar itu sendiri
    sum_coords = true_corners[:, 0] + true_corners[:, 1]
    diff_coords = true_corners[:, 0] - true_corners[:, 1]
    
    tl_idx = np.argmin(sum_coords)  # Top-Left (Kiri-Atas, X+Y terkecil)
    br_idx = np.argmax(sum_coords)  # Bottom-Right (Kanan-Bawah, X+Y terbesar)
    tr_idx = np.argmax(diff_coords) # Top-Right (Kanan-Atas, X-Y terbesar)
    bl_idx = np.argmin(diff_coords) # Bottom-Left (Kiri-Bawah, X-Y terkecil)
    
    src_pts = np.array([
        true_corners[tl_idx],
        true_corners[tr_idx],
        true_corners[br_idx],
        true_corners[bl_idx]
    ], dtype=np.float32)
    
    # Grid 2D ideal (0,0 ada di Kiri-Atas)
    dst_pts = np.array([
        [0, 0],
        [grid_size[0] - 1, 0],
        [grid_size[0] - 1, grid_size[1] - 1],
        [0, grid_size[1] - 1]
    ], dtype=np.float32)
    
    # --- 3. Homography Snapping ---
    H, _ = cv2.findHomography(dst_pts, src_pts)
    if H is None: return None
    
    sorted_corners = []
    used_indices = set()
    
    # Looping wajib: Baris dulu (Y), baru Kolom (X) agar sinkron dengan objp (kiri->kanan, atas->bawah)
    for row in range(grid_size[1]):
        for col in range(grid_size[0]):
            ideal_pt = cv2.perspectiveTransform(np.array([[[col, row]]], dtype=np.float32), H)[0][0]
            dists = np.linalg.norm(true_corners - ideal_pt, axis=1)
            
            for idx_closest in np.argsort(dists):
                if idx_closest not in used_indices:
                    sorted_corners.append(true_corners[idx_closest])
                    used_indices.add(idx_closest)
                    break

    return np.array(sorted_corners, dtype=np.float32)
