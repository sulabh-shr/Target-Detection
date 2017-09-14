import numpy as np
import cv2
import math


def circle_check(contours, frame, round_check=0.82, show=False, verbose=False):
    grouped_circles_image = np.copy(frame)
    circles_details = []
    circles = []

    for c in contours:
        area = cv2.contourArea(c)
        length = cv2.arcLength(c, closed=True)
        roundness = 4 * math.pi * area / length ** 2
        # print('\narea:', area)
        # print('length:', length)
        # print('roundness:', roundness)

        if roundness >= round_check:
            # print('\n\tCircle found...')

            moments = cv2.moments(c)
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])

            # print('moments:', moments)
            # print('cx:', cx)
            # print('cy:', cy)

            contour = {  # dictionary of a contour with property
                'c': c,
                'area': area,
                'roundness': roundness,
                'moments': moments,
                'cx': cx,
                'cy': cy
            }
            circles_details.append(contour)  # array of dictionaries of contours with properties
            circles.append(c)  # array of contours for drawing

    return circles_details, circles


def group_circle(circles_details, tolerance=20, verbose=False):
    if not verbose:
        groups = {(circles_details[0]['cx'], circles_details[0]['cy']): [circles_details[0]['c']]}

        # Iterating over each circle of the frame
        for contour in circles_details[1:]:
            # Matching a circle's center in already found centers (keys)
            found = False  # value set True after common center found
            found_key = None  # value of the center matched
            for key in groups:
                if abs(contour['cx'] - key[0]) <= tolerance and abs(contour['cy'] - key[1]) <= tolerance:
                    found = True
                    found_key = key
                    break

            if found:
                groups[found_key].append(contour['c'])
            else:
                groups[(contour['cx'], contour['cy'])] = [contour['c']]
    else:
        print('\nINSIDE GROUP CIRCLE................')
        groups = {
            (circles_details[0]['cx'], circles_details[0]['cy']): [circles_details[0]['c']]
        }

        for contour in circles_details[1:]:
            # Match the center in already found centers (keys)
            print('Matching center:', contour['cx'], contour['cy'])
            found = False  # value set True after common center found
            found_key = None  # value of the center matched
            for key in groups:
                print('\tagainst', key)
                if abs(contour['cx'] - key[0]) <= tolerance and abs(contour['cy'] - key[1]) <= tolerance:
                    found = True
                    found_key = key
                    print('Found')
                    break
                else:
                    print('Not found, adding the key')

            if found:
                groups[found_key].append(contour['c'])
            else:
                groups[(contour['cx'], contour['cy'])] = [contour['c']]

        print('\nNumber of circle groups found:', len(groups))
        for key in groups:
            print('Center:', key, '\n\tn_circles:', len(groups[key]))

    return groups


def find_target(circles_details, ratio):
    """
    It is used to find the exact target based on ratio of radius of contours

    :param circles_details: a list of dictionary of contours and it's various details
    :param ratio: the ratio to search for
    :return:
    """
    sorted_details = sorted(circles_details, key=lambda k: k['area'])
    for c in sorted_details:
        pass


if __name__ == 'main':
    pass