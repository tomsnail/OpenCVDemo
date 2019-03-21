import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
debug = 1

matplotlib.rcParams['font.family'] = 'SimHei'

def canny():
    src = cv2.imread('kk.jpg')

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 100, 150, apertureSize=3, L2gradient=False);
    dst=cv2.bitwise_and(src,src,dst,dst)
    cv2.imwrite('canny.jpg', dst)
    f, axarr = plt.subplots(1, 2)
    axarr[0].imshow(cv2.imread('kk.jpg'))
    axarr[0].set_title('原图')
    axarr[1].imshow(cv2.imread('canny.jpg'))
    axarr[1].set_title('canny')
    plt.show()




def contours():
   contours1()
   contours2()
   contours3()
   contours4()
   f, axarr = plt.subplots(1, 5)
   axarr[0].imshow(cv2.imread('s5.jpg'))
   axarr[0].set_title('原图')
   axarr[1].imshow(cv2.imread('contours1.jpg'))
   axarr[1].set_title('contours50')
   axarr[2].imshow(cv2.imread('contours2.jpg'))
   axarr[2].set_title('contours100')
   axarr[3].imshow(cv2.imread('contours3.jpg'))
   axarr[3].set_title('GaussianBlur3')
   axarr[4].imshow(cv2.imread('contours4.jpg'))
   axarr[4].set_title('GaussianBlur15')
   plt.show()

def contours1():
    src = cv2.imread('s5.jpg')
    # gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False);
    imp1,contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imwrite('contours1.jpg', src)

def contours2():
    src = cv2.imread('s5.jpg')
    # gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 100, 200, apertureSize=3, L2gradient=False);
    imp1,contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imwrite('contours2.jpg', src)



def contours3():
    src = cv2.imread('s5.jpg')
    gray = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False);
    imp1,contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imwrite('contours3.jpg', src)


def contours4():
    src = cv2.imread('s5.jpg')
    gray = cv2.GaussianBlur(src, (15, 15), 0)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False);
    imp1,contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(src, contours, -1, (0, 0, 255), 1)
    cv2.imwrite('contours4.jpg', src)


def matchTemplate():
    src = cv2.imread('s5.jpg')
    tmpl = cv2.imread('s6.jpg')

    methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
    th, tw = tmpl.shape[:2]
    f, axarr = plt.subplots(1, len(methods)+2)
    axarr[0].imshow(cv2.imread('s5.jpg'))
    axarr[1].imshow(cv2.imread('s6.jpg'))
    i = 2
    for md in methods:
        result = cv2.matchTemplate(src, tmpl, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if md == cv2.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        cv2.rectangle(src, tl, br, [0, 255, 0],2)
        cv2.imwrite("pipei" + np.str(md)+'.jpg', src)
        axarr[i].imshow(cv2.imread("pipei" + np.str(md)+'.jpg'))
        axarr[i].set_title(np.str(methods[i-2]))
        i = i+1
    plt.show()





def main():
    canny()
    contours()
    matchTemplate()

main()