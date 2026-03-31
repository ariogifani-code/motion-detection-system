# Real-Time Motion Detection System (OpenCV)

## Overview
This project is a live motion detection system built using OpenCV and Python.  
It detects motion through a webcam frames, logs events, captures images/videos, and sends email notifications.

---

## Features
- Real-time motion detection using frame differencing
- Event logging with timestamps and duration
- Image capture when motion is detected
- Video recording mode
- Email notification system with cooldown
- FPS display
- On screen status and time display

---

## How It Works
1. Captures live frames from webcam  
2. Converts frames to grayscale and applies blur  
3. Compares current frame with previous frame  
4. Detects motion using thresholding and contours  
5. Triggers events when motion starts/stops  
6. Logs event details and optionally saves media
7. Sends email alerts when motion starts (with cooldown time)

---

## Technologies Used
- Python  
- OpenCV  
- smtplib (email alerts)  

---

## Email Configuration (Required)

To enable email notifications, you must provide your own email.

1. Open `motion_detector.py`

2. Locate the email configuration section:

   
      sender_email = "YOUR_EMAIL"


      sender_password = "YOUR_APP_PASSWORD" (ex.Gmail App Password - NOT your real Password)


      receiver_email = "RECEIVER_EMAIL"

## Output Directory

Captured images and videos are saved in the `SavedMotion/` folder.

The folder will be automatically created if it does not exist.

---

## Instructions

1. Clone the repository:
   
      git clone https://github.com/ariogifani-code/motion-detection-system.git

2. Install dependencies:
   
      pip3 install opencv-python

3. Run the Program:
   
      python3 motion_detector.py

Note: You can also run the program using your IDE (e.g., VS Code).
