import cv2

cap = cv2.VideoCapture(0)

c = 1


while c <= 100:
    x, frame = cap.read()

    path = 'DUMP/IMG_{0}.jpg'.format(c)

    cv2.imwrite(path, frame)
    c += 1