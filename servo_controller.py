import time
import io
import pigpio
from servo import Servo
from detection import Detector


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

    def center_laser(self, det = Detector):
        #TODO: find elegant way of doing it. with and/or without trial&error / other way
        #ryk laser op/ned indtil den rammer midterlinjen
        coords = det.find_red()
        if coords == (1280/2,720/2):
            return True
        else:
            self.servo_x.move(90)
            self.servo_y.move(90)
            #NOTE: also, bare lige for at være sikker. hvor starter billedets koordina
            #lasers cordinat hvis laser 90 90. x= center_of_frame +/- cm_conv_px(cam_to_laser)
                            #if  x_coord == 1111:
                                #self.calc_angle_for_frame_center(servo_y, x_coord)
            while(det.find_red('x') > coords[0]):
                self.servo_y.move(self.servo_y.angle-1)
            while(det.find_red('x') < coords[0]):
                self.servo_y.move(self.servo_y.angle+1)
            while(det.find_red('y') > coords[1]):
                self.servo_x.move(self.servo_x.angle-1)
            while(det.find_red('y') < coords[1]):
                self.servo_x.move(self.servo_x.angle+1)
            return True


    def calc_laser_angle_when_centered(self):
        #hvis laser vinkelret er = 90, så find vinkelforskel mellem det og når den peger på midten:

            angle_for_center_y = 90 - self.servo_x.angle #tjek om det er den ene eller anden laser. alt efter drejing om akse, eller bevægelse langs
            angle_for_center_x = 90 - self.servo_y.angle #same
            # angle_for_origin = den kan man også finde 
            return (angle_for_center_y, angle_for_center_x)
