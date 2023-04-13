# _*_ coding = utf-8 _*_
# @Time : 2023/3/17 16:16
# @Author : Yoimiya
# @File : print_network.py
# @Software : Pycharm

import keras
from keras.layers import Input, Embedding, Bidirectional, LSTM, Dense, concatenate
from keras.models import Model
from keras.utils.vis_utils import plot_model

import lib
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# 输入层
# 输入层
inputs = Input(shape=(lib.max_len, ),batch_size=128)

# 嵌入层
embedding_layer = Embedding(input_dim=lib.max_len, output_dim=lib.len_word_vector,input_length=128)(inputs)

# 双向LSTM层
lstm_layer = Bidirectional(LSTM(units=18, return_sequences=True))(embedding_layer)

# 全连接层1
dense_layer_1 = Dense(units=64, activation='relu')(lstm_layer)

# 全连接层2
dense_layer_2 = Dense(units=32, activation='relu')(dense_layer_1)

# 输出层
output_layer = Dense(units=lib.final_output, activation='softmax')(dense_layer_2)

# 定义模型
model = Model(inputs=inputs, outputs=output_layer)

# 绘制模型示意图
plot_model(model, to_file='lstm_model.png', show_shapes=True, show_layer_names=True)

# 显示模型示意图
from IPython.display import Image
Image(filename='lstm_model.png')
