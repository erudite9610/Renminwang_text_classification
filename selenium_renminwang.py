# _*_ coding = utf-8 _*_
# @Time : 2022/12/7 10:45
# @Author : Yoimiya
# @File : selenium.py
# @Software : Pycharm

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import datetime
import os

filelist = os.listdir(r"./")
csv_file = open(r"./renminwang_startid=12450005.csv", encoding="utf-8-sig", newline='', mode="a")
csv_writer = csv.writer(csv_file)
if 'logfile.txt' in filelist:
    file = open(r"./logfile.txt", "r", encoding="utf-8-sig")
    text = file.read()
    try:
        startpoint = int(text[-9:])
    except Exception as e:
        startpoint = int(text[-16:-8])
    print(startpoint)
else:
    startpoint = int(input("请输入爬虫起始点(2021年12月31日tid：12450006)"))
    csv_writer.writerow(
        ["target", "title", "category", "reply_state", "username", "ID", "time", "content", "reply", "reply_time",
         "reply_content"])
# endpoint = int(input("请输入本次爬虫终止点(2022年12月9日tid：16859124)"))
endpoint = 14700000
"""
2021年12月31日 tid：12450005
"""
count = 1
# count_ip = 1
# ip_list = ["http://61.171.107.48:9002", "https://103.10.22.236:8080", "https://45.81.170.20:8080"]#测试ip
# ip_number = len(ip_list)
for tid in range(startpoint, endpoint):
    log_file = open(r"./logfile.txt", mode="a", newline="", encoding="utf-8-sig")
    print("--------------------当前id：", tid, "-------------------------")
    strnow = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    log_file.write(strnow)
    log_file.write("\n")
    log_file.write("当前id：%d\n" % tid)
    """
    每20个网页换一次ip
    """
    # count_ip_20 = int(count_ip / 20)
    # count_ip_20_mod = count_ip_20 % ip_number
    # ip = ip_list[count_ip_20_mod]

    """
    换ip
    """
    url = "https://liuyan.people.com.cn/threads/content?tid=%d&from=search" % tid
    # chrome_argument = "--proxy-server=%s " % ip
    # print("当前ip：", chrome_argument)
    chromeOptions = selenium.webdriver.ChromeOptions()
    chromeOptions.add_argument("--headless")  # 静默模式
    prefs = {'profile.managed_default_content_settings.images': 2}
    chromeOptions.add_experimental_option('prefs', prefs)  # 不加载图片
    browser = selenium.webdriver.Chrome(options=chromeOptions)
    browser.implicitly_wait(2)
    browser.get(url)
    # time.sleep(1)
    browser.current_window_handle
    def try_page_type():
        try:
            page_type = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div/div').text
            return page_type
        except Exception as networkerror:
            print("网络错误，重试中")
            log_file.write("网络错误，重试中\n")
            browser.get(url)
            return try_page_type()
    print(try_page_type())
    if try_page_type()[0:7] != "页面找不到了！":
        try:
            target = browser.find_element(by=By.XPATH,
                                          value="/ html / body / div[1] / div[2] / main / div / div / div[2] / div / div "
                                                "/ div / div[1] / div[1] / div[1]").text
            title = browser.find_element(by=By.XPATH,
                                         value="/html/body/div[1]/div[2]/main/div/div/div[2]/div/div/div/div[1]/div[2]/h1").text
            category = browser.find_element(by=By.XPATH,
                                            value="/ html / body / div[1] / div[2] / main / div / div / div[2] / div / "
                                                  "div / div / div[1] / div[2] / p[2]").text
            reply_state = browser.find_element(by=By.XPATH,
                                               value="/ html / body / div[1] / div[2] / main / div / div / div[2] / div / "
                                                     "div / div / div[1] / div[2] / p[3]").text
            username = browser.find_element(by=By.XPATH,
                                            value="/html/body/div[1]/div[2]/main/div/div/div[2]/div/div/div/div[1]/ul/li["
                                                  "1]").text
            ID = browser.find_element(by=By.XPATH,
                                      value="/html/body/div[1]/div[2]/main/div/div/div[2]/div/div/div/div[1]/ul/li["
                                            "2]/span[1]").text
            post_time = browser.find_element(by=By.XPATH,
                                             value="/html/body/div[1]/div[2]/main/div/div/div[2]/div/div/div/div["
                                                   "1]/ul/li[2]/span[2]").text
            content = browser.find_element(by=By.XPATH,
                                           value=" /html/body/div[1]/div[2]/main/div/div/div[2]/div/div/div/div[2]/p").text
            row = [target, title, category, reply_state, username, ID, post_time, content]
            if reply_state == '已办理':
                reply = browser.find_element(by=By.XPATH,
                                             value="/ html / body / div[1] / div[2] / main / div / div / div[2] / div / "
                                                   "div[2] / div / div / div / div[2] / div / h4").text
                reply_time = browser.find_element(by=By.XPATH,
                                                  value="/html/body/div[1]/div[2]/main/div/div/div[2]/div/div["
                                                        "2]/div/div/div/div[2]/div/div").text
                reply_content = browser.find_element(by=By.XPATH,
                                                     value="/ html / body / div[1] / div[2] / main / div / div / div[2] / "
                                                           "div / div[2] / div / div / div / div[2] / div / p").text
                row.append(reply)
                row.append(reply_time)
                row.append(reply_content)
            csv_writer.writerow(row)
            log_file.write("-----------------成功写入%d条------------------------\n" % count)
            print("-----------------成功写入%d条------------------------\n" % count)
            count = count + 1

        except Exception as e:
            print("写入出错")
            print("--------------------当前id：", tid, "-------------------------")
            log_file.write("写入出错\n")
            continue
    else:
        log_file.write("不存在该页面\n")
    log_file.close()

    # count_ip = count_ip + 1
    # browser.quit()
