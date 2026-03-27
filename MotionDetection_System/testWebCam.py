#This python file tests whether your webcam is working sufficiently and displaying on the screen

import cv2

#Initialize webcam capture
cap = cv2.VideoCapture(0)

#Constantly track frames using the webcam
while True:
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)


    #Close the window whenever ready (ESC = 27 in ASCII)
    if cv2.waitKey(1) == 27: #press ESC
        break

#Release resources and close windows
cap.release()
cv2.destroyAllWindows()