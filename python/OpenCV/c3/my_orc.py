import cv2
import pytesseract
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
debug = 1

matplotlib.rcParams['font.family'] = 'SimHei'



def morphologyEx(img,type):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    if type == 1 :
        dst = cv2.morphologyEx(img,cv2.MORPH_DILATE,kernel)
    if type == 2 :
        dst = cv2.morphologyEx(img,cv2.MORPH_ERODE,kernel)
    if type == 3 :
        dst = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
    if type == 4 :
        dst = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
    if type == 5 :
        dst = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)
    if type == 6 :
        dst = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)
    if type == 7 :
        dst = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)
    return dst


def threshold(img,type):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if type == 1:
        retval, dst = cv2.threshold(gray,60,255,cv2.THRESH_BINARY)
    if type == 2:
        retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    if type == 3:
        retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    if type == 4:
        retval, dst = cv2.threshold(gray, 60, 255, cv2.THRESH_TOZERO)
    if type == 5:
        retval, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO_INV)
    if type == 6:
        dst = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 15,10)
    if type == 41:
        retval, dst = cv2.threshold(gray, 0,255, cv2.THRESH_TOZERO | cv2.THRESH_TRIANGLE)
    return dst;

def recognizePreIDCardText(srcImg=None):
    if srcImg == None:
        srcImg = 's9.jpg'
    img = cv2.imread(srcImg)
    preImg = cv2.GaussianBlur(img, (15, 15), 0)
    cv2.imwrite('orc2_preScharr.jpg', preImg)

    preImgx = cv2.Scharr(preImg,cv2.CV_32F,1,0)
    preImgx = cv2.convertScaleAbs(preImgx)
    preImgy = cv2.Scharr(preImg, cv2.CV_32F, 0, 1)
    preImgy = cv2.convertScaleAbs(preImgy)
    preImg = cv2.addWeighted(preImgx,0.5,preImgy,0.5,30)
    preImg = cv2.GaussianBlur(preImg, (15, 15), 0)
    cv2.imwrite('orc2_preThreshold.jpg', preImg)

    preImg = morphologyEx(preImg, 2)
    preImg = cv2.GaussianBlur(preImg, (15, 15), 0)
    preImg =threshold(preImg,41)
    cv2.imwrite('orc2_preCannyImg.jpg', preImg)

    binary = cv2.Canny(preImg, 50, 150, apertureSize=3, L2gradient=False);
    imp1,contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sp = img.shape
    roiArea = None
    for i in contours:
        retval = cv2.boundingRect(i)
        if retval[2] < sp[1] and retval[2] > sp[1] / 2:
            if round(retval[2] / retval[3], 1) == 1.6:
                roiArea = retval
    if roiArea == None:
        cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
        cv2.imwrite('orc2_roiArea.jpg', img)
        if debug:
            f, axarr = plt.subplots(2, 3)
            axarr[0,0].imshow(cv2.imread(srcImg))
            axarr[0,0].set_title("原始图片")
            axarr[0,1].imshow(cv2.imread("orc2_preScharr.jpg"))
            axarr[0,1].set_title("高斯模糊图片")
            axarr[0,2].imshow(cv2.imread("orc2_preThreshold.jpg"))
            axarr[0,2].set_title("Scharr算子图片")
            axarr[1,0].imshow(cv2.imread("orc2_preCannyImg.jpg"))
            axarr[1,0].set_title("阈值取零图片")
            axarr[1,1].imshow(cv2.imread("orc2_roiArea.jpg"))
            axarr[1,1].set_title("轮廓分析后图片")
            plt.show()
        return;
    else:
        _srcimg = cv2.imread(srcImg)
        cv2.drawContours(_srcimg, contours, -1, (255, 0, 0), 1)
        cv2.imwrite('orc2_roiArea.jpg', _srcimg)

    cropImg = img[roiArea[1]:roiArea[1] + roiArea[3], roiArea[0]: roiArea[0] + roiArea[2]]
    cropImg = cv2.resize(cropImg, (547, 342), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('orc2_cropImg.jpg', cropImg)
    methods = [cv2.TM_CCOEFF_NORMED]
    tmpl = cv2.imread('card_template.png')
    th, tw = tmpl.shape[:2]
    for md in methods:
        result = cv2.matchTemplate(cropImg, tmpl, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        cropImg = cropImg[tl[1]:tl[1] + 40, tl[0] + 130:tl[0] + 130 + 330]
        cv2.imwrite('orc2_crop.jpg', cropImg)
        rImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
        rImg = Image.fromarray(rImg)
        text = pytesseract.image_to_string(rImg,config = "-l nums --oem 1 --psm 7")
        print(text)
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        cv2.putText(img, text, (20, 90), font, 1, (255, 255, 255), 2, cv2.LINE_AA, False)
        cv2.imwrite('recognizeIDCardText.jpg', img)
    if debug:
        f, axarr = plt.subplots(2, 4)
        axarr[0, 0].imshow(cv2.imread(srcImg))
        axarr[0, 0].set_title("原始图片")
        axarr[0, 1].imshow(cv2.imread("orc2_preScharr.jpg"))
        axarr[0, 1].set_title("高斯模糊图片")
        axarr[0, 2].imshow(cv2.imread("orc2_preThreshold.jpg"))
        axarr[0, 2].set_title("Scharr算子图片")
        axarr[0, 3].imshow(cv2.imread("orc2_preCannyImg.jpg"))
        axarr[0, 3].set_title("阈值取零图片")
        axarr[1, 0].imshow(cv2.imread("orc2_roiArea.jpg"))
        axarr[1, 0].set_title("轮廓分析后图片")
        axarr[1, 1].imshow(cv2.imread("orc2_cropImg.jpg"))
        axarr[1, 1].set_title("RESIZE图片")
        axarr[1, 2].imshow(cv2.imread("orc2_crop.jpg"))
        axarr[1, 2].set_title("目标剪裁图片")
        axarr[1, 3].imshow(cv2.imread("recognizeIDCardText.jpg"))
        axarr[1, 3].set_title( text)
        plt.show()



def main():
    recognizePreIDCardText('card.png')
    recognizePreIDCardText('s5.jpg')
    recognizePreIDCardText('s9.jpg')
    # recognizePreIDCardText('timg.jpg')
    # recognizePreIDCardText('timg1.jpg')
    # recognizePreIDCardText('timg2.jpg')

main()