#!/bin/bash

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 复制上层目录的requirements.txt到当前目录
cp ../requirements.txt .

# 激活虚拟环境
source venv/bin/activate || source venv/Scripts/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 启动Supervisor
echo "启动Supervisor..."
if ! command -v supervisord &> /dev/null; then
    echo "安装supervisor..."
    pip install supervisor
fi

# 检查supervisord配置文件
if [ ! -f "supervisord.conf" ]; then
    echo "创建supervisord配置文件..."
    cat > supervisord.conf << EOF
[supervisord]
nodaemon=true
logfile=logs/supervisord.log
pidfile=supervisord.pid

[program:unisound-agent-web]
command=python ../service.py --env prod
directory=/app/unisound-agent-web
autostart=true
autorestart=true
stdout_logfile=/var/log/unisound-agent-web.out.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=5
stderr_logfile=/var/log/unisound-agent-web.err.log
stderr_logfile_maxbytes=50MB
stderr_logfile_backups=5
environment=PYTHONPATH="."
EOF
fi

# 创建日志目录
mkdir -p /app/logs

# 启动supervisord
echo "启动服务..."
supervisord -c supervisord.conf

# 检查服务状态
sleep 2
supervisorctl status

echo "服务启动完成！"