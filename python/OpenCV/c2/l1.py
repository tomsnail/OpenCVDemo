import cv2
import numpy as np



#通道分离与合并
def td():
    img = cv2.imread('kk.jpg')
    mv = cv2.split(img)
    print(len(mv))
    for i in range(len(mv)):
        cv2.imwrite('kk'+str(i)+".jpg",mv[i])


#均值方差计算


#图像亮度与对比度
def ll0():
    img = cv2.imread('kk.jpg')
    img2 = np.ones(img.shape, dtype=np.uint8)  # 通过二维NumPy数组来简单创建一个黑色的正方形图像
    dst = cv2.add(img,img2)
    cv2.imshow('kk12.jpg',dst)
    cv2.waitKey()

#图像叠加
def ll():
    img = cv2.imread('kk.jpg')
    img2 = cv2.imread('kk.jpg')
    dst = cv2.addWeighted(img,1.5,img2,-0.5,30)
    cv2.imshow('kk12.jpg',dst)
    cv2.waitKey()

def ll2():
        img = cv2.imread('kk.jpg')
        img2 = cv2.imread('s1.jpg')
        sp = img.shape
        img2 = cv2.resize(img2,(sp[1],sp[0]),interpolation=cv2.INTER_CUBIC)
        dst = cv2.addWeighted(img, 0.8, img2,0.2, 30)
        cv2.imshow('kk12.jpg', dst)
        cv2.waitKey()

#其他操作

def main():
    ll2()

main()