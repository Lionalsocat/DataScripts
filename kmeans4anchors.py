import numpy as np
import xml.etree.ElementTree as ET
import glob
import random

xml_path = "./Annotations"    # xml文件存储位置
anchors_num = 9               # 锚框（anchors box) 个数，默认9个，3个大小的尺度，每个尺度3个锚框

def cas_iou(box,cluster):
    x = np.minimum(cluster[:,0],box[0])
    y = np.minimum(cluster[:,1],box[1])

    intersection = x * y
    area1 = box[0] * box[1]

    area2 = cluster[:,0] * cluster[:,1]
    iou = intersection / (area1 + area2 -intersection)

    return iou

def avg_iou(box,cluster):
    return np.mean([np.max(cas_iou(box[i],cluster)) for i in range(box.shape[0])])


def kmeans(box,k):
    # box.shape[0]计算一共有多少框，box为（[w1, h1], [w2, h2], .....)
    row = box.shape[0]
    
    # 初始化distance数组为空
    distance = np.empty((row,k))
    
    # 初始化最后的聚类位置
    last_clu = np.zeros((row,))

    # 随机选9个框当聚类中心
    np.random.seed()
    # 从大小为row的数字中随机组成k维数组，replace = False表示不能随机到相同的数字
    cluster = box[np.random.choice(row,k,replace = False)]  

    while True:
        # 计算每一行距离九个点的iou情况
        for i in range(row):
            distance[i] = 1 - cas_iou(box[i],cluster)
        
        # 取出最小点
        near = np.argmin(distance,axis=1)

        if (last_clu == near).all():
            break
        
        # 求每一个类的中位点
        for j in range(k):
            cluster[j] = np.median(
                box[near == j],axis=0)

        last_clu = near

    return cluster

# 读取数据，返回所有bounding box的宽高到data数组中
def load_data(path):
    data = []
    # 对于每一个xml都寻找box
    for xml_file in glob.glob('{}/*xml'.format(path)):
        tree = ET.parse(xml_file)
        height = int(tree.findtext('./size/height'))
        width = int(tree.findtext('./size/width'))
        # 对于每一个目标都获得它的宽高
        for obj in tree.iter('object'):
            xmin = int(float(obj.findtext('bndbox/xmin'))) / width
            ymin = int(float(obj.findtext('bndbox/ymin'))) / height
            xmax = int(float(obj.findtext('bndbox/xmax'))) / width
            ymax = int(float(obj.findtext('bndbox/ymax'))) / height

            xmin = np.float64(xmin)
            ymin = np.float64(ymin)
            xmax = np.float64(xmax)
            ymax = np.float64(ymax)
            # 得到宽高，加入数组中，数组包含了所有图片的所有框
            data.append([xmax-xmin,ymax-ymin])
    return np.array(data)


if __name__ == '__main__':
    SIZE = 416   
    # 载入所有xml格式的数据集, 返回值为按比例转换后的width和height
    data = load_data(xml_path)
    
    # 使用k聚类算法
    out = kmeans(data,anchors_num)
    out = out[np.argsort(out[:,0])]
    print('acc:{:.2f}%'.format(avg_iou(data,out) * 100))
    print(out*SIZE)
    data = out*SIZE
    f = open("anchors.txt", 'w')
    row = np.shape(data)[0]
    for i in range(row):
        if i == 0:
            x_y = "%d,%d" % (data[i][0], data[i][1])
        else:
            x_y = ", %d,%d" % (data[i][0], data[i][1])
        f.write(x_y)
    f.close()