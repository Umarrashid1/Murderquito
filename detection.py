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
        self.bbox = self.find_circle(cam.gray_frame())
        self.init_tracker(cam)
    
    def init_tracker(self, cam):
        ok = self.tracker.init(getattr(cam, 'frame'), self.bbox)

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

    def find_circle(self, image):
        # Apply GaussianBlur to reduce noise and help the circle detection
        blurred = cv2.GaussianBlur(image, (9, 9), 2)

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