import serial
import time
import cv2
import os
from datetime import datetime

# ==========================================
# --- KONFIGURASI MESIN CNC & KAMERA ---
# ==========================================
# PORT = 'COM10'
# BAUDRATE = 115200
# BACKLASH = 0.0133 #SUMBU X
# #BACKLASH = 0.0244 + 0.0070 #SUMBU Y
# SKEW_FACTOR = 0.009213 # DRIFT SUMBU Y PADA PERGERAKAN SUMBU X
# # SKEW_FACTOR = - 0.009200 # DRIFT SUMBU X PADA PERGERAKAN SUMBU Y
# STEPX = 79.72
# STEPY = 80.40

PORT = 'COM10'
BAUDRATE = 115200
BACKLASH = 0 #SUMBU X
#BACKLASH = 0.0244 + 0.0070 #SUMBU Y
SKEW_FACTOR = 0 # DRIFT SUMBU Y PADA PERGERAKAN SUMBU X
# SKEW_FACTOR = - 0.009200 # DRIFT SUMBU X PADA PERGERAKAN SUMBU Y
STEPX = 80
STEPY = 80

# --- PILIHAN MODE PENGUJIAN ---
# Pilih salah satu: 'X+', 'X-', 'Y+', 'Y-'
TEST_MODE = 'X+'  

# Setup Folder Berdasarkan Waktu Sesi & Mode
waktu_sesi = datetime.now().strftime("%Y%m%d_%H%M%S")
base_folder = f"dataset_{TEST_MODE.replace('+', 'pos').replace('-', 'neg')}_sesi_{waktu_sesi}"
folder_kalibrasi = os.path.join(base_folder, "kalibrasi")
os.makedirs(folder_kalibrasi, exist_ok=True)

print(f"=== SESI OTOMATIS DIMULAI | MODE: {TEST_MODE} ===")
print(f"Folder Gambar : {folder_kalibrasi}\n")

# ==========================================
# --- SETUP LOGIKA PERGERAKAN ---
# ==========================================
if TEST_MODE == 'X+':
    active_axis = 'X'
    fwd_move = (0.5, 0.0)
    bck_move = (-0.5, 0.0)
    needs_initial_preload = False
    preload_out = (-10.0, 0.0) # Menjauh berlawanan fwd
    preload_in = (10.0, 0.0)   # Mengunci searah fwd
    
elif TEST_MODE == 'X-':
    active_axis = 'X'
    fwd_move = (-10.0, 0.0)
    bck_move = (10.0, 0.0)
    needs_initial_preload = True
    preload_out = (10.0, 0.0)  # Menjauh berlawanan fwd
    preload_in = (-10.0, 0.0)  # Mengunci searah fwd

elif TEST_MODE == 'Y+':
    active_axis = 'Y'
    fwd_move = (0.0, 0.5)
    bck_move = (0.0, -0.5)
    needs_initial_preload = False
    preload_out = (0.0, -10.0) # Menjauh berlawanan fwd
    preload_in = (0.0, 10.0)   # Mengunci searah fwd

elif TEST_MODE == 'Y-':
    active_axis = 'Y'
    fwd_move = (0.0, -10.0)
    bck_move = (0.0, 10.0)
    needs_initial_preload = True
    preload_out = (0.0, 10.0)  # Menjauh berlawanan fwd
    preload_in = (0.0, -10.0)  # Mengunci searah fwd

else:
    raise ValueError("TEST_MODE tidak valid! Pilih 'X+', 'X-', 'Y+', atau 'Y-'")

# ==========================================
# --- FUNGSI PENDUKUNG ---
# ==========================================
def send_gcode(ser, cmd):
    print(f"Mengirim: {cmd} ", end="", flush=True)
    ser.write((cmd + '\n').encode('utf-8'))
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            if "busy: processing" in line.lower():
                print(".", end="", flush=True)
            else:
                print(f"\nMesin: {line}")
        if line.lower().startswith('ok'):
            break

def calc_cnc_logic(dx, dy, apply_backlash=False):
    # 1. KOMPENSASI SKEW (KEMIRINGAN)
    if active_axis == 'X':
        # Jika X bergerak, koreksi drift pada sumbu Y
        dx_comp = dx
        dy_comp = dy - (dx * SKEW_FACTOR)
    elif active_axis == 'Y':
        # Jika Y bergerak, koreksi drift pada sumbu X
        dx_comp = dx - (dy * SKEW_FACTOR)
        dy_comp = dy

    # 2. KOMPENSASI BACKLASH
    if apply_backlash:
        if active_axis == 'X':
            dx_comp = dx_comp - BACKLASH if dx_comp < 0 else dx_comp + BACKLASH
        elif active_axis == 'Y':
            dy_comp = dy_comp - BACKLASH if dy_comp < 0 else dy_comp + BACKLASH    
    return dx_comp, dy_comp

def capture_frame(cap):
    for _ in range(5):
        cap.read()
    
    ret, frame = cap.read()
    if ret:
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame
    else:
        print("[!] Gagal mengambil frame dari kamera.")
        return None

