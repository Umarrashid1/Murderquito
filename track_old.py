from Bounding_Boxes_subclasses.rectangle import Rectangle
from Bounding_Boxes_subclasses.circle import Circle
import cv2


# Specifying the color that we want to detect
# lower = np.array([30, 100, 20])
# upper = np.array([90, 250, 255])

# Detection of face file
face_file_path = "data_cascade/haarcascade_frontalface_default.xml"

cascade = cv2.CascadeClassifier(face_file_path)

# Activating camera image - We will change this later to the camera class.
webcam_video = cv2.VideoCapture(0)

while True:
    # Read the camera footage
    success, video = webcam_video.read()

    # Converting the BGR image from webcam to HSV format
    img = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

    # Converting the BGR image from webcam to gray scale
    gray_scale = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

    # Thresh
    thresh = cv2.threshold(gray_scale, 100, 1, cv2.THRESH_BINARY_INV)[1]

    # Creating a mask to find our color
    # mask = cv2.inRange(img, lower, upper)

    # Finding contours in mask image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Recognize a face
    faces = cascade.detectMultiScale(gray_scale, 1.2, 3)

    bounding_boxes = []

    circle_obj = Circle.from_contours(contours)
    if circle_obj is not None:
        bounding_boxes.append(circle_obj)

    for (x, y, w, h) in faces:
        rectangle_obj = Rectangle(x, y, w, h)
        bounding_boxes.append(rectangle_obj)

    for box in bounding_boxes:
        box.display(video)

    # Open a window and display the mask image
    cv2.imshow("Mask image", img)

    # Open a window and display the webcam image
    cv2.imshow("Webcam Image", video)

    # Defining the delay pr frame.
    cv2.waitKey(1)
