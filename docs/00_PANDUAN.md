# PANDUAN HANDOFF — Cara Pakai & Mereproduksi Penelitian

Dokumen ini untuk **orang berikutnya** yang melanjutkan atau memakai repo ini.
Ikuti berurutan. Setiap tahap mencantumkan masukan, keluaran, dan **hasil yang
seharusnya Anda lihat**, supaya Anda tahu pekerjaan Anda benar atau tidak.

> Seluruh angka di dokumen ini sudah **diverifikasi ulang** dengan menjalankan kembali
> notebook di repo ini (bukan salinan dari naskah). Lihat bagian 4.

---

## 1. Ringkasan penelitian

Kalibrasi sumbu mesin 3D printer **tanpa dial gauge dan tanpa encoder**, memakai satu
kamera + papan catur sebagai **virtual encoder**. Yang dikalibrasi: **steps/mm**,
**backlash**, dan **skew/ortogonalitas XY**. Pembuktiannya lintasan elips bolak-balik
dibandingkan dengan ground truth.

Alur besar:

```
kalibrasi kamera -> kalibrasi mesin (linear) -> lintasan elips -> virtual encoder -> evaluasi
```

## 2. Hasil utama

**A. Kalibrasi mesin (pengujian linear, target 10 mm, 10 sampel valid dari 40)**

| Metrik | Baseline | Setelah kalibrasi | Perbaikan |
|---|---|---|---|
| Error sumbu X | 0.0463 mm | 0.0071 mm | 84.7 % |
| Error sumbu Y | 0.0550 mm | 0.0054 mm | 90.2 % |
| Drift Y saat gerak X (skew) | 0.0937 mm | 0.0043 mm | 95.4 % |
| Drift X saat gerak Y (skew) | 0.0898 mm | 0.0036 mm | 96.0 % |

Parameter: awal steps/mm **80 / 80**, backlash comp **0**, skew comp **0**.
Hasil: steps/mm **79.72 / 80.40**, backlash **0.0124 / 0.0244 mm**,
skew **-0.009327 / 0.009025** (≈ ±0.52°).

**B. Evaluasi lintasan elips (RMSE terhadap ground truth)**

| Metrik | Baseline | Setelah kalibrasi |
|---|---|---|
| RMSE X | 76.91 µm (std 5.33) | 34.42 µm (std 1.61) |
| RMSE Y | 65.29 µm (std 4.67) | 30.75 µm (std 1.30) |
| **RMSE Total** | **100.89 µm** (std 7.00) | **46.17 µm** (std 1.68) |

**Perbaikan akurasi lintasan: 54.24 %.**

## 3. Prasyarat

**Perangkat lunak**

```bash
pip install -r requirements.txt
```

- Python **3.11** (penelitian memakai 3.11.9).
- `opencv-contrib-python` **wajib** versi contrib — kode memakai `cv2.ximgproc`
  (`createEdgeDrawing`) yang tidak ada di `opencv-python` biasa.
- Paket: opencv-contrib-python 4.12.0.88, numpy 2.2.6, scipy 1.17.1, pandas 3.0.2,
  matplotlib 3.10.8. Jalankan notebook dengan `pandas` dan `numpy` tersedia karena
  pertukaran parameter kamera memakai CSV.

**Data** — sudah ikut di folder ini:

| Lokasi | Isi | Ukuran |
|---|---|---|
| `data/raw/camera_calibration/` | citra papan catur untuk kalibrasi kamera | 19 MB |
| `data/raw/linear_baseline_x`, `linear_baseline_y` | dataset linear sebelum kalibrasi | 44 MB |
| `data/raw/linear_calibrated_x`, `linear_calibrated_y` | dataset linear setelah kalibrasi | 44 MB |
| `data/raw/measurement_error/` | dataset dial gauge (0.5 mm, parameter baseline) | 63 MB |
| `data/raw/circular_baseline`, `circular_calibrated` | CSV + gambar lintasan elips | 13 MB |
| `data/raw/video_*` | video mentah lintasan (untuk menjalankan ulang virtual encoder) | 1.7 GB |

