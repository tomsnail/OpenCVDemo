package com.book.chapter.eight;

import android.graphics.Bitmap;
import android.util.Log;

import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.RotatedRect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

import static org.opencv.core.CvType.CV_32F;

/**
 * Created by gloomy fish on 2017/12/07.
 */

public class CardNumberROIFinder {

    public static Bitmap extractNumberROI(Bitmap input, Bitmap template) {
        Mat src = new Mat();
        Mat tpl = new Mat();
        Mat dst = new Mat();
        Mat fixSrc = new Mat();
        Utils.bitmapToMat(input, src);

        Utils.bitmapToMat(template, tpl);
        Imgproc.cvtColor(src, dst, Imgproc.COLOR_BGRA2GRAY);
        Imgproc.Canny(dst, dst, 100, 400, 3, false);
        List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
        Mat hierachy = new Mat();
        Imgproc.findContours(dst, contours, hierachy, Imgproc.RETR_TREE, Imgproc.CHAIN_APPROX_SIMPLE);
        Imgproc.cvtColor(dst, dst, Imgproc.COLOR_GRAY2BGR);
        int width = input.getWidth();
        int height = input.getHeight();
        Rect roiArea = null;
        for(int i=0; i<contours.size(); i++) {
            List<Point> points = contours.get(i).toList();
            Rect rect = Imgproc.boundingRect(contours.get(i));
            if(rect.width < width && rect.width > (width / 2)) {
                if(rect.height <= (height / 4)) continue;
                roiArea = rect;
            }
        }

        if(roiArea==null){
            fixSrc.release();
            src.release();
            dst.release();
            return null;
        }
        // clip ROI Area
        Mat result = src.submat(roiArea);

        // fix size, in order to match template
        Size fixSize = new Size(547, 342);
        Imgproc.resize(result, fixSrc, fixSize);
        result = fixSrc;

        // detect location
        int result_cols =  result.cols() - tpl.cols() + 1;
        int result_rows = result.rows() - tpl.rows() + 1;
        Mat mr = new Mat(result_rows, result_cols, CvType.CV_32FC1);

        // template match
        Imgproc.matchTemplate(result, tpl, mr, Imgproc.TM_CCORR_NORMED);
        Core.normalize(mr, mr, 0, 1, Core.NORM_MINMAX, -1);
        Core.MinMaxLocResult minMaxLocResult = Core.minMaxLoc(mr);
        Point maxLoc = minMaxLocResult.maxLoc;
        Bitmap.Config conf = Bitmap.Config.ARGB_8888; // see other conf types

        // find id number ROI
        Rect idNumberROI = new Rect((int)(maxLoc.x+tpl.cols()-40), (int)maxLoc.y, (int)(result.cols() - (maxLoc.x+tpl.cols())-40), tpl.rows()-10);
        Mat idNumberArea = result.submat(idNumberROI);

        // 返回对象
        Bitmap bmp = Bitmap.createBitmap(idNumberArea.cols(), idNumberArea.rows(), conf);
        Utils.matToBitmap(idNumberArea, bmp);

        // 释放内存
        idNumberArea.release();
        idNumberArea.release();
        result.release();
        fixSrc.release();
        src.release();
        dst.release();
        return bmp;
    }

    public static Bitmap extractPreNumberROI(Bitmap input, Bitmap template) {
        Mat src = new Mat();
        Mat tpl = new Mat();
        Mat dst = new Mat();
        Mat fixSrc = new Mat();
        Utils.bitmapToMat(input, src);
        Utils.bitmapToMat(template, tpl);
        Mat preImg = new Mat();
        Bitmap.Config conf = Bitmap.Config.ARGB_8888; // see other conf types
        Imgproc.GaussianBlur(src,preImg,new Size(15,15),0);
//        preImg = cv2.GaussianBlur(preImg, (15, 15), 0)
        Mat preImgx = new Mat();
        Imgproc.Scharr(preImg,preImgx,CV_32F,1,0);
        Core.convertScaleAbs(preImgx,preImgx);
        Mat preImgy = new Mat();
        Imgproc.Scharr(preImg,preImgy,CV_32F,0,1);
        Core.convertScaleAbs(preImgy,preImgy);
        Core.addWeighted(preImgx,0.5,preImgy,0.5,30,preImg);
        Imgproc.GaussianBlur(preImg,preImg,new Size(15,15),0);
        Imgproc.cvtColor(preImg, preImg, Imgproc.COLOR_BGRA2GRAY);
        Imgproc.threshold(preImg, preImg,0,255, Imgproc.THRESH_TOZERO | Imgproc.THRESH_TRIANGLE);
        Imgproc.Canny(preImg, dst, 50, 150, 3, false);
        List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
        Mat hierachy = new Mat();
        Imgproc.findContours(dst, contours, hierachy, Imgproc.RETR_TREE, Imgproc.CHAIN_APPROX_SIMPLE);
        Imgproc.cvtColor(dst, dst, Imgproc.COLOR_GRAY2BGR);
        int width = input.getWidth();
        int height = input.getHeight();
        Rect roiArea = null;
        for(int i=0; i<contours.size(); i++) {
            Rect rect = Imgproc.boundingRect(contours.get(i));

            if(rect.width < width && rect.width > (width / 2)) {
                BigDecimal w = new BigDecimal(rect.width);
                BigDecimal h = new BigDecimal(rect.height);
                if(w.divide(h,1,BigDecimal.ROUND_HALF_UP).doubleValue()!=1.6)continue;
                roiArea = rect;

            }
        }

        if(roiArea==null){
            Bitmap bmp = Bitmap.createBitmap(preImg.cols(), preImg.rows(), conf);
            Utils.matToBitmap(preImg, bmp);
            preImgx.release();
            preImgy.release();
            preImg.release();
            fixSrc.release();
            src.release();
            dst.release();
            return bmp;
        }
        // clip ROI Area
        Mat result = src.submat(roiArea);

        // fix size, in order to match template
        Size fixSize = new Size(547, 342);
        Imgproc.resize(result, fixSrc, fixSize);
        result = fixSrc;
//
//        // detect location//170 275 310 35
//        int result_cols =  result.cols() - tpl.cols() + 1;
//        int result_rows = result.rows() - tpl.rows() + 1;
//        Mat mr = new Mat(result_rows, result_cols, CvType.CV_32FC1);
//
//
//
//        // template match
//        Imgproc.matchTemplate(result, tpl, mr, Imgproc.TM_CCORR_NORMED);
//       Core.normalize(mr, mr, 0, 1, Core.NORM_MINMAX, -1);
//        Core.MinMaxLocResult minMaxLocResult = Core.minMaxLoc(mr);
//        Point maxLoc = minMaxLocResult.maxLoc;


        // find id number ROI
        Rect idNumberROI = new Rect(170, 275, 320, 38);
        Mat idNumberArea = result.submat(idNumberROI);

        // 返回对象
        Bitmap bmp = Bitmap.createBitmap(idNumberArea.cols(), idNumberArea.rows(), conf);
        Utils.matToBitmap(idNumberArea, bmp);

        // 释放内存
        preImgx.release();
        preImgy.release();
        preImg.release();
        idNumberArea.release();
//        idNumberArea.release();
        result.release();
        fixSrc.release();
        src.release();
        dst.release();
        return bmp;
    }


