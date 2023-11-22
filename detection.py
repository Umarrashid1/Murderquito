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
        self.bbox = self.find_circle(cam)
       # self.init_tracker(cam)

    def init_tracker(self, cam):
        self.tracker.init(getattr(cam, 'frame'), self.bbox)

    def update_tracker(self, cam):
        ok, self.bbox = self.tracker.update(getattr(cam, 'frame'))

    def draw_boundingbox(self, cam):
        frame_boundingbox = cam.gray_frame()
        if self.ok:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(frame_boundingbox, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame_boundingbox, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.imshow("Tracking", frame_boundingbox)

    def find_circle(self, cam):
        # Convert the image to grayscale
        gray = cam.gray_frame()

        # Apply GaussianBlur to reduce noise and help the circle detection
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=30,
            param1=50,
            param2=30,
            minRadius=2,
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

    def find_black_dot(self, cam):
        
        # Finding contours in mask image
        mask_contours, _ = cv2.findContours(cam.thresh_frame(), cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour) > 100:  # minimum amount of pixels to register/filter away noise
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    bbox = (x, y, w, h)
                    #cv2.putText(gray_frame, f'({x},{y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return bbox