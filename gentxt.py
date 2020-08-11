import os
import glob

train_img_path = "./images/train"       # 训练集图像存储位置
valid_img_path = "./images/valid"       # 验证集图像存储位置 
suffix = ".jpg"                         # 图片后缀名 
    
train_img_Lists = glob.glob(train_img_path + '/*' + suffix)
valid_img_Lists = glob.glob(valid_img_path + '/*' + suffix)

# 生成train.txt
train_img_basenames = [] # e.g. 100.jpg
for item in train_img_Lists:
    train_img_basenames.append(os.path.basename(item)) 

train_img_names = [] # e.g. 100
for item in train_img_basenames:
    temp1, temp2 = os.path.splitext(item)
    train_img_names.append(temp1)
 
train_file = open("train.txt", 'w')
for img in train_img_names:
    train_file.write("data/images/train/"+ img + suffix + '\n')
print("Generating train.txt succeed!")

# 生成valid.txt
valid_img_basenames = [] # e.g. 100.jpg
for item in valid_img_Lists:
    valid_img_basenames.append(os.path.basename(item)) 

valid_img_names = [] # e.g. 100
for item in valid_img_basenames:
    temp1, temp2 = os.path.splitext(item)
    valid_img_names.append(temp1)
 
valid_file = open("valid.txt", 'w')
for img in valid_img_names:
    valid_file.write("data/images/valid/"+ img + suffix + '\n')
print("Generating valid.txt succeed!")