import inspect
import sys
import os

#til at tilgå ting i parent dir
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

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
