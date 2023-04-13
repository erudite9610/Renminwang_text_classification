# _*_ coding = utf-8 _*_
# @Time : 2023/3/8 23:33
# @Author : Yoimiya
# @File : Q1_LSTM_model.py
# @Software : Pycharm

import torch
from torch import optim
from data_preparer import get_dataloader
import lib
from lib import ws
import os
import numpy
import json

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class Simple_model(torch.nn.Module):
    def __init__(self):
        super(Simple_model, self).__init__()
        self.embedding = torch.nn.Embedding(len(ws), lib.len_word_vector)
        self.lstm_1 = torch.nn.LSTM(input_size=lib.len_word_vector, hidden_size=lib.lstm_unit_num_1,
                                    num_layers=lib.lstm_num_layer_1, bidirectional=True, batch_first=True,
                                    dropout=lib.dropout)
        self.lstm_2 = torch.nn.LSTM(input_size=lib.lstm_unit_num_1 * 2, hidden_size=lib.lstm_unit_num_2,
                                    num_layers=lib.lstm_num_layer_2, bidirectional=False, batch_first=True,
                                    dropout=lib.dropout)
        self.full_connection_layer_1 = torch.nn.Linear(lib.lstm_unit_num_2, lib.full_connection_layer_1_output)
        self.full_connection_layer_2 = torch.nn.Linear(lib.full_connection_layer_1_output, lib.final_output)

    def forward(self, input):
        x = self.embedding(input.to(device)).to(device)  # 进行embedding操作，形状(batch_size,sentence_length,vector_length)
        # shape:  h,c[number_layer*direction,batch_size,lstm_unit_num]
        output, (hidden_layer, cell) = self.lstm_1(x)
        # 获取两个方向最后一次的output
        # output_forward = hidden_layer[-2, :, :]
        # output_backward = hidden_layer[-1, :, :]
        # output = torch.cat([output_forward, output_backward], dim=-1)  # [batch_size,hidden_size*2]
        output, (hidden_layer, cell) = self.lstm_2(output)
        output = hidden_layer[-1, :, :]
        output = self.full_connection_layer_1(output)
        output = self.full_connection_layer_2(output)
        return torch.nn.functional.log_softmax(output, dim=-1)


simple_model = Simple_model().to(device)
optimizer = torch.optim.Adam(simple_model.parameters(), 0.001)
if os.path.exists(r"./models/lstm_model_%s.pkl" % lib.current_training):
    simple_model.load_state_dict(torch.load("./models/lstm_model_%s.pkl" % lib.current_training))
    optimizer.load_state_dict(torch.load("./models/lstm_optimizer_%s.pkl" % lib.current_training))


def train(epoch):
    for idx, (input, label) in enumerate(get_dataloader(train=True)):
        optimizer.zero_grad()  # 梯度归零
        output = simple_model(input).to(device)
        criteria = torch.nn.CrossEntropyLoss()  # 多分类使用CrossEntropyLoss
        loss = criteria(output, label.to(device))
        loss.backward()
        optimizer.step()
        print(epoch, idx, loss.item())

        if idx % 100 == 0:
            torch.save(simple_model.state_dict(), "./models/lstm_model_%s.pkl" % lib.current_training)
            torch.save(optimizer.state_dict(), "./models/lstm_optimizer_%s.pkl" % lib.current_training)


def eval():
    loss_list = []
    acc_list = []
    for index, (input, label) in enumerate(get_dataloader(train=False)):
        input = input.to(device)
        label = label.to(device)
        with torch.no_grad():
            output = simple_model(input)
            criteria = torch.nn.CrossEntropyLoss()  # 多分类使用CrossEntropyLoss
            current_loss = criteria(output, label.to(device))
            loss_list.append(current_loss.item())
            pred = output.max(dim=-1)[-1]
            current_acc = pred.eq(label).float().mean()
            acc_list.append(current_acc.item())
    print("total_loss,acc:", numpy.mean(loss_list), numpy.mean(acc_list))


def pred():
    pred_dict = {}
    for index, (input, tid) in enumerate(get_dataloader(train=False)):
        input = input.to(device)
        with torch.no_grad():
            output = simple_model(input)
            pred = output.max(dim=-1)[-1].tolist()
        for i in range(0, len(pred)):
            pred_dict[list(tid)[i]] = pred[i]
    print(len(pred_dict))
    json.dump(pred_dict, open(r"./predict_result/%s.json" % lib.current_training, mode='w', encoding='utf-8'))


if lib.mode == "train_test":
    for i in range(lib.epoch_num):
        train(i)
    eval()
else:
    pred()
