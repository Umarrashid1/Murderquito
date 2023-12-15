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
            #pan
            self.pin = 12
            self.angle_offset = 10
            # højre mod venstre
        else:
            #tilt
            self.pin = 13
            self.angle_offset =  38
            #self.angle_max = 160 #?
            # op mod ned
        self.io = io
        self.io.set_mode(self.pin, pigpio.OUTPUT)

    def move(self, angle):
        self.angle = angle
        if self.axis == "x":
            self.set_pwm(self.angle_pwm_conv(angle + 100))
        else:
            self.set_pwm(self.angle_pwm_conv(angle + 128))


    def angle_pwm_conv(self, angle):
        duty = (self.dc_max - self.dc_min) / 100 * angle + self.dc_min
    
    
        return duty
    
    def set_pwm(self, dc):
        print("dc is:", dc)
        self.io.hardware_PWM(self.pin, self.pwm_hz, int(dc*10000))

    def stop(self):
        self.io.stop()
        GPIO.cleanup()
