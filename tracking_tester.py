import cv2
import sys
import numpy as np
from detection import Detector

#tracker = cv2.legacy.TrackerKCF.create()
tracker = cv2.TrackerKCF.create()

frame_counter = 0

# Read video
video = cv2.VideoCapture(0)

# Exit if video not opened.
if not video.read():
    print("Could not open video")
    sys.exit()

# Read first frame.
ok, frame = video.read()

if not ok:
    print("Cannot read video file")
    sys.exit()

# Converting the BGR image from webcam to gray scale
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Thresh
thresh = cv2.threshold(gray_frame, 100, 1, cv2.THRESH_BINARY_INV)[1]

# Initialize tracker with first frame and bounding box
detection = Detector()
bbox = detection.find_circle(frame)
ok = tracker.init(frame, bbox)

while True:

    # Read a new frame
    ok, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Increment frame counter
    frame_counter += 1

    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box TODO: egen funktion?
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(gray_frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        # Tracking failure
        cv2.putText(gray_frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display FPS on frame
    cv2.putText(gray_frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

    # Display result
    cv2.imshow("Tracking", gray_frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
