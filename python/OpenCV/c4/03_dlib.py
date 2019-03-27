# -*- coding: utf-8 -*-
import face_recognition
import cv2
from PIL import Image, ImageDraw
import numpy


def find_facial_features(path):
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(path)

    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)

    print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

    # Create a PIL imagedraw object so we can draw on the picture
    pil_image = Image.fromarray(image)
    frame = cv2.cvtColor(numpy.asarray(pil_image), cv2.COLOR_RGB2BGR)
    for face_landmarks in face_landmarks_list:

        # Print the location of each facial feature in this image
        for facial_feature in face_landmarks.keys():
            print("The {} in this face has the following points: {}".format(facial_feature,
                                                                            face_landmarks[facial_feature]))

        # Let's trace out each facial feature in the image with a line!
        for facial_feature in face_landmarks.keys():
            #d.line(face_landmarks[facial_feature], width=5)
            print(facial_feature)
            for i in range(len(face_landmarks[facial_feature])):
                cv2.circle(frame, face_landmarks[facial_feature][i], 0, (55, 255, 155), 5)



    cv2.imshow('find_facial_features', frame)
    cv2.waitKey()

find_facial_features("./image/liuwei.jpg")