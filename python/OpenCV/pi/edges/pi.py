import cv2
import time
import threading
import json
import urllib
import urllib2
import requests
import pickle
import base64

server_url = "http://192.168.169.35:8000/image"
face_cascade = None
eye_cascade = None
def piCameraCaptureFaceDectorWithImage():
    work = True
    cameraCapture = cv2.VideoCapture(0)
    fps = 20
    size = (640,320)
    global eye_cascade
    global face_cascade
    videoWrite = cv2.VideoWriter('./camera_datas/camera_data.avi', cv2.cv.CV_FOURCC(*'XVID'), fps, size)
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
    success, frame = cameraCapture.read()
    count = 1
    while success and work :
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
        flag = False
        filename = ""
        if faces is not None and len(faces) > 0:
            unusual = frame.copy()
            filename = 'camera-' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".jpg"
            cv2.imwrite('./unusual/' + filename, unusual)
            flag = True
        elif eyes is not None and len(eyes) > 0:
            unusual = frame.copy()
            filename = 'camera-' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".jpg"
            cv2.imwrite('./unusual/' + filename, unusual)
            flag = True
        if flag:
            t = PostUnusualThread(filename)
            t.start()
        count += 1
        if count % 5 == 0 :
            videoWrite.write(frame)
        cv2.waitKey(50)
        success, frame = cameraCapture.read()
    cameraCapture.release()

def post(server_url, params):
    data = urllib.urlencode(params)
    request = urllib2.Request(server_url, data)
    return json.loads(urllib2.urlopen(request, timeout=10).read())

class PostUnusualThread(threading.Thread):
    def __init__(self,arg):
        super(PostUnusualThread, self).__init__()
        self.arg=arg
    def run(self):
        with open('./unusual/' + self.arg, 'rb') as fileObj:
            image_data = fileObj.read()
            content = base64.b64encode(image_data)
            params = {"content": content, "filename": self.arg}
            print(post(server_url, params))




def main():
    piCameraCaptureFaceDectorWithImage()
    pass

main()
