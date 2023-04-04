from keras.layers import Input
from frcnn import FRCNN 
from PIL import Image
from tensorflow.contrib.slim import nets
import tensorflow as tf
import keras
import time

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# keras.backend.tensorflow_backend.set_session(tf.Session(config=config))
slim = tf.contrib.slim
frcnn = FRCNN()

# with slim.arg_scope(nets.resnet_v1.resnet_arg_scope()):
#     net, endpoints = nets.resnet_v1.resnet_v1_50(inputs, num_classes=None,
#                                                  is_training=is_training)

while True:
    img = input('Input image filename:')
    try:
        image = Image.open("img/"+img+'.jpg')
        # image = Image.open(img)
    except:
        print('Open Error! Try again!')
        continue
    else:
        start = time.ctime()
        r_image = frcnn.detect_image(image.convert('RGB'))
        out = time.ctime()
        print(start)
        print(out)
        r_image.show()
frcnn.close_session()
    