Rincian nama asli tiap folder: **`data/MANIFEST.md`**.

**Perangkat keras** — hanya diperlukan bila ingin **mengambil data baru** (folder `05_akuisisi_alat/`).
Untuk sekadar mengecek/mereproduksi hasil dari data yang sudah ada, tidak perlu mesin.

## 4. Bukti repo ini jalan (sudah diuji)

Setelah penataan, ketiga notebook dijalankan ulang dari nol di repo ini:

| Notebook | Hasil yang keluar | Cocok dengan log penelitian? |
|---|---|---|
| `01_.../kalibrasi_kamera.ipynb` | 10 citra valid. **RMSE reprojection keseluruhan 0.1154 px** (rata-rata per citra 0.1152 px; min 0.0979, maks 0.1249) | tidak ada log aslinya — artefak ini baru dibuat sekarang |
| `02_.../kalibrasi_mesin.ipynb` | X: Δ 10.0045 mm, error 0.0071 mm, RMSE 0.1186 px, `M92 X79.68`, `M425 X0.0068`, skew 0.000427 | **identik digit-per-digit** dengan `DATA HASIL KALIBRASI LINEAR X DAN Y.txt` |
| `02_.../kalibrasi_mesin.ipynb` | Y: Δ -10.0022 mm, error 0.0054 mm, RMSE 0.1281 px, `M92 Y80.38`, `M425 Y0.0068`, skew 0.000362 | **identik** dengan log yang sama |
| `04_.../evaluasi_lintasan.ipynb` | Baseline 100.89 µm -> terkalibrasi 46.17 µm, **perbaikan 54.24 %** | sesuai angka yang dilaporkan |

Artinya: data, konfigurasi path, dan pemisahan notebook sudah konsisten.

## 5. Struktur repo

```
Folder Rapih Code & Data Thesis/
├─ README.md                  ringkasan + hasil
├─ config_paths.py            >>> SEMUA PATH ADA DI SINI <<<
├─ calibration_pipeline.py    fungsi deteksi sudut (dipakai bersama semua notebook)
├─ requirements.txt
├─ 01_camera_calibration_paper/kalibrasi_kamera.ipynb
├─ 02_machine_calibration/kalibrasi_mesin.ipynb
├─ 03_virtual_encoder/kalibrasi_lintasan.ipynb
├─ 04_trajectory_evaluation/evaluasi_lintasan.ipynb
├─ 05_akuisisi_alat/          skrip yang butuh mesin & kamera (lihat README di dalamnya)
├─ 06_measurement_error/plot_measurement_error.py   dial gauge vs virtual encoder
├─ data/raw/                  data mentah + video (TIDAK di-commit ke git, ikut lewat folder ini)
├─ data/processed/            keluaran tiap tahap (masuk git, ukurannya kecil)
├─ figures/                   gambar untuk naskah
└─ docs/                      00 panduan ini, 01 audit, 02 peran file, 03 hasil & lokasi data
```

## 6. Cara menjalankan

### Langkah 0 — cek data (30 detik)

```bash
python config_paths.py
```

Keluarannya tabel: tiap dataset ditandai `OK` atau `TIDAK DITEMUKAN`, beserta lokasi
yang dipakai. Kalau ada yang `TIDAK DITEMUKAN`, taruh datasetnya di lokasi yang
ditunjukkan (atau ubah bagian `LEGACY_PATHS` di `config_paths.py`).

Jalankan notebook **dari dalam folder notebooknya masing-masing** (Jupyter sudah
melakukannya otomatis), supaya `config_paths.py` di akar repo bisa ditemukan.

### Langkah 1 — kalibrasi kamera

`01_camera_calibration_paper/kalibrasi_kamera.ipynb` — seluruh sel, urut.

