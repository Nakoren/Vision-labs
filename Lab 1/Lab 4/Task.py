import math
import cv2
import numpy as np

def start(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    cv2.namedWindow('Normal', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Normal', 1000, 500)
    cv2.imshow("Normal", img)

    size = 5
    smooth_value = 0.5
    blurred = gaussianBlurCV(img, size, smooth_value)

    lengths, angles = getGradients(blurred)
    #print(lengths)
    print(angles)

    cv2.namedWindow('Blurred', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Blurred', 1000, 500)
    cv2.imshow("Blurred", blurred)
    cv2.waitKey(0)
    cv2.destroyWindow('Normal')

def gaussianBlurCV(img, core_size, smooth_value):
    blur_img = cv2.GaussianBlur(img, (core_size, core_size), smooth_value)
    return blur_img

def getGradients(img):
    resMatrixLength = np.ones((img.shape[0], img.shape[1]), np.float64)
    resMatrixAngle = np.ones((img.shape[0], img.shape[1]), np.float64)

    xKernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    yKernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    for i in range(1, len(img)-1):
        for j in range(1, len(img[i])-1):
            xLocalRes = 0
            yLocalRes = 0
            for k in range(3):
                for n in range(3):
                    xLocalRes += img[i-k-1][j-n-1] * xKernel[k][n]
                    yLocalRes += img[i-k-1][j-n-1] * yKernel[k][n]
            resMatrixLength[i][j] = math.sqrt(pow(xLocalRes, 2)+pow(yLocalRes, 2))
            if(xLocalRes != 0):
                resMatrixAngle[i][j] = math.atan(yLocalRes/xLocalRes)
            else:
                resMatrixAngle[i][j] = 0

    return resMatrixLength, resMatrixAngle


start(path = "City_shakal.png")