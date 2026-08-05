# Multilingual Core Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stabilize nine core pages for 11 retained languages, remove four confirmed languages, and make English the tested structural baseline without deploying the site.

**Architecture:** Keep the current static HTML architecture. Add one focused integrity test module that defines the supported language/page matrix and structural invariants, then make surgical repairs to current HTML and active generators. Existing localized copy remains in place; English supplies missing structure and already-approved technical facts.

**Tech Stack:** Static HTML/CSS/JavaScript, Python 3 standard-library tests, existing Node.js builders, Pagefind CLI.

## Global Constraints

- Retain exactly `en zh es ko ja pt pl it de fr nl`.
- Remove exactly `tr ru vi th`; Arabic is not present.
- Maintain exactly `index about parameters contact compatibility roi payment privacy 404` for every retained language.
- Blog and case-study content remains English-only.
- Do not deploy to Cloudflare Pages.
- Preserve unrelated uncommitted changes.
- Do not change product claims, contact details, analytics identifiers, or company positioning.

---

### Task 1: Add the failing multilingual core integrity tests

**Files:**
- Create: `tests/test_multilingual_core.py`
- Modify: `tests/test_site_integrity.py`

**Interfaces:**
- Consumes: static files below `public/`.
- Produces: `RETAINED_LANGS`, `REMOVED_LANGS`, `CORE_PAGES`, `page_path()`, and a `MultilingualCoreTests` suite runnable with `python3 -m unittest -v`.

- [ ] **Step 1: Write the test constants and helpers**

```python
RETAINED_LANGS = ("en", "zh", "es", "ko", "ja", "pt", "pl", "it", "de", "fr", "nl")
REMOVED_LANGS = ("tr", "ru", "vi", "th")
CORE_PAGES = (
    "index.html", "about.html", "parameters.html", "contact.html",
    "compatibility.html", "roi.html", "payment.html", "privacy.html", "404.html",
)

def page_path(lang, filename):
    return PUBLIC / filename if lang == "en" else PUBLIC / lang / filename
```

Add helpers based on `html.parser.HTMLParser` to collect start tags, IDs, links, local assets, form field names, canonical links, hreflang codes, and JSON-LD blocks. Normalize only these permitted structural differences: the `active` class on language options, translated text nodes, `lang`, canonical/hreflang URLs, localized link prefixes, `alt`, `title`, and form labels/placeholders.

- [ ] **Step 2: Add one assertion per required behavior**

Add these exact test methods, each with direct assertions against the parsed static files:

- `test_exact_core_page_matrix`
- `test_removed_language_directories_and_outputs_are_absent`
- `test_component_counts_match_english`
- `test_contact_form_fields_match_english`
- `test_local_assets_resolve`
- `test_internal_links_resolve`
- `test_localized_blog_links_use_english_blog`
- `test_core_hreflang_set_is_exact`
- `test_canonical_urls_match_page_locale`
- `test_jsonld_is_valid`
- `test_no_placeholders_or_duplicate_ids`
- `test_sitemap_excludes_removed_languages`

Structural comparison uses the page-specific component selectors already present in the site:

```python
COMPONENT_SELECTORS = (
    "section", ".advantage-card", ".brand-card", ".params-card",
    ".blog-post-card", ".contact-method", ".form-group", ".form-row",
    ".footer-links", ".lang-option", ".faq-item", ".case-card",
)
```

- [ ] **Step 3: Restrict the existing suite to retained languages**

Update `LANGS`, `SUB_LANGS`, `TRANSLATED_ABOUT_MARKERS`, and the expected sitemap About count in `tests/test_site_integrity.py` to the retained set and `11` respectively.

- [ ] **Step 4: Run the new tests and verify RED**

Run: `python3 -m unittest -v tests.test_multilingual_core`

Expected: failures for existing `tr/ru/vi/th` outputs, current component-count drift, missing contact fields, malformed multi-dot CSS paths, localized `/xx/blog/` links, and the old 16-language hreflang sets.

---

### Task 2: Remove confirmed languages and prevent regeneration

