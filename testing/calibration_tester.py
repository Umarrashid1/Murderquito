import inspect
import sys
import os


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from camera_calibration import ImageCalibrator
from detection import Detection
import cv2
import numpy as np
import sys


"""
video = cv2.VideoCapture(0)

# Exit if video not opened.
if not video.read():
    print("Could not open video")
    sys.exit()

# Read first frame.
ok, frame = video.read()
if not ok:
    print("Cannot read video file")
    sys.exit()"""

frame = cv2.imread('calibration\img-chessboard-01.png')
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

img_cal = ImageCalibrator(gray_frame)
img_cal.run_calibrations()
img_cal.show_corners()
img_cal.undistort()


