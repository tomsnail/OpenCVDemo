package com.book.chapter.eight;

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

import com.gloomyfish.opencv.plugin.c.BitmapUtils;
import com.gloomyfish.opencv.plugin.c.GlideImageLoader;
import com.gloomyfish.opencv.plugin.c.ImagePickerAdapter;
import com.gloomyfish.opencv.plugin.c.SelectDialog;
import com.googlecode.tesseract.android.TessBaseAPI;
import com.lzy.imagepicker.ImagePicker;
import com.lzy.imagepicker.bean.ImageItem;
import com.lzy.imagepicker.ui.ImageGridActivity;
import com.lzy.imagepicker.view.CropImageView;

import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import gloomyfish.opencvdemo.ImageSelectUtils;
import gloomyfish.opencvdemo.R;

public class OcrDemoActivity extends AppCompatActivity implements View.OnClickListener,ImagePickerAdapter.OnRecyclerViewItemClickListener {
    private static final String DEFAULT_LANGUAGE = "chi_sim";
    private String TAG = "OcrDemoActivity";
    private int REQUEST_CAPTURE_IMAGE = 1;
    private int option;
    private Uri fileUri;
    private TessBaseAPI baseApi;


    public static final int REQUEST_CODE_SELECT = 100;
    public static final int REQUEST_CODE_PREVIEW = 101;

