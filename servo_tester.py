import time
import io
from servo import Servo


def main():
    servo_x = Servo("x")
    servo_x.move(180)
    servo_x.stop()
