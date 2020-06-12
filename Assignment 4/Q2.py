import cv2
import numpy as np 

img = cv2.imread('n2.jpg')
image=img.copy()
pts=[]
def mouse(event,x,y,flags,param):
    if event== cv2.EVENT_LBUTTONDOWN:
        pts.append((x,y))

    if len(pts)==2:
        img1=image[pts[0][1]:pts[1][1],pts[0][0]:pts[1][0]]
        cv2.imshow("Cropped img",img1)
        
cv2.namedWindow('img')
cv2.setMouseCallback('img',mouse)
cv2.imshow('Original img',img)
cv2.waitKey(0)