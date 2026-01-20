import yagmail
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_attendance_email(csv_files, subject=None, body=None):
    """
    Send attendance report via email with CSV attachments
    
    Args:
        csv_files: List of file paths to attach
        subject: Email subject (optional)
        body: Email body text (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        teacher_email = os.getenv("TEACHER_EMAIL")
        
        if not all([sender_email, sender_password, teacher_email]):
            print("❌ Email credentials not configured in .env file")
            return False
        
        # Initialize yagmail
        yag = yagmail.SMTP(sender_email, sender_password)
        
        # Default subject and body if not provided
        if subject is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            subject = f"📊 Attendance Report - {date_str}"
        
        if body is None:
            body = f"""
            <html>
            <body>
                <h2>Daily Attendance Report</h2>
                <p>Dear Teacher,</p>
                <p>Please find attached the attendance reports for today:</p>
                <ul>
                    <li><b>Daily Attendance Log:</b> Contains all attendance records with timestamps</li>
                    <li><b>Student Statistics:</b> Shows attendance percentage and late arrival count for each student</li>
                </ul>
                <p>This is an automated email from the Smart Attendance System.</p>
                <br>
                <p>Best regards,<br>Smart Attendance System</p>
            </body>
            </html>
            """
        
        # Send email with attachments
        yag.send(
            to=teacher_email,
            subject=subject,
            contents=body,
            attachments=csv_files
        )
        
        print(f"✅ Email sent successfully to {teacher_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False


def send_daily_report(daily_log_path, stats_path):
    """
    Send daily attendance report with both CSV files
    
    Args:
        daily_log_path: Path to daily attendance CSV
        stats_path: Path to student statistics CSV
    
    Returns:
        bool: True if successful
    """
    attachments = []
    
    # Check if files exist
    if os.path.exists(daily_log_path):
        attachments.append(daily_log_path)
    else:
        print(f"⚠️ Daily log not found: {daily_log_path}")
    
    if os.path.exists(stats_path):
        attachments.append(stats_path)
    else:
        print(f"⚠️ Statistics file not found: {stats_path}")
    
    if not attachments:
        print("❌ No files to send")
        return False
    
    return send_attendance_email(attachments)
