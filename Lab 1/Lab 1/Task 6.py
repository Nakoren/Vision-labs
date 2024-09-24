import cv2

def readIPWriteTOFile():
    cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
    video = cv2.VideoCapture(0)
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while (True):
        ok, img = video.read()
        if not(ok):
            break
        cv2.rectangle(img, (int(w / 2 - 100), int(h / 2 + 10)), (int(w / 2 + 100), int(h / 2 - 10)), (0, 0, 255), 3)
        cv2.rectangle(img, (int(w / 2 - 10), int(h / 2 + 100)), (int(w / 2 + 10), int(h / 2 - 100)), (0, 0, 255), 3)
        cv2.imshow('Window', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

readIPWriteTOFile()