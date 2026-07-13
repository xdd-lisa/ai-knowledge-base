# AGENTS.md

## 项目概述
- 每天自动抓取 GitHub Trending（daily + weekly），筛选 AI 相关仓库，用 Agent 分析后产出结构化知识条目。

## 抓取策略
- 来源：GitHub Trending，同时拉 daily 和 weekly
- 数量：各取 Top 25，合并去重
- 筛选流程：
  1. 先按 GitHub Topics 粗筛，命中关键词（`ai`, `llm`, `machine-learning`, `deep-learning`, `gpt`, `rag`, `nlp`, `agent` 等）的仓库进入候选
  2. 再用 LLM 对候选仓库做二次判定，覆盖未打标签的 AI 项目
- 预期日产出：5~15 条有效条目
- 去重：同一仓库连续上榜时仅更新已有条目，标注"连续上榜第 N 天"，不重复生成新条目
- 定时：每天 9:00 UTC+8 触发，10 分钟内完成全流程

## Agent 分析维度
对每条候选仓库，Agent 必须产出以下维度：

| 维度 | 产出要求 |
|------|----------|
| 一句话摘要 | 用一句话说清项目是干嘛的 |
| 技术亮点 | 列出架构/算法上与同类项目的差异点 |
| 上手门槛 | 评估 README 清晰度、有无 Docker、有无 demo、有无中文文档，给出 level（低/中/高）及备注 |
| 成熟度 | 评估 Star 趋势、Issue 活跃度、最近提交时间、是否有 release |
| 技术栈相关性 | 判断能否降低我方研发成本（基础设施、框架、工具链、Agent 平台等），给出评级（直接/间接/无） |
| 业务场景相关性 | 判断能否用于小贷/信贷场景（风控、信审、催收、客服、OCR 单据识别、数据报表等），给出评级（直接/间接/无） |
| 综合关联等级 | 综合技术和业务，给出最终等级：`无` / `间接` / `直接` |
| 标签 | 从 `RAG` / `Agent` / `Infra` / `Fine-tune` / `Tool` 中选择匹配的标签 |

## 输出格式
- 每条条目同时产出 **JSON** 和 **Markdown**
- JSON：结构化数据，存于 `data/` 目录，按日期分文件，用于检索、对接企微推送等
- Markdown：从 JSON 渲染生成，存于 `output/` 目录，按日期分文件，用于人直接阅读、存 Git、推送知识库

### JSON Schema（每条条目必须符合）
```json
{
  "id": "string, 格式 2026-07-13-github-trending-001",
  "repo": "string, owner/repo",
  "url": "string, 仓库完整 URL",
  "stars": "number, 总 Star 数",
  "starsToday": "number, 当日新增 Star",
  "language": "string, 主编程语言",
  "topics": ["string, GitHub Topics 列表"],
  "summary": "string, 一句话摘要",
  "highlights": ["string, 技术亮点列表"],
  "onboarding": {
    "level": "string, 低 | 中 | 高",
    "notes": "string, 上手门槛备注"
  },
  "maturity": {
    "lastCommit": "string, 最近提交日期",
    "hasRelease": "boolean, 是否有正式 release",
    "issueActivity": "string, 活跃 | 一般 | 不活跃"
  },
  "relevance": {
    "tech": "string, 直接 | 间接 | 无",
    "business": "string, 直接 | 间接 | 无",
    "level": "string, 无 | 间接 | 直接"
  },
  "tags": ["string, RAG | Agent | Infra | Fine-tune | Tool"],
  "consecutiveDays": "number, 连续上榜天数",
  "analyzedAt": "string, ISO 8601 时间戳"
}
```

## 不做什么（明确排除）
- 不分析 GitHub 之外的来源（arXiv、Hacker News、Product Hunt 等），v1 仅聚焦 GitHub Trending
- 不做自动测试/运行 repo 代码，避免安全风险和高成本
- 不做个性化推荐 / 订阅，v1 只产出内容不涉及分发
- 不做历史趋势对比 / 可视化，留到 v2
- 不维护中文翻译，保留英文摘要即可

## 边界约束
- 数据来源：仅使用 GitHub Trending API，不做语种过滤
- 处理时限：每天 9:00 UTC+8 触发，10 分钟内必须跑完
- 输出存放：JSON → `data/` 按日期分文件，Markdown → `output/` 按日期分文件
- 失败处理：单条抓取/分析失败时跳过该条目并记录日志，不得阻塞后续条目
- 无需人工介入：流程必须全自动，仅在所有条目全部失败时触发告警

## 验收标准

| 指标 | 标准 |
|------|------|
| 日产出量 | 5~15 条有效条目 |
| 格式合规 | 100% 通过 JSON Schema 校验 |
| 稳定性 | 连续 7 天运行无中断 |
| 误分析率 | ≤ 5% |
| 误分析判定 | LLM-as-Judge 综合评分 < 3 分即算误分析 |
| 告警触发 | 连续 3 天误分析率 > 5% 时告警 |

## 验证方式

### Schema 校验
- 产出 JSON 必须通过 JSON Schema 校验，字段不全或类型错误直接判定失败

### LLM-as-Judge
- 另起独立 LLM 调用，拿原始 README 内容与产出条目进行对比
- 对摘要准确性、标签正确性、关联合理性各打 1~5 分
- 综合评分 < 3 分的条目计为误分析

### 幻觉检测
- 正则匹配 + LLM 检查：条目中不得出现 README 中不存在的数据（虚假数字、编造的功能描述等）

### 黄金基线集
- 人工预先标注 20 条仓库的期望分析结果作为 benchmark
- 每次运行后与新产出自动对比，计算评分偏差

### 一致性检查
- 同一仓库连续两天对比，摘要和标签不能矛盾
- 如昨天标签为 `RAG` 今天变为 `Agent`，必须有变动说明

### 集成测试
- 用 5 个已知仓库 mock GitHub API 返回，跑全流程验证产出正确性

## 验收 Checklist
- [ ] 每天定时触发成功
- [ ] 输出文件生成在正确路径（`data/` + `output/`）
- [ ] JSON 字段齐全、类型正确
- [ ] Markdown 可读、格式统一
- [ ] 失败条目有日志、不影响其他条目
- [ ] 连续 7 天无遗漏
- [ ] 误分析率 ≤ 5%
