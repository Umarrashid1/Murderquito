import inspect
import sys
import os
import cv2
import sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from camera import Camera
from detection import Detector
from servo_controller import  Servo_controller
from servo_calbration import  ServoCalibrator
from laser import Laser

#Get CLI arguments
args = sys.argv[1:]
if len(args)>0:
    input_param = int(args[0])
else:
    input_param = None

servo_c = Servo_controller()
cam = Camera(input_param)
cv2.imwrite("ref_frame.jpg", cam.get_frame())
det = Detector(cam)
servo_cal = ServoCalibrator(cam, servo_c)
laser = Laser()
laser.toggle_laser()

check = False
frame = cam.run()
chosen_servo = 'y'
# servox virker ikke. ved vinkelret bevæger den sig ikke ind i billedet
if chosen_servo == 'x': servo_cal.prepare_for_calibration(servo_c, chosen_servo)
#y virker
elif chosen_servo == 'y': servo_cal.prepare_for_calibration(servo_c, chosen_servo)
while(check is False):
    frame = cam.run()
    check = servo_cal.find_indiv_center_angles(frame, det, servo_c, chosen_servo)        
identical, distance = servo_cal.calc_dist_from_centerangle(servo_c)

check = False
servo_cal.prepare_for_calibration(servo_c)
while(check is False):
    frame = cam.run()
    check = servo_cal.center_laser(frame, det, servo_c) # virker!      
identical, distance2 = servo_cal.calc_dist_from_centerangle(servo_c)
laser.toggle_laser()
