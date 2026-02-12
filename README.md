# Smart Attendance System

A face-recognition based attendance system with a client camera UI and a Flask server for recognition, logging, and email reporting.

## Features
- Blink-to-scan client UI with a futuristic HUD
- Face recognition with per-student datasets
- Attendance logging and late detection
- Intruder capture after repeated unknowns
- Daily email report with statistics

## Architecture
- Client: captures frames and sends them to the server
- Server: identifies faces, logs attendance, and sends reports

## Folder Structure
```
Smart-Attendance-System/
	client/
		main.py
		ui_helper.py
	server/
		app.py
		database_mgr.py
		mail_sender.py
		processor.py
		send_email_report.py
		test_email_feature.py
	.env.example
	.gitignore
	config.py
	requirements.txt
```

## Requirements
- Python 3.9+ (3.10 or 3.11 recommended)
- A webcam for the client
- Windows users: C++ Build Tools may be required for `face_recognition`

## Setup
1) Create and activate a virtual environment.
2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Create a `.env` file from the example:

```bash
copy .env.example .env
```

4) Update `.env` values:
- `SENDER_EMAIL`
- `SENDER_PASSWORD` (Gmail App Password)
- `TEACHER_EMAIL`
- `API_SECRET_KEY`

## Dataset
Place student images in:

```
server/dataset/<student_name>/*.jpg
```

Each folder name is treated as the student identity.

## Run
Start the server:

```bash
python server/app.py
```

Start the client (in a new terminal):

```bash
python client/main.py
```

## API
- `POST /recognize` (header: `X-API-KEY`) with `image` file
- `POST /send_report` (header: `X-API-KEY`) to email the daily report
- `GET /statistics` (header: `X-API-KEY`) to fetch attendance statistics

## Reports
- Logs are saved to `logs/attendance_YYYY-MM-DD.csv`
- Statistics are saved to `logs/student_statistics.csv`

You can also manually send a report:

```bash
python server/send_email_report.py
```

## Security Notes
This project uses an API key stored in `.env` and ignores sensitive files in `.gitignore`.
For production, consider:
- Use HTTPS (reverse proxy like Nginx/Caddy)
- Rotate the API key and use a longer random value
- Add request size limits and file-type validation
- Add rate limiting and audit logging
- Run the server behind a firewall and restrict access

## Troubleshooting
- If `face_recognition` fails to install, install Visual C++ Build Tools and retry.
- If email sending fails, confirm App Passwords are enabled and `.env` is set.

