# GasMixTech SEO and GEO Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the English GasMixTech site easier to discover and cite for laser-cutting gas-mixer queries while keeping claims evidence-based, preserving seven active languages, and separating search access from model-training access.

**Architecture:** Keep the existing static HTML architecture and nine-page core. Add an automated SEO/GEO contract, rewrite English metadata and answer-first content in place, normalize JSON-LD to accurate page entities, update the existing sitemap/LLM generator, and rebuild the existing Pagefind index. Do not add a case-study index; `/#samples` remains the English case entry point.

**Tech Stack:** Static HTML/CSS, Python 3 standard library, Node.js for existing Pagefind tooling, Cloudflare Pages deployment (deployment excluded until separately confirmed).

## Global Constraints

- Product wording: **gas mixer for laser cutting** or **laser cutting gas mixing device**.
- Site identity: GasMixTech may identify the website, not a proprietary product brand.
- Company identity: **Jinan Euchio Machinery Co., Ltd. — China-based supplier and solution provider**.
- Do not describe the company as the manufacturer or factory.
- Do not present EUCHIO, SAGEMRO, or LISHI as this product's brand.
- Retain `en`, `zh`, `es`, `ko`, `ja`, `pt`, and `pl`; retain English as `x-default`.
- Keep `it`, `de`, `fr`, `nl`, `tr`, `ru`, `vi`, and `th` withdrawn and redirected to English.
- Fully optimize English only; apply technical SEO parity to the other six active languages.
- Keep blog and case content English-only.
- Do not create a case-study index; use `https://gasmixtech.com/#samples` as the case entry.
- Do not create keyword doorway pages, `pricing.md`, an OKF bundle, or new product features.
- Remove or qualify unsupported brand, manufacturer, scale, and absolute performance claims.
- Production deployment, Search Console changes, Bing Webmaster changes, and IndexNow submission require separate explicit confirmation.
- The worktree contains extensive pre-existing user changes, including overlapping HTML files. Never reset, restore, or overwrite them. Inspect diffs per file and do not create implementation commits unless the staged diff is proven to contain only this plan's changes.

---

## File Map

**Create**

- `tests/test_seo_geo.py` — SEO/GEO contract for metadata, schema, AI files, robots, sitemap, and evidence policy.

**Modify — tests and generators**

- `tests/test_site_integrity.py` — replace the obsolete `1,000+` installation assertion with the approved conservative evidence rule.
- `generate-sitemap-geo.py` — generate only canonical/indexable URLs and conservative AI-readable files for the seven active languages.
- `stabilize-core-locales.py` — preserve the seven-language canonical/hreflang/noindex contract after English edits.
- `public/robots.txt` — allow search-and-citation crawlers while disallowing GPTBot training access.
- `public/sitemap.xml` — generated output.
- `public/llms.txt`, `public/llms-full.txt`, `public/llms-en.txt`, `public/llms-zh.txt`, `public/llms-es.txt`, `public/llms-ko.txt`, `public/llms-ja.txt`, `public/llms-pt.txt`, `public/llms-pl.txt` — generated conservative AI summaries.

**Modify — English core**

- `public/index.html`
- `public/about.html`
- `public/compatibility.html`
- `public/parameters.html`
- `public/roi.html`
- `public/payment.html`
- `public/contact.html`
- `public/privacy.html`
- `public/404.html`

**Modify — English supporting content**

- `public/blog/index.html`
- `public/blog/assist-gas-complete-guide.html`
- `public/blog/assist-gas-is-the-real-bottleneck.html`
- `public/blog/cutting-parameters-guide.html`
- `public/blog/how-to-choose-gas-mixer.html`
- `public/blog/laser-cutting-gas-faq.html`
- `public/blog/mixed-gas-for-stainless-steel-aluminum.html`
- `public/blog/mixed-gas-nitrogen-savings.html`
- `public/blog/mixed-gas-vs-oxygen-comparison.html`
- `public/blog/nitrogen-vs-mixed-gas-comparison.html`
- `public/blog/one-to-three-gas-mixing-setup.html`
- `public/blog/roi-calculator-real-numbers.html`
- `public/case-studies/60kw-thick-plate.html`
- `public/case-studies/bodor-12kw-aluminum.html`
- `public/case-studies/foshan-hans-20kw.html`
- `public/case-studies/southeast-asia-bodor.html`
- `public/case-studies/taiwan-penta-30kw.html`

**Modify — technical parity outputs**

- `public/{zh,es,ko,ja,pt,pl}/{index,about,compatibility,parameters,roi,payment,contact,privacy,404}.html`
- `public/_template.html` and `public/i18n/{en,zh,es,ko,ja,pt}.json` only where needed to prevent a future homepage rebuild from restoring obsolete product-brand metadata.

**Regenerate**

- `public/pagefind/**` — seven-language search index only.

---

### Task 1: Lock the Approved SEO/GEO Contract in Tests

**Files:**

- Create: `tests/test_seo_geo.py`
- Modify: `tests/test_site_integrity.py`

**Interfaces:**

- Consumes: static HTML and text outputs under `public/`.
- Produces: `SeoGeoTests`, used as the acceptance contract for every later task.

- [ ] **Step 1: Create the new contract test**

Create `tests/test_seo_geo.py` with these exact constants and test responsibilities:

