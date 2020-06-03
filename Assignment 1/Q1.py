import cv2

cap = cv2.VideoCapture(0)

while True:

    x, frame = cap.read()

    # Horizontal flipping
    frame = cv2.flip(frame, 1)

    cv2.imshow(' Horizontal flipping ', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): #Escape Sequence
        break
