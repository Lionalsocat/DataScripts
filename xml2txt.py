import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd
from os.path import join
from PIL import Image

img_path = "./JPEGImages"       # 图像存储位置
txt_path = "./labels"           # txt文件存储位置
xml_path = "./Annotations"      # xml存储位置
classes = ["", ""]              # 获得对应ID，要和xml格式中类别对应起来
suffix = ".jpg"                 # 图片后缀名
  
if not os.path.exists(txt_path):
	os.makedirs(txt_path)
	
# 坐标转换   （xmin, ymin, xmax, ymax)-<左上和右下坐标>   转换为   (x, y, w, h)-<归一化的中心点坐标和框的宽高>   
def convert(size, box):
	dw = 1. / (size[0])
	dh = 1. / (size[1])
	x = (box[0] + box[1]) / 2.0 
	y = (box[2] + box[3]) / 2.0 
	w = box[1] - box[0]
	h = box[3] - box[2]
	x = x * dw
	w = w * dw
	y = y * dh
	h = h * dh
	return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open(xml_path + '/%s.xml' % (image_id),'rb')       # 输入文件xml
    out_file = open(txt_path + '/%s.txt' % (image_id), 'w')      # 输出文件txt
    
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')

    # 如果xml中没有size字段，则从图片中读取w和h, 不然则从xml中读取
    if size == None:      
        img = Image.open(img_path + '/' + image_id + suffix)
        w, h = img.size  
        print('{}.xml缺失size字段, 读取{}{}图片得到对应 w：{} h：{}'.format(image_id, image_id,suffix, w, h))       
    else:
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        
    for obj in root.iter('object'):
        # 获取类别名
        cls = obj.find('name').text
        if cls not in classes:
            continue
        # 查找类别对应的索引
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
            float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                
if __name__=='__main__':   		
	list_file = os.listdir(img_path)    
	for file in list_file:
		image_id = file.split('.')[0]
		convert_annotation(image_id)
		
	# 已生成的txt总数 
	txt_num = len([lists for lists in os.listdir(txt_path) if os.path.isfile(os.path.join(txt_path, lists))])
	print(str(txt_num)+" flie is done!")
