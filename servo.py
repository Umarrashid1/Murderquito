import time
import pigpio

class Servo:
    dc_min = 1       # duty cycle for 0 degrees
    dc_max = 12    # duty cyckle for 180 degrees
    pwm_hz = 50    # Frequency
    angle = 0
    axis = 0

    def __init__(self, axis, io):
        
        self.axis = axis
        if axis == "x":
            self.pin = 14
        else:
            self.pin = 15

        self.angle = 90

        self.io.set_mode(self.pin, pigpio.OUTPUT)
        

    def move(self, angle):
        self.set_pwm(self.angle_pwm_conv(angle))

    def angle_pwm_conv(self, angle):
        duty = (self.dc_max - self.dc_min) / 180 * angle + self.dc_min
        return duty
    
    def set_pwm(self, dc):
        if dc < self.dc_min or dc > self.dc_max:
            raise Exception

        self.io.hardware_PWM(self.pin, self.pwm_hz, int(duty*10000))



    def stop(self):
        self.io.hardware_PWM(self.pin, 0, 0)
        GPIO.cleanup()
