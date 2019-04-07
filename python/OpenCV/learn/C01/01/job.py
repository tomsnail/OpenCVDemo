
import cv2
import numpy as np

def job_1(imagepath,y=10,x=20,h=40,w=60,step=4):

    img = cv2.imread(imagepath)


    new_img = img[y:y+h,x:x+w]

    cw = 0
    pre_img = None
    for _w in range(0,w-step,step):
        for _h in range(0,h-step,step):
            pre_img = new_img[_h,_w]
            for i in range(step):
                for j in range(step):
                    new_img[_h+j,_w+i] = pre_img
    img[y:y+h,x:x+w] = new_img
    cv2.imshow("job_1",img)
    pass

def job_2(imagepath):
    img = cv2.imread(imagepath,cv2.IMREAD_GRAYSCALE)
    (h,w) = img.shape
    img_new = np.zeros([img.shape[0]-2,img.shape[1]-2])
    laplacien = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])

    for x in range(1,h-2,1):
        for y in range(1,w-2,1):
            v = img[x-1,y-1]*laplacien[0,0]+img[x-1,y]*laplacien[0,1]+img[x-1,y+1]*laplacien[0,2] \
            +img[x, y - 1] * laplacien[1, 0] + img[x, y] * laplacien[1, 1] + img[x, y +1] * laplacien[1, 2] \
            +img[x+1,y-1]*laplacien[2,0]+img[x+1,y]*laplacien[2,1]+img[x+1,y+1]*laplacien[2,2]
            if v < 0 :
                v = 0
            if v > 255:
                v = 255
            img_new[x,y] = v
    print(img_new)
    cv2.imshow("job_2", img_new)
    pass




if __name__ == '__main__':
    job_1("images/1.jpg")
    job_2("images/1.jpg")
    cv2.waitKey()
