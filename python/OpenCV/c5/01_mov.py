import cv2
import numpy as np

def mov(show=False,save=False):
    bs = cv2.createBackgroundSubtractorKNN(detectShadows = True)
    camera = cv2.VideoCapture(0)
    out = None
    if save :
        size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        out = cv2.VideoWriter('./resource/mov_output.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), 20.0, size)
    while True:
      ret, frame = camera.read()
      fgmask = bs.apply(frame)
      th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
      th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 2)
      dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,3)), iterations = 2)
      image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      for c in contours:
        if cv2.contourArea(c) > 1000:
          (x,y,w,h) = cv2.boundingRect(c)
          cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
      if show :
          cv2.imshow("mog", fgmask)
          cv2.imshow("thresh", th)
          cv2.imshow("diff", frame & cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR))
      cv2.imshow("detection", frame)
      if save:
        out.write(frame)
      k = cv2.waitKey(30) & 0xff
      if k == 27:
          break
    if save:
        out.release()
    camera.release()
    cv2.destroyAllWindows()

mov()