    public static Bitmap extractNumberROI(Bitmap input, int x, int y, int width, int height) {
        Mat src = new Mat();
        Bitmap.Config conf = Bitmap.Config.ARGB_8888; // see other conf types
        Utils.bitmapToMat(input, src);
        // find id number ROI
        Mat fixSrc = new Mat();
        Size fixSize = new Size(1680, 1071);
        Imgproc.resize(src, fixSrc, fixSize);
        Mat result = fixSrc;
        Rect orcROI = new Rect(x,y,width,height);
        Mat orcArea = result.submat(orcROI);

        // 返回对象
        Bitmap bmp = Bitmap.createBitmap(orcArea.cols(), orcArea.rows(), conf);
        Utils.matToBitmap(orcArea, bmp);


        orcArea.release();
        src.release();
        fixSrc.release();
        result.release();
        return bmp;
    }


    public static Bitmap extractNumberROIDraw(Bitmap input) {
        Mat src = new Mat();
        Mat tpl = new Mat();
        Mat dst = new Mat();
        Mat fixSrc = new Mat();
        Utils.bitmapToMat(input, src);

        Imgproc.cvtColor(src, dst, Imgproc.COLOR_BGRA2GRAY);
        Imgproc.Canny(dst, dst, 100, 400, 3, false);
        List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
        Mat hierachy = new Mat();
        Imgproc.findContours(dst, contours, hierachy, Imgproc.RETR_TREE, Imgproc.CHAIN_APPROX_SIMPLE);
        Imgproc.cvtColor(dst, dst, Imgproc.COLOR_GRAY2BGR);
        int width = input.getWidth();
        int height = input.getHeight();
        Rect roiArea = null;
        Mat draw = new Mat(dst.size(),dst.type());
        for(int i=0; i<contours.size(); i++) {
            Imgproc.drawContours(draw, contours, i, new Scalar(0, 0, 255), 2);
        }

        Bitmap.Config conf = Bitmap.Config.ARGB_8888; // see other conf types
        // 返回对象
        Bitmap bmp = Bitmap.createBitmap(draw.cols(), draw.rows(), conf);
        Utils.matToBitmap(draw, bmp);


        fixSrc.release();
        src.release();
        dst.release();
        draw.release();
        return bmp;
    }

    public static void deSkewText(Mat textImage, Mat dst) {
        // 二值化图像
        Mat gray = new Mat();
        Mat binary = new Mat();
        Imgproc.cvtColor(textImage, gray, Imgproc.COLOR_BGR2GRAY);
        Imgproc.threshold(gray, binary, 0, 255,Imgproc.THRESH_BINARY_INV | Imgproc.THRESH_OTSU);

        // 寻找文本区域最新外接矩形
        int w = binary.cols();
        int h = binary.rows();
        List<Point> points = new ArrayList<>();
        int p = 0;
        byte[] data = new byte[w*h];
        binary.get(0, 0, data);
        int index = 0;
        for(int row=0; row<h; row++) {
            for(int col=0; col<w; col++) {
                index = row*w + col;
                p = data[index]&0xff;
                if(p == 255) {
                    points.add(new Point(col, row));
                }
            }
        }
        RotatedRect box = Imgproc.minAreaRect(new MatOfPoint2f(points.toArray(new Point[0])));
        double angle = box.angle;
        if (angle < -45.)
            angle += 90.;

        Point[] vertices = new Point[4];
        box.points(vertices);
        // de-skew 偏斜校正
        Mat rot_mat = Imgproc.getRotationMatrix2D(box.center, angle, 1);
        Imgproc.warpAffine(binary, dst, rot_mat, binary.size(), Imgproc.INTER_CUBIC);
        Core.bitwise_not(dst, dst);

        gray.release();
        binary.release();
        rot_mat.release();
    }
}
