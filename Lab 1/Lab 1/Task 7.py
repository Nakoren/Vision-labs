import cv2
def readIPWriteTOFile():
    cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
    video = cv2.VideoCapture(0)
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("outputCam.mp4", fourcc, 25, (w, h))
    while (True):
        ok, img = video.read()
        if not(ok):
            break
        cv2.imshow('Window', img)

        video_writer.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

readIPWriteTOFile()