# -*- coding: utf-8 -*-
import cv2
import sys

def face(imagePath):
	#输入文件名
	#imagePath = sys.argv[1]
	#输入所用识别数据文件（可以用来替换9行中xml文件）
	# cascPath = sys.argv[2]

	#载入识别人脸数据xml文件进入内存
	faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	#读入图像文件
	image = cv2.imread(imagePath)

	#image = cv2.GaussianBlur(image,(3,3),0)
	#转换图像为灰度图像
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#识别所有可能的人脸
	#gray:灰度图像； scaleFactor:可能的人脸的远近差别系数； minNeighbors:当前物体周围有多少物体；
	#minSize:每个窗口的尺寸；
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.3,
		minNeighbors = 3,
		minSize = (10, 10),
		flags = cv2.CASCADE_SCALE_IMAGE
	)

	#显示识别出的人脸数量
	print("Found {0} faces!".format(len(faces)))

	#在人脸上画出绿色方块
	for(x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	image = cv2.resize(image,(640,480))

	#显示在结果图像上显示方块
	cv2.imshow("Faces found", image)
	#按键退出
	cv2.waitKey(0)

if __name__ == '__main__':
    face("g8.jpg")