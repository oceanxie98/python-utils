import os

def main():
    path = "D:\Sugon\全栈云\文档\全栈云白皮书\全栈云接口文档\html"
    files = os.listdir(path)
    for filename in files:
        oldname = path + '/' + filename

        print(filename)
        # newname=path + '/huawei4_manageCluster_' + filename
        # os.rename(oldname, newname)

def renamefile():
    path = "D:/Sugon/全栈云/文档/全栈云白皮书/全栈云接口文档/html"
    files = os.listdir(path)
    for filename in files:
        oldname = path + '/' + filename
        newname = filename.replace("-router-default", "接口文档")
        newfile=path + '/' + newname
        # print(newfile)
        os.rename(oldname, newname)

if __name__ == '__main__':
    renamefile()