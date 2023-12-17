import inspect
import sys
import os
import pigpio

#til at tilgå ting i parent dir
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import time
from servo import Servo
io = pigpio.pi()
servo_x = Servo("y", io)
for i in range(180):
    servo_x.move(100)
    time.sleep(0.5)
    servo_x.move(0)
    print(i)
    time.sleep(0.5)
