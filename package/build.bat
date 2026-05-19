@echo off
chcp 65001 >nul
echo ========================================
echo MuMuAINovel 打包脚本
echo ========================================
echo.

cd /d "%~dp0.."

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.11 或更高版本
    pause
    exit /b 1
)

REM 检查 Node.js 是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)

echo [1/6] 安装后端依赖...
cd backend
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
pip install -r ..\package\requirements-package.txt
cd ..

echo.
echo [2/6] 安装前端依赖...
cd frontend
call npm install
if errorlevel 1 (
    echo [警告] npm install 失败，尝试使用淘宝镜像...
    call npm install --registry=https://registry.npmmirror.com
)
cd ..

echo.
echo [3/6] 构建前端...
cd frontend
call npm run build
if errorlevel 1 (
    echo [错误] 前端构建失败
    pause
    exit /b 1
)
cd ..

echo.
echo [4/6] 复制启动器到后端目录...
copy package\launcher.py backend\launcher.py

echo.
echo [5/6] 使用 PyInstaller 打包...
cd backend
call venv\Scripts\activate.bat

REM 清理旧的构建文件
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM 复制配置文件
copy alembic-sqlite.ini alembic.ini

REM 运行 PyInstaller
pyinstaller --clean ..\package\mumu_ainovel.spec

if errorlevel 1 (
    echo [错误] 打包失败
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo [6/6] 整理输出文件...
if not exist "output" mkdir output
if exist "output\MuMuAINovel.exe" del /q output\MuMuAINovel.exe
copy backend\dist\MuMuAINovel.exe output\

echo.
echo ========================================
echo 打包完成！
echo 可执行文件位置: output\MuMuAINovel.exe
echo ========================================
echo.
echo 注意：
echo 1. 首次运行会自动创建数据库和配置文件
echo 2. 默认账号: admin / admin123
echo 3. 请在 .env 文件中配置您的 AI API Key
echo.
pause
