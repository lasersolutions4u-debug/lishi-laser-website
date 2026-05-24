# LISHI LASER 混合气体设备网站项目

> **集团背景**：本网站由 **Euchio Machinery（济南钰峭机械有限公司）** 运营。LISHI LASER 是合作工厂品牌，Euchio 负责其海外推广与销售（**非独家代理，非子公司**）。Euchio 旗下另有自有品牌 EUCHIO（euchio.com）和独立售后平台 SAGEMRO（sagemro.com）。
>
> 跨项目认知见 `group-operating-manual.md`，三品牌协同见 `cross-project-synergy.md`。
>
> **对外措辞规范**：禁用「独家代理 / exclusive distributor」等表述，统一表述为"合作推广品牌"或"Euchio 旗下混合气体技术专用品牌"。

## 1. 项目基本信息

- **网站**：https://gasmixtech.com
- **运营主体**：济南欧奇欧机械有限公司 (Jinan Euchio Machinery Co., Ltd.)
- **产品**：激光切割混气装置（N₂/O₂ 精确配比混合气，3kW–60kW 光纤激光机辅助气体）
- **核心卖点**：切割速度 3 倍提升、零毛刺、氮气消耗减少 33%
- **部署**：Cloudflare Pages，命令：`npx wrangler pages deploy public --project-name lishi-laser-website`

## 2. 产品核心信息

- **功率覆盖**：3 / 6 / 12 / 20 / 30 / 60 kW
- **混气比例**：N₂/O₂ 可调（典型 95%/5% 微氧）
- **适用材料**：碳钢、不锈钢、铝
- **竞争定位**：vs 纯氧气切割（3x 速度）、vs 空气切割（零毛刺）、唯一支持一拖二
- **兼容品牌**：HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, MESSER
- **技术特征**：IGBT 智能混气、免维护（功耗仅 2kWh/24h）
- **设备规格**：800×350×1100mm，90kg

## 3. 目标客户与市场

**客户类型**：钣金加工厂 / 含钣金工艺的各行业工厂 / 钣金设备代理商和经销商

**目标市场（全部 P1，发达国家）**：欧洲（DE/FR/IT/ES/PT/NL/PL）、美国、加拿大（EN+FR）、澳洲、新西兰、韩国、日本

## 4. 联系方式

- **邮箱**：sales@gasmixtech.com（2026-04-26 由 sales@euchio.com 切换）
- **电话/微信**：+86 186 1558 4520
- **WhatsApp**：+52 557 208 0065（墨西哥）、+66 961 135 966（泰国）

## 5. 网站语言版本（15 种全部上线）

`en` `es` `zh` `ko` `ja` `pt` `tr` `pl` `it` `de` `fr` `nl` `ru` `vi` `th`

每个语言均有完整三页：首页 / 参数 / 联系，路径为 `/[lang]/`（英语为根路径）。

## 6. 项目结构

public/                   # 网站源文件（HTML + styles.css + script.js + images/）
 ├── index.html / parameters.html / contact.html  # 英语
 ├── _template.html / sitemap.xml / robots.txt / _headers
 └── [lang]/               # 15 种语言子目录
 marketing/                # 营销资产库（详见 marketing/README.md）
 ├── skills/   ├── content/   ├── plans/   └── research/
 SEO-*.md                  # SEO 路线图、关键词研究、技术审计、内容规划、多语言架构、视频策略
 COMPETITOR-ANALYSIS.md    # 竞品分析
 .claude-portable/         # Claude Code 配置备份（换电脑用）

## 7. SEO 现状（技术 SEO 评分 95/100）

**已完成基线**：Title/Meta、Canonical + 16 hreflang（全部 52 页）、Open Graph、JSON-LD（Organization/Product/WebSite/FAQPage/VideoObject/Article/BreadcrumbList/HowTo）、响应式、图片 alt、robots.txt（含 8 个 AI 爬虫白名单：GPTBot/CCBot/Claude-Web/anthropic-ai/PerplexityBot/Google-Extended/OAI-SearchBot/ClaudeBot）、sitemap.xml（51 URLs）、Google Search Console 已验证、LCP 优化、_headers 安全响应头、自定义 404、隐私政策（GDPR）、llms.txt + llms-full.txt（GEO 基础）。

**待办**：GSC 结构化数据验证（Rich Results Test 手动）。

## 8. 市场推广现状

**已完成**：Phase 1 基础建设（GSC、FAQPage/VideoObject schema）+ Phase 2 语言扩展（15 语言 × 3 页 + 5 篇英文博客）。

**当前阶段（Phase 3 规模化）已确立的渠道方向**（2026-04-29）：

1. **LinkedIn — P0 首选**。双轨：公司页面（品牌）+ 个人 Profile（关系）
   - 公司：https://www.linkedin.com/company/euchio/
   - 个人：https://www.linkedin.com/in/josephji/
   - 冷启动方案见 `marketing/plans/linkedin-launch-plan.md`（含前 10 篇文案）
2. **ThomasNet + DirectIndustry — P1**，工业 B2B 平台被动获客，待注册
3. **Email 营销 — P1**，配合 LinkedIn / 展会 / 平台询盘
4. **印刷品邮寄 — 已搁置**，等待产品照片 + logo 矢量文件
5. **YouTube** — 方案已就绪（`marketing/plans/youtube-channel-plan.md`），待视频制作资源

**Footer 品牌定位（全 15 语言）**：「LISHI LASER 是 Euchio 旗下混合气体技术专用品牌」

**当前待办**（2026-05-21）：暂无待办。

**已完成/搁置**：
- ✅ LinkedIn 个人 Profile + 公司页面
- ✅ GSC 结构化数据验证
- ✅ ThomasNet 注册（需缴费认证）
- ✅ DirectIndustry 注册（需缴费认证）
- ❌ 印刷品 — 搁置（缺产品照片 + logo 矢量）
- ❌ YouTube — 搁置（缺视频制作资源）

## 9. 常用操作

```bash
# 部署
cd "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站"
npx wrangler pages deploy public --project-name lishi-laser-website
```

项目根路径在坚果云同步目录中，跨电脑路径一致。

## 10. 开发约定

- HTML 文件小写命名 + 连字符分隔
- 图片统一放 `/images/`
- 语言版本统一 `/[lang]/` 子目录结构
- 每页含完整 16 hreflang（15 语言 + x-default）
- 阿拉伯语页面（如未来添加）需 `dir="rtl"`

## 11. 换电脑工作流程

1. 装 Claude Code + 坚果云，等待项目同步
2. 一键恢复 Claude Code 环境：

powershell -ExecutionPolicy Bypass -File .claude-portable/restore.ps1

自动合并全局 CLAUDE.md（不覆盖）+ 恢复 settings.json + 项目记忆

3. 如需 gstack skills：项目根目录运行 `gstack setup`

4. 重启 Claude Code

