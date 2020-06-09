import cv2 
import random
  

img = cv2.imread('n2.jpg')
shape = img.shape
height = shape[0] / 7
width = shape[1] / 7

 
for i in range(1, 8):
    i_start = int(width * (i-1))
    i_end= int(width * i)

    for j in range(1, 8):
        j_start = int(height * (j-1))
        j_end = int(height * j)

        img[ j_start:j_end,i_start:i_end ] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

cv2.imshow('Frame', img)
cv2.waitKey(0)