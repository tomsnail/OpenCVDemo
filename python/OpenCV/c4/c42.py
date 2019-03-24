import cv2
import time
import numpy as np
import os
import sys


def generate():
    clicked = False

    def omMouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            clicked = True
        pass

    cv2.setMouseCallback('CameraWindow', omMouse);
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml')
    camera = cv2.VideoCapture(0)
    count = 0
    while cv2.waitKey(1) == -1 and not clicked:
        ret,frame = camera.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for (x, y, w, h) in faces:
            f = cv2.resize(gray[y:y+h,x:x+w],(200,200))
            cv2.imwrite('./datasets/%s.pgm'%str(count),f)
            count+=1
            if count > 100:
                clicked = True
                break
        cv2.imshow("CameraWindow",frame)

    camera.release()
    cv2.destroyAllWindows()

def read_image(path,sz=None):
    c=0
    X,y = [],[]
    for dirname,dirnames,filenames in os.walk(path):
        for filename in filenames:
            try:
                if filename == ".directory":
                    continue
                real_path = path+"/"+filename
                print(real_path)
                im = cv2.imread(real_path, cv2.IMREAD_GRAYSCALE)
                if sz is not None:
                    im = cv2.resize(im, (200, 200))
                    X.append(np.asanyarray(im, dtype=np.uint8))
                    y.append(c)
            except IOError:
                print("I/O error()")
            except:
                print("Unexpeted error:", sys.exc_info()[0])
                raise
        c = c + 1

    return [X,y]

def face_rec(path):
    clicked = False

    def omMouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            clicked = True
        pass

    cv2.setMouseCallback('CameraWindow', omMouse);

    [X,y] = read_image(path,1)
    y = np.asarray(y,dtype=np.int32)
    #model = cv2.face.EigenFaceRecognizer_create()
    model = cv2.face.LBPHFaceRecognizer_create()
    #model = cv2.face.FisherFaceRecognizer_create();
    model.train(np.asarray(X),np.asarray(y))
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    while cv2.waitKey(1) == -1 and not clicked:
        read,img = camera.read()
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            roi = gray[x:x+w,y:y+h]
            try:
                roi = cv2.resize(roi,(200,200),interpolation=cv2.INTER_LINEAR)
                params = model.predict(roi)
                print(params)
                s = params[1]
                if s < 50:
                    cv2.putText(img,'yangsong',(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
            except:
                print("error")
                continue
        cv2.imshow("camera",img)
    cv2.destroyAllWindows()


def main():
    #generate()
    face_rec('./datasets')
    pass


main()