import cv2
import os
import time
from datetime import datetime

# 1. Set up Directories Based on Session Time (so data does not mix between sessions)
waktu_sesi = datetime.now().strftime("%Y%m%d_%H%M%S")
base_folder = f"dataset_sesi_{waktu_sesi}"

folder_kalibrasi = os.path.join(base_folder, "kalibrasi")
folder_video = os.path.join(base_folder, "video")

# Create the folders
os.makedirs(folder_kalibrasi, exist_ok=True)
os.makedirs(folder_video, exist_ok=True)

print(f"=== RECORDING SESSION STARTED ===")
print(f"Main Folder   : {base_folder}")
print(f"Image Folder  : {folder_kalibrasi}")
print(f"Video Folder  : {folder_video}\n")

# 2. Initialize Camera (0, 1, or 2 depending on USB order)
cap = cv2.VideoCapture(1)

# 3. Camera Configuration (1280x720, MJPG, 120 FPS)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

# --- ADD THIS CODE TO LOCK BRIGHTNESS/EXPOSURE ---

# Disable Auto Exposure
# Note: On UVC (USB) cameras, a value of 1 usually means "Manual", and 3 means "Auto".
# If the value 1 has no effect, try changing to 0 or 0.25
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

# Set the Exposure value manually (experiment with the number)
# The value is often negative (e.g. -4, -5, -6) or in the tens/hundreds (e.g. 50, 100)
# depending on your OS driver. Feel free to change the -5 below to find the right brightness level.
cap.set(cv2.CAP_PROP_EXPOSURE, -7)

# (Optional) Lock the Gain if the camera still shows fluctuating "noise"
# cap.set(cv2.CAP_PROP_GAIN, 0)

# ---------------------------------------------------------

actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
actual_fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Camera active at: {int(actual_width)}x{int(actual_height)} @ {actual_fps} FPS\n")

# Control variables
img_counter = 0
vid_counter = 1
recording = False
out = None

print("--- CONTROL ---")
print("[f] Capture Calibration Image (PNG)")
print("[g] Start/Stop Video Recording (MJPG)")
print("[q] Exit the Program\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab a frame from the camera.")
        break

    # Force conversion to Grayscale for a Monochrome camera
    if len(frame.shape) == 3 and frame.shape[2] == 3:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = frame

    # Copy for the UI display
    display_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

    if recording:
        # On-screen recording indicator
        cv2.circle(display_frame, (30, 30), 10, (0, 0, 255), -1)
        cv2.putText(display_frame, "REC 120FPS", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Write the grayscale frame to the video
        out.write(gray_frame)

    # Show the camera
    cv2.imshow('OV9281 Capture', display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
        
    elif key == ord('f'):
        # Save to the dedicated calibration folder
        img_name = os.path.join(folder_kalibrasi, f"calib_{img_counter:04d}.png")
        cv2.imwrite(img_name, gray_frame)
        print(f"[{img_counter}] Saved: {img_name}")
        img_counter += 1
        
    elif key == ord('g'):
        if not recording:
            # Start recording to the dedicated video folder
            vid_name = os.path.join(folder_video, f"pose_video_{vid_counter:02d}.avi")
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            
            # isColor=False for Grayscale
            out = cv2.VideoWriter(vid_name, fourcc, 120.0, (int(actual_width), int(actual_height)), isColor=False)
            recording = True
            print(f"[*] STARTED recording to: {vid_name}")
        else:
            # Stop recording
            recording = False
            out.release()
            print(f"[*] STOPPED recording. Video {vid_counter:02d} complete.")
            vid_counter += 1

# Clean up resources
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()