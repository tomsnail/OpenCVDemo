import cv2



import pickle
import face_recognition


model_path = "./knn_resource/model/trained_knn_model.clf"
knn_clf = None
with open(model_path, 'rb') as f:
    knn_clf = pickle.load(f)
    print(knn_clf)


def predict(frame,distance_threshold=0.5):

    # Load a trained KNN model (if one was passed in)

    # Load image file and find face locations
    X_face_locations = face_recognition.face_locations(frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    global knn_clf
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def face_rec():
    camera = cv2.VideoCapture(0)
    while cv2.waitKey(30) & 0xff != 27 and  True:
        read,frame = camera.read()
        predictions = predict(frame)
        for name, (top, right, bottom, left) in predictions:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imshow("camera",frame)
    camera.release()
    cv2.destroyAllWindows()


def main():
    face_rec()

if __name__ == '__main__':
    main()
    pass