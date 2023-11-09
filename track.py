import cv2
import numpy as np

# Specifying the color that we want to detect
lower = np.array([30, 100, 20])
upper = np.array([90, 250, 255])

# Activating camera image - We will change this later, as we gonna use the camera class.
webcam_video = cv2.VideoCapture(1)

while True:
    # Read the camera footage
    success, video = webcam_video.read()

    # Converting the BGR image from webcam to HSV format
    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)

    # Creating a mask to find our color
    mask = cv2.inRange(img, lower, upper)

    # Finding contours in mask image
    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the position of the contour and draw a circle
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            # Defining the least amount of pixels, I want it to register.
            if cv2.contourArea(mask_contour) > 200:
                # Setting up the circle
                (x, y), radius = cv2.minEnclosingCircle(mask_contour)
                center = (int(x), int(y))
                radius = int(radius)
                # Creating the circle
                cv2.circle(video, center, radius, (0, 0, 255), 3)

    # Open a window and display the mask image
    cv2.imshow("Mask image", mask)

    # Open a window and display the webcam image
    cv2.imshow("Webcam Image", video)

    # Defining the delay pr frame.
    cv2.waitKey(1)
