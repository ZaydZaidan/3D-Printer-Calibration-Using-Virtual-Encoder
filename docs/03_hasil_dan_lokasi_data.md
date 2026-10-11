# Hasil Penelitian & Lokasi Data Final

## 1. Lokasi data final

> Dinyatakan penulis: *"data fix dari penelitian saya yang saya pakai itu ada di
> `Kuliah/After Lulus Paper/Data`"*

**Rujukan final = `After Lulus Paper/Data/`.** Folder `Semester 7/SEMPRO/Code/` berisi
salinan kerja + arsip eksperimen dan **tidak** dipakai sebagai rujukan.

### 1.1 Pemetaan dataset — TERKONFIRMASI penulis

| Nama di repo (baru) | Nama asli | Sumbu | Kondisi | File | Ukuran |
|---|---|---|---|---|---|
| `linear_baseline_x/` | `BASELINE_X_INDIVIDUAL` | X | **baseline** linear | 120 | 22 MB |
| `linear_baseline_y/` | `BASELINE_Y_FIX_METHOD` | Y | **baseline** linear | 120 | 22 MB |
| `linear_calibrated_x/` | `X_LAST_FIX` | X | **setelah kalibrasi** | 120 | 22 MB |
| `linear_calibrated_y/` | `Y_LAST_FIX` | Y | **setelah kalibrasi** | 120 | 21 MB |
| `measurement_error/x_camera_calibration/` | `kalibrator_systematic_error_x` | X | dataset kalibrasi kamera sesi measurement error | 54 | 11 MB |
| `measurement_error/x_machine_movement/` | `systematic_error_x` | X | pergerakan mesin, 0.5 mm, baseline | 120 | 24 MB |
| `measurement_error/y_camera_calibration/` | `kalibrator_systematic_y` | Y | dataset kalibrasi kamera sesi measurement error | 31 | 5.4 MB |
| `measurement_error/y_machine_movement/` | `systematic_error_Y` | Y | pergerakan mesin, 0.5 mm, baseline | 120 | 21 MB |
| `circular_baseline/` | `Circular Baseline` | XY | lintasan elips, baseline | 20 | 4.1 MB |
| `circular_calibrated/` | `Circular Kalibrasi` | XY | lintasan elips, terkalibrasi | 33 | 8.2 MB |
| `camera_calibration/dataset_kalibrasi_fix_prime_260/` | `dataset_kalibrasi_fix_prime_260` | - | citra kalibrasi kamera | 10 | kecil |
| `camera_calibration/dataset_kalibrasi_ditambah/` | `dataset_kalibrasi_ditambah` | - | citra kalibrasi tambahan | 97 | ~20 MB |

Rincian + status git per dataset: `data/MANIFEST.md`.

### 1.2 Pemetaan nama berkas hasil

| Nama di `SEMPRO/Code/` | Nama di `After Lulus Paper/Data/` |
|---|---|
| `kalibrasicamera/DATA FIX/hasil_fix_banget_baseline_XX.csv` | `Circular Baseline/hasil_fix_banget_baseline_XX.csv` |
| `kalibrasicamera/JALUR_VIDEO_FINAL_3_XX.csv` | `Circular Kalibrasi/JALUR_VIDEO_FINAL_3_XX.csv` |

Dasar: `evaluasilintasan.ipynb` membaca kedua pola nama itu (sel 0 -> baseline, sel 1 & 4 -> kalibrasi).

Kedua CSV itu dihasilkan oleh **kode yang sama** (`virtualencodervideo`), hanya berbeda
video masukan dan path CSV keluaran (dinyatakan pemilik penelitian). Di kode yang tersisa
tidak ada notebook yang menulis nama `hasil_fix_banget_baseline_*` — semuanya hanya membaca.
Di repo ini perbedaan itu sudah disatukan lewat `KALIBRASI_VIDEO` + `KALIBRASI_CSV_PREFIX`
di `config_paths.py`:

| Video masukan | Prefiks CSV keluaran |
|---|---|
| `video_baseline_x` (`BASELINE_JALUR_FINAL_VIDEO`) | `hasil_fix_banget_baseline` |
| `video_calibrated_x` (`KALIBRASI_JALUR_FINAL_VIDEO_3`) | `JALUR_VIDEO_FINAL_3` |

---

## 2. Parameter awal (baseline) dan akhir

