import cv2
from Bounding_Boxes_subclasses.rectangle import Rectangle

# from Bounding_Boxes_subclasses.circle import Circle
import numpy as np
# from camera import Camera


class Detector:

    def find_black_rectangle(): #TODO find hjørner og evt sidelængder på rektangel/kvadrat maaske?
        x = 1
        y = 2
        point_one = [x,y]
        point_two = [x,y]
        point_three = [x,y]
        point_four = [x,y]
        return point_one, point_two, point_two, point_three

    """def find_laser_dot(cam = Camera, coord_choice = None):
        frame = cam.run() 
        #TODO: find grøn lasers koordinat til frame
        # (Janice har lavet en. jeg finder den i commit history)

        if coord_choice is 'y': return x_coord
        elif coord_choice is 'x': return y_coord
        else: return (x_coord, y_coord)
        s = 1
    """
   
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

    def find_black_dot(self, thresh):
        bbox = None

        # Finding contours in mask image
        mask_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 100:  # minimum amount of pixels to register/filter away noise
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    bbox = (x, y, w, h)
                    #cv2.putText(gray_frame, f'({x},{y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return bbox

    def find_circle(self, image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and help the circle detection
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,  # 1 means the accumulator has the same resolution as the input image
            minDist=30,  # Minimum distance between the centers of detected circles
            param1=50,  # Higher value means less sensitive edge detection
            param2=30,  # Higher value allows detection with lower confidence
            minRadius=2,  # Minimum radius of detected circles
            maxRadius=50   # Maximum radius of detected circles
        )

        if circles is not None:
            # Convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # Return the bounding box of the first detected circle
            x, y, radius = circles[0]
            bbox = (x - radius, y - radius, 2 * radius, 2 * radius)
            return bbox

        # Return None if no circle is found
        return None


#ekstra ting kopieret et sted fra:
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