- **Masukan:** `data/raw/camera_calibration/dataset_kalibrasi_fix_prime_260/`
- **Proses:** EDLines -> line screening -> optimasi subpiksel -> pengurutan 49 sudut
  lewat homografi -> `cv2.calibrateCamera`
- **Keluaran (semua ke `data/processed/camera_calibration/`):**
  - `camera_matrix.csv` — matriks intrinsik K (3x3)
  - `dist_coeffs.csv` — koefisien distorsi `[k1, k2, p1, p2, k3]`
  - `camera_params.csv` — tabel parameter/nilai + ukuran citra (mudah dibaca)
  - `reprojection_rmse.csv` — RMSE reprojection per citra
- **Hasil yang diharapkan:** sekitar 10 citra valid, RMSE ~0.10-0.13 px.
  Status "AKURAT" bila < 0.15 px.
  Ada dua angka RMSE yang dicetak notebook dan **keduanya benar**, jangan tertukar:
  **"Keseluruhan Reprojection Error (RMSE)"** = `sqrt(total_SSE / total_titik)` →
  **0.1154 px**; sedangkan **rata-rata RMSE per citra** = rata-rata biasa dari kolom
  `rmse_px` di `reprojection_rmse.csv` → **0.1152 px**. Keduanya berbeda sedikit karena
  yang pertama adalah akar-dari-rata-rata (RMS), yang kedua rata-rata-dari-akar.
  **Untuk dikutip di naskah, pakai angka yang dicetak notebook sendiri: 0.1154 px.**
- **Waktu:** ~25 detik untuk 10 citra.

Hasil pengujian di repo ini (RMSE reprojection keseluruhan 0.1154 px): `fx=2314.64`, `fy=2328.29`, `cx=637.08`, `cy=222.88`,
`D = [-0.056105, 0.959537, 0.000141, 0.000407, -5.033022]`.

> **Catatan:** K dan D di sini dihitung dari **10 citra** yang ada di repo, padahal nama
> foldernya menyiratkan 260 citra. Yang penting: K/D dari 10 citra ini **sudah terbukti
> mereproduksi seluruh angka naskah** (lihat bagian 4) — jadi untuk mereproduksi hasil
> penelitian, 10 citra ini cukup. Untuk pengambilan data baru, K/D Anda akan berbeda;
> itu normal dan tidak masalah (lihat bagian 7).

### Langkah 2 — kalibrasi mesin

`02_machine_calibration/kalibrasi_mesin.ipynb` — seluruh sel, urut.

- **Masukan:**
  - `data/processed/camera_calibration/*.csv` (dari langkah 1, dimuat otomatis)
  - dataset linear sesuai `RUN_MODE` (lihat di bawah): `oriy{i}.png`, `fwd{i}.png`,
    `bck{i}.png`, i = 1..40
- **Keluaran:** statistik rata-rata + rekomendasi firmware `M92`, `M425`, `M852`
  (cetak di layar), dan berkas gambar `visualisasi_*.png` di folder notebook.
- **Waktu:** ~2 menit per sumbu.

**Pilih mode tanpa mengedit notebook:**

```bash
# Windows
set KALIBRASI_MODE=baseline
# Linux / macOS
export KALIBRASI_MODE=baseline
```

| Mode | Dataset | steps/mm | target | catatan |
|---|---|---|---|---|
| `calibrated` (default) | `linear_calibrated_x/y` | 79.72 / 80.40 | 10 mm | mengukur **sisa** error setelah kalibrasi |
| `baseline` | `linear_baseline_x/y` | 80 / 80 | 10 mm | kondisi sebelum kalibrasi |
| `measurement_error` | `measurement_error/*_machine_movement` | 80 / 80 | 0.5 mm | untuk dibandingkan dengan dial gauge |

- **Hasil yang diharapkan (mode `calibrated`):** X → Δ 10.0045 mm, error 0.0071 mm,
  RMSE 0.1186 px. Y → Δ -10.0022 mm, error 0.0054 mm, RMSE 0.1281 px.
