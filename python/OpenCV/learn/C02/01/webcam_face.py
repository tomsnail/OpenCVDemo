# -*- coding: utf-8 -*-
import cv2
import numpy as np

def face():
    #载入识别人脸数据xml文件进入内存
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #调用摄像
    cam = cv2.VideoCapture(0)

    while(True):
        #读入数据
        ret, img = cam.read()
        #变灰度
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #识别人脸
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        #在人脸上画出绿色方块
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        #显示在结果图像上显示方块
        cv2.imshow("Face", img)

        #按q键退出
        if(cv2.waitKey(1) == ord('q')):
            break

    #释放摄像
    cam.release()
    #删掉所有窗口
    cv2.destroyAllWindows()


if __name__ == '__main__':
    face()