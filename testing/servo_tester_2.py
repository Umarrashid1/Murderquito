import pigpio
io = pigpio.pi()
io.set_mode(12, pigpio.OUTPUT)


while True:
    try:
        dc = float(input("Enter a value for servo_x to move: "))
        io.hardware_PWM(12, 50, int(dc*10000))

    except ValueError:
        print("Please enter a valid integer.")
    except KeyboardInterrupt:
        print("Exiting...")
        break