```python
import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CORE = {
    "index.html": ("Gas Mixer for Laser Cutting | China-Based Supplier", "Gas Mixer for Laser Cutting"),
    "about.html": ("Gas Mixing Device Supplier in China | About Us", "A China-Based Gas Mixing Device Supplier and Solution Provider"),
    "compatibility.html": ("Laser Cutting Gas Mixer Compatibility Guide", "Check Laser Cutting Gas Mixer Compatibility"),
    "parameters.html": ("Gas Mixer for Laser Cutting: Ratios & Parameters", "Gas Mixer Ratios and Laser Cutting Parameters"),
    "roi.html": ("Laser Cutting Gas Mixer ROI & Cost Factors", "Evaluate Laser Cutting Gas Mixer ROI"),
    "payment.html": ("How to Buy a Gas Mixer from China | Payment Guide", "How to Buy a Gas Mixer from China"),
    "contact.html": ("Contact a Laser Cutting Gas Mixer Supplier in China", "Discuss Your Laser Cutting Gas Mixing Requirements"),
    "privacy.html": ("Privacy Policy | GasMixTech", "Privacy Policy"),
    "404.html": ("Page Not Found | GasMixTech", "Page Not Found"),
}
ACTIVE_LANGS = ("en", "zh", "es", "ko", "ja", "pt", "pl")
REMOVED_LANGS = ("it", "de", "fr", "nl", "tr", "ru", "vi", "th")
FORBIDDEN_POSITIONING = (
    "euchio mixed gas",
    "sagemro mixed gas",
    "lishi laser",
    "manufactured by jinan euchio",
    "manufacturer: jinan euchio",
    "500+ installed",
    "1,000+",
    "50+ countries",
    "30+ distributors",
)


class Probe(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.h1_parts = []
        self.meta = {}
        self.links = []
        self.jsonld = []
        self._capture = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"title", "h1"}:
            self._capture = tag
        if tag == "meta" and attrs.get("name"):
            self.meta[attrs["name"].casefold()] = attrs.get("content", "")
        if tag == "link":
            self.links.append(attrs)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._capture = "jsonld"
            self.jsonld.append("")

    def handle_endtag(self, tag):
        if tag in {"title", "h1", "script"}:
            self._capture = None

    def handle_data(self, data):
        if self._capture == "title":
            self.title_parts.append(data)
        elif self._capture == "h1":
            self.h1_parts.append(data)
        elif self._capture == "jsonld":
            self.jsonld[-1] += data

    @property
    def title(self):
        return " ".join("".join(self.title_parts).split())

    @property
    def h1(self):
        return " ".join("".join(self.h1_parts).split())


def parse(path):
    probe = Probe()
    probe.feed(path.read_text(encoding="utf-8"))
    return probe


def schema_types(value):
    found = set()
    if isinstance(value, dict):
        raw = value.get("@type")
        if isinstance(raw, str):
            found.add(raw)
        elif isinstance(raw, list):
            found.update(item for item in raw if isinstance(item, str))
        for child in value.values():
            found.update(schema_types(child))
    elif isinstance(value, list):
        for child in value:
            found.update(schema_types(child))
    return found


class SeoGeoTests(unittest.TestCase):
    def assert_core_contract(self, filenames):
        for filename in filenames:
            title, h1 = CORE[filename]
            with self.subTest(filename=filename):
                page = parse(PUBLIC / filename)
                self.assertEqual(page.title, title)
                self.assertEqual(page.h1, h1)
                self.assertTrue(page.meta.get("description"))

    def test_primary_positioning_page_metadata_and_h1(self):
        self.assert_core_contract(("index.html", "about.html"))

    def test_remaining_core_metadata_and_h1(self):
        self.assert_core_contract(tuple(name for name in CORE if name not in {"index.html", "about.html"}))

    def test_low_value_pages_are_noindex(self):
        for filename in ("privacy.html", "404.html"):
            self.assertEqual(parse(PUBLIC / filename).meta.get("robots"), "noindex, follow")

    def assert_schema_contract(self, filenames):
        expected = {
            "index.html": {"WebSite", "Organization", "WebPage"},
            "about.html": {"AboutPage", "Organization"},
            "contact.html": {"ContactPage"},
        }
        forbidden = {"Product", "Offer", "Review", "AggregateRating"}
        for filename in filenames:
            page = parse(PUBLIC / filename)
            values = [json.loads(raw) for raw in page.jsonld]
            types = set().union(*(schema_types(value) for value in values)) if values else set()
            self.assertTrue(expected.get(filename, {"WebPage"}) <= types, (filename, types))
            self.assertFalse(types & forbidden, (filename, types))

    def test_primary_positioning_page_schema(self):
        self.assert_schema_contract(("index.html", "about.html"))

    def test_remaining_core_schema(self):
        self.assert_schema_contract(tuple(name for name in CORE if name not in {"index.html", "about.html"}))

    def test_positioning_and_ai_files_use_conservative_facts(self):
        paths = [PUBLIC / name for name in CORE]
        paths += [PUBLIC / "llms.txt", PUBLIC / "llms-full.txt"]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths).casefold()
        for phrase in FORBIDDEN_POSITIONING:
            self.assertNotIn(phrase.casefold(), combined)
        self.assertIn("china-based supplier and solution provider", combined)
        self.assertIn("gas mixer for laser cutting", combined)

    def test_robots_separates_search_from_training(self):
        robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
        for agent in ("OAI-SearchBot", "ChatGPT-User", "PerplexityBot"):
            self.assertRegex(robots, rf"(?s)User-agent: {re.escape(agent)}\s+Allow: /")
        self.assertRegex(robots, r"(?s)User-agent: GPTBot\s+Disallow: /")

    def test_sitemap_contains_only_indexable_active_urls(self):
        tree = ET.parse(PUBLIC / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [node.text for node in tree.findall("s:url/s:loc", ns)]
        self.assertFalse(any("privacy" in loc or "404" in loc for loc in locs))
        self.assertFalse(any(f"/{lang}/" in loc for lang in REMOVED_LANGS for loc in locs))
        self.assertEqual(tree.findall("s:url/s:lastmod", ns), [])

    def test_blog_and_case_metadata_do_not_present_a_product_brand(self):
        paths = list((PUBLIC / "blog").glob("*.html"))
        paths += list((PUBLIC / "case-studies").glob("*.html"))
        for path in paths:
            page = parse(path)
            metadata = f"{page.title}\n{page.meta.get('description', '')}".casefold()
            self.assertNotIn("euchio mixed gas", metadata, path)
            self.assertNotIn("sagemro mixed gas", metadata, path)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Replace the obsolete installation-count test**

In `tests/test_site_integrity.py`, replace `test_about_deployment_proof_uses_verified_installation_data` with:

```python
def test_about_pages_do_not_publish_unverified_scale_claims(self):
    forbidden = re.compile(
        r"1,000\+|500\+\s+(?:installed|systems)|50\+\s+countries|30\+\s+(?:authorized\s+)?distributors",
        re.IGNORECASE,
    )
    for lang in LANGS:
        with self.subTest(lang=lang):
            content = page_path(lang, "about.html").read_text(encoding="utf-8")
            self.assertIsNone(forbidden.search(content))
