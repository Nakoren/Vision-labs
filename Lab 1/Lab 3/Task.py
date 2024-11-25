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
    av_deviation = (math.ceil(size), math.ceil(size))
    result_matrix = np.ones((size, size), np.float64)
    for x in range(size):
        for y in range(size):
            power = -1*(((x-av_deviation[0]) ^ 2 + (y-av_deviation[1]) ^ 2)/2*(pow(smooth_value,2)))

            result_matrix[x, y] = pow(1/(2*math.pi*(pow(smooth_value,2)))*math.e, power)
    return result_matrix


def normalize(matr, size):
    sum = 0
    for line in matr:
        for el in line:
            sum+=el
    result_matrix = np.ones((size, size), np.float64)
    for i in range(len(matr)):
       for j in range(len(matr)):
           result_matrix[i,j] = matr[i,j]/sum

    return result_matrix


size = 5

matr = get_gaussian_matrix(size, 1)
new_matr = normalize(matr, size)
print(new_matr)


