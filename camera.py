import cv2
from picamera2 import Picamera2
from track import track

camera = Picamera2()
camera.start()
while True:
    frame  = camera.capture_array()
    cv2.imshow("camera", frame)
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()