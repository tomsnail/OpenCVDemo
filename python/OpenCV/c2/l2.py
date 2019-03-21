import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
debug = 1

matplotlib.rcParams['font.family'] = 'SimHei'


### 模糊

def blur():
    img = cv2.imread('s2.jpg')
    dst = cv2.blur(img,(9,9))
    cv2.imwrite('blur.jpg',dst)
    dst = cv2.GaussianBlur(img, (15, 15), 0)
    cv2.imwrite('GaussianBlur.jpg', dst)
    dst = cv2.medianBlur(img, 15)
    cv2.imwrite('medianBlur.jpg', dst)
    f, axarr = plt.subplots(1, 4)
    axarr[0].imshow(cv2.imread('s2.jpg'))
    axarr[0].set_title('原图')
    axarr[1].imshow(cv2.imread('blur.jpg'))
    axarr[1].set_title('blur')
    axarr[2].imshow(cv2.imread('GaussianBlur.jpg'))
    axarr[2].set_title('GaussianBlur')
    axarr[3].imshow(cv2.imread('medianBlur.jpg'))
    axarr[3].set_title('medianBlur')
    plt.show()





def dilateAerode():
    img = cv2.imread('s2.jpg')
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    dst = cv2.dilate(img,kernel)
    cv2.imwrite('dilate.jpg', dst)
    dst = cv2.erode(img, kernel)
    cv2.imwrite('erode.jpg', dst)
    f, axarr = plt.subplots(1, 3)
    axarr[0].imshow(cv2.imread('s2.jpg'))
    axarr[0].set_title('原图')
    axarr[1].imshow(cv2.imread('dilate.jpg'))
    axarr[1].set_title('dilate')
    axarr[2].imshow(cv2.imread('erode.jpg'))
    axarr[2].set_title('erode')
    plt.show()




### 边缘保留滤波
def bilateralFilterApyrMeanShiftFiltering():
    img = cv2.imread('s3.jpg')
    dst = cv2.bilateralFilter(img, 0,150,15)
    cv2.imwrite('bilateralFilter.jpg', dst)
    dst = cv2.pyrMeanShiftFiltering(img, 10, 50)
    cv2.imwrite('pyrMeanShiftFiltering.jpg', dst)
    f, axarr = plt.subplots(1, 3)
    axarr[0].imshow(cv2.imread('s3.jpg'))
    axarr[0].set_title('原图')
    axarr[1].imshow(cv2.imread('bilateralFilter.jpg'))
    axarr[1].set_title('bilateralFilter')
    axarr[2].imshow(cv2.imread('pyrMeanShiftFiltering.jpg'))
    axarr[2].set_title('pyrMeanShiftFiltering')
    plt.show()

### 自定义滤波


### 形态学操作

def morphologyEx():
    img = cv2.imread('s2.jpg')
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dst = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)
    cv2.imwrite('MORPH_DILATE.jpg', dst)
    dst = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
    cv2.imwrite('MORPH_ERODE.jpg', dst)
    dst = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.imwrite('MORPH_OPEN.jpg', dst)
    dst = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite('MORPH_CLOSE.jpg', dst)
    dst = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
    cv2.imwrite('MORPH_BLACKHAT.jpg', dst)
    dst = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
    cv2.imwrite('MORPH_TOPHAT.jpg', dst)
    dst = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    cv2.imwrite('MORPH_GRADIENT.jpg', dst)

    f, axarr = plt.subplots(2, 4)
    axarr[0,0].imshow(cv2.imread('s2.jpg'))
    axarr[0,0].set_title('原图')
    axarr[0, 1].imshow(cv2.imread('MORPH_DILATE.jpg'))
    axarr[0, 1].set_title('MORPH_DILATE')
    axarr[0, 2].imshow(cv2.imread('MORPH_ERODE.jpg'))
    axarr[0, 2].set_title('MORPH_ERODE')
    axarr[0, 3].imshow(cv2.imread('MORPH_OPEN.jpg'))
    axarr[0, 3].set_title('MORPH_OPEN')
    axarr[1, 0].imshow(cv2.imread('MORPH_CLOSE.jpg'))
    axarr[1, 0].set_title('MORPH_CLOSE')
    axarr[1, 1].imshow(cv2.imread('MORPH_BLACKHAT.jpg'))
    axarr[1, 1].set_title('MORPH_BLACKHAT')
    axarr[1, 2].imshow(cv2.imread('MORPH_TOPHAT.jpg'))
    axarr[1, 2].set_title('MORPH_TOPHAT')
    axarr[1, 3].imshow(cv2.imread('MORPH_GRADIENT.jpg'))
    axarr[1, 3].set_title('MORPH_GRADIENT')
    plt.show()

### 阈值化

def threshold():
    img = cv2.imread('s5.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, dst = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    cv2.imwrite('THRESH_BINARY.jpg', dst)
    retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('THRESH_BINARY_INV.jpg', dst)
    retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    cv2.imwrite('THRESH_TRUNC.jpg', dst)
    retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)
    cv2.imwrite('THRESH_TOZERO.jpg', dst)
    retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO_INV)
    cv2.imwrite('THRESH_TOZERO_INV.jpg', dst)
    dst = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 15,10)
    cv2.imwrite('ADAPTIVE_THRESH_GAUSSIAN_C.jpg', dst)
    f, axarr = plt.subplots(2, 4)
    axarr[0, 0].imshow(cv2.imread('s5.jpg'))
    axarr[0, 0].set_title('原图')
    axarr[0, 1].imshow(cv2.imread('THRESH_BINARY.jpg'))
    axarr[0, 1].set_title('THRESH_BINARY')
    axarr[0, 2].imshow(cv2.imread('THRESH_BINARY_INV.jpg'))
    axarr[0, 2].set_title('THRESH_BINARY_INV')
    axarr[0, 3].imshow(cv2.imread('THRESH_TRUNC.jpg'))
    axarr[0, 3].set_title('THRESH_TRUNC')
    axarr[1, 0].imshow(cv2.imread('THRESH_TOZERO.jpg'))
    axarr[1, 0].set_title('THRESH_TOZERO')
    axarr[1, 1].imshow(cv2.imread('THRESH_TOZERO_INV.jpg'))
    axarr[1, 1].set_title('THRESH_TOZERO_INV')
    axarr[1, 2].imshow(cv2.imread('ADAPTIVE_THRESH_GAUSSIAN_C.jpg'))
    axarr[1, 2].set_title('ADAPTIVE_THRESH_GAUSSIAN_C')
    plt.show()

def main():
   blur()
   dilateAerode()
   bilateralFilterApyrMeanShiftFiltering()
   morphologyEx()
   threshold()

main()