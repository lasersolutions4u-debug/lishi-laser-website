# GasMixTech Multilingual Core Sales Path Design

**Date:** 2026-09-10  
**Status:** Approved for implementation planning  
**Production site:** https://gasmixtech.com

## 1. Objective

Create a complete, internally consistent sales journey in English plus six priority languages without retaining the current mixture of new pages, legacy LISHI content, missing product translations, and unsupported language routes.

The completed release must let a visitor select a supported language, remain in that language from product discovery through inquiry submission, and switch languages while staying on the equivalent page.

## 2. Supported Languages

The core sales path will support these seven languages:

| Code | Language |
|---|---|
| `en` | English |
| `zh` | Simplified Chinese |
| `es` | Spanish |
| `pt` | Portuguese |
| `ja` | Japanese |
| `ko` | Korean |
| `pl` | Polish |

English is the content and product-fact source of truth. The six translations must use professional industrial B2B language rather than literal consumer-oriented wording.

## 3. Core Page Scope

Each supported language receives the same seven-page sales path:

1. Homepage
2. About
3. Contact and inquiry form
4. PSA nitrogen generation system
5. Integrated gas mixing cabinet
6. MSPV2-4000 proportional valve
7. Mixed-gas controller comparison

This produces 42 non-English pages and 49 core pages including English.

### English routes

- `/`
- `/about`
- `/contact`
- `/products/psa-nitrogen-generation-system`
- `/products/integrated-gas-mixing-cabinet`
- `/products/mspv2-4000-proportional-valve`
- `/products/mixed-gas-control-comparison`

### Localized route pattern

- `/{lang}/`
- `/{lang}/about`
- `/{lang}/contact`
- `/{lang}/products/psa-nitrogen-generation-system`
- `/{lang}/products/integrated-gas-mixing-cabinet`
- `/{lang}/products/mspv2-4000-proportional-valve`
- `/{lang}/products/mixed-gas-control-comparison`

The English route slugs remain unchanged in localized URLs. This keeps route mapping deterministic and avoids maintaining translated slug aliases.

## 4. Out of Scope

The following pages will not be translated in this phase:

- ROI
- Parameters
- Payment
- Privacy
- Compatibility
- 404
- Blog articles

Existing localized versions of these pages in the six supported language directories must redirect to their current English equivalents until a later translation phase. They must not continue serving legacy brand or product content.

No product specifications, commercial terms, email infrastructure, Cloudflare Email Sending configuration, or inquiry backend behavior will be changed in this phase.

## 5. Content Rules

### 5.1 Source of truth

The approved English production pages define:

- product relationships;
- technical facts and units;
- business role and company identity;
- CTA intent;
- navigation hierarchy;
- form fields and options.

Translation must not introduce, remove, or reinterpret product claims.

### 5.2 Terminology

Each language must use consistent terminology for:

- PSA nitrogen generation;
- laser cutting assist gas;
- nitrogen and oxygen mixing;
- mixing ratio;
- inlet and outlet pressure;
- flow rate;
- gas source;
- integrated cabinet;
- proportional valve;
- system integration and retrofit.

Product model names, the company name, URLs, measurement units, and confirmed numeric data remain unchanged.

### 5.3 Claims and brand cleanup

Generated pages must not contain:

- legacy LISHI LASER branding;
- unsupported installation counts;
- unsupported certification, delivery-time, warranty, or exclusivity claims;
- absolute marketing claims not present in the approved English source;
- mistranslations that imply the cabinet and proportional valve are installed in series.

The integrated cabinet and MSPV2-4000 must remain clearly positioned as alternative products with the same core mixed-gas control function.

## 6. Generation Architecture

Use deterministic static generation based on shared templates and language data.

### 6.1 Templates

The seven core page types share the approved English structure. Common site elements are represented once:

- header and navigation;
- product menu;
- language switcher;
- footer;
- CTA components;
- inquiry form structure;
- SEO metadata structure.

Page-specific templates cover the homepage, About, Contact, the three product pages, and the comparison page.

### 6.2 Translation data

Translation data is organized by language and page namespace. Each supported language contains:

- shared navigation and footer strings;
- page title and meta description;
- headings and body content;
- CTA labels;
- product-card content;
- inquiry form labels, options, validation messages, and success messages;
- localized structured-data descriptions.

The existing `public/build-i18n.js` workflow should be extended or reorganized into one deterministic core-page build command. The implementation must not require manually editing 42 generated HTML files.

### 6.3 Build failure rules

The build must fail before output is accepted when it finds:

- a missing required translation key;
- an unresolved template placeholder;
- an unsupported language in the core language menu;
- a broken same-site link;
- a legacy LISHI brand string;
- a localized core page pointing to an English core product page;
- malformed canonical or `hreflang` data.

