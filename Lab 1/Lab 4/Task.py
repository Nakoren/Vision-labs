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
    suppressed = supressMaximums(img, lengths, angles)

    maxGradient = getMaxValueFromMatrix(lengths)

    lowLevel = maxGradient//15
    highLevel = maxGradient//5

    filtered = doubleEdgeFiltration(suppressed, lengths, lowLevel, highLevel)

    cv2.namedWindow('Kanni', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Kanni', 1000, 500)
    cv2.imshow("Kanni", filtered)
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
            if(xLocalRes==0):
                xLocalRes = 0.001
            resMatrixLength[i][j] = math.sqrt(pow(xLocalRes, 2)+pow(yLocalRes, 2))
            #SOMETHING WRONG... MAYBE
            tangRes = math.tan(yLocalRes/xLocalRes)
            finRes = -1
            if(xLocalRes > 0 and yLocalRes < 0 and tangRes < -2.414) or (xLocalRes<0 and yLocalRes<0 and tangRes>2.414):
                finRes = 0
            elif(xLocalRes > 0 and yLocalRes < 0 and tangRes <-0.414):
                finRes = 1
            elif(xLocalRes>0 and yLocalRes<0 and tangRes > -0.414) or (xLocalRes>0 and yLocalRes>0 and tangRes < 0.414):
                finRes = 2
            elif(xLocalRes>0 and yLocalRes>0 and tangRes <2.414):
                finRes = 3
            elif(xLocalRes>0 and yLocalRes>0 and tangRes > 2.414) or (xLocalRes<0 and yLocalRes>0 and tangRes > -2.414):
                finRes = 4
            elif(xLocalRes<0 and yLocalRes>0 and tangRes < -0.414):
                finRes = 5
            elif(xLocalRes<0 and yLocalRes>0 and tangRes > -0.414) or (xLocalRes<0 and yLocalRes<0 and tangRes < 0.414):
                finRes = 6
            elif(xLocalRes<0 and yLocalRes<0 and tangRes < 2.414):
                finRes = 7
            resMatrixAngle[i][j] = finRes

    return resMatrixLength, resMatrixAngle

def supressMaximums(img, lengths, directions):
    resMatrix = np.zeros((img.shape[0], img.shape[1]), np.float64)
    for i in range(1, len(img) - 1):
        for j in range(1, len(img[i]) - 1):
            check = False
            if (directions[i][j] == 0) or (directions[i][j] == 4):
                if(lengths[i][j]>lengths[i+1][j]) and (lengths[i][j]>lengths[i-1][j]): check = True
            elif (directions[i][j] == 1) or (directions[i][j] == 5):
                if (lengths[i][j] > lengths[i + 1][j + 1]) and (lengths[i][j] > lengths[i - 1][j - 1]): check = True
            elif (directions[i][j] == 2) or (directions[i][j] == 6):
                if (lengths[i][j] > lengths[i][j + 1]) and (lengths[i][j] > lengths[i][j - 1]): check = True
            elif (directions[i][j] == 3) or (directions[i][j] == 7):
                if (lengths[i][j] > lengths[i + 1][j - 1]) and (lengths[i][j] > lengths[i - 1][j + 1]): check = True

            if check: resMatrix[i][j] = 255

    return resMatrix

def getMaxValueFromMatrix(matrix):
    max = 0
    for line in matrix:
        for cur in line:
            if cur > max:
                max = cur
    return max


def doubleEdgeFiltration(img, lengths, lowLevel, highLevel):
    resMatrix = np.zeros((img.shape[0], img.shape[1]), np.float64)
    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            if img[i][j] == 255:
                pixelLength = lengths[i][j]
                if pixelLength > highLevel:
                    resMatrix[i][j] = 255
                elif pixelLength < lowLevel:
                    continue

    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            if img[i][j] == 255:
                if lowLevel < lengths[i][j] < highLevel:
                    check = False
                    for k in range(-1,1):
                        for n in range(-1,1):
                            if resMatrix[i+k][j+n] != 0:
                                    check = True
                    if check:
                        resMatrix[i][j] = 255
    return resMatrix



start(path = "City_shakal.png")