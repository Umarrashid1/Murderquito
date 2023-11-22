import cv2
from camera import Camera
from detection import Detection

#No Camera() input parameter for picam
cam = Camera()
det = Detection(cam)

while True:
    frame = cam.run()
    det.update_tracker(cam)
    det.draw_boundingbox(cam)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

