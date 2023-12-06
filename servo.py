import pigpio
import time
import RPi.GPIO as GPIO


class Servo:
    dc_min = 1       # duty cycle for 0 degrees
    dc_max = 12    # duty cyckle for 180 degrees
    pwm_hz = 50    # Frequency
    angle = 0
    axis = 0
    def __init__(self, axis):
        self.axis = axis
        GPIO.setmode(GPIO.BCM)
        if axis == "x":
            self.pin = 14
        else:
            self.pin = 15
        GPIO.setup(self.pin, GPIO.OUT)
        self.io = GPIO.PWM(self.pin, 50)
        self.io.start(0)  # Initizialation
        self.move(0)    # Move to current angle (0)

    def move(self, angle):
        print("angle:", angle)
        print("self.angle:", self.angle)
        if angle != self.angle:
            self.angle = angle + 90
            self.set_pwm(self.angle_pwm_conv(angle))

    def angle_pwm_conv(self, angle):
        duty = (self.dc_max - self.dc_min) / 180 * angle + self.dc_min
        return duty
    
    def set_pwm(self, dc):
        self.io.ChangeDutyCycle(dc)

    def stop(self):
        self.io.stop()
        GPIO.cleanup()
