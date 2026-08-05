# GasMixTech SEO and GEO Optimization Design

**Date:** 2026-08-05  
**Status:** Approved in conversation; pending implementation plan  
**Primary site:** https://gasmixtech.com

## 1. Objective

Improve discoverability of the English site in Google, Bing-backed search, and AI-assisted search for buyers researching laser-cutting gas mixers, while keeping the site accurate, maintainable, and consistent with the operating company's role.

Priority query cluster:

- gas mixer for laser cutting
- gas mixer from China
- gas mixing device in China
- gas mixer for laser cutting China
- gas mixer for laser cut

The wording `gas mixer for laser cut` is grammatically awkward and will be covered naturally in visible FAQ content rather than forced into titles or repeated throughout the site.

## 2. Agreed Positioning and Constraints

- The product is described generically as a **gas mixer for laser cutting** or **laser cutting gas mixing device**.
- EUCHIO, SAGEMRO, and LISHI must not be presented as the product brand on this site.
- GasMixTech may be used only as the website/site-name identity, not as a claimed proprietary product brand.
- Jinan Euchio Machinery Co., Ltd. is described as a **China-based supplier and solution provider**, not as the manufacturer or factory.
- Chinese content remains available.
- Active languages remain English, Chinese, Spanish, Korean, Japanese, Portuguese, and Polish.
- Withdrawn languages remain redirected to English and must not re-enter navigation, hreflang clusters, or sitemaps.
- English receives full content optimization. Other active languages receive technical SEO synchronization only in this phase.
- Blog and case content continue to be maintained in English only.
- No new near-duplicate keyword landing pages will be created.
- No price, review, rating, certification, installation count, country count, distributor count, or performance claim may be invented.

## 3. Evidence Policy

Use a conservative evidence standard:

- Retain only claims supported by current technical documentation, clearly identified test conditions, or published case material.
- Remove or rewrite conflicting figures such as 500 versus 1,000 installations, 50+ countries, or 30+ distributors unless verified evidence is supplied.
- Avoid unconditional claims such as `3x faster`, `zero burrs`, or fixed gas savings when the result depends on material, thickness, laser power, machine condition, gas supply, or test method.
- When a measured result is retained, state the conditions and identify the source page or case.
- Structured data and machine-readable files must match visible page content.

## 4. Page and Keyword Architecture

The existing nine English core pages remain the fixed core. Each page has one distinct search intent to reduce cannibalization.

| Page | Primary role | Target topic |
|---|---|---|
| `index.html` | Main commercial category page | gas mixer for laser cutting; China-based supplier |
| `about.html` | Company identity and sourcing trust | gas mixer from China; gas mixing device supplier in China |
| `compatibility.html` | Fit and integration | laser cutting gas mixer compatibility; machines, materials, gas sources |
| `parameters.html` | Technical evaluation | gas ratios, pressure, flow, and application parameters |
| `roi.html` | Commercial evaluation | gas consumption, operating cost, and ROI calculation |
| `payment.html` | Procurement process | how to buy a gas mixer from China; payment and delivery process |
| `contact.html` | Conversion | quotation, selection support, and technical consultation |
| `privacy.html` | Compliance | no product-keyword target; `noindex,follow` |
| `404.html` | Error recovery | `noindex,follow` |

The English blog index and case index will be optimized as supporting hubs. Existing English articles and cases will link to the most relevant core page rather than all pointing only to the homepage.

## 5. On-Page Content Design

Every indexable English core page will have:

- one unique title, meta description, and H1 aligned with its search intent;
- the primary topic stated naturally near the beginning;
- a concise answer-first introduction explaining what the page covers;
- descriptive H2/H3 structure;
- self-contained factual paragraphs that remain understandable when quoted;
- relevant internal links with natural anchor text;
- a clear contact or selection-support CTA;
- descriptive image alt text where images carry information.

The homepage will explain:

1. what a gas mixer for laser cutting is;
2. who it is intended for;
3. what information is needed for selection;
4. that the supplier and solution provider is based in China;
5. where to verify compatibility, parameters, ROI assumptions, and procurement steps.

The About page will clearly separate the website identity, product category, and legal operating company. It will not describe the company as the manufacturer unless the user later supplies evidence and explicitly changes the approved positioning.

FAQ content will answer genuine buyer questions, including natural variants of the user's target phrases. Exact-match repetition will not be used as a substitute for useful content.

## 6. Technical SEO Design

### 6.1 Indexing and Canonicalization

- Every unique, indexable locale page uses a self-referencing canonical.
- Privacy and 404 pages use `noindex,follow` and are excluded from the XML sitemap.
- The sitemap contains only canonical URLs that return HTTP 200 and are intended for indexing.
- Sitemap `lastmod` values change only when page content materially changes.
- Redirected and withdrawn locale URLs are excluded from the sitemap.

### 6.2 International SEO

- Retain reciprocal, self-referencing hreflang clusters for the seven active languages.
- Use English as `x-default`.
- Canonical, hreflang, sitemap, protocol, hostname, and trailing-slash conventions must agree.
- Withdrawn languages must not appear in hreflang annotations.
- Other active languages receive technical parity only; this phase does not add translated keyword copy.

### 6.3 Internal Discovery

