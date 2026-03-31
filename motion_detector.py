"""
Real-Time Motion Detection System (OpenCV)

Description:
- Captures live video frames from webcam
- Detects motion using frame differencing
- Logs motion events with timestamps and duration
- Supports image capture and video recording modes
- Sends email alerts with cooldown control

Key Concepts:
- Frame differencing for motion detection
- Contour filtering to remove noise
- Event-based state tracking (motion start/end)
- Real-time performance monitoring (FPS)

Author: Ario Gifani
"""

#Key libraries for Computer Vision, Timing, Logging, and Email Alerts
import cv2
import time
import datetime
import smtplib
from email.mime.text import MIMEText

open("motion_log.txt", "a")

#Initialize webcam capture
cam = cv2.VideoCapture(0)

#Mode Selection: "image" (default), "video", or "None"
mode = "image"

#Video recording control variables
video_Writer = None
is_Recording = False

#Previous frame used for frame comparisons 
prev_Frame = None

#Motion state flag for previous frame (0 = no motion, 1 = motion)
prev_FLAG = 0

#FPS calculation tracking
prevFPS_time = 0

#Frame counter to warmup system
counter = 0
warmup_Frames = 10

#Motion Event Tracking 
event_Counter = 1
start_Dur = None

#Tracking Analytics
total_Motiontime = 0
maxDur = 0
minDur = 1000

#Dates and Times of motion (start and end)
first_Detect_Date = None
first_Detect_Time = None
last_Detect_Date = None
last_Detect_Time = None

#Email notification cooldown control (prevents email spamming)
last_email_time = 0
cooldown = 50


