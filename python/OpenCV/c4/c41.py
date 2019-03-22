import cv2
import time
import numpy as np

def saveCameraCapture():
    cameraCapture = cv2.VideoCapture(0)
    fps = 30
    size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    videoWrite = cv2.VideoWriter('MyOutoutVid.avi',cv2.VideoWriter_fourcc('I','4','2','0'),fps,size)

    success,frame = cameraCapture.read()
    numFramesRemaing = 10 * fps - 1
    while success and numFramesRemaing >0 :
        videoWrite.write(frame)
        success,frame = cameraCapture.read()
        numFramesRemaing -= 1
    cameraCapture.release()

def showCameraCapture():
    clicked  = False
    def omMouse(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONUP:
            clicked = True
        pass
    cameraCapture = cv2.VideoCapture(0)
    cv2.namedWindow('CameraWindow')
    cv2.setMouseCallback('CameraWindow',omMouse);
    success,frame = cameraCapture.read()
    while success and cv2.waitKey(1) == -1 and not clicked:
        cv2.imshow('CameraWindow',frame)
        success,frame = cameraCapture.read()
    cv2.destroyWindow("CameraWindow")
    cameraCapture.release()
    pass

def showCameraCaptureAndSaveFrameImage():
    clicked  = False
    def omMouse(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONUP:
            clicked = True
        pass
    cameraCapture = cv2.VideoCapture(0)
    cv2.namedWindow('CameraWindow')
    cv2.setMouseCallback('CameraWindow',omMouse);
    success,frame = cameraCapture.read()
    time0 = int(time.time())
    while success and cv2.waitKey(1) == -1 and not clicked:
        cv2.imshow('CameraWindow',frame)
        success,frame = cameraCapture.read()
        time1 = int(time.time())
        if time1 - time0 > 2:
            time0 = int(time.time())
            cv2.imwrite('image/camera-'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+".jpg",frame)
    cv2.destroyWindow("CameraWindow")
    cameraCapture.release()
    pass

def showCameraCaptureAndFace():
    clicked  = False
    def omMouse(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONUP:
            clicked = True
        pass
    cameraCapture = cv2.VideoCapture(0)
    cv2.namedWindow('CameraWindow')
    cv2.setMouseCallback('CameraWindow',omMouse);
    success,frame = cameraCapture.read()
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')

    while success and cv2.waitKey(1) == -1 and not clicked:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,2)
        print(faces)
        for(x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imshow('CameraWindow',frame)
        success,frame = cameraCapture.read()
    cv2.destroyWindow("CameraWindow")
    cameraCapture.release()
    pass


def main():
    showCameraCaptureAndFace()
    pass

main()