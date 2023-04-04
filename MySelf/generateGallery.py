import os

def main(path):
    FileList = os.listdir(path)
    for files in FileList:
        oldDirPath = os.path.join(path, files)
        '如果是文件夹则递归调用'
        if os.path.isdir(oldDirPath):
            main(oldDirPath)
        '文件名'
        fileName = os.path.splitext(files)[0]
        '文件扩展名'
        fileType = os.path.splitext(files)[1]
        print("![](https://xiejy-image.oss-cn-shanghai.aliyuncs.com/gallery/%E5%B3%A8%E7%9C%89%E4%B9%8B%E8%A1%8C/"+fileName+fileType+")")


if __name__ == '__main__':
    path = "D:\\FirstRain\\DCIM\\2022newyear"
    main(path)
