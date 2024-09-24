import cv2

def readVideoWriteTOFile():
    cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
    video = cv2.VideoCapture("C:/Users/minen/Desktop/Unik/Vision/random.mp4")
    state, img = video.read()
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    video_writer = cv2.VideoWriter("output.mov", fourcc, 25, (w, h))
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

readVideoWriteTOFile()