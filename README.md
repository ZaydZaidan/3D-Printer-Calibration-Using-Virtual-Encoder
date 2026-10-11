# Kalibrasi 3D Printer Berbasis Virtual Encoder & Visi Komputer

Kalibrasi sumbu mesin 3D printer (**steps/mm**, **backlash**, **skew/ortogonalitas XY**)
tanpa dial gauge dan tanpa encoder — memakai satu kamera + papan catur sebagai
**virtual encoder**. Hasilnya diuji dengan membebankan lintasan elips dan mengukur
deviasi terhadap ground truth.

> **Mulai dari sini:** [`docs/00_PANDUAN.md`](docs/00_PANDUAN.md) — panduan handoff
> langkah demi langkah, lengkap dengan hasil yang seharusnya Anda lihat di tiap tahap.

---

## Hasil Utama

**Kalibrasi mesin** (pengujian linear, target 10 mm, 10 sampel valid dari 40 percobaan):

| Metrik | Baseline | Setelah kalibrasi | Perbaikan |
|---|---|---|---|
| Error sumbu X | 0.0463 mm | 0.0071 mm | 84.7 % |
| Error sumbu Y | 0.0550 mm | 0.0054 mm | 90.2 % |
| Drift Y saat gerak X | 0.0937 mm | 0.0043 mm | 95.4 % |
| Drift X saat gerak Y | 0.0898 mm | 0.0036 mm | 96.0 % |

Parameter awal: steps/mm X 80, Y 80; backlash comp 0; skew comp 0.
Parameter hasil kalibrasi: steps/mm X 79.72, Y 80.40; backlash X 0.0124 mm, Y 0.0244 mm;
skew -0.009327 (X), 0.009025 (Y) — sekitar ±0.52 derajat.

**Evaluasi lintasan elips** (RMSE terhadap ground truth):

| Metrik | Baseline | Setelah kalibrasi |
|---|---|---|
| RMSE X | 76.91 µm (std 5.33) | 34.42 µm (std 1.61) |
| RMSE Y | 65.29 µm (std 4.67) | 30.75 µm (std 1.30) |
| **RMSE Total** | **100.89 µm** (std 7.00) | **46.17 µm** (std 1.68) |

**Perbaikan akurasi lintasan: 54.24 %.** Angka-angka ini dihasilkan dengan menjalankan
ulang notebook di repo ini, bukan disalin dari naskah.

**Soal nilai akhirnya, penting dipahami:** 79.72 / 80.40 bukan hasil satu kali hitung.
Kalibrasi ini dilakukan **berulang** — tiap putaran, rekomendasi parameter baru
dimasukkan lagi ke mesin, dataset diambil ulang, lalu diukur lagi, sampai **errornya tidak
bergerak jauh lagi (steady state)** dan sudah masuk orde batas *measurement error* alat
ukur. Rantainya: 80.00 (baseline) -> 79.6314 (rekomendasi putaran 1) -> beberapa putaran
antara -> **79.72 (final)**. Jadi kalau Anda menjalankan notebook dengan dataset yang ada
dan mendapat rekomendasi 79.6314, itu bukan bug — itu putaran pertama, bukan nilai final.
Prosedur lengkapnya di [`docs/00_PANDUAN.md`](docs/00_PANDUAN.md) Langkah 2b.

**Measurement error** (validasi terhadap dial gauge, jarak gerak 0.5 mm, 5 iterasi):
selisih absolut rata-rata antara pembacaan virtual encoder dan dial gauge adalah
**4.96 µm** (gabungan sumbu X) dan **7.81 µm** (gabungan sumbu Y) — masih di dalam
ketelitian alat ukur dial gauge yang ±10 µm.

---

## Alur Penelitian

```
 [1] Kalibrasi KAMERA
     EDLines -> line screening -> subpixel corner -> corner sorting (homografi)
     -> cv2.calibrateCamera -> matriks intrinsik K + koefisien distorsi D
     (keluaran: data/processed/camera_calibration/*.csv)
                     |
                     v
 [2] Kalibrasi MESIN (pengujian linear per sumbu)
     Data dari otomasi_pengujian_linear.py, parameter awal 80/80/0/0
     -> solvePnP per citra -> dX/dY, backlash, skew
     -> rekomendasi firmware M92 (steps/mm), M425 (backlash), M852 (skew)
                     |
                     v
 [3] Pakai nilai rekomendasi
     Nilai baru dimasukkan ke otomasi_lintasan_elips.py
     -> ambil video lintasan elips terkalibrasi (dan sebelumnya saat baseline)
     -> ulangi [2] untuk mengukur sisa error
                     |
                     v
 [4] Virtual Encoder
     Tiap frame video: deteksi papan -> solvePnP -> tvec
     -> posisi relatif terhadap frame awal -> lintasan X(t), Y(t) dalam mm
     -> ekspor CSV
                     |
                     v
 [5] Evaluasi lintasan
     Ground truth = 2 elips berpotongan (45 & 135 derajat), segmen maju + mundur
     Nearest neighbour (cKDTree) -> RMSE X, Y, total dalam mikron
     Baseline vs terkalibrasi -> persen perbaikan

 [6] Measurement error (terpisah, dilengkapi dial gauge)
     Parameter baseline, jarak gerak diperkecil ke 0.5 mm
     -> bandingkan pembacaan metode ini dengan dial gauge
     (data tersedia di data/raw/measurement_error/, kode pengolahan belum ada)
```

