@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================
echo   Joplin → 博客 一键同步发布
echo ============================================
echo.

REM ============================================================
REM 查找可用的 Python
REM ============================================================
set PYTHON=
for %%p in (
    "python3"
    "python"
    "C:\Users\cnfea\.workbuddy\binaries\python\versions\3.14.3\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
) do (
    if not defined PYTHON (
        where /q %%~p 2>nul
        if !errorlevel! equ 0 set PYTHON=%%~p
    )
)

if not defined PYTHON (
    echo [错误] 未找到 Python，请先安装 Python
    echo       下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [Python] !PYTHON!

REM ============================================================
REM 查找可用的 Git
REM ============================================================
set GIT=git
where /q git 2>nul
if !errorlevel! neq 0 (
    set GIT=C:\Program Files\Git\cmd\git.exe
    if not exist "!GIT!" (
        echo [错误] 未找到 Git，请先安装 Git
        echo       下载地址: https://git-scm.com/download/win
        pause
        exit /b 1
    )
)
echo [Git] !GIT!
echo.

REM ============================================================
REM [1/3] 同步 Joplin 笔记
REM ============================================================
echo [1/3] 正在从 Joplin 同步笔记...
!PYTHON! joplin_sync.py --notebook "博客文章"
if !errorlevel! neq 0 (
    echo.
    echo ============================================
    echo   同步失败！
    echo ============================================
    echo.
    echo   请检查：
    echo   1. Joplin 是否正在运行
    echo   2. Web Clipper 服务是否已启用
    echo      (工具 → 选项 → Web Clipper)
    echo.
    pause
    exit /b 1
)

REM ============================================================
REM [2/3] Git 提交
REM ============================================================
echo.
echo [2/3] 提交到 Git...
"!GIT!" add _posts/
"!GIT!" commit -m "sync: Joplin 博客自动同步 %date%"
if !errorlevel! neq 0 (
    echo [提示] 没有新的变更需要提交（可能已全部同步）
)

REM ============================================================
REM [3/3] Git 推送
REM ============================================================
echo.
echo [3/3] 推送到 GitHub...
"!GIT!" push
if !errorlevel! neq 0 (
    echo.
    echo ============================================
    echo   推送失败！请检查网络和 Git 认证
    echo ============================================
    pause
    exit /b 1
)

echo.
echo ============================================
echo   完成！等待 1-2 分钟后刷新博客
echo   https://cnfeat.com
echo ============================================
pause
