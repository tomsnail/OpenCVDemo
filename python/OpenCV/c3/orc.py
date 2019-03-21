import cv2
import pytesseract
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
debug = 1

matplotlib.rcParams['font.family'] = 'SimHei'

def recognizeChineseText():
    src = cv2.imread('s6.jpg')
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    #src = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
    src = Image.fromarray(src)
    text = pytesseract.image_to_string(src,config = "-l chi_sim --oem 1 --psm 7")
    print(text)
    cv2.waitKey()

def recognizeChineseContext(src):
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        src = Image.fromarray(src)
        text = pytesseract.image_to_string(src, config = "-l chi_sim --oem 1 --psm 7")
        return text

def recognizeEnglishText():
    src = Image.open('s7.jpg')
    text = pytesseract.image_to_string(src)
    img = np.zeros((1000, 600, 3), np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (80, 90), font, 1, (255, 255, 255),1 )
    cv2.imshow('recognizeChineseText.jpg', img)
    cv2.waitKey()


def recognizeIDCardText(srcImg=None):
    if srcImg == None:
        srcImg = 's9.jpg';
    img = cv2.imread(srcImg)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('orc1_gray.jpg',gray)
    binary = cv2.Canny(gray, 100, 300, apertureSize=3, L2gradient=False);
    img1, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sp = img.shape
    roiArea = None
    for i in contours:
        retval = cv2.boundingRect(i)
        if retval[2] < sp[1] and retval[2] > sp[1] / 2:
            if round(retval[2] / retval[3], 1) == 1.6:
                roiArea = retval
    if roiArea == None :
        cv2.drawContours(img, contours, -1, (255, 0, 0), 2)
        cv2.imwrite('orc1_roiArea.jpg', img)
        if debug:
            f, axarr = plt.subplots(1, 2)
            axarr[0].imshow(cv2.imread(srcImg))
            axarr[1].imshow(cv2.imread("orc1_roiArea.jpg"))
            plt.show()
        return;
    else:
        _srcimg = cv2.imread(srcImg)
        cv2.drawContours(_srcimg, contours, -1, (255, 0, 0), 1)
        cv2.imwrite('orc1_roiArea.jpg', _srcimg)
    cropImg = img[roiArea[1]:roiArea[1]+roiArea[3], roiArea[0]: roiArea[0]+roiArea[2]]
    cv2.imwrite('orc1_cropImg1.jpg', cropImg)
    cropImg = cv2.resize(cropImg, (547, 342), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('orc1_cropImg2.jpg', cropImg)
    nameText = recognizeChineseContext(cropImg[40:80, 95: 300]);
    print(nameText)
    methods = [cv2.TM_CCOEFF_NORMED]
    tmpl = cv2.imread('card_template.png')
    cv2.imwrite('orc1_tmpl.jpg', tmpl)
    th, tw = tmpl.shape[:2]
    text = ""
    for md in methods:
        result = cv2.matchTemplate(cropImg, tmpl, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        cropImg = cropImg[tl[1]:tl[1]+40,tl[0]+130:tl[0]+130+330 ]
        cv2.imwrite('orc1_crop1.jpg', cropImg)
        rImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
        rImg = cv2.cvtColor(rImg, cv2.COLOR_GRAY2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
        rImg = Image.fromarray(rImg)
        text = pytesseract.image_to_string(rImg, lang='nums')
        print(text)
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        cv2.putText(img, text, (20, 90), font, 1, (255, 255, 255), 2,cv2.LINE_AA,False)
        cv2.imwrite('recognizeIDCardText.jpg', img)
    if debug:
        f, axarr = plt.subplots(2, 4)
        axarr[0, 0].imshow(cv2.imread(srcImg))
        axarr[0, 0].set_title("原始图片")
        axarr[0, 1].imshow(cv2.imread("orc1_gray.jpg"))
        axarr[0, 1].set_title("灰度图片")
        axarr[0, 2].imshow(cv2.imread("orc1_roiArea.jpg"))
        axarr[0, 2].set_title("轮廓图片")
        axarr[0, 3].imshow(cv2.imread("orc1_cropImg1.jpg"))
        axarr[0, 3].set_title("原始剪裁图片")
        axarr[1, 0].imshow(cv2.imread("orc1_cropImg2.jpg"))
        axarr[1, 0].set_title("RESIZE图片")
        axarr[1, 1].imshow(cv2.imread("orc1_tmpl.jpg"))
        axarr[1, 1].set_title("模板图片")
        axarr[1, 2].imshow(cv2.imread("orc1_crop1.jpg"))
        axarr[1, 2].set_title("目标区域剪裁图片")
        axarr[1, 3].imshow(cv2.imread("recognizeIDCardText.jpg"))
        axarr[1, 3].set_title(nameText+":"+text)
        plt.show()





def main():
    recognizeIDCardText('card.png')
    recognizeIDCardText('s5.jpg')
    recognizeIDCardText('s9.jpg')

main()