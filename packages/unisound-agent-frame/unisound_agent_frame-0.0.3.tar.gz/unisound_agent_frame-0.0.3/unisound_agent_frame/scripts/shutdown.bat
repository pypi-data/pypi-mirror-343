@echo off

REM 检查supervisorctl是否存在
supervisorctl --version >nul 2>&1
if errorlevel 1 (
    echo 错误: supervisorctl 未安装
    exit /b 1
)

REM 停止所有服务
echo 停止所有服务...
supervisorctl stop all

REM 关闭supervisord
echo 关闭supervisord...
if exist "supervisord.pid" (
    for /f "tokens=*" %%a in (supervisord.pid) do (
        set pid=%%a
        taskkill /pid %%a /f
        del supervisord.pid
    )
)

echo 服务已停止！ 