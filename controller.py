import cv2
from picamera2 import Picamera2
from camera import Camera

cam = Camera()
cam.init()
cam.start()
cam.autofocus()

while True:
    frame = cam.run()
    cam.show("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

