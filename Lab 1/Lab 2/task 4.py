import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    downRed1 = np.array([0, 100, 100])
    upRed1 = np.array([10, 255, 255])
    downRed2 = np.array([160, 100, 100])
    upRed2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv_frame, downRed1, upRed1)
    mask2 = cv2.inRange(hsv_frame, downRed2, upRed2)
    redMask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    opened = cv2.morphologyEx(redMask, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('Closed', closed)

    res = cv2.bitwise_and(hsv_frame, hsv_frame, mask=redMask)

    moments = cv2.moments(closed)
    if moments['m00'] != 0:
        area = moments['m00']  # Площадь объекта
        print(f"Area of the object: {area}")
        print(f"Zero-moment:{moments['m00']}")
        print(f"First-order moments:{moments['m01']},{moments['m10']}")

    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
