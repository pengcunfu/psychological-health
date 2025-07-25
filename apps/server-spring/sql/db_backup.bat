@echo off
setlocal enabledelayedexpansion

:: 加载环境变量
for /f "tokens=1,* delims==" %%a in (.env) do (
    if not "%%a"=="" (
        set "%%a=%%b"
    )
)

:: 设置日期时间格式
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

:: 设置MySQL路径
set MYSQL_PATH=%MYSQL_HOME%\bin

:: 检查MySQL路径是否存在
if not exist "%MYSQL_PATH%\mysql.exe" (
    echo MySQL path not found: %MYSQL_PATH%
    echo Please check your .env file and make sure MYSQL_HOME is correctly set.
    pause
    exit /b 1
)

:menu
cls
echo =====================================
echo   MySQL Database Backup Utility
echo =====================================
echo 1. Export Database
echo 2. Import Database
echo 3. Exit
echo.
set /p choice="Please enter your choice (1-3): "

if "%choice%"=="1" goto export
if "%choice%"=="2" goto import
if "%choice%"=="3" goto end

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:export
echo.
echo Exporting database...
"%MYSQL_PATH%\mysqldump.exe" -h%MYSQL_HOST% -P%MYSQL_PORT% -u%MYSQL_USERNAME% -p%MYSQL_PASSWORD% %MYSQL_DATABASE% > "mental_health_%TIMESTAMP%.sql"
if %errorlevel% equ 0 (
    echo Database exported successfully to mental_health_%TIMESTAMP%.sql
) else (
    echo Error exporting database
)
pause
goto menu

:import
echo.
echo Available SQL files:
set /a count=0
for %%f in (*.sql) do (
    set /a count+=1
    echo !count!. %%f
)
if %count%==0 (
    echo No SQL files found in current directory.
    pause
    goto menu
)
echo.
set /p file_num="Enter the number of the file to import: "

set /a current=0
for %%f in (*.sql) do (
    set /a current+=1
    if !current!==%file_num% (
        echo Importing %%f...
        "%MYSQL_PATH%\mysql.exe" -h%MYSQL_HOST% -P%MYSQL_PORT% -u%MYSQL_USERNAME% -p%MYSQL_PASSWORD% %MYSQL_DATABASE% < "%%f"
        if !errorlevel! equ 0 (
            echo Database imported successfully
        ) else (
            echo Error importing database
        )
        pause
        goto menu
    )
)

echo Invalid file number
pause
goto menu

:end
echo Goodbye!
timeout /t 2 >nul 