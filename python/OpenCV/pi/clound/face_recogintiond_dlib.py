# -*- coding:utf-8 -*-

import face_recognition
import cv2
import dlib

_face_encodings = ['','']

persons = ['./images/camera-20190325103711.jpg','./images/liuwei.jpg']

names = ['yangsong','liuwei']

def face_init():
    global _face_encodings
    for i in range(len(persons)):
        face_img = face_recognition.load_image_file(persons[i])
        _face_encodings[i] = face_recognition.face_encodings(face_img)[0]

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
            isKonw = False
            match = face_recognition.compare_faces(_face_encodings, face_encoding)
            for i in range(len(names)):
                if match[i] :
                    print(filename + ">>>>>>>>>>>>>>>>this is " + names[i])
                    isKonw = True
                    break

            if isKonw :
                pass
            else:
                print(filename+">>>>>>>>>>>>>>>>this is unknown")
    pass


if __name__ == "__main__":
    face_init()