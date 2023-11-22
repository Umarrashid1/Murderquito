import cv2
from picamera2 import Picamera2
from camera import Camera
from detection import Detection

#No Camera() input parameter for picam
cam = Camera(1)
det = Detection(cam)

while True:
    frame = cam.run()
    det.update_tracker(cam)
    det.draw_boundingbox(cam)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

