import pickle
import cv2
import math
import glob
from camera import Camera
import numpy as np
from servo import Servo
from detection import Detection

class ServoCalibrator:
    
    cam_fov = 80
    cam_sensor_size = 1 # 1.22 micrometer × 1.22 micrometer     1 micrometer = 0,001mm eller tæt på
    cam_focal_length = 4.28 # mål i mm
    # cam_focal_ratio = 1.75
    cam_to_wall = 30

    def __init__(self, cam, cam_laser_axis_x_dist, cam_laser_axis_y_dist ) -> None:
        self.cam_to_laser_axis_x = cam_laser_axis_x_dist
        self.cam_to_laser_axis_y = cam_laser_axis_y_dist
        self.cam_to_laser_origin_dist = math.sqrt(self.cam_to_laser_axis_x^2 + self.cam_to_laser_axis_y^2)
        self.cam_px_width = cam.px_width
        self.cam_px_height = cam.px_height
        self.frame_center_coords = (cam.px_width/2, cam.px_height/2)



    def find_distance_to_wall(self, det = Detection, servo_x = None, servo_y = None):
        if det.find_black_rectangle() != False:
            self.calc_dist_to_wall_using_box(det)
        elif servo_x is Servo or servo_y is Servo:
            self.calc_distance_from__angle(det, servo_x = Servo, servo_y = Servo)
        else: self.calc_dist_to_wall_using_checkerboard(det)
        
    def calc_dist_to_wall_using_checkerboard(NotImplemented): NotImplemented  #TODO    
    def calc_dist_to_wall_using_box(): NotImplemented  #TODO: youtube metoden(?) elller kan dne her bruges #https://www.researchgate.net/publication/235196461_A_Simple_Method_for_Range_Finding_via_Laser_Triangulation      
    def calc_dist_to_wall_using_angle(self, det = Detection, servo_x = None, servo_y = None):   #return bools værdi
        #TODO: 
        #laseren skal enten vaere centreret, ellers skal den være i billedet om man skal omregne dimensioner til pixel
        # b = a × tan(β)
        cam_to_laser = 4
        if servo_x is Servo and servo_y is Servo:
            # de to variable kanter i retvinklet skal <90 også, servo går 0..180, så find siden som kameraet er på
            angle_x = servo_x.angle # +/- self.angle_offsett_x ????? TODO
            angle_y = servo_y.angle # +/- self.angle_offsett_y ????? TODO
            if angle_x > 90: angle_x - 90 
            if angle_y > 90: angle_y - 90
            
        laser_coord_x, laser_coord_y = det.find_laser_dot() #!!!!!!!!!!!!!
        if ((laser_coord_x, laser_coord_y) == self.frame_center_coords):
            # b = a × tan(β)
            cam_to_wall_x = self.cam_to_laser_axis_y * math.tan(angle_y)
            cam_to_wall_y = self.cam_to_laser_axis_x * math.tan(angle_x)
            #tjek om de giver den samme distance til væggen. returnerer om de giver den samme distance, og så en distance
            if cam_to_wall_x == cam_to_wall_y: 
                self.cam_to_wall = cam_to_wall_x
                return True, cam_to_wall_x
            else:
                self.cam_to_wall = (cam_to_wall_x + cam_to_wall_y / 2)
                return False, (cam_to_wall_x + cam_to_wall_y / 2)
            
        elif laser_coord_y == self.frame_center_coords[1]: 
            self.cam_to_wall = self.cam_to_laser_axis_x * math.tan(angle_x)
            return False, self.cam_to_wall
        elif laser_coord_x == self.frame_center_coords[0]: 
            self.cam_to_wall = self.cam_to_laser_axis_y * math.tan(angle_y)
            return False, self.cam_to_wall
        
        else: # do some conversion bullshit or center laser in frame idk
            mid_to_dot_x = abs(laser_coord_x - self.frame_center_coords[0])
            mid_to_dot_y = abs(laser_coord_y - self.frame_center_coords[1])
            NotImplemented
        
        return False, self.cam_to_wall



    def find_dimension_conversion_factor(self, method_choice = str, detector = Detection, servo_x= None, servo_y= None,):
        if method_choice == "box":
            self._px_cm_conversion_factor_known_square(detector)
        elif method_choice == "checkerboard":
            self._px_cm_conversion_factor_checkerboard(detector)
        elif (servo_x is Servo or servo_y is Servo):
            self._px_cm_conversion_factor_perpendicular_laser(detector, servo_x, servo_y,)
        else: return False
        
    def _px_cm_conversion_factor_perpendicular_laser(self, detector = Detection, servo_x= None, servo_y= None):
        px_to_cm_heigth_scale = False 
        px_to_cm_width_scale = False

        if servo_y is Servo and servo_y.angle == 90:
            dot_offset_x = abs((self.cam_px_width/2)- detector.find_laser_dot('axis_y')) #abs for kun at få positv værdi
            px_to_cm_width_scale = (dot_offset_x / self.cam_to_laser_axis_y) 
        
        elif servo_x is Servo:
            return NotImplemented #TODO: make method  servo perpendicular
        
        if servo_x is Servo and servo_x.angle == 90:
            dot_offset_y = abs((self.cam_px_height/2)- detector.find_laser_dot('axis_x')) #abs for kun at få positv værdi
            px_to_cm_heigth_scale = (dot_offset_y / self.cam_to_laser_axis_x)
        
        elif servo_y is Servo:
            return NotImplemented #TODO: make method for servo perpendicular
        
        return px_to_cm_heigth_scale, px_to_cm_width_scale
        
    def _px_cm_conversion_factor_checkerboard(self, detector = Detection): NotImplemented       
    def _px_cm_conversion_factor_known_square(self, detector = Detection):NotImplemented


    def calc_laser_angle_from_distance(self, det = Detection, servo_x = None, servo_y = None):  #TODO:
    # Given α(angle of corner at wall): β(angle of laser corner) = 90 - α
    # β = arctan(b / a)     OR     β = arccot(a / b)

        #vinklen for hvor laser ville møde midten af kameraet
        #   β=arctan(b/a)
        if(det.find_laser_dot == self.frame_center_coords):
            self.laser_to_center_angle_origin = 90 - math.atan(self.cam_to_wall/self.cam_to_laser_origin_dist)
            self.laser_to_center_angle_x = 90 - math.atan(self.cam_to_wall/self.cam_to_laser_axis_x)
            self.laser_to_center_angle_y = 90 - math.atan(self.cam_to_wall/self.cam_to_laser_axis_y)
        elif servo_x is Servo and servo_y is Servo: # Har det nogen værdi at prøve at finde afstanden hvis laseren ikke er centreret? de burde faktisk være det samme som dem over. måske værd at teste
            if(servo_x.angle == 90): NotImplemented
            if(servo_y.angle == 90): NotImplemented

        #something with difference between angle from calculations and angle saved to servo
        # maaske return et offset af en art?
        if servo_x is Servo and servo_y is Servo:
            if servo_y.angle != self.laser_to_center_angle_y:
                self.angle_offsett_x = servo_x.angle - self.laser_to_center_angle_x
            if servo_x.angle != self.laser_to_center_angle_x:
                self.angle_offsett_y = servo_y.angle - self.laser_to_center_angle_y


    def center_laser_in_img(self, det = Detection, servo_x=Servo, servo_y=Servo):
               #TODO: find elegant way of doing it. with and/or without trial&error / other way
        #ryk laser op/ned indtil den rammer midterlinjen
        servo_x.move(90)
        servo_y.move(90)
        x_coord = det.find_laser_dot('x')
        y_coord = det.find_laser_dot('y')

        #NOTE: also, bare lige for at være sikker. hvor starter billedets koordina
        #lasers cordinat hvis laser 90 90. x= center_of_frame +/- cm_conv_px(cam_to_laser)
        if  x_coord == 1111:
            self.calc_angle_for_frame_center(servo_y, x_coord)

        """
            while(det.find_laser_dot('x') > (self.cam_px_width)/2):
                servo_x.move(servo_x.angle - 1)
            while(det.find_laser_dot('x') < (self.cam_px_width)/2):
                servo_x.move(servo_x.angle + 1)
            while(det.find_laser_dot('y') > (self.cam_px_height)/2):
                servo_y.move(servo_y.angle - 1)
            while(det.find_laser_dot('y') < (self.cam_px_height)/2):
                servo_x.move(servo_x.angle + 1)
                """
    def calc_angle_for_frame_center(self, det = Detection, servo = Servo ,coordinate = None): #TODO:det hænger ikke sammen
        if servo.axis == "x":
            dist_cam_to_axis = self.cam_to_laser_axis_y
            if coordinate < self.cam_px_width/2 : gokbok = 1
        elif servo.axis == "y":
            dist_cam_to_axis = self.cam_to_laser_axis_x
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

