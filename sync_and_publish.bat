@echo off
cd /d "%~dp0"

echo ============================================
echo   Joplin to Blog Sync
echo ============================================
echo.

set PYTHON=C:\Users\cnfea\.workbuddy\binaries\python\versions\3.14.3\python.exe
set GIT=C:\Program Files\Git\cmd\git.exe

echo [Step 1] Syncing from Joplin...
"%PYTHON%" joplin_sync.py --notebook "博客文章"
if %errorlevel% neq 0 (
    echo.
    echo Sync failed. Joplin running? Web Clipper on?
    pause
    exit /b 1
)

echo.
echo [Step 2] Git commit...
"%GIT%" add _posts/
"%GIT%" commit -m "sync: Joplin auto-sync %date%"

echo.
echo [Step 3] Git push...
"%GIT%" push
if %errorlevel% neq 0 (
    echo Push failed.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Done! https://cnfeat.com
echo ============================================
pause
