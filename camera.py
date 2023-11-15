import cv2
from picamera2 import Picamera2


class Camera:

    def __init__(self):
        self.camera = Picamera2()

    def start(self):
        self.camera.start

    def autofocus(self):
        autofocus

    def run(self):
        frame = self.camera.capture_array()
        return frame

    def show(self):
        cv2.imshow("camera", self.frame)
       # if cv2.waitKey(1)==ord('q'):
        #    break
    #cv2.destroyAllWindows()