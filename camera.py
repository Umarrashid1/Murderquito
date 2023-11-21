import cv2
from picamera2 import Picamera2
from libcamera import controls


class Camera:
    frame = 0
    camera = 0

    def init(self):
        self.camera = Picamera2()
        config = self.camera.create_preview_configuration({'format': 'RGB888'})
        self.camera.configure(config)

    def start(self):
        self.camera.start()

    def autofocus(self):
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    def run(self):
        self.frame = self.camera.capture_array()
        return self.frame

    def show(self, name, frame):
        cv2.imshow(name, frame)

    def gray_conv(self, frame):
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.frame

    def thresh(self, frame):
        self.frame = cv2.threshold(frame, 100, 1, cv2.THRESH_BINARY_INV)[1]
        return self.frame
