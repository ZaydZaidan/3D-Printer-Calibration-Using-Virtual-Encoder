import cv2
import os
import time
from datetime import datetime

# 1. Setup Direktori Berdasarkan Waktu Sesi (Agar data tidak tercampur antar sesi)
waktu_sesi = datetime.now().strftime("%Y%m%d_%H%M%S")
base_folder = f"dataset_sesi_{waktu_sesi}"

folder_kalibrasi = os.path.join(base_folder, "kalibrasi")
folder_video = os.path.join(base_folder, "video")

# Buat foldernya
os.makedirs(folder_kalibrasi, exist_ok=True)
os.makedirs(folder_video, exist_ok=True)

print(f"=== SESI REKAMAN DIMULAI ===")
print(f"Folder Utama   : {base_folder}")
print(f"Folder Gambar  : {folder_kalibrasi}")
print(f"Folder Video   : {folder_video}\n")

# 2. Inisialisasi Kamera (0, 1, atau 2 tergantung urutan USB)
cap = cv2.VideoCapture(1)

# 3. Konfigurasi Kamera (1280x720, MJPG, 120 FPS)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

# --- TAMBAHKAN KODE INI UNTUK LOCK BRIGHTNESS/EXPOSURE ---

# Matikan Auto Exposure
# Catatan: Pada kamera UVC (USB), nilai 1 biasanya berarti "Manual", dan 3 berarti "Auto".
# Jika nilai 1 tidak mempan, coba ganti ke 0 atau 0.25
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

# Set nilai Exposure secara manual (Eksperimen dengan angkanya)
# Nilainya sering kali negatif (misal: -4, -5, -6) atau puluhan/ratusan (misal: 50, 100)
# Tergantung driver OS Anda. Silakan ubah angka -5 di bawah ini untuk mencari tingkat keterangan yang pas.
cap.set(cv2.CAP_PROP_EXPOSURE, -7)

# (Opsional) Mengunci Gain jika kamera masih terlihat ada "noise" yang berubah-ubah
# cap.set(cv2.CAP_PROP_GAIN, 0)

# ---------------------------------------------------------

actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
actual_fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Kamera aktif pada: {int(actual_width)}x{int(actual_height)} @ {actual_fps} FPS\n")

# Variabel kontrol
img_counter = 0
vid_counter = 1
recording = False
out = None

print("--- KONTROL ---")
print("[f] Capture Gambar Kalibrasi (PNG)")
print("[g] Mulai/Berhenti Rekam Video (MJPG)")
print("[q] Keluar dari Program\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal mengambil frame dari kamera.")
        break

    # Paksa konversi ke Grayscale untuk kamera Monochrome
    if len(frame.shape) == 3 and frame.shape[2] == 3:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = frame

    # Copy untuk display UI
    display_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    if recording:
        # Indikator recording di layar
        cv2.circle(display_frame, (30, 30), 10, (0, 0, 255), -1)
        cv2.putText(display_frame, "REC 120FPS", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Tulis frame grayscale ke video
        out.write(gray_frame)

    # Tampilkan kamera
    cv2.imshow('OV9281 Capture', display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
        
    elif key == ord('f'):
        # Simpan ke folder khusus kalibrasi
        img_name = os.path.join(folder_kalibrasi, f"calib_{img_counter:04d}.png")
        cv2.imwrite(img_name, gray_frame)
        print(f"[{img_counter}] Disimpan: {img_name}")
        img_counter += 1
        
    elif key == ord('g'):
        if not recording:
            # Mulai perekaman ke folder khusus video
            vid_name = os.path.join(folder_video, f"pose_video_{vid_counter:02d}.avi")
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            
            # isColor=False untuk Grayscale
            out = cv2.VideoWriter(vid_name, fourcc, 120.0, (int(actual_width), int(actual_height)), isColor=False)
            recording = True
            print(f"[*] MULAI merekam ke: {vid_name}")
        else:
            # Hentikan perekaman
            recording = False
            out.release()
            print(f"[*] BERHENTI merekam. Video {vid_counter:02d} selesai.")
            vid_counter += 1

# Bersihkan resources
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()