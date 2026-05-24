# Google Ads 推广方案 — LISHI LASER 混合气体设备

> 创建日期：2026-05-22
> 状态：方案已就绪，待执行
> 前置条件：需安装 Google Tag Manager（当前仅有 GA4）

---

## 一、渠道适配性判断

| 优势 | 劣势 |
|------|------|
| 捕获高意向搜索（正在找解决方案的人） | 搜索量小——"laser gas mixer" 月搜索量可能只有几百 |
| 精准投放，按点击付费 | B2B 工业品关键词 CPC 可能 $2-8/次 |
| 15 种语言落地页已就绪，可直接用 | 成交周期长（几周到几个月），不是点广告就下单 |
| 可以按国家/地区精准投放 | 需要持续优化，不是设完就不管 |

**结论**：适合作为获客渠道之一，定位为"搜索流量的付费加速器"。

---

## 二、广告类型：仅搜索广告（Search Ads）

- ✅ 搜索广告（Search）— 用户搜关键词时出现在结果顶部
- ❌ 展示广告（Display）— 太泛，浪费钱
- ❌ 视频广告（Video）— B2B 工业品不适合
- ❌ 购物广告（Shopping）— 非标设备不适用
- ❌ Performance Max — 仅在搜索广告稳定后可测试

---

## 三、关键词策略

### P0 — 高意向（贵但转化好）
- `laser gas mixer supplier`
- `mixed gas device for laser cutting`
- `N2 O2 gas mixing system`
- `laser assist gas mixer manufacturer`
- `buy gas mixer for fiber laser`
- `industrial laser gas mixing equipment`

### P1 — 问题型（中等意向，教育阶段）
- `how to cut carbon steel faster laser`
- `eliminate burrs laser cutting`
- `laser cutting gas comparison`
- `reduce nitrogen consumption laser cutting`
- `laser cutting speed improvement`
- `O2 vs N2 laser cutting`
- `air compressor vs gas mixer laser`

### P2 — 品牌/竞品型
- `LISHI LASER`
- `Bodor laser gas system`
- `Penta laser assist gas`
- `Han's laser gas mixer`
- `HSG laser gas system`
- `mixed gas cutting parameters`

### 否定关键词（必须添加，避免浪费）
- `diy` `homemade` `used` `second hand` `hobby` `small`
- `plasma` `waterjet` `CO2 laser`（不是光纤激光客户）
- `job` `salary` `career` `internship` `free`

---

## 四、广告结构

```
Google Ads 账号 (sales@gasmixtech.com)
│
├── Campaign: US-Canada (English) — 预算 40%
│   ├── Ad Group: High Intent
│   ├── Ad Group: Problem Awareness
│   └── Ad Group: Brand/Competitor
│
├── Campaign: Europe (DE+FR+IT+ES+PT+NL+PL) — 预算 35%
│   ├── Ad Group: High Intent (EN)
│   ├── Ad Group: DE-specific
│   └── Ad Group: FR-specific
│
├── Campaign: Asia-Pacific (KR+JP+AU+TH+VI) — 预算 15%
│   ├── Ad Group: High Intent (EN)
│   ├── Ad Group: KR-specific
│   └── Ad Group: JP-specific
│
└── Campaign: Other (TR+RU) — 预算 10%
    ├── Ad Group: High Intent (EN)
    └── Ad Group: TR-specific
```

---

## 五、落地页映射

| 搜索意图 | 落地页 |
|----------|--------|
| 了解产品 / 询价 | `gasmixtech.com/` |
| 查参数 / 对比型号 | `gasmixtech.com/parameters.html` |
| 对比方案 | `gasmixtech.com/blog/mixed-gas-vs-oxygen-comparison.html` |
| 省钱 / 省氮气 | `gasmixtech.com/blog/mixed-gas-nitrogen-savings.html` |
| 选型指南 | `gasmixtech.com/blog/how-to-choose-gas-mixer.html` |
| 联系 / 询盘 | `gasmixtech.com/contact.html` |

**核心原则**：广告文案关键词 → 落地页内容 → 用户搜索意图，三者必须一致。

---

## 六、预算规划

### 测试期（前 2-4 周）
- 每天 $20-30，总计 $500-800/月
- 目标：收集数据，验证关键词和国家效果
- 只投 P0 关键词，3-5 个国家
- 使用 Maximize Clicks 出价策略

