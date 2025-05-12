# -*- coding: utf-8 -*-

import os
import time
from curl_cffi import requests
from yescaptcha import YesCaptchaSolver, YesCaptchaSolverError
from turnstile_solver import TurnstileSolver, TurnstileSolverError
# ---------------- 通知模块动态加载 ----------------
hadsend = False
send = None
try:
    from notify import send
    hadsend = True
except ImportError:
    print("未加载通知模块，跳过通知功能")

# ---------------- 环境检测函数 ----------------
def detect_environment():
    """检测当前运行环境"""
    # 检测是否在青龙环境中
    ql_path_markers = ['/ql/data/', '/ql/config/', '/ql/', '/.ql/']
    in_ql_env = False
    
    for path in ql_path_markers:
        if os.path.exists(path):
            in_ql_env = True
            break
    
    # 检测是否在GitHub Actions环境中
    in_github_env = os.environ.get("GITHUB_ACTIONS") == "true" or (os.environ.get("GH_PAT") and os.environ.get("GITHUB_REPOSITORY"))
    
    if in_ql_env:
        return "qinglong"
    elif in_github_env:
        return "github"
    else:
        return "unknown"

# ---------------- GitHub 变量写入函数 ----------------
def save_cookie_to_github_var(var_name: str, cookie: str):
    import requests as py_requests
    token = os.environ.get("GH_PAT")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print("GH_PAT 或 GITHUB_REPOSITORY 未设置，跳过GitHub变量更新")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    url_check = f"https://api.github.com/repos/{repo}/actions/variables/{var_name}"
    url_create = f"https://api.github.com/repos/{repo}/actions/variables"

    data = {"name": var_name, "value": cookie}

    response = py_requests.patch(url_check, headers=headers, json=data)
    if response.status_code == 204:
        print(f"GitHub: {var_name} 更新成功")
        return True
    elif response.status_code == 404:
        print(f"GitHub: {var_name} 不存在，尝试创建...")
        response = py_requests.post(url_create, headers=headers, json=data)
        if response.status_code == 201:
            print(f"GitHub: {var_name} 创建成功")
            return True
        else:
            print(f"GitHub创建失败: {response.status_code}, {response.text}")
            return False
    else:
        print(f"GitHub设置失败: {response.status_code}, {response.text}")
        return False

# ---------------- 青龙面板变量删除函数 ----------------
def delete_ql_env(var_name: str):
    """删除青龙面板中的指定环境变量"""
    try:
        print(f"查询要删除的环境变量: {var_name}")
        env_result = QLAPI.getEnvs({"searchValue": var_name})
        
        env_ids = []
        if env_result.get("code") == 200 and env_result.get("data"):
            for env in env_result.get("data"):
                if env.get("name") == var_name:
                    env_ids.append(env.get("id"))
        
        if env_ids:
            print(f"找到 {len(env_ids)} 个环境变量需要删除: {env_ids}")
            delete_result = QLAPI.deleteEnvs({"ids": env_ids})
            if delete_result.get("code") == 200:
                print(f"成功删除环境变量: {var_name}")
                return True
            else:
                print(f"删除环境变量失败: {delete_result}")
                return False
        else:
            print(f"未找到环境变量: {var_name}")
            return True
    except (TurnstileSolverError, YesCaptchaSolverError) as e:
        print(f"验证码解析错误: {e}")
        return None
    except Exception as e:
        print(f"删除环境变量异常: {str(e)}")
        return False

# ---------------- 青龙面板变量更新函数 ----------------
def save_cookie_to_ql(var_name: str, cookie: str):
    """保存Cookie到青龙面板环境变量"""
    
    try:
        delete_result = delete_ql_env(var_name)
        if not delete_result:
            print("删除已有变量失败，但仍将尝试创建新变量")
        
        create_data = {
            "envs": [
                {
                    "name": var_name,
                    "value": cookie,
                    "remarks": "NodeSeek签到自动创建",
                    "status": 2  # 启用状态
                }
            ]
        }
        
        create_result = QLAPI.createEnv(create_data)
        if create_result.get("code") == 200:
            print(f"青龙面板环境变量 {var_name} 创建成功")
            return True
        else:
            print(f"青龙面板环境变量创建失败: {create_result}")
            return False
    except Exception as e:
        print(f"青龙面板环境变量操作异常: {str(e)}")
        return False

# ---------------- 统一变量保存函数 ----------------
def save_cookie(var_name: str, cookie: str):
    """根据当前环境保存Cookie到相应位置"""
    env_type = detect_environment()
    
    if env_type == "qinglong":
        print("检测到青龙环境，保存变量到青龙面板...")
        return save_cookie_to_ql(var_name, cookie)
    elif env_type == "github":
        print("检测到GitHub环境，保存变量到GitHub Actions...")
        return save_cookie_to_github_var(var_name, cookie)
    else:
        print("未检测到支持的环境，跳过变量保存")
        return False