#Main processing loop: constantly captures and compares frames, detects motion, and handles events
while True:
    
    clock_Now = datetime.datetime.now()

    ret, curr_Frame = cam.read()

    height, width, _ = curr_Frame.shape 
    
    #Convert frame to grayscale and blur it to reduce noise and improve motion detection
    grayed_Frame = cv2.cvtColor(curr_Frame, cv2.COLOR_BGR2GRAY)
    blurred_Frame = cv2.GaussianBlur(grayed_Frame, (25,25), 0)

    #Skip initial warmup frames to allow camera to adjust (prevents false motion very early into the system) 
    if counter < warmup_Frames:
        prev_Frame = blurred_Frame
        cv2.imshow("Camera", curr_Frame)
        cv2.waitKey(1)
        counter += 1
        continue
 
    #Compute difference between current frame and previous frame
    diff_Value = cv2.absdiff(blurred_Frame, prev_Frame)

    #Apply threshold to allow binary representation and isolate motion regions 
    retval, binary_Image = cv2.threshold(diff_Value, 18, 255, cv2.THRESH_BINARY)

    #Extract contours to represent larger areas of motion
    contours, hierarchy = cv2.findContours(binary_Image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Calculate frames per second (FPS) for performance monitoring
    currFPS_Time = time.time()
    FPS = 1/(currFPS_Time - prevFPS_time)

    #Display system info on screen: Date, Time, FPS, Status
    clock_Date = clock_Now.strftime("%m-%d-%Y")
    clock_Time = clock_Now.strftime("%H:%M:%S")    
    cv2.putText(curr_Frame, clock_Date, (18, 1000), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(curr_Frame, clock_Time, (18, 1050), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)
    current_Time = time.perf_counter()
    cv2.putText(curr_Frame, f"Time: {current_Time:.3f}", (18, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(curr_Frame, "Status: ", (800, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)
    cv2.putText(curr_Frame, f"FPS: {FPS:.1f}", (1650, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)
    cv2.rectangle(curr_Frame, (10, 10), (1900, 65), (0, 0, 0), 2)
    
   
    current_FLAG = 0
    
    min_x = 2000
    min_y = 2000
    max_w = 0
    max_h = 0

    #Iterate through each detected contour and filter out small noise
    for contour in contours:
        contour_Area = cv2.contourArea(contour)
        #Ignore small noise that is detected 
        if contour_Area < 300:
            pass
        else:

            #Change in motion status
            current_FLAG = 1
            cv2.putText(curr_Frame, "Motion", (1000, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)
                
            #Track max/min coordinates to create a bounding box around motion detected 
            x, y, w, h = cv2.boundingRect(contour)
            if(x < min_x):
                min_x = x
            if(y < min_y):
                min_y = y
            if(w > max_w):
                max_w = w
            if(h > max_h):
                max_h = h

            rect_Start_Point = (min_x, min_y)
            rect_End_Point = (min_x + max_w + 100, min_y + max_h)

    #Detect transition: no motion -> motion (start of a new event)
    if(prev_FLAG == 0 and current_FLAG == 1):
        start_Dur = time.perf_counter()
        clock_Start = datetime.datetime.now()
        clock_Date_Start = clock_Now.strftime("%m-%d-%Y")
        clock_Time_Start = clock_Now.strftime("%H:%M:%S")

        if (event_Counter == 1):
            first_Detect_Date = clock_Date_Start
            first_Detect_Time = clock_Time_Start

        last_Detect_Date = clock_Date_Start
        last_Detect_Time = clock_Time_Start

        print(f"MOTION DETECTED at: {current_Time:.2f} seconds \n")

        #Send email alert to recipient with cooldown to prevent spamming emails
        email_time = time.time()
        if (email_time - last_email_time) > cooldown:
            msg = MIMEText(f"MOTION DETECTED ALERT\n\nA motion event has been detected by your monitoring system.\n\nEvent Details\n\nEvent ID:\t{event_Counter}\nDate:\t\t{clock_Date}\nTime:\t\t{clock_Time}\n\nStatus:\t\t\tMotion Detected\nCamera ID:\tDefault Camera (0)\n\nThis is an automated message from your Motion Detection System.")

            # -------------------------------
            # EMAIL CONFIGURATION (USER INPUT REQUIRED)
            # -------------------------------
            
            sender_email = "motionalertsystem92@gmail.com"
            sender_password = "amganfzvnnbvovgv"
            receiver_email = "ariogifani@gmail.com"
            # -------------------------------
            
            msg["Subject"] = "Motion Alert"
            msg["From"] = sender_email
            msg["To"] = receiver_email

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(sender_email, sender_password)

            server.send_message(msg)

            server.quit() 
            last_email_time = email_time 

        

        #Take image screenshot when motion is detected and save on dedicated directory
        if(mode == "image"):
            cv2.imwrite(f"MotionDetection_System/SavedMotion/motion_detected_{current_Time:.1f}_{clock_Date_Start}.jpg", curr_Frame)

        #Start video recording once motion has begun
        if (mode == "video"):
            filename = f"MotionDetection_System/SavedMotion/motion_detected_{event_Counter}_{clock_Date_Start}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_Writer = cv2.VideoWriter(filename, fourcc, 30, (width, height))
            is_Recording = True
            

    #Detect transition: motion -> no motion (end of event)
    if(current_FLAG == 0 and prev_FLAG == 1):
        if(start_Dur == None):
            continue
        end_Dur = time.perf_counter()
        elapsed_Dur = end_Dur - start_Dur
        total_Motiontime = total_Motiontime + elapsed_Dur
        if(elapsed_Dur > maxDur):
            maxDur = elapsed_Dur

        if(elapsed_Dur < minDur):
            minDur = elapsed_Dur

        #Stop video recording once motion has stopped
        if(mode == "video"):
            if is_Recording:
                video_Writer.release()
                is_Recording = False
        
        #Log motion event details to text file (start, end, duration)
        with open("motion_log.txt", "a") as f:
            f.write(f"Event {event_Counter}\n")
            f.write(f"Start Time: {clock_Date_Start}, {clock_Time_Start} \n")
            f.write(f"End Time: {clock_Date}, {clock_Time} \n")
            f.write(f"Duration: {elapsed_Dur:.2f} seconds \n \n")
        
        event_Counter = event_Counter + 1



    #Write frames to video file if recording is active
    if is_Recording and mode == "video":
        video_Writer.write(curr_Frame)
    

    if(current_FLAG == 1):
        cv2.rectangle(curr_Frame, rect_Start_Point, rect_End_Point, (0, 255, 0), 3)
        if is_Recording and mode == "video":
            video_Writer.write(curr_Frame)


    #Display all changes frame changes on screen
    cv2.imshow("Camera", curr_Frame)

    #Update previous frame and flags for next iteration
    prev_FLAG = current_FLAG
    prev_Frame = blurred_Frame
    prevFPS_time = currFPS_Time
    
    #Close the window whenever ready (ESC = 27 in ASCII)
    if cv2.waitKey(1) == 27: #press ESC
        break

#Release resources and close all windows
if video_Writer is not None:
    video_Writer.release()
cam.release()
cv2.destroyAllWindows()

#Write summary analytics of all motion events to log file
with open("motion_log.txt", "a") as f:
    f.write("\n===========================================================\n\t\t\t\t\tMOTION ANALYTICS\n===========================================================\n\n")
    f.write(f"Date:\t{clock_Date_Start}\t\tTime:\t{clock_Time}\n\n")
    f.write(f"Total Events:\t\t\t{event_Counter - 1}\n\n")
    f.write(f"Total Active Time:\t\t{current_Time:.2f}\n")
    avg_Motiontime = total_Motiontime/(event_Counter - 1)
    f.write(f"Avg Event Duration:\t\t{avg_Motiontime:.2f}\n\n")
    f.write(f"First Detection:\t\t{first_Detect_Date}\t{first_Detect_Time}\n")
    f.write(f"Last Detection:\t\t\t{last_Detect_Date}\t{last_Detect_Time}\n\n")
    f.write(f"Max Duration:\t\t\t{maxDur:.2f}\n")
    f.write(f"Min Duration:\t\t\t{minDur:.2f}\n\n")
    f.write("===========================================================\n\n\n\n")
