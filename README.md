# xhs-k-search

小红书搜索脚本，通过浏览器自动化技术获取搜索结果、帖子内容及评论数据。

## 技术栈

- Python 3.10+
- [Playwright](https://playwright.dev/) - 浏览器控制
- [playwright-stealth](https://github.com/AtinyOne/Playwright-stealth) - 反爬隐藏
- [Pydantic](https://docs.pydantic.dev/) - 数据模型

## 安装

```bash
# 安装依赖
uv sync

# 安装浏览器
uv run playwright install chromium
```

## 使用方法

### 首次登录

首次使用需要登录小红书账号：

```bash
uv run python main.py --login
```

这将打开浏览器窗口，请完成扫码登录。登录成功后，状态会自动保存到 `auth.json`。

### 搜索内容

```bash
# 有头模式（显示浏览器窗口）
uv run python main.py --keyword "Python"

# 无头模式（后台运行，适合自动化）
uv run python main.py --keyword "Python" --headless
```

## 项目结构

```
xhs-k-search/
├── .python-version      # Python 版本声明
├── pyproject.toml       # 项目依赖配置
├── auth.json            # 登录状态（自动生成）
├── main.py              # 脚本入口
├── login_helper.py      # 登录逻辑
├── xhs_utils/           # 核心模块
│   ├── browser.py       # 浏览器配置
│   ├── api_handler.py   # API 处理
│   └── data_models.py   # 数据模型
└── PLAN.md              # 技术方案
```

## 注意事项

- 请勿将 `auth.json` 提交到版本库
- 如登录状态失效，删除 `auth.json` 后重新登录
