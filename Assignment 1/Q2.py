import cv2

cap = cv2.VideoCapture(0)
counter = 0

while True:
    x, frame = cap.read()

    if counter % 2 == 0:
        flipped = cv2.flip(frame, 1) # horizontal flipping
    else:
        flipped = frame

    cv2.imshow('Frame', flipped)

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

    counter += 1