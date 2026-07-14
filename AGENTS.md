# AGENTS.md — AI Knowledge Base Assistant

## 项目概述

AI 知识库助手是一个自动化知识管理 pipeline，每天定时从 GitHub Trending 和 Hacker News 采集 AI/LLM/Agent 领域最新技术动态，利用大语言模型进行分析与摘要，产出结构化 JSON 知识条目，并通过 Telegram / 飞书机器人分发到团队。

## 技术栈

| 层       | 工具 / 框架                          |
| -------- | ------------------------------------ |
| 语言     | Python 3.12                          |
| AI 编排  | OpenCode + 国产大模型 (DeepSeek/Qwen) |
| 工作流   | LangGraph                            |
| 爬虫引擎 | OpenClaw                             |
| 存储     | JSON 文件（本地 / 对象存储）           |

## 编码规范 v0.1

### 语言 & 工具
| 配置        | 工具            | 规则                                        |
| ----------- | --------------- | ------------------------------------------- |
| 格式化      | black           | 行宽 88、PEP 8、不允许 TODO 提交到 main     |
| Lint        | ruff            | E/F/I/N/W/UP/B/SIM/ARG/PTH/PL 规则组        |
| 类型检查    | mypy --strict   | 全覆盖类型注解、no_implicit_optional         |
| 测试        | pytest + pytest-cov | 单测覆盖率 ≥ 80%，`--cov-fail-under=80` |

### 代码要求
- Python 用 **black** 格式化，CI 上 `black --check .`
- 标识符一律使用 **snake_case**
- **所有公开函数必须有 Google 风格 docstring**（含 Args / Returns / Raises）
- **禁止裸 `print()`** — 统一使用 `logging`（已配置 `logging.getLogger(__name__)`）
- **类型注解全覆盖**（`from __future__ import annotations`）
- **禁止硬编码字符串常量**（如 API 路径、错误消息等），使用模块级常量
- **不允许 TODO 合并到 main** — CI 将检查 `ruff` 的 `TODO` 规则（`TOD`）
- **不允许在 `try/except` 里吞掉所有异常不加日志** — 至少 `logging.exception()`

### 验证方式
CI (`push` / `pull_request` to `main`) 按序执行：
1. `black --check .`
2. `ruff check .`
3. `mypy .`
4. `pytest --cov-fail-under=80`

## 项目结构

```
.opencode/
├── agents/          # OpenCode Agent 定义（YAML）
├── skills/          # Agent 技能模块
├── knowledge/
│   ├── raw/         # 原始抓取结果（无结构化）
│   └── articles/    # AI 分析后的知识条目
└── shared/          # 工具函数 & 数据模型
```

## 知识条目 JSON 格式

```json
{
  "id": "uuid-v4",
  "title": "文章/仓库标题",
  "source_url": "https://...",
  "source_type": "github_trending | hacker_news",
  "summary": "AI 生成的 100-200 字技术摘要",
  "tags": ["LLM", "Agent", "RAG"],
  "status": "draft | published | archived",
  "collected_at": "2026-07-14T10:00:00+08:00",
  "analyzed_at": "2026-07-14T10:05:00+08:00"
}
```

## Agent 角色概览

| 角色     | 职责                                  | 触发方式     |
| -------- | ------------------------------------- | ------------ |
| Collector | 爬取 GitHub Trending + Hacker News    | Cron 每日 9:00 |
| Analyzer  | 调用 LLM 生成摘要、打标、quality gate | Collector 完成时 |
| Publisher | 将知识条目分发到 Telegram / 飞书       | Analyzer 完成时 |

每个 Agent 独立定义在 `.opencode/agents/` 下，依赖通过 `.opencode/shared/` 中的工具函数共享。

## 红线（绝对禁止）

1. **不允许在代码中硬编码 API Key / Token / Secret** — 必须通过环境变量或 `.env` 注入
2. **不允许将原始爬取页面不经处理直接入库** — 至少执行 HTML→Markdown 转换
3. **不允许在 Agent 之间共享可变状态** — 使用 JSON 文件或消息队列传递不可变数据
4. **不允许跳过 Analyzer 的 quality gate** — 摘要置信度低于阈值时必须标记 `draft` 而非 `published`
5. **不允许在 `try/except` 里吞掉所有异常不加日志** — 至少 `logging.exception()`
