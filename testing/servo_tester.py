import time
import io
from servo import Servo

servo_x = Servo("x")
time.sleep(5)
servo_x.move(179)
time.sleep(5)
servo_x.move(90)
time.sleep(5)
servo_x.stop()
