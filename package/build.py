"""
MuMuAINovel 跨平台构建脚本
支持 Windows、macOS 和 Linux
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_step(step, total, message):
    """打印步骤信息"""
    print(f"\n[{step}/{total}] {message}")


def run_command(cmd, cwd=None, shell=True):
    """运行命令"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        print(f"输出: {e.stdout}")
        return False


def main():
    """主函数"""
    print("=" * 40)
    print("MuMuAINovel 打包脚本")
    print("=" * 40)

    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    os.chdir(root_dir)

    # 检查 Python
    python_cmd = "python3" if sys.platform != "win32" else "python"
    try:
        subprocess.run([python_cmd, "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            python_cmd = "python"
            subprocess.run([python_cmd, "--version"], check=True, capture_output=True)
        except:
            print("[错误] 未找到 Python")
            return 1

    # 检查 Node.js
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
    except:
        print("[错误] 未找到 Node.js")
        return 1

    total_steps = 6

    # 步骤 1: 安装后端依赖
    print_step(1, total_steps, "安装后端依赖...")
    backend_dir = root_dir / "backend"
    venv_dir = backend_dir / "venv"

    if not venv_dir.exists():
        print("创建虚拟环境...")
        if not run_command(f"{python_cmd} -m venv venv", cwd=backend_dir):
            return 1

    # 激活虚拟环境并安装依赖
    if sys.platform == "win32":
        pip_cmd = f"{venv_dir / 'Scripts' / 'pip.exe'}"
    else:
        pip_cmd = f"{venv_dir / 'bin' / 'pip'}"

    if not run_command(f"{pip_cmd} install --upgrade pip"):
        return 1
    if not run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir):
        return 1
    if not run_command(f"{pip_cmd} install -r ../package/requirements-package.txt", cwd=backend_dir):
        return 1

    # 步骤 2: 安装前端依赖
    print_step(2, total_steps, "安装前端依赖...")
    frontend_dir = root_dir / "frontend"
    if not run_command("npm install", cwd=frontend_dir):
        print("尝试使用淘宝镜像...")
        if not run_command("npm install --registry=https://registry.npmmirror.com", cwd=frontend_dir):
            return 1

    # 步骤 3: 构建前端
    print_step(3, total_steps, "构建前端...")
    if not run_command("npm run build", cwd=frontend_dir):
        return 1

    # 步骤 4: 复制启动器
    print_step(4, total_steps, "复制启动器到后端目录...")
    shutil.copy(
        root_dir / "package" / "launcher.py",
        backend_dir / "launcher.py"
    )

    # 步骤 5: PyInstaller 打包
    print_step(5, total_steps, "使用 PyInstaller 打包...")

    # 清理旧文件
    for dir_name in ["build", "dist"]:
        dir_path = backend_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)

    # 复制配置文件
    shutil.copy(
        backend_dir / "alembic-sqlite.ini",
        backend_dir / "alembic.ini"
    )

    # 运行 PyInstaller
    if sys.platform == "win32":
        pyinstaller_cmd = f"{venv_dir / 'Scripts' / 'pyinstaller.exe'}"
    else:
        pyinstaller_cmd = f"{venv_dir / 'bin' / 'pyinstaller'}"

    spec_file = root_dir / "package" / "mumu_ainovel.spec"
    if not run_command(f"{pyinstaller_cmd} --clean {spec_file}", cwd=backend_dir):
        return 1

    # 步骤 6: 整理输出
    print_step(6, total_steps, "整理输出文件...")
    output_dir = root_dir / "output"
    output_dir.mkdir(exist_ok=True)

    exe_name = "MuMuAINovel.exe" if sys.platform == "win32" else "MuMuAINovel"
    src_exe = backend_dir / "dist" / exe_name
    dst_exe = output_dir / exe_name

    if dst_exe.exists():
        dst_exe.unlink()
    shutil.copy(src_exe, dst_exe)

    # 完成
    print("\n" + "=" * 40)
    print("打包完成！")
    print(f"可执行文件位置: {dst_exe}")
    print("=" * 40)
    print("\n注意：")
    print("1. 首次运行会自动创建数据库和配置文件")
    print("2. 默认账号: admin / admin123")
    print("3. 请在 .env 文件中配置您的 AI API Key")

    return 0


if __name__ == "__main__":
    sys.exit(main())
