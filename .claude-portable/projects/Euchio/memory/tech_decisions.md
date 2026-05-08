---
name: Technical Decisions Log
description: Key technical choices made during development
type: project
---

## Deployment
- **Cloudflare Pages** via wrangler CLI, no Git Provider
- Had to delete and recreate project to disconnect GitHub override
- Deploy command: `npx wrangler pages deploy public --project-name lishi-laser-website`

## Forms
- Migrated from Formspree (broken, "Form Not Found") to **Web3Forms**
- Access key: `2352c2d3-9578-4f1e-aa56-611e2ad355d1`
- Success state via redirect to `#success` anchor

## Issues Resolved
- Formspree endpoint invalid → migrated to Web3Forms
- GitHub overriding CLI deployments → deleted/recreated Cloudflare project without Git
- Blue color not updating → was Git Provider issue, not CSS
- btn-secondary invisible on light backgrounds → context-aware styling (dark text on light, white on dark)
