# LISHI LASER 混合气体设备网站项目

> **集团背景**：本网站由 **Euchio Machinery（济南钰峭机械有限公司）** 运营。LISHI LASER 是合作工厂品牌，Euchio 负责其海外推广与销售（非独家代理，非子公司关系）。Euchio 旗下还有自有品牌 EUCHIO（euchio.com）和独立售后平台 SAGEMRO（sagemro.com）。
>
> 跨项目统一认知框架见：`group-operating-manual.md`
> 三品牌协同策略见：`cross-project-synergy.md`
>
> **对外措辞规范**：不使用「独家代理」「exclusive distributor」等表述。LISHI 是合作推广品牌。

## 1. 项目概述

- **网站**: https://gasmixtech.com
- **品牌**: LISHI LASER / 济南欧奇欧机械有限公司 (Jinan Euchio Machinery Co., Ltd.)
- **产品**: 激光切割混气装置（Mixed Gas Device）
  - 将液氮(N₂)和液氧(O₂)按精确配比混合成 N₂/O₂ 混合气
  - 用于 12kW-60kW 光纤激光切割机辅助气体
  - 核心优势：切割速度提升 3 倍、零毛刺、氮气消耗减少 33%
- **部署平台**: Cloudflare Pages (`lishi-laser-website`)
- **部署命令**: `npx wrangler pages deploy public --project-name lishi-laser-website`

## 2. 产品核心信息

- **功率范围**: 12kW / 20kW / 30kW / 60kW
- **混气比例**: N₂/O₂ 可调（典型 95%/5% 微氧）
- **适用材料**: 碳钢、不锈钢、铝
- **竞争定位**: 对比纯氧气切割（3x 速度提升）、对比空气切割（零毛刺）、唯一支持一拖二配置
- **兼容品牌**: HAN'S, DNE, PENTA, LEAD, HSG, BODOR, KIMLA, MESSER
- **技术优势**: IGBT 智能混气技术、免维护（仅 2kWh/24h 功耗）

## 3. 目标客户群体（发达国家市场）

1. 钣金加工工厂
2. 拥有专业钣金加工设备的各行各业工厂
3. 钣金加工设备的代理商和经销商

## 4. 目标市场（按优先级）

| 优先级 | 市场 | 语言版本 | 说明 |
|--------|------|----------|------|
| P1 | 欧洲 | DE/FR/IT/ES/PT/NL/PL | 德、法、意、西、葡、荷、波 - 全部发达国家 |
| P1 | 美国 | EN (美) | 英语市场，高价值 |
| P1 | 加拿大 | EN (美) + FR | 英法双语 |
| P1 | 澳大利亚 | EN | 英语市场 |
| P1 | 新西兰 | EN | 英语市场 |
| P1 | 韩国 | KO | 已建目录 |
| P1 | 日本 | JA | 已建目录 |

> 所有目标市场均为发达国家，客户购买力强。

## 5. 联系方式（已更新）

- **邮箱**: sales@gasmixtech.com（2026-04-26 已从 sales@euchio.com 更改）
- **电话/微信**: +86 186 1558 4520
- **WhatsApp 墨西哥**: +52 557 208 0065
- **WhatsApp 泰国**: +66 961 135 966

## 6. 现有语言版本

| 语言 | 代码 | 状态 | URL |
|------|------|------|-----|
| 英语 | en | ✅ 已上线 | / |
| 西班牙语 | es | ✅ 已上线 | /es/ |
| 简体中文 | zh | ✅ 已上线 | /zh/ |
| 韩语 | ko | ✅ 已上线 | /ko/ |
| 日语 | ja | ✅ 已上线 | /ja/ |
| 葡萄牙语 | pt | ✅ 已上线 | /pt/ |
| 土耳其语 | tr | ✅ 已上线 | /tr/ |
| 波兰语 | pl | ✅ 已上线 | /pl/ |
| 意大利语 | it | ✅ 已上线 | /it/ |
| 德语 | de | ✅ 已上线 | /de/ |
| 法语 | fr | ✅ 已上线 | /fr/ |
| 荷兰语 | nl | ✅ 已上线 | /nl/ |
| 俄语 | ru | ✅ 已上线 | /ru/ |
| 越南语 | vi | ✅ 已上线 | /vi/ |
| 泰语 | th | ✅ 已上线 | /th/ |

## 6b. 项目文档结构

