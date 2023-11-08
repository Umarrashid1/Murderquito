import cv2
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.configure("preview")
picam2.start()
while True:
    frame  = picam2.capture_array()
    cv2.imshow("camera", frame)
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()