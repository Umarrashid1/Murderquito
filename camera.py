import cv2
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.configure("preview")
picam2.start()
while True:
    frame  = picam2.capture_array()
    cv2.imshow("camera", frame)
break
cv2.destroyAllWindows()