# MANIFEST DATA

Pemetaan dataset: nama asli (di `After Lulus Paper/Data/`) -> nama di repo ini.
Semua dataset citra/video **tidak masuk git** (lihat `.gitignore`); yang masuk git
hanya CSV hasil olahan di `data/processed/`.

## 1. Kalibrasi kamera

| Nama di repo | Nama asli | Isi | Ukuran | Git |
|---|---|---|---|---|
| `camera_calibration/dataset_kalibrasi_fix_prime_260/` | `dataset_kalibrasi_fix_prime_260` | 10 citra `calib_XXXX.png` + margin hitam | kecil | ya |
| `camera_calibration/dataset_kalibrasi_ditambah/` | `dataset_kalibrasi_ditambah` | 97 citra `oriy/fwd/bck` | ~20 MB | tidak |

> Catatan: nama folder `fix_prime_260` menyiratkan 260 citra, isinya hanya 10.
> Perlu dikonfirmasi apakah ini dataset yang menghasilkan angka di naskah.

## 2. Pengujian linear (kalibrasi mesin) - TERKONFIRMASI penulis

| Nama di repo | Nama asli | Sumbu | Kondisi | File | Ukuran | Git |
|---|---|---|---|---|---|---|
| `linear_baseline_x/` | `BASELINE_X_INDIVIDUAL` | X | baseline | 120 | 22 MB | tidak |
| `linear_baseline_y/` | `BASELINE_Y_FIX_METHOD` | Y | baseline | 120 | 22 MB | tidak |
| `linear_calibrated_x/` | `X_LAST_FIX` | X | setelah kalibrasi | 120 | 22 MB | tidak |
| `linear_calibrated_y/` | `Y_LAST_FIX` | Y | setelah kalibrasi | 120 | 21 MB | tidak |

Tiap folder berisi 40 triplet: `oriy{i}.png`, `fwd{i}.png`, `bck{i}.png` (i = 1..40),
sesuai `FILE_INDICES = list(range(1, 41))` di notebook kalibrasi mesin.

## 3. Measurement error (sebelumnya "systematic error") - RENAME DISETUJUI penulis

Dipakai untuk membandingkan pembacaan metode ini dengan **dial gauge**.
Konfigurasi: parameter baseline semua (backlash comp 0, skew comp 0, steps/mm 80),
dan **jarak gerak diperkecil menjadi 0.5 mm** (bukan 10 mm).

| Nama di repo | Nama asli | Isi | File | Ukuran | Git |
|---|---|---|---|---|---|
| `measurement_error/x_camera_calibration/` | `kalibrator_systematic_error_x` | dataset kalibrasi kamera untuk sesi ini | 54 | 11 MB | tidak |
| `measurement_error/x_machine_movement/` | `systematic_error_x` | hasil pergerakan mesin sumbu X | 120 | 24 MB | tidak |
| `measurement_error/y_camera_calibration/` | `kalibrator_systematic_y` | dataset kalibrasi kamera untuk sesi ini | 31 | 5.4 MB | tidak |
| `measurement_error/y_machine_movement/` | `systematic_error_Y` | hasil pergerakan mesin sumbu Y | 120 | 21 MB | tidak |
| `measurement_error/x_dial_gauge/` | `Semester 8/.../images/Hasil/Kalibrator_x` | 15 foto dial gauge sumbu X (`orix/fwd/bck` 1-5) + 3 gambar visualisasi | 18 | kecil | tidak |
| `measurement_error/y_dial_gauge/` | `Semester 8/.../images/Hasil/Kalibrator_y` | 15 foto dial gauge sumbu Y (`oriy/fwd/bck` 1-5) + 3 gambar visualisasi | 18 | kecil | tidak |

> Yang menghasilkan dataset ini: `otomasikalibrasi.py` dengan `TEST_MODE = 'X+'` / `'Y+'`,
> di mana `fwd_move = (0.5, 0.0)` / `(0.0, 0.5)` — inilah bukti jarak 0.5 mm di kode.
> Untuk mengolahnya di notebook kalibrasi mesin, pilih `KALIBRASI_MODE=measurement_error`
> (otomatis memakai target 0.5 mm dan steps/mm baseline).
>
> `*_camera_calibration/` berasal dari `otomasikalibrasi.py`; `*_dial_gauge/` adalah FOTO
> dial gauge yang dipakai untuk menghitung measurement error. Angka hasil pembandingnya
> ada di `data/processed/measurement_error/dial_vs_ve.csv`.

## 4. Lintasan elips (circular)

| Nama di repo | Nama asli | Isi | Ukuran | Git |
|---|---|---|---|---|
| `circular_baseline/` | `Circular Baseline` | `hasil_fix_banget_baseline_XX.csv` + PNG | 4.1 MB | CSV ya, PNG tidak |
| `circular_calibrated/` | `Circular Kalibrasi` | `JALUR_VIDEO_FINAL_3_XX.csv` + PNG | 8.2 MB | CSV ya, PNG tidak |

Video mentahnya (tidak masuk git), sesuai penjelasan pemilik penelitian:

