import face_recognition
import os
import cv2
import numpy as np
from datetime import datetime
from config import CLASS_START_TIME, LATE_THRESHOLD_MINUTES

class AttendanceProcessor:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self.reload_dataset()

    def reload_dataset(self):
        self.known_encodings = []
        self.known_names = []
        path = "server/dataset"
        if not os.path.exists(path): os.makedirs(path)
        
        for file in os.listdir(path):
            if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                img = face_recognition.load_image_file(f"{path}/{file}")
                encode = face_recognition.face_encodings(img)
                if encode:
                    self.known_encodings.append(encode[0])
                    self.known_names.append(os.path.splitext(file)[0])
        print(f"🧠 AI: Memory loaded with {len(self.known_names)} students.")

    def get_punctuality(self):
        now = datetime.now()
        start = datetime.combine(now.date(), CLASS_START_TIME)
        minutes_late = (now - start).total_seconds() / 60
        return "Late" if minutes_late > LATE_THRESHOLD_MINUTES else "Present"

    def identify(self, img_bytes):
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        encodes = face_recognition.face_encodings(rgb_img)
        if not encodes: return "No Face"
        
        matches = face_recognition.compare_faces(self.known_encodings, encodes[0])
        face_dis = face_recognition.face_distance(self.known_encodings, encodes[0])
        
        if any(matches):
            best_match = np.argmin(face_dis)
            return self.known_names[best_match]
        return "Unknown"