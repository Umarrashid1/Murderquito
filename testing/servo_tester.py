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
servo_x = Servo("x", io)
servo_y = Servo("y", io)
while True:
    try:
        x_val = int(input("Enter a value for servo_x to move: "))
        y_val = int(input("Enter a value for servo_y to move: "))
        
        servo_x.move(x_val)
        servo_y.move(y_val)
    except ValueError:
        print("Please enter a valid integer.")
    except KeyboardInterrupt:
        print("Exiting...")
        break