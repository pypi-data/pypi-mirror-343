FROM registry.cn-hangzhou.aliyuncs.com/otterhub/python:3.10-slim

# 安装软件包
RUN sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update && apt-get install -y nginx supervisor procps vim curl net-tools iputils-ping iproute2


COPY . /app/unisound-agent-web

# 项目依赖
RUN python -m venv /app/unisound-agent-web/venv && \
    /app/unisound-agent-web/venv/bin/pip install -r /app/unisound-agent-web/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# supervisord配置
#COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY /app/unisound-agent-web/scripts/supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# 启动命令
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]