import cv2

cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
videoCap = cv2.VideoCapture("C:/Users/minen/Desktop/Unik/Vision/random.mp4", cv2.CAP_ANY)
print(videoCap.isOpened())

while(True):
    ret, frame = videoCap.read()
    if not(ret):
        break
    cv2.imshow('Window', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break