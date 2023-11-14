import time
import io
from servo import Servo

servo_x = Servo("x")
time.sleep(5)
servo_x.move(180)
servo_x.stop()
