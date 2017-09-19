import math
import numpy as np
import pickle

import cv2


def perspective_transform_calc():
    file_path = "persp.jpg"
    img = cv2.imread(file_path)
    img_w = img.shape[1]
    img_h = img.shape[0]

    src = np.float32((
        [0, 0],
        [img_w, 0],
        [img_w, img_h],
        [0, img_h]
    ))

    # TODO proper offset value calculation
    offset = 200
    dst = np.float32((
        [0, 0],
        [img_w, 0],
        [img_w, img_h+offset],
        [0, img_h+offset]
    ))

    transform_matrix = cv2.getPerspectiveTransform(src, dst)
    transform_matrix_inv = cv2.getPerspectiveTransform(dst, src)

    m_values = {
        "M": transform_matrix,
        "M_inv": transform_matrix_inv
    }

    pickle.dump(m_values, open("perspective_transform.p", "wb"))
    print("Perspective transform ")
    return m_values, offset


def root_mean_squared_error(calculated_values, actual_values):
    """
    Calculates the root mean squared error of the values.

    :param calculated_values: list of calculated ratios
    :param actual_values: list of actual ratios
    :return: returns the mean squared error of the list
    """

    # assert len(calculated_values) == len(actual_values)
    total = 0
    for i in range(len(calculated_values)):
        error = calculated_values[i]-actual_values[i]
        total += error*error

    return (total/len(calculated_values)) ** .5


if __name__ == '__main__':
    perspective_transform, offset = perspective_transform_calc()
    M = perspective_transform['M']
    img = cv2.imread('persp.jpg')
    # print(img[:, :, :])
    # img[:100, :100, :] = 255
    transformed = cv2.warpPerspective(img, M, (img.shape[1]+offset, img.shape[0]+offset),
                                      flags=cv2.INTER_LINEAR)
    cv2.imshow("Original", img)
    cv2.imshow("transformed", transformed)
    cv2.waitKey(0)