```

- [ ] **Step 3: Run the new tests and verify the current site fails for the intended reasons**

Run:

```bash
python3 -m unittest tests.test_seo_geo tests.test_site_integrity -v
```

Expected: failures include the current EUCHIO-branded titles, Product/Offer schema, GPTBot `Allow`, unsupported installation counts, and sitemap privacy URLs. There must be no import or parser errors.

- [ ] **Step 4: Record the test-only checkpoint**

Run:

```bash
git diff -- tests/test_seo_geo.py tests/test_site_integrity.py
git status --short -- tests/test_seo_geo.py tests/test_site_integrity.py
```

Expected: only the new contract test and the one obsolete assertion are shown. Do not commit if `tests/test_site_integrity.py` contains unrelated unstaged user changes that cannot be separated safely.

---

### Task 2: Make Sitemap, AI Files, and Robots Match the Approved Policy

**Files:**

- Modify: `generate-sitemap-geo.py`
- Modify: `public/robots.txt`
- Regenerate: `public/sitemap.xml`
- Regenerate: `public/llms.txt`
- Regenerate: `public/llms-full.txt`
- Regenerate: `public/llms-en.txt`, `public/llms-zh.txt`, `public/llms-es.txt`, `public/llms-ko.txt`, `public/llms-ja.txt`, `public/llms-pt.txt`, `public/llms-pl.txt`

**Interfaces:**

- Consumes: active static pages and the seven-language matrix.
- Produces: `generate_sitemap()`, `generate_llms_txt()`, `generate_llms_full_txt()`, and `generate_locale_llms(code, label, path)`.

- [ ] **Step 1: Add focused generator tests to `tests/test_seo_geo.py`**

Add these assertions to `SeoGeoTests`:

```python
    def test_ai_files_link_only_to_real_authoritative_pages(self):
        for filename in ("llms.txt", "llms-full.txt"):
            content = (PUBLIC / filename).read_text(encoding="utf-8")
            self.assertNotIn("/case-studies/", content)
            self.assertIn("https://gasmixtech.com/#samples", content)
            self.assertIn("https://gasmixtech.com/compatibility.html", content)
            self.assertIn("https://gasmixtech.com/parameters", content)
            self.assertIn("https://gasmixtech.com/roi.html", content)

    def test_locale_ai_files_exist_for_active_languages_only(self):
        for lang in ACTIVE_LANGS:
            self.assertTrue((PUBLIC / f"llms-{lang}.txt").is_file())
        for lang in REMOVED_LANGS:
            self.assertFalse((PUBLIC / f"llms-{lang}.txt").exists())
```

Run `python3 -m unittest tests.test_seo_geo.SeoGeoTests.test_ai_files_link_only_to_real_authoritative_pages -v` and expect failure because the current files link to the nonexistent `/case-studies/` index.

- [ ] **Step 2: Reduce `generate-sitemap-geo.py` to verified outputs**

Keep the existing `DOMAIN`, `BASE`, seven-language URL helpers, and alternate groups. Make these exact behavior changes:

```python
def is_indexable_html(path):
    if path.name in {"404.html", "_template.html", "privacy.html"}:
        return False
    content = path.read_text(encoding="utf-8", errors="ignore")
    return not re.search(
        r'<meta\s+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
        content,
        re.IGNORECASE,
    )


def get_all_pages():
    pages = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [name for name in dirs if name not in {"pagefind", ".wrangler"}]
        for filename in files:
            path = Path(root) / filename
            if filename.endswith(".html") and is_indexable_html(path):
                pages.append(path.relative_to(BASE).as_posix())
    return sorted(pages)
```

Import `re` and `Path`, remove the `date` import, and remove all generated `<lastmod>`, `<changefreq>`, and `<priority>` nodes. This prevents false freshness and deprecated hint maintenance.

Replace the two AI generator bodies with concise, evidence-safe content containing:

```python
CORE_LINKS = (
    ("Gas mixer for laser cutting", f"{DOMAIN}/"),
    ("Supplier and solution-provider profile", f"{DOMAIN}/about"),
    ("Compatibility assessment", f"{DOMAIN}/compatibility.html"),
    ("Gas ratios and cutting parameters", f"{DOMAIN}/parameters"),
    ("ROI and cost factors", f"{DOMAIN}/roi.html"),
    ("Payment and procurement process", f"{DOMAIN}/payment.html"),
    ("Selection support and quotation", f"{DOMAIN}/contact"),
    ("English technical articles", f"{DOMAIN}/blog/"),
    ("English case examples", f"{DOMAIN}/#samples"),
)

