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


def showCameraCaptureAndFilterFace():
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
        for(x,y,w,h) in faces:
            # face_frame = gray[y:y+h,x:x+w]
            # face_frame0 = frame[y:y + h, x:x + w]
            # binary = cv2.Canny(face_frame, 50, 150, apertureSize=3, L2gradient=False);
            # imp,contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(face_frame0, contours, -1, (255, 0, 0), 1)
            #for i in contours:
                #roiArea = cv2.boundingRect(i)
                #cropImg = face_frame0[roiArea[1]:roiArea[1] + roiArea[3], roiArea[0]: roiArea[0] + roiArea[2]]
                #cropImg = cv2.bilateralFilter(cropImg, 0,150,15)
                #cropImg = cv2.GaussianBlur(cropImg, (15, 15), 0)
                #face_frame0[roiArea[1]:roiArea[1] + roiArea[3], roiArea[0]: roiArea[0] + roiArea[2]] = cropImg
            # frame[y:y + h, x:x + w] = face_frame0
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
        cv2.imshow('CameraWindow',frame)
        success,frame = cameraCapture.read()
    cv2.destroyWindow("CameraWindow")
    cameraCapture.release()
    pass

def main():
    showCameraCaptureAndFilterFace()
    pass

main()