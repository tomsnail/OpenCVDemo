# -*- coding:utf-8 -*-

from tornado.web import Application, RequestHandler
from tornado.escape import json_decode
from tornado.escape import json_encode
from tornado.ioloop import IOLoop
import base64
import traceback
import threading

import face_recogintiond as fr


class IndexHandler(RequestHandler):

    def get(self):
        self.write("hello")

class ImageHandler(RequestHandler):

    def get(self):
        fr.face_recognitiond("G:/02_workspace/33_git_open/OpenCVDemo/python/OpenCV/c2/s3.jpg")#
        self.write("image service ok")


    # def post(self):
    #     data=json_decode(self.request.body)
    #     img = data["img_data"]

    def post(self):
        result = {}
        content = self.get_argument("content", default=None)
        filename = self.get_argument("filename", default=None)
        if content is None:
            result["msg"] = "no image content"
        else:
            content = self.get_argument("content", default=None)
            result["msg"] = self.content_process(content,filename)
        self.write(json_encode(result))

    def content_process(self, image_content,filename):
        try:
            ori_image_data = base64.b64decode(image_content)
            fout = open("./unusual/"+filename, 'wb')
            fout.write(ori_image_data)
            fout.close()
            t = FaceThread("./unusual/"+filename)
            t.start()
            return "ok"
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            return str(e)



class FaceThread(threading.Thread):
    def __init__(self,arg):
        super(FaceThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.arg=arg
    def run(self):
        print(self.arg)
        fr.face_recognitiond(self.arg)

if __name__ == "__main__":
    fr.face_init()
    app = Application([
        (r"/", IndexHandler),
        (r"/image", ImageHandler)])

    app.listen(8000)

    IOLoop.current().start()
