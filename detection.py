import cv2
from Bounding_Boxes_subclasses.rectangle import Rectangle
from Bounding_Boxes_subclasses.circle import Circle
import numpy as np


class Identifyer:
    # Read the camera footage
    webcam_video = cv2.VideoCapture(0)
    success, video = webcam_video.read()

    # Converting the BGR image from webcam to HSV format
    frame = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

     # Converting the BGR image from webcam to gray scale
    gray_scale = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

    # Thresh
    thresh = cv2.threshold(gray_scale, 100, 1, cv2.THRESH_BINARY_INV)[1]

    def track_faces(self, gray_scale, img, video):
        # Detection of face file
        face_file_path = "data_cascade/haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(face_file_path)

        # Activating camera image - We will change this later, as we gonna use the camera class.
        webcam_video = cv2.VideoCapture(1)
        while True:
            # Recognize a face
            faces = cascade.detectMultiScale(gray_scale, 1.2, 3)

            bounding_boxes = []

            for (x, y, w, h) in faces:
                rectangle_obj = Rectangle(x, y, w, h)
                bounding_boxes.append(rectangle_obj)

            for box in bounding_boxes:
                box.display(video)

    def find_black_dot(self, thresh, gray, frame = None, video = None,):
        bbox = (287, 23, 86, 320)
        # Finding contours in mask image
        mask_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 100:  # minimum amount of pixels to register
                x, y, w, h = cv2.boundingRect(mask_contour)
                bboxes = (x, y, w, h)

                cv2.putText(gray, f'({x},{y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return bboxes





"""
contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    rect = cv2.boundingRect(c)
    if rect[2] < 100 or rect[3] < 100: continue
    print cv2.contourArea(c)
    x,y,w,h = rect
    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.putText(im,'Moth Detected',(x+w+10,y+h),0,0.3,(0,255,0))
cv2.imshow("Show",im)
cv2.waitKey()  
cv2.destroyAllWindows() 



 bounding_boxes = []
            circle_obj = Circle.from_contours(contours)
            if circle_obj is not None:
                bounding_boxes.append(circle_obj)

            for box in bounding_boxes:
                box.display(video)

            # Open a window and display the mask image
            cv2.imshow("Mask image", img)

            # Open a window and display the webcam image
            cv2.imshow("Webcam Image", video)

            # Defining the delay pr frame.
            cv2.waitKey(1)
            
"""

