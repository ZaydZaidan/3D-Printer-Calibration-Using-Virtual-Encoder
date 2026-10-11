# 05 — Skrip Akuisisi (butuh mesin & kamera)

Skrip di folder ini **hanya bisa dijalankan dengan perangkat keras**: 3D printer yang
tersambung serial + kamera. Skrip ini **mengisi** `data/raw/`, bukan mengolahnya.
Isinya sama dengan kode penelitian asli (tidak diubah isinya, hanya nama berkas).

| Berkas | Peran | Baris yang WAJIB disesuaikan |
|---|---|---|
| `buat_papan_catur.py` | Cetak papan kalibrasi A4 (8x8 kotak 20 mm + 3 lingkaran penanda) | - |
| `capture_kalibrasi_kamera.py` | Ambil citra papan catur untuk kalibrasi kamera (tombol `f`) | baris 23 `cv2.VideoCapture(1)` (indeks kamera), baris 29 FPS, baris 41 eksposur |
| `otomasi_pengujian_linear.py` | Pergerakan linear `oriy`/`fwd`/`bck` 40x untuk kalibrasi mesin | baris 19 `PORT` (mis. `COM10`), baris 21-26 `BACKLASH`/`SKEW_FACTOR`/`STEPX`/`STEPY`, baris 30 `TEST_MODE` |
| `otomasi_lintasan_elips.py` | Jalankan lintasan elips + rekam video | baris 12 `PORT`, baris 15-21 parameter kalibrasi, baris 23 `TOTAL_ITERASI`, baris 322 indeks kamera |

Prasyarat mesin:

- Firmware RepRap/Marlin yang menerima `M92`, `M425`, `M852`, `G28`, `G1`, `M400`, `G4`.
- Kamera **monokrom** 1280x720 (penelitian memakai OV9281). Skrip memaksa grayscale.
- Eksposur dikunci manual (`AUTO_EXPOSURE=1`, `EXPOSURE=-7`) agar pencahayaan stabil.

Alur akuisisi per sesi:

```
capture_kalibrasi_kamera.py   -> dataset_sesi_<timestamp>/kalibrasi/calib_XXXX.png
otomasi_pengujian_linear.py   -> dataset_<Xpos|Xneg|Ypos|Yneg>_sesi_<ts>/kalibrasi/oriy,fwd,bck{i}.png
otomasi_lintasan_elips.py     -> dataset_otomatis_sesi_<timestamp>/video/pose_video_XX.avi
```

Setelah selesai, pindahkan hasilnya ke `data/raw/` sesuai `data/MANIFEST.md`.

> Skrip `otomasi_pengujian_linear.py` asli memakai jarak gerak **10 mm** untuk mode
> `X-`/`Y-` dan **0.5 mm** untuk mode `X+`/`Y+` (yang terakhir dipakai untuk eksperimen
> measurement error / dial gauge).
