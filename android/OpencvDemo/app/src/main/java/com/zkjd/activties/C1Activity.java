package com.zkjd.activties;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.book.chapter.eight.CardNumberROIFinder;
import com.gloomyfish.opencv.plugin.c.BitmapUtils;
import com.gloomyfish.opencv.plugin.c.GlideImageLoader;
import com.gloomyfish.opencv.plugin.c.ImagePickerAdapter;
import com.gloomyfish.opencv.plugin.c.SelectDialog;
import com.googlecode.tesseract.android.TessBaseAPI;
import com.lzy.imagepicker.ImagePicker;
import com.lzy.imagepicker.bean.ImageItem;
import com.lzy.imagepicker.ui.ImageGridActivity;
import com.lzy.imagepicker.view.CropImageView;
import com.zkjd.activties.utils.ToastUtils;

import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Rect;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import gloomyfish.opencvdemo.ImageSelectUtils;
import gloomyfish.opencvdemo.R;

public class C1Activity extends AppCompatActivity implements View.OnClickListener,ImagePickerAdapter.OnRecyclerViewItemClickListener {
    private static final String DEFAULT_LANGUAGE = "chi_sim";
    private String TAG = "OcrDemoActivity";
    private int REQUEST_CAPTURE_IMAGE = 1;
    private int option;
    private Uri fileUri;
    private TessBaseAPI baseApi;

    private List<Integer> viewList = new LinkedList<>();


    public static final int REQUEST_CODE_SELECT = 100;
    public static final int REQUEST_CODE_PREVIEW = 101;

    private ImagePickerAdapter adapter;
    private ArrayList<ImageItem> selImageList; //当前选择的所有图片
    private int maxImgCount = 1;               //允许选择图片最大数
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_c1);
        Button btn1_c1 = (Button)this.findViewById(R.id.btn1_c1);
        Button btn2_c1 = (Button)this.findViewById(R.id.btn2_c1);
        Button select_photo_btn_c1 = (Button)this.findViewById(R.id.select_photo_btn_c1);
        select_photo_btn_c1.setOnClickListener(this);
        btn1_c1.setOnClickListener(this);
        btn2_c1.setOnClickListener(this);
        option = getIntent().getIntExtra("TYPE", 0);
        viewList.add(R.id.dest1_imageView_c1);
        viewList.add(R.id.dest2_imageView_c1);
        viewList.add(R.id.dest3_imageView_c1);
        viewList.add(R.id.dest4_imageView_c1);
    }

    @Override
    public void onClick(View view) {
        int id = view.getId();
        switch (id) {
            case R.id.btn1_c1:
                split();
                break;
            case R.id.btn2_c1:
                merge();
                break;
            case R.id.select_photo_btn_c1:
                startUploadImage(1000,1000,1000,1000,false);
                break;
            default:
                break;
        }
    }

    private List<Mat> mv = new ArrayList<>();
    private void split(){
        if(fileUri == null) ToastUtils.makeText(this,"请先选择图片");
        Mat src = Imgcodecs.imread(fileUri.getPath());;
        Core.split(src, mv);
        ToastUtils.makeText(this,"通道数量："+mv.size());
        Bitmap.Config conf = Bitmap.Config.ARGB_8888; // see other conf types
        for(int i=0;i<mv.size();i++){
            Mat m = mv.get(i);
            Bitmap bmp = Bitmap.createBitmap(m.cols(), m.rows(), conf);
            Utils.matToBitmap(m, bmp);
            if(i<viewList.size()){
                displayImage(viewList.get(i),bmp);
            }
        }

    }

    private void merge(){
        if(mv==null||mv.size()<=0) ToastUtils.makeText(this,"请先选择图片");
        if(fileUri == null) ToastUtils.makeText(this,"请先选择图片");
        Bitmap input = BitmapFactory.decodeFile(fileUri.getPath());
        Mat src = new Mat();
        Utils.bitmapToMat(input, src);
        int count = (int)System.currentTimeMillis()%mv.size();
        List<Mat> _mv = new ArrayList<>();

        for(int i=0;i<mv.size();i++){
            if(i!=count){
                _mv.add(mv.get(i));
            }
        }

        Core.merge(_mv, src);
        Bitmap.Config conf = Bitmap.Config.ARGB_8888; // see other conf types
        Bitmap bmp = Bitmap.createBitmap(src.cols(), src.rows(), conf);
        Utils.matToBitmap(src, bmp);
        displayImage(viewList.get(0),bmp);

      _mv.clear();
      _mv = null;

    }



    private void clear(){
        if(mv!=null&&mv.size()>0){
            for(Mat m:mv){
                m.release();
            }
            mv.clear();
        }
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
                        Intent intent = new Intent(C1Activity.this, ImageGridActivity.class);
                        intent.putExtra(ImageGridActivity.EXTRAS_TAKE_PICKERS, true); // 是否是直接打开相机
                        startActivityForResult(intent, REQUEST_CODE_SELECT);
                        break;
                    case 1:
                        //打开选择,本次允许选择的数量
                        ImagePicker.getInstance().setSelectLimit(maxImgCount - selImageList.size());
                        Intent intent1 = new Intent(C1Activity.this, ImageGridActivity.class);
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
        ImageView imageView = (ImageView)this.findViewById(R.id.src_imageView_c1);
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
        ToastUtils.makeText(this,"clear");
    }
}