| Folder di repo | Nama asli | Isi | Berkas | Ukuran |
|---|---|---|---|---|
| `video_baseline_x/` | `BASELINE_JALUR_FINAL_VIDEO` | video pengujian **circular baseline** | 21 | 970 MB |
| `video_calibrated_x/` | `KALIBRASI_JALUR_FINAL_VIDEO_3` | video pengujian **circular hasil kalibrasi** | 11 | 547 MB |
| `video_kalibrasi_x/` | `KALIBRASI_X_VIDEO_BENERAN` | video sumbu X (gambar naskah) | 3 | 100 MB |
| `video_baseline_y/` | `BASELINE_Y_VIDEO_FINAL_BGT_BGT` | video sumbu Y baseline | 1 | 34 MB |
| `video_calibrated_y/` | `KALIBRASI_Y_VIDEO_FINAL_BGT_BGT` | video sumbu Y terkalibrasi | 1 | 38 MB |

Total 37 berkas / 1.7 GB. **Tidak perlu diproses ulang** untuk mereproduksi hasil
penelitian — CSV lintasan sudah ada di `circular_baseline/` dan `circular_calibrated/`.
(`HASIL_PENGUJIAN_LINTASAN` tidak disalin karena isinya gambar evaluasi, bukan video.)

## 5. Keluaran olahan (masuk git)

| Berkas | Isi | Ukuran |
|---|---|---|
| `processed/camera_calibration/camera_matrix.csv` | matriks intrinsik K 3x3 | kecil |
| `processed/camera_calibration/dist_coeffs.csv` | koefisien distorsi 1x5 | kecil |
| `processed/camera_calibration/camera_params.csv` | tabel parameter/nilai + ukuran citra | kecil |
| `processed/camera_calibration/reprojection_rmse.csv` | RMSE reprojection per citra | kecil |
| `processed/virtual_encoder/*.csv` | CSV lintasan untuk gambar naskah | kecil |
| `processed/measurement_error/dial_vs_ve.csv` | 20 baris pembanding dial gauge vs VE | kecil |

## 6. Duplikat di `SEMPRO/Code/`

Folder `systematic_error_x`, `systematic_error_Y`, `kalibrator_systematic_error_x`,
`kalibrator_systematic_y`, `X_LAST_FIX`, `Y_LAST_FIX`, `X_LAST`, `Y_LAST`,
`BASELINE_X_FIX_METHOD`, `BASELINE_Y_FIX_METHOD`, `KALIBRASI_X_SKEW_1_FIX`,
`KALIBRASI_X_STEPBACK_1_FIX_METHOD`, `KALIBRASI_Y_STEPBACK_1_FIX_METHOD` semuanya
punya salinan di `After Lulus Paper/Data/`. **Rujukan final = `After Lulus Paper/Data/`**;
yang di `Code/` dianggap arsip kerja.

---

## 7. Unduhan data mentah (untuk handoff)

Repo git sengaja **tidak** memuat data mentah yang besar.

**Tautan Google Drive:** https://drive.google.com/drive/folders/1-t_4XDX1aLUvNeTrkfXd1f1-iWcVR9tP?usp=sharing

(folder bernama `raw`, berisi seluruh isi `data/raw/`). Unduh, lalu taruh isinya sesuai
kolom "nama di repo" di atas.

| Paket | Isi | Ukuran | Tautan |
|---|---|---|---|
| Video lintasan | 5 folder `video_*` (37 berkas) | 1.7 GB | [https://drive.google.com/drive/folders/1-t_4XDX1aLUvNeTrkfXd1f1-iWcVR9tP?usp=sharing](https://drive.google.com/drive/folders/1-t_4XDX1aLUvNeTrkfXd1f1-iWcVR9tP?usp=sharing) |
| Citra + CSV mentah | `camera_calibration/`, `linear_*`, `measurement_error/`, `circular_*` | 183 MB | termasuk folder Drive di atas |

**Cara memakai:** unduh, ekstrak, lalu letakkan isinya **langsung di dalam** `data/raw/`
sehingga strukturnya menjadi `data/raw/linear_baseline_x/...`,
`data/raw/video_baseline_x/...`, dan seterusnya. Verifikasi dengan:

```bash
python config_paths.py
```

Semua baris harus berstatus `OK`. Kalau ada yang `TIDAK DITEMUKAN`, lokasinya akan
ditunjukkan di kolom terakhir.

**Cek kelengkapan paket video** (agar tidak ada berkas yang tertinggal saat mengunggah):

| Folder | Nama asli | Harus berisi |
|---|---|---|
| `video_baseline_x/` | `BASELINE_JALUR_FINAL_VIDEO` | 21 berkas `pose_video_01..21.avi` |
| `video_calibrated_x/` | `KALIBRASI_JALUR_FINAL_VIDEO_3` | 11 berkas (`pose_video_01..10.avi` + `pose_video_01 - KALIBRASI.avi`) |
| `video_kalibrasi_x/` | `KALIBRASI_X_VIDEO_BENERAN` | 3 berkas |
| `video_baseline_y/` | `BASELINE_Y_VIDEO_FINAL_BGT_BGT` | 1 berkas |
| `video_calibrated_y/` | `KALIBRASI_Y_VIDEO_FINAL_BGT_BGT` | 1 berkas |
