# AI 知识库 · 项目愿景 v1.0

## 要做什么

### 抓取策略
- 来源：GitHub Trending（daily + weekly）
- 数量：各取 Top 25，合并去重
- 筛选：先按 GitHub Topics 粗筛（`ai`, `llm`, `machine-learning`, `deep-learning`, `gpt`, `rag`, `nlp`, `agent` 等），再用 LLM 二次判定（覆盖未打标签的 AI 项目）
- 预期日产出：5~15 条有效条目
- 去重：同一仓库连续上榜仅更新条目（标注"连续上榜第 N 天"），不重复生成
- 定时：每天 9:00 UTC+8 触发，10 分钟内完成

### Agent 分析维度

| 维度 | 说明 |
|------|------|
| 一句话摘要 | 项目是干嘛的 |
| 技术亮点 | 架构/算法上与同类项目的差异 |
| 上手门槛 | README 清晰度、有无 Docker、有无 demo、有无中文文档 |
| 成熟度 | Star 趋势、Issue 活跃度、最近提交时间、是否有 release |
| 技术栈相关性 | 能否降低我方研发成本（基础设施、框架、工具链、Agent 平台等） |
| 业务场景相关性 | 能否用于小贷/信贷场景（风控、信审、催收、客服、OCR 单据识别、数据报表等） |
| 综合关联等级 | `无` / `间接` / `直接` |
| 标签 | 自动打标签（如 `RAG` / `Agent` / `Infra` / `Fine-tune` / `Tool`） |

### 输出格式
- **JSON**：结构化数据，用于检索、对接企微推送等
- **Markdown**：从 JSON 渲染，用于人直接阅读、存 Git、推送知识库

JSON Schema：
```json
{
  "id": "2026-07-13-github-trending-001",
  "repo": "owner/repo",
  "url": "https://github.com/...",
  "stars": 4200,
  "starsToday": 318,
  "language": "Python",
  "topics": ["llm", "rag"],
  "summary": "一句话摘要",
  "highlights": ["技术亮点1", "技术亮点2"],
  "onboarding": { "level": "低", "notes": "有 Docker, README 清晰" },
  "maturity": { "lastCommit": "2026-07-12", "hasRelease": true, "issueActivity": "活跃" },
  "relevance": { "tech": "直接", "business": "间接", "level": "直接" },
  "tags": ["RAG", "Infra"],
  "consecutiveDays": 3,
  "analyzedAt": "2026-07-13T09:00:00+08:00"
}
```

## 不做什么

| 不做什么 | 原因 |
|----------|------|
| 不分析 GitHub 之外的来源（arXiv、Hacker News、Product Hunt 等） | v1 聚焦单一来源 |
| 不做自动测试/运行 repo 代码 | 安全风险 + 成本高 |
| 不做个性化推荐 / 订阅 | v1 只产出内容，不涉及分发 |
| 不做历史趋势对比 / 可视化 | v2 再说 |
| 不维护中文翻译 | 英文摘要即可 |

## 边界 & 验收

### 边界
| 边界 | 说明 |
|------|------|
| 数据来源 | 仅 GitHub Trending API，不做语种过滤 |
| 处理时限 | 每天 9:00 触发，10 分钟内完成 |
| 输出存放 | JSON → `data/` 按日期分文件；Markdown → `output/` 按日期分文件 |
| 失败处理 | 单条抓取/分析失败时跳过并记日志，不影响后续条目 |
| 无需人工介入 | 全自动，仅全部失败时告警 |

### 验收标准
| 指标 | 标准 |
|------|------|
| 日产出量 | 5~15 条有效条目 |
| 格式合规 | 100% 通过 JSON Schema 校验 |
| 稳定性 | 连续 7 天无中断 |
| 误分析率 | ≤ 5% |
| 误分析判定 | LLM-as-Judge 综合评分 < 3 分算误分析 |
| 告警触发 | 连续 3 天误分析率 > 5% |

## 怎么验证

### 自动验收流程

| 验证方式 | 说明 |
|----------|------|
| Schema 校验 | 产出 JSON 自动跑 JSON Schema 校验，字段不全/类型错直接 fail |
| LLM-as-Judge | 另起独立 LLM 调用，拿原始 README 与产出条目对比，对摘要准确性、标签正确性、关联合理性各打 1-5 分 |
| 幻觉检测 | 正则匹配 + LLM 检查条目中是否出现 README 里不存在的虚假数字/功能描述 |
| 黄金基线集 | 人工预先标注 20 条作为 benchmark，每次跑完自动对比评分 |
| 一致性检查 | 连续两天同一 repo 的摘要不能矛盾（如昨天打 `RAG` 今天打 `Agent` 必须有合理变化说明） |
| 集成测试 | 用 5 个已知仓库 mock GitHub 返回，跑全流程验证产出正确 |

### 验收 Checklist
- [ ] 每天定时触发成功
- [ ] 输出文件产出在正确路径（`data/` + `output/`）
- [ ] JSON 字段齐全、类型正确
- [ ] Markdown 可读、格式统一
- [ ] 失败条目有日志，不影响其他条目
- [ ] 连续 7 天无遗漏
- [ ] 误分析率 ≤ 5%
