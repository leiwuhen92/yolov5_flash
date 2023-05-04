# -*- coding: utf-8 -*-
import os
import cv2

path = "./flash"      # jpg图片和对应的生成结果的txt标注文件，放在一起
path3 = "./result"    # 裁剪出来的小图保存的根目录

img_total = []
txt_total = []

file = os.listdir(path)
for filename in file:
    if filename == "labels":
        for txt in os.listdir(os.path.join(path, filename)):
            first, last = os.path.splitext(txt)
            txt_total.append(first)
    else:
        first, last = os.path.splitext(filename)
        img_total.append(first)

print("txt_total:%s" % txt_total)
print("img_total:%s" % img_total)


for img_ in img_total:
    if img_ in txt_total:
        filename_img = img_+".png"
        png_path = os.path.join(path, filename_img)
        filename_txt = img_ + ".txt"
        txt_path = os.path.join(path, "labels", filename_txt)
        print("png_path:%s, txt_path:%s" % (png_path, txt_path))

        # 获取图片的宽高
        img = cv2.imread(png_path)
        size = img.shape
        w = img.shape[1]
        h = img.shape[0]

        img = cv2.imread(png_path)
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)  # resize 图像大小，否则roi区域可能会报错

        n = 1
        with open(txt_path, "r+", encoding="utf-8", errors="ignore") as f:
            for line in f:
                aa = line.split(" ")
                if int(aa[0]) == 0:  # flash类别
                    x_center = w * float(aa[1])       # aa[1]左上点的x坐标
                    y_center = h * float(aa[2])       # aa[2]左上点的y坐标
                    width = int(w * float(aa[3]))       # aa[3]图片width
                    height = int(h * float(aa[4]))      # aa[4]图片height
                    print("x_center:%s, y_center:%s, width:%s, height:%s" % (x_center, y_center, width, height))

                    left_topx = int(x_center-width/2.0)
                    left_topy = int(y_center-height/2.0)

                    # [左上y:右下y, 左上x:右下x] (y1:y2, x1:x2)需要调参，否则裁剪出来的小图可能不太好
                    roi = img[left_topy + 1:left_topy + height + 3, left_topx + 1:left_topx + width + 1]
                    # print('roi:', roi)                        # 如果不resize图片统一大小，可能会得到有的roi为[]导致报错

                    filename_last = img_ + "_" + str(n) + ".png"    # 裁剪出来的小图文件名
                    print("filename_last:%s" % filename_last)
                    cv2.imwrite(os.path.join(path3, filename_last), roi)
                    n = n+1
                    
    else:
        continue
