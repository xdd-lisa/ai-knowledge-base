---
name: tech-summary
description: 当需要对采集的技术内容进行深度分析总结时使用此技能
allowed-tools: [Read, Grep, Glob, WebFetch]
---

# 技术内容深度分析技能

## 使用场景

- 需要对 `knowledge/raw/` 中的原始采集数据进行结构化分析时
- 需要为每个项目生成摘要、亮点、评分和标签时
- 需要从批量项目中识别共同趋势和新兴概念时

## 执行步骤

1. **读取采集数据**：通过 Glob 查找 `knowledge/raw/` 中最新日期的 JSON 文件，Read 读取全部条目
2. **逐条深度分析**：对每条项目执行以下分析：
   - 中文摘要（≤ 50 字，突出项目核心价值）
   - 2-3 个技术亮点，用事实和数据说话（如 Star 数、性能指标、独特功能）
   - 1-10 分评分，附评分理由
   - 标签建议（从 `RAG` / `Agent` / `Infra` / `Fine-tune` / `Tool` / `LLM` / `NLP` / `Multi-modal` 中选择）
3. **趋势发现**：分析全部项目后，归纳共同主题、新兴概念、领域热点方向
4. **输出 JSON**：写入 `knowledge/articles/tech-summary-YYYY-MM-DD.json`

## 评分标准

| 分值  | 含义     | 说明                     |
| ----- | -------- | ------------------------ |
| 9-10  | 改变格局 | 可能影响行业方向或研发架构 |
| 7-8   | 直接有帮助 | 可降低我方研发成本或直接落地 |
| 5-6   | 值得了解 | 有参考价值，暂时不急需    |
| 1-4   | 可略过   | 与 AI 知识库相关性低       |

## 约束

- 15 个项目中，9-10 分（改变格局）不超过 2 个
- 摘要必须使用中文，不得编造原文不存在的内容
- 亮点须有事实支撑，避免泛泛而谈
- 标签从预定义词表中选择

## 注意事项

- 分析前先通过 WebFetch 访问项目 GitHub 页面获取最新 README 上下文
- 评分应拉开差距，避免所有项目集中在同一分数段
- 趋势发现应基于本次采集项目中的实际规律，而非泛泛的行业趋势

## 输出格式

```json
{
  "source": "github_trending",
  "skill": "tech-summary",
  "analyzed_at": "2026-07-14T10:00:00+08:00",
  "trends": {
    "common_themes": ["主题1", "主题2"],
    "emerging_concepts": ["新概念1", "新概念2"]
  },
  "items": [
    {
      "name": "owner/repo",
      "url": "https://github.com/owner/repo",
      "summary": "≤50 字中文摘要",
      "highlights": ["亮点1（附事实）", "亮点2（附事实）"],
      "score": 8,
      "score_reason": "评分理由",
      "tags": ["Agent", "LLM"]
    }
  ]
}
```