def save_image(img, prefix, index):
    if img is not None:
        filename = f"{prefix}{index}.png"
        filepath = os.path.join(folder_kalibrasi, filename)
        cv2.imwrite(filepath, img)
        print(f"[KAMERA] Tersimpan -> {filename}")

# ==========================================
# --- INISIALISASI KAMERA ---
# ==========================================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 120)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 
cap.set(cv2.CAP_PROP_EXPOSURE, -7) 

# ==========================================
# --- PROGRAM UTAMA ---
# ==========================================
try:
    printer = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2) 
    
    # --- TAHAP 1: SETUP & STABILISASI AWAL ---
    print("\n--- TAHAP 1: SETUP MESIN ---")
    send_gcode(printer, f"M92 X{STEPX} Y{STEPY}") 
    send_gcode(printer, "M500")
    send_gcode(printer, "G21")
    send_gcode(printer, "G28 X Y")
    send_gcode(printer, "G90")
    
    # Bergerak ke (150, 150). Gerakan ini adalah gerakan POSITIF pada X dan Y.
    # Otomatis memberikan preload positif.
    send_gcode(printer, "G1 X150 Y150 F3000")
    
    send_gcode(printer, "G91") # Ubah ke relatif
    
    # --- PRELOAD AWAL (KHUSUS MODE X- DAN Y-) ---
    if needs_initial_preload:
        print(f"\nMelakukan Pre-load Awal untuk mode {TEST_MODE} (Mengubah arah kunci gerigi)...")
        
        # Gerak menjauh (out) lalu mendekat (in) untuk mengunci gerigi ke arah negatif
        tx_pout, ty_pout = calc_cnc_logic(*preload_out, apply_backlash=False)
        tx_pin, ty_pin = calc_cnc_logic(*preload_in, apply_backlash=False)
        
        send_gcode(printer, f"G1 X{tx_pout:.4f} Y{ty_pout:.4f} F500")
        send_gcode(printer, f"G1 X{tx_pin:.4f} Y{ty_pin:.4f} F500")

    print("\nMenunggu stabilisasi 5 detik...")
    send_gcode(printer, "G4 P5000")
    
    # Capture Gambar Pertama (oriy1)
    print("Mengambil foto awal (oriy1)...")
    img_awal = capture_frame(cap)
    save_image(img_awal, "oriy", 1)

    # --- TAHAP 2: LOOP 40 ITERASI ---
    for i in range(1, 41): 
        print(f"\n======================================")
        print(f"--- Iterasi {i} / 40 | Mode: {TEST_MODE} ---")
        print(f"======================================")
        
        # 1. BERGERAK FORWARD
        # apply_backlash=False karena gerigi sudah ter-preload searah fwd
        tx1, ty1 = calc_cnc_logic(*fwd_move, apply_backlash=False)
        send_gcode(printer, f"G1 X{tx1:.4f} Y{ty1:.4f} F500")
        send_gcode(printer, "G4 P2000") 
        
        # Capture FWD
        img_fwd = capture_frame(cap)
        save_image(img_fwd, "fwd", i)
        
        # 2. BERGERAK BACKWARD (Putar Balik)
        # apply_backlash=True karena mesin putar balik menyeberangi celah backlash
        tx2, ty2 = calc_cnc_logic(*bck_move, apply_backlash=True)
        send_gcode(printer, f"G1 X{tx2:.4f} Y{ty2:.4f} F500")
        send_gcode(printer, "G4 P2000") 
        
        # Capture BCK
        img_bck = capture_frame(cap)
        save_image(img_bck, "bck", i)
        
        # 3. MENGHAPUS SISA BACKLASH UNTUK ITERASI BERIKUTNYA
        if i < 40:
            print(f"-> Menghapus Backlash untuk Iterasi {i+1}...")
            
            # Gerakan saling menghilangkan (out + in = 0) dan mengembalikan kontak gigi searah fwd
            tx_out, ty_out = calc_cnc_logic(*preload_out, apply_backlash=False)
            send_gcode(printer, f"G1 X{tx_out:.4f} Y{ty_out:.4f} F500")
            
            tx_in, ty_in = calc_cnc_logic(*preload_in, apply_backlash=False)
            send_gcode(printer, f"G1 X{tx_in:.4f} Y{ty_in:.4f} F500")
            
            send_gcode(printer, "G4 P2000") 
            
            # Capture ORIY selanjutnya
            img_oriy_next = capture_frame(cap)
            save_image(img_oriy_next, "oriy", i + 1)

    print("\n=== SEMUA PROSES SELESAI DENGAN SUKSES ===")

except Exception as e:
    print(f"\n[!] Terjadi Error: {e}")

finally:
    if 'printer' in locals() and printer.is_open:
        printer.close()
        print("Koneksi Serial ditutup.")
    if cap.isOpened():
        cap.release()
        print("Kamera dimatikan.")