# _*_ coding = utf-8 _*_
# @Time : 2023/3/5 22:35
# @Author : Yoimiya
# @File : word_embedding.py
# @Software : Pycharm

class word2sequence():
    UNK_TAG = "UNK"  # 未出现的词语，特殊字符
    PAD_TAG = "PAD"  # 填充短句子的特殊符号
    UNK = 0
    PAD = 1

    def __init__(self):
        self.vocab_dict = {
            self.UNK_TAG: self.UNK,
            self.PAD_TAG: self.PAD
        }
        self.count_dict = {}
        self.inverse_dict = {}

    def fit(self, sentence):
        """
        把一个分好词的句子保存到dict中,并统计词频
        :param sentence:[word1,word2,......,wordN]
        :return:
        """
        for word in sentence:
            self.count_dict[word] = self.count_dict.get(word, 0) + 1

    def bulid_vocab(self, min_frequence=5, max_frequence=None, max_features=None):
        """
        :param min_frequence:保留的词，至少要出现多少次
        :param max_frequence:保留的词，至多出现多少次
        :param max_features:至多保留的词语数
        :return:
        """
        # 删除count_dict中小于min_frequence的词
        if min_frequence:
            self.count_dict = {word: value for word, value in self.count_dict.items() if value >= min_frequence}
        if max_frequence:
            self.count_dict = {word: value for word, value in self.count_dict.items() if value <= max_frequence}
        if max_features:
            temp = sorted(self.count_dict.items(), key=lambda x: x[-1], reverse=True)[:max_features]
            self.count_dict = dict(temp)
        for word in self.count_dict.keys():
            self.vocab_dict[word] = len(self.vocab_dict)
        # 反转字典
        self.inverse_dict = dict(zip(self.vocab_dict.values(), self.vocab_dict.keys()))

    def sentence2numsequence(self, sentence, max_len=None):
        """
        :param sentence:[word1,word2,......,wordN]
        :param max_len: 对句子进行规范化长度，填充或裁剪
        :return:
        """
        if max_len:
            while len(sentence) > max_len:
                sentence = sentence[:-1]
            while len(sentence) < max_len:
                sentence.append(self.PAD_TAG)

        numsequence = []
        for word in sentence:
            if word in self.vocab_dict.keys():
                numsequence.append(self.vocab_dict[word])
            else:
                numsequence.append(self.UNK)
        return numsequence

    def numsequnece2sentence(self, numbersequence):
        sentence = []
        return [self.inverse_dict.get(idx) for idx in numbersequence]

    def __len__(self):
        return len(self.vocab_dict)


"""
以下为测试代码
"""
# ws = word2sequence()
# ws.fit(['甲','乙','丙'])
# ws.fit(['丙','丁'])
# ws.bulid_vocab(min_frequence=0,max_features=1)
# print(ws.count_dict)
# print(ws.vocab_dict)
# print(ws.sentence2numsequence(["甲",'丙',"戊"],max_len=10))
# print(ws.numsequnece2sentence([1,5,3,0,4,0]))
"""
以上为测试代码
"""
