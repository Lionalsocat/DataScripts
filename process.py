import os
import random
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import math

train_percent = 0.8                         #训练集比例, 与valid_percent相加为1
valid_percent = 0.2                         #验证集比例, 与train_percent相加为1
suffix='.jpg'                               #图片后缀名

sets = ['train','valid']                    #输出结果集合
labelfilepath = './labels'                  #labels存储路径
txtsavepath = './ImageSets'                 #输出的txt存储路径
total_label = os.listdir(labelfilepath)
 
if not os.path.exists('ImageSets/'):
    os.makedirs('ImageSets/')
 
def StepOne():
    num = len(total_label)
    list = range(num)
    train_num = int(num * train_percent)
    valid_num = int(num * valid_percent)
    train_list = random.sample(list, train_num)

    ftrain = open('ImageSets/train.txt', 'w')
    fvalid = open('ImageSets/valid.txt', 'w')

    for i in list:
        name = total_label[i][:-4] + '\n'
        if i in train_list:
            ftrain.write(name)
        else:
            fvalid.write(name)

    ftrain.close()
    fvalid.close()

def StepTow():
    if not os.path.exists('images/'):
        os.makedirs('images/')
    for image_set in sets:
        image_ids = open('ImageSets/%s.txt' % (image_set)).read().strip().split()
        list_file = open('%s.txt' % (image_set), 'w')
        for image_id in image_ids:
            list_file.write('data/images/%s%s\n' % (image_id,suffix))
        list_file.close()

if __name__ == "__main__":
    StepOne()
    StepTow()
    