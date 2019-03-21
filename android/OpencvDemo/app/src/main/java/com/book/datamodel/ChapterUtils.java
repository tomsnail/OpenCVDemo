package com.book.datamodel;

import com.zkjd.activties.C10Activity;
import com.zkjd.activties.C11Activity;
import com.zkjd.activties.C12Activity;
import com.zkjd.activties.C13Activity;
import com.zkjd.activties.C14Activity;
import com.zkjd.activties.C15Activity;
import com.zkjd.activties.C16Activity;
import com.zkjd.activties.C17Activity;
import com.zkjd.activties.C1Activity;
import com.zkjd.activties.C2Activity;
import com.zkjd.activties.C3Activity;
import com.zkjd.activties.C4Activity;
import com.zkjd.activties.C5Activity;
import com.zkjd.activties.C6Activity;
import com.zkjd.activties.C7Activity;
import com.zkjd.activties.C8Activity;
import com.zkjd.activties.C9Activity;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by gloomy fish on 2017/6/27.
 */

public class ChapterUtils implements AppConstants {

    public static Map<String,Class> SectionsActivityClass = new HashMap<>();

    public static List<ItemDto> getChapters() {
        List<ItemDto> items = new ArrayList<>();
        ItemDto item1 = new ItemDto(1, "C1", "像素与通道操作");
        ItemDto item2 = new ItemDto(2, "C2", "作图操作");
        ItemDto item3 = new ItemDto(3, "C3", "图像高级操作");
        ItemDto item4 = new ItemDto(4, "C4", "基本特征检测");
        ItemDto item5 = new ItemDto(5, "C5", "文字识别");
        ItemDto item6 = new ItemDto(6, "C6", "ORC");
        items.add(item1);
        items.add(item2);
        items.add(item3);
        items.add(item4);
        items.add(item5);
        items.add(item6);
        return items;
    }

    public static List<ItemDto> getSections(int chapterNum) {
        List<ItemDto> items = new ArrayList<>();
        if(chapterNum == 1) {
            items.add(new ItemDto(1, "通道分离与合并","通道分离与合并", C1Activity.class));
            items.add(new ItemDto(2, "均值方差计算","均值方差计算", C2Activity.class));
            items.add(new ItemDto(3, "图像亮度与对比度","图像亮度与对比度", C3Activity.class));
            items.add(new ItemDto(4, "图像叠加","图像叠加", C4Activity.class));
            items.add(new ItemDto(5, "其他操作","其他操作"));
        }
        if(chapterNum == 2) {
            items.add(new ItemDto(1, "作图操作","作图操作", C5Activity.class));

        }
        if(chapterNum == 3) {
            items.add(new ItemDto(1, "模糊","模糊", C6Activity.class));
            items.add(new ItemDto(2, "统计排序滤波","统计排序滤波", C7Activity.class));
            items.add(new ItemDto(3, "边缘保留滤波","边缘保留滤波", C8Activity.class));
            items.add(new ItemDto(4, "自定义滤波","自定义滤波", C9Activity.class));
            items.add(new ItemDto(5, "形态学滤波","形态学滤波", C10Activity.class));
            items.add(new ItemDto(6, "阈值化","阈值化", C11Activity.class));
        }
        if(chapterNum == 4) {
            items.add(new ItemDto(1, "边缘检测","边缘检测", C12Activity.class));
            items.add(new ItemDto(2, "直线与圆检测","直线与圆检测", C13Activity.class));
            items.add(new ItemDto(3, "轮廓发现与绘制","轮廓发现与绘制", C14Activity.class));
            items.add(new ItemDto(4, "轮廓分析","轮廓分析"));
            items.add(new ItemDto(5, "模板匹配","模板匹配", C15Activity.class));

        }
        if(chapterNum == 5) {
            items.add(new ItemDto(1, "文字识别","文字识别", C16Activity.class));
        }
        if(chapterNum == 6) {
            items.add(new ItemDto(1, "ORC","ORC", C17Activity.class));
        }


        return items;
    }
}
