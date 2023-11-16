from BoundingBoxes import BoundingBoxes
import cv2

class Circle(BoundingBoxes):
    def __init__(self, x, y, h, w, radius, center, cascade_or_mask_object):
        super().__init__(x, y, cascade_or_mask_object)
        self.radius = radius
        self.center = center

    def calc_radius(self, frame):
        (self.x, self.y), self.radius = cv2.minEnclosingCircle(frame)
        self.radius = int(self.radius)
        return self.radius

    def calc_center(self):
        self.center = (int(self.x), int(self.y))
        return self.center

    def circle_bounding_box(self, frame):
        # Creating the circle
        cv2.circle(frame, self.center, self.radius, (0, 0, 255), 3)

        # Show coordinates for the center of the black object
        cv2.putText(frame, f'({self.x},{self.y})', self.center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.circle(frame, self.center, 3, (0, 255, 255), -1)
