import cv2
import numpy as np

def canny():
    src = cv2.imread('kk.jpg')

   # gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 100, 150, apertureSize=3, L2gradient=False);
    dst=cv2.bitwise_and(src,src,dst,dst)
    cv2.imshow('canny.jpg', dst)
    cv2.waitKey()

def contours():
    src = cv2.imread('s5.jpg')

    #gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False);
    img1, contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imshow('contours.jpg', src)
    cv2.waitKey()
    pass

def contours1():
    src = cv2.imread('s5.jpg')

    gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False);
    img1, contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imshow('contours.jpg', src)
    cv2.waitKey()
    pass

def contours2():
    src = cv2.imread('s5.jpg')

    gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.bilateralFilter(gray, 0, 150, 15)
    # gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    # dst = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False);
    # img1, contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imshow('contours.jpg', gray)
    cv2.waitKey()
    pass

def contours3():
    src = cv2.imread('s5.jpg')

    gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray);
    retval, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    dst = cv2.Canny(gray, 100, 200, apertureSize=3, L2gradient=False);
    img1, contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imshow('contours.jpg', src)
    cv2.waitKey()
    pass

def matchTemplate():
    src = cv2.imread('s5.jpg')
    tmpl = cv2.imread('s6.jpg')

    methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
    th, tw = tmpl.shape[:2]
    for md in methods:
        result = cv2.matchTemplate(src, tmpl, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if md == cv2.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        cv2.rectangle(src, tl, br, [0, 255, 0],2)
        cv2.imshow("pipei" + np.str(md), src)
        cv2.waitKey()






def main():
    matchTemplate()

main()