import cv2
import numpy as np


### 模糊

def blur():
    img = cv2.imread('s2.jpg')
    dst = cv2.blur(img,(9,9))
    cv2.imshow('blur.jpg',dst)
    cv2.waitKey()


def GaussianBlur():
    img = cv2.imread('s2.jpg')
    dst = cv2.GaussianBlur(img,(15,15),0)
    cv2.imshow('GaussianBlur.jpg', dst)
    cv2.waitKey()

### 统计排序滤波

def medianBlur():
    img = cv2.imread('s2.jpg')
    dst = cv2.medianBlur(img,15)
    cv2.imshow('medianBlur.jpg',dst)
    cv2.waitKey()


def dilate():
    img = cv2.imread('s2.jpg')
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    dst = cv2.dilate(img,kernel)
    cv2.imshow('dilate.jpg', dst)
    cv2.waitKey()


def erode():
    img = cv2.imread('s2.jpg')
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dst = cv2.erode(img,kernel)
    cv2.imshow('erode.jpg', dst)
    cv2.waitKey()

### 边缘保留滤波
def bilateralFilter():
    img = cv2.imread('s3.jpg')
    dst = cv2.bilateralFilter(img, 0,150,15)
    cv2.imshow('bilateralFilter.jpg', dst)
    cv2.waitKey()

def pyrMeanShiftFiltering():
    img = cv2.imread('s3.jpg')
    dst = cv2.pyrMeanShiftFiltering(img, 10,50)
    cv2.imshow('pyrMeanShiftFiltering.jpg', dst)
    cv2.waitKey()
### 自定义滤波


### 形态学操作

def morphologyEx(type):
    img = cv2.imread('s2.jpg')
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    if type == 1 :
        dst = cv2.morphologyEx(img,cv2.MORPH_DILATE,kernel)
    if type == 2 :
        dst = cv2.morphologyEx(img,cv2.MORPH_ERODE,kernel)
    if type == 3 :
        dst = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
    if type == 4 :
        dst = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
    if type == 5 :
        dst = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)
    if type == 6 :
        dst = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)
    if type == 7 :
        dst = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)
    cv2.imshow('morphologyEx.jpg', dst)
    cv2.waitKey()

### 阈值化

def threshold(type):
    img = cv2.imread('s5.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if type == 1:
        retval, dst = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    if type == 2:
        retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    if type == 3:
        retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    if type == 4:
        retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)
    if type == 5:
        retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO_INV)
    if type == 6:
        dst = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 15,10)
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGRA)
    cv2.imshow('threshold.jpg', dst)
    cv2.waitKey()
    pass

def main():
    #threshold(1)
    pyrMeanShiftFiltering();

main()