"""
Test script to verify email and statistics functionality
Creates sample data and tests the email sending feature
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datetime import datetime, timedelta
from server.database_mgr import save_student_statistics, generate_student_statistics
from server.mail_sender import send_daily_report

def create_sample_data():
    """Create sample attendance data for testing"""
    print("📝 Creating sample attendance data...")
    
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create data for the last 5 days
    students = ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Eve Wilson"]
    
    for day_offset in range(5):
        date = datetime.now() - timedelta(days=day_offset)
        date_str = date.strftime("%Y-%m-%d")
        
        records = []
        for student in students:
            # Randomly assign on-time or late status
            import random
            if random.random() > 0.3:  # 70% attendance rate
                status = "On Time" if random.random() > 0.2 else "Late"  # 20% late rate
                time_str = f"09:{random.randint(0, 30):02d}:00"
                records.append({
                    "Name": student,
                    "Time": time_str,
                    "Status": status
                })
        
        if records:
            df = pd.DataFrame(records)
            file_path = os.path.join(log_dir, f"attendance_{date_str}.csv")
            df.to_csv(file_path, index=False)
            print(f"  ✅ Created: attendance_{date_str}.csv ({len(records)} records)")


def test_statistics():
    """Test statistics generation"""
    print("\n📊 Testing statistics generation...")
    
    stats_df = generate_student_statistics()
    
    if stats_df.empty:
        print("  ⚠️  No statistics generated (no attendance data)")
        return False
    
    print(f"  ✅ Generated statistics for {len(stats_df)} students")
    print("\n" + "="*80)
    print(stats_df.to_string(index=False))
    print("="*80)
    
    # Save statistics
    stats_path = save_student_statistics()
    print(f"\n  ✅ Saved to: {stats_path}")
    
    return True


def test_email():
    """Test email sending"""
    print("\n📧 Testing email functionality...")
    
    # Get file paths
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    daily_log_path = os.path.join(log_dir, f"attendance_{date_str}.csv")
    stats_path = os.path.join(log_dir, "student_statistics.csv")
    
    # Check if files exist
    if not os.path.exists(stats_path):
        print("  ⚠️  Statistics file not found. Generating...")
        save_student_statistics()
    
    # Send email
    print(f"\n  📄 Daily Log: {daily_log_path}")
    print(f"  📄 Statistics: {stats_path}")
    print("\n  🚀 Sending email...")
    
    success = send_daily_report(daily_log_path, stats_path)
    
    if success:
        print("\n  ✅ Email sent successfully!")
        print("  📬 Check the teacher's inbox")
        return True
    else:
        print("\n  ❌ Email sending failed")
        print("  💡 Check your .env file configuration")
        return False


def main():
    print("=" * 80)
    print("🧪 ATTENDANCE EMAIL FEATURE - TEST SUITE")
    print("=" * 80)
    
    # Ask user what to test
    print("\nWhat would you like to test?")
    print("1. Create sample data")
    print("2. Generate statistics only")
    print("3. Send test email")
    print("4. Full test (all of the above)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    print("\n" + "=" * 80)
    
    if choice == "1":
        create_sample_data()
    elif choice == "2":
        test_statistics()
    elif choice == "3":
        test_email()
    elif choice == "4":
        create_sample_data()
        if test_statistics():
            test_email()
    else:
        print("❌ Invalid choice")
    
    print("\n" + "=" * 80)
    print("✅ Test completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
