---
name: github-trending
description: 当需要采集 GitHub 热门开源项目时使用此技能
allowed-tools: [Read, Grep, Glob, WebFetch]
---

# GitHub Trending 采集技能

## 使用场景

- 每日定时采集 GitHub Trending 的 AI/LLM/Agent 领域热门项目
- 需要获取 GitHub 热门项目的结构化数据用于知识库入库
- 需要排除 Awesome 列表等非项目类仓库

## 执行步骤

1. **搜索热门仓库**：通过 GitHub API (`https://api.github.com/search/repositories`) 或 GitHub Trending 页面获取本周热门项目，搜索关键词覆盖 `ai`、`llm`、`machine-learning`、`deep-learning`、`gpt`、`rag`、`nlp`、`agent` 等
2. **提取信息**：从搜索结果中提取仓库名称、URL、Star 数、语言、Topics、简介
3. **过滤**：纳入 AI/LLM/Agent 相关项目，排除 Awesome 列表（如 `awesome-*`）、纯文档仓库和无代码项目
4. **去重**：与 `knowledge/articles/` 中已有条目对比 URL，已存在的跳过
5. **撰写中文摘要**：按公式 `项目名 + 做什么 + 为什么值得关注` 生成 30-50 字摘要
6. **排序取 Top 15**：按 Star 增量降序排列，取前 15 条
7. **输出 JSON**：写入 `knowledge/raw/github-trending-YYYY-MM-DD.json`

## 注意事项

- 优先使用 GitHub Search API 而非页面爬取，API 数据更结构化
- 每日采集一次即可，避免频繁请求触发 API 限流
- Awesome 列表和其他纯资源汇总类项目应排除
- 摘要必须使用中文，简洁准确，不编造原文不存在的内容
- 输出文件路径中的日期使用采集当天的日期

## 输出格式

```json
{
  "source": "github_trending",
  "skill": "github-trending",
  "collected_at": "2026-07-14T09:00:00+08:00",
  "items": [
    {
      "name": "owner/repo",
      "url": "https://github.com/owner/repo",
      "summary": "项目名 + 做什么 + 为什么值得关注",
      "stars": 214548,
      "language": "Python",
      "topics": ["ai", "llm", "agent"]
    }
  ]
}
```
