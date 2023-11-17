import pickle
import cv2
import math
import glob
from camera import Camera
import numpy as np
from servo import Servo
from detection import Identifyer

class ServoCalibrator:
    cam_to_laser_axis_y = 4
    cam_to_laser_axis_x = 8
    cam_fov = 80
    cam_px_width = 1080
    cam_px_height = 720
    cam_sensor_size = 1 # 1.22 micrometer × 1.22 micrometer     1 micrometer = 0,001mm eller tæt på
    cam_focal_length = 4.28 # mål i mm
    # cam_focal_ratio = 1.75

    cam_distance_wall = 30
    

    def find_dimension_conversion_factor(self,servo_x= None, servo_y= None, choice_of_method = None):
        if servo_x is Servo or servo_y is Servo and choice_of_method is 1:
            self._px_cm_conversion_factor_perpendicular_laser(servo_x, servo_y, choice_of_method)

        elif choice_of_method is 2:
            self._px_cm_conversion_factor_checkerboard(choice_of_method)
        
    def _px_cm_conversion_factor_perpendicular_laser(self, servo_x= None, servo_y= None, laser_dot_object = None):
        if servo_x is Servo and servo_x.angle == 0:
            dot_offset_x = abs((self.cam_px_width/2)- laser_dot_object.coord_x) #abs for kun at få positv værdi
            self.px_to_cm_width_scale = (dot_offset_x / self.cam_to_laser_axis_y)
        elif servo_x is Servo:
            return NotImplemented #TODO: make method  servo perpendicular
    
        if servo_y is Servo and servo_y.angle == 0:
            dot_offset_y = abs((self.cam_px_height/2)- laser_dot_object.coord_y) #abs for kun at få positv værdi
            self.px_to_cm_heigth_scale = (dot_offset_y / self.cam_to_laser_axis_x)
        elif servo_y is Servo:
            return NotImplemented #TODO: make method for servo perpendicular
        
    def _px_cm_conversion_factor_known_square(choice_of_method):  
        #TODO: implement conversion of pixel to cm / mm using a square OR checkerboard
        NotImplemented


    def approx_dist_to_wall_using_box(): #https://www.researchgate.net/publication/235196461_A_Simple_Method_for_Range_Finding_via_Laser_Triangulation
       #TODO: youtube metoden(?)
        NotImplemented
        
        
    def calculate_frame_dimensions():
        #TODO: skriv method for at finde rummål. NOTE: nødvendigt?
        #hvis man har pixel til reelle mål plob den ind
        #hvis laser peger lige frem, så er:
        # center_to_dot == cam_to_laser (skal bruge x og y)
        # man kunne bruge camera fov og distance til væggen
        #omregn mellem pixel og cm

        #hvis laser centreret og cam_to_wall er kendt
        NotImplemented


    def calc_angle_from_distance(self):  #TODO:
        cam_to_wall = 12
        laser_x = 1
        laser_y = 1 #kald track eller identification

        NotImplemented

    def calc_distance_from__angle(self):   #TODO: 
        #laseren skal enten vaere centreret, ellers skal den være i billedet om man skal omregne dimensioner til pixel
        cam_to_laser = 4
        x_angle = 2
        y_angle = 2 #servo.get_angle(y)?

        NotImplemented

    def center_laser_in_img(self, det = Identifyer, servo_x=Servo, servo_y=Servo):  
        #TODO: find elegant way of doing it. with and/or without trial&error / other way
        #ryk laser op/ned indtil den rammer midterlinjen
        x_coord = det.find_laser_dot('x')
        y_coord = det.find_laser_dot('y')

        #NOTE: also, bare lige for at være sikker. hvor starter billedets koordina
        if  x_coord > self.cam_px_width/2:
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



    def calc_angle_for_frame_center(self, servo = Servo ,coordinate = None): #TODO:det hænger ikke sammen
        if servo.axis == "x":
            dist_cam_to_axis = self.cam_to_laser_axis_y
            if coordinate < self.cam_px_width/2 : gokbok = 1
        elif servo.axis == "y":
            dist_cam_to_axis = self.cam_to_laser_axis_x
            det.find_laser_dot('x')


        # angle_to_point_laser_center = math.atan(self.cam_distance_wall/dist_cam_to_axis) NOTE regnefejl. 
        servo.move(angle_to_point_laser_center)
        return NotImplemented

class ImageCalibrator:
    chessboard_size = (9, 6) # number of corners in width and height
    frame_size = (640, 480)  # pixels in image width and height. standard example 1920x1080
        
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