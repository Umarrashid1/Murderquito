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
        self.servo_x = Servo("x", io)
        self.servo_y = Servo ("y", io)
        
    
    
    def move(self, coordinates):
        x = coordinates[0] / 180
        y = coordinates[1] / 180

        self.servo_x.move(x)
        self.servo_y.move(y)

    def center_laser(self, cam, det):
        #TODO: find elegant way of doing it. with and/or without trial&error / other way
        #ryk laser op/ned indtil den rammer midterlinjen
        coords = det.find_red(cam)
        center = (1280/2,720/2)
        if coords == center:
            print('oops coords == center')
            return True
        else:
            self.servo_x.move(100)
            angle_servo_x = 100
            self.servo_y.move(128)
            angle_servo_y = 128
            #NOTE: also, bare lige for at være sikker. hvor starter billedets koordina
            #lasers cordinat hvis laser 90 90. x= center_of_frame +/- cm_conv_px(cam_to_laser)
                            #if  x_coord == 1111:
                                #self.calc_angle_for_frame_center(servo_y, x_coord)
            while(det.find_red('x') > center[0]):
                angle_servo_y = angle_servo_y + 1
                self.servo_y.move(angle_servo_y)
            while(det.find_red('x') < center[0]):
                angle_servo_y = angle_servo_y - 1
                self.servo_y.move(angle_servo_y)
            while(det.find_red('y') > center[1]):
                angle_servo_x = angle_servo_x -1
                self.servo_x.move(angle_servo_x)
            while(det.find_red('y') < center[1]):
                angle_servo_x = angle_servo_x + 1
                self.servo_x.move(angle_servo_x)
            return True


    def calc_laser_angle_when_centered(self):
        #hvis laser vinkelret er = 90, så find vinkelforskel mellem det og når den peger på midten:

            angle_for_center_y = 90 - self.servo_x.angle #tjek om det er den ene eller anden laser. alt efter drejing om akse, eller bevægelse langs
            angle_for_center_x = 90 - self.servo_y.angle #same
            # angle_for_origin = den kan man også finde 
            return (angle_for_center_y, angle_for_center_x)
