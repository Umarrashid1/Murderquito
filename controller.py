import cv2
import sys
from camera import Camera
from detection import Detection


#Get CLI arguments
args = sys.argv[1:]
if len(args)>0:
    input_param = int(args[0])
else:
    input_param = None

cam = Camera(input_param)
det = Detection(cam)


while True:
    frame = cam.run()
    det.update_tracker(cam)
    det.draw_boundingbox(cam)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
