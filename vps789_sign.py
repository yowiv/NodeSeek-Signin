import requests
import os

TOKEN = os.environ.get("TOKEN","")
pushplus_token = os.environ.get("PUSHPLUS_TOKEN")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","")
chat_id = os.environ.get("CHAT_ID","")
telegram_api_url = os.environ.get("TELEGRAM_API_URL","https://api.telegram.org") # 代理api,可以使用自己的反代
def telegram_Bot(token,chat_id,message):
    url = f'{telegram_api_url}/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    r = requests.post(url, json=data,verify=False)
    response_data = r.json()
    msg = response_data['ok']
    print(f"telegram推送结果：{msg}\n")
def pushplus_ts(token, rw, msg):
    url = 'https://www.pushplus.plus/send/'
    data = {
        "token": token,
        "title": rw,
        "content": msg
    }
    r = requests.post(url, json=data,verify=False)
    msg = r.json().get('msg', None)
    print(f'pushplus推送结果：{msg}\n')

if TOKEN:
    url = "https://vps789.com/user/signin"
    headers = {
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
      'Accept': "application/json, text/plain, */*",
      'Accept-Encoding': "gzip, deflate, br, zstd",
      'sec-ch-ua': "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
      'yf-token': TOKEN,
      'sec-ch-ua-mobile': "?0",
      'sec-ch-ua-platform': "\"Windows\"",
      'sec-fetch-site': "same-origin",
      'sec-fetch-mode': "cors",
      'sec-fetch-dest': "empty",
      'referer': "https://vps789.com/",
      'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
      'priority': "u=1, i",
    }

    try:
        response = requests.post(url, headers=headers,verify=False)
        response_data = response.json()
        message = response_data.get('message')
        code = response_data.get('code')
        
        if code == "0":
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
        else:
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
            if pushplus_token:
                pushplus_ts(pushplus_token, "vps789签到", message)
    except Exception as e:
        print("发生异常:", e)
else:
    print("请先设置TOKEN")