SUPPLIER_FACT = (
    "Jinan Euchio Machinery Co., Ltd. is the China-based supplier and solution "
    "provider operating this website. Product selection is assessed against "
    "laser power, material, thickness, assist-gas supply, pressure, flow, and "
    "integration requirements before quotation."
)
```

`generate_llms_txt()` must contain the site name, the generic product definition, `SUPPLIER_FACT`, `CORE_LINKS`, the seven active locale homepages, and links to `llms-full.txt`, `sitemap.xml`, and `robots.txt`.

`generate_llms_full_txt()` must explain only:

- what a laser-cutting gas mixer does;
- who should assess it;
- the selection inputs listed in `SUPPLIER_FACT`;
- that parameter tables and case results depend on recorded conditions;
- the compatibility, parameters, ROI, payment, contact, blog, and `/#samples` evidence paths;
- the legal company role and contact details already visible on the site.

It must not contain a manufacturer claim, product brand, fixed outcome, unverified installed base, distributor network, warranty, delivery-time promise, or unsupported specification.

Add:

```python
LOCALES = (
    ("en", "English", "/"),
    ("zh", "Chinese", "/zh/"),
    ("es", "Spanish", "/es/"),
    ("ko", "Korean", "/ko/"),
    ("ja", "Japanese", "/ja/"),
    ("pt", "Portuguese", "/pt/"),
    ("pl", "Polish", "/pl/"),
)


def generate_locale_llms(code, label, path):
    return "\n".join([
        f"# GasMixTech — {label}",
        f"> Maintained locale: {DOMAIN}{path}",
        "> Product category: gas mixer for laser cutting.",
        f"> {SUPPLIER_FACT}",
        "",
        "## Authoritative English Resources",
        *[f"- {name}: {url}" for name, url in CORE_LINKS],
        "",
        f"- Full site summary: {DOMAIN}/llms-full.txt",
        f"- Sitemap: {DOMAIN}/sitemap.xml",
        "",
    ])
```

The main block must write `llms-{code}.txt` for each `LOCALES` entry after writing the sitemap and two root AI files.

- [ ] **Step 3: Apply the exact robots policy**

Update `public/robots.txt` to preserve the global crawl allowance and sitemap, explicitly allow search/citation access, and separate GPTBot training access:

```text
User-agent: *
Allow: /
Disallow: /_template.html

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: GPTBot
Disallow: /

Sitemap: https://gasmixtech.com/sitemap.xml
```

Do not add crawler claims to visible page copy. Do not treat `Google-Extended` as a requirement for Google AI Overviews.

- [ ] **Step 4: Regenerate outputs**

Run:

```bash
python3 generate-sitemap-geo.py
```

Expected: one sitemap, `llms.txt`, `llms-full.txt`, and seven locale LLM files are written without traceback. The sitemap count excludes privacy, 404, `_template.html`, and all withdrawn locale pages.

- [ ] **Step 5: Run focused tests**

Run:

```bash
python3 -m unittest \
  tests.test_seo_geo.SeoGeoTests.test_robots_separates_search_from_training \
  tests.test_seo_geo.SeoGeoTests.test_sitemap_contains_only_indexable_active_urls \
  tests.test_seo_geo.SeoGeoTests.test_ai_files_link_only_to_real_authoritative_pages \
  tests.test_seo_geo.SeoGeoTests.test_locale_ai_files_exist_for_active_languages_only -v
```

Expected: all four tests pass.

- [ ] **Step 6: Inspect the generator/output diff checkpoint**

Run:

```bash
git diff -- generate-sitemap-geo.py public/robots.txt public/sitemap.xml public/llms.txt public/llms-full.txt public/llms-en.txt public/llms-zh.txt public/llms-es.txt public/llms-ko.txt public/llms-ja.txt public/llms-pt.txt public/llms-pl.txt
```

Expected: no withdrawn-language link, nonexistent case-index link, manufacturer claim, product-brand claim, or unverified metric remains.

---

### Task 3: Reposition and Optimize the Homepage and About Page

**Files:**

- Modify: `public/index.html`
- Modify: `public/about.html`
- Modify for rebuild safety: `public/_template.html`, `public/i18n/en.json`

**Interfaces:**

- Consumes: the approved keyword map and organization `@id` `https://gasmixtech.com/#organization`.
- Produces: the primary category page and China-supplier entity page used by all other internal links and schema nodes.

- [ ] **Step 1: Run the two page contract tests and confirm failure**

Run:

```bash
python3 -m unittest \
  tests.test_seo_geo.SeoGeoTests.test_primary_positioning_page_metadata_and_h1 \
  tests.test_seo_geo.SeoGeoTests.test_primary_positioning_page_schema -v
```

Expected: homepage/About failures identify the old titles, H1s, Product/Offer schema, and brand/manufacturer fields.

- [ ] **Step 2: Apply the approved homepage metadata and answer-first copy**

Use these exact strings in `public/index.html` and mirror the source values in `public/_template.html` / `public/i18n/en.json` where the current build system owns them:

```text
Title: Gas Mixer for Laser Cutting | China-Based Supplier
Meta description: Evaluate a gas mixer for laser cutting with compatibility, gas-ratio, parameter, ROI, and procurement guidance from a China-based supplier and solution provider.
H1: Gas Mixer for Laser Cutting
Answer-first paragraph: A gas mixer for laser cutting blends nitrogen and oxygen into a controlled assist-gas mixture for compatible fiber laser processes. This site is operated by Jinan Euchio Machinery Co., Ltd., a China-based supplier and solution provider that helps buyers assess machine compatibility, process requirements, and gas-supply conditions before quotation.
```

