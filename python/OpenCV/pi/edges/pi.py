import cv2
import time
import threading
import json
import urllib
import urllib2
import requests
import pickle


server_url = "http://192.168.169.53:8000/image"


def piCameraCaptureFaceDectorWithImage():
    work = True
    cameraCapture = cv2.VideoCapture(0)
    fps = 20
    size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    videoWrite = cv2.VideoWriter('./camera_datas/camera_data.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye_tree_eyeglasses.xml')
    success, frame = cameraCapture.read()
    count = 1
    while success and work :
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 3)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 3)
        if faces is not None and len(faces) > 0 :
            unusual = frame.copy()
            filename = 'camera-' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".jpg"
            cv2.imwrite('./unusual/' + filename, unusual)
            t = PostUnusualThread(filename)
            t.start()
        elif eyes is not None and len(eyes) > 0 :
            unusual = frame.copy()
            filename = 'camera-' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".jpg"
            cv2.imwrite('./unusual/'+filename, unusual)
            t = PostUnusualThread(filename)
            t.start()
        count += 1
        if count % 5 == 0 :
            videoWrite.write(frame)
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
        r_file = open('/unusual/'+self.arg, "rb")
        content = pickle.dumps(r_file.read())
        params = {"content": content,"filename":self.arg}
        print(post(server_url, params))


def main():
    piCameraCaptureFaceDectorWithImage()
    pass

main()