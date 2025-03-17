# -- coding: utf-8 --
import os
import sys
import time
from curl_cffi import requests
from turnstile_solver import TurnstileSolver, TurnstileSolverError
from yescaptcha import YesCaptchaSolver, YesCaptchaSolverError

# 配置参数
API_BASE_URL = os.environ.get("API_BASE_URL", "")
CLIENTT_KEY = os.environ.get("CLIENTT_KEY", "")
NS_RANDOM = os.environ.get("NS_RANDOM", "true")
NS_COOKIE = os.environ.get("NS_COOKIE", "")
USER = os.environ.get("USER", "")
PASS = os.environ.get("PASS", "")
SOLVER_TYPE = os.environ.get("SOLVER_TYPE", "turnstile")

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


def session_login():
    # 根据环境变量选择使用哪个验证码解决器
    try:
        if SOLVER_TYPE.lower() == "yescaptcha":
            print("正在使用 YesCaptcha 解决验证码...")
            solver = YesCaptchaSolver(
                api_base_url="https://api.yescaptcha.com",
                client_key=CLIENTT_KEY
            )
        else:  # 默认使用 turnstile_solver
            print("正在使用 TurnstileSolver 解决验证码...")
            solver = TurnstileSolver(
                api_base_url=API_BASE_URL,
                client_key=CLIENTT_KEY
            )
        
        token = solver.solve(
            url="https://www.nodeseek.com/signIn.html",
            sitekey="0x4AAAAAAAaNy7leGjewpVyR",
            verbose=True
        )
        
        if not token:
            print("获取验证码令牌失败，无法登录")
            return None
            
    except (TurnstileSolverError, YesCaptchaSolverError) as e:
        print(f"验证码解析错误: {e}")
        return None
    except Exception as e:
        print(f"获取验证码过程中发生异常: {e}")
        return None
    
    # 创建会话并登录
    session = requests.Session(impersonate="chrome110")
    
    try:
        session.get("https://www.nodeseek.com/signIn.html")
    except Exception as e:
        print(f"访问登录页面失败: {e}")
    
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
        'origin': "https://www.nodeseek.com",
        'referer': "https://www.nodeseek.com/board",
        'Cookie': NS_COOKIE
    }

    try:
        response = requests.post(url, headers=headers, impersonate="chrome110")
        response_data = response.json()
        print(f"签到返回: {response_data}")
        message = response_data.get('message', '')
        
        # 简化判断逻辑
        if "鸡腿" in message or response_data.get('success') == True:
            # 如果消息中包含"鸡腿"或success为True，都视为签到成功
            print(f"签到成功: {message}")
            return "success", message
        elif "已完成签到" in message:
            print(f"已经签到过: {message}")
            return "already_signed", message
        elif message == "USER NOT FOUND" or response_data.get('status') == 404:
            print("Cookie已失效")
            return "invalid_cookie", message
        else:
            print(f"签到失败: {message}")
            return "fail", message
            
    except Exception as e:
        print("发生异常:", e)
        return "error", str(e)

if __name__ == "__main__":
    # 尝试使用现有Cookie签到
    sign_result, sign_message = "no_cookie", ""
    
    if NS_COOKIE:
        sign_result, sign_message = sign()
    
    # 处理签到结果
    if sign_result in ["success", "already_signed"]:
        status = "签到成功" if sign_result == "success" else "今天已经签到过了"
        print(status)
        if hadsend:
            send("nodeseek签到", f"{sign_message}")
    else:
        # 签到失败或没有Cookie，尝试登录
        if USER and PASS:
            print("尝试登录获取新Cookie...")
            cookie = session_login()
            if cookie:
                print("登录成功，使用新Cookie签到")
                NS_COOKIE = cookie
                sign_result, sign_message = sign()
                
                status = "签到成功" if sign_result in ["success", "already_signed"] else "签到失败"
                print(status)
                if hadsend:
                    message = f"{sign_message}"
                    if sign_result in ["success", "already_signed"]:
                        message += f"\nCookie: {cookie}"
                    send("nodeseek签到", message)
            else:
                print("登录失败")
                if hadsend:
                    send("nodeseek登录", "登录失败")
        else:
            print("无法执行操作：没有有效Cookie且未设置用户名密码")
            if hadsend:
                send("nodeseek签到", "无法执行操作：没有有效Cookie且未设置用户名密码")
