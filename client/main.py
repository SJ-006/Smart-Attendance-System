import cv2
import requests
import os
import sys
import time

# Add parent directory to path to import local config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SERVER_URL
from dotenv import load_dotenv
import ui_helper as ui

# Load environment variables
load_dotenv()
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

# Eye detector
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def run_eye():
    cam = cv2.VideoCapture(0)
    # SET LOWER RESOLUTION FOR BETTER FPS
    cam.set(3, 640) 
    cam.set(4, 480)

    blink_frames = 0
    feedback_end = 0
    display_info = {"msg": "Standby", "color": ui.COLOR_CYAN, "name": "", "status": ""}
    
    frame_count = 0
    
    print("\n=== Smart Attendance System ===")
    print("Controls:")
    print("  Q or X - Quit")
    print("  ESC - Exit")
    print("  Blink to scan attendance")
    print("==============================\n")

    while True:
        ret, frame = cam.read()
        if not ret: break
        frame_count += 1
        
        # 1. OPTIMIZATION: Process AI only every 2nd frame
        if frame_count % 2 == 0:
            # Resize for AI (Make it tiny so it's fast)
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, 1.1, 5)

            if len(eyes) == 0:
                blink_frames += 1
            else:
                if blink_frames >= 2: # Blink Detected
                    display_info["msg"] = "Processing"
                    # UI update before the slow network call
                    ui_copy = frame.copy()
                    ui.draw_futuristic_hud(ui_copy, "SCANNING...")
                    ui.draw_scanning_line(ui_copy)
                    cv2.imshow("Smart Attendance", ui_copy)
                    cv2.waitKey(1)

                    # Trigger Scan
                    _, buffer = cv2.imencode('.jpg', frame)
                    try:
                        res = requests.post(SERVER_URL, 
                                         files={'image': buffer.tobytes()}, 
                                         headers={'X-API-KEY': API_SECRET_KEY}, timeout=3).json()
                        
                        if res['status'] == 'success':
                            display_info = {"msg": "Verified", "color": ui.COLOR_NEON_GREEN, "name": res['name'], "status": res['attendance']}
                        else:
                            display_info = {"msg": "Unknown", "color": ui.COLOR_NEON_RED, "name": "Unauthorized", "status": "Blocked"}
                    except:
                        display_info = {"msg": "Network Error", "color": ui.COLOR_NEON_RED}
                    
                    feedback_end = time.time() + 4
                    blink_frames = 0
                blink_frames = 0

        # 2. UI RENDERING
        ui_frame = frame.copy()
        
        if time.time() < feedback_end:
            ui.draw_futuristic_hud(ui_frame, display_info["msg"], display_info["color"])
            ui.draw_attendance_card(ui_frame, display_info["name"], display_info["status"], display_info["color"])
        else:
            ui.draw_futuristic_hud(ui_frame, "Blink to Scan")
            ui.draw_scanning_line(ui_frame) # Always show scanning line when idle

        cv2.imshow("Smart Attendance", ui_frame)
        
        # Press 'q', ESC, or 'x' to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('x') or key == 27:  # 27 is ESC key
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_eye()