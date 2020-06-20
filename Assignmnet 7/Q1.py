import cv2
import numpy as np

def track(x):
    pass



cap = cv2.VideoCapture(0)

cv2.namedWindow('Frame', flags=cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar('HL', 'Frame', 0, 180, track)
cv2.createTrackbar('HU', 'Frame', 0, 180, track)
cv2.createTrackbar('SL', 'Frame', 0, 255, track)
cv2.createTrackbar('SU', 'Frame', 0, 255, track)
cv2.createTrackbar('VL', 'Frame', 0, 255, track)
cv2.createTrackbar('VU', 'Frame', 0, 255, track)
cv2.setTrackbarPos('HL', 'Frame', 0)
cv2.setTrackbarPos('HU', 'Frame', 179)
cv2.setTrackbarPos('SL', 'Frame', 0)
cv2.setTrackbarPos('SU', 'Frame', 255)
cv2.setTrackbarPos('VL', 'Frame', 0)
cv2.setTrackbarPos('VU', 'Frame', 255)

while (True):
    x, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hul = cv2.getTrackbarPos('HL', 'Frame')
    huh = cv2.getTrackbarPos('HU', 'Frame')
    sal = cv2.getTrackbarPos('SL', 'Frame')
    sah = cv2.getTrackbarPos('SU', 'Frame')
    val = cv2.getTrackbarPos('VL', 'Frame')
    vah = cv2.getTrackbarPos('VU', 'Frame')

    hsv_low = np.array([hul, sal, val])
    hsv_high = np.array([huh, sah, vah])

    mask = cv2.inRange(hsv, hsv_low, hsv_high)

    maskedFrame = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Masked', maskedFrame)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break