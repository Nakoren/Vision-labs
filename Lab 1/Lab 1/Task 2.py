import cv2

im = cv2.imread("C:/Users/minen/Desktop/Unik/Vision/random.png")

cv2.namedWindow('Window',cv2.WINDOW_FREERATIO)
cv2.resizeWindow('Window',(1000,500))
cv2.imshow('Window', im)
cv2.waitKey(0)
cv2.destroyWindow('Window')