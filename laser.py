import time
import pigpio
import io
import RPi.GPIO as GPIO

class Laser:

    def __init__(self, pulse_ln = None):
        self.io = pigpio.pi()
        if pulse_ln is None: 
            self.pulse_length = 2
        else:
            self.pulse_length = pulse_ln
        GPIO.setwarnings(False)
        self.pin = 16
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.pin, GPIO.OUT)
        #self.io.set_mode(self.pin, pigpio.OUTPUT)
        self.laser_status = 0
        self._set_laser_off()


    def toggle_laser(self, command = None):
        if command is not None:
            if command == 1:
                self.laser_status = self._set_laser_on()
                return True
            elif command == 0: 
                self.laser_status = self._set_laser_off()
                return False
            else:
                print("toggle_laser() Error: Invalid argument.")
        elif self.laser_status == 0:
            self.laser_status = self._set_laser_on()
            return True
        else:
            self.laser_status = self._set_laser_off()
            return False
        
    def _set_laser_on(self):
        self.laser_status = 1
        GPIO.output(self.pin, True)
        return True
    
    def _set_laser_off(self):
        self.laser_status = 0
        GPIO.output(self.pin, False)
        return False
    
    def fire_pulse(self, duration = None):
        if duration is None: duration = self.pulse_length
        self.laser_status = self._set_laser_on()
        time.sleep(duration)
        self.laser_status = self._set_laser_off()
    
    def set_pulse_length(self, time_ln):
        self.pulse_length = time_ln