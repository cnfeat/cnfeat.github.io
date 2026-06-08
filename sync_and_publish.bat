@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================
echo   Joplin - Blog Sync
echo ============================================
echo.

REM Find Python
set PYTHON=
for %%p in (python3 python py) do (
    if not defined PYTHON (
        where /q %%p 2>nul
        if !errorlevel! equ 0 set PYTHON=%%p
    )
)

if not defined PYTHON (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)
echo [Python] !PYTHON!

REM Find Git
set GIT=git
where /q git 2>nul
if !errorlevel! neq 0 (
    echo [ERROR] Git not found. Please install Git first.
    pause
    exit /b 1
)
echo [Git] !GIT!
echo.

REM Step 1: Sync from Joplin
echo [1/3] Syncing from Joplin...
!PYTHON! joplin_sync.py --notebook "博客文章"
if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Sync failed.
    echo   1. Check if Joplin is running
    echo   2. Check if Web Clipper is enabled
    pause
    exit /b 1
)

REM Step 2: Git commit
echo.
echo [2/3] Committing to Git...
"!GIT!" add _posts/
"!GIT!" commit -m "sync: Joplin auto-sync %date%"

REM Step 3: Git push
echo.
echo [3/3] Pushing to GitHub...
"!GIT!" push
if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Push failed. Please check your network and Git auth.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Done! Wait 1-2 min for deployment.
echo   https://cnfeat.com
echo ============================================
pause
