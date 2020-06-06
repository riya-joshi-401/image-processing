
import cv2

img = cv2.imread('n2.jpg')
size = img.shape

cv2.line(img, (0,0), (size[1],size[0]), (0, 0, 255), 4)

cv2.imshow ('Image', img)
cv2.waitKey (0)