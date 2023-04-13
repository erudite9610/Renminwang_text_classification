# @*-*coding = utf-8 *-*
# @Author sukuya
# @Software: PyCharm
# @Time:2023/3/10 10:39
# @File:summarize.py
import csv
import datetime
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
csv_file = open(r"./final_data.csv", mode="r", encoding="utf-8", newline="")
csv_reader = list(csv.reader(csv_file))
data_dict = {}
Question_dict = {"Q1": {}, "Q2": {}, "Q31": {}, "Q32": {}, "Q33": {}, "Q34": {}, "Q35": {}, "Q36": {}, "Q4": {},
                 "Q5": {}, "Q6": {}, "Q7": {}, "Q8": {}, "Q9": {}, "Q10": {}}
"""
按时间、省份和问题汇总
"""
Variable_list = csv_reader[0]
Question_name_list = csv_reader[0][5:]
for row in csv_reader[1:]:
    time = datetime.datetime.strptime(row[1], "%Y/%m/%d")
    year = time.year
    prov = row[2]
    if int(row[5]) == 1 or int(row[5]) == 2:
        if year not in data_dict.keys():
            data_dict[year] = {
                prov: {"Q1": {}, "Q2": {}, "Q31": {}, "Q32": {}, "Q33": {}, "Q34": {}, "Q35": {}, "Q36": {}, "Q4": {},
                       "Q5": {}, "Q6": {}, "Q7": {}, "Q8": {}, "Q9": {}, "Q10": {}}}
            for i in range(0, 15):
                label = row[i + 5]
                if label in data_dict[year][prov][Question_name_list[i]].keys():
                    data_dict[year][prov][Question_name_list[i]][label] = data_dict[year][prov][Question_name_list[i]][
                                                                              label] + 1
                else:
                    data_dict[year][prov][Question_name_list[i]][label] = 1

        else:
            if prov not in data_dict[year]:
                data_dict[year][prov] = {"Q1": {}, "Q2": {}, "Q31": {}, "Q32": {}, "Q33": {}, "Q34": {}, "Q35": {},
                                         "Q36": {}, "Q4": {},
                                         "Q5": {}, "Q6": {}, "Q7": {}, "Q8": {}, "Q9": {}, "Q10": {}}
                for i in range(0, 15):
                    label = row[i + 5]
                    if label == "":
                        label = None
                    if label in data_dict[year][prov][Question_name_list[i]].keys():
                        data_dict[year][prov][Question_name_list[i]][label] = \
                            data_dict[year][prov][Question_name_list[i]][
                                label] + 1
                    else:
                        data_dict[year][prov][Question_name_list[i]][label] = 1
            else:
                for i in range(0, 15):
                    label = row[i + 5]
                    if label == "":
                        label = None
                    if label in data_dict[year][prov][Question_name_list[i]].keys():
                        data_dict[year][prov][Question_name_list[i]][label] = \
                            data_dict[year][prov][Question_name_list[i]][label] + 1
                    else:
                        data_dict[year][prov][Question_name_list[i]][label] = 1

# print(data_dict)

yearlist = [i for i in range(2009, 2022)]


# 总诉求变化趋势

def total_petition():
    total_num_list = []
    total_num_list_1 = []
    total_num_list_2 = []
    for year in yearlist:
        total_num_1 = 0
        total_num_2 = 0
        total_num = 0
        j = data_dict[year]
        for prov in j.values():
            if "1" in prov["Q1"].keys():
                Num_1 = prov["Q1"]["1"]
            if "2" in prov["Q1"].keys():
                Num_2 = prov["Q1"]["2"]
            else:
                Num_2 = 0
            total_num_1 = Num_1 + total_num_1
            total_num_2 = Num_2 + total_num_2
            total_num = total_num + Num_1 + Num_2
        total_num_list.append(total_num)
        total_num_list_1.append(total_num_1)
        total_num_list_2.append(total_num_2)
    plt.plot(yearlist, total_num_list_1, "s--k", label="在职职工诉求")
    plt.plot(yearlist, total_num_list_2, "o--k", label="退休职工诉求")
    plt.plot(yearlist, total_num_list, "o-k", label="合计")
    plt.xlabel("年份")
    plt.ylabel("诉求数")
    plt.legend(loc="best")
    plt.show()
    print(sum(total_num_list))


# 按年汇总不同类别诉求：
Q_dict = {"Q31": {"title": "补发工资", "line": "-ok"}, "Q32": {"title": "补缴社会保险", "line": "-.k"},
          "Q33": {"title": "补发其他非工资性福利", "line": "-vk"}, "Q34": {"title": "提升工资待遇", "line": "--ok"},
          "Q35": {"title": "提升其他非工资待遇", "line": "--.k"}, "Q36": {"title": "其他非经济性诉求", "line": "--vk"}}


def summarize_by_Q3():
    for Q in Q_dict.keys():
        total_num_list = []
        for year in yearlist:
            j = data_dict[year]
            total_num = 0
            for k in j.values():
                if "1" in k[Q].keys():
                    Num = k[Q]["1"]
                else:
                    Num = 0
                total_num = total_num + Num
            total_num_list.append(total_num)
        plt.plot(yearlist, total_num_list, Q_dict[Q]["line"], label=Q_dict[Q]["title"])
        plt.xlabel("年份")
        plt.ylabel("诉求数")

        plt.legend(loc="best")
    plt.show()


def prepare_did_data():
    reformed_2018 = ["北京市", "天津市", "上海市", "重庆市", "辽宁省", "福建省", "广东省", "四川省", "陕西省"]

    csv_writer = csv.writer(open(r"./DID_all.csv", mode="w", encoding='utf-8-sig', newline=""))
    csv_writer.writerow(["year", "prov", "Count", "Treat", "Post_a", "Post_b", "Treat_post_a", "time"])
    prov_list = ['甘肃省', '陕西省', '贵州省', '广东省', '云南省', '吉林省', '河南省', '广西壮族自治区', '天津市',
                 '辽宁省',
                 '黑龙江省', '湖北省', '新疆维吾尔自治区', '山西省', '北京市', '福建省', '江苏省', '四川省', '青海省',
                 '湖南省',
                 '山东省', '河北省', '安徽省', '内蒙古自治区', '江西省', '西藏自治区', '重庆市', '浙江省',
                 '宁夏回族自治区', '上海市', '海南省']
    for year in yearlist:
        for prov in prov_list:
            j = data_dict[year]
            if prov in j.keys():
                if "1" in j[prov]["Q1"].keys():
                    Num = j[prov]["Q1"]["1"]
                else:
                    Num = 0
            else:
                Num = 0
            if prov in reformed_2018:
                treat = 1
            else:
                treat = 0
            if year >= 2018:
                post_a = 1
            else:
                post_a = 0
            if year >= 2019:
                post_b = 1
            else:
                post_b = 0
            Treat_post_a = treat * post_a
            time = year - 2008
            row = [year, prov, Num, treat, post_a, post_b, Treat_post_a, time]
            csv_writer.writerow(row)


total_petition()
summarize_by_Q3()
# prepare_did_data()