## 7. Navigation and Language Switching

All seven languages use the same navigation structure and page hierarchy.

The language switcher must map the current route to its equivalent route. Examples:

- `/es/products/mspv2-4000-proportional-valve` switched to Japanese becomes `/ja/products/mspv2-4000-proportional-valve`.
- `/zh/contact` switched to English becomes `/contact`.
- `/products/integrated-gas-mixing-cabinet` switched to Polish becomes `/pl/products/integrated-gas-mixing-cabinet`.

The switcher must list only EN, ZH, ES, PT, JA, KO, and PL during this phase. It must not send a visitor to a missing page or reset a visitor to the homepage when an equivalent route exists.

No automatic redirect based on browser language will be added.

## 8. Unsupported and Legacy Language Handling

The following languages are not supported in the new core journey in this phase:

- German (`de`)
- French (`fr`)
- Italian (`it`)
- Dutch (`nl`)
- Turkish (`tr`)
- Russian (`ru`)
- Vietnamese (`vi`)
- Thai (`th`)

Their legacy routes must use permanent redirects to the equivalent English route. When no equivalent English route exists, the redirect target is the English homepage.

These eight languages must be removed from:

- visible language menus;
- core-page `hreflang` groups;
- the current core-page sitemap set;
- documentation that claims all 15 languages are fully available.

Redirect rules must be explicit and tested. They must not form redirect loops or interfere with the seven supported languages.

## 9. SEO Requirements

Every core page must include:

- a self-referencing canonical URL;
- reciprocal `hreflang` entries for EN, ZH, ES, PT, JA, KO, and PL;
- an `x-default` entry pointing to the English equivalent;
- the correct HTML `lang` attribute;
- a localized title and meta description;
- localized visible headings and descriptive content;
- localized descriptive text in relevant structured data while preserving factual identifiers and company data.

The sitemap must include all 49 core URLs and the correct language alternates. Unsupported or redirected language URLs must not be presented as indexable localized alternatives.

## 10. Inquiry Form

The Contact page must localize:

- the three-step headings;
- field labels;
- select options;
- consent text;
- validation messages;
- review labels;
- submitting, success, and failure states.

The form continues to submit to the existing `/api/inquiry` endpoint and the existing Cloudflare service binding. The production recipient remains `sales@gasmixtech.com`.

The honeypot, validation, rate limiting, consent requirement, and email-sending workflow must remain functionally unchanged.

## 11. Validation

### 11.1 Automated checks

Automated validation must cover:

- the full 7-language by 7-page route matrix;
- expected page count;
- unique and localized titles and descriptions;
- HTML `lang` values;
- self-referencing canonicals;
- reciprocal `hreflang` links and `x-default`;
- same-page language-switch mappings;
- product-card and CTA targets;
- absence of unresolved placeholders;
- absence of legacy brand terms;
- supported and unsupported language redirects;
- no redirect loops;
- localized form labels, validation, and success states;
- unchanged inquiry API contract.

### 11.2 Browser checks

Browser validation must cover desktop and mobile widths. It must verify:

- all six non-English homepages;
- all localized product and comparison routes;
- header, menu, footer, CTA, and language-switch behavior;
- text overflow and line wrapping in longer translations;
- form progression and validation in every supported language;
- at least one complete non-English inquiry journey in preview.

## 12. Release Process

1. Work in an isolated Git worktree and feature branch.
2. Generate the localized pages and run automated checks locally.
3. Complete browser checks locally.
4. Deploy a Cloudflare Pages preview.
5. Present the preview for user review.
6. Obtain separate confirmation before merging the PR or publishing production.
7. After production deployment, verify the homepage, all 49 core routes, redirects, and `/api/inquiry` behavior.
8. Submit no real email test without immediate user confirmation. If authorized, submit one clearly labeled fictional test inquiry only.

The previous Cloudflare production deployment remains the rollback target until the production verification is complete.

If production shows a 500 response, blank page, missing core route, broken inquiry path, or unexpected customer-facing content, stop immediately and report the issue instead of attempting an unapproved repair.

## 13. Acceptance Criteria

The phase is complete when:

- all 42 non-English core pages are generated and reachable;
- the seven supported languages provide the same complete sales path;
- language switching preserves the current page;
- no supported-language core link falls back to English;
- unsupported language routes redirect as designed;
- old LISHI content is not reachable through localized routes covered by this phase;
- canonical, `hreflang`, sitemap, and structured metadata checks pass;
- the localized inquiry form reaches the existing secure API in preview;
- desktop and mobile browser checks pass;
- the user approves the preview before production release.
