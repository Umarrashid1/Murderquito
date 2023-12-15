import time
import io
import pigpio
from servo import Servo
from detection import Detector

# højre mod venstre 0 mod 180 : midtpunkt = 100 (ikke halvfems)
# op mod ned 0 mod 180 : midtpunkt = 128 (ikke halvfems)

class Servo_controller:
    
    def __init__(self):
        io = pigpio.pi()
        self.pan_servo = Servo("x", io)
        self.tilt_servo = Servo ("y", io)
        self.make_laser_perpendicular()
        self.servoes = (self.pan_servo, self.tilt_servo)

    def make_laser_perpendicular(self):
        self.pan_servo.move(100)
        self.pan_servo.angle = 100
        time.sleep(2)
        self.tilt_servo.move(128)
        self.tilt_servo.angle = 128
        time.sleep(2)
        return self.pan_servo.angle, self.tilt_servo.angle    
    
    def move(self, coordinates):
        x = coordinates[0] / 180
        y = coordinates[1] / 180

    def move_center(self): NotImplemented
    #skal bare have de gemte koordinater fra midten blev fundet under kalibrering.

