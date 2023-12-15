import time
import cv2
import sys
from camera import Camera
from camera_calibration import CameraCalibrator
from detection import Detector
from servo_controller import  Servo_controller
from servo_calibrator import  ServoCalibrator
from laser import Laser

#Get CLI arguments
args = sys.argv[1:]
if len(args)>0:
    input_param = int(args[0])
else:
    input_param = None
laser = Laser()
laser.toggle_laser(0)

cam = Camera(input_param)
cam.run()
cv2.imwrite("ref_frame.jpg", cam.run())
servo_c = Servo_controller()
servo_cal = ServoCalibrator(cam, servo_c)
det = Detector(cam)
laser.toggle_laser()
#chosen_servo = 'y' #er måske smartere at finde vinklerne indivduelt, så de ikke påvirker hinanden
#if chosen_servo == 'x': 
    #servo_cal.prepare_for_calibration(servo_c, chosen_servo)
#elif chosen_servo == 'y': 
    #servo_cal.prepare_for_calibration(servo_c, chosen_servo)
#servo_cal.find_indiv_center_angles(cam, det, servo_c, chosen_servo)        
#identical, distance = servo_cal.calc_dist_from_centerangle(servo_c)

servo_cal.prepare_for_calibration(det, cam, servo_c)
servo_cal.center_laser(cam, det, servo_c) # virker!      
identical, distance2 = servo_cal.calc_dist_from_centerangle(servo_c)
if identical is True : print('siiiiiick')
laser.toggle_laser()
px_to_cm_x, px_to_cm_y = servo_cal.calc_dim_conv_fact_perpendicular_laser()
phys_angles = servo_cal.get_angle_for_coords((520,220))
servo_c.pan_servo.move(100 + phys_angles[0])
time.sleep(2)
servo_c.tilt_servo.move(128 + phys_angles[1])
time.sleep(2)
laser.fire_pulse()
#time.sleep(120)
cam_cal = CameraCalibrator(cam.get_frame())
cal_matrix, cal_dist = cam_cal.run_calibrations()
'''
while True:
    frame = cam.run()
    det.update_tracker(cam)
   
    det.find_red(frame)
    center_coordinates = det.find_red(frame)
    if center_coordinates:
        print("Red dot found at:", center_coordinates)
    else:
        print("No red dot found.")

    det.draw_cross(cam)
    det.draw_boundingbox(cam)

    coordinates = det.get_center_coordinates()
    laser.toggle_laser()
    print("coordinates are", coordinates)
    #servo_c.move(coordinates)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        laser.toggle_laser(0)
        break
    '''
# ##########    se evt:     ######################
#   https://www.youtube.com/watch?v=1CVmjTcSpIw
#   https://www.youtube.com/watch?v=sW4CVI51jDY&t=1202s
#   OneNote -> Vidensindsamling -> Computer Visualization og openCV -> GODE VIDEOER
######################################
