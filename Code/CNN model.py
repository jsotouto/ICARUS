# 라이브러리 소환
import numpy as np
import tensorflow as tf
import tflearn

import glob
import sys

from sklearn.model_selection import train_test_split
from tf.learn.layers.core import input_data, dropot, fully_connected
from tf.learn.layers.conv import conv_2d, max_pool_2d
from tf.learn.layers.normalization import local_response_normalization
from tf.learn.layers.estimator import regression
from matplotlib import pyplot as plt


# 데이터셋 제작

x_train = np.empty((0, 120, 320))
y_train = np.empty((0, 4))
training_data = glob.glob('./training_data/*.npz') #<경로>

for single_npz in training_data:
     with np.load(single_npz) as data:
        x = data['train']
        y = data['train_labels']
     x_train = np.vstack((x_train, x))
     y_train = np.vstack((y_train, y))

x_train=x_train.reshape(-1,120,320,1)

# train test split, 7:3
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.3)

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

# 데이터 확인

get_ipython().run_line_magic('matplotlib', 'inline')

plt_row = 3
plt_col = 3

plt.rcParams["figure.figsize"] = (10,10)

f, axarr = plt.subplots(plt_row, plt_col)

for i in range(plt_row*plt_col):

    sub_plt = axarr[i/plt_row, i%plt_col]
    sub_plt.axis('off')
    sub_plt.imshow(x_train[i].reshape(120, 320))
    sub_plt_title = 'R: ' + str(np.argmax(y_train[i]))
    sub_plt.set_title(sub_plt_title)

plt.show()

tf.clear_session()

# 모델 구성 ---------------------여기부터 수정-------------------------

def lrelu(x, leak=0.2, name='lrelu'):
    with tf.variable_scope(name):
        f1 = 0.5 * (1 + leak)
        f2 = 0.5 * (1 - leak)
        return f1 * x + f2 * abs(x)

     
def ICANet():
     
     CNN = input_data(shape[None, 120, 320,1], name='input')
     
     #합성곱
     CNN = conv_2d(CNN, 32 ,5, activation='relu', strides=2, regularizer="L2")
     CNN = max_pool_2d(CNN,2)
     CNN = local_response_normaliztion(CNN)
     CNN = conv_2d(CNN, 64 ,5, activation='relu', strides=2, regularizer="L2")
     CNN = max_pool_2d(CNN,2)
     CNN = local_response_normaliztion(CNN)
     CNN = conv_2d(CNN, 96 ,5, activation='relu', strides=2, regularizer="L2")
     CNN = max_pool_2d(CNN,2)
     CNN = local_response_normaliztion(CNN)
     CNN = conv_2d(CNN, 128, 4 , activation='relu', regularizer="L2")
     CNN = max_pool_2d(CNN,2)
     CNN = local_response_normaliztion(CNN)
     CNN = conv_2d(CNN, 128, 4 , activation='relu', regularizer="L2")
     CNN = max_pool_2d(CNN,2)
     CNN = local_response_normaliztion(CNN)
     
     #FC layer
     CNN = fully_connected(CNN, 1024, activation=None)
     CNN = dropout(CNN, 0.5)
     CNN = fully_connected(CNN, 10 ,activation='softmax')
     CNN = regression(CNN, optimizer='adam', learning_rate=0.0001,
                      loss='categorical_crossentropy', name='target')

     model = tf.learn.DNN(CNN, tensorboard_verbose=0,
                          tensorboard_dir = 'MNIST_tflearn_board/',
                          checkpoint_path = 'MNIST_tflearn_checkpoints/checkpoint')
     model.fit({'input':x_train}, {'target':y_train}, n_epoch=3,
               validation_set=({'input':x_test}, {'target':y_test}),
               snapshot_step=1000,show_metric=True, run_id='convnet_run')
        
