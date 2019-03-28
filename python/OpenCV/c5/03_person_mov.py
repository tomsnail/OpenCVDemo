#! /usr/bin/python

"""Surveillance Demo: Tracking Pedestrians in Camera Feed

The application opens a video (could be a camera or a video file)
and tracks pedestrians in the video.
"""
__author__ = "joe minichino"
__copyright__ = "property of mankind."
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Joe Minichino"
__email__ = "joe.minichino@gmail.com"
__status__ = "Development"

import cv2
import numpy as np
import os.path as path
import argparse
import pickle
import face_recognition


names = {'yangsong': 0, 'liuwei': 0, 'yangda': 0}

model_path = "./../c4/knn_resource/model/trained_knn_model.clf"
knn_clf = None
with open(model_path, 'rb') as f:
    knn_clf = pickle.load(f)
    print(knn_clf)


def predict(frame,distance_threshold=0.6):

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

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--algorithm",
    help = "m (or nothing) for meanShift and c for camshift")
args = vars(parser.parse_args())

def center(points):
    """calculates centroid of a given matrix"""
    x = (points[0][0] + points[1][0] + points[2][0] + points[3][0]) / 4
    y = (points[0][1] + points[1][1] + points[2][1] + points[3][1]) / 4
    return np.array([np.float32(x), np.float32(y)], np.float32)

font = cv2.FONT_HERSHEY_SIMPLEX

class Pedestrian():
  """Pedestrian class

  each pedestrian is composed of a ROI, an ID and a Kalman filter
  so we create a Pedestrian class to hold the object state
  """
  def __init__(self, id,name, frame, track_window):
    """init the pedestrian object with track window coordinates"""
    # set up the roi
    self.id = int(id)
    self.name = name
    x,y,w,h = track_window
    self.track_window = track_window
    self.roi = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([self.roi], [0], None, [16], [0, 180])
    self.roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # set up the kalman
    self.kalman = cv2.KalmanFilter(4,2)
    self.kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
    self.kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
    self.kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03
    self.measurement = np.array((2,1), np.float32) 
    self.prediction = np.zeros((2,1), np.float32)
    self.term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
    self.center = None
    self.update(frame)
    
  def __del__(self):
    print ("Pedestrian %s destroyed" % self.name)

  def update(self, frame):
    # print "updating %d " % self.id
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    back_project = cv2.calcBackProject([hsv],[0], self.roi_hist,[0,180],1)
    
    if args.get("algorithm") == "c":
      ret, self.track_window = cv2.CamShift(back_project, self.track_window, self.term_crit)
      pts = cv2.boxPoints(ret)
      pts = np.int0(pts)
      self.center = center(pts)
      cv2.polylines(frame,[pts],True, 255,1)
      
    if not args.get("algorithm") or args.get("algorithm") == "m":
      ret, self.track_window = cv2.meanShift(back_project, self.track_window, self.term_crit)
      x,y,w,h = self.track_window
      self.center = center([[x,y],[x+w, y],[x,y+h],[x+w, y+h]])  
      cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
      font = cv2.FONT_HERSHEY_DUPLEX
      cv2.putText(frame, self.name, (x + 30, y + 30), font, 1.0, (0, 0, 255), 1)

    self.kalman.correct(self.center)
    prediction = self.kalman.predict()
    cv2.circle(frame, (int(prediction[0]), int(prediction[1])), 4, (255, 0, 0), -1)
    # fake shadow
    cv2.putText(frame, "ID: %s -> %s" % (self.name, self.center), (11, (self.id + 1) * 25 + 1),
        font, 0.6,
        (0, 0, 0),
        1,
        cv2.LINE_AA)
    # actual info
    cv2.putText(frame, "ID: %s -> %s" % (self.name, self.center), (10, (self.id + 1) * 25),
        font, 0.6,
        (0, 255, 0),
        1,
        cv2.LINE_AA)

def main(type=1,save=False,face=False):
  camera = None
  if type == 0:
    camera = video_capture = cv2.VideoCapture(0)
  else:
    camera = cv2.VideoCapture(path.join(path.dirname(__file__), "./resource/768x576.avi"))
    save = False

  # camera = cv2.VideoCapture(path.join(path.dirname(__file__), "traffic.flv"))

  # camera = cv2.VideoCapture(path.join(path.dirname(__file__), "..", "movie.mpg"))
  # camera = cv2.VideoCapture(0)
  history = 20
  # KNN background subtractor
  bs = cv2.createBackgroundSubtractorKNN()

  # MOG subtractor
  # bs = cv2.bgsegm.createBackgroundSubtractorMOG(history = history)
  # bs.setHistory(history)

  # GMG
  # bs = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames = history)
  
  cv2.namedWindow("surveillance")
  pedestrians = {}
  frames = 0
  if save :
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter('./resource/person_output1.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), 10.0, size)
  counter = 0
  while True:
    print(" -------------------- FRAME %d --------------------" % frames)
    grabbed, frame = camera.read()
    if (grabbed is False):
      print("failed to grab frame.")
      break

    fgmask = bs.apply(frame)

    # this is just to let the background subtractor build a bit of history
    if frames < history:
      frames += 1
      continue


    th = cv2.threshold(fgmask.copy(), 127, 255, cv2.THRESH_BINARY)[1]
    th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 2)
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,3)), iterations = 2)
    image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for c in contours:
      if cv2.contourArea(c) > 500:
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 1)
        # only create pedestrians in the first frame, then just follow the ones you have
        person_name = str(counter)
        if face :
            face_frame = frame[y:y+h,x:x+w]
            face_locations = face_recognition.face_locations(face_frame)
            if face_locations is not None and len(face_locations) > 0 :
                predictions = predict(face_frame)
                for name, (top, right, bottom, left) in predictions:
                    person_name = name
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (x+30,y+30), font, 1.0, (0, 255, 0), 1)
        if names.get(person_name) is not None and names[person_name] == 0:
            names[person_name] = 1
            pedestrians[counter] = Pedestrian(counter,person_name, frame, (x,y,w,h))
            counter += 1


    for i, p in pedestrians.items():
      p.update(frame)

    frames += 1

    cv2.imshow("surveillance", frame)
    if save:
      out.write(frame)
    if cv2.waitKey(110) & 0xff == 27:
        break
  if save:
    out.release()
  camera.release()

if __name__ == "__main__":
  main(0,save=True,face=True)