Change the visible product identity from `EUCHIO Mixed Gas Device` to the generic category. GasMixTech may remain as the site-name label. Keep the legal company name in the supplier disclosure and footer. Reframe fixed performance language as links to recorded parameter and case conditions; remove unconditional `3x faster`, `zero burrs`, `33% less nitrogen`, and similar statements from the title, meta description, hero, schema, and FAQ answers.

Add contextual links in the answer/selection area to:

```html
<a href="/compatibility.html">compatibility assessment</a>
<a href="/parameters">gas ratios and cutting parameters</a>
<a href="/roi.html">ROI and cost factors</a>
<a href="/payment.html">procurement process</a>
```

Keep the existing `#samples` section as the only case-entry hub.

- [ ] **Step 3: Replace homepage JSON-LD with an accurate graph**

Use one JSON-LD `@graph` containing these nodes and identifiers:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://gasmixtech.com/#organization",
      "name": "Jinan Euchio Machinery Co., Ltd.",
      "url": "https://gasmixtech.com/",
      "description": "China-based supplier and solution provider for laser-cutting gas mixing equipment.",
      "logo": "https://gasmixtech.com/images/logo.png",
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "sales",
        "email": "sales@gasmixtech.com",
        "telephone": "+86-186-1558-4520"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://gasmixtech.com/#website",
      "url": "https://gasmixtech.com/",
      "name": "GasMixTech",
      "publisher": {"@id": "https://gasmixtech.com/#organization"}
    },
    {
      "@type": "WebPage",
      "@id": "https://gasmixtech.com/#webpage",
      "url": "https://gasmixtech.com/",
      "name": "Gas Mixer for Laser Cutting",
      "description": "Evaluation and sourcing guidance for laser-cutting gas mixing equipment.",
      "isPartOf": {"@id": "https://gasmixtech.com/#website"},
      "about": {"@id": "https://gasmixtech.com/#organization"}
    }
  ]
}
```

Retain `FAQPage` only if every question and answer exactly matches visible page content after editing. Do not include `Product`, `Offer`, `Brand`, `manufacturer`, `Review`, or `AggregateRating`.

- [ ] **Step 4: Apply the approved About metadata and content**

Use:

```text
Title: Gas Mixing Device Supplier in China | About Us
Meta description: Learn how Jinan Euchio Machinery Co., Ltd. supports laser-cutting gas mixer selection, integration, delivery, and after-sales coordination from China.
H1: A China-Based Gas Mixing Device Supplier and Solution Provider
Answer-first paragraph: Jinan Euchio Machinery Co., Ltd. is a China-based supplier and solution provider for laser-cutting gas mixing equipment. We coordinate application assessment, product selection, integration requirements, delivery, and after-sales support with qualified manufacturing partners.
```

Remove or rewrite the current claims that the company developed/manufactured the device, the `1,000+` deployment block, `15 languages`, product-brand positioning, and the two-brand section where it distracts from the generic gas-mixer sourcing intent. Company brands may be described only as corporate context, not as the gas mixer's brand.

Replace About JSON-LD with an `@graph` containing `Organization`, `AboutPage`, and `BreadcrumbList`; reuse `https://gasmixtech.com/#organization` and `https://gasmixtech.com/#website`. Do not include founding date, brand ownership claims, service-area counts, or other facts not verified for this site.

- [ ] **Step 5: Run focused page and evidence tests**

Run:

```bash
python3 -m unittest \
  tests.test_seo_geo.SeoGeoTests.test_primary_positioning_page_metadata_and_h1 \
  tests.test_seo_geo.SeoGeoTests.test_primary_positioning_page_schema \
  tests.test_site_integrity.SiteIntegrityTests.test_about_pages_do_not_publish_unverified_scale_claims -v
```

Expected: all three focused homepage/About tests pass.

- [ ] **Step 6: Inspect the homepage/About diff**

Run:

```bash
git diff -- public/index.html public/about.html public/_template.html public/i18n/en.json
```

Expected: changes trace only to generic positioning, approved metadata/copy, schema accuracy, and internal links. Existing forms, analytics, navigation behavior, media, and unrelated styling remain intact.

---

### Task 4: Optimize the Remaining Seven English Core Pages

**Files:**

- Modify: `public/compatibility.html`
- Modify: `public/parameters.html`
- Modify: `public/roi.html`
- Modify: `public/payment.html`
- Modify: `public/contact.html`
- Modify: `public/privacy.html`
- Modify: `public/404.html`

**Interfaces:**

- Consumes: homepage organization/site `@id` values and page keyword map.
- Produces: seven intent-specific pages with unique metadata, cautious copy, accurate page schemas, and contextual links.

- [ ] **Step 1: Add per-page description checks**

Extend `CORE` in `tests/test_seo_geo.py` to a three-value tuple containing each exact description below, update `assert_core_contract` to unpack `(title, h1, description)`, and assert `page.meta["description"] == description`.

```text
compatibility.html: Check whether a fiber laser, material, thickness range, gas supply, pressure, and flow requirements are suitable for a laser cutting gas mixer.
parameters.html: Review reference gas ratios and laser cutting parameters with the process conditions needed before applying them to another machine or material.
roi.html: Evaluate laser cutting gas mixer ROI using gas consumption, cycle time, edge finishing, labor, utilization, and local operating costs.
payment.html: Understand how to buy a gas mixer from China, including assessment, quotation, proforma invoice, bank verification, payment, and delivery coordination.
contact.html: Contact a China-based laser cutting gas mixer supplier for compatibility assessment, selection support, integration questions, and quotation.
privacy.html: Read the GasMixTech privacy policy and learn how inquiry and website data are collected, used, and protected.
404.html: The requested GasMixTech page could not be found. Return to the laser cutting gas mixer guide or contact the supplier for help.
```

