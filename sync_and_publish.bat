@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "PYTHON=C:\Users\cnfea\.workbuddy\binaries\python\versions\3.14.3\python.exe"
set "GIT=C:\Program Files\Git\cmd\git.exe"

echo ============================================
echo   Joplin - Blog Sync & Publish
echo ============================================
echo.
echo [Python] %PYTHON%
echo [Git]    %GIT%
echo.

REM Step 1: Sync from Joplin
echo [1/3] Syncing from Joplin...
"%PYTHON%" joplin_sync.py --notebook "博客文章"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Sync failed.
    echo   - Is Joplin running?
    echo   - Is Web Clipper enabled? (Tools - Options - Web Clipper)
    pause
    exit /b 1
)

REM Step 2: Git commit
echo.
echo [2/3] Committing to Git...
"%GIT%" add _posts/
"%GIT%" commit -m "sync: Joplin auto-sync %date%"
if %errorlevel% equ 0 (
    echo [OK] Committed.
) else (
    echo [INFO] Nothing new to commit.
)

REM Step 3: Git push
echo.
echo [3/3] Pushing to GitHub...
"%GIT%" push
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Push failed. Check network or git auth.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Done! Wait 1-2 min, then refresh:
echo   https://cnfeat.com
echo ============================================
pause
