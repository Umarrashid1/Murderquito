import cv2
from Bounding_Boxes_subclasses.rectangle import Rectangle

# from Bounding_Boxes_subclasses.circle import Circle
import numpy as np
from camera import Camera


class Detector:
    bbox = None
    tracker = None
    ok = False

    def __init__(self, cam):
        self.tracker = cv2.TrackerKCF.create()
        self.bbox = self.find_circle(cam)
        self.init_tracker(cam)

    def init_tracker(self, cam):
        frame = cam.get_frame()

        if frame is not None and self.bbox is not None and not all(i == 0 for i in self.bbox):
            try:
                self.tracker.init(frame, self.bbox)
            except cv2.error as e:
                print(f"Error during tracker initialization: {e}")
                # print(frame)
                # print(self.bbox)
                # exit(1)
                # Handle the error gracefully, e.g., by falling back to find_circle
                self.bbox = self.find_circle(cam)

    def update_tracker(self, cam):
        if self.bbox is not None and not all(i == 0 for i in self.bbox):
            frame = cam.get_frame()

            if frame is not None:
                try:
                    # Check if the frame size matches the expected size
                    if frame.shape[:2] == self.bbox[2:]:
                        self.ok, self.bbox = self.tracker.update(frame)
                        if not self.ok:
                            # Object is lost, fall back to find_circle
                            self.bbox = self.find_circle(cam)
                            self.init_tracker(cam)
                    else:
                        # Handle the case where frame size doesn't match
                        self.bbox = self.find_circle(cam)
                        self.init_tracker(cam)
                except cv2.error as e:
                    print(f"Error during tracker update: {e}")
                    # Handle the error gracefully, e.g., by falling back to find_circle
                    self.bbox = self.find_circle(cam)
                    self.init_tracker(cam)
            else:
                # Handle the case where frame is None
                self.bbox = self.find_circle(cam)
                self.init_tracker(cam)
        else:
            # Handle the case where self.bbox is None or all elements are 0
            self.bbox = self.find_circle(cam)
            self.init_tracker(cam)



    def draw_boundingbox(self, cam):
        frame_boundingbox = cam.get_frame()
        if self.bbox is not None:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(frame_boundingbox, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame_boundingbox, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 0, 255), 2)
        cv2.imshow("Tracking", frame_boundingbox)

    def get_center_coordinates(self):
        if self.bbox is not None:
            x, y, w, h = self.bbox
            center_x = x + w / 2
            center_y = y + h / 2
            return center_x, center_y
        else:
            return 0, 0

    def draw_cross(self, cam):

        center_x, center_y = self.get_center_coordinates()

        frame = cam.get_frame()

        # Draw horizontal line
        cv2.line(frame, (int(center_x - 10), int(center_y)), (int(center_x + 10), int(center_y)), (0, 255, 0), 2)

        # Draw vertical line
        cv2.line(frame, (int(center_x), int(center_y - 10)), (int(center_x), int(center_y + 10)), (0, 255, 0), 2)


    def find_circle(self, cam):
        # Convert the image to grayscale
        gray = cam.get_gray_frame()

        # Apply GaussianBlur to reduce noise and help the circle Detector
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,  # 1 means the accumulator has the same resolution as the input image
            minDist=30,  # Minimum distance between the centers of detected circles
            param1=70,  # Higher value means less sensitive edge Detector
            param2=70,  # Higher value allows Detector with lower confidence
            minRadius=2,  # Minimum radius of detected circles
            maxRadius=90  # Maximum radius of detected circles
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

    def find_black_dot(self, cam):

        # Finding contours in mask image
        mask_contours, _ = cv2.findContours(cam.thresh_frame(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 100:  # minimum amount of pixels to register/filter away noise
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    bbox = (x, y, w, h)
                    # cv2.putText(gray_frame, f'({x},{y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return bbox
    
    def find_red(self, cam):
        
        # Specifying the color that we want to detect
        lower = np.array([0, 250, 220])
        upper = np.array([255, 255, 225])
        # Creating a mask to find our color
        frame_rgb = cv2.cvtColor(cam.get_frame(), cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(frame_rgb(), lower, upper)
        # Finding contours in mask image
        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
         # Find the position of the contour and draw a circle
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                 # Defining the least amount of pixels, I want it to register.
                if cv2.contourArea(mask_contour) > 200:
                    # Setting up the circle
                    (x, y), radius = cv2.minEnclosingCircle(mask_contour)
                    center = (int(x), int(y))
                    radius = int(radius)
                    return x, y
        return False


    def find_person(self, cam):
        bounding_boxes = []
        person_detector = cv2.CascadeClassifier("data_cascade/haarcascade_frontalface_default.xml")

        # Assuming cam.get_gray_frame() returns the current gray frame from the camera
        gray_frame = cam.get_gray_frame()

        persons = person_detector.detectMultiScale(
            gray_frame, scaleFactor=1.05, minNeighbors=5,
            minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in persons:
            bounding_boxes.append((x, y, x + w, y + h))

        # Draw bounding boxes on the original frame
        self.draw_bounding_boxes(cam.get_frame(), bounding_boxes)

    def draw_bounding_boxes(self, frame, bounding_boxes):
        for (x1, y1, x2, y2) in bounding_boxes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
