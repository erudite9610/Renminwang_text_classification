# @*-*coding = utf-8 *-*
# @Author sukuya
# @Software: PyCharm
# @Time:2023/3/7 18:51
# @File:training_data_preparer.py

import json
import csv
import os
import re

# 准备第一题总测试集、训练集文件
correct_file = json.load(open(r"./correct_id.json", mode="r", encoding='utf-8'))
wrong_file = json.load(open(r"./wrong_id.json", mode="r", encoding='utf-8'))
filelist = [correct_file, wrong_file]


def Q1():
    Q1_json = {}

    for item in wrong_file.items():
        value = item[1]
        id = item[0]
        content = value['content']
        label_list = value["question"]
        if len(label_list) == 2:
            if label_list[0][0] == label_list[1][0]:
                label = label_list[0][0]
            else:
                label = None
        if label:
            Q1_json[id] = {"label": label, "content": content}
    for item in correct_file.items():
        value = item[1]
        id = item[0]
        content = value['content']
        label = value["question"][0]
        Q1_json[id] = {"label": label, "content": content}

    print(len(Q1_json))
    with open(r"./Q1_dataset.json", mode="w") as f:
        json.dump(Q1_json, f)


def Q2():
    Q2_json = {}
    for item in correct_file.items():
        value = item[1]
        id = item[0]
        content = value['content']
        Q1 = int(value["question"][0])
        if Q1 != 0:
            label = int(value["question"][1])
        else:
            label = None
        if label:
            Q2_json[id] = {"label": label, "content": content}
    print(len(Q2_json))
    with open(r"./Q2_dataset.json", mode="w") as f:
        json.dump(Q2_json, f)


def Q4_10():
    for i in range(4, 11):
        Q_json = {}
        for item in correct_file.items():
            value = item[1]
            id = item[0]
            content = value['content']
            Q1 = int(value["question"][0])
            Q_num = i - 1
            if Q1 != 0:
                label = (value["question"][Q_num])
            else:
                label = None
            if label:
                Q_json[id] = {"label": label, "content": content}
        print(len(Q_json))
        with open(r"./Q%d_dataset.json" % i, mode="w") as f:
            json.dump(Q_json, f)


def Q3():

    for i in range(1, 7):
        Q3_json = {}
        for item in correct_file.items():
            value = item[1]
            id = item[0]
            content = value['content']
            Q1 = int(value["question"][0])
            if Q1 != 0:
                label =list(value["question"][2])
                label = [label[2],label[7],label[12],label[17],label[22],label[27]]
            else:
                label = None
            if label:
                Q3_label =label[i-1]
                Q3_json[id] = {"label": Q3_label, "content": content}
        print(len(Q3_json))
        with open(r"./Q3%d_dataset.json" % i, mode="w") as f:
            json.dump(Q3_json, f)


# Q3()
# Q4_10()
# Q2()