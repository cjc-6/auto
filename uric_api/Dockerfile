FROM python:3.8-slim

WORKDIR /app

# 安装系统依赖和netcat工具
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

# 添加执行权限
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"] 