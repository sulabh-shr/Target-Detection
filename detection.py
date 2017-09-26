import numpy as np
import cv2
import math
import random

from show_video import show_video
from parameters import *
from helper import root_mean_squared_error


def find_contours(img, frame, points=50, show=False):
    """
    It is used to find all contours in an image frame
    which have number of points more than specified minimum value

    :param img: processed input image
    :param frame: original frame
    :param points: minimum points to approve as required contour
    :param show: flag to display the window or not
    :return: list of contours with area greater than a specified value
    """

    # Finding all contours in the image
    im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filtering contours based on their minimum points
    filtered = []
    for i in range(len(contours)):
        if len(contours[i]) > points:
            filtered.append(contours[i])

    if show:
        frame_copy = np.copy(frame)
        cv2.drawContours(frame_copy, filtered, -1, (0, 0, 255), 1)
        show_video(frame_copy, 'Points Filtered Contours', WIN_X, WIN_Y, 2*(WIN_X+POS_X_OFFSET), 0)

    return filtered


def circle_check(contours, frame, round_check=0.82, show=False, verbose=False):
    """
    It is used to return only those contours which have
    roundness greater a minimum specified value

    :param contours: list of contours
    :param frame: original frame
    :param round_check: minimum roundness to certify as a circle
    :param show: flag to the video frame
    :param verbose: flag to print details to the console
    :return: list of contours certified as circles
    """

    if not verbose:
        circles_details = []        # list of dictionaries of circles with their properties
        circle_image = np.copy(frame)   # copy of main frame to draw contours on
        circles = []                # list of circles used to draw contours while showing

        # Checking roundness of each contour
        for c in contours:
            area = cv2.contourArea(c)
            length = cv2.arcLength(c, closed=True)
            roundness = 4 * math.pi * area / length ** 2

            if roundness >= round_check:
                moments = cv2.moments(c)
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])

                contour = {  # dictionary of a circle with its properties
                    'c': c,
                    'area': area,
                    'roundness': roundness,
                    'moments': moments,
                    'cx': cx,
                    'cy': cy
                }
                # Appending the found contour to the list of dictionaries and the list
                circles_details.append(contour)
                circles.append(c)
    else:
        circles_details = []  # list of dictionaries of circles with their properties
        circle_image = np.copy(frame)  # copy of main frame to draw contours on
        circles = []  # list of circles used to draw contours while showing

        # Checking roundness of each contour
        for c in contours:
            area = cv2.contourArea(c)
            length = cv2.arcLength(c, closed=True)
            roundness = 4 * math.pi * area / length ** 2
            print('\narea:', area)
            print('length:', length)
            print('roundness:', roundness)

            if roundness >= round_check:
                print('\n\tCircle found...')

                moments = cv2.moments(c)
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])

                print('moments:', moments)
                print('cx:', cx)
                print('cy:', cy)

                contour = {  # dictionary of a circle with its properties
                    'c': c,
                    'area': area,
                    'roundness': roundness,
                    'moments': moments,
                    'cx': cx,
                    'cy': cy
                }
                # Appending the found contour to the list of dictionaries and the list
                circles_details.append(contour)
                circles.append(c)

    if show:
        cv2.drawContours(circle_image, circles, -1, (0, 0, 255), 3)
        show_video(circle_image, 'All Found circles', WIN_X, WIN_Y, 2* (WIN_X + POS_X_OFFSET), WIN_Y+POS_Y_OFFSET)

    return circles_details


