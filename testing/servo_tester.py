import inspect
import sys
import os
import pigpio

# til at tilgaa ting i parent dir
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import time
from servo import Servo
io = pigpio.pi()
servo_x = Servo("x", io)
servo_y = Servo("y", io)
for i in range(10):
    servo_x.move(i+90)  # x står i 90 grad
    servo_y.move(i+119)  # y står i 90 grad
    print(i)
    time.sleep(0.5)
