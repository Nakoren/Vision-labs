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

    cv2.namedWindow('Blurred', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Blurred', 1000, 500)
    cv2.imshow("Blurred", suppressed)
    cv2.waitKey(0)
    cv2.destroyWindow('Normal')

def gaussianBlurCV(img, core_size, smooth_value):
    blur_img = cv2.GaussianBlur(img, (core_size, core_size), smooth_value)
    return blur_img

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

def getGradients(img):
    resMatrixLength = np.ones((img.shape[0], img.shape[1]), np.float64)
    resMatrixAngle = np.ones((img.shape[0], img.shape[1]), np.float64)

    normImg = normalize(img)

    xKernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    yKernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    for i in range(1, len(normImg)-1):
        for j in range(1, len(normImg[i])-1):
            x = img[i][j]
            y = img[i][j]
            xLocalRes = 0
            yLocalRes = 0
            for k in range(3):
                for n in range(3):
                    xLocalRes += normImg[i-k-1][j-n-1] * xKernel[k][n]
                    yLocalRes += normImg[i-k-1][j-n-1] * yKernel[k][n]
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


start(path = "Pic_shakal.jpg")