# 请先将csv转成txt  然后去掉没必要的信息！

import os, sys
import glob
from PIL import Image

#img_path = "./train"           # 图像存储位置
img_path = "./valid"            # 图像存储位置
txt_path = "./labels"           # txt文件存储位置
suffix = ".jpg"                 # 图片后缀名
 
# 注意对应box的Xmin Ymin Xmax Ymax !!   
def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[2]) / 2.0 
    y = (box[1] + box[3]) / 2.0 
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
    
img_Lists = glob.glob(img_path + '/*' + suffix)
 
img_basenames = [] # e.g. 100.jpg
for item in img_Lists:
    img_basenames.append(os.path.basename(item))
 
img_names = [] # e.g. 100
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)
 
#img_all_label = open('train_label.txt').read().splitlines() 
img_all_label = open('valid_label.txt').read().splitlines() 
 
for img in img_names:
    im = Image.open((img_path + '/' + img + suffix))
    width, height = im.size
 
    txt_file = open((txt_path + '/' + img + '.txt'), 'w')
 
    for img_each_label in img_all_label:
        spt = img_each_label.split(' ') 
        if(img == spt[0]):
            b = (float(spt[1]), float(spt[2]), float(spt[3]), float(spt[4]))
            bb = convert((width, height), b)
            txt_file.write("0" + " " + " ".join([str(a) for a in bb]) + '\n')
            #txt_file.write("0" + " " + str(bb[0]) + " " + str(bb[1]) + " " + str(bb[2]) + " " + str(bb[3]) + '\n')           
    print(img + "  is done!")
                
txt_num = len([lists for lists in os.listdir(txt_path) if os.path.isfile(os.path.join(txt_path, lists))])
print("Total " + str(txt_num) + " flie is done!")