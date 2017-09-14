import numpy as np
import random
import cv2


from WebcamVideoStream import WebcamVideoStream
from show_video import show_video
from preprocess import l_select
from detection import find_contours, circle_check, group_circle

from parameters import *


def callback(x):
    pass


if __name__ == '__main__':
    # Initializing camera
    camera = WebcamVideoStream(src=VIDEO_SOURCE_INPUT).start()

    # Adding trackbars
    cv2.namedWindow("Trackbars")
    # cv2.createTrackbar("H_low", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("H_high", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("S_low", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("S_high", "Trackbars", 0, 255, callback)
    cv2.createTrackbar("L_low", "Trackbars", 190, 255, callback)
    cv2.createTrackbar("L_high", "Trackbars", 255, 255, callback)

    # Continuously reading from the camera until break
    while True:
        # Reading frame from camera
        frame = camera.read()

        # Processing the frame
        l_selected = l_select(frame, show=True)
        contours = find_contours(l_selected, frame, points=MIN_CONTOUR_POINTS, show=True)
        circles_details = circle_check(contours, frame, round_check=ROUND_CHECK, show=True, verbose=False)
        grouped_circles_image = np.copy(frame)

        # If circle(s) found, group circles
        if len(circles_details) > 0:
            groups = group_circle(circles_details, tolerance=GROUPING_DISTANCE, verbose=False)
            centers = list(groups.keys())
            for center in groups:
                color = (center[0], center[1], random.randint(0, 255))
                cv2.drawContours(grouped_circles_image, groups[center], -1, color, 3)

            show_video(grouped_circles_image, WIN4)

        # Waiting for exit key
        key = cv2.waitKey(1)
        if (key & 0xFF == ord('q')) | (key & 0xFF == 27):
            break

    camera.stop()
    cv2.destroyAllWindows()
