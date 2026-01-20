import sys
import os
# Add the root directory to the python path so it can find config.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
from database_mgr import log_attendance, save_intruder_photo, initialize_folders, save_student_statistics
from processor import AttendanceProcessor
from mail_sender import send_daily_report
from dotenv import load_dotenv
from datetime import datetime

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


@app.route('/send_report', methods=['POST'])
def send_report():
    """
    Endpoint to manually trigger sending attendance report via email
    Requires API key authentication
    """
    # Security Check
    if request.headers.get("X-API-KEY") != os.getenv("API_SECRET_KEY"):
        return jsonify({"status": "denied", "message": "Unauthorized"}), 401
    
    try:
        # Generate student statistics
        stats_path = save_student_statistics()
        
        # Get today's attendance log path
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        daily_log_path = os.path.join(log_dir, f"attendance_{date_str}.csv")
        
        # Send email with both files
        success = send_daily_report(daily_log_path, stats_path)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Attendance report sent successfully",
                "files": [daily_log_path, stats_path]
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to send email"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Endpoint to get student statistics without sending email
    Requires API key authentication
    """
    # Security Check
    if request.headers.get("X-API-KEY") != os.getenv("API_SECRET_KEY"):
        return jsonify({"status": "denied", "message": "Unauthorized"}), 401
    
    try:
        from database_mgr import generate_student_statistics
        stats_df = generate_student_statistics()
        
        return jsonify({
            "status": "success",
            "statistics": stats_df.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)