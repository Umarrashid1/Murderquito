from BoundingBoxes import BoundingBoxes
import cv2


class Circle(BoundingBoxes):
    def __init__(self, x, y, radius, contour_points):
        super().__init__(x, y)
        self.radius = radius
        self.center = (self.x + self.radius, self.y + self.radius)
        self.contour_points = contour_points

    @classmethod
    def from_contours(cls, contours):
        max_contour = max(contours, key=cv2.contourArea)
        if max_contour is not None:
            ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
            return cls(int(x), int(y), int(radius), max_contour)

    def display(self, frame):
        cv2.circle(frame, (self.x, self.y), self.radius, (0, 0, 255), 3)
        cv2.putText(frame, f'({self.x}, {self.y})', (self.x, self.y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.circle(frame, (self.x, self.y), 3, (0, 255, 255), -1)
