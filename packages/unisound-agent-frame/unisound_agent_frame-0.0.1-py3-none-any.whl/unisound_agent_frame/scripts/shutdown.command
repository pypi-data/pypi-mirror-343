#!/bin/bash

# 获取脚本所在目录
cd "$(dirname "$0")"

# 检查supervisorctl是否存在
if ! command -v supervisorctl &> /dev/null; then
    echo "错误: supervisorctl 未安装"
    exit 1
fi

# 停止所有服务
echo "停止所有服务..."
supervisorctl stop all

# 关闭supervisord
echo "关闭supervisord..."
if [ -f "supervisord.pid" ]; then
    pid=$(cat supervisord.pid)
    kill $pid
    rm -f supervisord.pid
fi

# 检查进程是否完全停止
sleep 2
if ps -p $pid > /dev/null 2>&1; then
    echo "强制终止进程..."
    kill -9 $pid
fi

echo "服务已停止！" 