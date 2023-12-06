import time
import io
import pigpio
from servo import Servo


class Servo_controller:
    
    def __init__(self):
        io = pigpio.pi()
        self.servo_x = Servo("x", io)
        self.servo_y = Servo ("y", io)
    
    
    def move(self, coordinates):
        x = coordinates[0] / 180
        y = coordinates[1] / 180

        self.servo_x.move(x)
        self.servo_y.move(y)
