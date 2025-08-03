import sys
import subprocess
from dotenv import load_dotenv

def main():
    """
    加载 .env 文件并执行签到脚本
    """
    load_dotenv()
    print(".env 文件已加载，正在准备执行签到脚本...")
    subprocess.run([sys.executable, "nodeseek_sign.py"])

if __name__ == "__main__":
    main()