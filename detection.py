

def group_circle(contours_details, tolerance=20):
    groups = {
        (contours_details[0]['cx'], contours_details[0]['cy']): [contours_details[0]['c']]
    }

    for contour in contours_details[1:]:
        # moments = cv2.moments(contour.c)
        # cx = int(moments['m10'] / moments['m00'])
        # cy = int(moments['m01'] / moments['m00'])
        #
        # # print('moments:', moments)
        # print('cx:', cx)
        # print('cy:', cy)
        #
        # contour['moments'] = moments
        # contour['cx'] = cx
        # contour['cy'] = cy
        for key in groups:
            if abs(contour['cx'] - key[0]) <= tolerance and abs(contour['cy'] - key[1]) <= tolerance:
                groups[key].append(contour['c'])
            else:
                groups[(contour['cx'], contour['cy'])] = [contour['c']]
                break

    print(groups.keys())
    return groups


def find_target(contours_details, ratio):
    """
    It is used to find the exact target based on ratio of radius of contours

    :param contours_details: a list of dictionary of contours and it's various details
    :param ratio: the ratio to search for
    :return:
    """
    sorted_details = sorted(contours_details, key=lambda k: k['area'])
    for c in sorted_details:
        pass


if __name__ == 'main':
    pass