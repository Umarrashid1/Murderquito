import cv2
from picamera2 import Picamera2
from libcamera import controls


class Camera:
    frame = None
    camera = None
    device = 0

    def __init__(self, device = 0):
        #device 0 is for pi cam, and any inputparameter is for normal pc camera
        if device == 0:
            self.camera = Picamera2()
            config = self.camera.create_preview_configuration({'format': 'RGB888'})
            self.camera.configure(config)
            self.camera.start()
            self.autofocus()
            self.frame = self.camera.capture_array()
        else:
            self.camera = cv2.VideoCapture(0)
            self.frame = self.camera.read()
            self.device = 1

    def autofocus(self):
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    def run(self):
        if self.device == 0:
            self.frame = self.camera.capture_array()
        else:
            self.frame = self.camera.read()
        return self.frame

    def show(self, name, frame):
        cv2.imshow(name, frame)

    def gray_frame(self):
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def thresh_frame(self):
        thresh_frame = cv2.threshold(self.gray_frame(), 100, 1, cv2.THRESH_BINARY_INV)[1]
        return thresh_frame
