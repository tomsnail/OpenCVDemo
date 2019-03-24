import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def generateMask(src,mask=None):
    sp = src.shape
    w = sp[1]
    h = sp[0]
    mask = np.zeros(src.shape, np.uint8)
    ycrcb = cv2.cvtColor(src,cv2.COLOR_BGR2YCrCb)
    for i in range(0,h):
        for j in range(0,w) :
            data = ycrcb[i,j]
            y = data[0] & 0xff;
            cr = data[1] & 0xff;
            cb = data[2] & 0xff;
            if (y > 80)and (85 <cb and cb < 135) and (135 <cr and cr < 180):
                mask[i,j] = [255,255,255]
            pass
    return mask


def FastEPFilter(src, sum,sqsum, dst=None):
    w = src.shape[1]
    h = src.shape[0]
    x2 = 0
    y2 = 0;
    x1 = 0
    y1 = 0;
    ksize = 15;
    radius = int(ksize / 2);
    ch = 3;
    data = src.copy()
    cx = 0
    cy = 0;
    sigma = 30.0
    sigma2 = sigma * sigma;
    for  row  in range(radius,h + radius):
        if (row + 1) > h :
            y2 = h
        else:
            y2 = (row + 1);
        if (row - ksize) < 0 :
            y1 = 0
        else:
            y1 = (row - ksize);
        for col  in range(0,w + radius):
            if (col + 1) > w :
                x2 = w
            else:
                x2 = (col + 1);
            if (col - ksize) < 0 :
                x1 =  0
            else:
                x1 = (col - ksize);
            if (col - radius) < 0 :
                cx = 0
            else :
                cx = col - radius
            if (row - radius) < 0 :
                 cy = 0
            else :
                 cy =row - radius
            num = (x2 - x1) * (y2 - y1);
            for i in range(0,ch) :
                s = getblockMean(sum, x1, y1, x2, y2, i, w+1);
                var = getblockSqrt(sqsum, x1, y1, x2, y2, i, w+1);

                # 计算系数K
                # print(var)
                # print(s)
                # print(num)
                try:
                    dr = (var - (s * s) / num) / num
                except:
                    print(var)
                    print(s)
                    print(num)
                mean = s / num;
                kr = dr / (dr + sigma2);

                # 得到滤波后的像素值
                r = data[cy  , cx ][i] & 0xff;
                r = int((1 - kr) * mean + kr * r);
                data[cy  , cx ][i] = r;
    dst = data.copy()
    return dst

def getblockMean(sum, x1, y1, x2, y2, i, w):
    tl = sum[y1 , x1][i];
    tr = sum[y2 , x1][i];
    bl = sum[y1, x2][i];
    br = sum[y2, x2][i];
    s = (br - bl - tr + tl);
    return s;

def getblockSqrt(sum, x1, y1, x2, y2, i, w) :
     tl = sum[y1 , x1][i];
     tr = sum[y2 , x1][i];
     bl = sum[y1 , x2][i];
     br = sum[y2 , x2][i];
     var = (br - bl - tr + tl);
     return var

def blendImage(src, mask,dst):
    blur_mask =None
    blur_mask_f = None

    # 高斯模糊
    blur_mask = cv2.GaussianBlur(mask, (3, 3), 0.0);
    blur_mask_f = np.float32(blur_mask)
    blur_mask_f = cv2.normalize(blur_mask_f, blur_mask_f, 1.0, 0, cv2.NORM_MINMAX);

    #获取数据
    w = src.shape[1];
    h = src.shape[0];
    ch = 3;
    mdata = blur_mask_f.copy()
    data1 = src.copy()
    data2 = dst.copy()

    # 高斯权重混合
    for row in range(0,h) :
        for col in range(0,w) :
            b1 = data1[row  , col ][0] & 0xff;
            g1 = data1[row  , col ][1] & 0xff;
            r1 = data1[row  , col ][2] & 0xff;

            b2 = data2[row  , col ][0] & 0xff;
            g2 = data2[row  , col ][1] & 0xff;
            r2 = data2[row  , col ][2] & 0xff;

            w2 = mdata[row , col];

            b2 = int(b2 * w2[0] + (1-w2[0]) * b1);
            g2 = int(g2 * w2[1] + (1-w2[1]) * g1);
            r2 = int(r2 * w2[2] + (1-w2[2]) * r1);

            data2[row  , col ][0]=b2;
            data2[row  , col][1]=g2;
            data2[row  , col ][2]=r2;

    return data2


def enhanceEdge(src, dst, mask):
    mask = cv2.Canny(src, 150, 300,apertureSize= 3, L2gradient=True);
    dst = cv2.bitwise_and(src, src, dst, mask);
    dst = cv2.GaussianBlur(dst, (3, 3), 0.0);
    return dst


def main():
    src = cv2.imread('timg1.jpg')
    mask = generateMask(src)
    sum, sqsum= cv2.integral2(src,sdepth=cv2.CV_32S, sqdepth=cv2.CV_32F)
    dst = FastEPFilter(src,sum,sqsum)
    dst = blendImage(src,mask,dst)
    dst = enhanceEdge(src,dst,mask)
    cv2.imwrite("fb.jpg",dst)
    f, axarr = plt.subplots(1, 2)
    axarr[0].imshow(cv2.imread('timg1.jpg'))
    axarr[1].imshow(cv2.imread('fb.jpg'))
    plt.show()

main();