- Keep each core page reachable from primary navigation or contextual links within three clicks of the homepage.
- Connect supporting blog and case pages to compatibility, parameters, ROI, payment, or contact according to topic.
- Check for broken links, redirecting internal links, and orphaned indexable pages.

## 7. Structured Data Design

Use JSON-LD only when it accurately represents visible content.

| Page type | Schema |
|---|---|
| Homepage | `WebSite`, `Organization`, `WebPage` |
| About | `AboutPage`, `Organization` |
| Contact | `ContactPage` |
| Other core pages | `WebPage`, `BreadcrumbList` where visible navigation supports it |
| Visible question-and-answer sections | `FAQPage` matching the exact visible questions and answers |
| English articles | `BlogPosting` with real author/publisher and publication/modification dates |

Do not fabricate `Offer`, `Review`, or `AggregateRating`. Because the site does not publish a fixed price, verified reviews, or aggregate ratings, the design does not target Google's Product rich result in this phase. Generic product meaning will be communicated through visible content and the page graph instead of incomplete or misleading rich-result markup.

FAQ markup is for accurate machine understanding; enhanced Google FAQ presentation is not promised.

## 8. GEO and Machine-Readable Design

### 8.1 Extractable Content

- Use direct definitions, selection criteria, comparison tables, and buyer questions where appropriate.
- Keep paragraphs focused on one factual idea without fragmenting pages into artificial AI-only text blocks.
- Add real source links or internal evidence references for technical and performance claims.
- Use honest modification dates and do not simulate freshness.

### 8.2 AI Files

- Rewrite `/llms.txt` as a short site overview with links to authoritative English pages.
- Rewrite `/llms-full.txt` as a consistent factual summary of product category, supplier role, selection inputs, compatibility, parameters, procurement, and contact paths.
- Remove brand conflicts, manufacturer claims, and unsupported scale or performance statistics from both files.
- Do not add `pricing.md` because there is no fixed public pricing to publish.
- Do not create AI-only duplicate pages or an OKF bundle in this phase.

These files are supplementary for non-Google consumers. They are not represented as ranking requirements for Google AI Overviews.

### 8.3 Crawler Policy

Public, indexable content should be accessible to search-and-citation crawlers:

- `Googlebot`
- `Bingbot`
- `OAI-SearchBot`
- `ChatGPT-User`
- `PerplexityBot`

Search access and model-training access are treated separately. `GPTBot` will be disallowed by default so that ChatGPT search discovery can remain enabled without granting the broader potential-training permission controlled by GPTBot. Existing directives for other crawlers will not be expanded without checking their current official documentation and purpose.

## 9. Implementation Scope

The implementation phase will modify only files required for:

- the nine English core pages;
- the English blog and case index pages;
- shared English article/case metadata or templates needed for author, date, schema, and internal-link consistency;
- technical SEO parity in the six other active languages;
- robots, sitemap, hreflang, schema, and AI-readable files;
- automated SEO/GEO verification.

It will not add new product features, redesign unrelated components, restore withdrawn languages, translate new marketing copy, or mass-produce new articles.

## 10. Verification Criteria

Before presenting a deployment candidate:

- all existing automated tests pass;
- new SEO assertions pass for title, description, H1, canonical, robots, and indexability rules;
- hreflang clusters are reciprocal and contain only active 200-status locale pages;
- sitemap URLs are canonical, indexable, and return 200 locally or in the preview environment;
- withdrawn languages do not appear in navigation, hreflang, or sitemap;
- structured data parses as JSON-LD and matches visible content;
- supported schema types are checked with Schema.org Validator and, where eligible, Google's Rich Results Test;
- internal links and generated search indexes build successfully;
- unsupported brand, manufacturer, scale, and absolute performance claims are absent from the optimized surfaces;
- the English experience and page performance show no material regression.

## 11. Publishing and Post-Launch Checks

Implementation and verification happen locally first. Production publishing is a separate gated action.

1. Present the exact change summary, test results, and deployment candidate.
2. Obtain explicit user confirmation before Cloudflare deployment.
3. After deployment, verify live status codes, redirects, canonical tags, hreflang, JSON-LD, robots, sitemap, and priority pages.
4. Present Search Console, Bing Webmaster Tools, sitemap resubmission, URL inspection, or IndexNow actions separately and obtain confirmation before changing those external systems.
5. Monitor target-query impressions, indexed pages, organic clicks, ChatGPT referral traffic, Bing visibility, and qualified inquiries over an initial 4–12 week observation window.

Rankings, indexing, rich results, and AI citations are not guaranteed.

## 12. Primary References

- [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product-snippet)
- [Google: Snippet controls and meta descriptions](https://developers.google.com/search/docs/appearance/snippet)
- [Google: Title links](https://developers.google.com/search/docs/appearance/title-link)
- [Google: Localized versions and hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [OpenAI: Publishers and developers FAQ](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq)
- [Perplexity: Crawler documentation](https://docs.perplexity.ai/docs/resources/perplexity-crawlers)
- [Bing: Webmaster Guidelines](https://www.bing.com/webmasters/help/bing-webmaster-guidelines-30fba23a)
- [IndexNow: Getting started](https://www.indexnow.org/documentation)
