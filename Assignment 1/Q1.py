import cv2

n = int (input (" Enter the number of frames after which the webcam should flip : "))

cap = cv2.VideoCapture(0)

counter = 0

while True:
    x, frame = cap.read()

    if counter % n == 0:
        flipped = cv2.flip (frame, -1)  # vertical flip
    else:
        flipped = frame

    cv2.imshow ('cap', flipped)

    if cv2.waitKey (1) & 0xFF == ord('q'): 
        break

    counter += 1