- **Hasil yang diharapkan (mode `baseline`):** X → error 0.0463 mm;
  Y → error 0.0550 mm.

> **Jangan bingung kalau rekomendasi yang keluar berbeda dari nilai di `config_paths.py`.**
> Dataset yang tersedia menghasilkan rekomendasi **79.6314 (X)** dan **80.4425 (Y)** —
> itu rekomendasi putaran pertama. Nilai final penelitian adalah **79.72 / 80.40**, hasil
> beberapa putaran *fine-tuning* (lihat naskah `bab4.tex` Tabel *Parameter Hasil Kalibrasi
> Fine Tuning*, dan `docs/03_hasil_dan_lokasi_data.md` bagian 5). Mode `calibrated` di repo
> ini memakai nilai final tersebut karena itulah yang menghasilkan angka pada naskah.

> Notebook ini **berhenti otomatis setelah 10 sampel valid**. Kalau banyak sampel gagal
> ("pose tidak ditemukan"), biasanya karena pencahayaan/eksposur berbeda dari waktu
> pengambilan data.

### Langkah 2b — fine-tuning: ulangi kalibrasi sampai error *steady state*

**Inti metode ini: satu kali kalibrasi belum cukup. Rekomendasinya harus dimasukkan
berulang kali.** Alurnya seperti ini, dan putaran ini yang diulang terus:

```
   parameter yang ADA di mesin            ukur                      rekomendasi BARU
   (STEPX, STEPY, BACKLASH,     -->   jalankan langkah 2   -->   (M92 steps/mm,
    SKEW_FACTOR)                      atas dataset baru          M425 backlash, M852 skew)
          ^                                                            |
          |                    MASUKKAN rekomendasi tadi              |
          +------------------- ke mesin, ambil data lagi <-------------+
                              (ulangi putaran ini)

   teruskan sampai error tidak bergerak jauh lagi   ->   STEADY STATE
```

Kenapa harus berulang: kondisi mekanik mesin (gesekan, kelonggaran gerigi, kemiringan
rangka) bisa bergeser antar sesi pengambilan data, jadi satu kali koreksi belum tentu
pas. Yang Anda lakukan adalah mengoreksi terus sampai **koreksi berikutnya tinggal nol** —
yaitu saat rekomendasi baru sudah hampir sama dengan nilai yang sedang dipakai.

Satu putaran praktisnya:

1. Masukkan parameter yang sekarang dipakai ke
   `05_akuisisi_alat/otomasi_pengujian_linear.py` (`STEPX`, `STEPY`, `BACKLASH`,
   `SKEW_FACTOR`).
2. Ambil dataset pengujian linear **baru** (mesin bergerak dengan parameter itu).
3. Jalankan notebook langkah 2 atas dataset baru tersebut → tercetak **error sisa** dan
   **rekomendasi baru**.
4. Kembali ke langkah 1 dengan rekomendasi tadi. Ulangi sampai *steady state*.

**Tanda sudah mencapai *steady state*:**

- Error perpindahan maju tidak lagi turun berarti, dan **sudah di orde batas
  *measurement error* alat ukur Anda** (di penelitian ini dial gauge beresolusi ±10 µm,
  dan error akhirnya 7,1 µm untuk X serta 5,4 µm untuk Y — sudah di dalam batas itu).
- Rekomendasi `steps/mm` baru **hampir sama** dengan nilai yang sedang dipakai.
- Rekomendasi `skew` sudah kecil; di penelitian ini putaran terakhir memberi
  0.000427 (≈0.024°) dan notebook menyatakan *"Sudah siku (Orthogonal), kompensasi
  tidak diperlukan"*.

**Contoh nyata dari penelitian ini** (rantai nilainya, lihat juga `docs/03` bagian 5):