`otomasikalibrasi.py` baris 19-26 — konfigurasi **baseline**:

| Parameter | Nilai baseline |
|---|---|
| `BACKLASH` (kompensasi) | 0 |
| `SKEW_FACTOR` | 0 |
| `STEPX` | 80 |
| `STEPY` | 80 |

Blok terkomentari di baris 10-17 memuat nilai **hasil kalibrasi** yang kemudian dipakai:
backlash 0.0133 (X), skew 0.009213, steps/mm 79.72 (X) dan 80.40 (Y).

---

## 3. Hasil pengujian linear (sumbu X dan Y)

Target pergerakan **10 mm** per sumbu, 10 sampel valid dari 40 percobaan,
ambang penolakan RMSE 0.2 px.

### 3.1 Baseline

| Metrik | Sumbu X | Sumbu Y |
|---|---|---|
| Rata-rata perpindahan sumbu gerak | 10.0463 mm (std 0.0072) | -9.9450 mm (std 0.0108) |
| Rata-rata error sumbu gerak | **0.0463 mm** | **0.0550 mm** |
| Rata-rata drift sumbu tegak lurus | -0.0937 mm (std 0.0089) | -0.0898 mm (std 0.0054) |
| Rata-rata RMSE reprojection | 0.1137 px (std 0.0178) | 0.1178 px (std 0.0190) |
| Sampel ditolak / gagal | 16 dari 40 | 28 dari 40 |

**Rekomendasi firmware hasil baseline:**

| | Sumbu X | Sumbu Y |
|---|---|---|
| Steps/mm awal | 80.0000 | 80.0000 |
| Steps/mm baru | **79.6314** (`M92 X79.63`) | **80.4425** (`M92 Y80.44`) |
| Backlash | 0.0124 mm (`M425 X0.0124`) | 0.0244 mm (`M425 Y0.0244`) |
| Skew | -0.009327 (-0.5344 derajat) | 0.009025 (0.5171 derajat) |

### 3.2 Setelah kalibrasi

Dijalankan ulang dengan steps/mm X = 79.72 dan Y = 80.40.

| Metrik | Sumbu X | Sumbu Y |
|---|---|---|
| Rata-rata perpindahan sumbu gerak | 10.0045 mm (std 0.0079) | -10.0022 mm (std 0.0071) |
| Rata-rata error sumbu gerak | **0.0071 mm** | **0.0054 mm** |
| Rata-rata drift sumbu tegak lurus | 0.0043 mm (std 0.0058) | 0.0036 mm (std 0.0053) |
| Rata-rata RMSE reprojection | 0.1186 px (std 0.0151) | 0.1281 px (std 0.0168) |
| Sampel ditolak / gagal | 9 dari 40 | 10 dari 40 |

**Rekomendasi lanjutan (sisa error):**

| | Sumbu X | Sumbu Y |
|---|---|---|
| Steps/mm saat itu | 79.7200 | 80.4000 |
| Steps/mm baru | 79.6845 | 80.3826 |
| Backlash | 0.0068 mm | 0.0068 mm |
| Skew | 0.000427 -> sudah siku, tanpa kompensasi | 0.000362 -> sudah siku |

### 3.3 Perbaikan baseline -> terkalibrasi

| Metrik | Baseline | Setelah kalibrasi | Perbaikan |
|---|---|---|---|
| Error sumbu X | 0.0463 mm | 0.0071 mm | **84.7 %** |
| Error sumbu Y | 0.0550 mm | 0.0054 mm | **90.2 %** |
| Drift Y saat gerak X | 0.0937 mm | 0.0043 mm | **95.4 %** |
| Drift X saat gerak Y | 0.0898 mm | 0.0036 mm | **96.0 %** |

---

## 4. Measurement error (sebelumnya bernama "systematic error")

> Pernyataan penulis: *"saya menghitung measurement error dengan cara saya bandingin
> pembacaan metode saya dengan dial gauge. nah itu kalo di folder tulisannya systematic
> error. nanti anda rename aja buat yang baru namanya measurement error. itu ada kalibrator
> dan systematic error untuk masing-masing sumbu. kalibrator itu kayak dataset buat kalibrasi
> kameranya dan yang pure systematic error itu hasil pergerakan mesinnya dari proses otomasi
> kalibrasi tapi jarak geraknya dikecilin jadi 0.5mm dan parameternya pakai baseline semua"*

