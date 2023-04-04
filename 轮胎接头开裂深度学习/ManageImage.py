import numpy as np
from PIL import Image
import os
import os.path
import cv2
from xml.dom.minidom import parse
from PIL import Image, ImageFilter
import shutil


def getImageVar(imgPath):
    image = cv2.imread(imgPath);
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    cv2.imshow('out', image)
    return imageVar


def mange(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            xmlfilename = filename.strip('.jpg')
            oldXmlPath = "./xml/"+xmlfilename+".xml"
            currentPath = os.path.join(parent, filename)
            im = Image.open(currentPath)

            # out_horizontal = im.transpose(Image.FLIP_LEFT_RIGHT)      #水平翻转
            # horizontal_name = "./Image/A"+filename
            # newXmlPathA = "./xml/A"+xmlfilename+".xml"
            # print("水平变换新图像路径："+horizontal_name)
            # print("水平变换新xml路径："+newXmlPathA)
            # shutil.copyfile(oldXmlPath, newXmlPathA)
            # readXML(newXmlPathA, 1)
            # # out_horizontal.save(horizontal_name)
            #
            # out_vertical = im.transpose(Image.FLIP_TOP_BOTTOM)    #垂直翻转
            # vertical_name = "./Image/B" +filename
            # newXmlPathB = "./xml/B" + xmlfilename + ".xml"
            # print("垂直翻转新图像路径：" + vertical_name)
            # print("垂直翻转新xml路径：" + newXmlPathB)
            # shutil.copyfile(oldXmlPath, newXmlPathB)
            # readXML(newXmlPathB, 2)
            # # out_vertical.save(vertical_name)
            #
            # out_180 = im.transpose(Image.ROTATE_180)  # 180°翻转
            # out_180_name = "./Image/C" + filename
            # newXmlPathC = "./xml/C" + xmlfilename + ".xml"
            # print("180°翻转新图像路径：" + out_180_name)
            # print("180°翻转新xml路径：" + newXmlPathC)
            # shutil.copyfile(oldXmlPath, newXmlPathC)
            # readXML(newXmlPathC, 3)
            # out_180.save(out_180_name)

            gaoSi = im.filter(ImageFilter.GaussianBlur) # 高斯模糊
            newImagePath = "./After/GaussianBlur/GaussianBlur"+filename
            newXmlPath = "./xml/GaussianBlur/GaussianBlur"+xmlfilename+".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.BLUR)  # 普通模糊
            newImagePath = "./After/BLUR/BLUR" + filename
            newXmlPath = "./xml/BLUR/BLUR" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.EDGE_ENHANCE)  # 边缘增强
            newImagePath = "./After/EDGE_ENHANCE/EDGE_ENHANCE" + filename
            newXmlPath = "./xml/EDGE_ENHANCE/EDGE_ENHANCE" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.FIND_EDGES)  # 找到边缘
            newImagePath = "./After/FIND_EDGES/FIND_EDGES" + filename
            newXmlPath = "./xml/FIND_EDGES/FIND_EDGES" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.EMBOSS)  # 浮雕
            newImagePath = "./After/EMBOSS/EMBOSS" + filename
            newXmlPath = "./xml/EMBOSS/EMBOSS" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.CONTOUR)  # 轮廓
            newImagePath = "./After/CONTOUR/CONTOUR" + filename
            newXmlPath = "./xml/CONTOUR/CONTOUR" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.SHARPEN)  # 锐化
            newImagePath = "./After/SHARPEN/SHARPEN" + filename
            newXmlPath = "./xml/SHARPEN/SHARPEN" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.SMOOTH)  # 平滑
            newImagePath = "./After/SMOOTH/SMOOTH" + filename
            newXmlPath = "./xml/SMOOTH/SMOOTH" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

            gaoSi = im.filter(ImageFilter.DETAIL)  # 细节
            newImagePath = "./After/DETAIL/DETAIL" + filename
            newXmlPath = "./xml/DETAIL/DETAIL" + xmlfilename + ".xml"
            print("新图像路径：" + newImagePath)
            print("新xml路径：" + newXmlPath)
            shutil.copyfile(oldXmlPath, newXmlPath)
            gaoSi.save(newImagePath)

