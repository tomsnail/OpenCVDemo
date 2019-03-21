import cv2
import numpy as np
#画线
def lines():
    img=np.zeros((300,400,3),np.uint8)
    cv2.line(img,(10,10),(200,200),(0,255,0),3)
    cv2.imshow('line.jpg',img)
    cv2.waitKey()


#矩形
def rectangle():
    img = np.zeros((300, 400, 3), np.uint8)
    cv2.rectangle(img,(10,10),(30,40),(134,2,34),1)
    cv2.imshow('line.jpg', img)
    cv2.waitKey()
#圆
def circle():
    img = np.zeros((300, 400, 3), np.uint8)
    cv2.circle(img,(60,60),30,(0,0,213),-1)
    cv2.imshow('line.jpg', img)
    cv2.waitKey()
#文字
def text():
    img = np.zeros((300, 400, 3), np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'text at here', (80, 90), font, 1, (255, 255, 255), 3)
    cv2.imshow('line.jpg', img)
    cv2.waitKey()


def main():
    text()

main()