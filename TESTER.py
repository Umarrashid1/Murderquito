from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

factory = PiGPIOFactory()
joint_base = AngularServo(14, min_angle=-90, max_angle=90, pin_factory=factory)
angle_base = 0
while True:
    angle = int(input("Angle: "))

    angle_base = angle
    joint_base.angle = angle_base

    print(angle, angle_base)from gpiozero import AngularServo
from time import sleep

joint_base = AngularServo(14, min_angle=-90, max_angle=90)
joint_top = AngularServo(15, min_angle=-90, max_angle=90)
angle_base = 0
angle_top = 0
while True:
    angle = int(input())
  
    angle_base = angle
    joint_base.angle = angle_base

    angle_top = 90-angle_base
    joint_top.angle = angle_top

    print(angle, angle_base, angle_top)
