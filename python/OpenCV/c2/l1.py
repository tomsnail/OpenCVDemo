import cv2
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
debug = 1

matplotlib.rcParams['font.family'] = 'Hei'



#通道分离与合并

def td():
    img = cv2.imread('kk.jpg')
    mv = cv2.split(img)
    f, axarr = plt.subplots(1, 5)
    axarr[0].imshow(cv2.imread('kk.jpg'))
    for i in range(len(mv)):
        cv2.imwrite('kk' + str(i) + ".jpg", mv[i])
        axarr[i+1].imshow(cv2.imread('kk' + str(i) + ".jpg"))
    plt.show()


#均值方差计算


#图像亮度与对比度
def ll0():
    img = cv2.imread('kk.jpg')
    img2 = np.ones(img.shape, dtype=np.uint8)  # 通过二维NumPy数组来简单创建一个黑色的正方形图像
    dst = cv2.add(img,img2)
    cv2.imwrite('kk11.jpg',dst)
    f, axarr = plt.subplots(1, 2)
    axarr[0].imshow(cv2.imread('kk.jpg'))
    axarr[1].imshow(cv2.imread('kk11.jpg'))
    plt.show()

#图像叠加
def ll():
    img = cv2.imread('kk.jpg')
    img2 = cv2.imread('kk.jpg')
    dst = cv2.addWeighted(img,1.5,img2,-0.5,30)
    cv2.imwrite('kk12.jpg', dst)
    f, axarr = plt.subplots(1, 2)
    axarr[0].imshow(cv2.imread('kk.jpg'))
    axarr[1].imshow(cv2.imread('kk12.jpg'))
    plt.show()

def ll2():
        img = cv2.imread('kk.jpg')
        img2 = cv2.imread('s2.jpg')
        sp = img.shape
        img2 = cv2.resize(img2,(sp[1],sp[0]),interpolation=cv2.INTER_CUBIC)
        dst = cv2.addWeighted(img, 0.8, img2,0.2, 30)
        cv2.imwrite('kk13.jpg', dst)
        f, axarr = plt.subplots(1, 3)
        axarr[0].imshow(cv2.imread('kk.jpg'))
        axarr[1].imshow(cv2.imread('s2.jpg'))
        axarr[2].imshow(cv2.imread('kk13.jpg'))
        plt.show()

#其他操作

def main():
    td()
    ll0()
    ll()
    ll2()
main()