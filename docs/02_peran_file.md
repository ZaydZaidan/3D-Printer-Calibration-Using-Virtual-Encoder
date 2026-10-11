# Peran Setiap File — Hasil Konfirmasi

Diisi bertahap sambil penulis menunjuk file mana yang benar-benar dipakai.
Status: **terkonfirmasi** = dinyatakan langsung penulis; **dugaan** = disimpulkan dari isi
kode/nama dataset; **belum** = menunggu penunjukan.

---

## 1. `capturedatasetbiasa.py` — TERKONFIRMASI

**Peran:** hanya untuk **mengambil dataset foto papan catur** sebagai bahan kalibrasi kamera.
Tujuannya: mendapatkan **matriks intrinsik dan koefisien distorsi kamera** (profiling kamera).

Pernyataan penulis:

> "dulu saya pakainya yang capturedatasetbiasa buat ngambil gambar dataset chessboard untuk
> kalibrasi camera. saya cuman pake f capture foto."

| Tombol | Fungsi di kode | Dipakai? |
|---|---|---|
| `f` | Simpan ke `dataset_sesi_<timestamp>/kalibrasi/calib_XXXX.png` | **YA** |
| `g` | Rekam video `pose_video_XX.avi` | **TIDAK** |
| `q` | Keluar | ya |

Konsekuensi: semua logika video di file ini (`vid_counter`, `VideoWriter`) tidak relevan.
Dataset video berasal dari `otomasilintasan.py` — lihat bagian 3.

Rantai pemakaian:

```
capturedatasetbiasa.py (tombol f)          -> calib_XXXX.png
        v
kalibrasi_kamera.ipynb (dulu kalibrasisesuaipaper.ipynb sel 0-5)
        -> K (intrinsik) + D (distorsi) + RMSE reprojection
        v
dipakai ulang oleh virtual encoder untuk solvePnP per frame
```

## 2. `otomasikalibrasi.py` — TERKONFIRMASI

**Peran:** mengambil dataset **pengujian linear** untuk kalibrasi mesin. Dijalankan **dua kali**:

| Run | Parameter | Dataset hasil | Notebook pengolah |
|---|---|---|---|
| Baseline | backlash 0, skew 0, steps/mm 80 (X dan Y) | `BASELINE_X_INDIVIDUAL` (X), `BASELINE_Y_FIX_METHOD` (Y) | `kalibrasi_mesin.ipynb` sel X / Y |
| Setelah kalibrasi | steps/mm 79.72 (X) / 80.40 (Y) | `X_LAST_FIX` (X), `Y_LAST_FIX` (Y) | idem, ganti `base_path` + `CURRENT_STEPS_MM` |
| Measurement error | baseline semua, **jarak gerak 0.5 mm** | `systematic_error_x`, `systematic_error_Y` | bandingkan dengan dial gauge |

Nilai parameter terbaca langsung di kode, baris 10-26:
blok terkomentari (baris 10-17) berisi nilai **hasil kalibrasi**, blok aktif (baris 19-26)
berisi nilai **baseline**.

`fwd_move` per mode menentukan jarak gerak:
`X+`/`Y+` = **0.5 mm** (dipakai untuk measurement error),
`X-`/`Y-` = 10 mm (pengujian linear normal, dan nilai yang cocok dengan
`EXPECTED_DELTA = 10` di notebook).

**Keluaran:** `dataset_<Xpos|Xneg|Ypos|Yneg>_sesi_<timestamp>/kalibrasi/`
berisi `oriy{i}.png`, `fwd{i}.png`, `bck{i}.png` (i = 1..40).

## 3. `otomasilintasan.py` — TERKONFIRMASI

**Peran:** menjalankan **lintasan elips** di mesin sambil merekam video, dipakai dua kali
(parameter baseline, lalu parameter hasil kalibrasi).

- Parameter kalibrasi ada di baris 15-21 (`BACKLASH_X`, `BACKLASH_Y`, `SKEW_X_ON_Y`,
  `SKEW_Y_ON_X`, `STEPX`, `STEPY`) — nilai inilah yang dimasukkan dari rekomendasi
  `kalibrasi_mesin.ipynb`.
- `TOTAL_ITERASI = 10` -> 10 video per sesi.
- `precompute_ellipse_commands()` membangkitkan gcode elips (lihat bagian 5).
- Di `cnc_worker_thread` baris 235 nilai `STEPX`/`STEPY` dikirim sebagai `M92`.
- **Keluaran:** `dataset_otomatis_sesi_<timestamp>/video/pose_video_XX.avi`
  (prefix `dataset_otomatis_sesi_` inilah penanda file ini, bukan file capture lain).

> Catatan: file ini hanya menyimpan konfigurasi **hasil kalibrasi**. Konfigurasi baseline
> tidak tersimpan di kode, hanya terekam di datasetnya.

## 4. `virtualencodervideo copy 2.ipynb` — TERKONFIRMASI (mata rantai yang sempat terlewat)

**Peran:** mengubah video lintasan **hasil kalibrasi** menjadi CSV lintasan.
Bukan sekadar salinan eksperimen — dia bagian dari rantai final.

- Sel 6: `VIDEO_PATH = ...\KALIBRASI_JALUR_FINAL_VIDEO_3\video\pose_video_XX.avi`
- `CSV_OUTPUT_PATH = f"JALUR_VIDEO_FINAL_3_{video_index:02d}.csv"` -> dibaca
  `evaluasilintasan.ipynb`.

Rantai lengkap:

