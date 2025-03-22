# 使用官方 Python 镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制所有文件到容器
COPY . .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行 chatbot.py
CMD ["python", "chatbot.py"]
