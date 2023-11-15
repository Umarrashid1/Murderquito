class Object:

    def __init__(self):


def track_faces(self, gray_scale, img, video):

    # Detection of face file
    face_file_path = "data_cascade/haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(face_file_path)

    while True:
        # Recognize a face
        faces = cascade.detectMultiScale(gray_scale, 1.2, 3)

        for x, y, w, h in faces:
            cv2.rectangle(video, (x, y), (x + w, y + h), (255, 0, 0), 2)


def find_black_dot(self, thresh, img, video):

    # Find the position of the contour and draw a circle
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            # Defining the least amount of pixels, I want it to register.
            if cv2.contourArea(mask_contour) > 100:
                # Setting up the circle
                (x, y), radius = cv2.minEnclosingCircle(mask_contour)
                center = (int(x), int(y))
                radius = int(radius)

                # Creating the circle
                cv2.circle(video, center, radius, (0, 0, 255), 3)

                # Show coordinates for the center of the black object
                cv2.putText(video, f'({x},{y})', center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.circle(video, center, 3, (0, 255, 255), -1)
