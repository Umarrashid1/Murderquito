class BondingBoxes:
    def __init__(self):
        x, y, w, h, radius, center, radius = 0

    def rectangle(self, object):
        for x, y, w, h in object:
            cv2.rectangle(video, (x, y), (x + w, y + h), (255, 0, 0), 2)

    def circle(self, x, y, mask_contour):
        # Setting up the circle
        (x, y), radius = cv2.minEnclosingCircle(mask_contour)
        center = (int(x), int(y))
        radius = int(radius)

        # Creating the circle
        cv2.circle(video, center, radius, (0, 0, 255), 3)

        # Show coordinates for the center of the black object
        cv2.putText(video, f'({x},{y})', center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.circle(video, center, 3, (0, 255, 255), -1)