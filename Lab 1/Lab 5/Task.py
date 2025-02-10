import math
import cv2
import numpy as np

def start(core_size, smooth_value, delta_thres, contour_size):
    cv2.namedWindow('Window', cv2.WINDOW_NORMAL)
    video = cv2.VideoCapture('LR4_main_video.mov')
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('output.mp4', fourcc, 144, (w, h))
    print(video_writer)

    ok, frame = video.read()

    if(ok):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gauss_frame = cv2.GaussianBlur(gray_frame, (core_size, core_size), sigmaX=smooth_value, sigmaY=smooth_value)
        new_frame = gauss_frame

        while True:
            prev_frame = new_frame.copy()
            ok, frame = video.read()
            if not ok:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gauss_frame = cv2.GaussianBlur(gray_frame, (core_size, core_size), sigmaX=smooth_value, sigmaY=smooth_value)

            new_frame = gauss_frame

            diff_frame = cv2.absdiff(prev_frame, new_frame)

            thres_frame = cv2.threshold(diff_frame, delta_thres, 255, cv2.THRESH_BINARY)[1]

            (contours, hierarchy) = cv2.findContours(thres_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contr in contours:
                area = cv2.contourArea(contr)
                if area < contour_size:
                    continue
                video_writer.write(frame)
                cv2.imshow('frame', thres_frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    video.release()
    video_writer.release()
    cv2.destroyAllWindows()


start(11, 70, 60, 10)
