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
    det.draw_cross(cam)
    det.draw_boundingbox(cam)

    coordinates = det.get_center_coordinates()
    print(coordinates[0], coordinates[1])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
