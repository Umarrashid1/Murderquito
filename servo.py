import pigpio
import time
import GPIO


class Servo:
    dc_min = 1       # duty cycle for 0 degrees
    dc_max = 12    # duty cyckle for 180 degrees
    pwm_hz = 50    # Frequency

    def __init__(self, axis, PIN):
        self.axis = axis
        self.angle = 0
        GPIO.setmode(GPIO.PWM)
        if axis == "x":
            self.pin = 14
        else:
            self.pin = 15
        GPIO.setup(self.pin, GPIO.OUT)
        self.io = GPIO.PWM(self.pin, 50)
        self.io.start(0)  #Initizialation

    def move(self, angle):
        if angle < 180 or angle > 0:
            if angle != angle:
                self.angle = angle
                self.set_pwm(self.angle_pwm_conv(angle))

    def angle_pwm_conv(angle):
        duty = (dc_max - dc_min) / 180 * angle + dc_min
        return duty
    
    def set_pwm(dc):
         io.ChangeDutyCycle(dc_min)

    def stop():
        p.stop()
        GPIO.cleanup()
