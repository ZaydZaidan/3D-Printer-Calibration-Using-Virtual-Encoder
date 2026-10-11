# Audit & Rencana Penataan Kode

Sumber: `Semester 7/SEMPRO/Code/kalibrasicamera` (+ beberapa file .py di `Code/`).
Tanggal audit: 12 Oktober 2026.

## 1. Notebook yang Dipakai (final)

| File sumber | Ukuran | Jumlah sel | Catatan |
|---|---|---|---|
| `kalibrasicamera/kalibrasisesuaipaper.ipynb` | 3.4 MB | 12 | Implementasi pipeline sesuai paper + rekomendasi firmware X & Y |
| `kalibrasicamera/virtualencodervideo.ipynb` | 766 KB | 12 | Kalibrasi kamera (duplikat) + virtual encoder & plot |
| `kalibrasicamera/evaluasilintasan.ipynb` | 40 KB | 5 | Ground truth elips + RMSE baseline vs kalibrasi |

### Notebook lain di folder `Code/` (bukan inti, tapi terkait)

- `KALIBRASI_SESUAI_PAPER_DAN_VIRTUALENCODER_FOTO.ipynb` — versi berbasis foto (bukan video)
- `VIRTUALENCODER_VIDEOPROCESSING.ipynb` — versi lebih awal dari virtual encoder video
- `virtualencodervideo copy.ipynb`, `copy 2/3/4.ipynb` — salinan eksperimen
- `tulispaper_kalibrasi.ipynb` — notebook penulisan naskah
- `animasiplot.ipynb`, `datalintasan.ipynb`, `regresibaseline.ipynb`, `debuggingcirle.ipynb`, `CLAHEdanGAUSSIANBLUR.IPYNB`
- Skrip utilitas: `virtualencoder.py`, `otomasikalibrasi.py`, `otomasilintasan.py`,
  `capturedatasetbiasa.py`, `capturedatasetpengujianfoto.py`, `linescreeningparameter.py`,
  `distorsikamera.py`, `distorsikameravisualisasisim.py`, `cekfps.py`, `plotpergerakancapturedata.py`,
  `alasantetatidaksimetris.py`, `Chessboard_generator.py`, `jalaninrepetierhost.py`

Keputusan yang perlu diambil: mana yang ikut ke repo publik, mana yang diarsipkan.

## 2. Masalah yang Ditemukan

### 2.1 Path absolut hardcoded (paling menghambat)
Setiap notebook memakai path `C:\Users\zaydz\Documents\Onedrive Kuliah\...` secara literal,
minimal di titik berikut:

- `FOLDER_PATH` dataset kalibrasi
- `base_path` dataset `X_LAST_FIX` / `Y_LAST_FIX` (triplet oriy/fwd/bck)
- `base_path` cari noise
- `VIDEO_PATH` (`KALIBRASI_X_VIDEO_BENERAN\video\pose_video_XX.avi`)
- `filename_csv` di notebook evaluasi (`DATA FIX\hasil_fix_banget_baseline_XX.csv`, `JALUR_VIDEO_FINAL_3_XX.csv`)
- `output_plot_name` (folder `HASIL_KALIBRASI_JALUR_FIX_EVALUASI`, `HASIL_PENGUJIAN_LINTASAN`)
- `TARGET_FOLDER` pada `cek_frame_folder`

**Perbaikan:** tarik ke satu sel konfigurasi (`PROJECT_ROOT`, `DATA_DIR`, `OUTPUT_DIR`)
atau file `config.py`/`.env`, lalu dokumentasikan struktur folder yang diharapkan di README.

### 2.2 Duplikasi blok kode
- Sel kalibrasi kamera (0-5) di `kalibrasisesuaipaper.ipynb` **sama persis** dengan
  sel 0-5 di `virtualencodervideo.ipynb`.
- `calibrateCamera` + perhitungan RMSE juga ditulis dua kali (sel 5 dan komentar "Cell 7").
- Sel 8 dan sel 9 di notebook 1 hampir identik (X vs Y), hanya beda target, steps/mm,
  `base_path`, dan nama file visualisasi.
- Notebook 3: sel 0 dan sel 1 hampir identik (baseline vs kalibrasi), sel 4 menggabungkan keduanya.

**Perbaikan:** jadikan satu modul `src/` (mis. `pipeline.py`: `detect_corners`, `calibrate_camera`,
`pose_from_image`, `evaluate_path`), lalu notebook hanya mengimpor. Ini juga langsung
menjawab permintaan "code rapi" untuk repo GitHub.

### 2.3 Output notebook membengkak
`kalibrasisesuaipaper.ipynb` 3.4 MB karena gambar tersimpan di output sel.
Untuk repo, jalankan **Clear All Outputs** sebelum commit, dan simpan gambar
hasil eksekusi ke `figures/` saja.

### 2.4 Baris mati / komentar ganda
- Blok `cv2.putText` versi "font kekecilan" masih ada dalam bentuk komentar panjang
  di sel 8 notebook 1.
- `FILE_INDICES = [1,2,3,4,5,6,7,8,9,10]` langsung ditimpa `FILE_INDICES = [1,2,3]`
  di sel 6 notebook 2 (nilai efektif hanya 3 video).
- `sample_idx = 0 if len(image_files) > 7 else 0` (dua cabang nilainya sama).
- `try/except` telanjang (`except:`) di `intersect_lines` dan `optimize_subpixel_gradient`.

### 2.5 Dependensi tidak didokumentasikan
Wajib: `opencv-contrib-python` (untuk `cv2.ximgproc`), `numpy`, `scipy`, `pandas`, `matplotlib`.
Belum ada `requirements.txt`. Versi OpenCV juga memengaruhi kestabilan deteksi,
sebaiknya dipin (pin) di requirements.

### 2.6 Belum ada berkas repo standar
Belum ada `LICENSE`, `.gitignore`, dan README. `.gif` animasi berukuran 15-23 MB
sebaiknya **tidak** ikut git (atau lewat Git LFS), karena membengkakkan histori.

## 3. Usulan Urutan Pengerjaan

1. Salin 3 notebook final + CSV kecil ke struktur folder ini (tanpa dataset besar).
2. Ekstrak blok berulang menjadi `src/` (`pipeline.py`, `evaluate.py`, `plot.py`).
3. Ganti semua path absolut dengan konfigurasi relatif + `config.py`.
4. Hapus baris mati, ganti `except:` telanjang dengan penanganan eksplisit.
5. Clear notebook outputs, simpan gambar ke `figures/`.
6. Tambah `requirements.txt`, `LICENSE`, `.gitignore`, dan perbaiki README dengan hasil
   angka final (RMSE kalibrasi kamera, RMSE lintasan baseline vs kalibrasi, persen perbaikan).
7. Tentukan mana file di `Code/` yang ikut repo dan mana yang ke `archive/` atau `.gitignore`.
8. `git init` di folder ini (bukan di dalam OneDrive lama), commit, lalu push ke GitHub.

## 4. Yang Masih Perlu Diisi (belum ada di kode)

Beberapa angka hasil akhir tidak tertulis di kode (hanya muncul sebagai print output
saat dijalankan): nilai K, D, RMSE reprojection keseluruhan, RMSE lintasan per trial,
dan persen perbaikan. Angka-angka ini perlu diambil dari naskah atau dengan menjalankan
ulang notebook memakai dataset, supaya bisa ditampilkan di README repo.
