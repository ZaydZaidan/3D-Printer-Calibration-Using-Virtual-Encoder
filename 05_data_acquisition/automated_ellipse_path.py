from datetime import datetime
import math
import os
import threading
import time
import cv2
import serial

# =====================================================================
# --- KINEMATICS & SERIAL PARAMETER CONFIGURATION ---
# =====================================================================
PORT = "COM10"
BAUDRATE = 115200

BACKLASH_X = 0.0133
BACKLASH_Y = 0.0244 + 0.0070
SKEW_X_ON_Y = -0.009200  # X-axis drift when the Y axis moves
SKEW_Y_ON_X = 0.009213  # Y-axis drift when the X axis moves

STEPX = 79.72
STEPY = 80.40

TOTAL_ITERASI = 10  # Number of automatic repetitions starting from homing
# =====================================================================

# Global Variable for Synchronization between Threads
program_running = True


class RecorderState:

    def __init__(self):
        self.cmd_start = False
        self.cmd_stop = False
        self.is_recording = False
        self.vid_counter = 1


state = RecorderState()


# =====================================================================
# --- KINEMATICS FUNCTIONS & PATH GENERATOR ---
# =====================================================================
def get_ellipse_point(center_x, center_y, a, b, angle_deg, t):
    angle_rad = math.radians(angle_deg)
    x = a * math.cos(t)
    y = b * math.sin(t)
    x_rot = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    y_rot = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return center_x + x_rot, center_y + y_rot


def apply_kinematics(
    points, center_x, center_y, current_dir_x=1, current_dir_y=1
):
    compensated_points = []
    skewed_points = []

    for x_ideal, y_ideal in points:
        dy_from_center = y_ideal - center_y
        dx_from_center = x_ideal - center_x
        x_skew = x_ideal - (dy_from_center * SKEW_X_ON_Y)
        y_skew = y_ideal - (dx_from_center * SKEW_Y_ON_X)
        skewed_points.append((x_skew, y_skew))

    for i in range(len(skewed_points)):
        x, y = skewed_points[i]
        if i > 0:
            prev_x, prev_y = skewed_points[i - 1]
            dx, dy = x - prev_x, y - prev_y
            if dx > 1e-5:
                current_dir_x = 1
            elif dx < -1e-5:
                current_dir_x = -1
            if dy > 1e-5:
                current_dir_y = 1
            elif dy < -1e-5:
                current_dir_y = -1

        x_final = x if current_dir_x == 1 else x - BACKLASH_X
        y_final = y if current_dir_y == 1 else y - BACKLASH_Y
        compensated_points.append((x_final, y_final))

    return compensated_points, current_dir_x, current_dir_y


def generate_path(
    center_x,
    center_y,
    a,
    b,
    angle_deg,
    t_start,
    t_end,
    num_points,
    feedrate,
    dir_x=1,
    dir_y=1,
):
    raw_points = []
    step = (t_end - t_start) / num_points
    for i in range(0, num_points + 1):
        t = t_start + i * step
        raw_points.append(
            get_ellipse_point(center_x, center_y, a, b, angle_deg, t)
        )

    comp_points, next_dir_x, next_dir_y = apply_kinematics(
        raw_points, center_x, center_y, dir_x, dir_y
    )
    gcode = [f"G1 X{x:.4f} Y{y:.4f} F{feedrate}" for x, y in comp_points]
    return gcode, next_dir_x, next_dir_y


