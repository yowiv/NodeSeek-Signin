# -- coding: utf-8 --
import os
import sys
import time
import re
from curl_cffi import requests
from turnstile_solver import TurnstileSolver, TurnstileSolverError
from yescaptcha import YesCaptchaSolver, YesCaptchaSolverError

# 配置参数
API_BASE_URL = os.environ.get("API_BASE_URL", "")
CLIENTT_KEY = os.environ.get("CLIENTT_KEY", "")
NS_RANDOM = os.environ.get("NS_RANDOM", "true")
NS_COOKIE = os.environ.get("NS_COOKIE", "")
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

def get_env_account_pairs():
    """获取所有账号密码对"""
    accounts = []
    
    # 获取基本账号（无编号）
    base_user = os.environ.get("USER", "")
    base_pass = os.environ.get("PASS", "")
    if base_user and base_pass:
        accounts.append((base_user, base_pass))
    
    # 获取编号账号 (USER1/PASS1, USER2/PASS2...)
    i = 1
    while True:
        user_key = f"USER{i}"
        pass_key = f"PASS{i}"
        username = os.environ.get(user_key, "")
        password = os.environ.get(pass_key, "")
        
        if not username or not password:
            break
            
        accounts.append((username, password))
        i += 1
    
    return accounts

def parse_accounts(user_str, pass_str):
    """解析多账号配置，返回账号密码对列表"""
    if not user_str or not pass_str:
        return []
    
    # 使用正则表达式分割字符串（换行或&符号）
    users = re.split(r'[\n&]', user_str)
    passwords = re.split(r'[\n&]', pass_str)
    
    # 清理空白内容
    users = [u.strip() for u in users if u.strip()]
    passwords = [p.strip() for p in passwords if p.strip()]
    
    # 确保账号和密码数量一致
    accounts = []
    for i in range(min(len(users), len(passwords))):
        accounts.append((users[i], passwords[i]))
    
    return accounts

def session_login(username, password):
    # 根据环境变量选择使用哪个验证码解决器
    try:
        if SOLVER_TYPE.lower() == "yescaptcha":
            print(f"正在使用 YesCaptcha 解决验证码...")
            solver = YesCaptchaSolver(
                api_base_url="https://api.yescaptcha.com",
                client_key=CLIENTT_KEY
            )
        else:  # 默认使用 turnstile_solver
            print(f"正在使用 TurnstileSolver 解决验证码...")
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
            print(f"获取验证码令牌失败，无法登录")
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
        "username": username,
        "password": password,
        "token": token,
        "source": "turnstile"
    }
    
    try:
        response = session.post(url, json=data, headers=headers)
        response_data = response.json()
        print(f"账号 {username} 登录结果:", response_data)
        
        if response_data.get('success') == True:
            cookie_dict = session.cookies.get_dict()
            cookie_string = '; '.join([f"{name}={value}" for name, value in cookie_dict.items()])
            return cookie_string
        else:
            message = response_data.get('message', '登录失败')
            print(f"账号 {username} 登录失败: {message}")
            return None
    except Exception as e:
        print(f"账号 {username} 登录异常:", e)
        print("实际响应内容:", response.text if 'response' in locals() else "没有响应")
        return None

def sign(cookie, account_name=""):
    if not cookie:
        print(f"账号 {account_name} 请先设置Cookie")
        return "no_cookie", ""
        
    url = f"https://www.nodeseek.com/api/attendance?random={NS_RANDOM}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'origin': "https://www.nodeseek.com",
        'referer': "https://www.nodeseek.com/board",
        'Cookie': cookie
    }

    try:
        response = requests.post(url, headers=headers, impersonate="chrome110")
        response_data = response.json()
        print(f"账号 {account_name} 签到返回: {response_data}")
        message = response_data.get('message', '')
        
        # 简化判断逻辑
        if "鸡腿" in message or response_data.get('success') == True:
            # 如果消息中包含"鸡腿"或success为True，都视为签到成功
            print(f"账号 {account_name} 签到成功: {message}")
            return "success", message
        elif "已完成签到" in message:
            print(f"账号 {account_name} 已经签到过: {message}")
            return "already_signed", message
        elif message == "USER NOT FOUND" or response_data.get('status') == 404:
            print(f"账号 {account_name} Cookie已失效")
            return "invalid_cookie", message
        else:
            print(f"账号 {account_name} 签到失败: {message}")
            return "fail", message
            
    except Exception as e:
        print(f"账号 {account_name} 发生异常:", e)
        return "error", str(e)

