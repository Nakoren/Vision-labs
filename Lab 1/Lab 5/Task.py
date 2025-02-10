import math
import cv2
import numpy as np

def start():
    cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
    video = cv2.VideoCapture("LR4_main_video.mov")
    state, img = video.read()
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter.fourcc(*'XVID')
    video_writer = cv2.VideoWriter("output.mov", fourcc, 25, (w, h))

    core_size = 11
    smooth_value = 70

    delta_thres = 60
    contourSize = 10

    ok, img = video.read()
    if ok:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        prev_blur_frame = cv2.GaussianBlur(img, (core_size, core_size), smooth_value)
        while True:
            ok, img = video.read()
            if not ok:
                break

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            new_blur_frame = cv2.GaussianBlur(img, (core_size, core_size), smooth_value, smooth_value)

            diff = cv2.absdiff(prev_blur_frame, new_blur_frame)

            thres_frame = cv2.threshold(diff, delta_thres, 255, cv2.THRESH_BINARY)[1]

            (cont, hierarchy) = cv2.findContours(thres_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contr in cont:
                area = cv2.contourArea(contr)
                if area < contourSize:
                    continue
                video_writer.write(img)
                cv2.imshow('Window', img)

            if cv2.waitKey(1) & 0xFF == 27:
                break
            prev_blur_frame = new_blur_frame

    video.release()
    video_writer.release()
    cv2.destroyAllWindows()


start()