**Files:**
- Delete: `public/tr/`, `public/ru/`, `public/vi/`, `public/th/`
- Delete: `public/llms-tr.txt`, `public/llms-ru.txt`, `public/llms-vi.txt`, `public/llms-th.txt`
- Delete: matching language-specific files below `public/pagefind/`
- Modify: `public/build-i18n.js`
- Modify: `public/build-privacy.js`
- Modify: `build-about-langs.py`
- Modify: `build-langs.py`
- Modify: `generate-sitemap-geo.py`
- Modify: `normalize-site.py`
- Modify: active language lists in `add-about-nav.py`, `add-about-sitemap.py`, `fix-logo-srcset.py`, `fix-hreflang-subpages.py`, and `fix-integrate-langs.py`

**Interfaces:**
- Consumes: the confirmed retained/removed language lists.
- Produces: active builders that cannot recreate removed locale pages.

- [ ] **Step 1: Delete only the confirmed generated targets**

Resolve every target explicitly, verify it is below `public/`, then remove the four directories and their language-specific `llms` and Pagefind artifacts. Do not delete English or retained-language files.

- [ ] **Step 2: Change all active language lists**

Use these exact lists:

```python
LANGS = ["en", "zh", "es", "ko", "ja", "pt", "pl", "it", "de", "fr", "nl"]
SUB_LANGS = LANGS[1:]
```

```javascript
const LANGUAGES = ['zh', 'es', 'ko', 'ja', 'pt', 'pl', 'it', 'de', 'fr', 'nl'];
```

Large historical translation dictionaries may remain when removing them would cause unrelated churn, but no executed language list may reference a removed locale.

- [ ] **Step 3: Run the removal tests**

Run: `python3 -m unittest -v tests.test_multilingual_core.MultilingualCoreTests.test_removed_language_directories_and_outputs_are_absent`

Expected: PASS.

---

### Task 3: Normalize the English baseline and shared locale metadata

**Files:**
- Modify: `public/compatibility.html`
- Modify: `public/roi.html`
- Modify: `public/payment.html`
- Modify: retained core HTML pages under `public/`
- Modify: `normalize-site.py`

**Interfaces:**
- Consumes: retained language list and English page URLs.
- Produces: 12-entry hreflang sets (11 languages plus `x-default`), correct language switchers, canonical URLs, asset paths, and English-only Blog links.

- [ ] **Step 1: Add failing English metadata assertions**

Verify all indexable English core pages have the exact retained hreflang set and that the three utility pages have the same language switcher component as their localized equivalents.

- [ ] **Step 2: Add deterministic normalization helpers**

Extend `normalize-site.py` with:

```python
RETAINED_LANGS = ["en", "zh", "es", "ko", "ja", "pt", "pl", "it", "de", "fr", "nl"]
REMOVED_LANGS = {"tr", "ru", "vi", "th"}

def normalize_asset_paths(content):
    content = re.sub(r'(?P<q>["\'])\.{2,}/(?P<asset>styles(?:\.min)?\.css|script(?:\.min)?\.js)', r'\g<q>../\g<asset>', content)
    return content

def normalize_blog_links(content):
    return re.sub(r'href="/[a-z]{2}/blog(?:/)?"', 'href="/blog/"', content)
```

Add helpers that replace, rather than append to, the language dropdown and hreflang block so repeated execution is idempotent.

- [ ] **Step 3: Normalize all retained core pages**

Run the normalizer once, inspect the diff, and verify it changes only URL, metadata, asset, dropdown, and language-reference lines.

- [ ] **Step 4: Run focused metadata/link tests**

Run: `python3 -m unittest -v tests.test_multilingual_core.MultilingualCoreTests.test_core_hreflang_set_is_exact tests.test_multilingual_core.MultilingualCoreTests.test_local_assets_resolve tests.test_multilingual_core.MultilingualCoreTests.test_localized_blog_links_use_english_blog`

Expected: PASS.

---

### Task 4: Repair visible component drift while preserving translations

**Files:**
- Modify: retained `index.html`, `about.html`, `parameters.html`, and `contact.html` locale pages identified by the failing component tests

