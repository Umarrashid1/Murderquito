import cv2
from picamera2 import Picamera2


class Camera:
    frame = 0
    camera = 0

    def __init__(self):
        self.camera = Picamera2()
        return self.camera

    def start(self, camera):
        camera.start

    def autofocus(self):
        autofocus

    def run(self, camera):
        self.frame = camera.capture_array()
        return self.frame

    def show(self):
        cv2.imshow("camera", self.frame)
       # if cv2.waitKey(1)==ord('q'):
        #    break
    #cv2.destroyAllWindows()

    def gray_conv(self, frame):
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.frame

    def thresh(self, frame):
        self.frame = cv2.threshold(frame, 100, 1, cv2.THRESH_BINARY_INV)[1]
        return self.frame

    def imshow(self, name, img)
        cv2.imshow("image", frame)
