# 网站数据分析报告 — 自动化技能

> 从 Cloudflare Analytics 拉取 gasmixtech.com 流量数据，生成专业报告并推送至 Notion 营销中心。
> 创建：2026-05-07 | 维护：Claude Code

## 数据源

| 数据源 | 可获取维度 | 限制 | 状态 |
|--------|-----------|------|------|
| Cloudflare GraphQL (`httpRequests1dGroups`) | 日期、请求数、PV、UV、带宽 | 仅 date 维度，30天范围 | ✅ 可用 |
| Cloudflare GraphQL (`httpRequestsAdaptiveGroups`) | 国家、页面路径、状态码、浏览器 | **单日查询**（免费计划限制） | ✅ 可用（需逐日） |
| Google Analytics 4 (GA4) | 用户行为、会话、转化 | 需 OAuth/Service Account | ❌ 未接入 |
| Google Search Console | 搜索词、点击、排名 | 需 OAuth | ❌ 未接入 |

## 技术要点

### Cloudflare API 认证
- Token 位置：`~/Library/Preferences/.wrangler/config/default.toml` 中的 `oauth_token`
- Token 每日过期，需重新从文件读取
- Scopes 需包含 `zone:read`

### Zone ID
- gasmixtech.com: `257134b24262d28c342f40efd8d6c9a7`
- Account ID: `2648afebf10fce6324f955fc0c1c6dc0`

### GraphQL 查询模板

**1. 30天日趋势（`httpRequests1dGroups`，支持宽日期范围）：**
```graphql
{
  viewer {
    zones(filter: {zoneTag: "ZONE_ID"}) {
      httpRequests1dGroups(
        limit: 40,
        filter: {date_geq: "YYYY-MM-DD", date_leq: "YYYY-MM-DD"},
        orderBy: [date_ASC]
      ) {
        dimensions { date }
        sum { requests pageViews bytes }
        uniq { uniques }
      }
    }
  }
}
```

**2. 国家/页面/状态码（`httpRequestsAdaptiveGroups`，仅单日）：**
```graphql
{
  viewer {
    zones(filter: {zoneTag: "ZONE_ID"}) {
      httpRequestsAdaptiveGroups(
        limit: 20,
        filter: {date_geq: "YYYY-MM-DD", date_leq: "YYYY-MM-DD"},
        orderBy: [count_DESC]
      ) {
        count
        dimensions { clientCountryName }  # 或 clientRequestPath / edgeResponseStatus
      }
    }
  }
}
```

### 踩坑记录
1. **多查询合并失败**：GraphQL 不支持在 `httpRequests1dGroups` 中混合使用不同维度的 alias 查询，需分开发送
2. **字段名错误**：`httpRequests1dGroups` 不支持 `clientCountryName`、`clientRequestPath`、`edgeResponseStatus` 等维度，只能用 `date`
3. **adaptive 1天限制**：`httpRequestsAdaptiveGroups` 在免费计划上不允许跨天查询，报错 "cannot request a time range wider than 1d"
4. **orderBy 语法差异**：`httpRequests1dGroups` 用 `sum_requests_DESC`，`httpRequestsAdaptiveGroups` 用 `count_DESC`
5. **Token 提取**：不能用 `wrangler whoami` 输出直接拼 API header，需从 toml 文件提取 `oauth_token` 字段
6. **Python SSL 问题**：macOS Python 3.14 的 SSL 证书验证可能失败，curl 更可靠

### 查询策略（推荐）
1. 用 `httpRequests1dGroups` 一次性拉取 30 天日趋势
2. 用 `httpRequestsAdaptiveGroups` + 昨天日期拉取地理/页面/状态码最后一天快照
3. 如需完整 30 天多维数据 → 需循环 30 次逐日查询（API 调用量大，按需使用）

## 报告结构模板

报告推送到 Notion 营销中心（page_id: `35895643234781ceb231e1510c77d401`）下，包含：

1. **执行摘要** — 30天总计 + 日均（请求/PV/UV/带宽）+ 趋势一句话
2. **30天日趋势表** — 日期、请求、PV、UV、带宽
3. **周趋势表** — ISO周、请求、PV、带宽、环比变化
4. **地理分布** — Top 10 国家（昨日快照）
5. **热门页面** — Top 10 路径（昨日快照）
6. **技术健康** — HTTP 状态码分布
7. **关键洞察** — 3-6 条分析结论
8. **建议行动** — 3-5 条可执行建议

## 执行清单

- [ ] 从 `~/Library/Preferences/.wrangler/config/default.toml` 读取 token
- [ ] 确认 token 未过期（检查 `expiration_time` 字段）
- [ ] 查询 `httpRequests1dGroups` 获取 30 天日趋势
- [ ] 查询 `httpRequestsAdaptiveGroups`（昨日）获取国家 + 页面 + 状态码
- [ ] Python 处理数据：计算总计/日均/周聚合/峰值
- [ ] 生成 Notion 页面（Markdown 格式，含表格）
- [ ] 更新营销中心首页链接（`notion-update-page` → `update_content`）
- [ ] 清洁临时文件

## 触发方式

- **手动**：用户说"生成网站数据报告"或"推送网站分析"
- **定时**：CronCreate 每月 1 日触发（需注意 7 天自动过期限制，届时手动续期）
