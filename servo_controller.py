import time
import io
from servo import Servo


class Servo_controller:
    
    def __init__(self):
        self.servo_x = Servo("x")
        self.servo_y = Servo ("y")
    
    
    def move(self, coordinates):
        x = coordinates[0] / 180
        y = coordinates[1] / 180

        self.servo_x.move(x)
        self.servo_y.move(y)
