# 使用Python 3.11.9作为基础镜像
FROM python:3.11.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（包括Manim所需的图形库和字体）
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    libgirepository1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libatlas-base-dev \
    gfortran \
    wget \
    curl \
    fonts-dejavu \
    fonts-liberation \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-roboto \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p data/videos data/srt media/videos/result/480p15

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 暴露端口（根据main.py默认端口8080）
EXPOSE 8080

# 设置数据卷挂载点
VOLUME ["/app/data"]

# 启动命令
CMD ["python", "main.py", "--host=0.0.0.0", "--port=8080"]