import cv2


img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray);
binary = cv2.Canny(gray,  50, 200,apertureSize=3,L2gradient=False);
img1, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,(0,0,255),3)

cv2.imwrite("t.jpg", img)
