import cv2
import numpy as np
from show_video import show_video
from parameters import *


def hls_select(img, key='HLS', show=False):
    """
    It is used to threshold the channels of image
    with the threshold value input from the track bar

    :param img: input image to check the l value
    :param key: choose the channel to change.
    :param show: flag to display the window or not
    :return: image with thresholded value of l channel
    """

    # Converting to HLS space
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # Getting minimum and maximum threshold values from track bars
    if key == 'HLS':
        H_thresh[0] = cv2.getTrackbarPos("H_low", WIN_TRACK_BAR)
        H_thresh[1] = cv2.getTrackbarPos("H_high", WIN_TRACK_BAR)
        L_thresh[0] = cv2.getTrackbarPos("L_low", WIN_TRACK_BAR)
        L_thresh[1] = cv2.getTrackbarPos("L_high", WIN_TRACK_BAR)
        S_thresh[0] = cv2.getTrackbarPos("S_low", WIN_TRACK_BAR)
        S_thresh[1] = cv2.getTrackbarPos("S_high", WIN_TRACK_BAR)

        channel_process_img = np.zeros_like(hls[:, :, 2])
        channel_values = []
        for index, channel in enumerate('HLS'):
            thresh_low = cv2.getTrackbarPos(channel + '_low', WIN_TRACK_BAR)
            thresh_high = cv2.getTrackbarPos(channel + '_high', WIN_TRACK_BAR)
            channel_value = hls[:, :, index]
            channel_binary_img = np.zeros_like(channel_value)
            # channel_binary_img[(channel_value > (channel+'_thresh')[0])
            #                    & (channel_value <= (channel+'_thresh')[1])] = 255
            channel_binary_img[(channel_value > thresh_low) & (channel_value <= thresh_high)] = 255
            channel_values.append(channel_binary_img)

        channel_process_img[(channel_values[0] == 255)
                            & (channel_values[1] == 255)
                            & (channel_values[2] == 255)] = 255

    else:
        if key == 'H':
            channel = 0
        elif key == 'L':
            channel = 1
        elif key == 'S':
            channel = 2
        thresh_low = cv2.getTrackbarPos(key+'_low', WIN_TRACK_BAR)
        thresh_high = cv2.getTrackbarPos(key+'_high', WIN_TRACK_BAR)
        channel_value = hls[:, :, channel]
        channel_process_img = np.zeros_like(channel_value)
        channel_process_img[(channel_value > thresh_low) & (channel_value <= thresh_high)] = 255

        # l_thresh[0] = cv2.getTrackbarPos("L_low", WIN_TRACK_BAR)
        # l_thresh[1] = cv2.getTrackbarPos("L_high", WIN_TRACK_BAR)
        # l_value = hls[:, :, 1]
        # l_selected = np.zeros_like(l_value)  # all pixels 0
        # l_selected[(l_value > l_thresh[0]) & (l_value <= l_thresh[1])] = 255  #selected pixels 255

    if show:
        show_video(channel_process_img, key+' threshold', WIN_X, WIN_Y, WIN_X+POS_X_OFFSET, 0)

    return channel_process_img
