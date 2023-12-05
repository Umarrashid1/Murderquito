import pickle
import cv2
import math
import glob
from camera import Camera
import numpy as np
from servo import Servo
from detection import Detector

class ServoCalibrator:
    
    cam_fov = 80
    cam_sensor_size = 1 # 1.22 micrometer × 1.22 micrometer     1 micrometer = 0,001mm eller tæt på
    cam_focal_length = 4.28 # mål i mm
    # cam_focal_ratio = 1.75
    cam_to_wall = 30

    def __init__(self, detector = Detector, axis_x_dist = int, axis_y_dist = int) -> None:
        self.dist_cam_axis_x = axis_x_dist
        self.dist_cam_axis_y = axis_y_dist
        self.dist_cam_axis_origin = math.sqrt(self.dist_cam_axis_x^2 + self.dist_cam_axis_y^2)
        self.px_width = detector.frame.px_width
        self.px_height = detector.frame.px_height
        self.center_coords = (self.px_width/2, self.px_height/2)



    def find_distance_to_wall(self, det = Detector, servo_x = None, servo_y = None):
        if det.find_black_rectangle() != False:
            self.calc_dist_box(det)
        elif servo_x is Servo or servo_y is Servo:
            self.calc_dist_angle(det, servo_x = Servo, servo_y = Servo)
        else: self.calc_dist_checkers(det)
        
    def calc_dist_checkers(NotImplemented): NotImplemented  #TODO    
    def calc_dist_box(): NotImplemented  #TODO: youtube metoden(?) elller kan dne her bruges #https://www.researchgate.net/publication/235196461_A_Simple_Method_for_Range_Finding_via_Laser_Triangulation      
    def calc_dist_angle(self, det = Detector, servo_x = None, servo_y = None):   #return bools værdi
        #TODO: 
        #laseren skal enten vaere centreret, ellers skal den være i billedet om man skal omregne dimensioner til pixel
        # b = a × tan(β)
        cam_to_laser = 4
        if servo_x is Servo and servo_y is Servo:
            # de to variable kanter i retvinklet skal <90 også, servo går 0..180, så tag højde siden som kameraet er på
            angle_x = servo_x.angle # +/- self.angle_offsett_x ????? TODO
            angle_y = servo_y.angle # +/- self.angle_offsett_y ????? TODO
            if angle_x > 90: angle_x - 90 
            if angle_y > 90: angle_y - 90
            
        dot_coord_x, dot_coord_y = det.find_laser_dot() #!!!!!!!!!!!!!
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
            return False, 00000



    def find_dimension_conversion_factor(self, method_choice = str, detector = Detector, servo_x= None, servo_y= None,):
        if method_choice == "box":
            self._calc_dim_conv_fact_known_square(detector)
        elif method_choice == "checkerboard":
            self._calc_dim_conv_fact_checkerboard(detector)
        elif (servo_x is Servo or servo_y is Servo):
            self._calc_dim_conv_fact_perpendicular_laser(detector, servo_x, servo_y,)
        else: return False
        
    def _calc_dim_conv_fact_perpendicular_laser(self, detector = Detector, servo_x= None, servo_y= None):
        px_to_cm_heigth_scale = False 
        px_to_cm_width_scale = False

        #hvis laseren er lige på, så er afstand fra midten til laserdot, det samme som kamera til laser

        if servo_y is Servo and servo_y.angle == 90:
            dot_offset_x = abs((self.px_width/2)- detector.find_laser_dot('axis_y')) #abs for kun at få positv værdi
            px_to_cm_width_scale = (dot_offset_x / self.dist_cam_axis_y) 
        
        elif servo_x is Servo:
            return NotImplemented #TODO: make method  servo perpendicular
        
        if servo_x is Servo and servo_x.angle == 90:
            dot_offset_y = abs((self.px_height/2)- detector.find_laser_dot('axis_x')) #abs for kun at få positv værdi
            px_to_cm_heigth_scale = (dot_offset_y / self.dist_cam_axis_x)
        
        elif servo_y is Servo:
            return NotImplemented #TODO: make method for servo perpendicular
        
        return px_to_cm_heigth_scale, px_to_cm_width_scale
        
    def _calc_dim_conv_fact_checkerboard(self, detector = Detector): NotImplemented       
    def _calc_dim_conv_fact_known_square(self, detector = Detector):NotImplemented


    def calc_laser_angle_from_distance(self, det = Detector, servo_x = None, servo_y = None):
    # Given α(angle of corner at wall): β(angle of laser corner) = 90 - α
    # β = arctan(b / a)     OR     β = arccot(a / b)
        #vinklen for hvor laser ville møde midten af kameraet
        #   β=arctan(b/a)
        if(det.find_laser_dot == self.center_coords):
            self.laser_to_center_angle_origin = 90 - math.atan(self.cam_to_wall/self.dist_cam_axis_origin)
            self.laser_to_center_angle_x = 90 - math.atan(self.cam_to_wall/self.dist_cam_axis_x)
            self.laser_to_center_angle_y = 90 - math.atan(self.cam_to_wall/self.dist_cam_axis_y)
        else: return False
        #Man kan også gøre noget lignende, hvis laseren er vinkelret med væggen, men det gider jeg ikke lige nu
        # maaske return et offset af en art?
        if servo_x is Servo and servo_y is Servo:   #NOTE: Det skal nok bruges, men det gider jeg heller ikke
            if servo_y.angle != self.laser_to_center_angle_y:
                self.angle_offsett_x = servo_x.angle - self.laser_to_center_angle_x
            if servo_x.angle != self.laser_to_center_angle_x:
                self.angle_offsett_y = servo_y.angle - self.laser_to_center_angle_y
            
    def calc_laser_angle_when_centered(self, det = Detector, servo_x = None, servo_y = None):
        #hvis laser vinkelret er = 90, så find vinkelforskel mellem det og når den peger på midten:
        if(det.get_center_coordinates(en_fucking_laser_tak) == self.center_coords):
            angle_for_center_y = 90 - servo_x.angle #tjek om det er den ene eller anden laser. alt efter drejing om akse, eller bevægelse langs
            angle_for_center_x = 90 - servo_y.angle #same
            # angle_for_origin = den kan man også finde 
        return (angle_for_center_y, angle_for_center_x)


    def center_laser_in_img(self, det = Detector, servo_x=Servo, servo_y=Servo):
               #TODO: find elegant way of doing it. with and/or without trial&error / other way
        #ryk laser op/ned indtil den rammer midterlinjen
        x_coord = det.find_laser_dot('x')
        y_coord = det.find_laser_dot('y')
        if (x_coord, y_coord) == self.center_coords:
            return True
        else:
            servo_x.move(90)
            servo_y.move(90)
            #NOTE: also, bare lige for at være sikker. hvor starter billedets koordina
            #lasers cordinat hvis laser 90 90. x= center_of_frame +/- cm_conv_px(cam_to_laser)
                            #if  x_coord == 1111:
                                #self.calc_angle_for_frame_center(servo_y, x_coord)
            while(det.find_laser_dot('x') > (self.px_width)/2):
                servo_x.move(servo_x.angle - 1)
            while(det.find_laser_dot('x') < (self.px_width)/2):
                servo_x.move(servo_x.angle + 1)
            while(det.find_laser_dot('y') > (self.px_height)/2):
                servo_y.move(servo_y.angle - 1)
            while(det.find_laser_dot('y') < (self.px_height)/2):
                servo_x.move(servo_x.angle + 1)


            
    
    def calc_angle_for_frame_center(self, det = Detector, servo = Servo ,coordinate = None): #TODO:det hænger ikke sammen
        if servo.axis == "x":
            dist_cam_to_axis = self.dist_cam_axis_y
            if coordinate < self.px_width/2 : gokbok = 1
        elif servo.axis == "y":
            dist_cam_to_axis = self.dist_cam_axis_x
            det.find_laser_dot('x')

        angle_to_center_laser = 1 #111111111

        # angle_to_point_laser_center = math.atan(self.cam_distance_wall/dist_cam_to_axis) NOTE regnefejl. 
        servo.move(angle_to_center_laser)
        return NotImplemented
    
            
    def calculate_frame_dimensions():
        #TODO: skriv method for at finde rummål. NOTE: nødvendigt?
        #hvis man har pixel til reelle mål plob den ind
        #hvis laser peger lige frem, så er:
        # center_to_dot == cam_to_laser (skal bruge x og y)
        # man kunne bruge camera fov og distance til væggen
        #omregn mellem pixel og cm

        #hvis laser centreret og cam_to_wall er kendt
        NotImplemented