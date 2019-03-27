import sys
import shutil
import os
import cv2
import dlib
import time

input_dir = './images/input'
output_dir = './images/faces'
size = 64


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def capture(name,count=None):
    if count is None:
        count = 500
    if not os.path.exists(input_dir+"/"+name):
        os.makedirs(input_dir+"/"+name)
    shutil.rmtree(input_dir+"/"+name)
    os.mkdir(input_dir+"/"+name)
    work = True
    cameraCapture = cv2.VideoCapture(0)
    cv2.namedWindow('CameraWindow')
    success, frame = cameraCapture.read()
    index = 1
    while success and cv2.waitKey(1)== -1 and index < count:
        filename = str(index) + ".jpg"
        cv2.imwrite(input_dir+"/"+name+"/"+filename, frame)
        print('Being processed picture %s' % index)
        cv2.imshow('CameraWindow',frame)
        success, frame = cameraCapture.read()
        index += 1
    cv2.destroyWindow("CameraWindow")
    cameraCapture.release()

def face_decector(name,count=2000):
    detector = dlib.get_frontal_face_detector()
    index = 1
    if not os.path.exists(output_dir+"/"+name):
        os.makedirs(output_dir+"/"+name)
    shutil.rmtree(output_dir + "/" + name)
    os.mkdir(output_dir + "/" + name)
    for (path, dirnames, filenames) in os.walk(input_dir+"/"+name):
        for filename in filenames:
            if filename.endswith('.jpg'):
                print(filename+'Being processed picture %s'  % index)
                img_path = path+'/'+filename
                # 从文件读取图片
                img = cv2.imread(img_path)
                # 转为灰度图片
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # 使用detector进行人脸检测 dets为返回的结果
                dets = detector(gray_img, 1)
                #使用enumerate 函数遍历序列中的元素及它们的下标
                #下标i即为人脸序号
                #left：人脸左边与图片左边界的距离 ；right：人脸右边与图片左边界的距离
                #top：人脸上边与图片上边界的距离 ；bottom：人脸下边与图片上边界的距离
                for i, d in enumerate(dets):
                    x1 = d.top() if d.top() > 0 else 0
                    y1 = d.bottom() if d.bottom() > 0 else 0
                    x2 = d.left() if d.left() > 0 else 0
                    y2 = d.right() if d.right() > 0 else 0
                    # img[y:y+h,x:x+w]
                    face = img[x1:y1,x2:y2]
                    # 调整图片的尺寸
                    face = cv2.resize(face, (size,size))
                    #cv2.imshow('image',face)
                    # 保存图片
                    cv2.imwrite(output_dir+'/'+name+"/"+str(index)+'.jpg', face)
                    index += 1
                #不断刷新图像，频率时间为30ms
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    sys.exit(0)
        if index >= count:
            break
def main():
    capture('yangda',2000)
    #face_decector('other_faces')
    pass

if __name__ == '__main__':
    main()