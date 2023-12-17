import cv2
import sys
import time
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
frame_counter = 0


def get_frame_counter():
    return frame_counter


start_time = time.time()
fps = 0


while True:
    frame_counter += 1
    frame = cam.run()
    det.update_tracker(cam)
    det.draw_cross(cam)
    det.draw_boundingbox(cam, fps)
    coordinates = det.get_center_coordinates()
    print(coordinates)
    if coordinates[0] != 0 or coordinates[1] != 0:
        servo_c.move(coordinates, linear_ratio, frame)

     # Calculate FPS every  frames

    end_time = time.time()
    elapsed_time = end_time - start_time
    fps = round(frame_counter / elapsed_time)




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
