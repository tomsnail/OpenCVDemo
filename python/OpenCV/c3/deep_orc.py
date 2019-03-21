import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from PIL import Image
debug = 1
matplotlib.rcParams['font.family'] = 'SimHei'

def grayImg(img):
    # 转化为灰度图
    gray = cv2.resize(img, (img.shape[1] * 3, img.shape[0] * 3), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    #otsu二值化操作
    retval, gray = cv2.threshold(gray, 120, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    return gray
def preprocess(gray):
    #二值化操作，但与前面grayimg二值化操作中不一样的是要膨胀选定区域所以是反向二值化
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    ele = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 10))
    #膨胀操作
    dilation = cv2.dilate(binary, ele, iterations=1)
    cv2.imwrite("do_binary.png", binary)
    cv2.imwrite("do_dilation.png", dilation)
    return dilation
def findTextRegion(img):
    region = []
    # 1. 查找轮廓
    image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 2. 筛选那些面积小的
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)
        # 面积小的都筛选掉
        if (area < 300):
            continue
        # 轮廓近似，作用很小
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)

        #函数 cv2.minAreaRect() 返回一个Box2D结构 rect：（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）。
        if debug:
            print("rect is: ", rect)
        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选那些太细的矩形，留下扁的
        if (height > width * 1.2):
            continue
        # 太扁的也不要
        if (height * 18 < width):
            continue
        if (width > img.shape[1] / 2 and height > img.shape[0] / 20):
            region.append(box)
    return region


def findTextRegion1(img):
    region = []
    # 1. 查找轮廓
    sp = img.shape
    image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 2. 筛选那些面积小的
    for i in range(len(contours)):
        cnt = contours[i]


        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)
        # 面积小的都筛选掉
        # if (area < 300):
        #     continue
        # 轮廓近似，作用很小
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        print(rect)
        print(round(rect[1][0] / rect[1][1], 1))
        if rect[1][0] < sp[1] and rect[1][0] > sp[1] / 2:
            if round(rect[1][0] / rect[1][1], 1) == 1.5:
                pass
            else:
                continue
        else:
            continue
        #函数 cv2.minAreaRect() 返回一个Box2D结构 rect：（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）。
        if debug:
            print("rect is: ", rect)
        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选那些太细的矩形，留下扁的
        if (height > width * 1.2):
            continue
        # 太扁的也不要
        if (height * 18 < width):
            continue
        if (width > img.shape[1] / 2 and height > img.shape[0] / 20):
            region.append(box)
    return region

def detect(img):
    # fastNlMeansDenoisingColored(InputArray src, OutputArray dst, float h=3, float hColor=3, int templateWindowSize=7, int searchWindowSize=21 )
    gray = cv2.fastNlMeansDenoisingColored(img, None, 10, 3, 3, 3)
    #gray = cv2.GaussianBlur(img, (3, 3), 0)
    #cv2.fastNlMeansDenoisingColored作用为去噪
    if debug:
        cv2.imwrite("do_fastNlMeansDenoisingColored.png", gray)
    coefficients = [0, 1, 1]
    m = np.array(coefficients).reshape((1, 3))
    gray = cv2.transform(gray, m)
    if debug:
        cv2.imwrite("do_gray.png", gray)
    # 2. 形态学变换的预处理，得到可以查找矩形的图片
    dilation = preprocess(gray)

    # 3. 查找和筛选文字区域
    region = findTextRegion(dilation)
    # 4. 用绿线画出这些找到的轮廓
    for box in region:
        h = abs(box[0][1] - box[2][1])
        w = abs(box[0][0] - box[2][0])
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        y1 = min(Ys)

        if w > 0 and h > 0 and x1 < gray.shape[1] / 2:
            print(w /h)
            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
            idImg = grayImg(img[y1:y1 + h, x1:x1 + w])
            cv2.imwrite("do_idImg.png", idImg)
            cv2.imwrite("do_contours.png", img)
            return idImg

def ocrIdCard(imgPath):
    img0 = cv2.imread(imgPath, cv2.IMREAD_COLOR)
    img = cv2.resize(img0, (428, 270), interpolation=cv2.INTER_CUBIC)
    idImg = detect(img)
    result = ""
    image = Image.fromarray(idImg)
    result = pytesseract.image_to_string(image, lang='nums')
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    cv2.putText(img0, result, (20, 90), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA, False)
    cv2.imwrite('do_recognizeIDCardText.jpg', img0)

    if debug:
        f, axarr = plt.subplots(2, 4)
        axarr[0, 0].imshow(cv2.imread(imgPath))
        axarr[0, 0].set_title("原始图片")
        axarr[0, 1].imshow(cv2.imread("do_fastNlMeansDenoisingColored.png"))
        axarr[0, 1].set_title("去噪图片")
        axarr[0, 2].imshow(cv2.imread("do_gray.png"))
        axarr[0, 2].set_title("二值化图片")
        axarr[0, 3].imshow(cv2.imread("do_binary.png"))
        axarr[0, 3].set_title("阈值图片")
        axarr[1, 0].imshow(cv2.imread("do_dilation.png"))
        axarr[1, 0].set_title("膨胀图片")
        axarr[1, 1].imshow(cv2.imread("do_contours.png"))
        axarr[1, 1].set_title("轮廓图片")
        axarr[1, 2].imshow(cv2.imread("do_idImg.png"))
        axarr[1, 2].set_title("剪裁图片")
        axarr[1, 3].imshow(cv2.imread("do_recognizeIDCardText.jpg"))
        axarr[1, 3].set_title(result)
        plt.show()





def main():
    ocrIdCard('card.png')
    ocrIdCard('s5.jpg')
    ocrIdCard('s9.jpg')

main()