Run `python3 -m unittest tests.test_seo_geo.SeoGeoTests.test_remaining_core_metadata_and_h1 -v` and expect failures for these seven pages.

- [ ] **Step 2: Apply exact titles, H1s, and descriptions**

Use the values in `CORE` and Step 1. Place one answer-first paragraph directly under each page's existing hero H1 without adding a new `<section>`:

```text
Compatibility: Compatibility depends on the fiber laser, material and thickness range, available nitrogen and oxygen supply, required pressure and flow, and the machine's assist-gas interface. These inputs must be checked together before a gas mixer is quoted.

Parameters: Gas ratios and cutting parameters are reference starting points, not universal settings. Results vary with laser power, optics, nozzle, focus, material condition, gas purity, pressure, flow, and machine condition.

ROI: A laser cutting gas mixer's return depends on local gas prices, cycle-time change, edge-finishing labor, machine utilization, material mix, and the conditions used for any comparison. The calculator provides an estimate, not a guaranteed saving.

Payment: Procurement starts with an application assessment and written quotation. Payment details are provided only on a confirmed proforma invoice issued for the agreed equipment and delivery scope; buyers should verify beneficiary details before transfer.

Contact: Send the laser brand, power, material, thickness range, current assist gas, gas-supply method, and production objective. These inputs allow the China-based supplier and solution provider to check suitability before quotation.
```

Keep the Privacy and 404 body copy functional and neutral; their H1s remain `Privacy Policy` and `Page Not Found`.

- [ ] **Step 3: Normalize the seven page schemas**

For Compatibility, Parameters, ROI, and Payment, use `WebPage` plus `BreadcrumbList`. For Contact, use `ContactPage` plus `BreadcrumbList`. Privacy and 404 need no JSON-LD.

Use these page `@id` values:

```text
https://gasmixtech.com/compatibility.html#webpage
https://gasmixtech.com/parameters#webpage
https://gasmixtech.com/roi.html#webpage
https://gasmixtech.com/payment.html#webpage
https://gasmixtech.com/contact#webpage
```

Every page node uses `isPartOf: {"@id": "https://gasmixtech.com/#website"}` and `publisher: {"@id": "https://gasmixtech.com/#organization"}`. Breadcrumb item URLs must match the page canonical exactly. Remove Product/Offer/Review/AggregateRating and any schema claim not visible on the page.

- [ ] **Step 4: Strengthen contextual internal links without changing navigation structure**

Add or verify these relationships:

```text
Compatibility → Parameters, Contact
Parameters → Compatibility, ROI, Contact
ROI → Parameters, Contact
Payment → Contact, Privacy
Contact → Compatibility, Parameters, Payment, Privacy
404 → Homepage, Blog, Contact
```

Use natural anchor phrases. Do not repeat an exact-match keyword more than needed for reader clarity.

- [ ] **Step 5: Run the core SEO/GEO tests**

Run:

```bash
python3 -m unittest \
  tests.test_seo_geo.SeoGeoTests.test_primary_positioning_page_metadata_and_h1 \
  tests.test_seo_geo.SeoGeoTests.test_remaining_core_metadata_and_h1 \
  tests.test_seo_geo.SeoGeoTests.test_primary_positioning_page_schema \
  tests.test_seo_geo.SeoGeoTests.test_remaining_core_schema \
  tests.test_seo_geo.SeoGeoTests.test_low_value_pages_are_noindex \
  tests.test_seo_geo.SeoGeoTests.test_positioning_and_ai_files_use_conservative_facts \
  tests.test_seo_geo.SeoGeoTests.test_robots_separates_search_from_training \
  tests.test_seo_geo.SeoGeoTests.test_sitemap_contains_only_indexable_active_urls -v
```

Expected: all listed core, schema, noindex, robots, sitemap, and AI-file tests pass. Supporting-content tests are intentionally run in Task 5.

- [ ] **Step 6: Run legacy core integrity tests**

Run:

```bash
python3 -m unittest tests.test_site_integrity tests.test_multilingual_core -v
```

Expected: failures, if any, are limited to multilingual component parity caused by intentional English content placement. Resolve by moving answer-first text inside existing containers, not by deleting localized content or adding untranslated sections.

---

### Task 5: Normalize English Blog and Case Metadata, Attribution, and Internal Links

**Files:**

- Modify: `public/blog/index.html`
- Modify: all 11 English article files listed in the File Map
- Modify: all 5 English case files listed in the File Map

**Interfaces:**

- Consumes: core page canonicals and organization `@id`.
- Produces: English-only supporting content that attributes the publisher consistently and routes buyers to the relevant core page or `/#samples`.

- [ ] **Step 1: Add supporting-content schema tests**

Add to `SeoGeoTests`:

```python
    def test_articles_and_cases_use_legal_publisher(self):
        paths = [path for path in (PUBLIC / "blog").glob("*.html") if path.name != "index.html"]
        paths += list((PUBLIC / "case-studies").glob("*.html"))
        for path in paths:
            values = [json.loads(raw) for raw in parse(path).jsonld]
            serialized = json.dumps(values, ensure_ascii=False)
            self.assertIn("Jinan Euchio Machinery Co., Ltd.", serialized, path)
            self.assertNotIn("EUCHIO Mixed Gas", serialized, path)
            self.assertNotIn('"@type": "Product"', serialized, path)

    def test_case_pages_link_back_to_case_entry_and_relevant_core_page(self):
        for path in (PUBLIC / "case-studies").glob("*.html"):
            content = path.read_text(encoding="utf-8")
            self.assertIn('href="/#samples"', content, path)
            self.assertRegex(content, r'href="/(?:parameters|compatibility\.html|roi\.html|contact)"')
```

Run both tests and expect failure on the old `EUCHIO Mixed Gas` author/publisher names and missing `/#samples` links.