    private ImagePickerAdapter adapter;
    private ArrayList<ImageItem> selImageList; //当前选择的所有图片
    private int maxImgCount = 1;               //允许选择图片最大数
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ocr_demo);
      //  Button selectBtn = (Button)this.findViewById(R.id.select_image_btn);
        Button ocrRecogBtn = (Button)this.findViewById(R.id.ocr_recognize_btn);
        Button ocrRecogDBtn = (Button)this.findViewById(R.id.ocr_recognize_contour_btn);
        Button select_photo_crop_btn = (Button)this.findViewById(R.id.select_photo_crop_btn);
        Button select_photo_btn = (Button)this.findViewById(R.id.select_photo_btn);
        Button ocr_recognize_crop_btn = (Button)this.findViewById(R.id.ocr_recognize_crop_btn);
       // selectBtn.setOnClickListener(this);
        ocrRecogBtn.setOnClickListener(this);
        ocrRecogDBtn.setOnClickListener(this);
        select_photo_btn.setOnClickListener(this);
        select_photo_crop_btn.setOnClickListener(this);
        ocr_recognize_crop_btn.setOnClickListener(this);
        option = getIntent().getIntExtra("TYPE", 0);

        try {
            initTessBaseAPI();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }

        if(option == 2) {
            this.setTitle("身份证号码识别演示");
        } else if(option == 3) {
            this.setTitle("偏斜校正演示");
            ocrRecogBtn.setText("校正");
        }
        else {
            this.setTitle("Tesseract OCR文本识别演示");
        }
    }

    @Override
    public void onClick(View view) {
        int id = view.getId();
        switch (id) {
//            case R.id.select_image_btn:
//                pickUpImage();
//                break;
            case R.id.ocr_recognize_btn:
                if(option == 2) {
                    recognizeCardId();
                } else if(option == 3) {
                    deSkewTextImage();
                }else {
                    recognizeTextImage();
                }
                break;
            case R.id.ocr_recognize_contour_btn:
                recognizeCardIdDraw();
                break;
            case R.id.select_photo_btn:
                startUploadImage(1000,1000,1000,1000,false);
                break;
            case R.id.select_photo_crop_btn:

                startUploadImage(960,600,960,600,true);
                break;
            case R.id.ocr_recognize_crop_btn:

                recognizeCardIdCrop();
                break;
            default:
                break;
        }
    }

    private void deSkewTextImage() {
        Mat src = Imgcodecs.imread(fileUri.getPath());
        if(src.empty()){
            return;
        }
        Mat dst = new Mat();
        CardNumberROIFinder.deSkewText(src, dst);

        // 转换为Bitmap，显示
        Bitmap bm = Bitmap.createBitmap(src.cols(), src.rows(), Bitmap.Config.ARGB_8888);
        Utils.matToBitmap(dst, bm);

        // show
        ImageView iv = this.findViewById(R.id.chapter8_imageView);
        iv.setImageBitmap(bm);

        // 释放内存
        dst.release();
        src.release();
    }


    private void initTessBaseAPI() throws IOException {
        baseApi = new TessBaseAPI();
        String datapath = Environment.getExternalStorageDirectory() + "/tesseract/";
        File dir = new File(datapath + "tessdata/");
        if (!dir.exists()) {
            dir.mkdirs();
            InputStream input = getResources().openRawResource(R.raw.nums);
            File file = new File(dir, "nums.traineddata");
            FileOutputStream output = new FileOutputStream(file);
            byte[] buff = new byte[1024];
            int len = 0;
            while((len = input.read(buff)) != -1) {
                output.write(buff, 0, len);
            }
            input.close();
            output.close();
        }
        File chi_sim = new File(datapath + "tessdata/chi_sim.traineddata");
        if (!chi_sim.exists()) {
            dir.mkdirs();
            InputStream input = getResources().openRawResource(R.raw.chi_sim);
            File file = new File(dir, "chi_sim.traineddata");
            FileOutputStream output = new FileOutputStream(file);
            byte[] buff = new byte[1024];
            int len = 0;
            while((len = input.read(buff)) != -1) {
                output.write(buff, 0, len);
            }
            input.close();
            output.close();
        }
        boolean success = baseApi.init(datapath, DEFAULT_LANGUAGE);
        if(success){
            Log.i(TAG, "load Tesseract OCR Engine successfully...");
        } else {
            Log.i(TAG, "WARNING:could not initialize Tesseract data...");
        }
    }

    private void recognizeCardId() {
        final Bitmap template = BitmapFactory.decodeResource(this.getResources(), R.drawable.card_template);
        final Bitmap cardImage = BitmapFactory.decodeFile(fileUri.getPath());
        Bitmap temp = CardNumberROIFinder.extractNumberROI(cardImage.copy(Bitmap.Config.ARGB_8888, true), template);
        if(temp==null){
            TextView txtView = findViewById(R.id.text_result_id);
            txtView.setText("无法识别" );
            return;
        }
        baseApi.setImage(temp);
        String myIdNumber = baseApi.getUTF8Text();
        TextView txtView = findViewById(R.id.text_result_id);
        txtView.setText("身份证号码为:" + myIdNumber);
        ImageView imageView = findViewById(R.id.chapter8_imageView);
        imageView.setImageBitmap(temp);
    }

    private void recognizeCardIdCrop() {
        StringBuffer sb = new StringBuffer();
        final Bitmap cardImage = BitmapFactory.decodeFile(fileUri.getPath());
        Bitmap temp = CardNumberROIFinder.extractNumberROI(cardImage.copy(Bitmap.Config.ARGB_8888, true), 550,870,1000,140);
        if(temp!=null){
            baseApi.setImage(temp);
            sb.append(baseApi.getUTF8Text());
        }else{

        }

        temp = CardNumberROIFinder.extractNumberROI(cardImage.copy(Bitmap.Config.ARGB_8888, true), 300,130,500,100);
        if(temp!=null){
            baseApi.setImage(temp);
            sb.append(baseApi.getUTF8Text());
        }
        temp = CardNumberROIFinder.extractNumberROI(cardImage.copy(Bitmap.Config.ARGB_8888, true), 300,540,800,300);
        if(temp!=null){
            baseApi.setImage(temp);
            sb.append(baseApi.getUTF8Text());
        }

        TextView txtView = findViewById(R.id.text_result_id);
        txtView.setText("识别信息为:" + sb.toString());
        ImageView imageView = findViewById(R.id.chapter8_imageView);
        imageView.setImageBitmap(temp);
    }

    private void recognizeCardIdDraw() {
        final Bitmap cardImage = BitmapFactory.decodeFile(fileUri.getPath());
        Bitmap temp = CardNumberROIFinder.extractNumberROIDraw(cardImage.copy(Bitmap.Config.ARGB_8888, true));
        ImageView imageView = findViewById(R.id.chapter8_contour_imageView);
        imageView.setImageBitmap(temp);
    }

    private void recognizeTextImage() {
        if(fileUri == null) return;
        Bitmap bmp = BitmapFactory.decodeFile(fileUri.getPath());
        baseApi.setImage(bmp);
        String recognizedText = baseApi.getUTF8Text();
        TextView txtView = findViewById(R.id.text_result_id);
        if(!recognizedText.isEmpty()) {
            txtView.append("识别结果:\n"+recognizedText);
        }
    }

    public void startUploadImage(int fw, int fh, int ox, int oy, boolean crop) {
        initImagePicker(fw, fh, ox, oy, crop);
        initWidget();
    }

    private void pickUpImage() {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent, "图像选择..."), REQUEST_CAPTURE_IMAGE);
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
        // RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recyclerView);
        if (selImageList == null) {
            selImageList = new ArrayList<>();
            adapter = new ImagePickerAdapter(this, selImageList, maxImgCount);
            adapter.setOnItemClickListener(this);
        }


//        recyclerView.setLayoutManager(new GridLayoutManager(this, 4));
//        recyclerView.setHasFixedSize(true);
//        recyclerView.setAdapter(adapter);

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
                        Intent intent = new Intent(OcrDemoActivity.this, ImageGridActivity.class);
                        intent.putExtra(ImageGridActivity.EXTRAS_TAKE_PICKERS, true); // 是否是直接打开相机
                        startActivityForResult(intent, REQUEST_CODE_SELECT);
                        break;
                    case 1:
                        //打开选择,本次允许选择的数量
                        ImagePicker.getInstance().setSelectLimit(maxImgCount - selImageList.size());
                        Intent intent1 = new Intent(OcrDemoActivity.this, ImageGridActivity.class);
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
        ImageView imageView = (ImageView)this.findViewById(R.id.chapter8_imageView);
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

    @Override
    public void onItemClick(View view, int position) {

    }
}
