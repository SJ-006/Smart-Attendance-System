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
        """Processes images stored in student-specific folders."""
        self.known_encodings = []
        self.known_names = []
        dataset_path = "server/dataset"
        
        # Create dataset folder if it's missing
        if not os.path.exists(dataset_path): 
            os.makedirs(dataset_path)
        
        # 1. Loop through each folder (Each folder is a student)
        for folder_name in os.listdir(dataset_path):
            student_folder = os.path.join(dataset_path, folder_name)
            
            # Make sure we are looking at a folder, not a stray file
            if os.path.isdir(student_folder):
                print(f"📁 Processing folder for: {folder_name.upper()}")
                
                # 2. Loop through every image inside that student's folder
                for filename in os.listdir(student_folder):
                    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                        img_path = os.path.join(student_folder, filename)
                        
                        # Load and encode the face
                        img = face_recognition.load_image_file(img_path)
                        encodings = face_recognition.face_encodings(img)
                        
                        if encodings:
                            self.known_encodings.append(encodings[0])
                            # Use the FOLDER NAME as the student's identity
                            self.known_names.append(folder_name)
                            
        print(f"🧠 AI Memory: Loaded {len(self.known_encodings)} images for {len(set(self.known_names))} students.")

    def get_punctuality(self):
        """Calculates if the current time is within the grace period."""
        now = datetime.now()
        start = datetime.combine(now.date(), CLASS_START_TIME)
        minutes_late = (now - start).total_seconds() / 60
        return "Late" if minutes_late > LATE_THRESHOLD_MINUTES else "Present"

    def identify(self, img_bytes):
        """Compares the incoming frame from the Pi with the database."""
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        encodes = face_recognition.face_encodings(rgb_img)
        if not encodes: return "No Face"
        
        # Compare current face with our entire list of known encodings
        matches = face_recognition.compare_faces(self.known_encodings, encodes[0])
        face_dis = face_recognition.face_distance(self.known_encodings, encodes[0])
        
        if any(matches):
            # Find the closest match (lowest distance)
            best_match_idx = np.argmin(face_dis)
            return self.known_names[best_match_idx]
        
        return "Unknown"