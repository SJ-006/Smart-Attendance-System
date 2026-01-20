"""
Utility script to manually send attendance reports via email
This can be run independently or scheduled using Windows Task Scheduler
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.database_mgr import save_student_statistics
from server.mail_sender import send_daily_report
from datetime import datetime

def send_attendance_report():
    """
    Generate statistics and send attendance report email
    """
    print("=" * 60)
    print("📧 Attendance Report Email Sender")
    print("=" * 60)
    
    try:
        # Generate student statistics
        print("\n📊 Generating student statistics...")
        stats_path = save_student_statistics()
        
        # Get today's attendance log path
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        daily_log_path = os.path.join(log_dir, f"attendance_{date_str}.csv")
        
        print(f"\n📄 Files to send:")
        print(f"  1. Daily Log: {daily_log_path}")
        print(f"  2. Statistics: {stats_path}")
        
        # Check if daily log exists
        if not os.path.exists(daily_log_path):
            print(f"\n⚠️  Warning: No attendance recorded for today ({date_str})")
            print("   Only statistics file will be sent.")
        
        # Send email
        print("\n📧 Sending email...")
        success = send_daily_report(daily_log_path, stats_path)
        
        if success:
            print("\n✅ SUCCESS! Attendance report sent successfully!")
        else:
            print("\n❌ FAILED! Could not send email. Check your email settings in .env file")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    send_attendance_report()
