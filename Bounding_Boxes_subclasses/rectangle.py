from boundingboxes import BoundingBoxes
import cv2


class Rectangle(BoundingBoxes):
    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.w = w
        self.h = h

    def display(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 0, 0), 2)
