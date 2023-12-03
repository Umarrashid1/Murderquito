import pickle
import cv2
import math
import glob
#from camera import Camera
import numpy as np
#from servo import Servo
from detection import Detector


class ImageCalibrator:  #TODO unfinished
    # NOTE: https://youtu.be/3h7wgR5fYik?si=Ij60L5DQ3I3LYzy4
    chessboard_size = (9, 6) # number of corners in width and height
    #frame_size = (ServoCalibrator.cam_px_width, ServoCalibrator.cam_px_height)  # pixels in image width and height. standard example 1920x1080
    frame_size = (320, 240)   
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

    def show_corners(self):
        cv2.drawChessboardCorners(self.img_corners, self.chessboard_size, self.corners2, None)
        cv2.imwrite('calibration\chessybesy.png', self.img_corners)


    def __init__(self, img):  #camera = Camera
        # self.img = camera.gray_conv(camera.run())
        self.img = img
        self.img_corners = self.img


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

        self.ret, self.corners = cv2.findChessboardCorners(self.img, self.chessboard_size, None) #returns bool for ret
        if self.ret is True:
            self.objpoints.append(self.objp)
            self.corners2 = cv2.cornerSubPix(self.img, self.corners, (11, 11), (-1, -1), self.criteria)
            self.imgpoints.append(self.corners)
        
    

    def calibrate_camera(self):
        self.ret, self.camera_matrix, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.frame_size, None, None)

        # Save the camera calibration result for later use
        pickle.dump((self.camera_matrix, self.dist), open( "calibration\calibration.pkl", "wb" ))
        pickle.dump(self.camera_matrix, open( "calibration\camera_matrix.pkl", "wb" ))
        pickle.dump(self.dist, open( "calibration\dist.pkl", "wb" ))
        


    def undistort(self): #TODO: undersøg hvorfor man bruger de her billeder 
        img = cv2.imread('calibration\img-chessboard-02.png')
        h,  w = img.shape[:2]
        newcamera_matrix, roi = cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.dist, (w,h), 1, (w,h))

        # Undistort
        dst = cv2.undistort(img, self.camera_matrix, self.dist, None, newcamera_matrix)

        # crop image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite('calibration\caliResult1.png', dst)

        # Undistort with Remapping
        mapx, mapy = cv2.initUndistortRectifyMap(self.camera_matrix, self.dist, None, newcamera_matrix, (w,h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv2.imwrite('calibration\caliResult2.png', dst)

        # Reprojection Error
        mean_error = 0

        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv2.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], 
                                              self.camera_matrix, self.dist)
            error = cv2.norm(self.imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            mean_error += error

        print( "total error: {}".format(mean_error/len(self.objpoints)) ) 