# -- coding: utf-8 --
import os
import sys
import time
from curl_cffi import requests

CLIENTT_KEY = os.environ.get("CLIENTT_KEY", "")
NS_RANDOM = os.environ.get("NS_RANDOM", "true")
NS_COOKIE = os.environ.get("NS_COOKIE", "")
USER = os.environ.get("USER", "")
PASS = os.environ.get("PASS", "")
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
            hadsend = True
        except:
            print("加载notify.py的通知服务失败，请检查~")
            hadsend = False
    else:
        print("加载通知服务失败,缺少notify.py文件")
        hadsend = False

load_send()

def createTask():
    url = "https://api.yescaptcha.com/createTask"
    
    data = {
        "clientKey": CLIENTT_KEY,
        "task": {
            "type": "TurnstileTaskProxyless",
            "websiteURL": "https://www.nodeseek.com/signIn.html",
            "websiteKey": "0x4AAAAAAAaNy7leGjewpVyR"
        }
    }
    
    try:
        response = requests.post(url, json=data, impersonate="chrome110")
        result = response.json()
        
        if result.get("errorId") == 0:
            return result.get("taskId")
        else:
            print(f"创建验证码任务失败: {result.get('errorDescription')}")
            return None
    except Exception as e:
        print(f"创建验证码任务异常: {e}")
        return None

def getTaskResult(task_id):
    if not task_id:
        return None
        
    url = "https://api.yescaptcha.com/getTaskResult"
    data = {
        "clientKey": CLIENTT_KEY,
        "taskId": task_id
    }
    
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.post(url, json=data, impersonate="chrome110")
            result = response.json()
            
            if result.get("errorId") > 0:
                print(f"获取验证码结果失败: {result.get('errorDescription')}")
                return None
                
            if result.get("status") == "ready":
                return result.get("solution", {}).get("token")
                
            if result.get("status") == "processing":
                print(f"验证码正在处理中，等待3秒后重试 ({attempt+1}/{max_attempts})")
                time.sleep(3)
                continue
                
        except Exception as e:
            print(f"获取验证码结果异常: {e}")
            return None
            
    print("获取验证码结果超时")
    return None

def session_login():
    # 创建验证码任务
    task_id = createTask()
    if task_id is None:
        print("创建验证码任务失败，无法登录")
        return None
    
    # 获取验证码结果
    token = getTaskResult(task_id)
    if token is None:
        print("获取验证码失败，无法登录")
        return None
    
    session = requests.Session(impersonate="chrome110")
    
    if USE_PROXY and PROXY:
        print(f"使用代理: {PROXY}")
        session.proxies = {"http": PROXY, "https": PROXY}
    
    try:
        session.get("https://www.nodeseek.com/signIn.html")
    except:
        print("访问登录页面失败")
    
    url = "https://www.nodeseek.com/api/account/signIn"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'sec-ch-ua': "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://www.nodeseek.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.nodeseek.com/signIn.html",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Content-Type': "application/json"
    }
    
    data = {
        "username": USER,
        "password": PASS,
        "token": token,
        "source": "turnstile"
    }
    
    try:
        response = session.post(url, json=data, headers=headers)
        
        response_data = response.json()
        print(response_data)
        
        if response_data.get('success') == True:
            print("登录成功")
            
            cookie_dict = session.cookies.get_dict()
            cookie_string = '; '.join([f"{name}={value}" for name, value in cookie_dict.items()])
            #print(f"获取到的Cookie: {cookie_string}")
            
            return cookie_string
        else:
            message = response_data.get('message', '登录失败')
            print(f"登录失败: {message}")
            return None
    except Exception as e:
        print("登录异常:", e)
        print("实际响应内容:", response.text if 'response' in locals() else "没有响应")
        return None


def sign():
    if not NS_COOKIE:
        print("请先设置Cookie")
        return "no_cookie", ""
        
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
        'Cookie': NS_COOKIE
    }

    try:
        if USE_PROXY and PROXY:
            print(f"使用代理: {PROXY}")
            response = requests.post(url, headers=headers, impersonate="chrome110", proxies={"http": PROXY, "https": PROXY})
        else:
            response = requests.post(url, headers=headers, impersonate="chrome110")
        response_data = response.json()
        print(response_data)
        message = response_data.get('message', '')
        success = response_data.get('success')
        
        if success == "true":
            print(f"签到成功: {message}")
            return "success", message
        elif message and "已完成签到" in message:
            print(f"已经签到过: {message}")
            return "already_signed", message
        elif message == "USER NOT FOUND" or (response_data.get('status') == 404):
            print("Cookie已失效: USER NOT FOUND")
            return "invalid_cookie", message
        else:
            print(f"签到失败: {message}")
            return "fail", message
    except Exception as e:
        print("发生异常:", e)
        print("实际响应内容:", response.text if 'response' in locals() else "没有响应")
        return "error", str(e)

if __name__ == "__main__":
    if NS_COOKIE:
        sign_result, sign_message = sign()
        
        if sign_result in ["success", "already_signed"]:
            if sign_result == "success":
                print("签到成功")
                if hadsend:
                    send("nodeseek签到", f"{sign_message}")
            else:
                print("今天已经签到过了")
                if hadsend:
                    send("nodeseek签到", f"{sign_message}")
        elif sign_result in ["invalid_cookie", "error", "fail"]:
            if USER and PASS:
                print("Cookie失效或签到异常，尝试重新登录...")
                cookie = session_login()
                if cookie:
                    print("登录成功，使用新Cookie签到")
                    NS_COOKIE = cookie
                    sign_result, sign_message = sign()
                    
                    if sign_result in ["success", "already_signed"]:
                        print("使用新Cookie签到成功")
                        if hadsend:
                            send("nodeseek签到", f"{sign_message}\nCookie: {cookie}")
                    else:
                        print("使用新Cookie签到失败")
                        if hadsend:
                            send("nodeseek签到", f"{sign_message}")
                else:
                    print("重新登录失败")
                    if hadsend:
                        send("nodeseek登录", "登录失败")
            else:
                print("Cookie失效或签到异常，但未设置用户名密码，无法重新登录")
                if hadsend:
                    send("nodeseek签到", "Cookie已失效，未设置用户名密码，无法重新登录")
    else:
        if USER and PASS:
            print("没有找到Cookie，尝试登录获取...")
            cookie = session_login()
            if cookie:
                print("登录成功，使用获取的Cookie进行签到")
                NS_COOKIE = cookie
                sign_result, sign_message = sign()
                
                if sign_result in ["success", "already_signed"]:
                    print("首次登录签到成功")
                    if hadsend:
                        send("nodeseek签到", f"{sign_message}\nCookie: {cookie}")
                else:
                    print("首次登录签到失败")
                    if hadsend:
                        send("nodeseek签到", f"{sign_message}")
            else:
                print("登录失败")
                if hadsend:
                    send("nodeseek登录", "登录失败")
        else:
            print("没有Cookie且未设置用户名密码，无法执行任何操作")
            if hadsend:
                send("nodeseek签到", "没有Cookie且未设置用户名密码，无法执行任何操作")
