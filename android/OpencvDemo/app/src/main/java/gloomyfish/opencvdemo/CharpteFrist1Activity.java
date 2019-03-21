package gloomyfish.opencvdemo;

import android.app.ActivityManager;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.provider.Settings;
import android.support.annotation.RequiresApi;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;

public class CharpteFrist1Activity extends AppCompatActivity implements View.OnClickListener {
    private int REQUEST_CAPTURE_IMAGE = 1;
    private String TAG = "DEMO-OpenCV";
    private Uri fileUri;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_charpte_frist1);

        Button processBtn = (Button)this.findViewById(R.id.process_btn);
        processBtn.setOnClickListener(this);

        Button takePicBtn = (Button)this.findViewById(R.id.select_pic_btn);
        takePicBtn.setOnClickListener(this);

        Button selectPicBtn = (Button)this.findViewById(R.id.take_pic_btn);
        selectPicBtn.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        int id = v.getId();
        switch (id) {
            case R.id.take_pic_btn:
                start2Camera();
                break;
            case R.id.select_pic_btn:
                pickUpImage();
                break;
            case R.id.process_btn:
                convert2Gray();
                break;
            default:
                break;
        }
    }

    private void convert2Gray() {
        if(fileUri==null) return;
        Mat src = Imgcodecs.imread(fileUri.getPath());
        if(src.empty()) {
            return;
        }
        Mat dst = new Mat();

        Imgproc.cvtColor(src, dst, Imgproc.COLOR_BGR2GRAY);
        Bitmap bitmap = grayMat2Bitmap(dst);
        ImageView iv = (ImageView)this.findViewById(R.id.sample_img);
        iv.setImageBitmap(bitmap);
        src.release();
        dst.release();
    }

    private Bitmap grayMat2Bitmap(Mat result) {
        Mat image = null;
        if(result.cols() > 1000 || result.rows() > 1000) {
            image = new Mat();
            Imgproc.resize(result, image, new Size(result.cols() / 4, result.rows() / 4));
        } else {
            image = result;
        }
        Bitmap bitmap = Bitmap.createBitmap(image.cols(),image.rows(), Bitmap.Config.ARGB_8888);
        Imgproc.cvtColor(image, image, Imgproc.COLOR_GRAY2RGBA);
        Utils.matToBitmap(image, bitmap);
        image.release();
        return bitmap;
    }

    private void start2Camera() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Uri contentUri = FileProvider.getUriForFile(this, BuildConfig.APPLICATION_ID + ".provider", ImageSelectUtils.getSaveFilePath());

            intent.putExtra(MediaStore.EXTRA_OUTPUT, contentUri);
        }else{
            fileUri = Uri.fromFile(ImageSelectUtils.getSaveFilePath());
            intent.putExtra(MediaStore.EXTRA_OUTPUT, fileUri);
        }


        startActivityForResult(intent, REQUEST_CAPTURE_IMAGE);
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    private void startInstallPermissionSettingActivity() {
        //后面跟上包名，可以直接跳转到对应APP的未知来源权限设置界面。使用startActivityForResult 是为了在关闭设置界面之后，获取用户的操作结果，然后根据结果做其他处理
        Intent intent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:" + getPackageName()));

        intent.addFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        startActivityForResult(intent,1);
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
            }
        }
        displaySelectedImage();
    }

    private void displaySelectedImage() {
        if(fileUri == null) return;
        ImageView imageView = (ImageView)this.findViewById(R.id.sample_img);
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
}