```
网站根目录/
├── public/                     # 网站源文件
│   ├── index.html            # 英语首页
│   ├── parameters.html       # 英语参数页
│   ├── contact.html          # 英语联系页
│   ├── _template.html        # 模板文件
│   ├── styles.css            # 样式
│   ├── script.js             # 脚本
│   ├── sitemap.xml           # 网站地图
│   ├── robots.txt            # 爬虫规则
│   ├── _headers               # Cloudflare Pages 安全响应头
│   ├── zh/ | es/ | ko/ | ja/ | pt/  # 语言版本目录
│   └── images/               # 图片资源
├── marketing/                  # 营销资产库（策略+内容+计划+研究）
│   ├── README.md              # 营销资产库总览索引
│   ├── skills/                # 方法论和能力指南
│   │   ├── linkedin-strategy.md
│   │   ├── email-marketing.md
│   │   ├── print-materials-guide.md
│   │   ├── seo-strategy.md
│   │   └── b2b-platforms.md
│   ├── content/               # 具体内容资产和模板
│   │   ├── print-collateral-plan.md
│   │   ├── cover-letter-template.md
│   │   ├── linkedin-templates.md
│   │   └── email-templates.md
│   ├── plans/                 # 执行计划和时间表
│   │   ├── youtube-channel-plan.md
│   │   └── linkedin-launch-plan.md
│   └── research/              # 市场研究和渠道分析
│       └── channel-analysis.md
├── SEO-Implementation-Roadmap.md       # SEO 实施路线图
├── SEO-Keyword-Research-16Languages.md  # 16语言关键词研究
├── SEO-Technical-Audit-Report.md      # 技术SEO审计报告
├── SEO-Content-Plan-16Languages.md    # 内容规划
├── SEO-MultiLanguage-Architecture.md  # 多语言架构设计
├── Video-SEO-MultiPlatform-Strategy.md # 视频SEO策略
└── COMPETITOR-ANALYSIS.md             # 竞品分析
```

## 7. SEO 现状评分

**技术 SEO: 95/100**

已完成:
- ✅ Title/Meta 完善
- ✅ Canonical + hreflang 标签（全部52页含16 hreflang）
- ✅ Open Graph + Twitter Card（OG图片路径已修复，27页 2026-04-29）
- ✅ JSON-LD Schema (Organization/Product/WebSite/FAQPage/VideoObject/Article/BreadcrumbList/HowTo)
- ✅ JSON-LD @type 翻译修复（de/it/fr/vi/ru/th，14文件22处，2026-04-29）
- ✅ 响应式移动端
- ✅ 图片 alt 文本
- ✅ robots.txt（8个AI爬虫白名单: GPTBot, CCBot, Claude-Web, anthropic-ai, PerplexityBot, Google-Extended, OAI-SearchBot, ClaudeBot）
- ✅ sitemap.xml（51 URLs，覆盖全部页面）
- ✅ Google Search Console 已验证（2026-04-26）
- ✅ 全部15种语言版本含 BreadcrumbList schema
- ✅ Product schema 已添加到首页
- ✅ Blog hreflang 修复：仅保留 en + x-default（6页面，2026-04-29）
- ✅ GEO 基础已部署：llms.txt + llms-full.txt（13.6KB，2026-04-29 扩展）
- ✅ ru/vi/th hreflang 子页面URL修复（90条，30文件，2026-04-29）
- ✅ LCP 优化：hero image preload + fetchpriority="high" + width/height（15页面，2026-04-29）
- ✅ _headers 安全响应头（CSP, HSTS, X-Frame-Options, etc. 2026-04-29）
- ✅ Footer 版权年份 2025→2026（48文件，2026-04-29）
- ✅ 自定义 404 页面（匹配工业暗色主题，2026-05-02）
- ✅ 隐私政策页面（GDPR 合规，2026-05-02）
- ✅ Footer LinkedIn 链接（9 英文页，2026-05-02）

## 8. 市场推广计划（4阶段）

### Phase 1（第1-4周）: 基础建设 ✅ 已完成
- ✅ 接入 Google Search Console（2026-04-26）
- ✅ 添加 FAQPage schema 到参数页（6种语言，2026-04-26）
- ✅ 添加 VideoObject schema（6种语言首页，6个视频，2026-04-26）
- ✅ 审计未使用图片（device-1~5.jpg 不存在）

### Phase 2（第5-12周）: 扩展语言
- ✅ **英文博客5篇文章已完成（2026-04-26）**
- ✅ **韩语(ko)、日语(ja)、葡萄牙语(pt) 已有完整页面（首页/参数/联系）**
- ✅ **土耳其语(tr)、波兰语(pl) 已上线**
- ✅ **意大利语(it)、德语(de)、法语(fr)、荷兰语(nl) 已上线（2026-04-28）**
- ✅ **俄语(ru)、越南语(vi)、泰语(th) 已上线（2026-04-28）**
- 目标：索引页面从9增至45+（15种语言 × 3个核心页面）