- [ ] **Step 2: Optimize the blog hub**

Use:

```text
Title: Laser Cutting Gas Mixer Guides | GasMixTech
Meta description: Read practical guides on laser cutting assist gases, gas mixer selection, compatibility, parameters, comparisons, and ROI evaluation.
H1: Laser Cutting Gas Mixer Guides
```

Replace product-brand descriptions with category language. Keep all article cards and English-only behavior. Add a short hub introduction linking to `/compatibility.html`, `/parameters`, and `/roi.html`.

- [ ] **Step 3: Normalize article and case metadata without bulk-rewriting bodies**

For all 11 blog articles and 5 case pages:

- replace title suffixes such as `| EUCHIO Mixed Gas` with `| GasMixTech` or remove the suffix when the title would exceed 60–65 characters;
- remove `EUCHIO Mixed Gas` from meta descriptions;
- use `Jinan Euchio Machinery Co., Ltd.` as the `author`/`publisher` Organization in `BlogPosting` or `Article` JSON-LD;
- preserve the real `datePublished`;
- set `dateModified` to `2026-08-05` only on pages whose metadata, attribution, or visible internal-link block is changed in this implementation;
- remove embedded Product/Offer schema and unsupported aggregate claims;
- keep measured case numbers only when the page states the machine, material, thickness, and recorded conditions; otherwise soften the title/meta claim to `recorded result` or `case example` and explain that results vary;
- do not add a case-study index URL.

Use the legal publisher reference:

```json
{
  "@type": "Organization",
  "@id": "https://gasmixtech.com/#organization",
  "name": "Jinan Euchio Machinery Co., Ltd."
}
```

- [ ] **Step 4: Add topic-specific internal links**

At the end of each article/case, add one compact “Next step” paragraph using only relevant destinations:

```html
<p class="article-next-step"><strong>Next step:</strong> Check <a href="/compatibility.html">machine and gas-supply compatibility</a>, review <a href="/parameters">reference parameters</a>, or <a href="/contact">send your cutting conditions for assessment</a>.</p>
```

ROI/cost articles must also link to `/roi.html`. Case pages must include `Back to case examples` linking to `/#samples`.

- [ ] **Step 5: Run the supporting-content tests**

Run:

```bash
python3 -m unittest \
  tests.test_seo_geo.SeoGeoTests.test_blog_and_case_metadata_do_not_present_a_product_brand \
  tests.test_seo_geo.SeoGeoTests.test_articles_and_cases_use_legal_publisher \
  tests.test_seo_geo.SeoGeoTests.test_case_pages_link_back_to_case_entry_and_relevant_core_page -v
```

Expected: all three pass.

- [ ] **Step 6: Inspect supporting-content diffs**

Run:

```bash
git diff -- public/blog public/case-studies
```

Expected: metadata, schema attribution, claim qualification, and internal links only. Article topics, case conditions, media, analytics, and unrelated layout remain intact.

---

### Task 6: Synchronize the Six Other Active Languages Technically

**Files:**

- Modify: `stabilize-core-locales.py`
- Modify: `public/{zh,es,ko,ja,pt,pl}/{index,about,compatibility,parameters,roi,payment,contact,privacy,404}.html`
- Modify where necessary: `public/_template.html`, `public/i18n/{zh,es,ko,ja,pt}.json`
- Regenerate: `public/sitemap.xml` and locale LLM files

**Interfaces:**

- Consumes: the English page structure and seven-language matrix.
- Produces: reciprocal hreflang, locale-self canonicals, exact language switchers, valid JSON-LD, and `noindex,follow` privacy/404 pages without new translated keyword copy.

- [ ] **Step 1: Add technical-parity assertions**

Add `locale_path` above the existing `SeoGeoTests` class, then add the two indented methods inside that existing class:

```python
def locale_path(lang, filename):
    return PUBLIC / filename if lang == "en" else PUBLIC / lang / filename
```

Inside the existing `SeoGeoTests` class:

```python
    def test_all_privacy_and_404_pages_are_noindex(self):
        for lang in ACTIVE_LANGS:
            for filename in ("privacy.html", "404.html"):
                self.assertEqual(
                    parse(locale_path(lang, filename)).meta.get("robots"),
                    "noindex, follow",
                    (lang, filename),
                )

    def test_active_core_jsonld_is_valid(self):
        for lang in ACTIVE_LANGS:
            for filename in CORE:
                for raw in parse(locale_path(lang, filename)).jsonld:
                    json.loads(raw)
```

Run the two new tests and record any exact locale/page failures.

- [ ] **Step 2: Keep the locale normalizer strictly technical**

Update `stabilize-core-locales.py` only as needed so a run preserves:

```python
LANGUAGES = (
    ("en", "English"),
    ("zh", "中文"),
    ("es", "Español"),
    ("ko", "한국어"),
    ("ja", "日本語"),
    ("pt", "Português"),
    ("pl", "Polski"),
)
```

The normalizer must:

- leave body translations intact;
- keep locale-self canonical URLs;
- write exactly seven language alternates plus English `x-default` on indexable core pages;
- remove hreflang from 404 pages;
- ensure privacy and 404 pages contain `<meta name="robots" content="noindex, follow">`;
- never recreate withdrawn directories or `llms-<removed>.txt` files;
- never restore EUCHIO/SAGEMRO/LISHI as the English product brand.

Do not add translated SEO keyword paragraphs in this task.

- [ ] **Step 3: Run the normalizer and regenerate technical outputs**

Run:

```bash
python3 stabilize-core-locales.py
python3 generate-sitemap-geo.py
```

Expected: seven-language normalization completes, the sitemap is rewritten, and no withdrawn language directory/file is created.

