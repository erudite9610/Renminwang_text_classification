# _*_ coding = utf-8 _*_
# @Time : 2023/3/6 1:24
# @Author : Yoimiya
# @File : lib.py
# @Software : Pycharm

import pickle

ws = pickle.load(open(r"./models/ws.pkl", "rb"))
max_len = 300
batch_size = 128
test_batch_size = 1024
len_word_vector = 150
current_training = "Q36"
if current_training != "Q2":
    final_output = 2
    epoch_num = 10
else:
    final_output = 5
    epoch_num = 30
lstm_unit_num_1 = 18
lstm_num_layer_1 = 2
lstm_unit_num_2 = 18
lstm_num_layer_2 = 2
dropout = 0.5
full_connection_layer_1_output = 10

'''
mode = predict或者train_test
'''
mode = "predict"
# mode = "train_test"
if mode == "predict":
    path = "unpredicted"
elif mode == "train_test":
    path = "train_set_data"