def parse_cookies(cookie_str):
    """解析多个Cookie，返回Cookie列表"""
    if not cookie_str:
        return []
    
    # 使用正则表达式分割字符串（换行或&符号）
    cookies = re.split(r'[\n&]', cookie_str)
    
    # 清理空白内容
    return [c.strip() for c in cookies if c.strip()]

if __name__ == "__main__":
    # 结果统计
    success_count = 0
    already_signed_count = 0
    fail_count = 0
    total_results = []
    
    # 获取所有账号 - 包括编号账号
    accounts = get_env_account_pairs()
    cookies = parse_cookies(NS_COOKIE)
    
    print(f"检测到 {len(accounts)} 个账号配置")
    print(f"检测到 {len(cookies)} 个Cookie配置")
    
    # 先处理已有Cookie的情况
    for i, cookie in enumerate(cookies):
        account_name = f"Cookie账号{i+1}"
        print(f"开始处理 {account_name}")
        
        sign_result, sign_message = sign(cookie, account_name)
        
        if sign_result == "success":
            success_count += 1
            total_results.append(f"{account_name}: 签到成功 - {sign_message}")
        elif sign_result == "already_signed":
            already_signed_count += 1
            total_results.append(f"{account_name}: 已签到 - {sign_message}")
        else:
            fail_count += 1
            total_results.append(f"{account_name}: 签到失败 - {sign_message}")
    
    # 再处理需要登录的账号
    for i, (username, password) in enumerate(accounts):
        account_name = f"{username}"
        print(f"开始处理账号 {account_name}")
        
        # 尝试登录获取Cookie
        print(f"账号 {account_name} 尝试登录获取新Cookie...")
        cookie = session_login(username, password)
        
        if cookie:
            print(f"账号 {account_name} 登录成功，使用新Cookie签到")
            
            # 将新的Cookie保存到环境变量
            gh_env = os.environ.get("GITHUB_ENV")
            if gh_env:
                try:
                    with open(gh_env, "a", encoding="utf-8") as f:
                        # 使用追加模式添加或更新Cookie
                        if i == 0 and not cookies:  # 如果是第一个账号且没有已有的Cookie
                            f.write(f"NS_COOKIE={cookie}\n")
                        else:  # 否则追加到已有Cookie
                            existing_cookie = NS_COOKIE + "&" if NS_COOKIE else ""
                            f.write(f"NS_COOKIE={existing_cookie}{cookie}\n")
                    print(f"账号 {account_name} 的新Cookie已写入GITHUB_ENV环境变量文件")
                except Exception as e:
                    print(f"写入GITHUB_ENV环境变量文件失败: {e}")
            else:
                print("未检测到GITHUB_ENV环境变量，跳过写入")
                
            # 使用新Cookie签到
            sign_result, sign_message = sign(cookie, account_name)
            
            if sign_result == "success":
                success_count += 1
                total_results.append(f"{account_name}: 签到成功 - {sign_message}")
            elif sign_result == "already_signed":
                already_signed_count += 1
                total_results.append(f"{account_name}: 已签到 - {sign_message}")
            else:
                fail_count += 1
                total_results.append(f"{account_name}: 签到失败 - {sign_message}")
                
        else:
            print(f"账号 {account_name} 登录失败")
            fail_count += 1
            total_results.append(f"{account_name}: 登录失败")
    
    # 汇总结果
    total_accounts = len(cookies) + len(accounts)
    summary = f"NodeSeek签到结果统计\n" \
              f"总计: {total_accounts} 个账号\n" \
              f"成功: {success_count} 个\n" \
              f"已签: {already_signed_count} 个\n" \
              f"失败: {fail_count} 个\n\n" \
              f"详细结果:\n" + "\n".join(total_results)
    
    print("\n" + summary)
    
    # 发送通知
    if hadsend and total_accounts > 0:
        send("NodeSeek多账号签到", summary)
    elif total_accounts == 0:
        print("无法执行操作：没有有效Cookie且未设置用户名密码")
        if hadsend:
            send("NodeSeek签到", "无法执行操作：没有有效Cookie且未设置用户名密码")
