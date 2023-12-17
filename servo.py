import time
import pigpio


class Servo:
    dc_min = 2.4           # duty cycle for 0 degrees
    dc_max = 12.4    # duty cyckle for 180 degrees
    pwm_hz = 50    # Frequency
    angle = 0
    axis = 0
    BottomAngles  = [-26.054 , -19.63 , -12.6 , -5.29 , 2.3 , 9.98 , 17.27 , 24.06]
    BottomSignals = [139, 132.5, 125, 117.5, 108, 100.5, 91.5, 85]
    TopAngles     = [6.21 , 8.12 , 12.39 , 23.24 , 36.3]
    TopSignals    = [62.75 , 61 , 57.5 , 45 , 33]
    
    def __init__(self, axis, io):
        self.axis = axis
        self.io = io

        if axis == "x":
            #pan
            self.pin = 12
            self.angle_offset = 10
            self.io.set_mode(self.pin, pigpio.OUTPUT)
            self.move(90)
            # højre mod venstre
        else:
            #tilt
            self.pin = 13
            self.angle_offset =  38
            self.io.set_mode(self.pin, pigpio.OUTPUT)

            self.move(88)
            #self.angle_max = 160 #?
            # op mod ned


    def move(self, angle):
        self.angle = angle
        if self.axis == "x":
            self.set_pwm(self.angle_pwm_conv(angle))
        else:
            if angle < 100
            self.set_pwm(self.angle_pwm_conv(angle))


    def angle_pwm_conv(self, angle):
        duty = (self.dc_max - self.dc_min) / 180 * angle + self.dc_min
        
    
        return duty
    
    def set_pwm(self, dc):
        print("dc is:", dc)
        self.io.hardware_PWM(self.pin, self.pwm_hz, int(dc*10000))

    def stop(self):
        self.io.stop()
        GPIO.cleanup()