class ImageCalibrator:  #TODO unfinished
    # NOTE: https://youtu.be/3h7wgR5fYik?si=Ij60L5DQ3I3LYzy4
    chessboard_size = (9, 6) # number of corners in width and height
    frame_size = (ServoCalibrator.cam_px_width, ServoCalibrator.cam_px_height)  # pixels in image width and height. standard example 1920x1080
        
    # termination criteria til at finde præcise hjørner med subpixels
    #           ved ikke præcist hvad det er 
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # (x, y, gray_scale val)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0: chessboard_size[0], 0: chessboard_size[1]].T.reshape(-1, 2)
    # can't explain [:,:2], maybe   

    size_of_chessboard_squares_mm = 20 #actual physical size of squares on the printout. measure accurately!
    objp = objp * size_of_chessboard_squares_mm

    def __init__(self, Camera):
        self.img = Camera.gray_conv(Camera.run) #TODO: utilise Camera class instead

        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space. project down to 2d plane. lineær algebra
        self.imgpoints = [] # 2d points in image plane.
        self.run_calibrations()

    def run_calibrations(self):
        self.find_chess_corners()
        self.calibrate_camera()
        #self.undistort()


    def find_chess_corners(self):  #TODO: general
        # https://calib.io/blogs/knowledge-base/calibration-patterns-explained
        # rows need to be even
        # columns need odd

        self.ret, corners = cv2.findChessboardCorners(self.img, self.chessboard_size, None) #returns bool for ret
        if self.ret is True:
            self.objpoints.append(self.objp)
            self.corners2 = cv2.cornerSubPix(self.img, corners, (11, 11), (-1, -1), self.criteria)
            self.imgpoints.append(corners)
    

    def calibrate_camera(self):
        self.ret, self.camera_matrix, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.frameSize, None, None)

        # Save the camera calibration result for later use
        pickle.dump((self.camera_matrix, self.dist), open( "calibration.pkl", "wb" ))
        pickle.dump(self.camera_matrix, open( "camera_matrix.pkl", "wb" ))
        pickle.dump(self.dist, open( "dist.pkl", "wb" ))


    def undistort(self): #TODO: undersøg hvorfor man bruger de her billeder 
        img = cv2.imread('cali5.png')
        h,  w = img.shape[:2]
        newcamera_matrix, roi = cv2.getOptimalNewcamera_matrix(self.camera_matrix, self.dist, (w,h), 1, (w,h))

        # Undistort
        dst = cv2.undistort(img, self.camera_matrix, self.dist, None, newcamera_matrix)

        # crop image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite('caliResult1.png', dst)

        # Undistort with Remapping
        mapx, mapy = cv2.initUndistortRectifyMap(self.camera_matrix, self.dist, None, newcamera_matrix, (w,h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite('caliResult2.png', dst)

        # Reprojection Error
        mean_error = 0

        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv2.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], 
                                              self.camera_matrix, self.dist)
            error = cv2.norm(self.imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            mean_error += error

        print( "total error: {}".format(mean_error/len(self.objpoints)) ) 