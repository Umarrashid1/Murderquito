import cv2
import sys
import numpy

tracker = cv2.legacy.TrackerKCF.create()


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


#__________________________________________________________________________________

# Converting the BGR image from webcam to gray scale
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Thresh
thresh = cv2.threshold(gray_frame, 100, 1, cv2.THRESH_BINARY_INV)[1]

# Creating a mask to find our color
# mask = cv2.inRange(img, lower, upper)

# Finding contours in mask image
mask_contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Define an initial bounding box
bbox = (287, 23, 86, 320)

# Find the position of the contour and draw a rectangle
if len(mask_contours) != 0:
    for mask_contour in mask_contours:
        # Defining the least amount of pixels, I want it to register.
        if cv2.contourArea(mask_contour) > 100:
            # Get bounding box for the contour
            x, y, w, h = cv2.boundingRect(mask_contour)

            # Set bbox with the correct format
            bbox = (x, y, w, h)

            # Draw rectangle
            cv2.rectangle(gray_frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

            # Show coordinates for the top-left corner of the bounding box
            cv2.putText(gray_frame, f'({x},{y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.circle(gray_frame, (x + w // 2, y + h // 2), 3, (0, 255, 255), -1)


#__________________________________________________________________________________________

# Uncomment the line below to select a different bounding box
#bbox = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)

while True:
    # Read a new frame
    ok, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not ok:
        break

    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(gray_frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        # Tracking failure
        cv2.putText(gray_frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display tracker type on frame
    #cv2.putText(frame,"Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

    # Display FPS on frame
    cv2.putText(gray_frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

    # Display result
    cv2.imshow("Tracking", gray_frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
