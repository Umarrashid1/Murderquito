import time
import io
from servo import Servo

servo_x = Servo("x")
time.sleep(5)
servo_x.move(150)
time.sleep(5)
servo_x.move(1)
servo_x.stop()