```
80.00 steps/mm  (baseline, log tersimpan)
   -> 79.6314   (rekomendasi putaran 1, log tersimpan)
      -> 80.13 / 80.11 / varian skew   (putaran antara; datasetnya ada di ARSIP,
                                        TIDAK ditampilkan di naskah)
         -> 79.72  (FINAL, setelah steady state)
```

Naskah hanya menampilkan **dua titik**: baseline dan nilai final setelah fine-tuning.
Itu memang cukup untuk naskah — rantai antaranya tidak perlu.

**Catatan praktis kalau Anda mengulang dengan mesin sendiri:** repo ini menyediakan tiga
mode siap pakai (`baseline`, `calibrated`, `measurement_error`). Untuk iterasi fine-tuning
Anda sendiri, tambahkan satu entri di `config_paths.py` pada dua tempat:
`MODE_PARAMS` (nilai `delta`/`steps` yang sedang dipakai) dan
`DATASET_X_BY_MODE` / `DATASET_Y_BY_MODE` (folder dataset iterasi itu), lalu pilih
lewat `KALIBRASI_MODE`.

**Parameter final penelitian ini:**

| Parameter | Sumbu X | Sumbu Y |
|---|---|---|
| steps/mm | 79.72 | 80.40 |
| backlash | 13.3 µm | 31.4 µm |
| skew | -9.2 µm/mm (drift X saat Y bergerak) | 9.213 µm/mm (drift Y saat X bergerak) |

### Langkah 3 — virtual encoder (video -> lintasan)

`03_virtual_encoder/kalibrasi_lintasan.ipynb`

- **Masukan:** video `data/raw/video_*/pose_video_XX.avi`, dan K/D dari langkah 1
- **Keluaran:** `data/processed/virtual_encoder/<CSV_PREFIX>_XX.csv` —
  kolom `Frame, Waktu (detik), X Posisi (mm), Y Posisi (mm), Reprojection Error (px)`
- **Parameter:** atur `KALIBRASI_VIDEO` (folder video) dan `KALIBRASI_CSV_PREFIX`
  (nama berkal CSV keluaran) di `config_paths.py`. Kombinasi yang menghasilkan artefak
  penelitian (dinyatakan pemilik penelitian):

| Folder video di repo | Nama asli | Isi | Prefiks CSV keluaran |
|---|---|---|---|
| `video_baseline_x` | `BASELINE_JALUR_FINAL_VIDEO` | video pengujian **circular baseline** | `hasil_fix_banget_baseline` |
| `video_calibrated_x` | `KALIBRASI_JALUR_FINAL_VIDEO_3` | video pengujian **circular hasil kalibrasi** | `JALUR_VIDEO_FINAL_3` |
| `video_kalibrasi_x` | `KALIBRASI_X_VIDEO_BENERAN` | 3 video sumbu X | `KALIBRASI_X_VIDEO_FINAL_BENERAN` |
| `video_baseline_y`, `video_calibrated_y` | `..._BGT_BGT` | video sumbu Y | `..._BGT_BGT` |

> **JANGAN dijalankan kecuali perlu.** Video berukuran ~30-46 MB per berkas; total
> 1.7 GB untuk 37 berkas. Memproses satu video butuh waktu lama, dan **tidak perlu**
> untuk sekadar mereproduksi hasil penelitian: CSV lintasan yang dibutuhkan langkah 4
> sudah tersedia di `data/raw/circular_baseline/` dan `data/raw/circular_calibrated/`.
> Virtual encoder hanya perlu dijalankan ulang kalau Anda punya video lintasan baru.

- **Catatan:** sel terakhir membuat gambar perbandingan ke `figures/`.

### Langkah 4 — evaluasi lintasan

`04_trajectory_evaluation/evaluasi_lintasan.ipynb`

- **Masukan:** `data/raw/circular_baseline/hasil_fix_banget_baseline_XX.csv` dan
  `data/raw/circular_calibrated/JALUR_VIDEO_FINAL_3_XX.csv`
