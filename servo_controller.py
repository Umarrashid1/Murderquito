import time
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
        self.tilt_servo = Servo ("y", io)
        self.make_laser_perpendicular()
        self.servoes = (self.pan_servo, self.tilt_servo)

    def make_laser_perpendicular(self):
        self.pan_servo.move(100)
        self.pan_servo.angle = 100
        time.sleep(2)
        self.tilt_servo.move(128)
        self.tilt_servo.angle = 128
        time.sleep(2)
        return self.pan_servo.angle, self.tilt_servo.angle    
    
    def move(self, coordinates):
        x = coordinates[0] / 180
        y = coordinates[1] / 180

        

    def center_laser(self, cam, det):
        #TODO: find elegant way of doing it. with and/or without trial&error / other way
        #ryk laser op/ned indtil den rammer midterlinjen
        coords = det.find_red(cam)
        center = (1280/2,720/2)
        if coords == center:
            print('oops coords == center')
            return True
        else:
            self.pan_servo.move(100)
            pan_angle = 100
            self.tilt_servo.move(128)
            tilt_angle = 128
            #NOTE: also, bare lige for at være sikker. hvor starter billedets koordina
            #lasers cordinat hvis laser 90 90. x= center_of_frame +/- cm_conv_px(cam_to_laser)
                            #if  x_coord == 1111:
                                #self.calc_angle_for_frame_center(servo_y, x_coord)
            while(det.find_red('x') > center[0]):
                tilt_angle = tilt_angle + 1
                self.tilt_servo.move(tilt_angle)
            while(det.find_red('x') < center[0]):
                tilt_angle = tilt_angle - 1
                self.tilt_servo.move(tilt_angle)
            while(det.find_red('y') > center[1]):
                pan_angle = pan_angle -1
                self.pan_servo.move(pan_angle)
            while(det.find_red('y') < center[1]):
                pan_angle = pan_angle + 1
                self.pan_servo.move(pan_angle)
            return True


    def calc_laser_angle_when_centered(self):
        #hvis laser vinkelret er = 90, så find vinkelforskel mellem det og når den peger på midten:

            pan_angle_for_frame_center = 90 - self.pan_servo.angle #tjek om det er den ene eller anden laser. alt efter drejing om akse, eller bevægelse langs
            tilt_angle_for_frame_center = 90 - self.tilt_servo.angle #same
            # angle_for_origin = den kan man også finde 
            return (pan_angle_for_frame_center, tilt_angle_for_frame_center)
