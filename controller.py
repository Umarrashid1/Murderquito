import cv2
import sys
from camera import Camera
from detection import Detector
from servo_controller import  Servo_controller


#Get CLI arguments
args = sys.argv[1:]
if len(args)>0:
    input_param = int(args[0])
else:
    input_param = None

cam = Camera(input_param)
det = Detector(cam)
servo_c = Servo_controller()

while True:
    frame = cam.run()
    det.update_tracker(cam) #før vi overhovedet kan gå igang med det her, er der nogle ting vi skal vide ting vi skal vide: 
    #   afstand fra kameramidten til rotationspunktet om x-aksen
    #   afstand fra kameramidten til rotationspunktet om y-aksen
        #se skitse i fuckinglorteclean

    #vil også sige at vi skal bruge kamerakalibrering først
    #så skal vi have centreret laserpunktet i billedet. nemmest bare at gøre det brute-force style:
    #se servoCalibrator.center_laser_in_img(det, servo_x, servo_y) NOTE: servo x og y og servocontrolller..fgh

    # vi kan udregne afstanden på et par måder. 

        #hvis vi fysisk har målt afstanden til væg: 
        # #servoCalibrator.calc_laser_angle_from_distance(det, servo_x, servo_y)
        # så vi kan tjekke om tingene stemmer overens

        #ellers kan vi bruge lidt snyd til at udregne en vinkel for midten. Hvis ikke servoerne allerede giver vinklerne:
        # servoCalibrator.calc_laser_angle_when_centered(det, servo_x, servo_y)
        # Når den er centreret BØR det være en retvinklet trekant. b = a × tan(β), derfor:
        # servoCalibrator.calc_dist_angle(det, servo_x, servo_y)

        #hvis laseren ikke er centreret kan man bruge noget pis med focal length osv. det er lort. Man kunne også benytte sig af at kameraet har en fov =80

    # hvis vi kan finde ud af hvor mange pixels der går på ?? cm, så kan vi finde ud af afstande på væggen (kræver nok at kameraet er kalibreret. muligivs også omtanke for focal og lense Bullshit)
    # med afstande kan vi hurtigere udregne vinkler til servoerne. tænk: hvis vi har vinkel for midten til myg (det har vi, hvis vi bruger de andre ting) samt vinkel for servo til midten, 
        # så kan vi nemt finde vinklen fra laser til myg
     #måske også notere hvor meget servoen bevæger sig med 1 grads drejning. giver maske hurtige respons senere.
     # den kan også bare kontinuerligt følge den. Der skal vi også kende laserens placering, selv hvis den er slukket

     #jeg er træt, men så burde vi nemt kunne kortlægge coordinater med laser vinkler

     #så er der også det med at kameraet måske står lidt skævt, laseren måske sidder lidt skævt og fuck mig 

    #det var det jeg ville tjekke over weekenden, men... fucking clean
    det.draw_cross(cam)
    det.draw_boundingbox(cam)

    coordinates = det.get_center_coordinates()
    servo_c.move(coordinates)
    #servo_c.move(coordinates)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# ##########    se evt:     ######################
#   https://www.youtube.com/watch?v=1CVmjTcSpIw
#   https://www.youtube.com/watch?v=sW4CVI51jDY&t=1202s
#   OneNote -> Vidensindsamling -> Computer Visualization og openCV -> GODE VIDEOER
######################################