---
name: Project — LISHI LASER Website
description: Static HTML/CSS site for LISHI LASER mixed gas device, deployed on Cloudflare Pages at gasmixtech.com
type: project
originSessionId: 77b1b736-19f5-4f9c-b070-abebefd2107a
---
# Project: LISHI LASER Website

**Domain:** gasmixtech.com
**Deployment:** Cloudflare Pages (`npx wrangler pages deploy public --project-name lishi-laser-website`)
**Project name on Cloudflare:** `lishi-laser-website`
**Latest deploy preview:** https://b06daff7.lishi-laser-website.pages.dev (2026-04-21)

## What
Static HTML/CSS/JS product website for LISHI LASER Mixed Gas Device — B2B industrial product for high-power laser cutting (12KW–60KW). Jinan Euchio Machinery Co., Ltd. is the overseas market agent.

## Current State (2026-04-23)

### Languages — 6 total
| Lang | Path | Status |
|------|------|--------|
| EN | `/` | Complete |
| ZH | `/zh/` | Complete — synced from EN |
| ES | `/es/` | Complete — synced from EN |
| KO | `/ko/` | Complete — synced from EN |
| JA | `/ja/` | Complete — synced from EN |
| PT | `/pt/` | Complete — Global Network added, CSS in styles.css, JS in script.js |

**Planned later:** TR, VI

### What was synced 2026-04-23 (EN → ZH/ES/KO/JA/PT)
1. **New Global Network section** — animated SVG globe, pulsing location dots, animated arcs, IntersectionObserver stat counters, continent badges, gradient CTA block
2. **ROI Calculator fixes** — Utilization (Beam-On %) slider added, monthly N₂ cost default raised to $2000 USD, realism disclaimer added, utilization factor in annual profit formula
3. **script.js cleanup** — dead `animateCounters()` function removed

### Pages per language
- `index.html` — Homepage with hero, how it works, advantages, ROI calculator, video samples, parameters overview, Global Network, CTA
- `parameters.html` — Detailed cutting speed tables
- `contact.html` — Contact info + Web3Forms form

### Contact
- Web3Forms access key: `2352c2d3-9578-4f1e-aa56-611e2ad355d1`
- Email: sales@euchio.com
- WhatsApp Mexico: +52 557 208 0065
- WhatsApp Thailand: +66 961 135 966
- WeChat/Phone: +86 186 1558 4520

### Known Quirks
- Large inline `<style>` and `<script>` blocks in index.html — calculator + global-presence CSS/JS lives inline in each language version (EN, ZH, ES, KO, JA). PT uses external styles.css and script.js instead.
- gstack `browse` tool has a Windows build issue (missing server-node.mjs), so visual QA must be done manually in a real browser
- `图片1_1.png` and `httpsyoutu.bez3vfXdCFPlk...md` still exist in project root (not cleaned up yet)

## 2026-04-21 Session Changes (EN only)

### ROI Calculator Fixes (index.html)
- Removed undefined `comparisonMode` reference (was throwing ReferenceError every calc)
- Removed dead `updateAirComparison` call
- Removed dead `workDaysSlider` reference
- Added **Utilization (Beam-On %) slider** — default 60%, range 20–100%
- All currency labels now explicitly say "USD"
- Raised default monthly N₂ cost from $500 → $2000
- Added realism disclaimer under annual profit number

### Global Network section replaces old Reference Customers
- Completely new visual-first section: animated SVG globe, pulsing red/amber location dots, 3 animated dashed connection arcs
- IntersectionObserver-triggered number counters (20+ Countries / 4 Continents / 12–60kW / 24/7)
- Gradient heading "Where High-Power Lasers Cut. Our Gas Flows."
- Continent badges: ASIA / EUROPE / AMERICAS / AFRICA + dashed "OCEANIA 2026"
- Gradient CTA block
- **No specific agent/company names**
