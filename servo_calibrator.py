import pickle
import cv2
import math
import glob
from camera import Camera
import numpy as np
from servo import Servo
from detection import Detector
from servo_controller import Servo_controller
import time


class ServoCalibrator:
    cam_fov = 80
    cam_sensor_size = 1  # 1.22 micrometer × 1.22 micrometer     1 micrometer = 0,001mm eller tæt på
    cam_focal_length = 4.28  # mål i mm
    # cam_focal_ratio = 1.75
    cam_to_wall = 0

    def __init__(self, cam=Camera, det=Detector, servo_c=Servo_controller) -> None:
        self.cam_to_tilt_dist = 4.383 #hevet fra CAD
        self.cam_to_pan_dist = 4.904 #hevet fra CAD
        self.cam_to_pan_depth = 2.625 #hevet fra CAD
        self.dist_cam_axis_origin = math.sqrt(
            self.cam_to_tilt_dist * self.cam_to_tilt_dist + self.cam_to_pan_dist * self.cam_to_pan_dist)
        self.px_height, self.px_width, self.channels = cam.frame.shape
        self.center = (self.px_width / 2, self.px_height / 2)
        self.pan_angle, self.tilt_angle = servo_c.make_laser_perpendicular()
        time.sleep(2)
        self.las_perp_coords = det.find_red(cam.run())
        print('når laser er vinkelret:')
        print(self.las_perp_coords)

    def prepare_for_calibration(self, servo_c,  choice=None):
        self.pan_angle, self.tilt_angle = servo_c.make_laser_perpendicular()
        if (choice is None or choice == 'x'):
            time.sleep(2)
        if (choice is None or choice == 'y'):
            time.sleep(2)

    def center_laser(self, cam, det, servo_c, dist_to_wall=None):
        center = self.center

        if dist_to_wall is not None:
            self.cam_to_wall = dist_to_wall
            angles = self.calc_centerangle_from_distance(det, servo_c, dist_to_wall)
            servo_c.pan.move(angles[0])
            servo_c.tilt.move(angles[1])
            return True

        else:
            las_is_centered = False
            while las_is_centered is False:
                frame = cam.run()
                print(center)
                las_coords = det.find_red(frame)
                if las_coords is False:
                    print("Error: no laser found!")
                if (las_coords[0] != center[0]):
                    if (las_coords[0] > center[0] and self.pan_angle < 180):
                        if (las_coords[0] > center[0] + 20 and self.pan_angle < 180):
                            self.pan_angle = self.pan_angle + 1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(1)
                        elif (las_coords[0] > center[0] + 10 and self.pan_angle < 180):
                            self.pan_angle = self.pan_angle + 0.1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.5)
                        else:
                            self.pan_angle = self.pan_angle + 0.5
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.2)
                    elif las_coords[0] < center[0] and self.pan_angle > 0:
                        if las_coords[0] < center[0] - 20 and self.pan_angle > 0:
                            self.pan_angle = self.pan_angle - 1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(1)
                        elif las_coords[0] < center[0] - 10 and self.pan_angle > 0:
                            self.pan_angle = self.pan_angle - 0.1
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.5)
                        else:
                            self.pan_angle = self.pan_angle - 0.05
                            servo_c.pan_servo.move(self.pan_angle)
                            time.sleep(0.2)
                if las_coords[1] != center[1]:
                    if las_coords[1] < center[1] and self.tilt_angle < 180:
                        if las_coords[1] < center[1] - 20 and self.tilt_angle < 180:
                            self.tilt_angle = self.tilt_angle + 1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(1)
                        elif las_coords[1] < center[1] - 10 and self.tilt_angle < 18:
                            self.tilt_angle = self.tilt_angle + 0.1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.5)
                        else:
                            self.tilt_angle = self.tilt_angle + 0.05
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.2)
                    elif las_coords[1] > center[1] and self.tilt_angle > 0:
                        if las_coords[1] > center[1] + 20 and self.tilt_angle < 18:
                            self.tilt_angle = self.tilt_angle - 1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(1)
                        elif las_coords[1] > center[1] + 10 and self.tilt_angle < 180:
                            self.tilt_angle = self.tilt_angle - 0.1
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.5)
                        else:
                            self.tilt_angle = self.tilt_angle - 0.05
                            servo_c.tilt_servo.move(self.tilt_angle)
                            time.sleep(0.2)
                if las_coords[1] < center[1] * 1.05 and las_coords[1] > center[1] * 0.95:
                    if las_coords[0] < center[0] * 1.05 and las_coords[0] > center[0] * 0.95:
                        las_is_centered = True
                        return True, (self.pan_angle, self.tilt_angle)

    def find_indiv_center_angles(self, cam, det, servo_c, chosen_servo=None):
        center = self.center

        if chosen_servo == 'x':
            servo = 0
            angle = self.pan_angle
        elif chosen_servo == 'y':
            servo = 1
            angle = self.tilt_angle

        center_angle_found = False
        while center_angle_found is False:
            frame = cam.run()
            las_cord = det.find_red(frame)
            print("centercoords:")
            print(center)
            print("laser coords:")
            print(las_cord)
            if las_cord[servo] != center[servo] :
                if las_cord[servo] > center[servo]:
                    if las_cord[servo] > center[servo] + 20:
                        angle = angle - 1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(1)
                    elif las_cord[servo] > center[servo] + 10:
                        angle = angle - 0.1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                    else:
                        angle = angle - 0.05
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                elif las_cord[servo] < center[servo]:
                    if las_cord[servo] < center[servo] - 20:
                        angle = angle + 1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(1)
                    elif las_cord[servo] < center[servo] - 10:
                        angle = angle + 0.1
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                    else:
                        angle = angle + 0.05
                        servo_c.servoes[servo].move(angle)
                        time.sleep(0.5)
                if chosen_servo == 'y':
                    self.tilt_angle = angle
                elif chosen_servo == 'x':
                    self.pan_angle = angle
                if las_cord[servo] < center[servo] + 2 and las_cord[servo] > center[servo] - 2:
                    return True

    def calc_centerangle_from_distance(self, dist_to_wall):
        # Given α(angle of corner at wall): β(angle of laser corner) = 90 - α
        # β = arctan(b / a)     OR     β = arccot(a / b)
        self.centered_pan_angle = math.degrees(math.atan2((dist_to_wall + self.cam_to_pan_depth), self.cam_to_pan_dist))  + 100 # servo_c.pan.angle_offset
        self.centered_tilt_angle = math.degrees(math.atan2((dist_to_wall + self.cam_to_pan_depth), self.cam_to_tilt_dist)) + 128  # + 90 + servo_c.tilt.angle_offset
        print('calculated angles(pan, tilt) for center, using distance of:' + str(dist_to_wall))
        print(self.centered_pan_angle, self.centered_tilt_angle)
        return (self.centered_pan_angle, self.centered_tilt_angle)

    def calc_dist_from_centerangle(self, servo_c=Servo_controller, choice=None):
        # laseren skal  vaere centreret
        # b = a × tan(β)
        pan_angle = servo_c.pan_servo.angle - 10
        tilt_angle = servo_c.tilt_servo.angle - 38
        pan_angle = pan_angle - 90
        tilt_angle = tilt_angle - 90
        pan_angle = 90 - pan_angle
        tilt_angle = 90 - tilt_angle
        # b = a × tan(β) #men tag højde for at vinklen er påvirket af dybdeforskellen mellem kamera og origo. bare træk den fra
        cam_to_wall_pan = self.cam_to_pan_dist * (math.tan(math.radians(pan_angle))) + self.cam_to_pan_depth
        cam_to_wall_tilt = self.cam_to_tilt_dist * (math.tan(math.radians(tilt_angle))) + self.cam_to_pan_depth
        print('cam_to_wall_pan:')
        print(cam_to_wall_pan)
        print('cam_to_wall_tilt:')
        print(cam_to_wall_tilt)


        # cam_to_wall_pan = self.cam_to_tilt_dist * (math.tan(tilt_angle))
        # cam_to_wall_tilt = self.cam_to_pan_dist  * (math.tan(pan_angle))
        # tjek om de giver den samme distance til væggen. returnerer om de giver den samme distance, og så en distance
        if cam_to_wall_pan == cam_to_wall_tilt:
            self.cam_to_wall = cam_to_wall_pan
            return True, cam_to_wall_pan
        elif choice == 'y':
            return cam_to_wall_tilt
        elif choice == 'x':
            return cam_to_wall_pan
        else:
            self.cam_to_wall = (cam_to_wall_pan + cam_to_wall_tilt / 2)
            return False, ((cam_to_wall_pan + cam_to_wall_tilt) / 2)

    def calc_dim_conv_fact_perpendicular_laser(self):
        # hvis laseren er lige på, så er afstand fra midten til laserdot, det samme som kamera til laser
        pixel_dist =  (abs(self.las_perp_coords[0] - self.center[0]), abs(self.las_perp_coords[1] - self.center[1]))

        self.px_to_cm_width_scale = (pixel_dist[0] / self.cam_to_pan_dist)
        self.px_to_cm_height_scale = (pixel_dist[1] / self.cam_to_tilt_dist)

        return  self.px_to_cm_width_scale, self.px_to_cm_height_scale

    def get_angle_for_coords(self, coords):
        #skal nok omskrives for læsbarhed of effekt
        print('self.px_to_cm_width_scale')
        print(self.px_to_cm_width_scale)
        print('self.px_to_cm_height_scale')
        print(self.px_to_cm_height_scale)
        px_dist_x = abs(coords[0] - self.las_perp_coords[0])
        real_pan_dist = px_dist_x / self.px_to_cm_width_scale
        if coords[0] > self.las_perp_coords[0]:
            pan_angle_is_pos = False
        else:
            pan_angle_is_pos = True
        px_dist_y = abs(coords[1] - self.las_perp_coords[1])
        real_tilt_dist = px_dist_y / self.px_to_cm_height_scale
        print('px_dist_x')
        print(px_dist_x)
        print('px_dist_y')
        print(px_dist_y)
        if coords[1] < self.las_perp_coords[1]:
            tilt_angle_is_pos = False
        else:
            tilt_angle_is_pos = True
        
        if real_pan_dist > 0:
            a = real_pan_dist
            b = self.cam_to_wall
            print('real_pan_dist')
            print(a)
            print('self.cam_to_wall')
            print(b)
            real_pan_angle = math.degrees(math.atan2(a,b))
            if pan_angle_is_pos is False:
                real_pan_angle + real_pan_angle * -1
        else: real_pan_angle = False
        a = real_tilt_dist
        b = self.cam_to_wall
        print('real_tilt_dist')
        print(a)
        print('self.cam_to_wall')
        print(b)
        if real_tilt_dist > 0:
            
            real_tilt_angle = math.degrees(math.atan2(a,b))
            print('real_tilt_angle')
            print(real_tilt_angle)
            if tilt_angle_is_pos is False:
                real_tilt_angle = real_tilt_angle * -1
        else: real_tilt_angle = False

        #returnerer vinkler som skal lægges / trækkes fra perpendicular angle: ((vinkel, True for læg til, False træk fra), (tilt-vinkel)
        return (real_pan_angle , real_tilt_angle)

