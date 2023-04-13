# _*_ coding = utf-8 _*_
# @Time : 2023/3/3 19:18
# @Author : Yoimiya
# @File : data_preparer.py
# @Software : Pycharm

import json

import torch
from torch.utils.data import DataLoader, Dataset
import random
import jieba
import re
import os
import lib
from lib import ws


def segment_content(content):
    stop_words = list(open(r"./stop_words.txt", mode="r", newline="").readlines())
    filters = ["，", "。", "！", "”", "“", "？", "：","（","）"]
    content = re.sub("|".join(filters), "", content)
    seg = [k for k in jieba.lcut(content) if k not in stop_words]
    return seg


"""
导入数据
:return:列表数据集
"""


def generate_train_set(train_set_propotion):
    """
    :param train_set_propotion:
    :return: train&test_set_json
    :param train_set_propotion: 定义训练集比例
    :param querstion_no:问题编号
    :return:
    """
    data_file_list = os.listdir(r"./Q_data_set")
    for data_file in data_file_list:
        data_file_path = os.path.join(r"./Q_data_set", data_file)
        data_primal = json.load(open(data_file_path, mode="r", encoding="utf-8"))
        train_set_json = {}
        test_set_json = {}

        len_data_primal = len(data_primal)
        len_train_set = int(train_set_propotion * len_data_primal)
        L = [x for x in range(0, len_train_set)]
        random.shuffle(L)
        L = L[0:len_train_set]
        # print(L)
        # print(len_train_set)

        for idx, item in enumerate(data_primal.items()):
            if idx in L:
                train_set_json[item[0]] = item[1]
            else:
                test_set_json[item[0]] = item[1]
        train_and_test_set_json = {'train': train_set_json, "test": test_set_json}
        with open(r"./train_set_data/%s" % data_file, mode="w", encoding="utf-8", newline="") as f:
            f.write(json.dumps(train_and_test_set_json))


generate_train_set(0.90)

class renminwangDataset(Dataset):
    def __init__(self, train=True):
        train_and_test_set_file = open(r"./%s/%s_dataset.json" % (lib.path, lib.current_training), mode="r",
                                       encoding="utf-8", newline="").read()
        self.train_and_test_set_json = json.loads(train_and_test_set_file)
        self.train_set_json = self.train_and_test_set_json["train"]
        self.test_set_json = self.train_and_test_set_json["test"]
        if train:
            self.data_json = self.train_set_json
        else:
            self.data_json = self.test_set_json

    def __getitem__(self, index):
        # 获取label
        # if question_id !=3:
        #     label = self.data_json.values()[index]["question"][question_id]
        # else:
        #     label = self.data_json.values()[index]["question"][question_id][question_id_sub]

        if lib.mode != "predict":
            content = list(self.data_json.values())[index]['content']
            content = segment_content(content)
            label = int(list(self.data_json.values())[index]["label"])
            if lib.current_training == "Q1":
                if label == 2:
                    label = 1
                # 获取内容
            elif lib.current_training == "Q2":
                if label == 1:
                    label = 0
                elif label == 2 or label == 6:
                    label = 1
                elif label == 4:
                    label = 2
                elif label == 5:
                    label = 3
                elif label == 3 or label == 7 or label == 9:
                    label = 4
            return content, label
        else:
            content = list(self.data_json.values())[index]['content']
            content = segment_content(content)
            tid = list(self.data_json.keys())[index]
            return content, tid

    def __len__(self):
        return len(self.data_json)

    """
    通过修改collate_fn方法解决数据异常问题
    """


def collate_fn(batch):
    """
        :param batch: ([jieba,label],[jieba,label],......,[jieba,label])
        :return:
        """
    content, label = list(zip(*batch))
    content = [ws.sentence2numsequence(sentence=sentence, max_len=lib.max_len) for sentence in content]
    content = torch.LongTensor(content)
    if lib.mode == "train_test":
        label = torch.LongTensor(label)
    return content, label


def get_dataloader(train=True):
    renminwangdataset = renminwangDataset(train=train)
    data_loader = DataLoader(dataset=renminwangdataset, batch_size=lib.batch_size, shuffle=True, collate_fn=collate_fn)
    return data_loader

# for idx, (input, target) in enumerate(get_dataloader(train=True)):
#     print(idx)
#     print(input)
#     print(target)
#     break
