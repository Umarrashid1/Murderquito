import time
import pigpio
import io
import RPi.GPIO as GPIO

class Laser:

    def __init__(self):
        #self.io = pigpio.pi()
        self.pin = 16
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.pin, GPIO.OUT)
        #self.io.set_mode(self.pin, pigpio.OUTPUT)
        self.laser_status = 0
        self._set_laser_off()


    def toggle_laser(self, command = None):
        if command is not None:
            if command == 1:
                self._set_laser_on()
                return True
            elif command == 0: 
                self._set_laser_off()
                return True
            else:
                print("toggle_laser() Error: Invalid argument.")
        elif self.laser_status == 0:
            self._set_laser_on()
            return True
        else:
            self._set_laser_off()
            return False
        
    def _set_laser_on(self):
        self.laser_status = 1
        GPIO.output(self.pin, True)
        return True
    
    def _set_laser_off(self):
        self.laser_status = 0
        GPIO.output(self.pin, False)
        return True
    
    def fire_laser_pulse(self): NotImplemented