def precompute_ellipse_commands():
    skala, ratio = 10.0, 8.0
    a = 4.00 * skala / ratio
    b = 2.00 * skala / ratio
    feedrate, resolusi_titik = 500, 240

    t_start_1 = math.atan2(a, b)
    t_start_2 = math.atan2(-a, b)

    # Compute the Y offset mathematically precisely at the intersection point
    # At t_start_1 with a 45-degree rotation, x_offset = 0 and y_offset approx 3.162277...
    _, y_offset = get_ellipse_point(0, 0, a, b, 45, t_start_1)

    # Shift the ellipse center downward so the intersection point falls exactly at coordinate (150.0, 150.0)
    center_x = 150.0
    center_y = 150.0 - y_offset

    commands = [
        "G1 X150.0000 Y150.0000 F500 ; Start exactly from the reference point (intersection)"
    ]
    cur_dir_x, cur_dir_y = 1, 1

    # Loop 1: Forward
    p1, cur_dir_x, cur_dir_y = generate_path(
        center_x,
        center_y,
        a,
        b,
        45,
        t_start_1,
        t_start_1 + 2 * math.pi,
        resolusi_titik,
        feedrate,
        cur_dir_x,
        cur_dir_y,
    )
    commands.extend(p1)
    p2, cur_dir_x, cur_dir_y = generate_path(
        center_x,
        center_y,
        a,
        b,
        135,
        t_start_2,
        t_start_2 + 2 * math.pi,
        resolusi_titik,
        feedrate,
        cur_dir_x,
        cur_dir_y,
    )
    commands.extend(p2)

    # Loop 2: Reverse
    p3, cur_dir_x, cur_dir_y = generate_path(
        center_x,
        center_y,
        a,
        b,
        135,
        t_start_2 + 2 * math.pi,
        t_start_2,
        resolusi_titik,
        feedrate,
        cur_dir_x,
        cur_dir_y,
    )
    commands.extend(p3)
    p4, cur_dir_x, cur_dir_y = generate_path(
        center_x,
        center_y,
        a,
        b,
        45,
        t_start_1 + 2 * math.pi,
        t_start_1,
        resolusi_titik,
        feedrate,
        cur_dir_x,
        cur_dir_y,
    )
    commands.extend(p4)

    commands.append("G1 X150.0000 Y150.0000 F500 ; Return to origin")
    return commands

# =====================================================================
# --- THREAD 2: CNC CONTROLLER WORKER ---
# =====================================================================
def send_gcode(ser, cmd):
    global program_running
    print(f"Sending: {cmd} ", end="", flush=True)
    ser.write((cmd + "\n").encode("utf-8"))

    while program_running:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line:
            if "busy: processing" in line.lower():
                print(".", end="", flush=True)
            else:
                print(f"\nMachine: {line}")
                if line.lower().startswith("ok"):
                    break


def cnc_worker_thread(ellipse_commands):
    global program_running
    try:
        printer = serial.Serial(PORT, BAUDRATE, timeout=0.5)
        time.sleep(2)

        for loop_idx in range(1, TOTAL_ITERASI + 1):
            if not program_running:
                break

            print(
                f"\n" + "=" * 50 + f"\n=== STARTING AUTOMATIC ITERATION {loop_idx}/{TOTAL_ITERASI} ===\n" + "=" * 50
            )

            # 1. Setup & Homing Stage
            send_gcode(printer, f"M92 X{STEPX} Y{STEPY}")
            send_gcode(printer, "G21")
            send_gcode(printer, "G90")
            send_gcode(printer, "G28 X Y")
            send_gcode(
                printer, "G1 X150.0000 Y150.0000 F3000"
            )

            print(
                f"\n[CNC] Waiting 5 seconds for stabilization (G4 P5000)..."
            )
            send_gcode(printer, "G4 P5000")

            if not program_running:
                break

            # 2. Trigger Start Camera Recording
            state.cmd_start = True
            while not state.is_recording and program_running:
                time.sleep(0.005)
            state.cmd_start = False

            # ---> INITIAL 1-SECOND PAUSE (RECORDING IS RUNNING, THE MACHINE IS STILL) <---
            print("\n[CNC] Recording initial baseline (1-second still pause)...")
            time.sleep(1.0)

            # 3. Execute the Ellipse Trajectory
            print(
                f"\n[CNC] Running the compensated ellipse trajectory..."
            )
            for cmd in ellipse_commands:
                if not program_running:
                    break
                send_gcode(printer, cmd)

            # Wait for all physical motor movements to finish
            send_gcode(printer, "M400")

            if not program_running:
                break

            # ---> FINAL 1-SECOND PAUSE (THE MACHINE IS STILL, RECORDING IS STILL RUNNING) <---
            print("\n[CNC] Recording final baseline (1-second still pause)...")
            time.sleep(1.0)

            # 4. Trigger Stop Recording
            state.cmd_stop = True
            while state.is_recording and program_running:
                time.sleep(0.005)
            state.cmd_stop = False

            state.vid_counter += 1

        print(
            f"\n=== ALL {TOTAL_ITERASI} ITERATIONS COMPLETED SUCCESSFULLY ==="
        )

    except Exception as e:
        print(f"\n[!] An Error Occurred in the CNC Worker: {e}")
    finally:
        program_running = False
        if "printer" in locals() and printer.is_open:
            printer.close()
            print("[CNC] Serial connection closed.")


