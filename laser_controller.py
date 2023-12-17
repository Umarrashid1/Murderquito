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


frame = cam.get_frame()
frame_height, frame_width, _ = frame.shape
height_eights = frame_height/8
width_eights = frame_width/8
real_coords_column = []
laser_coords_column = []
real_coords_all = []
laser_coords_all = []
for x in range(7):
    width_eights = width_eights * (x+1)
    for y in range(7):
        frame = cam.run()
        height_eights = height_eights * (x+1)
        servo_c.move((width_eights,height_eights), linear_ratio, frame)
        laser_coords_column[y] = det.find_red(frame)
        real_coords[y] = (width_eights,height_eights)
    
    real_coords_all[x] = real_coords_column
    laser_coords_all[x] = laser_coords_column

with open('real_coords_all.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(real_coords_all)

# Write laser_coords_all to a CSV file
with open('laser_coords_all.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(laser_coords_all)