@echo off
chcp 65001 >nul
title 心理健康平台 - 数据目录设置

echo ========================================
echo      心理健康平台 - 数据目录设置
echo ========================================
echo.

REM 获取用户主目录
set "DATA_DIR=%USERPROFILE%\data\psychological-health"

echo 数据目录: %DATA_DIR%
echo.

REM 创建目录结构
echo 创建目录结构...
mkdir "%DATA_DIR%\uploads" 2>nul
mkdir "%DATA_DIR%\static" 2>nul
mkdir "%DATA_DIR%\instance" 2>nul
mkdir "%DATA_DIR%\web-logs" 2>nul
mkdir "%DATA_DIR%\mysql" 2>nul
mkdir "%DATA_DIR%\redis" 2>nul

echo ✓ 目录创建完成
echo.

REM 显示目录结构
echo 创建的目录结构:
dir "%DATA_DIR%" /B

echo.
echo ========================================
echo 🎉 数据目录设置完成！
echo ========================================
echo.
echo 现在可以运行以下命令启动服务:
echo docker-compose up -d
echo.
echo 数据将持久化到以下位置:
echo   - 上传文件: %DATA_DIR%\uploads
echo   - 静态文件: %DATA_DIR%\static
echo   - 数据库文件: %DATA_DIR%\mysql
echo   - Redis数据: %DATA_DIR%\redis
echo   - Web日志: %DATA_DIR%\web-logs
echo   - 实例数据: %DATA_DIR%\instance
echo.
echo 按任意键退出...
pause >nul 