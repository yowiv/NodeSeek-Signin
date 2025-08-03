import os
import time
import datetime
import random
import subprocess
import re
from datetime import timezone, timedelta

GMT8 = timezone(timedelta(hours=8))

def get_run_config():
    """
    从环境变量 RUN_AT 读取并解析运行时间配置。
    - 'HH:MM': 固定时间
    - 'HH:MM-HH:MM': 随机时间范围
    - 未设置或格式错误: 默认为 '08:00-10:59'
    返回一个元组 (mode, value)
    """
    run_at_env = os.environ.get('RUN_AT', '08:00-10:59')

    if re.fullmatch(r'\d{2}:\d{2}', run_at_env):
        print(f"检测到固定时间模式: {run_at_env}")
        return 'fixed', run_at_env
    
    if re.fullmatch(r'\d{2}:\d{2}-\d{2}:\d{2}', run_at_env):
        print(f"检测到随机时间范围模式: {run_at_env}")
        return 'range', run_at_env

    if os.environ.get('RUN_AT'):
        print(f"警告: 环境变量 RUN_AT 的格式 '{run_at_env}' 无效。")
    
    print("将使用默认随机时间范围 '08:00-10:59'。")
    return 'range', '08:00-10:59'

def calculate_next_run_time(mode, value):
    """
    根据当前时间和配置计算下一次运行的 datetime 对象。
    智能寻找下一个可用的运行时间点（今天或明天），并使用 GMT+8 时区。
    """
    now = datetime.datetime.now(GMT8)

    if mode == 'fixed':
        h, m = map(int, value.split(':'))
        next_run_attempt = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if next_run_attempt > now:
            return next_run_attempt
        else:
            return next_run_attempt + datetime.timedelta(days=1)

    elif mode == 'range':
        start_str, end_str = value.split('-')
        start_h, start_m = map(int, start_str.split(':'))
        end_h, end_m = map(int, end_str.split(':'))
        
        start_time = datetime.time(start_h, start_m)
        end_time = datetime.time(end_h, end_m)

        start_today = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)

        if now < start_today:
            target_date = now.date()
        else:
            target_date = now.date() + datetime.timedelta(days=1)

        start_target = datetime.datetime.combine(target_date, start_time, tzinfo=GMT8)
        end_target = datetime.datetime.combine(target_date, end_time, tzinfo=GMT8)

        if start_target > end_target:
            end_target += datetime.timedelta(days=1)

        start_timestamp = int(start_target.timestamp())
        end_timestamp = int(end_target.timestamp())
        
        random_timestamp = random.randint(start_timestamp, end_timestamp)
        return datetime.datetime.fromtimestamp(random_timestamp, tz=GMT8)

def run_checkin_task():
    """
    执行 nodeseek_sign.py 脚本。
    """
    print(f"[{datetime.datetime.now(GMT8).strftime('%Y-%m-%d %H:%M:%S')}] 开始执行签到任务...")
    try:
        subprocess.run(["python", "nodeseek_sign.py"], check=True)
        print(f"[{datetime.datetime.now(GMT8).strftime('%Y-%m-%d %H:%M:%S')}] 签到任务执行完毕。")
    except FileNotFoundError:
        print("错误: 'nodeseek_sign.py' 未找到。请确保它与 scheduler.py 位于同一目录。")
    except subprocess.CalledProcessError as e:
        print(f"签到任务执行失败，返回码: {e.returncode}")
    except Exception as e:
        print(f"执行签到任务时发生未知错误: {e}")

def main():
    """
    主调度循环。
    """
    print("调度器启动...")
    mode, value = get_run_config()
    print(f"调度模式: '{mode}', 配置值: '{value}'")
    
    run_checkin_task()

    while True:
        next_run_time = calculate_next_run_time(mode, value)
        now = datetime.datetime.now(GMT8)
        sleep_duration = (next_run_time - now).total_seconds()

        if sleep_duration > 0:
            print(f"下一次签到任务计划在: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
            hours, remainder = divmod(sleep_duration, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"程序将休眠 {int(hours)} 小时 {int(minutes)} 分钟。")
            time.sleep(sleep_duration)
        else:
            print("计算出的下一个运行时间已过，等待 60 秒后重试...")
            time.sleep(60)

        run_checkin_task()

if __name__ == "__main__":
    main()