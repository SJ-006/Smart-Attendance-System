import sys
import os
# Add the root directory to the python path so it can find config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
from database_mgr import log_attendance, save_intruder_photo, initialize_folders
from processor import AttendanceProcessor
from dotenv import load_dotenv

load_dotenv()
initialize_folders()

app = Flask(__name__)
engine = AttendanceProcessor()
unknown_counter = {} # Tracks unknown sightings per session

@app.route('/recognize', methods=['POST'])
def recognize():
    # Security Check
    if request.headers.get("X-API-KEY") != os.getenv("API_SECRET_KEY"):
        return jsonify({"status": "denied"}), 401

    file = request.files['image']
    img_bytes = file.read()
    
    name = engine.identify(img_bytes)
    
    if name in ["Unknown", "No Face"]:
        unknown_counter["current"] = unknown_counter.get("current", 0) + 1
        if unknown_counter["current"] >= 3:
            save_intruder_photo(img_bytes)
            print("🚨 Intruder Alert: Photo Saved!")
            unknown_counter["current"] = 0 # Reset
        return jsonify({"status": "unknown"})

    # Success Logic
    status = engine.get_punctuality()
    is_new = log_attendance(name, status)
    
    return jsonify({
        "status": "success", 
        "name": name, 
        "attendance": status,
        "new": is_new
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)