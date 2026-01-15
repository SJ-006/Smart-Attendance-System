from datetime import time

# SERVER NETWORK CONFIG
# While testing on one laptop, use "http://127.0.0.1:5000"
# When moving to Pi, you will change this to your Laptop's IP
SERVER_URL = "http://127.0.0.1:5000"

# ATTENDANCE LOGIC
CLASS_START_TIME = time(9, 0)       # Class starts at 09:00 AM
LATE_THRESHOLD_MINUTES = 15         # Students are marked 'Late' after 09:15 AM

# EMAIL SETTINGS
# Time to send the daily report to the HOD/Professor
REPORT_TIME = "17:00" 

# SECURITY
# How many times an unknown person is seen before saving their photo
UNKNOWN_THRESHOLD = 3