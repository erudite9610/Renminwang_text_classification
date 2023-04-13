# _*_ coding = utf-8 _*_
# @Time : 2023/3/6 1:21
# @Author : Yoimiya
# @File : save_word2sequence.py
# @Software : Pycharm

from word_embedding import word2sequence
from data_preparer import segment_content
import json
import pickle
import os


def save_word2sequence(dataset):
    """
    :param datapath: train_set_data文件夹内的文件名
    :return:
    """
    datapath = os.path.join(r"./train_set_data",dataset)
    file = open(datapath, mode="r", encoding="utf-8", newline="")
    str = file.read()
    file_json = json.loads(str)
    ws = word2sequence()
    for value_set in file_json.values():
        for value_sentence in value_set.values():
            sentence = value_sentence['content']
            sentence_seg = segment_content(sentence)
            # print(sentence_seg)
            ws.fit(sentence_seg)
    ws.bulid_vocab(min_frequence= 3,max_features=None)
    pickle.dump(ws,open(r"./models/ws_%s.pkl"%dataset[:-5],"wb"))
    print(len(ws))

# data_set_list = os.listdir(r"./train_set_data")
# for dataset in data_set_list:
#     save_word2sequence(dataset)