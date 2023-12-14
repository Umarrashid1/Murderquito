import pickle
import cv2
import math
import glob
#from camera import Camera
import numpy as np
#from servo import Servo
#from detection import Detector


class CameraCalibrator:  #TODO unfinished
    # NOTE: https://youtu.be/3h7wgR5fYik?si=Ij60L5DQ3I3LYzy4
    chessboard_size = (9, 6) # number of corners in width and height
    
    # termination criteria til at finde præcise hjørner med subpixels
    #           ved ikke præcist hvad det er 
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # (x, y, gray_scale val)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0: chessboard_size[0], 0: chessboard_size[1]].T.reshape(-1, 2)  

    size_of_chessboard_squares_mm = 24.1 #actual physical size of squares on the printout. measure accurately!
    objp = objp * size_of_chessboard_squares_mm

 

    def __init__(self, frame):  #camera = Camera
        # self.img = camera.gray_conv(camera.run())
        self.img = frame
        self.img_corners = self.img
        self.px_height, self.px_width, = frame.shape[:2]
        self.frame_size = (self.px_width, self.px_height)

        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space. project down to 2d plane. lineær algebra
        self.imgpoints = [] # 2d points in image plane.

    def show_corners(self):
        cv2.drawChessboardCorners(self.img_corners, self.chessboard_size, self.corners2, None)
        cv2.imwrite('calibration\chessybesy.png', self.img_corners)
    def get_calibration_data(self):
        return self.camera_matrix, self.dist
    
    def run_calibrations(self, frame = None):
        if frame is not None:
            self.img = frame
            self.img_corners = frame
        self.find_chess_corners()
        self.calibrate_camera()
        #self.undistort()
        #return self.get_calibration_data

    def reverse_project(self):
        cx = 300
        cy = 200
        pixel = np.array([[cx, cy, 1]], dtype=np.float32)
        pixel = pixel.reshape((1, 3)) # Reshape pixel to (1, 3)
        point, _ = cv2.projectPoints(pixel, np.zeros((3, 1)), np.zeros((3, 1)), self.camera_matrix, self.dist)       # Convert the 3D point to spherical coordinates
        print ("point:" point)
        a = point[0][0] - self.tvecs
        b = np.array([[0], [0], [1]])
        cos_theta = (a.squeeze() @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
        theta = np.arccos(cos_theta)
        # Convert theta from radians to degrees
        theta = np.degrees(theta)
        print("theta")
        print(theta)
    
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
        print("Camera matrix")
        print(self.camera_matrix)
        print("Distortion coeff")
        print(self.dist)
        # Save the camera calibration result for later use
        pickle.dump((self.camera_matrix, self.dist), open( "calibration.pkl", "wb" ))
        pickle.dump(self.camera_matrix, open( "camera_matrix.pkl", "wb" ))
        pickle.dump(self.dist, open( "dist.pkl", "wb" ))
        
        


    def undistort(self, frame, choice = None): #TODO: undersøg hvorfor man bruger de her billeder 
        h,  w = frame.shape[:2]
        newcamera_matrix, roi = cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.dist, (w,h), 1, (w,h))

        # Undistort
        dst1 = cv2.undistort(frame, self.camera_matrix, self.dist, None, newcamera_matrix)
        
        # crop image
        x, y, w, h = roi
        dst1_crop = dst1[y:y+h, x:x+w]
        #cv2.imwrite('calibration\caliResult1.png', dst)
        if choice == 1:
            return dst1, dst1_crop
        # Undistort with Remapping
        mapx, mapy = cv2.initUndistortRectifyMap(self.camera_matrix, self.dist, None, newcamera_matrix, (w,h), 5)
        dst2 = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst2_crop = dst2[y:y+h, x:x+w]
        if choice == 2:
            return dst2, dst2_crop
        #cv2.imwrite('calibration\caliResult2.png', dst)
        # Reprojection Error
        self.calc_reprojection_errors()
        if choice is None:
            return dst1_crop, dst2_crop


    def calc_reprojection_errors(self):
        mean_error = 0
        for i in range(len(self.objpoints)):
            self.imgpoints2, _ = cv2.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], 
                                              self.camera_matrix, self.dist)
            error = cv2.norm(self.imgpoints[i], self.imgpoints2, cv2.NORM_L2)/len(self.imgpoints2)
            mean_error += error

        print( "total error: {}".format(mean_error/len(self.objpoints)) )
        return mean_error, (mean_error/len(self.objpoints))