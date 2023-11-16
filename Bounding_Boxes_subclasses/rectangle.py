from boundingboxes import BoundingBoxes
import cv2


class Rectangle(BoundingBoxes):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def display(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), (255, 0, 0), 2)