### Phase 3（第13-24周）: 规模化
- YouTube 频道运营
- 外链建设

### Phase 4（第7-12月）: 权威建设
- 技术白皮书（PDF门控内容）
- 10+ 客户案例研究
- 多语言视频字幕/配音
- 品牌词保护

## 9. 常用操作

### 部署网站
```bash
cd "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站"
npx wrangler pages deploy public --project-name lishi-laser-website
```

### 搜索文件内容
```bash
grep -rn "关键词" "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public/"
```

## 10. 设计/开发约定

- 所有 HTML 文件小写命名，连字符分隔
- 图片路径: `/images/` 目录下
- 语言版本使用子目录结构 `/[lang]/`
- 每个页面包含完整 16 语言 hreflang 标签（15种语言 + x-default）
- 阿拉伯语页面设置 `dir="rtl"`
- `.claude-portable/` 目录包含本项目的 Claude Code 配置备份（settings.json + 记忆文件），换电脑时复制到 `C:\Users\<用户名>\.claude\` 即可恢复

## 12. 换电脑工作流程

1. 在新电脑上安装 Claude Code + 坚果云
2. 坚果云同步后，项目文件自动到位
3. **一键恢复 Claude Code 环境**：
   ```powershell
   powershell -ExecutionPolicy Bypass -File .claude-portable/restore.ps1
   ```
   脚本会自动合并全局 CLAUDE.md（不覆盖已有内容）+ 恢复 settings.json + 项目记忆
4. 如需 gstack skills: 在项目根目录运行 `gstack setup`
5. 重启 Claude Code，所有配置和记忆自动加载

## 11. 联系方式

- 销售邮箱: sales@gasmixtech.com（修改于 2026-04-26）
- 电话: +86 186 1558 4520 (微信)
- WhatsApp: +52 557 208 0065 (墨西哥), +66 961 135 966 (泰国)

## 12. 营销资产库

位于 `marketing/` 目录，参见 `marketing/README.md` 获取完整索引。

**架构**: Skills（方法论）→ Content（内容模板）→ Plans（执行计划）→ Research（市场研究）

**2026-04-29 已确立的营销方向**:
1. **LinkedIn** — P0 首选渠道。双轨策略：公司页面（品牌）+ 个人 Profile（关系）
   - 公司页面: https://www.linkedin.com/company/euchio/
   - 个人 Profile: https://www.linkedin.com/in/josephji/
2. **ThomasNet + DirectIndustry** — P1 工业 B2B 平台。被动获客，待注册
3. **Email 营销** — P1 直接触达。配合 LinkedIn + 展会 + 平台询盘
4. **印刷品邮寄** — P0 线下推广。5 件物料方案已完成，等待产品照片 + logo 矢量文件

**印刷品阻断项（2026-04-29，2026-05-06 搁置）**:
- [x] 确认设备尺寸重量 — 以 800×350×1100mm/90kg 为准（2026-05-06 已修正 llms-full.txt）
- [ ] 获取 logo 矢量文件（当前仅有 696×679 PNG，印刷需要 AI/EPS/SVG）— 搁置
- [ ] 拍摄产品照片（白底设备照 + 工厂照 + 切割效果照 + 一拖二照）— 暂无更多图片，搁置

> 印刷资料设计整体搁置，待后续条件具备再启动。

**YouTube**: 方案已完成（`marketing/plans/youtube-channel-plan.md`），等待视频制作资源后启动。

**2026-04-30 更新**:
- Footer 全球更新：品牌定位从"授权代理"改为"LISHI LASER 是 Euchio 旗下混合气体技术专用品牌"（全部15语言）
- LinkedIn 冷启动执行方案已完成：`marketing/plans/linkedin-launch-plan.md`（个人Profile为主 ~5000 followers，含前10篇完整文案已改写个人口吻）

**待办优先级**（2026-05-02）:
1. 个人 Profile 优化 + 开始每日连接（按 linkedin-launch-plan.md Step 2 + Step 5）
2. LinkedIn 公司页面装修（已存在 linkedin.com/company/euchio，按 Step 1 完善）
3. GSC 结构化数据验证（Rich Results Test 手动验证）
4. 印刷品照片拍摄 + logo 矢量获取
5. ThomasNet / DirectIndustry 注册