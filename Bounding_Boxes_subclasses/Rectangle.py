from BoundingBoxes import BoundingBoxes
import cv2


class Rectangle(BoundingBoxes):
    def __init__(self, cascade, x, y, w, h):
        super().__init__(cascade)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def rectangle_bounding_box(self, frame):
        for x, y, w, h in self.cascade_or_mask_object:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
