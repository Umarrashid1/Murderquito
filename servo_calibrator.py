import pickle
import cv2
import math
import glob
from camera import Camera
import numpy as np
from servo import Servo
from detection import Detector
from servo_controller import Servo_controller
import time

class ServoCalibrator:
    
    cam_fov = 80
    cam_sensor_size = 1 # 1.22 micrometer × 1.22 micrometer     1 micrometer = 0,001mm eller tæt på
    cam_focal_length = 4.28 # mål i mm
    # cam_focal_ratio = 1.75
    cam_to_wall = 0

    def __init__(self, cam = Camera, servo_c = Servo_controller) -> None:
        self.cam_to_tilt_dist = 43
        self.cam_to_pan_dist = 46
        self.dist_cam_axis_origin = math.sqrt(self.cam_to_tilt_dist*self.cam_to_tilt_dist + self.cam_to_pan_dist*self.cam_to_pan_dist)
        self.px_height, self.px_width, self.channels = cam.frame.shape
        self.center = (self.px_width/2, self.px_height/2)


    def prepare_for_calibration(self, servo_c, choice = None):
        self.pan_angle, self.tilt_angle = servo_c.make_laser_perpendicular()
        if(choice is None or choice == 'x'):
            servo_c.pan_servo.move(102)
            self.pan_angle = 102
            time.sleep(2)
        if(choice is None or choice == 'y'):
            servo_c.tilt_servo.move(135)
            self.tilt_angle = 135
            time.sleep(2)


    def center_laser(self, cam, det, servo_c, dist_to_wall = None):
        center = self.center

        if dist_to_wall is not None:
          self.cam_to_wall = dist_to_wall
          angles = self.calc_centerangle_from_distance( det, servo_c, dist_to_wall)
          servo_c.pan.move(angles[0])
          servo_c.tilt.move(angles[1])
          return True
          
        else: 
            las_is_centered = False 
            while las_is_centered is False:
                frame = cam.run()
                las_coords = det.find_red(frame)
                if las_coords is False:
                    print("Error: no laser found!")
                if(las_coords[0] != center[0]):
                    if(las_coords[0] > center[0] and self.pan_angle < 180):
                        if(las_coords[0] > center[0] + 20 and self.pan_angle < 180):
                            self.pan_angle = self.pan_angle + 1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(1)
                        elif(las_coords[0] > center[0] + 10 and self.pan_angle < 180):
                            self.pan_angle = self.pan_angle + 0.1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.5)
                        else:
                            self.pan_angle = self.pan_angle + 0.5
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.2)
                    elif(las_coords[0] < center[0] and self.pan_angle > 0):
                        if(las_coords[0] < center[0] - 20 and self.pan_angle > 0):
                            self.pan_angle = self.pan_angle - 1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(1)
                        elif(las_coords[0] < center[0] - 10 and self.pan_angle > 0):
                            self.pan_angle = self.pan_angle - 0.1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.5)
                        else:
                            self.pan_angle = self.pan_angle - 0.05
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.2)
                if(las_coords[1] != center[1]):
                    if(las_coords[1] < center[1] and self.tilt_angle < 180):
                        if(las_coords[1] < center[1]-20 and self.tilt_angle < 180):
                            self.tilt_angle = self.tilt_angle + 1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(1)
                        elif(las_coords[1] < center[1]-10 and self.tilt_angle < 180):
                            self.tilt_angle = self.tilt_angle + 0.1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.5)
                        else:
                            self.tilt_angle = self.tilt_angle + 0.05
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.2)
                    elif(las_coords[1] > center[1] and self.tilt_angle > 0):
                        if(las_coords[1] > center[1] + 20 and self.tilt_angle < 180):
                            self.tilt_angle = self.tilt_angle - 1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(1)
                        elif(las_coords[1] > center[1] + 10 and self.tilt_angle < 180):
                            self.tilt_angle = self.tilt_angle - 0.1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.5)
                        else:
                            self.tilt_angle = self.tilt_angle - 0.05
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.2)            
                if(las_coords[1] < center[1] * 1.05 and las_coords[1] > center[1] *0.95):
                    if(las_coords[0] < center[0] *1.05 and las_coords[0] > center[0] *0.95):
                        las_is_centered = True
                        return True

            
            

    def find_indiv_center_angles(self,cam, det, servo_c, chosen_servo = None):
        center = self.center

        if chosen_servo == 'x':
            servo = 0
            angle = self.pan_angle
        elif chosen_servo == 'y':
            servo = 1
            angle = self.tilt_angle
        
        center_angle_found = False
        while center_angle_found is False:
            frame = cam.run()
            las_cord = det.find_red(frame)
            print(las_cord)
            if(las_cord[servo] != center[servo]):
                if(las_cord[servo] > center[servo]):
                    if(las_cord[servo] > center[servo] + 20):
                        angle = angle - 1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(1)
                    elif(las_cord[servo] > center[servo] + 10):
                        angle = angle - 0.1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                    else:
                        angle = angle - 0.05
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                elif(las_cord[servo] < center[servo]):
                    if(las_cord[servo] < center[servo] - 20):
                        angle = angle + 1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(1)
                    elif(las_cord[servo] < center[servo] - 10):
                        angle = angle + 0.1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                    else:
                        angle = angle + 0.05
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                if chosen_servo == 'y':
                        self.tilt_angle = angle
                elif chosen_servo == 'x':
                        self.pan_angle = angle
                if(las_cord[servo] < center[servo] + 2 and las_cord[servo] > center[servo] - 2):
                    return True
        
        
    def calc_centerangle_from_distance(self, det, servo_c, dist_to_wall):
        # Given α(angle of corner at wall): β(angle of laser corner) = 90 - α
                # β = arctan(b / a)     OR     β = arccot(a / b)
        #self.laser_to_center_angle_origin = 90 - math.atan(self.cam_to_wall/self.dist_cam_axis_origin)
        self.centered_tilt_angle =  math.atan(dist_to_wall/self.cam_to_tilt_dist) # + 90 + servo_c.tilt.angle_offset
        self.centered_pan_angle =  math.atan(dist_to_wall/self.cam_to_pan_dist) # + 90 + servo_c.pan.angle_offset
        return (self.centered_pan_angle, self.centered_tilt_angle)
        
    def calc_dist_from_centerangle(self, servo_c = Servo_controller, choice = None):
        #laseren skal  vaere centreret
        # b = a × tan(β)
        pan_angle = servo_c.pan_servo.angle - 10
        tilt_angle = servo_c.tilt_servo.angle - 38
        pan_angle = pan_angle - 90
        tilt_angle = tilt_angle - 90
        pan_angle = 90 - pan_angle
        tilt_angle = 90 - tilt_angle
        print(pan_angle)
        print(tilt_angle)
        print('hhhhhhhhhmmmmmmmmm')    
        # b = a × tan(β)
        cam_to_wall_x = self.cam_to_pan_dist * (math.tan(tilt_angle))
        cam_to_wall_y = self.cam_to_tilt_dist * (math.tan(tilt_angle)) 
        print(cam_to_wall_x)
        print(cam_to_wall_y)

        #cam_to_wall_x = self.cam_to_tilt_dist * (math.tan(tilt_angle))
        #cam_to_wall_y = self.cam_to_pan_dist  * (math.tan(pan_angle)) 
        return(cam_to_wall_x,cam_to_wall_y)

        #tjek om de giver den samme distance til væggen. returnerer om de giver den samme distance, og så en distance
        if cam_to_wall_x == cam_to_wall_y: 
                self.cam_to_wall = cam_to_wall_x
                return True, cam_to_wall_x
        elif (choice == 'x'):
            return cam_to_wall_y
        elif(choice == 'y'):
            return cam_to_wall_x
        else:
            self.cam_to_wall = (cam_to_wall_x + cam_to_wall_y / 2)
            return False, (cam_to_wall_x + cam_to_wall_y / 2)


  
    

    def _calc_dim_conv_fact_checkerboard(self, detector = Detector): NotImplemented       
    def _calc_dim_conv_fact_known_square(self, detector = Detector):NotImplemented

    def calc_dist_checkers(NotImplemented): NotImplemented     
    def calc_dist_box(): NotImplemented 
    def _calc_dim_conv_fact_perpendicular_laser(self, frame, det = Detector,  servo_c = Servo_controller):
    
        servo_c.make_laser_perpendicular()
        las_coords =  det.find_red(frame)
        #hvis laseren er lige på, så er afstand fra midten til laserdot, det samme som kamera til laser
        #pixel_dist = lascoords - self.center

            #dot_offset_x = abs((self.px_width/2)- coords[0]) #abs for kun at få positv værdi
            #px_to_cm_width_scale = (dot_offset_x / self.cam_to_pan_dist)
        
        
        #if servo_c.pan_servo is Servo and servo_c.pan_servo.angle == 100:
         #   dot_offset_y = abs((self.px_height/2)- coords[1]) #abs for kun at få positv værdi
          #  px_to_cm_heigth_scale = (dot_offset_y / self.cam_to_tilt_dist)

        # return px_to_cm_heigth_scale, px_to_cm_width_scale