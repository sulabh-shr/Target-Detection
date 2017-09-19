VIDEO_SOURCE_INPUT = 1
WIN_TRACK_BAR = "Track Bars"
WIN1 = 'L Thresholded'
WIN2 = 'Points Filtered Contours'
WIN3 = 'Circle Contours'
WIN4 = 'Grouped Circles'
WIN_Y = 325
WIN_X = WIN_Y * 4 // 3
POS_X_OFFSET = int(WIN_X * 0.1)
POS_Y_OFFSET = 80
MIN_CONTOUR_POINTS = 25
ROUND_CHECK = 0.75
GROUPING_DISTANCE = 20

l_thresh = [190, 255]

RADII = [100, 150, 225, 350, 400, 575, 675]
RATIOS = []
for r in RADII[1:]:
    RATIOS.append(r/RADII[0])
MINIMUM_CIRCLES = 4         # Target should have at least this number of circles
MAXIMUM_CIRCLES = 7         # Target having circle greater than this value is rejected
CENTER_TOLERANCE = 2     # Tolerance of ratios
