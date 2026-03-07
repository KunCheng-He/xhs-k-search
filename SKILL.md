---
name: xhs-k-research
description: |
  小红书数据搜索与调研工具。通过浏览器自动化技术获取小红书搜索结果、帖子详情和评论数据。触发场景：(1) 搜索小红书关键词获取帖子列表 (2) 获取某篇帖子的详细内容和评论 (3) 进行产品调研或竞品分析需要从小红书收集数据。使用关键词如"搜索小红书"、"小红书帖子"、"小红书调研"、"XHS search"时会触发。
---

# 小红书数据搜索与调研

通过 Playwright 浏览器自动化获取小红书数据，支持关键词搜索和帖子详情获取。

## 环境要求

- Python 3.10+
- uv 包管理器
- Chromium 浏览器

首次使用前需安装依赖：

```bash
cd scripts && uv sync && uv run playwright install chromium
```

## 工作流程

### 1. 检查登录状态

登录状态存储在 `scripts/auth.json`。检查该文件是否存在：

```bash
ls scripts/auth.json
```

### 2. 登录（如需要）

若 `auth.json` 不存在或已过期：

```bash
cd scripts && uv run python main.py --login
```

会打开浏览器窗口，用户扫码登录后自动保存状态。

### 3. 执行搜索

```bash
cd scripts && uv run python main.py --keyword "搜索关键词" --headless
```

返回 JSON 格式的搜索结果，包含帖子列表（标题、作者、点赞数、评论数、链接等）。

### 4. 获取帖子详情

```bash
cd scripts && uv run python main.py --note-id <帖子ID> --xsec-token <token>
```

返回帖子正文、图片列表、标签及评论。

**注意**：帖子详情功能不支持无头模式（反爬限制），会自动弹出浏览器窗口。

## 数据结构

搜索结果见 `references/data-models.md`。

## 输出规范

调用脚本后，解析 JSON 输出并按用户需求整理：
- 搜索结果：提取相关帖子，汇总关键信息（标题、作者、互动数据）
- 帖子详情：提取正文内容、热门评论
- 调研报告：综合多个搜索结果，生成分析摘要

## 注意事项

- 登录状态有效期有限，若请求失败提示需重新登录，执行 `--login`
- 帖子详情功能强制有头模式
- 遵守小红书用户协议，仅供个人学习研究使用