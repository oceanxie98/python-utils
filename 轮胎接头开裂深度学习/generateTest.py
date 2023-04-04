def test():
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write(str(i) + '\n')
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write("A"+str(i) + '\n')
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write("B"+str(i) + '\n')
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write("C"+str(i) + '\n')
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write("EDGE_ENHANCE"+str(i) + '\n')
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write("GaussianBlur"+str(i) + '\n')
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write("SHARPEN"+str(i) + '\n')
    for i in range(60, 90):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test3.txt", "a+") as new_f:
            new_f.write("SMOOTH"+str(i) + '\n')

def normal():
    for i in range(1000,1040):
        with open("../../WorkSpace/faster-rcnn-keras/VOCdevkit/VOC2007/ImageSets/Main/test2.txt", "a+") as new_f:
            new_f.write(str(i) + '\n')

def generateTxt():
    for i in range(1001,1041):
        file = open("../../WorkSpace/faster-rcnn-keras/input/ground-truth/"+str(i)+".txt", "a+")
        file.close()

if __name__=="__main__":
    normal()




