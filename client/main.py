import sys
import os
# Add the root directory to the python path so it can find config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cv2
import requests
import time
from config import SERVER_URL, API_SECRET_KEY
import ui_helper as ui

# Eye detector for Liveness (Blink) detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def run_eye():
    cam = cv2.VideoCapture(0)
    blink_frames = 0
    feedback_end = 0
    display_info = {"msg": "Please Blink to Scan", "color": (255, 255, 255), "name": "", "status": ""}

    while True:
        ret, frame = cam.read()
        if not ret: break
        
        # 1. Blink Detection Logic
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

        if len(eyes) == 0:
            blink_frames += 1
        else:
            if blink_frames >= 2: # Eyes were closed for 2+ frames
                # --- TRIGGER SCAN ---
                display_info["msg"] = "Scanning..."
                _, buffer = cv2.imencode('.jpg', frame)
                try:
                    res = requests.post(SERVER_URL, 
                                     files={'image': buffer.tobytes()}, 
                                     headers={'X-API-KEY': API_SECRET_KEY}, timeout=5).json()
                    
                    if res['status'] == 'success':
                        display_info = {"msg": "✅ SUCCESS", "color": (0, 255, 0), "name": res['name'], "status": res['attendance']}
                    else:
                        display_info = {"msg": "❌ UNKNOWN", "color": (0, 0, 255), "name": "Unknown", "status": "Denied"}
                except:
                    display_info["msg"] = "⚠️ Server Offline"
                
                feedback_end = time.time() + 3
                blink_frames = 0
            blink_frames = 0

        # 2. UI Updates
        if time.time() > feedback_end:
            display_info = {"msg": "Blink to Mark Attendance", "color": (255, 255, 255), "name": "", "status": ""}
        
        ui.draw_ui(frame, display_info["msg"], display_info["color"], display_info["name"], display_info["status"])
        cv2.imshow("Smart Attendance", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_eye()