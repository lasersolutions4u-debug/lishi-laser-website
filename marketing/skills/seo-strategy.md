# SEO 策略参考

> 状态: 技术 SEO 已完成（95/100），内容 SEO 待推进
> 相关: 网站 CLAUDE.md 第 7 节有详细 SEO 现状
> 关键词研究: 2026-05-15 通过 Ubersuggest MCP 完成，数据源见文末

## 已完成

- ✅ 15 种语言 × 3 核心页面 + 6 博客 = 51 URL
- ✅ Title/Meta/Canonical/hreflang 全部完善
- ✅ JSON-LD Schema（8 种 @type）
- ✅ sitemap.xml + robots.txt
- ✅ _headers 安全响应头（CSP, HSTS, etc.）
- ✅ Open Graph + Twitter Card
- ✅ LCP 优化（hero image preload）
- ✅ GEO 基础（llms.txt + llms-full.txt）
- ✅ Google Search Console 已验证
- ✅ 15 种语言全部含 BreadcrumbList schema
- ✅ Ubersuggest MCP 已接入（全局安装，OAuth 认证）
- ✅ gasmixtech.com 项目已创建（US 市场，15 关键词追踪）

## 待推进

- [ ] Google Search Console 索引验证（目标 45+ 页面已索引）
- [ ] 外链建设（LinkedIn 帖子链接、行业目录、合作伙伴网站）
- [ ] 博客文章：基于关键词研究结果撰写
- [ ] 客户案例页面（真实案例 + 数据）
- [ ] 技术白皮书 PDF（门控下载，收集邮件）
- [ ] 多语言博客（至少德语/西班牙语/法语）

---

## 关键词研究（2026-05-15 Ubersuggest）

> 数据范围: US 市场 (locId 2840, en)
> 工具: Ubersuggest MCP (ubersuggest-mcp.neilpatelapi.com)
> 账号: lasersolutions4u@gmail.com (tier0 免费版)
> 追踪项目 ID: 86a1b7883897c42db80f2f3cfa769b4fd4874de5828a583a61fa7110b92c1362

### 核心发现：内容空白

SERP 分析显示，所有排名内容围绕氮气发生器或"选什么气体"，**没有任何内容涉及 N2/O2 混合气体技术**。这是建立内容权威的机会窗口。

### 关键词分层（US 英文）

**🥇 高优先（有搜索量 + 低难度）**

| 关键词 | 月搜索量 | SEO 难度 | CPC |
|--------|---------|----------|-----|
| nitrogen gas for laser cutting | 140 | SD 9 | $4.02 |
| nitrogen laser cutting | 140 | SD 17 | $4.02 |
| assist gas laser cutting | 20 | SD 5 | $0 |
| laser cutting assist gas | 20 | SD 5 | $0 |

**🥈 中优先（有量但低难度）**

| 关键词 | 月搜索量 | SEO 难度 |
|--------|---------|----------|
| laser cutting gas | 10 | SD 15 |
| laser assist gas | 10 | SD 13 |
| fiber laser cutting gas | 10 | SD 14 |
| gas used in laser cutting | 10 | SD 5 |
| laser cutter gas | 10 | SD 15 |
| mixed gas laser | 10 | SD 13 |

**🥉 长尾/防御**

| 关键词 | 月搜索量 | SEO 难度 |
|--------|---------|----------|
| laser cutting gas used | 10 | SD 36 |
| laser cutting with compressed air | 10 | SD 31 |
| fiber laser cutting with compressed air | 10 | SD 24 |

### SERP 竞争格局（top 排名域名）

| 域名 | DA | 类型 |
|------|-----|------|
| atlascopco.com | 61 | 工业气体设备（氮气发生器） |
| thefabricator.com | 56 | 行业媒体 |
| practicalmachinist.com | 56 | 行业论坛 |
| generon.com | 35 | 氮气发生器 |
| onsitegas.com | 32 | 氮气现场制气 |
| bodor.com | 32 | 激光切割机制造商 |
| pneumatech.com | 30 | 压缩空气/气体处理 |
| novair-usa.com | 27 | 氮气系统 |
| accurl.com | 27 | 激光切割机制造商 |
| nigen.com | 25 | 氮气发生器 |

> 核心洞察: 排名靠前的域名多为氮气发生器厂商（Generon, Atlas Copco, Nigen 等），而非直接竞品。混合气体设备品类在 SERP 中几乎无竞争。

### 欧洲市场概况

| 市场 | 关键词 | 月搜索量 | SEO 难度 |
|------|--------|---------|----------|
| 德国 | laserschneiden gas | 10 | SD 28 |
| 法国 | decoupe laser gaz | 0 | SD 12 |
| 意大利 | taglio laser gas | 0 | SD 12 |

> 欧洲非英语关键词体量极小，策略：英文内容为主 + hreflang 多语言页面覆盖。

### Ubersuggest 追踪关键词（15/25 已用）

```
laser cutting gas mixer, nitrogen generator for laser cutting,
laser assist gas, fiber laser cutting gas, n2 o2 gas mixer,
nitrogen laser cutting, nitrogen gas for laser cutting,
assist gas laser cutting, laser cutting assist gas,
laser cutting gas, gas used in laser cutting,
laser cutter gas, laser cutting gas used,
mixed gas laser, laser gas mixer system
```

---

## SEO 内容策略（更新版）

### 博客主题池（基于关键词研究排序）

1. **N2/O2 Mixed Gas vs Pure Nitrogen: Which Is Better for Laser Cutting?**
   - 目标词: nitrogen gas for laser cutting (vol 140, SD 9)
   - 角度: 对比混合气体 vs 纯氮气，自然引出 gasmixtech 产品
   
2. **Complete Guide to Laser Cutting Assist Gases: O2, N2, Air, and Mixed Gas**
   - 目标词: assist gas laser cutting (vol 20, SD 5), gas used in laser cutting (vol 10, SD 5)
   - 角度: 教育型内容，建立品类权威

3. **How Mixed Gas Technology Cuts Nitrogen Consumption by 33%**
   - 目标词: nitrogen laser cutting (vol 140, SD 17)
   - 角度: 成本分析，直击痛点（氮气成本高）

4. **3X Faster Laser Cutting: Mixed Gas Real-World Results**
   - 目标词: laser cutting gas (vol 10, SD 15)
   - 角度: 案例驱动，用数据说话

5. **Why Your Fiber Laser Needs Mixed Gas (Not Just Nitrogen)**
   - 目标词: fiber laser cutting gas (vol 10, SD 14)
   - 角度: 针对光纤激光用户的升级说服

### 关键词策略（更新版）
- 核心: nitrogen gas for laser cutting (140), assist gas laser cutting (20)
- 长尾: gas used in laser cutting (10), mixed gas laser (10), laser gas mixer system (10)
- 多语言: Laserschneidgas (DE, vol 10), 法/意/西搜索量极低，用英文主站 + hreflang 覆盖

### 竞争策略
- 现有排名者多为氮气发生器厂商，非混合气体直接竞品
- 差异化定位：混合气体 ≠ 氮气发生器，是更优的替代方案
- 内容角度：不要和氮气发生器比价格，要比切割效果和成本节省

---

## 数据来源

- Ubersuggest MCP (ubersuggest-mcp.neilpatelapi.com)
- 认证: OAuth 2.0 PKCE, 账号 lasersolutions4u@gmail.com
- 研究日期: 2026-05-15
- Token 有效期: 10 天，过期需重新认证
