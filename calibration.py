#added calibration file with some different (WIP) coord/angle and dimension approximations
import pickle
import cv2
import math
import glob
from camera import Camera
import numpy as np

class ServoCalibrator:
    cam_to_laser = 4
    cam_fov = 80
    cam_px_width = 1080
    cam_px_height = 720

    # β=arctan(b/a)

    
    def px_dim_conv():
        #kend væggens bredde højde i billedrammen, eller dimensionerne på et objekt i billedet
        fucknuaf=1

    def approximate_distance_to_wall():
            #kassen har kendte dimensioner: x_cm y_cm
            #kameraet har oploesning : x_pixel y_pixel
            #find kasses x_pixel y_pixel
            #brug det til at finde billedrammens bredde x_cm og hoejde y_cm
                #Kamera_x_pixel / kasse_x_pixel
            #und so weiter

            black_box_dim = 2
            mask_contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Find the position of the contour and draw a circle
            if len(mask_contours) != 0:
                for mask_contour in mask_contours:
                    # Defining the least amount of pixels, I want it to register.
                    if cv2.contourArea(mask_contour) > 100:
                        # Setting up the circle
                        (x, y), radius = cv2.minEnclosingCircle(mask_contour)
                        center = (int(x), int(y))
                        radius = int(radius)

                        # Creating the circle
                        cv2.circle(video, center, radius, (0, 0, 255), 3)

                        # Show coordinates for the center of the black object
                        cv2.putText(video, f'({x},{y})', center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.circle(video, center, 3, (0, 255, 255), -1)

    def calculate_frame_dimensions():
        #hvis laser peger lige frem, så er:
        # center_to_dot == cam_to_laser
        #omregn mellem pixel og cm

        #hvis laser centreret og cam_to_wall er kendt
        a = 1

    def calc_angle_for_frame_center(): #
        #   Use Pythagoras with DISTANCE between LASER ORIGIN and CAMERA CENTER 
        #   alongside distance of WALL to calculate LASER ANGLE]
        #   use x_coords to get x_angle     y_coords for angle_y
        cam_to_laser = 3
        cam_to_wall = 5

        laser_dot_x = 2
        laser_dot_y = 2
            #vinklen for hvor laser ville møde midten af kameraet
            #   α=arctan(a/b) for trekant med a = mid_to_dot, b = cam_to_wall
            #   laser_vinkel = 90 - arctan(mid_to_dot/cam_to_wall)
        
        #gider ikke flere trekanter lige nu

    def calc_angle_from_distance(self):
        cam_to_wall = 12
        laser_x = 1
        laser_y = 1 #kald track eller identification

    def calc_distance_from__angle(self):
        
        #laseren skal enten vaere centreret, ellers skal den være i billedet om man skal omregne dimensioner til pixel
        cam_to_laser = 4

        #
        x_angle = 2
        y_angle = 2 #servo.get_angle(y)?



        errr=1

    def center_laser_in_img():
        #ryk laser op/ned indtil den rammer midterlinjen
        #samme for højre venstre
        #når laser_dot = center_of_frame succes
        d = 1

class ImageCalibrator:
    chessboard_size = (9,6) # number of corners in width and height
    frame_size = (640,480)  # pixels in image width and height. standard example 1920x1080
        
    # termination criteria til at finde præcise hjørner med subpixels
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_size[0],0:chessboard_size[1]].T.reshape(-1,2)
    

    size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm

    def __init__(self, Camera):
        self.img = Camera.gray_conv(Camera.run)
        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space. project down to 2d plane. lineær algebra
        self.imgpoints = [] # 2d points in image plane.



    def find_chess_corners(self):
        # https://calib.io/blogs/knowledge-base/calibration-patterns-explained
        # rows need to be even
        # columns need odd

        self.ret, corners = cv2.findChessboardCorners(self.img, self.chessboard_size, None) #returns bool
        if self.ret is True:
            self.objpoints.append(self.objp)
            self.corners2 = cv2.cornerSubPix(self.img, corners, (11,11), (-1,-1), self.criteria)
            self.imgpoints.append(corners)
    


    def calibrate(self):
        self.ret, self.camera_matrix, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.frameSize, None, None)

        # Save the camera calibration result for later use
        pickle.dump((self.camera_matrix, self.dist), open( "calibration.pkl", "wb" ))
        pickle.dump(self.camera_matrix, open( "camera_matrix.pkl", "wb" ))
        pickle.dump(self.dist, open( "dist.pkl", "wb" ))



    def undistort(self): #### idk hvad 
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
        cv.imwrite('caliResult2.png', dst)

        # Reprojection Error
        mean_error = 0

        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv2.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], 
                                              self.camera_matrix, self.dist)
            error = cv2.norm(self.imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            mean_error += error

        print( "total error: {}".format(mean_error/len(self.objpoints)) )  
                





