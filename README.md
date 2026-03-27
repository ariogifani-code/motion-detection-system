# 🎥 Real-Time Motion Detection System (OpenCV)

## 📌 Overview
This project is a real-time motion detection system built using OpenCV and Python.  
It detects motion through a webcam feed, logs events, captures images/videos, and sends email alerts.

---

## 🚀 Features
- Real-time motion detection using frame differencing
- Event-based logging with timestamps and duration
- Image capture when motion is detected
- Video recording mode
- Email notification system with cooldown
- FPS (performance) display
- On-screen status and time display

---

## 🧠 How It Works
1. Captures live video from webcam  
2. Converts frames to grayscale and applies blur  
3. Compares current frame with previous frame  
4. Detects motion using thresholding and contours  
5. Triggers events when motion starts/stops  
6. Logs event details and optionally saves media  

---

## 🛠️ Technologies Used
- Python  
- OpenCV  
- smtplib (email alerts)  

---

## 🔐 Email Configuration (Required for Alerts)

To enable email notifications, you must provide your own email credentials.

1. Open `main.py`

2. Locate the email configuration section:
sender_email = "YOUR_EMAIL"
sender_password = "YOUR_APP_PASSWORD" (ex.Gmail App Password - NOT your real Password)
receiver_email = "RECEIVER_EMAIL"

---

## ⚙️ Instructions

1. Clone the repository:
git clone https://github.com/YOUR_USERNAME/motion-detection-system.git

2. Install dependencies:
pip3 install opencv-python

3. Run the Program:
python3 motion_detector.py
