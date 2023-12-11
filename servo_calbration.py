import pickle
import cv2
import math
import glob
from camera import Camera
import numpy as np
from servo import Servo
from detection import Detector
from servo_controller import Servo_controller

class ServoCalibrator:
    
    cam_fov = 80
    cam_sensor_size = 1 # 1.22 micrometer × 1.22 micrometer     1 micrometer = 0,001mm eller tæt på
    cam_focal_length = 4.28 # mål i mm
    # cam_focal_ratio = 1.75
    cam_to_wall = 0

    def __init__(self, cam = Camera) -> None:
        self.dist_cam_axis_x = 4.3
        self.dist_cam_axis_y = 4.6
        self.dist_cam_axis_origin = math.sqrt(self.dist_cam_axis_x^2 + self.dist_cam_axis_y^2)
        self.px_height, self.px_width = cam.frame.shape
        self.center_coords = (self.px_width/2, self.px_height/2)




    def center_laser(self, cam, det, servo_c, dist_to_wall = None):
        #TODO: find elegant way of doing it. with and/or without trial&error / other way
        #ryk laser op/ned indtil den rammer midterlinjen
        coords = det.find_red(cam)
        center = (1280/2,720/2)
        if coords == center:
            print('oops coords == center')
            return True
        elif dist_to_wall is not None:
          angles = self.calc_centerangle_from_distance( det, servo_c, dist_to_wall)
          servo_c.servo_x.move(angles[0])
          servo_c.servo_y.move(angles[1])
          return True  
        else:
            servo_c.servo_x.move(100)
            angle_servo_x = 100
            servo_c.servo_y.move(128)
            angle_servo_y = 128

            while(det.find_red('x') < center[0]):
                angle_servo_y = angle_servo_y + 1
                servo_c.servo_y.move(angle_servo_y)
            while(det.find_red('x') > center[0]):
                angle_servo_y = angle_servo_y - 1
                servo_c.servo_y.move(angle_servo_y)
            while(det.find_red('y') > center[1]):
                angle_servo_x = angle_servo_x + 1
                servo_c.servo_x.move(angle_servo_x)
            while(det.find_red('y') < center[1]):
                angle_servo_x = angle_servo_x - 1
                servo_c.servo_x.move(angle_servo_x)

            return True

    def calc_centerangle_from_distance(self, det, servo_c, dist_to_wall):
    # Given α(angle of corner at wall): β(angle of laser corner) = 90 - α
    # β = arctan(b / a)     OR     β = arccot(a / b)
        #vinklen for hvor laser ville møde midten af kameraet
        #   β=arctan(b/a)
        if(det.find_red == self.center_coords):
            return (servo_c.servo_x.angle, servo_c.servo_y.angle)
        else:
            #self.laser_to_center_angle_origin = 90 - math.atan(self.cam_to_wall/self.dist_cam_axis_origin)
            self.laser_to_center_angle_x =  math.atan(dist_to_wall/self.dist_cam_axis_x) + 90 + servo_c.servo_y.angle_offset
            self.laser_to_center_angle_y =  math.atan(dist_to_wall/self.dist_cam_axis_y) + 90 + servo_c.servo_x.angle_offset
            return (self.laser_to_center_angle_y, self.laser_to_center_angle_x)
        
    def calc_dist_from_centerangle(self, cam = Camera, det = Detector, servo_c = Servo_controller):
        #laseren skal  vaere centreret
        # b = a × tan(β)
        angle_x = servo_c.servo_x.angle - 10
        angle_y = servo_c.servo_y.angle - 38
        if angle_x > 90: angle_x - 90 
        if angle_y > 90: angle_y - 90
            
        dot_coord_x, dot_coord_y = det.find_red(cam)
        if ((dot_coord_x, dot_coord_y) == self.center_coords):
            # b = a × tan(β)
            cam_to_wall_x = self.dist_cam_axis_y * math.tan(angle_y)
            cam_to_wall_y = self.dist_cam_axis_x * math.tan(angle_x)
            #tjek om de giver den samme distance til væggen. returnerer om de giver den samme distance, og så en distance
            if cam_to_wall_x == cam_to_wall_y: 
                self.cam_to_wall = cam_to_wall_x
                return True, cam_to_wall_x
            else:
                self.cam_to_wall = (cam_to_wall_x + cam_to_wall_y / 2)
                return False, (cam_to_wall_x + cam_to_wall_y / 2)
            
        elif dot_coord_y == self.center_coords[1]: 
            self.cam_to_wall = self.dist_cam_axis_x * math.tan(angle_x)
            return False, self.cam_to_wall
        elif dot_coord_x == self.center_coords[0]: 
            self.cam_to_wall = self.dist_cam_axis_y * math.tan(angle_y)
            return False, self.cam_to_wall
        
        else: # do some conversion bullshit or center laser in frame idk
           # mid_to_dot_x = abs(dot_coord_x - self.center_coords[0])
           # mid_to_dot_y = abs(dot_coord_y - self.center_coords[1])
            #NotImplemented
            return False, 0
        
    def _calc_dim_conv_fact_perpendicular_laser(self, cam, det = Detector,  servo_c = Servo_controller):
        px_to_cm_heigth_scale = False 
        px_to_cm_width_scale = False
        coords =  det.find_red(cam)
        #hvis laseren er lige på, så er afstand fra midten til laserdot, det samme som kamera til laser

        if servo_c.servo_y is Servo and servo_c.servo_y.angle == 128:
            dot_offset_x = abs((self.px_width/2)- coords[0]) #abs for kun at få positv værdi
            px_to_cm_width_scale = (dot_offset_x / self.dist_cam_axis_y) 
        
        
        if servo_c.servo_x is Servo and servo_c.servo_x.angle == 100:
            dot_offset_y = abs((self.px_height/2)- coords[1]) #abs for kun at få positv værdi
            px_to_cm_heigth_scale = (dot_offset_y / self.dist_cam_axis_x)

        return px_to_cm_heigth_scale, px_to_cm_width_scale
    

    def _calc_dim_conv_fact_checkerboard(self, detector = Detector): NotImplemented       
    def _calc_dim_conv_fact_known_square(self, detector = Detector):NotImplemented

    def calc_dist_checkers(NotImplemented): NotImplemented     
    def calc_dist_box(): NotImplemented 