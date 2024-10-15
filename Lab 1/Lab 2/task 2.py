import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Default", frame)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('frame', hsvFrame)

    # creating mask
    downRed1 = np.array([0, 100, 100])
    upRed1 = np.array([10, 255, 255])
    downRed2 = np.array([160, 100, 100])
    upRed2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsvFrame, downRed1, upRed1)
    mask2 = cv2.inRange(hsvFrame, downRed2, upRed2)
    redMask = cv2.bitwise_or(mask1, mask2)

    # displaying red
    cv2.imshow('Thres Red', redMask)
    res = cv2.bitwise_and(hsvFrame, hsvFrame, mask=redMask)
    cv2.imshow("Result", cv2.cvtColor(res, cv2.COLOR_HSV2BGR))
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()