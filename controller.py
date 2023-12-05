import cv2
import sys
from camera import Camera
from detection import Detection
from servo_controller import  Servo_controller


#Get CLI arguments
args = sys.argv[1:]
if len(args)>0:
    input_param = int(args[0])
else:
    input_param = None

cam = Camera(input_param)
det = Detection(cam)
servo_c = Servo_controller()
##########
# Kig i 
##########
while True:
    frame = cam.run()
    det.update_tracker(cam) #før vi overhovedet kan gå igang med det her, er der nogle ting vi skal vide ting vi skal vide: 
    #   afstand til rotationspunktet om x-aksen
    #   afstand til rotationspunktet om y-aksen

    #hvis vi så får centreret laserpunktet i billedet. nemmest bare at gøre det brute-force style:
    #
    det.draw_boundingbox(cam)

    coordinates = det.get_center_coordinates()
    print(coordinates[0], coordinates[1])
    servo_c.move(coordinates) #nej, det er dumt. kig nu på det jeg har lavet!
    #der skal bruges trigonometri
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
