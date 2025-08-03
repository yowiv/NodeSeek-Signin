# 使用轻量级的 Python 基础镜像
FROM python:3.9-alpine

# 设置时区为 GMT+8
RUN apk add --no-cache tzdata ca-certificates
ENV TZ=Asia/Shanghai

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有 .py 文件到工作目录
COPY *.py ./

# 设置默认启动命令
CMD ["python", "scheduler.py"]