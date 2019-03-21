package com.zkjd.activties;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.gloomyfish.opencv.plugin.c.BitmapUtils;
import com.gloomyfish.opencv.plugin.c.GlideImageLoader;
import com.gloomyfish.opencv.plugin.c.ImagePickerAdapter;
import com.gloomyfish.opencv.plugin.c.SelectDialog;
import com.lzy.imagepicker.ImagePicker;
import com.lzy.imagepicker.bean.ImageItem;
import com.lzy.imagepicker.ui.ImageGridActivity;
import com.lzy.imagepicker.view.CropImageView;
import com.zkjd.activties.utils.ToastUtils;

import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import gloomyfish.opencvdemo.ImageSelectUtils;
import gloomyfish.opencvdemo.R;

public class C13Activity extends AppCompatActivity implements View.OnClickListener,ImagePickerAdapter.OnRecyclerViewItemClickListener {
    private String TAG = "C13Activity";
    private int REQUEST_CAPTURE_IMAGE = 1;
    private int option;
    private Uri fileUri;

    private List<Integer> viewList = new LinkedList<>();


    public static final int REQUEST_CODE_SELECT = 100;
    public static final int REQUEST_CODE_PREVIEW = 101;

    private ImagePickerAdapter adapter;
    private ArrayList<ImageItem> selImageList; //当前选择的所有图片
    private int maxImgCount = 1;               //允许选择图片最大数
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_c13);
        Button btn1_c13 = (Button)this.findViewById(R.id.btn1_c13);
        Button btn2_c13 = (Button)this.findViewById(R.id.btn2_c13);
        Button btn3_c13 = (Button)this.findViewById(R.id.btn3_c13);
        Button select_photo_btn_c13 = (Button)this.findViewById(R.id.select_photo_btn_c13);
        select_photo_btn_c13.setOnClickListener(this);
        btn1_c13.setOnClickListener(this);
        btn2_c13.setOnClickListener(this);
        btn3_c13.setOnClickListener(this);
        option = getIntent().getIntExtra("TYPE", 0);
        viewList.add(R.id.dest1_imageView_c13);

        iniLoadOpenCV();
    }

    private void iniLoadOpenCV() {
        boolean success = OpenCVLoader.initDebug();
        if(success) {
            Log.i(TAG, "OpenCV Libraries loaded...");
        } else {
            Toast.makeText(this.getApplicationContext(), "WARNING: Could not load OpenCV Libraries!", Toast.LENGTH_LONG).show();
        }
    }

    private int index = 1;

    @Override
    public void onClick(View view) {
        int id = view.getId();
        switch (id) {
            case R.id.btn1_c13:
                a1(id);
                break;

            case R.id.btn2_c13:
                a1(id);
                break;
            case R.id.btn3_c13:
                a1(id);
                break;
            case R.id.select_photo_btn_c13:
                index = 1;
                startUploadImage(1000,1000,1000,1000,false);
                break;

            default:
                break;
        }
    }

    private void a1(int index){
        if(fileUri == null) ToastUtils.makeText(this,"请先选择图片");
        Mat src = Imgcodecs.imread(fileUri.getPath());
        if(src.empty()) {
            return;
        }

       // Imgproc.cvtColor(src, src, Imgproc.COLOR_BGRA2GRAY);
        Mat dst = new Mat();

        switch (index) {
            case R.id.btn1_c13:
                Mat edges = new Mat();
                Imgproc.Canny(src, edges, 50, 150, 3, true);

                Mat lines = new Mat();
                Imgproc.HoughLinesP(edges, lines, 1, Math.PI/180.0, 100, 50, 10);

                Mat out = Mat.zeros(src.size(), src.type());
                for(int i=0; i<lines.rows(); i++) {
                    int[] oneline = new int[4];
                    lines.get(i, 0, oneline);
                    Imgproc.line(out, new Point(oneline[0], oneline[1]),
                            new Point(oneline[2], oneline[3]),
                            new Scalar(0, 0, 255), 2, 8, 0);
                }
                out.copyTo(dst);

                // 释放内存
                out.release();
                edges.release();
                break;
            case R.id.btn2_c13:
                edges = new Mat();
                Imgproc.Canny(src, edges, 50, 150, 3, true);

                lines = new Mat();
                Imgproc.HoughLines(edges, lines, 1,Math.PI/180.0, 200);
                out = Mat.zeros(src.size(), src.type());
                float[] data = new float[2];
                for(int i=0; i<lines.rows(); i++) {
                    lines.get(i, 0, data);
                    float rho = data[0], theta = data[1];
                    double a = Math.cos(theta), b = Math.sin(theta);
                    double x0 = a*rho, y0 = b*rho;
                    Point pt1 = new Point();
                    Point pt2 = new Point();
                    pt1.x = Math.round(x0 + 1000*(-b));
                    pt1.y = Math.round(y0 + 1000*(a));
                    pt2.x = Math.round(x0 - 1000*(-b));
                    pt2.y = Math.round(y0 - 1000*(a));
                    Imgproc.line(out, pt1, pt2, new Scalar(0,0,255), 3, Imgproc.LINE_AA, 0);
                }
                out.copyTo(dst);
                out.release();
                edges.release();
                lines.release();
                break;
            case R.id.btn3_c13:
                Mat gray = new Mat();
                Imgproc.pyrMeanShiftFiltering(src, gray, 15, 80);
                Imgproc.cvtColor(gray, gray, Imgproc.COLOR_BGR2GRAY);

                Imgproc.GaussianBlur(gray, gray, new Size(3, 3),  0);

                // detect circles
                Mat circles = new Mat();
                dst.create(src.size(), src.type());
                Imgproc.HoughCircles(gray, circles, Imgproc.HOUGH_GRADIENT, 1, 20, 100, 30, 10, 200);
                for(int i=0; i<circles.cols(); i++) {
                    float[] info = new float[3];
                    circles.get(0, i, info);
                    Imgproc.circle(dst, new Point((int)info[0], (int)info[1]), (int)info[2],
                            new Scalar(0, 255, 0), 2, 8, 0);
                }
                circles.release();
                gray.release();
                break;
            default:
                break;
        }
        Bitmap bm = Bitmap.createBitmap(src.cols(), src.rows(), Bitmap.Config.ARGB_8888);
        Mat result = new Mat();
        Imgproc.cvtColor(dst, result, Imgproc.COLOR_BGR2RGBA);
        Utils.matToBitmap(result, bm);



        displayImage(viewList.get(0),bm);
        src.release();
        dst.release();
        result.release();
    }









    private void clear(){

    }




    public void startUploadImage(int fw, int fh, int ox, int oy, boolean crop) {
        initImagePicker(fw, fh, ox, oy, crop);
        initWidget();
    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode == REQUEST_CAPTURE_IMAGE && resultCode == RESULT_OK) {
            if(data != null) {
                Uri uri = data.getData();
                File f = new File(ImageSelectUtils.getRealPath(uri, getApplicationContext()));
                fileUri = Uri.fromFile(f);
                displaySelectedImage();
            }


        }else if (resultCode == ImagePicker.RESULT_CODE_ITEMS) {
            //添加图片返回
            if (data != null && requestCode == REQUEST_CODE_SELECT) {
                ArrayList<ImageItem> images = (ArrayList<ImageItem>) data.getSerializableExtra(ImagePicker.EXTRA_RESULT_ITEMS);
                if (images != null) {

                    String newPath = BitmapUtils.compressImageUpload(images.get(0).path);
                    Uri uri = data.getData();
                    File f = new File(newPath);
                    fileUri = Uri.fromFile(f);
                    displaySelectedImage();
                    clear();
                }
            }
        } else if (resultCode == ImagePicker.RESULT_CODE_BACK) {
            if (data != null && requestCode == REQUEST_CODE_PREVIEW) {
                ArrayList<ImageItem> images = (ArrayList<ImageItem>) data.getSerializableExtra(ImagePicker.EXTRA_IMAGE_ITEMS);
                if (images != null) {
                    selImageList.clear();
                    selImageList.addAll(images);
                    adapter.setImages(selImageList);
                }
            }
        }



    }


    private void initImagePicker(int fw, int fh, int ox, int oy, boolean crop) {

        if (fw <= 0) {
            fw = 800;
        }

        if (fh <= 0) {
            fh = 1200;
        }

        if (ox <= 0) {
            ox = fw;
        }

        if (oy <= 0) {
            oy = fh;
        }

        ImagePicker imagePicker = ImagePicker.getInstance();
        imagePicker.setImageLoader(new GlideImageLoader());   //设置图片加载器
        imagePicker.setShowCamera(true);                      //显示拍照按钮
        imagePicker.setCrop(crop);                            //允许裁剪（单选才有效）
        imagePicker.setSaveRectangle(true);                   //是否按矩形区域保存
        imagePicker.setSelectLimit(maxImgCount);              //选中数量限制
        imagePicker.setMultiMode(false);                      //多选
        imagePicker.setStyle(CropImageView.Style.RECTANGLE);  //裁剪框的形状
        imagePicker.setFocusWidth(fw);                       //裁剪框的宽度。单位像素（圆形自动取宽高最小值）
        imagePicker.setFocusHeight(fh);                      //裁剪框的高度。单位像素（圆形自动取宽高最小值）
        imagePicker.setOutPutX(ox);                         //保存文件的宽度。单位像素
        imagePicker.setOutPutY(oy);                         //保存文件的高度。单位像素
    }

    private void initWidget() {

        if (selImageList == null) {
            selImageList = new ArrayList<>();
            adapter = new ImagePickerAdapter(this, selImageList, maxImgCount);
            adapter.setOnItemClickListener(this);
        }


        List<String> names = new ArrayList<>();
        names.add("拍照");
        names.add("相册");
        showDialog(new SelectDialog.SelectDialogListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                switch (position) {
                    case 0: // 直接调起相机
                        //打开选择,本次允许选择的数量
                        ImagePicker.getInstance().setSelectLimit(maxImgCount - selImageList.size());
                        Intent intent = new Intent(C13Activity.this, ImageGridActivity.class);
                        intent.putExtra(ImageGridActivity.EXTRAS_TAKE_PICKERS, true); // 是否是直接打开相机
                        startActivityForResult(intent, REQUEST_CODE_SELECT);
                        break;
                    case 1:
                        //打开选择,本次允许选择的数量
                        ImagePicker.getInstance().setSelectLimit(maxImgCount - selImageList.size());
                        Intent intent1 = new Intent(C13Activity.this, ImageGridActivity.class);
                        startActivityForResult(intent1, REQUEST_CODE_SELECT);
                        break;
                    default:
                        break;
                }
            }
        }, names);
    }

    private SelectDialog showDialog(SelectDialog.SelectDialogListener listener, List<String> names) {
        SelectDialog dialog = new SelectDialog(this, R.style.transparentFrameWindowStyle, listener, names);
        if (!this.isFinishing()) {
            dialog.show();
        }
        return dialog;
    }



    private void displaySelectedImage() {
        if(fileUri == null) return;
        ImageView imageView = null;

        imageView = (ImageView)this.findViewById(R.id.src_imageView_c13);



        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeFile(fileUri.getPath(), options);
        int w = options.outWidth;
        int h = options.outHeight;
        int inSample = 1;
        if(w > 1000 || h > 1000) {
            while(Math.max(w/inSample, h/inSample) > 1000) {
                inSample *=2;
            }
        }
        options.inJustDecodeBounds = false;
        options.inSampleSize = inSample;
        options.inPreferredConfig = Bitmap.Config.ARGB_8888;
        Bitmap bm = BitmapFactory.decodeFile(fileUri.getPath(), options);
        imageView.setImageBitmap(bm);


    }

    private void displayImage(int index,Bitmap bm){
        ImageView imageView = (ImageView)this.findViewById(index);
        if(imageView!=null){
            imageView.setImageBitmap(bm);
        }
    }

    @Override
    public void onItemClick(View view, int position) {

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        clear();
    }

    private Bitmap get(int index){
        ImageView mImageView = (ImageView)this.findViewById(index);
        if(mImageView==null) return null;
        mImageView.setDrawingCacheEnabled(true);
        Bitmap bitmap = Bitmap.createBitmap(mImageView.getDrawingCache());
        mImageView.setDrawingCacheEnabled(false);
        return bitmap;
    }
}
