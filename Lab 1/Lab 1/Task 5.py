import cv2

img = cv2.imread("C:/Users/minen/Desktop/Unik/Vision/random.png")
newImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

cv2.namedWindow('oldImg', cv2.WINDOW_NORMAL)
cv2.namedWindow('newImg', cv2.WINDOW_NORMAL)

cv2.imshow('oldImg',img)
cv2.imshow('newImg',newImg)

cv2.waitKey(0)
cv2.destroyWindow('Window')