### 优化期（2-4 周后）
- 每天 $30-50
- 根据数据砍掉无效关键词和国家
- 预算集中到有转化的组合
- 切换到 Maximize Conversions 出价（需≥15次转化/月）

### 参考：工业 B2B 获客成本
- CPL（每线索成本）：$30-80
- 如果单台设备利润数千美元，这个获客成本完全可接受
- 预期转化率：点击→询盘 2-5%（取决于落地页质量）

---

## 七、转化追踪设置

### 需追踪的转化事件
1. **提交联系表单**（contact.html） — 主要转化
2. **WhatsApp 点击** — 次要转化
3. **电话点击**（tel: 链接） — 次要转化
4. **ROI 计算器留资**（首页 lead capture 表单） — 主要转化

### 技术实现路径
```
Google Tag Manager (GTM)
  ├── GA4 Configuration Tag
  ├── Google Ads Conversion Linker
  ├── Form Submit Trigger → Google Ads Conversion
  ├── WhatsApp Click Trigger → Google Ads Conversion
  └── Phone Click Trigger → Google Ads Conversion
```

### 当前状态
- ✅ GA4 已安装（Measurement ID: G-5SY7DT95CJ）
- ❌ GTM 未安装 — 投 Google Ads 前必须安装
- ❌ Google Ads 转化追踪未配置

---

## 八、执行步骤

1. ☐ 安装 Google Tag Manager（GTM）
2. ☐ 在 GTM 中配置 GA4 + Google Ads 转化追踪
3. ☐ 注册 Google Ads 账号（用 sales@gasmixtech.com）
4. ☐ 设置转化事件（表单提交、WhatsApp 点击、电话点击）
5. ☐ 创建搜索广告系列（按国家/语言分组）
6. ☐ 上传关键词列表 + 否定关键词
7. ☐ 撰写广告文案（每个广告组 3 条 Responsive Search Ads）
8. ☐ 设置预算 $20-30/天，启动测试期
9. ☐ 2 周后复盘数据，优化关键词和国家分配

---

## 九、与 LinkedIn 的配合

| | Google Ads | LinkedIn |
|------|-----------|----------|
| 获客方式 | 等客户搜（被动） | 主动触达（主动） |
| 客户状态 | 已在找解决方案 | 不一定有即时需求 |
| 适合阶段 | 随时可投 | 配合内容长期运营 |
| 预算建议 | $500-800/月测试 | 免费内容为主 |

**协同策略**：LinkedIn 继续每周 3 帖的内容节奏，Google Ads 作为补充捕获搜索流量。两者不冲突，预算分开管理。

---

## 十、广告文案模板

### Responsive Search Ad 示例（P0 高意向）

**Headlines（最多 15 个，至少 3 个）**：
1. LISHI LASER Mixed Gas Device
2. 3× Faster Laser Cutting Speed
3. Burr-Free Carbon Steel Cutting
4. N₂/O₂ Gas Mixer for 3kW-60kW
5. Cut Your Gas Cost by 33%
6. Industrial Laser Gas Mixing System
7. No More Grinding After Cutting
8. One Device → Two Lasers
9. Factory Direct Pricing
10. Get Custom Cutting Parameters

**Descriptions（最多 4 个，至少 2 个）**：
1. Precision N₂/O₂ mixed gas device for fiber laser cutting. 3× faster than O₂, zero burrs, 33% less gas. Compatible with HANS, BODOR, PENTA & more. Get a quote today.
2. Eliminate grinding. Boost throughput 180%. Our gas mixer delivers weld-ready edges straight off the laser. 500+ installations worldwide. Contact us for parameters.
3. Mixed gas vs O₂: see the real speed comparison for your laser power. We'll send verified cutting parameters within 24 hours. WhatsApp support available.
4. One gas mixer, two lasers. Cut capital cost by 50%. 2 kWh/day power consumption, zero maintenance. Talk to our engineers today.

---

## 十一、备注

- 本文档为初始方案，执行过程中根据数据持续优化
- 所有广告投放预算以美元计，用信用卡支付
- 建议使用 Google Ads Editor 桌面软件批量管理关键词和广告
- 每月至少一次数据复盘，调整关键词出价和预算分配
