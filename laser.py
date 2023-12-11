import time
import pigpio
import io
import RPi.GPIO as GPIO

class Laser:

    def __init__(self):
        #self.io = pigpio.pi()
        self.pin = 17
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(17, GPIO.OUT)
        #self.io.set_mode(self.pin, pigpio.OUTPUT)
        self.laser_status = 0


    def toggle_laser(self):
        if self.laser_status == 0:
            self.laser_status = 1
            GPIO.output(17, True)
            return True
        else:
            self.laser_status = 0
            GPIO.output(17, False)
            return True