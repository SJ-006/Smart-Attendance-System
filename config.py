from datetime import time

# --- NETWORK ---
# 127.0.0.1 is for testing on one laptop. 
# Change to your laptop's IP when moving to the Pi.
SERVER_IP = "127.0.0.1" 
PORT = 5000
SERVER_URL = f"http://{SERVER_IP}:{PORT}/recognize"

# --- RULES ---
CLASS_START_TIME = time(9, 0) # 9:00 AM
LATE_THRESHOLD_MINUTES = 15   # Late after 9:15 AM

# --- SECURITY ---
# Must match the key in your .env file
API_SECRET_KEY = "college_attendance_2024_secret"
INTRUDER_THRESHOLD = 3  # Alert after 3 unknown sightings