def group_circle(circles_details, frame, tolerance=20, show=False, verbose=False):
    """
    It is used to group circles which have centers within the tolerance limit.

    :param circles_details: list of dictionaries of circles found
    :param frame: original frame
    :param tolerance: max distance in pixel value within which circles are said to have same center
    :param show: flag to show the frame
    :param verbose: flag to print details to the console
    :return:
    """

    """
        The variable groups is a dictionary with key as center of the group (x, y) 
        and value as list of the contours having that same center.
        It is used to draw contours when show flag is set.

        The variable groups_details is a dictionary with key as center (x, y) and
        value as list of dictionaries of the contours having that same center.
        The dictionary of each contour contains its various properties as well.
    """
    if not verbose:
        # Initializing the groups dictionary with 1st circle in the circle_details list
        groups = {
            (circles_details[0]['cx'], circles_details[0]['cy']): [circles_details[0]['c']]
        }
        groups_details = {
            (circles_details[0]['cx'], circles_details[0]['cy']): [circles_details[0]]
        }

        # Iterating over each circle of the frame
        for contour in circles_details[1:]:
            # Matching a circle's center in already found centers (keys)
            found = False  # Value set True after common center found
            found_key = None  # Value of the center matched
            for key in groups:
                if abs(contour['cx'] - key[0]) <= tolerance and abs(contour['cy'] - key[1]) <= tolerance:
                    found = True
                    found_key = key
                    break

            if found:
                # Append to the matched key i.e. matched center
                groups[found_key].append(contour['c'])
                groups_details[found_key].append(contour)
            else:
                # Create a new key with the unmatched center
                groups[(contour['cx'], contour['cy'])] = [contour['c']]
                groups_details[(contour['cx'], contour['cy'])] = [contour]
    else:
        print('\nINSIDE GROUP CIRCLE................')
        # Initializing the groups dictionary with 1st circle in the circle_details list
        groups = {
            (circles_details[0]['cx'], circles_details[0]['cy']): [circles_details[0]['c']]
        }
        groups_details = {
            (circles_details[0]['cx'], circles_details[0]['cy']): [circles_details[0]]
        }

        # Iterating over each circle of the frame
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
                # Append to the matched key i.e. matched center
                groups[found_key].append(contour['c'])
                groups_details[found_key].append(contour)
            else:
                # Create a new key with the unmatched center
                groups[(contour['cx'], contour['cy'])] = [contour['c']]
                groups_details[(contour['cx'], contour['cy'])] = [contour]

        print('\nNumber of circle groups found:', len(groups))
        for key in groups:
            print('Center:', key, '\n\tn_circles:', len(groups[key]))

    if show:
        grouped_circles_image = np.copy(frame)
        for center in groups:
            color = (center[0], center[1], random.randint(0, 255))
            cv2.drawContours(grouped_circles_image, groups[center], -1, color, 3)
        show_video(grouped_circles_image, 'Grouped Circles',
                   WIN_X, WIN_Y, WIN_X+POS_X_OFFSET, WIN_Y+POS_Y_OFFSET)

    return groups_details


def find_target(groups_details, frame, min_circles, max_circles, target_ratios,
                show=False):
    """
    It is used to find the exact target based on ratio of radius of contours

    :param groups_details: a list of dictionary of contours and it's various details
    :param target_ratios: the ratio to search for
    :param show: flag to show the frame
    :return:
    """

    targets = []
    best_target = None

    # Iterating over each group of contours in the list
    for center in groups_details:
        detected = True     # Flag that is set false if ratio don't match
        current_details = groups_details[center]        # List of dictionary of contours of iterating group

        # Checking if number of circles is greater than predefined value
        print("Number of circles in group: ", len(current_details))
        # print(current_details)
        if min_circles <= len(current_details) <= max_circles:
            # TODO Proper ratio comparision
            # Sorting the contours based on the increasing order of their area
            sorted_details = sorted(current_details, key=lambda k: k['area'])
            ratios = []     # List to add the ratios

            # Calculating the ratios of radii wrt inner most circle
            for contour in sorted_details[1:]:
                ratios.append((contour['area']/sorted_details[0]['area'])**(1/2))

            # print("Found ratio: ", ratios)
            # Checking the ratio against pre-defined target RATIO
            for index in range(len(ratios)):
                if abs(ratios[index] - target_ratios[index]) > CENTER_TOLERANCE:
                    detected = False
                    print("Not a target\n")
                    break

            if detected:
                print("Detected\n")
                target = {'details': groups_details[center],
                          'ratios': ratios}
                # targets.append(groups_details[center])
                targets.append(target)
                best_target = targets[0]

    if len(targets) > 1:
        # TODO detecting false groups too, need to check tolerance
        rmse = []
        for target in targets:
            ratios = target['ratios']
            rmse.append(root_mean_squared_error(ratios, target_ratios))

        # print("Found multiple targets: ", len(targets), 'RMSE: ', len(rmse))
        sorted_rmse = [i[0] for i in sorted(enumerate(rmse), key=lambda x: x[1])]
        # print(rmse, sorted_rmse)
        # print(targets[sorted_rmse[0]]['details'][0]['area'])
        best_target = targets[sorted_rmse[0]]

    if show:
        if best_target:
            best_platform = np.copy(frame)
            for contour in best_target['details']:
                cv2.drawContours(best_platform, contour['c'], -1, (255, 0, 0), 3)
            show_video(best_platform, 'Best Platform', WIN_X, WIN_Y, 0, (WIN_Y+POS_Y_OFFSET))

    print(".......")
    return best_target
