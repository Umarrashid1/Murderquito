import cv2


class Camera:
    frame = None
    camera = None
    device = 0

    def __init__(self, device = 0):
        #device 0 is for pi cam, and any inputparameter is for normal pc camera
        if device == 0:
            from picamera2 import Picamera2
            self.camera = Picamera2()
            config = self.camera.create_preview_configuration({'format': 'RGB888'})
            self.camera.configure(config)
            self.camera.start()
            self.autofocus()
            self.frame = cv2.flip(self.camera.capture_array(), 0)
        else:

            self.camera = cv2.VideoCapture(0)
            ok, int_frame = self.camera.read()
            self.frame = cv2.flip(int_frame)
            self.device = 1
        # print("value of frame:", self.frame)
    def autofocus(self):
        from libcamera import controls
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    def run(self):
        if self.device == 0:
            self.frame = cv2.flip(self.camera.capture_array(), 0)
        else:
            ok, self.frame = self.camera.read()
        return self.frame

    def show(self, name, frame):
        cv2.imshow(name, frame)

    def get_frame(self):
        return self.frame

    def get_gray_frame(self):
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def get_thresh_frame(self):
        thresh_frame = cv2.threshold(self.gray_frame(), 100, 1, cv2.THRESH_BINARY_INV)[1]
        return thresh_frame
