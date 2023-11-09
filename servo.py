import pigpio
import time


class Servo:
    dc_low = 1       # duty cycle for 0 degrees
    dc_high = 12    # duty cyckle for 180 degrees
    pwm_hz = 50    # Frequency

    def __init__(self, axis):
        self.axis = axis
        self.angle = 0

    def move(self, angle):
        if angle <  180 or angle > 0:
            if angle != angle
            self.angle = angle
            self.set_pwm(self.angle_pwm_conv(angle))

    
    def angle_pwm_conv(angle):
        duty = #insert convertion math
        return dc
    
    def set_pwm(dc)