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
        '新的文件路径'
        newDirPath = os.path.join("D:\Users\toreador\Desktop", "存储虚拟化-"+fileName + fileType)
        '重命名'
        os.rename(oldDirPath, newDirPath)
        print(newDirPath)


if __name__ == '__main__':
    path = "D:\Users\toreador\Desktop\存储虚拟化要求"
    main(path)