**Interfaces:**
- Consumes: English page component order and existing localized text.
- Produces: matching visible sections/card counts/form fields/footer columns for each retained locale.

- [ ] **Step 1: Repair Polish homepage**

Restore the missing fifth `.params-card`, third footer link group, and remove the two misplaced `.case-card` fragments. Preserve Polish text already present; translate only the heading and table labels copied from the corresponding English component.

- [ ] **Step 2: Repair compact About pages**

For `ko`, `pt`, `pl`, `it`, and `nl`, restore the four missing `.advantage-card` components in their English section positions. Use the existing translated About headings and descriptions where present; translate missing card titles/descriptions without changing numerical claims.

- [ ] **Step 3: Repair Parameters pages**

For `es`, `zh`, `ko`, `pt`, and `pl`, restore the three `.blog-post-card` links to the English articles and the missing third footer link group. All article URLs remain under `/blog/`.

- [ ] **Step 4: Repair Contact pages**

For `zh`, `ko`, `ja`, and `pl`, restore the six missing form groups and two missing form rows using the exact English field names and option values:

```text
website, buyer_type, timeline, material, thickness, current_gas
```

Labels, placeholders, and option display text are localized; field `name`, `id`, and `value` attributes remain identical to English. Restore the missing footer group.

- [ ] **Step 5: Verify component parity GREEN**

Run: `python3 -m unittest -v tests.test_multilingual_core.MultilingualCoreTests.test_component_counts_match_english tests.test_multilingual_core.MultilingualCoreTests.test_contact_form_fields_match_english`

Expected: PASS.

---

### Task 5: Rebuild sitemap and search artifacts

**Files:**
- Modify: `public/sitemap.xml`
- Modify: `public/llms.txt`
- Modify: `public/llms-full.txt`
- Modify: generated files below `public/pagefind/`

**Interfaces:**
- Consumes: cleaned `public/` tree.
- Produces: search and discovery artifacts containing only retained core locales plus English blog/case content.

- [ ] **Step 1: Rebuild the sitemap**

Run: `python3 generate-sitemap-geo.py`

Expected: no `tr`, `ru`, `vi`, or `th` core URLs; no 404 URLs; retained core URLs and English blog/case URLs present.

- [ ] **Step 2: Remove deleted-language entries from LLM discovery files**

Mechanically remove links and sections whose URL prefix is `/tr/`, `/ru/`, `/vi/`, or `/th/`; retain English and all kept languages.

- [ ] **Step 3: Rebuild Pagefind**

Run: `npx pagefind --site public`

Expected: exit code `0`; no metadata or index output for removed languages.

- [ ] **Step 4: Run discovery tests**

Run: `python3 -m unittest -v tests.test_multilingual_core.MultilingualCoreTests.test_sitemap_excludes_removed_languages`

Expected: PASS.

---

### Task 6: Full verification and local browser smoke test

**Files:**
- No planned source changes; fix only failures directly caused by Tasks 1–5.

**Interfaces:**
- Consumes: completed static site.
- Produces: evidence that the local deliverable is ready for a separate deployment review.

- [ ] **Step 1: Run all Python tests**

Run: `python3 -m unittest -v`

Expected: all tests PASS with zero failures and zero errors.

- [ ] **Step 2: Run static integrity scan**

Run the new suite's full asset, internal-link, canonical, hreflang, JSON-LD, duplicate-ID, and placeholder checks.

Expected: all PASS.

- [ ] **Step 3: Serve the site locally**

Run: `python3 -m http.server 8000 --directory public`

Open representative pages: English nine-page core, Chinese homepage/parameters/contact, German homepage, French homepage, Polish homepage/contact, Japanese contact, and one utility page with a language switcher.

- [ ] **Step 4: Browser smoke checks**

At desktop and mobile viewport widths, verify header navigation, language dropdown, footer, contact form, local assets, and console errors. Verify removed locale URLs are absent from navigation and no localized Blog link points to `/xx/blog/`.

- [ ] **Step 5: Inspect the final diff**

Run: `git diff --check` and inspect `git status --short` plus scoped diffs. Confirm unrelated pre-existing modifications remain untouched and no deployment command was run.