- **Proses:** bangkitkan ground truth 2 elips, cari tetangga terdekat tiap titik
  dengan `cKDTree`, hitung RMSE per sumbu dan total (µm)
- **Keluaran:** gambar evaluasi ke `figures/`, dan tabel ringkasan di layar
- **Hasil yang diharapkan:** baseline 100.89 µm -> terkalibrasi 46.17 µm, perbaikan **54.24 %**
- **Waktu:** ~15 detik

### Langkah 5 — measurement error (perbandingan dengan dial gauge)

Eksperimen ini membandingkan pembacaan metode ini (*virtual encoder*) dengan **dial gauge**.
Konfigurasi: parameter baseline semua, **jarak gerak diperkecil ke 0.5 mm**, 5 iterasi per
panel (maju dan balik, sumbu X dan Y).

```bash
python 06_measurement_error/plot_measurement_error.py
```

- **Masukan:** `data/processed/measurement_error/dial_vs_ve.csv`
  (foto dial gauge-nya di `data/raw/measurement_error/x_dial_gauge/` dan `y_dial_gauge/`)
- **Keluaran:** `figures/1_4_position_comparison_combined.png` (+ `.pdf`) dan tabel MAE di layar
- **Hasil yang diharapkan** (selisih absolut rata-rata |VE - dial|):

  | Panel | MAE | std |
  |---|---|---|
  | X Forward | 4.62 µm | 4.32 µm |
  | Y Forward | 8.54 µm | 7.77 µm |
  | X Backward | 5.30 µm | 2.54 µm |
  | Y Backward | 7.08 µm | 4.94 µm |
  | **Gabungan X** | **4.96 µm** | 3.36 µm |
  | **Gabungan Y** | **7.81 µm** | 6.18 µm |

  Dial gauge punya resolusi ±10 µm, jadi selisih di orde 5-8 µm berada di dalam
  ketelitian alat ukurnya.
- **Waktu:** ~5 detik. Gambar keluarannya identik dengan gambar naskah (2584x2134 px).

## 7. Menyesuaikan dengan mesin/kamera baru

1. Cetak papan kalibrasi: `python 05_akuisisi_alat/buat_papan_catur.py`
   (A4, grid 8x8 kotak 20 mm, 3 lingkaran penanda penentu origin).
2. Foto papan dari banyak sudut dengan `05_akuisisi_alat/capture_kalibrasi_kamera.py`
   (tombol `f`). Sebaiknya **jauh lebih dari 10 citra**, dan variasi kemiringan/posisi
   yang lebar.
3. Jalankan langkah 1 di atas. **K, D, dan nilai RMSE reprojection akan berbeda dari
   penelitian ini** — itu memang begitu, karena kamera dan posisi pemasangannya beda.
   Yang perlu sama hanyalah urutan tahapannya, bukan angkanya. Hal yang sama berlaku
   kalau Anda memakai dataset kalibrasi alternatif (mis. `measurement_error/x_camera_calibration`).
4. Ambil dataset linear dengan `05_akuisisi_alat/otomasi_pengujian_linear.py`
   (ubah `COM10` -> port Anda, `TEST_MODE`, parameter awal 80/80/0/0).
5. Jalankan langkah 2 -> Anda dapat nilai `M92`/`M425`/`M852` baru.
6. Masukkan nilai itu ke `05_akuisisi_alat/otomasi_lintasan_elips.py`, ambil video
   lintasan, lalu lanjut langkah 3 dan 4.

## 8. Batasan yang harus Anda ketahui (jujur, belum lengkap)

Hal-hal berikut **tidak** terselesaikan di penataan ini dan perlu keputusan pemilik penelitian:

1. **Nama folder kalibrasi menyesatkan: `dataset_kalibrasi_fix_prime_260` berisi 10 citra,
   bukan 260.** Ini **bukan masalah untuk reproduksi** — K/D dari 10 citra itu sudah
   mereproduksi seluruh angka naskah (bagian 4). Dicatat hanya supaya Anda tidak mencari
   "sisa 250 citra" yang mungkin memang tidak pernah ada. Kalau naskah menyebut jumlah
   citra kalibrasi secara eksplisit, angka itulah yang perlu dicocokkan.
