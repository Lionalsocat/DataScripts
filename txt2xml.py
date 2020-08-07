import os, sys
import glob
from PIL import Image

img_path = "./JPEGImages"       # 图像存储位置
txt_path = "./labels"           # txt文件存储位置
xml_path = "./Annotations"      # xml存储位置
classes = ["", ""]              # 获得对应ID，要和txt格式中类别对应起来
suffix = ".jpg"                 # 图片后缀名

if not os.path.exists(xml_path):
    os.makedirs(xml_path)
    
# 坐标转换   (x, y, w, h)-<归一化的中心点坐标和框的宽高>   转换为  （xmin, ymin, xmax, ymax)-<左上和右下坐标>
def convert(x, y, w, h):
    x_min = int(width * (float(x) - float(w)/2 ))
    y_min = int(height * (float(y) - float(h)/2 ))
    x_max = int(width * (float(x) + float(w)/2 ))
    y_max = int(height * (float(y) + float(h)/2 ))
    return (x_min, y_min, x_max, y_max)
    
img_Lists = glob.glob(img_path + '/*' + suffix)
 
img_basenames = [] # e.g. 100.jpg
for item in img_Lists:
    img_basenames.append(os.path.basename(item))
 
img_names = [] # e.g. 100
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)
 
for img in img_names:
    im = Image.open((img_path + '/' + img + suffix))
    width, height = im.size
 
    # 打开图片对应的txt文件  并且按照每一行为一个元素存入 img_all_label 数组中！
    img_all_label = open(txt_path + '/' + img + '.txt').read().splitlines()
 
    # 在xml中写入基本信息
    xml_file = open((xml_path + '/' + img + '.xml'), 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <filename>' + str(img) + suffix + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')
    xml_file.write('    <segmented>0</segmented>\n')
 
    # 在xml中写入位置信息
    for img_each_label in img_all_label:
        spt = img_each_label.split(' ') 
        # 如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
        # spt中存储的是 {label，x，y，w，h}
            
        xml_file.write('    <object>\n')
        xml_file.write('        <name>'+classes[int(spt[0])]+'</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        # 转换坐标         
        box = convert(spt[1], spt[2], spt[3], spt[4])            
        xml_file.write('            <xmin>' + str(box[0]) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(box[1]) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(box[2]) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(box[3]) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')
    xml_file.write('</annotation>')

# 已生成的xml总数
xml_num = len([lists for lists in os.listdir(xml_path) if os.path.isfile(os.path.join(xml_path, lists))])
print(str(xml_num) + " file is done!")