import math
import cv2
import numpy as np

'''
cv2.namedWindow('NormalWindow', cv2.WINDOW_NORMAL)
video = cv2.VideoCapture("C:/Users/minen/Desktop/Unik/Vision/random.mp4")

while (True):
    ret, frame = video.read()
    if not(ret):
        break
    cv2.imshow('NormalWindow', frame)
    if(cv2.waitKey(1) & 0xFF == 27):
        break
'''


def get_gaussian_matrix(size, smooth_value):
    av_deviation = (size, size)
    result_matrix = np.ones((size, size), np.float32)
    print(result_matrix[0,0])
    for x in range(size):
        for y in range(size):
            power = -1*(((x-av_deviation[0]) ^ 2 + (y-av_deviation[1]) ^ 2)/2*(smooth_value ^ 2))

            result_matrix[x, y] = pow(1/(2*math.pi*(smooth_value ^ 2))*math.e, power)
    return result_matrix


size = 3
matr = get_gaussian_matrix(size, 1)
print(matr)