```
otomasilintasan.py -> KALIBRASI_JALUR_FINAL_VIDEO_3/video/pose_video_XX.avi
        v
virtualencodervideo copy 2.ipynb (sel 6)
        -> JALUR_VIDEO_FINAL_3_XX.csv
        v
evaluasilintasan.ipynb (sel 1 & 4)
```

Untuk baseline, jalur yang sama berujung pada `hasil_fix_banget_baseline_XX.csv`
(sumber: `BASELINE_JALUR_FINAL_VIDEO`), tetapi **tidak ada notebook di folder yang menulis
nama file itu** — kemungkinan hasil rename manual. Perlu dikonfirmasi.

## 5. Catatan konsep: soal "ekstrinsik"

Di pipeline ini **tidak ada satu matriks ekstrinsik tetap** (transformasi kamera -> mesin):

- `cv2.calibrateCamera()` mengembalikan `rvecs`/`tvecs` yang merupakan **pose papan terhadap
  kamera untuk setiap citra kalibrasi** (dipakai untuk menghitung RMSE), bukan transformasi
  tetap.
- Kalibrasi mesin dan virtual encoder menghitung pose **ulang per citra/frame** dengan
  `cv2.solvePnP`. Lintasan didapat dari **selisih** `tvec` terhadap `tvec` frame origin.

Kalimat yang aman untuk naskah/repo: kalibrasi kamera menghasilkan **intrinsik (K) dan
koefisien distorsi (D)**; posisi diperoleh **per frame** melalui `solvePnP` dan dinyatakan
**relatif** terhadap frame awal.

## 6. Anomali & pertanyaan terbuka

1. `dataset_kalibrasi_fix_prime_260` hanya berisi **10 gambar** walau namanya menyiratkan 260,
   padahal notebook memakainya sebagai `FOLDER_PATH`.
2. `dataset_kalibrasi_ditambah` (97 file, pola `oriy/fwd/bck`) — dipakai untuk bagian mana?
   Kandidat: `PLOT_GABUNGAN_X_DITAMBAHDATASET.png`, `JALUR_DATASET_DITAMBAH_01.csv`.
3. FPS tidak konsisten di `capturedatasetbiasa.py`: baris 29 minta 60 FPS, baris 109
   `VideoWriter` 120.0 FPS. Tidak berdampak (tombol `g` tidak dipakai) tapi perlu dibetulkan
   sebelum rilis.
4. Overlay layar di kedua skrip capture menulis `"REC 120FPS"` secara hardcode.

## 7. Status seluruh file

| # | File | Status | Peran |
|---|---|---|---|
| 17 | `capturedatasetbiasa.py` | terkonfirmasi | Akuisisi citra papan catur untuk kalibrasi kamera (tombol `f`) |
| 16 | `otomasikalibrasi.py` | terkonfirmasi | Akuisisi dataset pengujian linear (baseline / setelah kalibrasi / measurement error) |
| 15 | `otomasilintasan.py` | terkonfirmasi | Jalankan lintasan elips + rekam video; parameter baseline dan terkalibrasi |
| 9 | `kalibrasicamera\virtualencodervideo copy 2.ipynb` | terkonfirmasi | Video lintasan terkalibrasi -> `JALUR_VIDEO_FINAL_3_XX.csv` |
| 1 | `kalibrasicamera\kalibrasisesuaipaper.ipynb` | terkonfirmasi | Dipecah jadi `kalibrasi_kamera.ipynb` + `kalibrasi_mesin.ipynb` |
| 2 | `kalibrasicamera\virtualencodervideo.ipynb` | terkonfirmasi | Virtual encoder (video -> lintasan) |
| 11 | `kalibrasicamera\evaluasilintasan.ipynb` | terkonfirmasi | Evaluasi RMSE lintasan vs ground truth |
| 18 | `capturedatasetpengujianfoto.py` | belum dipakai (dugaan) | Akuisisi triplet `oriy/fwd/bck`; tapi penulis menyebut `otomasikalibrasi.py` yang dipakai |
| — | `After Lulus Paper/code/plotmeasurement.py` | terkonfirmasi | Perbandingan dial gauge vs virtual encoder (measurement error). Dipindahkan ke `06_measurement_error/plot_measurement_error.py` |
| — | `Semester 8/.../images/Hasil/Kalibrator_x`, `Kalibrator_y` | terkonfirmasi | 15 foto dial gauge per sumbu (5 triplet `ori/fwd/bck`) untuk eksperimen measurement error |
| — | 22 file lainnya | belum | Menunggu penunjukan penulis |

## 8. Catatan: dua jalur CSV lintasan dari satu skrip

Sisi **terkalibrasi** (`JALUR_VIDEO_FINAL_3_XX.csv`) jelas dihasilkan
`virtualencodervideo copy 2.ipynb` sel 6. Sisi **baseline**
(`hasil_fix_banget_baseline_XX.csv`) menurut pemilik penelitian dihasilkan oleh
**kode yang sama**, hanya berbeda video masukan dan path CSV keluaran.

Pencarian ke seluruh notebook di `SEMPRO/Code/` mengonfirmasi tidak ada notebook lain
yang **menulis** nama `hasil_fix_banget_baseline_*` — semuanya hanya membacanya.
Jadi penjelasan tersebut konsisten dengan kode; yang tidak tersimpan hanyalah versi
skrip dengan path keluaran yang sudah diubah.

Di repo ini keduanya disatukan lewat `config_paths.py`: `KALIBRASI_VIDEO`
(folder video) + `KALIBRASI_CSV_PREFIX` (nama berkas CSV keluaran).
