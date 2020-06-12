'''Get the warped image using four mouse clicks'''

import cv2
import numpy as np

img = cv2.imread('n2.jpg')

clicks = np.zeros(shape = (4, 2), dtype = np.float32)  # storing coordinates of 4 mouse clicks
index = 0

def mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global index
        global clicks

        if (index < 4):
            clicks[index] = [x, y]
            index += 1

            if np.all (clicks):   # when all four clicks captured/stored then call wrap function
                warpImage()
                print(clicks)
        else:
            pass

def warpImage ():
    global clicks

     #  clicks in order top left , top right , bottom left , bottom right


    tl,tr,bl,br = clicks[0] , clicks[1] , clicks[2] , clicks[3]         
    
    warpedPoints = np.array ([(0, 0), (500, 0), (0, 500), (500, 500)], dtype = np.float32)

    perspective = cv2.getPerspectiveTransform(clicks, warpedPoints)
    warped = cv2.warpPerspective(img, perspective, (500, 500))

    cv2.imshow ('warped image', warped)

cv2.namedWindow ('orginal image')
cv2.setMouseCallback ('orginal image', mouse)
cv2.imshow ('orginal image', img)

cv2.waitKey(0)