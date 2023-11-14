#added calibration file with some different (WIP) coord/angle and dimension approximations
import cv2
import math

class Calibrator:
    cam_to_laser = 4
    cam_fov = 80
    cam_px_width = 1080
    cam_px_height = 720

    # β=arctan(b/a)

    def px_dim_conv():
        #kend væggens bredde højde i billedrammen, eller dimensionerne på et objekt i billedet
        fucknuaf=1

    def approximate_distance_to_wall():
            #kassen har kendte dimensioner: x_cm y_cm
            #kameraet har oploesning : x_pixel y_pixel
            #find kasses x_pixel y_pixel
            #brug det til at finde billedrammens bredde x_cm og hoejde y_cm
                #Kamera_x_pixel / kasse_x_pixel
            #und so weiter

            black_box_dim = 2
            mask_contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Find the position of the contour and draw a circle
            if len(mask_contours) != 0:
                for mask_contour in mask_contours:
                    # Defining the least amount of pixels, I want it to register.
                    if cv2.contourArea(mask_contour) > 100:
                        # Setting up the circle
                        (x, y), radius = cv2.minEnclosingCircle(mask_contour)
                        center = (int(x), int(y))
                        radius = int(radius)

                        # Creating the circle
                        cv2.circle(video, center, radius, (0, 0, 255), 3)

                        # Show coordinates for the center of the black object
                        cv2.putText(video, f'({x},{y})', center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.circle(video, center, 3, (0, 255, 255), -1)

    def calculate_frame_dimensions():
        #hvis laser peger lige frem, så er:
        # center_to_dot == cam_to_laser
        #omregn mellem pixel og cm

        #hvis laser centreret og cam_to_wall er kendt
        a = 1

    def calc_angle_for_frame_center(): #
        #   Use Pythagoras with DISTANCE between LASER ORIGIN and CAMERA CENTER 
        #   alongside distance of WALL to calculate LASER ANGLE]
        #   use x_coords to get x_angle     y_coords for angle_y
        cam_to_laser = 3
        cam_to_wall = 5

        laser_dot_x = 2
        laser_dot_y = 2
            #vinklen for hvor laser ville møde midten af kameraet
            #   α=arctan(a/b) for trekant med a = mid_to_dot, b = cam_to_wall
            #   laser_vinkel = 90 - arctan(mid_to_dot/cam_to_wall)
        
        #gider ikke flere trekanter lige nu

    def calc_angle_from_distance(self):
        cam_to_wall = 12
        laser_x = 1
        laser_y = 1 #kald track eller identification

    def calc_distance_from__angle(self):
        
        #laseren skal enten vaere centreret, ellers skal den være i billedet om man skal omregne dimensioner til pixel
        cam_to_laser = 4

        #
        x_angle = 2
        y_angle = 2 #servo.get_angle(y)?



        errr=1

    def center_laser_in_img():
        #ryk laser op/ned indtil den rammer midterlinjen
        #samme for højre venstre
        #når laser_dot = center_of_frame succes



