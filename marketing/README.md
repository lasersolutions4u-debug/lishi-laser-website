# LISHI LASER 营销资产库

> ⚠️ **营销管理已迁移至 Notion**（2026-05-06）
> 主入口：https://www.notion.so/35895643234781ceb231e1510c77d401
> 以下 Markdown 文件为初始存档，后续以 Notion 为准。
> 每月 1 日自动从 Notion 导出回写 `notion-export/` 目录。

## 工作流程

```
你在 Notion 改内容/标状态（日常）
        ↓
每月 1 日自动提醒导出
        ↓
Claude 从 Notion fetch 全量内容
        ↓
回写到 notion-export/ 目录（本地备份）
```

> 如需手动触发导出，在对话中说「导出 Notion 营销内容」。

## 目录结构

```
marketing/
├── README.md              ← 你在这里
├── .notion-sync-map.json  ← Notion 页面映射配置
├── notion-export/         ← 从 Notion 导出的最新内容（本地备份）
├── skills/                ← 方法论和能力指南（初始存档）
├── content/               ← 具体内容资产和模板（初始存档）
├── plans/                 ← 执行计划和时间表（初始存档）
└── research/              ← 市场研究和渠道分析（初始存档）
```

## Skills（方法论）

| 文档 | 说明 | 状态 |
|------|------|------|
| [linkedin-strategy.md](skills/linkedin-strategy.md) | LinkedIn 营销完整方法论 | ✅ 已创建 |
| [email-marketing.md](skills/email-marketing.md) | Email 营销手册 | 待创建 |
| [print-materials-guide.md](skills/print-materials-guide.md) | 印刷品设计制作指南 | ✅ 已创建 |
| [seo-strategy.md](skills/seo-strategy.md) | SEO 策略参考 | 待创建 |
| [b2b-platforms.md](skills/b2b-platforms.md) | ThomasNet / DirectIndustry 运营 | 待创建 |
| [analytics-reporting.md](skills/analytics-reporting.md) | 网站数据分析自动化报告 | ✅ 已创建 |

## Content（内容资产）

| 文档 | 说明 | 状态 |
|------|------|------|
| [print-collateral-plan.md](content/print-collateral-plan.md) | 5 件印刷品完整方案 | ✅ 已迁移 |
| [cover-letter-template.md](content/cover-letter-template.md) | 邮寄附信模板（英文） | ✅ 已创建 |
| [linkedin-templates.md](content/linkedin-templates.md) | LinkedIn 帖子/文章模板 | ✅ 已创建 |
| [email-templates.md](content/email-templates.md) | Email 序列模板 | 待创建 |

## Plans（执行计划）

| 文档 | 说明 | 状态 |
|------|------|------|
| [youtube-channel-plan.md](plans/youtube-channel-plan.md) | YouTube 频道启动计划 | ✅ 已迁移 |
| [linkedin-launch-plan.md](plans/linkedin-launch-plan.md) | LinkedIn 冷启动计划 | ✅ 已创建 |

## Research（市场研究）

| 文档 | 说明 | 状态 |
|------|------|------|
| [channel-analysis.md](research/channel-analysis.md) | 各推广渠道效果分析 | ✅ 已创建 |

## 维护规则

1. **Skills 文档** — 记录方法论和最佳实践。每次学到新东西时更新。
2. **Content 文档** — 记录具体内容资产（文案、模板、设计方案）。制作完成后归档。
3. **Plans 文档** — 记录执行计划和时间表。完成后标记状态并归档关键数据。
4. **Research 文档** — 记录市场情报和渠道评估。有新发现时补充。
