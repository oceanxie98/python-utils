#----------------------------------------------------#
#   获取测试集的ground-truth
#   具体视频教程可查看
#   https://www.bilibili.com/video/BV1zE411u7Vw
#----------------------------------------------------#
import sys
import os
import glob
import xml.etree.ElementTree as ET

image_ids = open('VOCdevkit/VOC2007/ImageSets/Main/train.txt').read().strip().split()
path="./input"
if not os.path.exists(path):
    os.makedirs(path)
if not os.path.exists(path+"/ground-truth"):
    os.makedirs(path+"/ground-truth")

for image_id in image_ids:
    with open(path+"/ground-truth/"+image_id+".txt", "w") as new_f:
        # root = ET.parse("VOCdevkit/VOC2007/Annotations/"+image_id+".xml").getroot()
        root = ET.parse("../ImageGenerator/AllXml/" + image_id + ".xml").getroot()
        for obj in root.findall('object'):
            obj_name = obj.find('name').text
            bndbox = obj.find('bndbox')
            left = bndbox.find('xmin').text
            top = bndbox.find('ymin').text
            right = bndbox.find('xmax').text
            bottom = bndbox.find('ymax').text
            new_f.write("%s %s %s %s %s\n" % (obj_name, left, top, right, bottom))
print("Conversion completed!")