import cv2

img = cv2.imread('kk.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite("kk1.jpg", gray)