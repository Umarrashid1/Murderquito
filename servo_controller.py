import time
import math
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
        self.tilt_servo = Servo("y", io)
        self.servoes = (self.pan_servo, self.tilt_servo)

    def move_center(self): NotImplemented

    # skal bare have de gemte koordinater fra midten blev fundet under kalibrering.
    def convert_pixel_angles(self, coordinates, linear_ratio, frame):
        img_height, img_width, _ = frame.shape
        # calc X and Z using linear_ratio
        X = ((img_width / 2) - coordinates[0]) * linear_ratio
        Y = (coordinates[1] - (img_height / 2)) * linear_ratio
             
        # calculate target position relative to turret
        x = X + 49.04         
        y = Y + 43.83
        z = 1300 + 26.25
        
        if x < 0:
            x = abs(X + 49.04)
            bottom_angle = math.degrees(math.atan2(x, z)) * -1
        else:
            # calc the bottom servo angle and conv to degrees
            bottom_angle = math.degrees(math.atan2(x, z))

        if y < 0:
            y = abs(Y + 43.83)
            top_angle = math.degrees(math.atan2(y,z)) * -1
        else:
            top_angle = math.degrees(math.atan2(y,z)) 
        # temp variable
        #h = math.sqrt(x * x + z * z)

        # calc the top servo angle and conv to degrees
        #top_angle = math.degrees(math.atan(y / h))
        

        return bottom_angle, top_angle
         
    def move(self, coordinates, linear_ratio, frame):

        bottom_angle, top_angle = self.convert_pixel_angles(coordinates, linear_ratio, frame)
        bottom_angle = (int(bottom_angle))
        top_angle = (int(top_angle))
        print("Angle is:", bottom_angle, top_angle)
        self.pan_servo.move(bottom_angle)
        self.tilt_servo.move(top_angle)
