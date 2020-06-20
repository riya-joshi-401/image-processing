import cv2
import numpy as np 

imgg=cv2.imread('img.jpg')
img=cv2.resize(imgg,(600,600))
image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel=np.ones((2,2))
gaussian_blur=cv2.GaussianBlur(image,(5,5),2)
edge=cv2.Canny(gaussian_blur,150,200)
contours,heirarchy=cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
areas=[cv2.contourArea(i) for i in contours]
max_index=np.argmax(areas)
max_contour=contours[max_index]

perimeter=cv2.arcLength(max_contour,True)
ROI=cv2.approxPolyDP(max_contour,0.01*perimeter,True)
cv2.drawContours(img,[ROI],-1,(0,255,0),2)

p1=np.array([ROI[0],ROI[1],ROI[3],ROI[2]],np.float32)  # points set1
p2=np.array([(0,0),(500,0),(0,500),(500,500)],np.float32) # points set2
perspective=cv2.getPerspectiveTransform(p1,p2)
warpped=cv2.warpPerspective(img,perspective,(500,500))

cv2.imshow('img',img)
cv2.imshow('warpped',warpped)
cv2.waitKey(0)