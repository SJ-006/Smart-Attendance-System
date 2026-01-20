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


def get_all_attendance_logs():
    """
    Get all attendance logs from all CSV files in the logs directory
    
    Returns:
        pd.DataFrame: Combined dataframe of all attendance records
    """
    all_logs = []
    
    if not os.path.exists(LOG_DIR):
        return pd.DataFrame(columns=["Name", "Time", "Status", "Date"])
    
    for filename in os.listdir(LOG_DIR):
        if filename.startswith("attendance_") and filename.endswith(".csv"):
            file_path = os.path.join(LOG_DIR, filename)
            df = pd.read_csv(file_path)
            # Extract date from filename (attendance_YYYY-MM-DD.csv)
            date_str = filename.replace("attendance_", "").replace(".csv", "")
            df["Date"] = date_str
            all_logs.append(df)
    
    if all_logs:
        return pd.concat(all_logs, ignore_index=True)
    else:
        return pd.DataFrame(columns=["Name", "Time", "Status", "Date"])


def generate_student_statistics():
    """
    Generate student statistics including attendance percentage and late count
    
    Returns:
        pd.DataFrame: Statistics dataframe with columns:
                     - Student Name
                     - Total Days Present
                     - Days On Time
                     - Days Late
                     - Attendance Percentage
                     - Late Percentage
    """
    all_logs = get_all_attendance_logs()
    
    if all_logs.empty:
        return pd.DataFrame(columns=[
            "Student Name", "Total Days Present", "Days On Time", 
            "Days Late", "Attendance Percentage", "Late Percentage"
        ])
    
    # Get unique dates to calculate total possible days
    total_days = all_logs["Date"].nunique()
    
    # Group by student name
    stats = []
    for name in all_logs["Name"].unique():
        student_data = all_logs[all_logs["Name"] == name]
        
        total_present = len(student_data)
        days_on_time = len(student_data[student_data["Status"] == "On Time"])
        days_late = len(student_data[student_data["Status"] == "Late"])
        
        attendance_pct = (total_present / total_days * 100) if total_days > 0 else 0
        late_pct = (days_late / total_present * 100) if total_present > 0 else 0
        
        stats.append({
            "Student Name": name,
            "Total Days Present": total_present,
            "Days On Time": days_on_time,
            "Days Late": days_late,
            "Attendance Percentage": round(attendance_pct, 2),
            "Late Percentage": round(late_pct, 2)
        })
    
    return pd.DataFrame(stats).sort_values("Student Name")


def save_student_statistics():
    """
    Generate and save student statistics to a CSV file
    
    Returns:
        str: Path to the saved statistics file
    """
    stats_df = generate_student_statistics()
    stats_path = os.path.join(LOG_DIR, "student_statistics.csv")
    stats_df.to_csv(stats_path, index=False)
    print(f"📊 Student statistics saved to: {stats_path}")
    return stats_path