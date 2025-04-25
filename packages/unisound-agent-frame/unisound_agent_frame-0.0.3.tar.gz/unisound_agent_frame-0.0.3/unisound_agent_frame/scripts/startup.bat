@echo off



REM 检查Python环境
python --version 2>NUL
if errorlevel 1 (
    echo 错误: 未找到 Python
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat


REM 复制上层目录的requirements.txt到当前目录
copy ..\requirements.txt .

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 安装supervisor
echo 安装supervisor...
pip install supervisor

REM 检查supervisord配置文件
if not exist "supervisord.conf" (
    echo 创建supervisord配置文件...
    (
        echo [supervisord]
        echo nodaemon=true
        echo logfile=logs/supervisord.log
        echo pidfile=supervisord.pid
        echo.
        echo [program:unisound-agent-web]
        echo command=python ../service.py --env prod
        echo directory=%CD%
        echo autostart=true
        echo autorestart=true
        echo stdout_logfile=logs/unisound-agent-web.out.log
        echo stdout_logfile_maxbytes=50MB
        echo stdout_logfile_backups=5
        echo stderr_logfile=logs/unisound-agent-web.err.log
        echo stderr_logfile_maxbytes=50MB
        echo stderr_logfile_backups=5
        echo environment=PYTHONPATH="."
    ) > supervisord.conf
)

REM 创建日志目录
if not exist "logs" mkdir logs

REM 启动supervisord
echo 启动服务...
supervisord -c supervisord.conf

REM 检查服务状态
timeout /t 2 /nobreak
supervisorctl status

echo 服务启动完成！