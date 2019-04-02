import cv2
import time
import threading
import json
import urllib
import urllib2
#import requests
import pickle
import base64
import os

server_url = "http://192.168.169.35:8000/image"

def piCameraCaptureFaceDectorWithImage():
    cameraCapture = cv2.VideoCapture(0)
    fps = 20
    #size = (640,480)
    size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))) 
    print(size)
    videoWrite = cv2.VideoWriter('./camera_datas/camera_data.avi', cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)
    success, frame = cameraCapture.read()
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
    count = 1
    while success and cv2.waitKey(10) != -1  :
	print(time.time())
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
	flag = False
        if faces is not None and len(faces) > 0:
            flag = True
        elif eyes is not None and len(eyes) > 0:
            flag = True
        if flag:
            filename = 'camera-' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".jpg"
            
            file_path = './unusual/' + filename
            for(x,y,w,h) in faces:
	        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
            cv2.imwrite(file_path, frame)
	    with open(file_path, 'rb') as fileObj:
                image_data = fileObj.read()
                content = base64.b64encode(image_data)
                params = {"content": content, "filename": filename}
                print(post(server_url, params))
        #frame = cv2.flip(frame, 0)
        #if count % 5 == 0 :
        videoWrite.write(frame)
        count += 1
        success, frame = cameraCapture.read()
    cameraCapture.release()

def post(server_url, params):
    print(server_url)
    #pass
    data = urllib.urlencode(params)
    request = urllib2.Request(server_url, data)
    return json.loads(urllib2.urlopen(request, timeout=10).read())

class PostUnusualThread(threading.Thread):
    def __init__(self,arg):
        super(PostUnusualThread, self).__init__()
        self.arg = arg
    def run(self):
        face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
        count = self.arg
        while True :
            #time.sleep(1)
            filename = 'camera-' + str(count) + ".jpg"
            file_path = './unusual/' + filename
            frame = cv2.imread(file_path)
            if frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 3)
                eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
                flag = False
                #filename = ""
                if faces is not None and len(faces) > 0:
                    flag = True
                elif eyes is not None and len(eyes) > 0:
                    flag = True
                if flag:
                    with open(file_path, 'rb') as fileObj:
                        image_data = fileObj.read()
                        content = base64.b64encode(image_data)
                        params = {"content": content, "filename": filename}
                        print(post(server_url, params))
                os.remove(file_path)
            count = count + 2
            #print(count)




def main():
    piCameraCaptureFaceDectorWithImage()
    pass

main()
