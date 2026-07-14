# AI 知识库 · 编码规范 v0.1

## 要做什么

### 语言 & 工具

| 配置     | 工具                  | 规则                                    |
| -------- | --------------------- | --------------------------------------- |
| 格式化   | black                 | 行宽 88、PEP 8                          |
| Lint     | ruff                  | E/F/I/N/W/UP/B/SIM/ARG/PTH/PL/TOD/C90 规则组 |
| 类型检查 | mypy --strict         | 全覆盖类型注解、no_implicit_optional    |
| 测试     | pytest + pytest-cov   | 单测覆盖率 ≥ 80%，`--cov-fail-under=80` |

### 代码要求

- Python 使用 **black** 格式化，CI 上运行 `black --check .`。如需改用 `ruff format` 须经团队一致同意并同步修改所有配置
- 标识符一律使用 **snake_case**
- **所有公开函数必须有 Google 风格 docstring**（含 Args / Returns / Raises）
- **类型注解全覆盖**（`from __future__ import annotations`）
- **禁止裸 `print()`** — 统一使用 `logging`（使用 `logging.getLogger(__name__)`）
- **日志分级**：`debug` / `info` / `warning` / `error` / `critical`，不得将所有信息打到同一级别
- **禁止硬编码字符串常量（魔法字符串）** — 如 API 路径、错误消息等必须提取为模块级常量或枚举
- **依赖声明**：所有运行时和开发依赖必须在 `pyproject.toml` 中显式声明，不允许依赖未声明的隐式包
- **禁止 TODO 合并到 main** — CI 通过 `ruff` 的 `TOD` 规则拦截
- **导入顺序**：标准库 → 第三方库 → 本地模块，各组之间空行分隔，使用绝对导入
- **配置管理**：API Key / Token / Secret 必须通过环境变量或 `.env` 注入，禁止硬编码进代码
- **异步规范**：
  - 所有 I/O 密集型函数（网络请求、文件读写、数据库操作）须声明为 `async def`
  - 异步函数内禁止使用 `time.sleep()`，统一使用 `asyncio.sleep()`
  - 禁止混用同步阻塞调用（如 `requests.get()`）与异步事件循环，应统一使用 `httpx.AsyncClient` / `aiohttp` 等异步库
  - 禁止在异步代码中调用 `asyncio.run()`（除顶级入口外），应使用 `asyncio.create_task()` 或 `gather()`
  - 异步上下文管理器（`async with`）和异步迭代器（`async for`）必须正确使用 `__aenter__` / `__aexit__` / `__aiter__` / `__anext__`

## 不做什么

- 不依赖未在 `pyproject.toml` 中声明的隐式依赖
- 不在 `try/except` 里吞掉所有异常不加日志 — 至少调用 `logging.exception()`
- 不将原始爬取页面不经处理直接入库 — 至少执行 HTML → Markdown 转换
- 不在 Agent 之间共享可变状态 — 使用 JSON 文件或消息队列传递不可变数据
- 不跳过 Analyzer 的 quality gate — 摘要置信度低于阈值时必须标记 `draft` 而非 `published`
- 不将 secrets 提交到 git 历史（`git secrets` / pre-commit 检测）
- 不允许 lint 警告进入 `main` 分支

## 边界 & 验收

| 边界     | 说明                                             |
| -------- | ------------------------------------------------ |
| 单测覆盖率 | ≥ 80%；`shared/`、Agent 核心逻辑（Collector / Analyzer / Publisher）模块必须 ≥ 90% |
| 类型检查   | 所有新增代码必须通过 mypy --strict                |
| 输出格式   | JSON 必须通过 JSON Schema 校验                    |
| 文件命名   | 全小写 + 下划线（`snake_case.py`）                |
| 函数长度   | 单函数不超过 60 行（不含 docstring 和空行）        |
| 圈复杂度   | 单函数 McCabe 复杂度 ≤ 10（通过 ruff `C901` 检测） |

## 怎么验证

CI (`push` / `pull_request` to `main`) 按顺序执行：

```bash
ruff check --fix .
black --check .
mypy .
pytest --cov-fail-under=80
```

- 本地提交前推荐配置 pre-commit hook，以上命令任一步失败则拦截提交。`ruff check --fix` 自动修复后，开发者须 `git add` 修改过的文件再继续提交
- Python 环境通过 `pyproject.toml` 锁定依赖版本
- mypy 在 `pyproject.toml` 的 `[tool.mypy]` 中配置 `exclude`，排除 `.opencode/`、`node_modules/` 等非 Python 目录
