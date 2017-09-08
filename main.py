import math
import sys

import cv2
import numpy as np


cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cannot acces device")
    sys.exit()

win1 = 'L'
win2 = 'Filtered Contours'
win3 = 'Circle Contours'
win_y = 300
win_x = win_y*4//3
pos_xoffset = int(win_x*0.3)
pos_yoffset = 50
l_thresh = [190, 255]
round_check = 0.82


def show_video(frame, name, x_size=712, y_size=400, pos_x=None, pos_y=None):
    """
    It is used to create and display a window for a particular frame.

    :param frame: image to display
    :param name: name of the window
    :param x_size: width of window
    :param y_size: height of the window
    :param pos_x: window starting x pos
    :param pos_y: window starting y pos
    """
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, x_size, y_size)
    if pos_x is not None:
        cv2.moveWindow(win2, x=pos_x, y=pos_y)
    cv2.imshow(name, frame)


def l_select(img, show=False):
    """
    :param img: input image to check the l value
    :param show: flag to display the window or not
    :return: None
    """

    # Adding trackbar
    cv2.namedWindow("Trackbars")
    # cv2.createTrackbar("H_low", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("H_high", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("S_low", "Trackbars", 0, 255, callback)
    # cv2.createTrackbar("S_high", "Trackbars", 0, 255, callback)
    cv2.createTrackbar("L_low", "Trackbars", 190, 255, callback)
    cv2.createTrackbar("L_high", "Trackbars", 255, 255, callback)

    l_thresh[0] = cv2.getTrackbarPos("L_low", "Trackbars")
    l_thresh[1] = cv2.getTrackbarPos("L_high", "Trackbars")

    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    l = hls[:, :, 1]
    l_selected = np.zeros_like(l)  # all pixels 0
    l_selected[(l > l_thresh[0]) & (l <= l_thresh[1])] = 255  # selected pixels 1

    if show:
        show_video(l_selected, win1, win_x, win_y)
        # show_video(l_selected, win1, win_x, win_y, 0, 0)

    return l_selected


def find_contours(img, frame, show=False):
    """

    :param img: processed input image
    :param frame: original frame
    :param show: flag to display the window or not
    :return: list of contours
    """
    im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered = []
    for i in range(len(contours)):
        if len(contours[i]) > 50:
            filtered.append(contours[i])

    if show:
        frame_copy = np.copy(frame)
        cv2.drawContours(frame_copy, filtered, -1, (0, 0, 255), 3)
        show_video(frame_copy, win2, win_x, win_y)
        # show_video(frame_copy, win2, win_x, win_y, pos_x=win_x+pos_xoffset, pos_y=0)

    return filtered


def callback(x):
    pass


if __name__ == '__main__':
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Cannot read Frame.")
            sys.exit()

        l_selected = l_select(frame, show=True)
        contours = find_contours(l_selected, frame, show=True)
        # find_contours(l_selected, frame, show=True)
        Contours = []
        circles = []

        for c in contours:
            area = cv2.contourArea(c)
            print('area', area)
            length = cv2.arcLength(c, closed=True)
            print('length', length)
            roundness = 4*math.pi*area/length**2
            print('roundness', roundness)
            if roundness >= round_check:
                print('true')
                contour = {
                    'c': c,
                    'area': area,
                    'roundness': roundness
                }
                Contours.append(contour)
                circles.append(c)
            else:
                print('false')

        circle_image = np.copy(frame)
        cv2.drawContours(circle_image, circles, -1, (0, 0, 255), 3)
        show_video(circle_image, win3, win_x, win_y)
        # show_video(circle_image, win3, win_x, win_y, pos_x=win_x+pos_xoffset, pos_y=win_y
        # +pos_yoffset)
        key = cv2.waitKey(1)
        if (key & 0xFF == ord('q')) | (key & 0xFF == 27):
            break

    cap.release()
    cv2.destroyAllWindows()
