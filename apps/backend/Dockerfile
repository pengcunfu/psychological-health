# 使用官方 Python 3.11 slim 镜像作为基础镜像
FROM python:3.11-slim as base

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    CONFIG_PATH=config-prod.yaml

# 配置中科大镜像源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# 配置 pip 使用中科大镜像
RUN pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple && \
    pip config set global.trusted-host mirrors.ustc.edu.cn

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非特权用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# ================================
# 构建阶段
# ================================
FROM base as builder

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --user --no-warn-script-location -r requirements.txt

# ================================
# 生产阶段
# ================================
FROM base as production

# 从构建阶段复制已安装的依赖
COPY --from=builder /root/.local /home/appuser/.local

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p static uploads instance && \
    chown -R appuser:appuser /app

# 切换到非特权用户
USER appuser

# 设置 PATH 环境变量
ENV PATH=/home/appuser/.local/bin:$PATH

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# 暴露端口
EXPOSE 5000

# 启动命令 (使用环境变量配置)
CMD ["sh", "-c", "python -m gunicorn --bind 0.0.0.0:${PORT:-5000} --workers ${WORKERS:-4} --timeout ${TIMEOUT:-60} --keep-alive ${KEEP_ALIVE:-5} --max-requests ${MAX_REQUESTS:-1000} --max-requests-jitter ${MAX_REQUESTS_JITTER:-100} --access-logfile - --error-logfile - app:app"]
