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
io = pigpio.pi()

servo_x = Servo("x", io)
for i in range(180):
    servo_x.move(i)
    print(i)
    time.sleep(0.5)
