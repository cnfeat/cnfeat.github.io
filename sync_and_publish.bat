@echo off
chcp 65001 >nul
echo ============================================
echo   Joplin → 博客 一键同步发布
echo ============================================
echo.

cd /d "%~dp0"

REM 同步 Joplin 笔记
echo [1/3] 正在从 Joplin 同步笔记...
python joplin_sync.py --notebook "博客文章"
if %errorlevel% neq 0 (
    echo.
    echo ❌ 同步失败，请检查 Joplin 是否运行且 Web Clipper 已启用
    pause
    exit /b 1
)

echo.
echo [2/3] 提交到 Git...
git add _posts/ .joplin_sync_state.json
git commit -m "sync: Joplin 博客自动同步 %date%"

echo.
echo [3/3] 推送到 GitHub...
git push

echo.
echo ✅ 完成！等待 GitHub Actions 自动部署...
echo    访问 https://cnfeat.com 查看最新文章
pause
