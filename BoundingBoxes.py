# Superclass
class BoundingBoxes:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self, frame):
        raise NotImplementedError("Subclasses must implement the display method")
