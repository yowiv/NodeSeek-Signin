# -- coding: utf-8 --
import os
import sys
from curl_cffi import requests

NS_RANDOM = os.environ.get("NS_RANDOM","true")
NS_COOKIE = os.environ.get("NS_COOKIE","")
COOKIE = os.environ.get("COOKIE", "")
COOKIE_ENV = NS_COOKIE or COOKIE
PROXY = os.environ.get("PROXY", "")  # 代理地址，格式如：http://username:password@127.0.0.1:7890 或 http://127.0.0.1:7890
USE_PROXY = os.environ.get("USE_PROXY", "false").lower() == "true"  # 是否使用代理，默认为false

def load_send():
    global send
    global hadsend
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            hadsend=True
        except:
            print("加载notify.py的通知服务失败，请检查~")
            hadsend=False
    else:
        print("加载通知服务失败,缺少notify.py文件")
        hadsend=False
load_send()

if COOKIE_ENV:
    url = f"https://www.nodeseek.com/api/attendance?random={NS_RANDOM}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'sec-ch-ua': "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://www.nodeseek.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.nodeseek.com/board",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Cookie': COOKIE_ENV
    }

    try:
        if USE_PROXY and PROXY:
            print(f"使用代理: {PROXY}")
            response = requests.post(url, headers=headers, impersonate="chrome110", proxies={"http": PROXY, "https": PROXY})
        else:
            response = requests.post(url, headers=headers, impersonate="chrome110")
        response_data = response.json()
        print(response_data)
        print(COOKIE_ENV)
        message = response_data.get('message')
        success = response_data.get('success')
        send("nodeseek签到", message)
        if success == "true":
            print(message)
        else:
            print(message)
    except Exception as e:
        print("发生异常:", e)
        print("实际响应内容:", response.text)
else:
    print("请先设置Cookie")
