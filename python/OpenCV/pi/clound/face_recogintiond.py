# -*- coding:utf-8 -*-

import face_recognition
import cv2
import dlib

yangsong_face_encoding = None

def face_init():
    global yangsong_face_encoding
    yangsong_img = face_recognition.load_image_file('./images/camera-20190325103711.jpg')
    yangsong_face_encoding = face_recognition.face_encodings(yangsong_img)[0]
    print("face_init ok")




def face_recognitiond(filename=None):
    if filename is None:
        print("filename is None")
        return
    img = cv2.imread(filename)
    process_this_frame = True
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    if process_this_frame:
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([yangsong_face_encoding], face_encoding)
            if match[0]:
                print(filename+">>>>>>>>>>>>>>>>this is yangsong")
            else:
                print(filename+">>>>>>>>>>>>>>>>this is unknown")
    pass


if __name__ == "__main__":
    face_init()