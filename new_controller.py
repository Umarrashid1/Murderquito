import cv2
import sys

import calc_distance
from servo_controller import Servo_controller
from camera import Camera
from detection import Detector

# Get CLI arguments
args = sys.argv[1:]
if len(args) > 0:
    input_param = int(args[0])
else:
    input_param = None

cam = Camera(input_param)
det = Detector(cam)
servo_c = Servo_controller()
linear_ratio = calc_distance.find_linear_ratio(cam)

while True:
    frame = cam.run()
    det.update_tracker(cam)
    det.draw_cross(cam)
    det.draw_boundingbox(cam)
    coordinates = det.get_center_coordinates()
    print(coordinates)
    servo_c.move(coordinates, linear_ratio, frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
