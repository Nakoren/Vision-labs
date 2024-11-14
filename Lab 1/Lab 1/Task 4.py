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

        '''updateImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)'''

        updateImg = cv2.resize(img, (100, 100))

        if not(ok):
            break
        cv2.imshow('Window', updateImg)
        video_writer.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

readVideoWriteTOFile()