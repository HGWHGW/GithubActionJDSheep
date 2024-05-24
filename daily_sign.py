import os
import requests
import re
import json
import time

#  配置你的SendKey
send_key = os.environ.get("PUSH_KEY")


# Python3通过 Server酱 的API接口让你的消息推送到你的微信。
# encoding:utf-8
def wechat_send(ftqq_title, ftqq_text):  # 发微信消息
    api = 'https://sctapi.ftqq.com/' + send_key + '.send'
    if ftqq_title != '':
        title = ftqq_title
    else:
        title = '默认通知标题'
    if ftqq_text != '':
        text = ftqq_text
    else:
        text = '默认文本内容'
    # 发送数据内容
    data = {'text': title.encode('utf-8'), 'desp': text.encode('utf-8')}
    req = requests.post(api, data=data)  # req 为200表示发送成功
    return req


def get_json_message(url, headers):
    response1 = requests.post(url=url, headers=headers)
    print(response1.text)
    print("------------------------------")
    json_data_match = re.search(r'\((.*?)\)', response1.text)
    if json_data_match:
        json_data = json_data_match.group(1)
        print(json_data)
        # 解析提取出的 JSON 数据
        json_data = json.loads(json_data)

        # 打印解析后的 JSON 数据
        print(json_data)
    else:
        json_data = None
        print("未找到有效的 JSON 数据部分")
    return response1, json_data


cookie = os.environ.get("JD_COOKIE")

url = ("https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1"
       "%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1"
       "%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld&client=apple&clientVersion=10.0.4&networkType=wifi&osVersion=14"
       ".8.1&uuid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&openudid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&jsonp"
       "=jsonp_1645885800574_58482")

headers = {"Connection": 'keep-alive',
           "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "Cache-Control": 'no-cache',
           "User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;",
           "accept": "*/*",
           "connection": "Keep-Alive",
           "Accept-Encoding": "gzip,deflate",
           "Cookie": cookie
           }

response, data = get_json_message(url, headers)
try:
    if response.status_code == 200:
        if data["code"] == '402':  # 活动繁忙
            for i in range(3):
                print(r"第{i+1}次重连...")
                response, data = get_json_message(url, headers)
                if data["code"] == '402':
                    title = data["data"]["dailyAward"]["title"]
                    text = data["data"]["dailyAward"]["subTitle"] + " " + data["data"]["dailyAward"]["beanAward"][
                        "beanCount"]
                    break
                time.sleep(600)
        else:
            title = data["data"]["dailyAward"]["title"]
            text = data["data"]["dailyAward"]["subTitle"] + " " + data["data"]["dailyAward"]["beanAward"]["beanCount"]
    else:
        title = str(response.status_code)
        text = "error\n" + response.text
except Exception as error_name:
    title = "program error!"
    text = str(error_name)+"\n"+response.text
    print(text)

req = wechat_send(title, text)
