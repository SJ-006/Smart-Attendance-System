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
# API_SECRET_KEY is now stored in .env file for security
# Load it using: os.getenv("API_SECRET_KEY")
INTRUDER_THRESHOLD = 3  # Alert after 3 unknown sightings