**Tujuan:** memvalidasi akurasi absolut pembacaan metode ini dengan membandingkannya
terhadap **dial gauge** (alat ukur referensi).

**Konfigurasi:** seluruh parameter baseline (backlash comp 0, skew comp 0, steps/mm 80)
dengan **jarak gerak diperkecil menjadi 0.5 mm**.

**Konsekuensi di kode:** inilah alasan `otomasikalibrasi.py` mode `X+` dan `Y+` memakai
`fwd_move = (0.5, 0.0)` / `(0.0, 0.5)`. Saat mengolah dataset ini di notebook kalibrasi
mesin, `EXPECTED_DELTA_X` / `EXPECTED_DELTA_Y` **harus diubah ke 0.5**, bukan 10.

**Penamaan baru:** `systematic_error_*` -> `measurement_error/*`.
`kalibrator_*` = dataset kalibrasi kamera untuk sesi ini; `*_machine_movement` = hasil
pergerakan mesinnya.

### 4.1 Hasil perbandingan dengan dial gauge

Sumber angka: `After Lulus Paper/code/plotmeasurement.py` (kini dipindahkan ke
`06_measurement_error/plot_measurement_error.py`, datanya dipisah ke
`data/processed/measurement_error/dial_vs_ve.csv`).

Satuan mikron. Dial gauge dibaca konstan di 5 iterasi, dengan ketelitian alat **±10 µm**.

| Panel | Dial gauge | Virtual Encoder (5 iterasi) | MAE | std |
|---|---|---|---|---|
| X Forward | 505.0 | 504.9 / 507.0 / 494.7 / 497.0 / 502.3 | 4.62 | 4.32 |
| Y Forward | 480.0 | 480.1 / 481.6 / 498.6 / 489.4 / 493.0 | 8.54 | 7.77 |
| X Backward | 10.0 | 11.2 / 5.1 / 16.8 / 17.8 / 15.8 | 5.30 | 2.54 |
| Y Backward | 20.0 | 4.9 / 23.0 / 24.7 / 11.5 / 15.9 | 7.08 | 4.94 |
| **Gabungan X** | | (10 pengukuran) | **4.96** | 3.36 |
| **Gabungan Y** | | (10 pengukuran) | **7.81** | 6.18 |

MAE = rata-rata |VE - dial|, sama dengan label "Mean Diff" pada legenda gambar naskah.
Selisih 5-8 µm berada di dalam resolusi dial gauge (±10 µm), jadi metode ini konsisten
dengan alat ukur referensi.

### 4.2 Berkas terkait

| Berkas | Isi |
|---|---|
| `data/processed/measurement_error/dial_vs_ve.csv` | 20 baris: axis, frame, iteration, dial_um, dial_err_um, ve_um, abs_diff_um |
| `data/raw/measurement_error/x_dial_gauge/` | 15 foto dial gauge sumbu X (`orix/fwd/bck` 1-5) + 3 gambar visualisasi |
| `data/raw/measurement_error/y_dial_gauge/` | 15 foto dial gauge sumbu Y (`oriy/fwd/bck` 1-5) + 3 gambar visualisasi |
| `figures/1_4_position_comparison_combined.png` | gambar naskah, 4 panel |

---

## 5. Provenance nilai kalibrasi — TERJAWAB: itu hasil *fine-tuning*, bukan salah salin

**Pertanyaan yang dulu terbuka:** nilai yang dipakai di kode (79.72 / 80.40 / 0.0133 /
0.009213) tidak sama dengan yang direkomendasikan log baseline (79.6314 / 80.4425 /
0.0124 / 0.009025). Mana yang benar?

**Jawaban:** keduanya benar dan memang berbeda. Log baseline mencatat **nilai baseline
serta rekomendasi putaran pertama**, sedangkan kode memuat **nilai final setelah
fine-tuning**. Naskah **sengaja hanya menyajikan dua titik itu** (baseline dan final);
rantai iterasi di antaranya tidak dimasukkan ke naskah — jadi tidak ada yang kurang
di naskah, dan tidak ada yang salah di kode.

Sumber otoritatifnya ada di naskah: Tabel *"Parameter Hasil Kalibrasi Fine Tuning"*
(`tab:parameter_final_kalibrasi`, `mainmatter/bab4.tex` baris 695-716):

