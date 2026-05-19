# MuMuAINovel 快速入门

## 🚀 三步开始使用

### 1️⃣ 运行程序

双击 `MuMuAINovel.exe`（Windows）或运行 `./MuMuAINovel`（macOS/Linux）

### 2️⃣ 配置 API

在程序同级目录创建 `.env` 文件：

```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3️⃣ 开始创作

浏览器会自动打开 http://127.0.0.1:8000

默认账号：
- 用户名：`admin`
- 密码：`admin123`

---

## 📝 常见配置示例

### 使用国内中转

```env
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://your-proxy.com/v1
```

### 使用 Claude

```env
ANTHROPIC_API_KEY=your-anthropic-key
DEFAULT_AI_PROVIDER=anthropic
DEFAULT_MODEL=claude-3-5-sonnet-20241022
```

### 修改端口

```env
APP_PORT=8080
```

---

## 💾 数据位置

| 内容 | 位置 |
|------|------|
| 小说、角色等数据 | `data/mumu_ainovel.db` |
| 日志 | `logs/` |
| AI 生成的封面 | `storage/generated_covers/` |

---

## 🆘 需要帮助？

查看 `README_PACKAGE.md` 获取详细说明。
