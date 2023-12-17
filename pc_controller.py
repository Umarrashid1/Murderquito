import cv2
import sys
import time
from camera import Camera
from detection import Detector

# Get CLI arguments
args = sys.argv[1:]
if len(args) > 0:
    input_param = int(args[0])
else:
    input_param = None

cam = Camera(input_param)
det = Detector(cam)

frame_counter = 0


def get_frame_counter():
    return frame_counter


start_time = time.time()
fps = 0

while True:
    frame_counter += 1

    frame = cam.run()
    det.update_tracker(cam)
    det.draw_cross(cam)
    det.draw_boundingbox(cam, fps)

    # Calculate FPS every 10 frames

    end_time = time.time()
    elapsed_time = end_time - start_time
    fps = round(frame_counter / elapsed_time)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