| Parameter | Nilai final (naskah) | Ekuivalen di kode |
|---|---|---|
| `STEPX` | 79,72 steps/mm | `STEPX = 79.72` |
| `STEPY` | 80,40 steps/mm | `STEPY = 80.40` |
| `BACKLASH_X` | 13,3 µm | `BACKLASH_X = 0.0133` mm |
| `BACKLASH_Y` | 31,4 µm | `BACKLASH_Y = 0.0244 + 0.0070` = 0.0314 mm |
| `SKEW_X_ON_Y` | -9,2 µm/mm | `SKEW_X_ON_Y = -0.009200` |
| `SKEW_Y_ON_X` | 9,213 µm/mm | `SKEW_Y_ON_X = 0.009213` |

Naskah (bab4.tex baris 693) menjelaskan tahapannya: setelah steps/mm dan backlash
diaplikasikan, dilakukan **fine-tuning** dengan mengulang pembaruan parameter berdasarkan
persamaan rekomendasi sampai mesin mencapai *steady-state*.

### 5.1 Artefak kerja iterasi fine-tuning di ARSIP (di luar naskah, hanya penjelas)

Iterasi antaranya tidak ditampilkan di naskah, tetapi **datasetnya masih ada** di
`SEMPRO/Code/ARSIP` (bertanggal 5 Mei 2026). Ini yang menjelaskan asal angka final
79.72 / 80.40 — bukan tebakan, tapi jejak run yang benar-benar dikerjakan:

| Folder ARSIP | Berkas | Menyiratkan |
|---|---|---|
| `kalibrasi_x_step80.11_skew0_5_may_2026` | 87 | steps 80.11, skew 0 |
| `kalibrasi_x_step80.11_skew+0.0128_5_may_2026` | 93 | steps 80.11, skew +0.0128 |
| `kalibrasi_x_step80.11_skew-0.0123_...`, `skew-0.0128_...` | — | steps 80.11, skew negatif |
| `kalibrasi_x_stepdoang_8013_5_may_2026` | 61 | uji steps 80.13 saja |
| `kalibrasi_x_skewfactorx2_5_may_2026` | 60 | uji skew factor 2x |
| `dataset_setelah_kalibrasi_step_x_1`, `_x_2`, `_y_1`..`_y_4` | — | iterasi steps per sumbu |
| `KALIBRASI_X_STEPBACK_1_FIX_METHOD`, `STEPBACK_2_FIX_METHOD` | 120 | iterasi *stepback* |
| `KALIBRASI_X_SKEW_1_FIX`, `SKEW_2_FIX`, `KALIBRASI_Y_SKEW_1_FIX` | 120 | iterasi skew |
| `dataset_jalur_setelah_kalibrasi_step_backlash_skew_feedrate_{500,1000,2000,3000}` | — | uji feedrate |
| `X_LAST_FIX/KALIBRASI_X_FINETUNING/kalibrasi` | 120 | data fine-tuning terakhir |

### 5.2 Kenapa tetap perlu dicatat di repo

Orang yang menurunkan sendiri kalibrasi dari **dataset baseline yang tersimpan** akan
mendapat **79.6314**, bukan 79.72. Itu **bukan** kesalahan: 79.6314 adalah rekomendasi
putaran pertama, sedangkan 79.72 adalah hasil akhir setelah beberapa putaran fine-tuning.
Repo ini memakai 79.72 / 80.40 karena itulah yang menghasilkan angka pada naskah
(dibuktikan: mode `calibrated` mereproduksi log secara identik).

Rantai lengkapnya: `80.00` (baseline) -> 79.6314 (rekomendasi putaran 1, log tersimpan)
-> iterasi di ARSIP (80.13 / 80.11 / varian skew; **tidak masuk naskah**) -> **79.72**
(final, naskah + kode). Naskah hanya menampilkan ujung-ujungnya, dan itu sudah cukup
untuk naskah; catatan ini semata supaya pembaca repo tidak menyangka 79.6314 itu salah.

## 6. Yang belum ada di repo

Matriks intrinsik `K` dan koefisien distorsi `D` belum pernah disimpan sebagai berkas —
hanya tercetak di layar. Notebook hasil pemisahan
(`01_camera_calibration_paper/kalibrasi_kamera.ipynb`) sekarang mengekspornya ke
`output/camera_params.npz` supaya bisa dirujuk dan dipakai notebook kalibrasi mesin.
