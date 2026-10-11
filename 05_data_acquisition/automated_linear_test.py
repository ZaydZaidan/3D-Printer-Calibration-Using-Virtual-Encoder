import serial
import time
import cv2
import os
from datetime import datetime

# ==========================================
# --- CNC MACHINE & CAMERA CONFIGURATION ---
# ==========================================
# PORT = 'COM10'
# BAUDRATE = 115200
# BACKLASH = 0.0133 # X AXIS
# #BACKLASH = 0.0244 + 0.0070 # Y AXIS
# SKEW_FACTOR = 0.009213 # Y-AXIS DRIFT WHEN MOVING THE X AXIS
# # SKEW_FACTOR = - 0.009200 # X-AXIS DRIFT WHEN MOVING THE Y AXIS
# STEPX = 79.72
# STEPY = 80.40

PORT = 'COM10'
BAUDRATE = 115200
BACKLASH = 0 # X AXIS
#BACKLASH = 0.0244 + 0.0070 # Y AXIS
SKEW_FACTOR = 0 # Y-AXIS DRIFT WHEN MOVING THE X AXIS
# SKEW_FACTOR = - 0.009200 # X-AXIS DRIFT WHEN MOVING THE Y AXIS
STEPX = 80
STEPY = 80

# --- TEST MODE SELECTION ---
# Choose one: 'X+', 'X-', 'Y+', 'Y-'
TEST_MODE = 'X+'  

# Set up Folder Based on Session Time & Mode
waktu_sesi = datetime.now().strftime("%Y%m%d_%H%M%S")
base_folder = f"dataset_{TEST_MODE.replace('+', 'pos').replace('-', 'neg')}_sesi_{waktu_sesi}"
folder_kalibrasi = os.path.join(base_folder, "kalibrasi")
os.makedirs(folder_kalibrasi, exist_ok=True)

print(f"=== AUTOMATED SESSION STARTED | MODE: {TEST_MODE} ===")
print(f"Image Folder : {folder_kalibrasi}\n")

# ==========================================
# --- MOVEMENT LOGIC SETUP ---
# ==========================================
if TEST_MODE == 'X+':
    active_axis = 'X'
    fwd_move = (0.5, 0.0)
    bck_move = (-0.5, 0.0)
    needs_initial_preload = False
    preload_out = (-10.0, 0.0) # Move away, opposite to fwd
    preload_in = (10.0, 0.0)   # Lock in the fwd direction
    
elif TEST_MODE == 'X-':
    active_axis = 'X'
    fwd_move = (-10.0, 0.0)
    bck_move = (10.0, 0.0)
    needs_initial_preload = True
    preload_out = (10.0, 0.0)  # Move away, opposite to fwd
    preload_in = (-10.0, 0.0)  # Lock in the fwd direction

elif TEST_MODE == 'Y+':
    active_axis = 'Y'
    fwd_move = (0.0, 0.5)
    bck_move = (0.0, -0.5)
    needs_initial_preload = False
    preload_out = (0.0, -10.0) # Move away, opposite to fwd
    preload_in = (0.0, 10.0)   # Lock in the fwd direction

elif TEST_MODE == 'Y-':
    active_axis = 'Y'
    fwd_move = (0.0, -10.0)
    bck_move = (0.0, 10.0)
    needs_initial_preload = True
    preload_out = (0.0, 10.0)  # Move away, opposite to fwd
    preload_in = (0.0, -10.0)  # Lock in the fwd direction

else:
    raise ValueError("TEST_MODE is not valid! Choose 'X+', 'X-', 'Y+', or 'Y-'")

# ==========================================
# --- HELPER FUNCTIONS ---
# ==========================================
def send_gcode(ser, cmd):
    print(f"Sending: {cmd} ", end="", flush=True)
    ser.write((cmd + '\n').encode('utf-8'))
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            if "busy: processing" in line.lower():
                print(".", end="", flush=True)
            else:
                print(f"\nMachine: {line}")
        if line.lower().startswith('ok'):
            break

def calc_cnc_logic(dx, dy, apply_backlash=False):
    # 1. SKEW COMPENSATION
    if active_axis == 'X':
        # If X moves, correct the drift on the Y axis
        dx_comp = dx
        dy_comp = dy - (dx * SKEW_FACTOR)
    elif active_axis == 'Y':
        # If Y moves, correct the drift on the X axis
        dx_comp = dx - (dy * SKEW_FACTOR)
        dy_comp = dy

    # 2. BACKLASH COMPENSATION
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
        print("[!] Failed to grab a frame from the camera.")
        return None

