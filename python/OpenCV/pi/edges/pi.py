import cv2
import time
import threading
import json
#import urllib
#import urllib2
#import requests
import pickle
import base64
import os

server_url = "http://192.168.169.35:8000/image"

def piCameraCaptureFaceDectorWithImage():
    cameraCapture = cv2.VideoCapture(0)
    fps = 20
    size = (640,320)
    videoWrite = cv2.VideoWriter('./camera_datas/camera_data.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    success, frame = cameraCapture.read()
    t = PostUnusualThread(int(time.time()))
    t.start()
    temp_file_name = ""
    count = 1
    while success and cv2.waitKey(10) == -1  :
        filename = 'camera-' + str(int(time.time())) + ".jpg"
        if filename != temp_file_name :
            file_path = './unusual/' + filename
            cv2.imwrite(file_path,frame);
        count += 1
        frame = cv2.flip(frame, 0)
        videoWrite.write(frame)
        success, frame = cameraCapture.read()
    cameraCapture.release()

def post(server_url, params):
    print(server_url)
    pass
    #data = urllib.urlencode(params)
    # request = urllib2.Request(server_url, data)
    # return json.loads(urllib2.urlopen(request, timeout=10).read())

class PostUnusualThread(threading.Thread):
    def __init__(self,arg):
        super(PostUnusualThread, self).__init__()
        self.arg = arg
    def run(self):
        face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
        count = self.arg
        while True :
            time.sleep(1)
            filename = 'camera-' + str(count) + ".jpg"
            file_path = './unusual/' + filename
            frame = cv2.imread(file_path)
            if frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 3)
                eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
                flag = False
                filename = ""
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
            count += 1




def main():
    piCameraCaptureFaceDectorWithImage()
    pass

main()