# ---------------- 登录逻辑 ----------------
def session_login(user, password, solver_type, api_base_url, client_key):
    try:
        if solver_type.lower() == "yescaptcha":
            print("正在使用 YesCaptcha 解决验证码...")
            solver = YesCaptchaSolver(
                api_base_url=api_base_url or "https://api.yescaptcha.com",
                client_key=client_key
            )
        else:  # 默认使用 turnstile_solver
            print("正在使用 TurnstileSolver 解决验证码...")
            solver = TurnstileSolver(
                api_base_url=api_base_url,
                client_key=client_key
            )

        token = solver.solve(
            url="https://www.nodeseek.com/signIn.html",
            sitekey="0x4AAAAAAAaNy7leGjewpVyR",
            verbose=True
        )
        if not token:
            print("验证码解析失败")
            return None
    except Exception as e:
        print(f"验证码错误: {e}")
        return None

    session = requests.Session(impersonate="chrome110")
    session.get("https://www.nodeseek.com/signIn.html")

    data = {
        "username": user,
        "password": password,
        "token": token,
        "source": "turnstile"
    }
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
    try:
        response = session.post("https://www.nodeseek.com/api/account/signIn", json=data, headers=headers)
        resp_json = response.json()
        if resp_json.get("success"):
            cookies = session.cookies.get_dict()
            cookie_string = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            return cookie_string
        else:
            print("登录失败:", resp_json.get("message"))
            return None
    except Exception as e:
        print("登录异常:", e)
        return None

# ---------------- 签到逻辑 ----------------
def sign(ns_cookie, ns_random):
    if not ns_cookie:
        return "invalid", "无有效Cookie"
        
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'origin': "https://www.nodeseek.com",
        'referer': "https://www.nodeseek.com/board",
        'Cookie': ns_cookie
    }
    try:
        url = f"https://www.nodeseek.com/api/attendance?random={ns_random}"
        response = requests.post(url, headers=headers, impersonate="chrome110")
        data = response.json()
        msg = data.get("message", "")
        if "鸡腿" in msg or data.get("success"):
            return "success", msg
        elif "已完成签到" in msg:
            return "already", msg
        elif data.get("status") == 404:
            return "invalid", msg
        return "fail", msg
    except Exception as e:
        return "error", str(e)

# ---------------- 主流程 ----------------
if __name__ == "__main__":
    solver_type = os.getenv("SOLVER_TYPE", "turnstile")
    api_base_url = os.getenv("API_BASE_URL", "")
    client_key = os.getenv("CLIENTT_KEY", "") 
    ns_random = os.getenv("NS_RANDOM", "true")

    env_type = detect_environment()
    print(f"当前运行环境: {env_type}")
    
    accounts = []

    user = os.getenv("USER")
    password = os.getenv("PASS")
    if user and password:
        accounts.append({"user": user, "password": password})

    index = 1
    while True:
        user = os.getenv(f"USER{index}")
        password = os.getenv(f"PASS{index}")
        if user and password:
            accounts.append({"user": user, "password": password})
            index += 1
        else:
            break
    
    # 读取现有Cookie
    all_cookies = os.getenv("NS_COOKIE", "")
    cookie_list = all_cookies.split("&")
    cookie_list = [c.strip() for c in cookie_list if c.strip()]
    
    print(f"共发现 {len(accounts)} 个账户配置，{len(cookie_list)} 个现有Cookie")
    
    if len(cookie_list) > len(accounts):
        cookie_list = cookie_list[:len(accounts)]
    while len(cookie_list) < len(accounts):
        cookie_list.append("")
    
    cookies_updated = False
    
    for i, account in enumerate(accounts):
        account_index = i + 1
        user = account["user"]
        password = account["password"]
        cookie = cookie_list[i] if i < len(cookie_list) else ""
        
        display_user = user if user else f"账号{account_index}"
        
        print(f"\n==== 账号 {display_user} 开始签到 ====")
        
        if cookie:
            result, msg = sign(cookie, ns_random)
        else:
            result, msg = "invalid", "无Cookie"

        if result in ["success", "already"]:
            print(f"账号 {display_user} 签到成功: {msg}")
            
            if hadsend:
                try:
                    send("NodeSeek 签到", f"账号 {display_user} 签到成功：{msg}")
                except Exception as e:
                    print(f"发送通知失败: {e}")
        else:
            print(f"签到失败或无效: {msg}")
            print("尝试重新登录...")
            if not user or not password:
                print(f"账号 {display_user} 无法登录: 缺少用户名或密码")
                continue
                
            new_cookie = session_login(user, password, solver_type, api_base_url, client_key)
            if new_cookie:
                print("登录成功，重新签到...")
                result, msg = sign(new_cookie, ns_random)
                if result in ["success", "already"]:
                    print(f"账号 {display_user} 签到成功: {msg}")
                    cookies_updated = True
                    
                    if i < len(cookie_list):
                        cookie_list[i] = new_cookie
                    else:
                        cookie_list.append(new_cookie)
                    
                    if hadsend:
                        try:
                            send("NodeSeek 签到", f"账号 {display_user} 签到成功：{msg}")
                        except Exception as e:
                            print(f"发送通知失败: {e}")
                else:
                    print(f"账号 {display_user} 签到失败: {msg}")
            else:
                print(f"账号 {display_user} 登录失败")
                if hadsend:
                    try:
                        send("NodeSeek 登录失败", f"账号 {display_user} 登录失败")
                    except Exception as e:
                        print(f"发送通知失败: {e}")
    
    if cookies_updated and cookie_list:
        print("\n==== 处理完毕，保存更新后的Cookie ====")
        all_cookies_new = "&".join(cookie_list)
        try:
            save_cookie("NS_COOKIE", all_cookies_new)
            print("所有Cookie已成功保存")
        except Exception as e:
            print(f"保存Cookie变量异常: {e}")
