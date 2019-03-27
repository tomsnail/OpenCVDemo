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
    d = ImageDraw.Draw(pil_image)

    for face_landmarks in face_landmarks_list:

        # Print the location of each facial feature in this image
        for facial_feature in face_landmarks.keys():
            print("The {} in this face has the following points: {}".format(facial_feature,
                                                                            face_landmarks[facial_feature]))

        # Let's trace out each facial feature in the image with a line!
        for facial_feature in face_landmarks.keys():
            d.line(face_landmarks[facial_feature], width=5)

    frame = cv2.cvtColor(numpy.asarray(pil_image), cv2.COLOR_RGB2BGR)
    cv2.imshow('find_facial_features', frame)
    cv2.waitKey()

def video_face_detector(makeup=False,blur=False):
    video_capture = cv2.VideoCapture(0)

    obama_img = face_recognition.load_image_file('./image/5.jpg')
    obama_face_encoding = face_recognition.face_encodings(obama_img)[0]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        if process_this_frame:
            face_locations = face_recognition.face_locations(small_frame)
            #face_locations = face_recognition.face_locations(small_frame,  model="cnn")

            face_encodings = face_recognition.face_encodings(small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                match = face_recognition.compare_faces([obama_face_encoding], face_encoding)

                if match[0]:
                    name = "yangsong"
                else:
                    name = "unknown"

                face_names.append(name)

        process_this_frame = not process_this_frame
        pil_image = None
        if makeup :
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_landmarks_list = face_recognition.face_landmarks(image)
            for face_landmarks in face_landmarks_list:
                pil_image = Image.fromarray(image)
                d = ImageDraw.Draw(pil_image, 'RGBA')

                # Make the eyebrows into a nightmare
                d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
                d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
                d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
                d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

                # Gloss the lips
                d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
                d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
                d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
                d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

                # Sparkle the eyes
                d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
                d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

                # Apply some eyeliner
                d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
                d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

        if pil_image is not None :
            frame = cv2.cvtColor(numpy.asarray(pil_image),cv2.COLOR_RGB2BGR)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4


            if blur:
                face_image = frame[top:bottom, left:right]
                face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
                frame[top:bottom, left:right] = face_image
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def main():
    #find_facial_features("./image/5.jpg")
    #find_facial_features("./image/liuwei.jpg")
    video_face_detector()
    pass

main()