import requests
import os

random = "true"  # 随机签到1-12鸡腿为true，固定鸡腿*5为false
Cookie = os.environ.get("COOKIE")  # 从环境变量中获取 Cookie

if Cookie:
    url = f"https://www.nodeseek.com/api/attendance?random={random}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        'sec-ch-ua': "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://www.nodeseek.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.nodeseek.com/board",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Cookie': Cookie
    }

    try:
        response = requests.post(url, headers=headers, verify=True)
        response_data = response.json()
        message = response_data.get('message')
        success = response_data.get('success')
        
        if success == "true":
            print(message)
        else:
            print(message)
    except Exception as e:
        print("发生异常:", e)
else:
    print("请先设置Cookie")
