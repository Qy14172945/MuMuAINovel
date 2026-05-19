#!/bin/bash

echo "========================================"
echo "MuMuAINovel 打包脚本"
echo "========================================"
echo ""

cd "$(dirname "$0")/.."

# 检查 Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.11 或更高版本"
    exit 1
fi

# 使用 python3 或 python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "[错误] 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

echo "[1/6] 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    $PYTHON_CMD -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r ../package/requirements-package.txt
cd ..

echo ""
echo "[2/6] 安装前端依赖..."
cd frontend
npm install || npm install --registry=https://registry.npmmirror.com
cd ..

echo ""
echo "[3/6] 构建前端..."
cd frontend
npm run build
if [ $? -ne 0 ]; then
    echo "[错误] 前端构建失败"
    exit 1
fi
cd ..

echo ""
echo "[4/6] 复制启动器到后端目录..."
cp package/launcher.py backend/launcher.py

echo ""
echo "[5/6] 使用 PyInstaller 打包..."
cd backend
source venv/bin/activate

# 清理旧的构建文件
rm -rf build dist

# 复制配置文件
cp alembic-sqlite.ini alembic.ini

# 运行 PyInstaller
pyinstaller --clean ../package/mumu_ainovel.spec

if [ $? -ne 0 ]; then
    echo "[错误] 打包失败"
    cd ..
    exit 1
fi

cd ..

echo ""
echo "[6/6] 整理输出文件..."
mkdir -p output
rm -f output/MuMuAINovel
cp backend/dist/MuMuAINovel output/

echo ""
echo "========================================"
echo "打包完成！"
echo "可执行文件位置: output/MuMuAINovel"
echo "========================================"
echo ""
echo "注意："
echo "1. 首次运行会自动创建数据库和配置文件"
echo "2. 默认账号: admin / admin123"
echo "3. 请在 .env 文件中配置您的 AI API Key"
echo ""
