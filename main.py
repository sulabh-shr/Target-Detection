import numpy as np
import cv2


from WebcamVideoStream import WebcamVideoStream
from preprocess import l_select
from detection import find_contours, circle_check, group_circle, find_target

from parameters import *


def callback(x):
    pass


if __name__ == '__main__':
    print(RATIOS)
    # Initializing camera
    camera = WebcamVideoStream(src=VIDEO_SOURCE_INPUT).start()

    # Adding trackbars
    cv2.namedWindow(WIN_TRACK_BAR, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WIN_TRACK_BAR, WIN_X, WIN_Y)
    # cv2.createTrackbar("H_low", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("H_high", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("S_low", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("S_high", "Trackbars", 0, 255, callback)
    cv2.createTrackbar("L_low", WIN_TRACK_BAR, 190, 255, callback)
    cv2.createTrackbar("L_high", WIN_TRACK_BAR, 255, 255, callback)

    # Continuously reading from the camera until break
    while True:
        # Reading frame from camera
        frame = camera.read()

        # Processing the frame
        l_selected = l_select(frame, show=True)
        contours = find_contours(l_selected, frame, points=MIN_CONTOUR_POINTS, show=True)
        circles_details = circle_check(contours, frame, round_check=ROUND_CHECK, show=True, verbose=False)
        grouped_circles_image = np.copy(frame)
        if len(circles_details) > 0:    # If circle(s) found, group circles
            groups_details = group_circle(circles_details, frame, tolerance=GROUPING_DISTANCE, show=True, verbose=False)
            find_target(groups_details, min_circles=MINIMUM_CIRCLES, max_circles=MAXIMUM_CIRCLES, target_ratios=RATIOS)

        # Waiting for exit key
        key = cv2.waitKey(1)
        if (key & 0xFF == ord('q')) | (key & 0xFF == 27):
            break

    camera.stop()
    cv2.destroyAllWindows()
