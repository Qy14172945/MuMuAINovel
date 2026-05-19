# MuMuAINovel 打包说明

## 快速开始

### 方式一：使用预打包版本（推荐）

如果您有预编译好的 `MuMuAINovel.exe`（Windows）或 `MuMuAINovel`（macOS/Linux）：

1. 双击运行可执行文件
2. 首次运行会自动创建以下目录：
   - `data/` - 数据库文件
   - `logs/` - 日志文件
   - `storage/` - 生成的封面等文件
3. 浏览器会自动打开 `http://127.0.0.1:8000`
4. 使用默认账号登录：
   - 用户名：`admin`
   - 密码：`admin123`
5. **重要**：在可执行文件同级目录创建 `.env` 文件，配置您的 AI API Key

### 方式二：从源码打包

#### 前置要求

- Python 3.11 或更高版本
- Node.js 18 或更高版本
- 8GB+ 可用内存
- 10GB+ 可用磁盘空间

#### Windows 系统

```cmd
cd package
build.bat
```

#### macOS / Linux 系统

```bash
cd package
chmod +x build.sh
./build.sh
```

#### 跨平台 Python 脚本（推荐）

```bash
cd package
python build.py
```

打包完成后，可执行文件位于 `output/` 目录。

---

## 配置说明

### 基础配置

在可执行文件同级目录创建 `.env` 文件：

```env
# 必须配置：AI API Key
OPENAI_API_KEY=sk-your-actual-api-key
OPENAI_BASE_URL=https://api.openai.com/v1

# 可选：使用其他 AI 提供商
# ANTHROPIC_API_KEY=your_anthropic_key
# GEMINI_API_KEY=your_gemini_key

# 可选：修改默认配置
DEFAULT_AI_PROVIDER=openai
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.7

# 可选：修改端口
APP_PORT=8000

# 可选：修改默认账号
LOCAL_AUTH_USERNAME=your_username
LOCAL_AUTH_PASSWORD=your_password
```

### OpenAI 兼容中转服务

如果使用国内中转服务：

```env
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://your-proxy-url.com/v1
```

---

## 使用说明

### 首次运行

1. 运行 `MuMuAINovel.exe`
2. 等待服务器启动（约 5-10 秒）
3. 浏览器会自动打开
4. 登录后开始使用

### 数据存储

- **数据库**：`data/mumu_ainovel.db` (SQLite)
- **日志**：`logs/` 目录
- **生成的封面**：`storage/generated_covers/`

### 备份数据

只需备份整个程序目录，包括：
- `data/` - 数据库
- `storage/` - 生成的文件
- `.env` - 配置文件

---

## 常见问题

### Q: 杀毒软件报毒怎么办？

A: 这是 PyInstaller 打包程序的常见误报。请：
1. 添加信任
2. 或从源码自行打包

### Q: 运行很慢怎么办？

A: 首次启动需要初始化，后续会快很多。确保：
- 关闭其他占用内存的程序
- 使用 SSD 存储

### Q: 如何修改端口？

A: 在 `.env` 文件中设置：
```env
APP_PORT=8080
```

### Q: 忘记密码怎么办？

A: 删除 `data/mumu_ainovel.db` 重新运行，或在 `.env` 中重新设置：
```env
LOCAL_AUTH_PASSWORD=new_password
```

### Q: 支持多个用户吗？

A: 打包版本使用单用户 SQLite，适合个人使用。如需多用户，请使用 Docker 部署 PostgreSQL 版本。

---

## 技术细节

### 打包架构

- **后端**：Python + FastAPI + SQLite
- **前端**：React + Ant Design（预构建为静态文件）
- **打包工具**：PyInstaller
- **数据库迁移**：Alembic

### 文件结构

```
MuMuAINovel.exe/
├── data/
│   └── mumu_ainovel.db      # SQLite 数据库
├── logs/                    # 日志文件
├── storage/
│   └── generated_covers/    # AI 生成的封面
└── .env                     # 配置文件（需手动创建）
```

---

## 从源码打包详细步骤

如果自动化脚本失败，可以手动执行：

### 1. 准备环境

```bash
# 后端
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller

# 前端
cd ../frontend
npm install
```

### 2. 构建前端

```bash
cd frontend
npm run build
# 构建产物会输出到 backend/static/
```

### 3. 准备打包文件

```bash
cd ../backend
cp ../package/launcher.py .
cp alembic-sqlite.ini alembic.ini
```

### 4. 运行 PyInstaller

```bash
pyinstaller --clean ../package/mumu_ainovel.spec
```

### 5. 获取结果

可执行文件位于 `backend/dist/MuMuAINovel.exe`

---

## 许可证

本项目使用 GPL v3 许可证。
