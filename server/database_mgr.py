import pandas as pd
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
INTRUDER_DIR = "server/intruders"

def initialize_folders():
    for folder in [LOG_DIR, INTRUDER_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

def log_attendance(name, status):
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(LOG_DIR, f"attendance_{date_str}.csv")
    
    # Create file with headers if it doesn't exist
    if not os.path.exists(file_path):
        pd.DataFrame(columns=["Name", "Time", "Status"]).to_csv(file_path, index=False)
    
    df = pd.read_csv(file_path)
    if name in df['Name'].values:
        return False # Already marked today
        
    now_time = datetime.now().strftime("%H:%M:%S")
    new_row = pd.DataFrame([{"Name": name, "Time": now_time, "Status": status}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_path, index=False)
    return True

def save_intruder_photo(image_bytes):
    initialize_folders()
    timestamp = datetime.now().strftime("%H%M%S")
    path = os.path.join(INTRUDER_DIR, f"intruder_{timestamp}.jpg")
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path