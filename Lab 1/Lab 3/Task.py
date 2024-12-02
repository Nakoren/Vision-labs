import math
import cv2
import numpy as np

def start():

    img = cv2.imread("Pic_compressed.jpg", cv2.IMREAD_GRAYSCALE)

    cv2.namedWindow('Normal', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Normal', 1000, 500)
    cv2.imshow("Normal", img)

    size1 = 5
    smooth_value1 = 1

    size2 = 10
    smooth_value2 = 0.5

    blurred = gaussianBlurCV(img, size1, smooth_value2)

    cv2.namedWindow('Blurred', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Blurred', 1000, 500)
    cv2.imshow("Blurred", blurred)
    cv2.waitKey(0)
    cv2.destroyWindow('Normal')


def gaussianBlurCV(img, core_size, smooth_value):
    blur_img = cv2.GaussianBlur(img, (core_size, core_size), smooth_value)
    return blur_img

def gaussianBlur(img, core_size, smooth_value):
    print("Getting matrix")
    gaussian_matr = get_gaussian_matrix(core_size, smooth_value)
    print("normalizing")
    normalized_matr = normalize(gaussian_matr)


    blur_img = img.copy()

    core_center = core_size // 2
    for i in range(core_center, blur_img.shape[0] - core_center):
        for j in range(core_center, blur_img.shape[1] - core_center):
            #print("Updating pixel" + str(i) +" - " + str(j))
            # операция свёртки
            new_value = 0
            for k in range(-(core_size // 2), core_size // 2+1):
                for l in range(-(core_size // 2), core_size // 2+1):
                    new_value += img[i + k, j + l] * normalized_matr[k + (core_size // 2), l + (core_size // 2)]
            blur_img[i, j] = new_value
    return blur_img


def get_gaussian_matrix(size, smooth_value):
    av_deviation = (math.ceil(size), math.ceil(size))
    result_matrix = np.ones((size, size))
    for x in range(size):
        for y in range(size):
            power = -1*(((x-av_deviation[0]) ** 2 + (y-av_deviation[1]) ** 2)/2*(pow(smooth_value,2)))
            print(power)

            result_matrix[x, y] = 1/(2*math.pi*(pow(smooth_value,2))) * pow(math.e, power)
    return result_matrix


def normalize(matr):
    sum = 0
    for line in matr:
        for el in line:
            sum+=el
    result_matrix = np.ones((matr.shape[0], matr.shape[1]), np.float64)
    for i in range(len(matr)):
       for j in range(len(matr)):
           result_matrix[i,j] = matr[i,j]/sum

    return result_matrix

start()