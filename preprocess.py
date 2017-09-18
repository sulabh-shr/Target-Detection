import cv2
import numpy as np
from show_video import show_video
from parameters import *


def l_select(img, show=False):
    """
    It is used to threshold the l channel of image
    with the threshold value input from the track bar

    :param img: input image to check the l value
    :param show: flag to display the window or not
    :return: image with thresholded value of l channel
    """

    # Getting minimum and maximum threshold values from track bars
    l_thresh[0] = cv2.getTrackbarPos("L_low", WIN_TRACK_BAR)
    l_thresh[1] = cv2.getTrackbarPos("L_high", WIN_TRACK_BAR)

    # Converting to HLS space
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # Selecting L channel
    l = hls[:, :, 1]

    # Thresholding on the L channel
    l_selected = np.zeros_like(l)  # all pixels 0
    l_selected[(l > l_thresh[0]) & (l <= l_thresh[1])] = 255  # selected pixels 255

    if show:
        show_video(l_selected, 'L Thresholded', WIN_X, WIN_Y, WIN_X+POS_X_OFFSET, 0)

    return l_selected