def save_image(img, prefix, index):
    if img is not None:
        filename = f"{prefix}{index}.png"
        filepath = os.path.join(folder_kalibrasi, filename)
        cv2.imwrite(filepath, img)
        print(f"[CAMERA] Saved -> {filename}")

# ==========================================
# --- CAMERA INITIALIZATION ---
# ==========================================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 120)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 
cap.set(cv2.CAP_PROP_EXPOSURE, -7) 

# ==========================================
# --- MAIN PROGRAM ---
# ==========================================
try:
    printer = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2) 
    
    # --- STAGE 1: SETUP & INITIAL STABILIZATION ---
    print("\n--- STAGE 1: MACHINE SETUP ---")
    send_gcode(printer, f"M92 X{STEPX} Y{STEPY}") 
    send_gcode(printer, "M500")
    send_gcode(printer, "G21")
    send_gcode(printer, "G28 X Y")
    send_gcode(printer, "G90")
    
    # Move to (150, 150). This movement is a POSITIVE move on X and Y.
    # Automatically provides a positive preload.
    send_gcode(printer, "G1 X150 Y150 F3000")
    
    send_gcode(printer, "G91") # Switch to relative
    
    # --- INITIAL PRELOAD (ONLY FOR X- AND Y- MODES) ---
    if needs_initial_preload:
        print(f"\nPerforming Initial Pre-load for mode {TEST_MODE} (Changing the gear lock direction)...")
        
        # Move away (out) then approach (in) to lock the gear in the negative direction
        tx_pout, ty_pout = calc_cnc_logic(*preload_out, apply_backlash=False)
        tx_pin, ty_pin = calc_cnc_logic(*preload_in, apply_backlash=False)
        
        send_gcode(printer, f"G1 X{tx_pout:.4f} Y{ty_pout:.4f} F500")
        send_gcode(printer, f"G1 X{tx_pin:.4f} Y{ty_pin:.4f} F500")

    print("\nWaiting 5 seconds for stabilization...")
    send_gcode(printer, "G4 P5000")
    
    # Capture the First Image (oriy1)
    print("Taking the initial photo (oriy1)...")
    img_awal = capture_frame(cap)
    save_image(img_awal, "oriy", 1)

    # --- STAGE 2: 40-ITERATION LOOP ---
    for i in range(1, 41): 
        print(f"\n======================================")
        print(f"--- Iteration {i} / 40 | Mode: {TEST_MODE} ---")
        print(f"======================================")
        
        # 1. MOVE FORWARD
        # apply_backlash=False because the gear is already preloaded in the fwd direction
        tx1, ty1 = calc_cnc_logic(*fwd_move, apply_backlash=False)
        send_gcode(printer, f"G1 X{tx1:.4f} Y{ty1:.4f} F500")
        send_gcode(printer, "G4 P2000") 
        
        # Capture FWD
        img_fwd = capture_frame(cap)
        save_image(img_fwd, "fwd", i)
        
        # 2. MOVE BACKWARD (Reverse)
        # apply_backlash=True because reversing crosses the backlash gap
        tx2, ty2 = calc_cnc_logic(*bck_move, apply_backlash=True)
        send_gcode(printer, f"G1 X{tx2:.4f} Y{ty2:.4f} F500")
        send_gcode(printer, "G4 P2000") 
        
        # Capture BCK
        img_bck = capture_frame(cap)
        save_image(img_bck, "bck", i)
        
        # 3. CLEAR THE REMAINING BACKLASH FOR THE NEXT ITERATION
        if i < 40:
            print(f"-> Clearing Backlash for Iteration {i+1}...")
            
            # Movements cancel each other out (out + in = 0) and restore the gear contact in the fwd direction
            tx_out, ty_out = calc_cnc_logic(*preload_out, apply_backlash=False)
            send_gcode(printer, f"G1 X{tx_out:.4f} Y{ty_out:.4f} F500")
            
            tx_in, ty_in = calc_cnc_logic(*preload_in, apply_backlash=False)
            send_gcode(printer, f"G1 X{tx_in:.4f} Y{ty_in:.4f} F500")
            
            send_gcode(printer, "G4 P2000") 
            
            # Capture the next ORIY
            img_oriy_next = capture_frame(cap)
            save_image(img_oriy_next, "oriy", i + 1)

    print("\n=== ALL PROCESSES COMPLETED SUCCESSFULLY ===")

except Exception as e:
    print(f"\n[!] An Error Occurred: {e}")

finally:
    if 'printer' in locals() and printer.is_open:
        printer.close()
        print("Serial connection closed.")
    if cap.isOpened():
        cap.release()
        print("Camera turned off.")