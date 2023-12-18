import cv2
import numpy as np
from camera import Camera


class Detector:
    bbox = None
    tracker = None
    ok = False
    TRACKER_TYPE = "TrackerCSRT"
    tracking_fail_counter = 0
    dupli_count = 0
    fail_array = []

    def __init__(self, cam):
        frame = cam.get_frame()
        Tracker = getattr(cv2, self.TRACKER_TYPE)
        self.tracker = Tracker.create()
        self.bbox = self.find_circle(cam)
        self.init_tracker(cam)
        self.bg_frame = cam.get_frame()

        

    def init_tracker(self, cam):
        frame = cam.get_frame()

        if frame is not None and self.bbox is not False and not all(i == 0 for i in self.bbox):
            try:
                self.tracker.init(frame, self.bbox)
            except cv2.error as e:
                print(f"Error during tracker initialization: {e}")
                self.bbox = self.find_circle(cam)

    def update_tracker(self, cam, frame_counter):
        self.bbox_old = self.bbox
        if self.bbox is not False and not all(i == 0 for i in self.bbox):
            frame = cam.get_frame()
            try:
                self.ok, self.bbox = self.tracker.update(frame)
                if not self.ok:
                    # Object is lost, fall back to find_circle
                    self.bbox = self.find_circle(cam)
                    Tracker = getattr(cv2, self.TRACKER_TYPE)
                    self.tracker = Tracker.create()
                    self.init_tracker(cam)
            except cv2.error as e:
                print(f"Error during tracker update: {e}")
                self.bbox = self.find_circle(cam)
                Tracker = getattr(cv2, self.TRACKER_TYPE)
                self.tracker = Tracker.create()
                self.init_tracker(cam)
        else:
            # Handle the case where self.bbox is False or all elements are 0
            self.bbox = self.find_circle(cam)
            Tracker = getattr(cv2, self.TRACKER_TYPE)
            self.tracker = Tracker.create()

            self.init_tracker(cam)
        self.detect_fail(cam, frame_counter)

    def draw_boundingbox(self, cam):
        frame_boundingbox = cam.get_frame()
        if self.bbox is not False:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(frame_boundingbox, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame_boundingbox, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (0, 0, 255), 2)
            self.tracking_fail_counter = self.tracking_fail_counter + 1
        # Add FPS text to the frame
        
        # Display the frame
        cv2.imshow("Tracking", frame_boundingbox)

    def get_center_coordinates(self):
        if self.bbox is not False:
            x, y, w, h = self.bbox
            center_x = x + w / 2
            center_y = y + h / 2
            return center_x, center_y
        else:
            return 0, 0

    def draw_cross(self, cam):
        center_x, center_y = self.get_center_coordinates()
        frame = cam.get_frame()

        # Draw horizontal line
        cv2.line(frame, (int(center_x - 10), int(center_y)), (int(center_x + 10), int(center_y)), (0, 255, 0), 2)

        # Draw vertical line
        cv2.line(frame, (int(center_x), int(center_y - 10)), (int(center_x), int(center_y + 10)), (0, 255, 0), 2)

    def find_circle(self, cam):
        # Convert the image to grayscale
        gray = cam.get_gray_frame()

        # Apply GaussianBlur to reduce noise and help the circle Detector
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,  # 1 means the accumulator has the same resolution as the input image
            minDist=30,  # Minimum distance between the centers of detected circles
            param1=65,  # Higher value means less sensitive edge Detector
            param2=65,  # Higher value allows Detector with lower confidence
            minRadius=5,  # Minimum radius of detected circles
            maxRadius=400  # Maximum radius of detected circles
        )

        if circles is not None:
            # Convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # Return the bounding box of the first detected circle
            x, y, radius = circles[0]
            bbox = (x - radius, y - radius, 2 * radius, 2 * radius)
            return bbox

        # Return False if no circle is found
        return False

    def find_red (self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray_bg = cv2.cvtColor(self.bg_frame, cv2.COLOR_RGB2GRAY)
        sub = cv2.subtract(gray_frame, gray_bg)
        cv2.imwrite("sub.jpg", sub)
        thresh = cv2.threshold(sub, 30, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite("sub22.jpg", thresh)

        mask_contour, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(sub, mask_contour, -1, (0,255,0), 3)
        cv2.imwrite("cuntjjjjj.jpg", sub)
        # Specify the minimum and maximum mass thresholds
        min_mass_threshold = 4
        max_mass_threshold = 200
        
        for contour in mask_contour:
            # Calculate the moments of the contour
            mass = cv2.moments(contour)

            # Check if the mass is within the specified range
            if min_mass_threshold < mass["m00"] < max_mass_threshold:
                # Calculate the center of mass of the contour
                cx = int(mass["m10"] / mass["m00"])
                cy = int(mass["m01"] / mass["m00"])

                # Draw bounding box around the contour
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display mass and center of mass
                cv2.putText(frame, f'Mass: {mass["m00"]}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame, f'Center: ({cx}, {cy})', (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                print(cx, cy)
                return (int(cx), int(cy))
            else:
                print("no red dot found")
                return False

  
    def find_person(self, cam):
        bounding_boxes = []
        person_detector = cv2.CascadeClassifier("data_cascade/haarcascade_frontalface_default.xml")

        # Assuming cam.get_gray_frame() returns the current gray frame from the camera
        gray_frame = cam.get_gray_frame()

        persons = person_detector.detectMultiScale(
            gray_frame, scaleFactor=1.05, minNeighbors=5,
            minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in persons:
            bounding_boxes.append((x, y, x + w, y + h))

        # Draw bounding boxes on the original frame
        self.draw_bounding_boxes(cam.get_frame(), bounding_boxes)

    def draw_bounding_boxes(self, frame, bounding_boxes):
        for (x1, y1, x2, y2) in bounding_boxes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)



    def detect_fail(self, cam, frame_counter):
        if self.bbox == self.bbox_old:
            self.dupli_count += 1
        if self.dupli_count == 5:
            self.fail_array.append([frame_counter, "failed"])
            self.bbox = self.find_circle(cam)
            self.tracker = cv2.TrackerKCF.create()
            self.init_tracker(cam)
            