# 文件路径
def readXML(filePath,method):
    domTree = parse(filePath)
    # 文档根元素
    rootNode = domTree.documentElement
    # print(rootNode.nodeName)
    folder = rootNode.getElementsByTagName("folder")
    filename = rootNode.getElementsByTagName("filename")[0]

    path = rootNode.getElementsByTagName("path")
    sources = rootNode.getElementsByTagName("source")
    for source in sources:
        database = source.getElementsByTagName("database")[0]
        # print(database.childNodes[0].data)
    sizes = rootNode.getElementsByTagName("size")
    for size in sizes:
        width = size.getElementsByTagName("width")[0].childNodes[0].data
        height = size.getElementsByTagName("height")[0].childNodes[0].data
        depth = size.getElementsByTagName("depth")[0].childNodes[0].data
        # print(width.childNodes[0].data)
    segmented = rootNode.getElementsByTagName("segmented")
    objects = rootNode.getElementsByTagName("object")
    for object in objects:
        name = object.getElementsByTagName("name")[0]
        pose = object.getElementsByTagName("pose")[0]
        truncated = object.getElementsByTagName("truncated")[0]
        difficult = object.getElementsByTagName("difficult")[0]
        bndboxs = object.getElementsByTagName("bndbox")
        for bndbox in bndboxs:
            # 获取原值
            xmin= bndbox.getElementsByTagName("xmin")[0].childNodes[0].data
            ymin = bndbox.getElementsByTagName("ymin")[0].childNodes[0].data
            xmax = bndbox.getElementsByTagName("xmax")[0].childNodes[0].data
            ymax = bndbox.getElementsByTagName("ymax")[0].childNodes[0].data
            # print("{},{},{},{}".format(xmin, ymin, xmax, ymax))
            # 计算
            if method==1:
                newXmin,newYmin,newXmax,newYmax=horizontal(int(width),int(height),int(xmin), int(ymin),int(xmax),int(ymax))
                print("{},{},{},{}".format(newXmin, newYmin, newXmax, newYmax))
            elif method==2:
                newXmin, newYmin, newXmax, newYmax = vertical(int(width), int(height), int(xmin), int(ymin), int(xmax),int(ymax))
                print("{},{},{},{}".format(newXmin, newYmin, newXmax, newYmax))
            elif method==3:
                newXmin, newYmin, newXmax, newYmax = rotate(int(width), int(height), int(xmin), int(ymin), int(xmax), int(ymax))
                print("{},{},{},{}".format(newXmin, newYmin, newXmax, newYmax))
            # 修改新值
            bndbox.getElementsByTagName("xmin")[0].childNodes[0].data=newXmin
            bndbox.getElementsByTagName("ymin")[0].childNodes[0].data=newYmin
            bndbox.getElementsByTagName("xmax")[0].childNodes[0].data=newXmax
            bndbox.getElementsByTagName("ymax")[0].childNodes[0].data=newYmax
            # print("新修改："+str(bndbox.getElementsByTagName("xmin")[0].childNodes[0].data))
        # 重新写入xml
        with open(filePath, 'w') as f:
            # 缩进 - 换行 - 编码
            domTree.writexml(f,newl="\n",encoding='utf-8')


# 水平计算
def horizontal(width,height,xmin,ymin,xmax,ymax):
    temp = xmin
    xmin = width - xmax
    xmax = width - temp
    # print("{},{},{},{}".format(xmin, ymin,xmax,ymax))
    return xmin,ymin,xmax,ymax

def vertical(width,height,xmin,ymin,xmax,ymax):
    temp = ymin
    ymin = height - ymax
    ymax = height - temp
    return xmin, ymin, xmax, ymax

def rotate(width,height,xmin,ymin,xmax,ymax):
    temp = xmin
    xmin = width - xmax
    xmax = width - temp
    temp1 = ymin
    ymin = height - ymax
    ymax = height - temp1
    return xmin, ymin, xmax, ymax




if __name__ == "__main__":
    rootdir = './Image'  # 读取文件夹位置
    mange(rootdir)