- [ ] **Step 4: Run multilingual and SEO parity tests**

Run:

```bash
python3 -m unittest tests.test_multilingual_core tests.test_site_integrity tests.test_seo_geo -v
```

Expected: all tests pass. If an English answer-first edit changed component counts, revise the English placement to reuse an existing element instead of copying English marketing content into localized pages.

- [ ] **Step 5: Inspect language-scope diff**

Run:

```bash
git diff -- stabilize-core-locales.py public/zh public/es public/ko public/ja public/pt public/pl public/_template.html public/i18n
```

Expected: locale changes are limited to canonical, hreflang, robots, schema identifiers/validity, language switching, and shared site identity. Chinese and the other five active translations remain present.

---

### Task 7: Rebuild Search, Validate the Static Site, and Prepare the Deployment Candidate

**Files:**

- Regenerate: `public/pagefind/**`
- Verify: all modified files from Tasks 1–6
- No production write in this task.

**Interfaces:**

- Consumes: the completed static site.
- Produces: a locally verified deployment candidate and a precise user-facing publish checklist.

- [ ] **Step 1: Rebuild Pagefind from the final public tree**

Run:

```bash
npx pagefind --site public
```

Expected: Pagefind completes successfully and reports only the seven active language indexes. No `de`, `fr`, `it`, `nl`, `ru`, `tr`, `vi`, or `th` metadata/wasm/index output may remain.

- [ ] **Step 2: Run the complete automated suite**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests pass with `OK`.

- [ ] **Step 3: Run deterministic text and artifact checks**

Run:

```bash
rg -n -i "EUCHIO Mixed Gas|SAGEMRO Mixed Gas|LISHI LASER|manufactured by Jinan Euchio|500\+ installed|1,000\+|50\+ countries|30\+ distributors" public/index.html public/about.html public/compatibility.html public/parameters.html public/roi.html public/payment.html public/contact.html public/llms*.txt public/blog public/case-studies
```

Expected: no product-brand, manufacturer, or unverified scale match. Corporate mentions of EUCHIO/SAGEMRO are acceptable only if explicitly presented as separate corporate brands on About, never as the gas mixer's brand.

Run:

```bash
find public -maxdepth 1 -type d \( -name de -o -name fr -o -name it -o -name nl -o -name ru -o -name tr -o -name vi -o -name th \) -print
```

Expected: no output.

- [ ] **Step 4: Serve locally and perform browser checks**

Run:

```bash
python3 -m http.server 8000 --directory public
```

In a browser, check:

```text
http://localhost:8000/
http://localhost:8000/about.html
http://localhost:8000/compatibility.html
http://localhost:8000/parameters.html
http://localhost:8000/roi.html
http://localhost:8000/payment.html
http://localhost:8000/contact.html
http://localhost:8000/blog/
http://localhost:8000/case-studies/60kw-thick-plate.html
http://localhost:8000/zh/
```

Expected: pages render, navigation and language switchers work, no visible raw JSON/template tokens appear, forms remain usable, the case page returns to `/#samples`, and no horizontal/mobile layout regression is visible.

- [ ] **Step 5: Validate structured data**

Extract every JSON-LD block with the existing test parser and confirm JSON parsing locally. For homepage, About, Contact, and one blog article, also validate the final preview or production URL with:

```text
https://validator.schema.org/
https://search.google.com/test/rich-results
```

Expected: Schema.org parsing has no errors. Google may report no eligible rich result for generic WebPage/Organization graphs; that is acceptable. Product, Offer, Review, and AggregateRating must not appear.

- [ ] **Step 6: Audit the final diff without staging unrelated work**

Run:

```bash
git diff --check
git status --short
git diff --stat
```

Expected: no whitespace errors. Review every SEO/GEO-touched file, preserve all unrelated user changes, and do not stage or commit overlapping files automatically.

- [ ] **Step 7: Present the deployment gate**

Copy the exact sitemap URL total from `rg -c '<url>' public/sitemap.xml`, the final `unittest` summary, and the Pagefind build summary into the report. Report:

```text
- English core pages changed: 9
- English blog hub changed: 1
- English articles normalized: 11
- English case pages normalized: 5
- Active locales technically checked: en, zh, es, ko, ja, pt, pl
- Withdrawn locales absent and redirected: it, de, fr, nl, tr, ru, vi, th
- Sitemap URL count and source command
- Complete automated-test pass count and final status
- Pagefind language/page count copied from the build output
- Production deployment: NOT YET PERFORMED
```

Then request explicit confirmation before running:

```bash
npx wrangler pages deploy public --project-name lishi-laser-website
```

Do not deploy, submit Search Console URLs, change Bing Webmaster Tools, or call IndexNow until the user separately confirms those exact external actions.

---

## Final Acceptance Checklist

- [ ] The homepage targets `gas mixer for laser cutting` without keyword stuffing.
- [ ] About targets China-supplier intent and states supplier/solution-provider status.
- [ ] The nine English core pages have unique title, description, and H1 values.
- [ ] Privacy and 404 are `noindex, follow` in all seven active languages.
- [ ] Canonical, hreflang, sitemap, and language switchers agree.
- [ ] Withdrawn languages remain absent from files, Pagefind, sitemap, and hreflang.
- [ ] No Product/Offer/Review/AggregateRating schema is fabricated.
- [ ] Blog/case metadata and publisher attribution are generic/legal-company based.
- [ ] No case-study index is created; `/#samples` is used.
- [ ] `OAI-SearchBot`, `ChatGPT-User`, and `PerplexityBot` can crawl; `GPTBot` is disallowed.
- [ ] AI files contain only conservative facts and real links.
- [ ] All automated tests and local visual checks pass.
- [ ] No production or webmaster-platform action occurs without confirmation.
