---
name: GA MCP Setup
description: Google Analytics MCP server配置，支持euchio和gasmixtech两个网站的过滤查询
type: reference
originSessionId: 6f6529a9-4fd9-4d1a-8b30-7aee1948f197
---
# Google Analytics MCP 配置

**MCP server 位置**: `C:\Users\Admin\.ga-mcp\server.py`
**配置文件**: `C:\Users\Admin\.claude.json` (mcpServers.google-analytics)

## GA4 Property

- Property ID: `420888879`
- 同一 property 下同时追踪 euchio.com 和 gasmixtech.com
- 通过 hostname 维度过滤区分两个网站

## 使用方式

查询 gasmixtech 数据时加 `"site": "gasmixtech"`：
```
mcp__google-analytics__get_analytics_report
  site: gasmixtech
  start_date: 30daysAgo
  end_date: today
  metrics: ["sessions","activeUsers","screenPageViews","bounceRate"]
```

查询 euchio 数据时加 `"site": "euchio"`，不填 site 则查全部。

## 可用的 dimensions
- pagePath, hostname, country, deviceCategory, date, sessionSource, sessionMedium, etc.

## 可用的 metrics
- sessions, activeUsers, screenPageViews, bounceRate, averageSessionDuration, conversions, eventCount, etc.

## 修改 server.py 后
需要重启 Claude Code 才能生效（MCP server 是 stdio 进程，Claude Code 启动时加载）。
