import cv2
import numpy as np
from fontTools.pens import areaPen

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    downRed = np.array([0, 100, 100])
    upRed = np.array([20, 255, 255])
    '''
    downRed2 = np.array([160,100,100])
    upRed2 = np.array([200,255,255])
    '''
    mask = cv2.inRange(hsv_frame, downRed, upRed)

    '''
    mask2 = cv2.inRange(hsv_frame, downRed2, upRed2)
    mask = cv2.bitwise_or(mask, mask2)
    '''

    transformKernel = np.ones((10, 10), np.uint8)

    maskOpened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, transformKernel)
    maskClosed = cv2.morphologyEx(maskOpened, cv2.MORPH_CLOSE, transformKernel)

    cv2.imshow('Closed', maskClosed)
    res = cv2.bitwise_and(hsv_frame, hsv_frame, mask=mask)
    moments = cv2.moments(maskClosed)

    areaSize = moments['m00']
    m01 = moments['m01']
    m10 = moments['m10']

    if (areaSize>100):
        centroidX = int(m10/areaSize)
        centroidY = int(m01/areaSize)
        cv2.circle(frame, (centroidX, centroidY), 3, (255, 255, 255), 1)
        y, x = np.nonzero(maskClosed)
        left = np.min(x)
        right = np.max(x)
        top = np.max(y)
        bottom = np.min(y)
        cv2.rectangle(frame, (left, bottom), (right, top), (255, 255, 255), 4)

    cv2.imshow('source frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