2. **Jejak pembuat `hasil_fix_banget_baseline_XX.csv` tidak tersimpan di kode.**
   Menurut pemilik penelitian, CSV baseline ini dihasilkan oleh **kode yang sama**
   (`virtualencodervideo`), hanya berbeda **video masukan** (`BASELINE_JALUR_FINAL_VIDEO`)
   dan **path CSV keluaran**. Di kode yang tersisa, tidak ada notebook yang menulis nama
   berkas itu — semua hanya membacanya (dikonfirmasi dengan pencarian ke seluruh notebook).
   Jadi jalur baseline dan jalur terkalibrasi memakai skrip yang sama, dan yang berbeda
   hanya parameter di kepala skrip. Di repo ini keduanya sudah disatukan lewat
   `config_paths.py`: `KALIBRASI_VIDEO` dan `KALIBRASI_CSV_PREFIX`.
4. **Skrip akuisisi belum diparameterisasi.** Isinya masih nilai asli penelitian
   (port `COM10`, indeks kamera, eksposur). Lihat tabel di `05_akuisisi_alat/README.md`.
5. **`measurement_error` butuh mode 0.5 mm**: saat mengolahnya, `EXPECTED_DELTA` harus
   0.5 (sudah ditangani otomatis lewat `RUN_MODE=measurement_error`).

## 9. Yang tervalidasi vs belum

| Bagian | Status |
|---|---|
| Kalibrasi kamera (tahap 1) | dijalankan ulang dari data di repo, berhasil, menulis 4 CSV |
| Kalibrasi mesin (tahap 2, mode `calibrated`) | dijalankan ulang, **identik digit-per-digit** dengan log naskah |
| Evaluasi lintasan (tahap 4) | dijalankan ulang, berhasil, perbaikan 54.24 % |
| Virtual encoder (tahap 3) | bootstrap + pemuatan K/D dari CSV diuji, berhasil. **Pemrosesan video sengaja tidak dijalankan** — videonya 1.7 GB dan grafnya sudah tidak diperlukan karena CSV lintasan tersedia |
| Measurement error (dial gauge vs VE) | dijalankan ulang, berhasil, gambar keluaran **identik** dengan gambar naskah (2584x2134 px) |
| Kalibrasi mesin mode `baseline` dan `measurement_error` | belum dijalankan ulang — datasetnya lengkap, tinggal ganti `KALIBRASI_MODE` |
| Skrip akuisisi (folder 05) | tidak dapat dijalankan tanpa mesin |

---

## 10. Kalau ada yang tidak jalan

| Gejala | Penyebab paling mungkin |
|---|---|
| `config_paths.py tidak ditemukan` | notebook dijalankan dari luar folder repo. Jalankan lewat Jupyter di folder notebooknya, atau set `KALIBRASI_REPO` ke akar repo |
| `Tidak ditemukan: .../camera_calibration/camera_matrix.csv` | tahap 1 (kalibrasi kamera) belum dijalankan sampai sel ekspor selesai |
| `TIDAK DITEMUKAN` di keluaran `python config_paths.py` | dataset belum ada di `data/raw/`; taruh sesuai `data/MANIFEST.md` |
| Banyak sampel "pose tidak ditemukan" | pencahayaan/eksposur berbeda dari waktu pengambilan data, atau papan tidak seluruhnya masuk frame |
| `ModuleNotFoundError: cv2` lalu `has no attribute 'ximgproc'` | yang terpasang `opencv-python`, bukan `opencv-contrib-python` |
| Kalibrasi kamera menghasilkan K/D yang jauh berbeda | jumlah citra kalibrasi hanya 10 (lihat bagian 8 butir 1) |
