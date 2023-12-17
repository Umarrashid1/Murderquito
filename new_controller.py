import cv2
import sys
import time
import calc_distance
from servo_controller import Servo_controller
from camera import Camera
from detection import Detector
import csv

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



elapsed_times = []
for i in range(1000):
    frame_counter += 1
    start_time = time.time()
    frame = cam.run()
    det.update_tracker(cam, frame_counter)
    det.draw_cross(cam)
    det.draw_boundingbox(cam)
    coordinates = det.get_center_coordinates()
    print(coordinates)
    if coordinates[0] != 0 or coordinates[1] != 0:
        servo_c.move(coordinates, linear_ratio, frame)

     # Calculate FPS every  frames

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_times.append(elapsed_time)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

results = det.__getattribute__("fail_array")
with open('fails.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Frame Counter", "Status"])
    # Write the data
    for result in results:
        writer.writerow(result)

with open('elapsed_times.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Elapsed Time"])
    for elapsed_time in elapsed_times:
        writer.writerow([elapsed_time])
