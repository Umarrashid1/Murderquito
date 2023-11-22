import cv2
from Bounding_Boxes_subclasses.rectangle import Rectangle

# from Bounding_Boxes_subclasses.circle import Circle
import numpy as np
from camera import Camera


class Detection:
    bbox = None
    tracker = None
    ok = False
    
    def __init__(self, cam):
        self.tracker = cv2.legacy.TrackerKCF.create()
        self.bbox = self.find_cirle(cam.gray_frame())

    def update_tracker(self, cam):
        ok, self.bbox = self.tracker.update(getattr(cam, 'frame'))

    def draw_boundingbox(self, cam):
        if self.ok:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(cam.gray_frame(), p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putTextcam(cam.gray_frame(), "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.imshow("Tracking", cam.gray_frame)

    ''''

    def find_black_rectangle(): #TODO find hjørner og evt sidelængder på rektangel/kvadrat maaske?
        x = 1
        y = 2
        point_one = [x,y]
        point_two = [x,y]
        point_three = [x,y]
        point_four = [x,y]  
        return point_one, point_two, point_two, point_three

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
''''
    def find_circle(self, image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and help the circle detection
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=5,
            maxRadius=50
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