---

## Notebook

| Tahap | Berkas | Masukan | Keluaran |
|---|---|---|---|
| 1 | `01_camera_calibration_paper/kalibrasi_kamera.ipynb` | citra papan catur | `camera_matrix.csv`, `dist_coeffs.csv`, `camera_params.csv`, `reprojection_rmse.csv` |
| 2 | `02_machine_calibration/kalibrasi_mesin.ipynb` | K/D + dataset `oriy/fwd/bck` | rekomendasi `M92`/`M425`/`M852`, gambar `visualisasi_*.png` |
| 3 | `03_virtual_encoder/kalibrasi_lintasan.ipynb` | video `pose_video_XX.avi` | CSV lintasan + gambar perbandingan |
| 4 | `04_trajectory_evaluation/evaluasi_lintasan.ipynb` | 2 CSV lintasan | gambar evaluasi, RMSE µm, % perbaikan |
| 6 | `06_measurement_error/plot_measurement_error.py` | `dial_vs_ve.csv` | gambar 4 panel + tabel MAE |

Berkas pendukung:

- `config_paths.py` — **semua path dataset ada di sini.** Cek kondisi data dengan
  `python config_paths.py`.
- `calibration_pipeline.py` — fungsi deteksi sudut (EDLines, screening, subpixel,
  sorting) yang dipakai bersama oleh semua notebook.
- `05_akuisisi_alat/` — skrip yang memerlukan mesin + kamera (lihat README di dalamnya).

---

## Struktur Folder

```
Folder Rapih Code & Data Thesis/
├─ README.md
├─ config_paths.py                  <- semua path (jalankan untuk cek data)
├─ calibration_pipeline.py          <- fungsi deteksi sudut bersama
├─ requirements.txt
├─ 01_camera_calibration_paper/kalibrasi_kamera.ipynb
├─ 02_machine_calibration/kalibrasi_mesin.ipynb
├─ 03_virtual_encoder/kalibrasi_lintasan.ipynb
├─ 04_trajectory_evaluation/evaluasi_lintasan.ipynb
├─ 05_akuisisi_alat/                <- butuh mesin & kamera
├─ 06_measurement_error/plot_measurement_error.py   <- dial gauge vs virtual encoder
├─ data/
│  ├─ MANIFEST.md                   <- pemetaan nama folder asli -> nama di repo
│  ├─ raw/                          <- data mentah + video (1.9 GB, TIDAK masuk git)
│  └─ processed/                    <- keluaran tiap tahap (masuk git)
├─ figures/                         <- gambar untuk naskah
└─ docs/
   ├─ 00_PANDUAN.md                 <- PANDUAN HANDOFF (mulai dari sini)
   ├─ 01_audit_kode.md              <- audit kode asli & rencana penataan
   ├─ 02_peran_file.md              <- peran tiap berkas penelitian
   └─ 03_hasil_dan_lokasi_data.md   <- angka hasil & lokasi data
```

> Data mentah **tidak** di-commit ke git (ukurannya 1.9 GB). Data ikut sebagai folder
> ini apa adanya, dan `data/MANIFEST.md` menjelaskan asal setiap folder.

---

## Menjalankan

```bash
pip install -r requirements.txt
python config_paths.py          # cek semua dataset terbaca
```

`cv2.ximgproc` (`EdgeDrawing`) **hanya ada di `opencv-contrib-python`**, bukan
`opencv-python`. Versi yang dipakai penelitian: Python 3.11.9,
opencv-contrib-python 4.12.0.88.

Mode pengujian dipilih lewat environment variable, tanpa mengedit notebook:

```bash
set KALIBRASI_MODE=baseline        # Windows   (baseline | calibrated | measurement_error)
export KALIBRASI_MODE=baseline     # Linux/macOS
```

Detail tiap tahap, hasil yang diharapkan, dan batasan yang masih terbuka ada di
[`docs/00_PANDUAN.md`](docs/00_PANDUAN.md).