# =====================================================================
# --- THREAD 1 (MAIN): FRAME GRABBING & VIDEO WRITER ---
# =====================================================================
def main():
    global program_running

    print("Computing ellipse coordinate points...")
    ellipse_commands = precompute_ellipse_commands()

    waktu_sesi = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_folder = f"dataset_otomatis_sesi_{waktu_sesi}"
    folder_kalibrasi = os.path.join(base_folder, "kalibrasi")
    folder_video = os.path.join(base_folder, "video")

    os.makedirs(folder_kalibrasi, exist_ok=True)
    os.makedirs(folder_video, exist_ok=True)

    print(f"=== AUTOMATED RECORDING SESSION STARTED ===")
    print(f"Main Folder   : {base_folder}")
    print(f"Video Folder  : {folder_video}\n")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 120)

    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cap.set(cv2.CAP_PROP_EXPOSURE, -7)

    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(
        f"Camera active at: {int(actual_width)}x{int(actual_height)} @ {actual_fps} FPS\n"
    )

    out = None
    img_counter = 0

    print("--- EMERGENCY CONTROL ---")
    print("[f] Capture Manual Image (PNG)")
    print("[q] Cancel & Exit the Program\n")

    cnc_thread = threading.Thread(
        target=cnc_worker_thread, args=(ellipse_commands,)
    )
    cnc_thread.start()

    while program_running:
        ret, frame = cap.read()
        if not ret:
            print("[!] Failed to grab a frame from the camera.")
            program_running = False
            break

        if len(frame.shape) == 3 and frame.shape[2] == 3:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray_frame = frame

        display_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

        # TRIGGER START
        if state.cmd_start and not state.is_recording:
            vid_name = os.path.join(
                folder_video, f"pose_video_{state.vid_counter:02d}.avi"
            )
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            out = cv2.VideoWriter(
                vid_name,
                fourcc,
                120.0,
                (int(actual_width), int(actual_height)),
                isColor=False,
            )
            state.is_recording = True
            print(f"\n[CAMERA] STARTED recording to: {vid_name}")

        # TRIGGER STOP
        if state.cmd_stop and state.is_recording:
            state.is_recording = False
            if out is not None:
                out.release()
                out = None
            print(
                f"[CAMERA] STOPPED recording. Video {state.vid_counter:02d} complete."
            )

        # FRAME WRITING
        if state.is_recording and out is not None:
            cv2.circle(display_frame, (30, 30), 10, (0, 0, 255), -1)
            cv2.putText(
                display_frame,
                f"REC 120FPS (Loop {state.vid_counter}/{TOTAL_ITERASI})",
                (50, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
            out.write(gray_frame)

        cv2.imshow("OV9281 Capture", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("\n[!] User cancelled the execution (Q key).")
            program_running = False
            break
        elif key == ord("f"):
            img_name = os.path.join(
                folder_kalibrasi, f"calib_manual_{img_counter:04d}.png"
            )
            cv2.imwrite(img_name, gray_frame)
            print(f"[CAMERA] Saved: {img_name}")
            img_counter += 1

    program_running = False
    cnc_thread.join()

    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
    print("[CAMERA] System shut down safely.")


if __name__ == "__main__":
    main()