import cv2


def find_linear_ratio(cam):
    linear_ratio = None

    while linear_ratio is None:
        frame = cam.run()
        # Assuming 'img' is your image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, threshhold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(threshhold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            actual_area = cv2.contourArea(contour)
            pred_area = w * h
            # DET HER MATEMATIK SKAL FORKLARES I RAPPORT

            if abs(h - w) < 20 and abs(actual_area - pred_area) < 0.1 * pred_area:
                targetblob = contour
                x, y, w, h = cv2.boundingRect(targetblob)
                linear_ratio = 107.4 / h
                print(linear_ratio)

                return linear_ratio
