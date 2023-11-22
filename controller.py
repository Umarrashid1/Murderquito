import cv2
from picamera2 import Picamera2
from camera import Camera
from detection import Detection

cam = Camera()
det = Detection(cam)

while True:
    frame = cam.run()
    det.update_tracker(cam)
    frame_boundingbox = det.draw_boundingbox(cam)
    cam.show("Murderquito", frame_boundingbox)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

