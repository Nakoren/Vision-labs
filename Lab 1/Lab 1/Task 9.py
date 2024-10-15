import cv2

URL = f'http://192.168.88.176:8080'

def readIPWriteTOFile():
    cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
    video = cv2.VideoCapture(URL+'/video')
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while (True):
        ok, img = video.read()
        if not(ok):
            break
        rectColor = getRectColor(img[w//2, h//2])
        cv2.rectangle(img, (int(w / 2 - 100), int(h / 2 + 10)), (int(w / 2 + 100), int(h / 2 - 10)), rectColor, 3)
        cv2.rectangle(img, (int(w / 2 - 10), int(h / 2 + 100)), (int(w / 2 + 10), int(h / 2 - 100)), rectColor, 3)
        cv2.imshow('Window', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


def getRectColor(sourceColor):
    blue, green, red = sourceColor
    if (blue >= green) and (blue >= red):
        resColor = (255, 0, 0)
    if (green >= blue) and (green >= red):
        resColor = (0, 255, 0)
    if (red >= blue) and (red >= green):
        resColor = (0, 0, 255)
    return resColor




readIPWriteTOFile()