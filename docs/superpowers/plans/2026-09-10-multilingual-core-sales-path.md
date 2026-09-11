# GasMixTech Multilingual Core Sales Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the complete GasMixTech sales journey in English, Simplified Chinese, Spanish, Portuguese, Japanese, Korean, and Polish while redirecting unsupported and legacy localized routes to maintained English equivalents.

**Architecture:** Keep the static Cloudflare Pages site and its current template-based homepage and product builders. Add a shared Python locale/route contract, make product generation locale-aware, add deterministic About and Contact generation, and expose one build command that produces the seven-language core route matrix and discovery artifacts. English remains the factual source; localized JSON carries copy only, while templates, product relationships, form field names, and technical values remain shared.

**Tech Stack:** Static HTML/CSS/JavaScript, Python 3 standard library, Node.js built-in test runner, Python `unittest`, Pagefind 1.5.2, Cloudflare Pages/Wrangler.

**Approved design:** `docs/superpowers/specs/2026-09-10-multilingual-core-sales-path-design.md`

---

## Baseline

- Source branch at planning time: `docs/multilingual-core-sales-path-design` based on merge commit `c851657`.
- Python baseline: `python -m unittest discover -s tests -p 'test_*.py'` → 78 tests pass.
- Node baseline: `node --test tests/*.test.mjs` → 25 tests pass.
- Production deployment, DNS, email bindings, and inquiry recipient are outside code-change scope.

## Locked Language and Route Contract

Supported locales, in display and `hreflang` order:

```python
SUPPORTED_LOCALES = ("en", "zh", "es", "pt", "ja", "ko", "pl")
LOCALIZED_LOCALES = SUPPORTED_LOCALES[1:]
UNSUPPORTED_LOCALES = ("de", "fr", "it", "nl", "tr", "ru", "vi", "th")
```

Core page keys and English routes:

```python
CORE_ROUTES = {
    "home": "/",
    "about": "/about",
    "contact": "/contact",
    "psa": "/products/psa-nitrogen-generation-system",
    "cabinet": "/products/integrated-gas-mixing-cabinet",
    "valve": "/products/mspv2-4000-proportional-valve",
    "comparison": "/products/mixed-gas-control-comparison",
}
```

The generated matrix contains 49 core URLs: seven pages for each of seven languages. English uses root routes; other languages prefix the same route with `/{locale}`.

## Planned File Structure

### Create

- `site_locales.py` — supported languages, route mapping, output-path mapping, canonical and `hreflang` helpers.
- `build-static-core-pages.py` — deterministic About and Contact renderer.
- `build-core-locales.py` — single orchestration command for all core pages and discovery files.
- `public/core-page-templates/about.html` — About body/template source.
- `public/core-page-templates/contact.html` — Contact body/template source with the unchanged secure form contract.
- `public/i18n/core/en.json`
- `public/i18n/core/zh.json`
- `public/i18n/core/es.json`
- `public/i18n/core/pt.json`
- `public/i18n/core/ja.json`
- `public/i18n/core/ko.json`
- `public/i18n/core/pl.json`
- `public/i18n/products/zh.json`
- `public/i18n/products/es.json`
- `public/i18n/products/pt.json`
- `public/i18n/products/ja.json`
- `public/i18n/products/ko.json`
- `public/i18n/products/pl.json`
- `tests/test_multilingual_sales_path.py` — route, translation-data, generated-page, redirect, and SEO contract.

### Modify

- `public/build-i18n.js` — fail-closed homepage generation and locale-aware core links.
- `build-product-pages.py` — generate four product pages for all supported locales.
- `public/_template.html` — use stable route placeholders where necessary.
- `public/_redirects` — unsupported-language and non-core localized redirects.
- `generate-sitemap-geo.py` — emit alternates for the 49 core URLs only.
- `tests/test_multilingual_core.py` — replace the old nine-page matrix with the approved seven-page sales path.
- `tests/test_product_expansion.py` — run product assertions for every locale while preserving English factual checks.
- `tests/test_inquiry_form_markup.py` — verify localized labels/options as well as the unchanged form field contract.
- `README.md` — document the maintained seven-language scope and the single build command.
- `public/llms.txt`, `public/llms-full.txt`, and `public/llms-*.txt` — regenerated language/discovery statements.
- `public/pagefind/**` — regenerated search index from the final public tree.

### Generate

- `public/{zh,es,pt,ja,ko,pl}/index.html`
- `public/{zh,es,pt,ja,ko,pl}/about.html`
- `public/{zh,es,pt,ja,ko,pl}/contact.html`
- `public/{zh,es,pt,ja,ko,pl}/products/*.html`

### Remove after an explicit execution-time confirmation

For each of `zh`, `es`, `pt`, `ja`, `ko`, and `pl`, remove these six obsolete localized files after their redirects are tested:

- `404.html`
- `compatibility.html`
- `parameters.html`
- `payment.html`
- `privacy.html`
- `roi.html`

The exact deletion set is 36 tracked files. No English page is deleted.

---

### Task 1: Add the shared locale and route contract

**Files:**
- Create: `site_locales.py`
- Create: `tests/test_multilingual_sales_path.py`

- [ ] **Step 0: Create the implementation branch after execution is selected**

Explain that implementation will continue in the existing isolated worktree and create a new branch from the approved design commit. After the user chooses an execution mode, run:

```powershell
git switch -c feat/multilingual-core-sales-path
```

Expected: the active branch is `feat/multilingual-core-sales-path`; the dirty main checkout remains untouched.

- [ ] **Step 1: Write failing route-contract tests**

Add these constants and assertions to `tests/test_multilingual_sales_path.py`:

```python
import unittest
from pathlib import Path

from site_locales import (
    CORE_ROUTES,
    LOCALIZED_LOCALES,
    SUPPORTED_LOCALES,
    UNSUPPORTED_LOCALES,
    canonical_url,
    output_path,
    route_for,
)

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


class LocaleRouteContractTests(unittest.TestCase):
    def test_language_sets_are_exact_and_disjoint(self):
        self.assertEqual(SUPPORTED_LOCALES, ("en", "zh", "es", "pt", "ja", "ko", "pl"))
        self.assertEqual(LOCALIZED_LOCALES, SUPPORTED_LOCALES[1:])
        self.assertEqual(UNSUPPORTED_LOCALES, ("de", "fr", "it", "nl", "tr", "ru", "vi", "th"))
        self.assertFalse(set(SUPPORTED_LOCALES) & set(UNSUPPORTED_LOCALES))

    def test_core_route_map_is_exact(self):
        self.assertEqual(set(CORE_ROUTES), {"home", "about", "contact", "psa", "cabinet", "valve", "comparison"})
        self.assertEqual(route_for("en", "valve"), "/products/mspv2-4000-proportional-valve")
        self.assertEqual(route_for("ja", "valve"), "/ja/products/mspv2-4000-proportional-valve")
        self.assertEqual(route_for("pl", "home"), "/pl/")

    def test_output_and_canonical_mapping(self):
        self.assertEqual(output_path(PUBLIC, "en", "contact"), PUBLIC / "contact.html")
        self.assertEqual(output_path(PUBLIC, "es", "contact"), PUBLIC / "es" / "contact.html")
        self.assertEqual(output_path(PUBLIC, "ko", "psa"), PUBLIC / "ko" / "products" / "psa-nitrogen-generation-system.html")
        self.assertEqual(canonical_url("pt", "comparison"), "https://gasmixtech.com/pt/products/mixed-gas-control-comparison")
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.LocaleRouteContractTests`

Expected: import failure because `site_locales.py` does not exist.

- [ ] **Step 3: Implement the route contract**

Create `site_locales.py` with immutable constants and these exact public functions:

```python
from pathlib import Path

DOMAIN = "https://gasmixtech.com"
SUPPORTED_LOCALES = ("en", "zh", "es", "pt", "ja", "ko", "pl")
LOCALIZED_LOCALES = SUPPORTED_LOCALES[1:]
UNSUPPORTED_LOCALES = ("de", "fr", "it", "nl", "tr", "ru", "vi", "th")

CORE_ROUTES = {
    "home": "/",
    "about": "/about",
    "contact": "/contact",
    "psa": "/products/psa-nitrogen-generation-system",
    "cabinet": "/products/integrated-gas-mixing-cabinet",
    "valve": "/products/mspv2-4000-proportional-valve",
    "comparison": "/products/mixed-gas-control-comparison",
}


def route_for(locale, page_key):
    route = CORE_ROUTES[page_key]
    if locale == "en":
        return route
    return f"/{locale}/" if page_key == "home" else f"/{locale}{route}"


def canonical_url(locale, page_key):
    return f"{DOMAIN}{route_for(locale, page_key)}"


def output_path(public_dir: Path, locale, page_key):
    route = CORE_ROUTES[page_key]
    if page_key == "home":
        relative = Path("index.html")
    else:
        relative = Path(route.lstrip("/") + ".html")
    return public_dir / relative if locale == "en" else public_dir / locale / relative


def alternates_for(page_key):
    values = {locale: canonical_url(locale, page_key) for locale in SUPPORTED_LOCALES}
    values["x-default"] = values["en"]
    return values
```

- [ ] **Step 4: Run the focused test and verify GREEN**

Run: `python -m unittest -v tests.test_multilingual_sales_path.LocaleRouteContractTests`

Expected: three tests pass.

- [ ] **Step 5: Commit**

```powershell
git add site_locales.py tests/test_multilingual_sales_path.py
git commit -m "test: define multilingual sales route contract"
```

---

### Task 2: Make homepage generation fail closed and locale-aware

**Files:**
- Modify: `public/build-i18n.js`
- Modify: `public/_template.html`
- Modify: `tests/test_multilingual_sales_path.py`
- Regenerate: `public/index.html`
- Regenerate: `public/{zh,es,pt,ja,ko,pl}/index.html`

- [ ] **Step 1: Add failing homepage-generation tests**

Add `HomepageGenerationTests` that asserts:

```python
for locale in SUPPORTED_LOCALES:
    path = output_path(PUBLIC, locale, "home")
    content = path.read_text(encoding="utf-8")
    self.assertNotIn("{{", content)
    self.assertEqual(content.count('class="lang-option'), 7)
    for page_key in ("about", "contact", "psa", "cabinet", "valve", "comparison"):
        self.assertIn(f'href="{route_for(locale, page_key)}', content)
```

Add a subprocess test that invokes Node with:

```javascript
const { replacePlaceholders } = require('./public/build-i18n.js');
replacePlaceholders('{{missing.required.key}}', {});
```

Assert a non-zero exit and stderr containing `Missing translation key: missing.required.key`. Add a second Node subprocess assertion that serializes the exported `SUPPORTED_LOCALES` array and compares it with Python's `SUPPORTED_LOCALES` tuple.

- [ ] **Step 2: Run the new tests and verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.HomepageGenerationTests`

Expected: localized product routes still point to English and missing translation keys do not stop the build.

- [ ] **Step 3: Replace warning-based placeholder handling**

Change `replacePlaceholders` in `public/build-i18n.js` to throw:

```javascript
function replacePlaceholders(html, strings) {
  return html.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
    const normalizedKey = key.trim();
    const value = getNestedValue(strings, normalizedKey);
    if (value === undefined) {
      throw new Error(`Missing translation key: ${normalizedKey}`);
    }
    return String(value);
  });
}
```

Move all current top-level build side effects into `main(args = process.argv.slice(2))`, call it only under `if (require.main === module)`, and export `replacePlaceholders`, `adjustPaths`, and `SUPPORTED_LOCALES`. Define the exact JavaScript locale constant as `['en', 'zh', 'es', 'pt', 'ja', 'ko', 'pl']`; the cross-runtime test above enforces parity with `site_locales.py`. After rendering, reject any remaining `{{` or `}}` marker.

Add repeatable `--locale` parsing. `node public/build-i18n.js --locale ja` builds Japanese only, `--locale en --locale zh` builds those two locales, and no argument builds all seven. An unknown code exits non-zero with `Unsupported locale: CODE`.

- [ ] **Step 4: Localize every core route in generated homepages**

Extend `adjustPaths(html, lang)` to map the approved routes explicitly:

```javascript
const CORE_PATHS = [
  '/about',
  '/contact',
  '/products/psa-nitrogen-generation-system',
  '/products/integrated-gas-mixing-cabinet',
  '/products/mspv2-4000-proportional-valve',
  '/products/mixed-gas-control-comparison',
];

for (const route of CORE_PATHS) {
  html = html.replaceAll(`href="${route}`, `href="/${lang}${route}`);
}
```

Do not localize `/blog/`, `/roi`, `/parameters`, `/payment.html`, `/privacy.html`, or `/compatibility.html` in this phase; those links intentionally remain English.

- [ ] **Step 5: Generate and test homepages**

Run: `node public/build-i18n.js`

Expected: seven homepages are written; no missing-key warning appears.

Run: `python -m unittest -v tests.test_multilingual_sales_path.HomepageGenerationTests`

Expected: all homepage tests pass.

- [ ] **Step 6: Commit**

```powershell
git add public/build-i18n.js public/_template.html public/index.html public/zh/index.html public/es/index.html public/pt/index.html public/ja/index.html public/ko/index.html public/pl/index.html tests/test_multilingual_sales_path.py
git commit -m "feat: generate locale-aware core homepages"
```

---

### Task 3: Refactor the product builder for seven locales

**Files:**
- Modify: `build-product-pages.py`
- Modify: `tests/test_product_expansion.py`
- Modify: `tests/test_multilingual_sales_path.py`

- [ ] **Step 1: Add failing locale-aware product tests**

Make the product helper accept a locale and assert the full matrix:

```python
def product_path(locale, filename):
    base = PUBLIC / "products" if locale == "en" else PUBLIC / locale / "products"
    return base / filename


def test_product_page_matrix(self):
    for locale in SUPPORTED_LOCALES:
        for filename in PAGES.values():
            with self.subTest(locale=locale, filename=filename):
                self.assertTrue(product_path(locale, filename).is_file())
```

For each generated product page assert:

- `<html lang>` equals the locale;
- canonical equals `canonical_url(locale, page_key)`;
- all eight alternate entries are present exactly once;
- product navigation and Contact CTA use `route_for(locale, ...)`;
- the current language option is active;
- JSON-LD `inLanguage` equals the locale;
- Product/Breadcrumb/FAQ/Video relationships remain structurally equal to English.

- [ ] **Step 2: Run the matrix test and verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.ProductRouteTests`

Expected: 24 localized product pages are missing.

- [ ] **Step 3: Add locale-aware builder inputs and CLI**

Replace the single English content constant with:

```python
from site_locales import SUPPORTED_LOCALES, alternates_for, canonical_url, output_path, route_for

CONTENT_DIR = PUBLIC / "i18n" / "products"


def content_path(locale):
    return CONTENT_DIR / f"{locale}.json"


def parse_locales(values):
    locales = tuple(values) if values else SUPPORTED_LOCALES
    unknown = sorted(set(locales) - set(SUPPORTED_LOCALES))
    if unknown:
        raise ValueError("Unsupported locale: " + ", ".join(unknown))
    return locales
```

Use `argparse` with repeatable `--locale`. `python build-product-pages.py --locale en` must build English only; no argument must build all seven locales.

- [ ] **Step 4: Render locale-specific shell metadata and routes**

Pass these values into the existing shell renderer:

```python
route = {
    "canonical": canonical_url(locale, page_key),
    "canonical_path": route_for(locale, page_key),
    "contact": f"{route_for(locale, 'contact')}?product={product_id}",
    "home": route_for(locale, "home"),
    "about": route_for(locale, "about"),
    "psa": route_for(locale, "psa"),
    "cabinet": route_for(locale, "cabinet"),
    "valve": route_for(locale, "valve"),
    "comparison": route_for(locale, "comparison"),
    "hreflangs": render_hreflangs(alternates_for(page_key)),
    "og_image": image_url,
}
```

Change `build_schema` to accept `locale`; set every applicable `inLanguage` to that locale and localize breadcrumb labels from the content file.

- [ ] **Step 5: Prove the English output still passes**

Run: `python build-product-pages.py --locale en`

Run: `python -m unittest -v tests.test_product_expansion`

Expected: all existing English product facts, CTA rules, media ownership, and schema tests pass.

- [ ] **Step 6: Commit**

```powershell
git add build-product-pages.py tests/test_product_expansion.py tests/test_multilingual_sales_path.py public/products
git commit -m "feat: make product generation locale-aware"
```

---

### Task 4: Add deterministic About and Contact generation

**Files:**
- Create: `build-static-core-pages.py`
- Create: `public/core-page-templates/about.html`
- Create: `public/core-page-templates/contact.html`
- Create: `public/i18n/core/en.json`
- Modify: `tests/test_inquiry_form_markup.py`
- Modify: `tests/test_multilingual_sales_path.py`

- [ ] **Step 1: Add failing English rendering tests**

Assert that a temporary render of the English About and Contact templates:

- has no unresolved placeholders;
- produces exactly one H1;
- has seven language options;
- uses all English translation keys exactly once unless a key is explicitly marked reusable;
- preserves all current Contact form names and product IDs;
- includes `/inquiry-form.js` and same-origin `action="/api/inquiry"`;
- contains no Web3Forms URL or access key.

- [ ] **Step 2: Run the rendering tests and verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.StaticCoreRendererTests`

Expected: renderer and templates do not exist.

- [ ] **Step 3: Extract the approved English pages into templates and data**

Create `public/i18n/core/en.json` with these top-level keys:

```json
{
  "locale": "en",
  "shared": {
    "language_label": "EN",
    "home": "Home",
    "products": "Products",
    "applications": "Applications",
    "results": "Cutting Results",
    "resources": "Resources",
    "about": "About",
    "request": "Request a Solution"
  },
  "about": {
    "title": "About GasMixTech",
    "description": "Jinan Euchio Machinery Co., Ltd. coordinates laser-cutting assist-gas equipment selection, application review, delivery and support for overseas industrial customers."
  },
  "contact": {
    "title": "Contact a Laser Cutting Gas Mixer Supplier in China",
    "description": "Send the machine, material, gas-source and installation conditions for a laser-cutting assist-gas application review."
  }
}
```

Continue the `about` and `contact` objects with every visible string from the approved English pages. The templates retain stable field names, IDs, data attributes, URLs, product IDs, company name, phone numbers, and email address; only visible copy and localized metadata become placeholders.

- [ ] **Step 4: Implement a fail-closed renderer**

`build-static-core-pages.py` must expose:

```python
def load_content(locale):
    return json.loads((CONTENT_DIR / f"{locale}.json").read_text(encoding="utf-8"))


def render_page(locale, page_key, template_text, content):
    rendered = render_template(template_text, content, locale=locale, page_key=page_key)
    if "{{" in rendered or "}}" in rendered:
        raise ValueError(f"{locale}/{page_key}: unresolved placeholder")
    return rendered


def build_locale(locale):
    content = load_content(locale)
    for page_key in ("about", "contact"):
        destination = output_path(PUBLIC, locale, page_key)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_page(locale, page_key, template_text(page_key), content), encoding="utf-8")
```

Generate language switcher URLs and `hreflang` through `site_locales.py`. Do not duplicate route logic in the renderer. Add `argparse` handling with repeatable `--locale`, the same validation behavior as the product builder, and all seven locales as the no-argument default.

- [ ] **Step 5: Generate English and run security/form regression tests**

Run: `python build-static-core-pages.py --locale en`

Run: `python -m unittest -v tests.test_inquiry_form_markup tests.test_multilingual_sales_path.StaticCoreRendererTests`

Expected: form structure, field names, honeypot, consent, scripts, and API action remain unchanged.

- [ ] **Step 6: Commit**

```powershell
git add build-static-core-pages.py public/core-page-templates public/i18n/core/en.json public/about.html public/contact.html tests/test_inquiry_form_markup.py tests/test_multilingual_sales_path.py
git commit -m "feat: generate shared about and contact pages"
```

---

### Task 5: Add the six professional translation datasets

**Files:**
- Modify: `public/i18n/{zh,es,pt,ja,ko,pl}.json`
- Create: `public/i18n/core/{zh,es,pt,ja,ko,pl}.json`
- Create: `public/i18n/products/{zh,es,pt,ja,ko,pl}.json`
- Modify: `tests/test_multilingual_sales_path.py`

- [ ] **Step 1: Add data-shape and invariant tests before translating**

Recursively compare every localized JSON file with its English counterpart:

```python
def leaf_paths(value, prefix=""):
    if isinstance(value, dict):
        result = set()
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            result.update(leaf_paths(child, child_prefix))
        return result
    if isinstance(value, list):
        result = set()
        for index, child in enumerate(value):
            result.update(leaf_paths(child, f"{prefix}.{index}"))
        return result
    return {prefix}
```

Assert equal leaf paths, list lengths, product IDs, model names, URLs, email/phone values, and technical `value` fields. Reject control characters, unresolved placeholders, legacy LISHI strings, and English-only UI labels outside an allowlist of proper names and technical abbreviations.

- [ ] **Step 2: Run the translation-data tests and verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.TranslationDataTests`

Expected: the six core and product translation files are missing and existing homepage strings fail selected terminology checks.

- [ ] **Step 3: Apply the locked industrial glossary**

Use these preferred terms consistently:

| Concept | ZH | ES | PT | JA | KO | PL |
|---|---|---|---|---|---|---|
| assist gas | 辅助气体 | gas de asistencia | gás de assistência | アシストガス | 보조 가스 | gaz pomocniczy |
| PSA nitrogen generation system | PSA 制氮系统 | sistema PSA de generación de nitrógeno | sistema PSA de geração de nitrogênio | PSA窒素発生システム | PSA 질소 발생 시스템 | system wytwarzania azotu PSA |
| integrated gas mixing cabinet | 一体式混气柜 | armario integrado de mezcla de gases | gabinete integrado de mistura de gases | 一体型ガス混合キャビネット | 통합 가스 혼합 캐비닛 | zintegrowana szafa mieszania gazów |
| proportional valve | 比例阀 | válvula proporcional | válvula proporcional | 比例弁 | 비례 밸브 | zawór proporcjonalny |
| inlet pressure | 入口压力 | presión de entrada | pressão de entrada | 入口圧力 | 입구 압력 | ciśnienie wlotowe |
| flow rate | 流量 | caudal | vazão | 流量 | 유량 | natężenie przepływu |
| retrofit | 改造集成 | modernización | modernização | レトロフィット | 개조 통합 | modernizacja |

Preserve `GasMixTech`, `Jinan Euchio Machinery Co., Ltd.`, `MSPV2-4000`, model identifiers, N₂/O₂, numeric values, and measurement units.

- [ ] **Step 4: Complete one locale at a time and validate it**

For each locale in this exact order—`zh`, `es`, `pt`, `ja`, `ko`, `pl`—complete all three data files, then run its exact command block below.

```powershell
node public/build-i18n.js --locale zh
python build-static-core-pages.py --locale zh
python build-product-pages.py --locale zh
python -m unittest -v tests.test_multilingual_sales_path.TranslationDataTests

node public/build-i18n.js --locale es
python build-static-core-pages.py --locale es
python build-product-pages.py --locale es
python -m unittest -v tests.test_multilingual_sales_path.TranslationDataTests

node public/build-i18n.js --locale pt
python build-static-core-pages.py --locale pt
python build-product-pages.py --locale pt
python -m unittest -v tests.test_multilingual_sales_path.TranslationDataTests

node public/build-i18n.js --locale ja
python build-static-core-pages.py --locale ja
python build-product-pages.py --locale ja
python -m unittest -v tests.test_multilingual_sales_path.TranslationDataTests

node public/build-i18n.js --locale ko
python build-static-core-pages.py --locale ko
python build-product-pages.py --locale ko
python -m unittest -v tests.test_multilingual_sales_path.TranslationDataTests

node public/build-i18n.js --locale pl
python build-static-core-pages.py --locale pl
python build-product-pages.py --locale pl
python -m unittest -v tests.test_multilingual_sales_path.TranslationDataTests
```

Run only the matching four commands after completing a locale. Do not create a page containing copied English paragraphs merely to satisfy key parity.

- [ ] **Step 5: Commit each complete locale independently**

Use these exact commit messages after the locale-specific tests pass:

```text
content(i18n): add Chinese core sales path
content(i18n): add Spanish core sales path
content(i18n): add Portuguese core sales path
content(i18n): add Japanese core sales path
content(i18n): add Korean core sales path
content(i18n): add Polish core sales path
```

Each commit includes that locale's three data files and generated seven-page output only.

---

### Task 6: Add one deterministic full build command

**Files:**
- Create: `build-core-locales.py`
- Modify: `public/build-i18n.js`
- Modify: `README.md`
- Modify: `tests/test_multilingual_sales_path.py`

- [ ] **Step 1: Add an orchestration test**

Patch `subprocess.run` in a unit test, invoke `build-core-locales.main()`, and assert that the ordered stages are:

```python
EXPECTED_STAGES = (
    "homepages",
    "about-contact",
    "products",
    "integrity-check",
)
```

Make the mocked third stage raise `subprocess.CalledProcessError`; assert that the exception propagates and every later stage remains uncalled.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.BuildOrchestrationTests`

Expected: `build-core-locales.py` does not exist.

- [ ] **Step 3: Implement the orchestrator**

Use `subprocess.run(..., check=True)` with argument arrays, never shell strings:

```python
STAGES = (
    ("homepages", (NODE, str(ROOT / "public" / "build-i18n.js"))),
    ("about-contact", (PYTHON, str(ROOT / "build-static-core-pages.py"))),
    ("products", (PYTHON, str(ROOT / "build-product-pages.py"))),
    ("integrity-check", (PYTHON, "-m", "unittest", "-v", "tests.test_multilingual_sales_path")),
)
```

Remove the direct `stabilize-core-locales.py` invocation from `public/build-i18n.js`. The new orchestrator is the sole documented core-HTML build entry point here; Task 8 adds the sitemap/LLM stage after its generator has been migrated to the new route contract.

- [ ] **Step 4: Document the build contract**

Update `README.md` with:

```powershell
python build-core-locales.py
python -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.mjs
```

State that maintained locales are EN, ZH, ES, PT, JA, KO, and PL. Do not modify the untracked project-level `AGENTS.md` from another working tree.

- [ ] **Step 5: Run and commit**

Run: `python build-core-locales.py`

Expected: all four stages pass.

```powershell
git add build-core-locales.py public/build-i18n.js README.md tests/test_multilingual_sales_path.py
git commit -m "build: add deterministic multilingual core build"
```

---

### Task 7: Withdraw legacy localized pages and add explicit redirects

**Files:**
- Delete: the 36 localized files listed in Planned File Structure
- Modify: `public/_redirects`
- Modify: `tests/test_multilingual_core.py`
- Modify: `tests/test_multilingual_sales_path.py`

- [ ] **Step 1: Pause for explicit deletion confirmation**

Before deleting, present the six language directories and the six filenames per directory. State that English pages remain and every removed route will receive a permanent English redirect. Continue only after the user explicitly confirms this 36-file deletion.

- [ ] **Step 2: Add failing redirect tests**

Parse `_redirects` and assert these mappings:

```python
LEGACY_PAGE_TARGETS = {
    "compatibility.html": "/compatibility.html",
    "parameters.html": "/parameters",
    "payment.html": "/payment.html",
    "privacy.html": "/privacy.html",
    "roi.html": "/roi.html",
    "404.html": "/",
}
```

For every supported non-English locale, require exact 301 rules for each legacy page. For every unsupported locale, require explicit 301 rules for `/LOCALE/about`, `/LOCALE/contact`, and each of the four `/LOCALE/products/...` routes to its English equivalent, followed by `/LOCALE`, `/LOCALE/`, and `/LOCALE/*` fallbacks to `/`. Do not rely on wildcard substitution to strip a locale prefix.

- [ ] **Step 3: Verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.RedirectContractTests`

Expected: localized non-core files still exist and exact redirect rules are absent.

- [ ] **Step 4: Delete only the confirmed files**

Use `git rm` with explicit literal paths. Before running it, resolve each target and verify that every resolved path remains below this isolated worktree's `public/{locale}/` directory. Do not use recursive deletion or globs.

- [ ] **Step 5: Add ordered redirect rules**

Place exact page redirects before language catch-alls. The required ordering is:

1. supported-locale legacy page → English equivalent;
2. unsupported-locale known core route → English equivalent;
3. unsupported-locale catch-all → `/`.

Keep all supported core routes outside redirect patterns. Include `/ar`, `/ar/`, and `/ar/*` as an existing defensive redirect even though Arabic is not a supported or current source locale.

- [ ] **Step 6: Run redirect and matrix tests**

Run: `python -m unittest -v tests.test_multilingual_sales_path.RedirectContractTests tests.test_multilingual_sales_path.GeneratedMatrixTests`

Expected: 49 core pages exist, 36 legacy files are absent, and all redirect assertions pass.

- [ ] **Step 7: Commit**

```powershell
git add public/_redirects tests/test_multilingual_core.py tests/test_multilingual_sales_path.py
git commit -m "fix: withdraw stale localized routes"
```

The deletion paths staged by `git rm` must be included in the same commit.

---

### Task 8: Rebuild canonical, hreflang, sitemap, LLM, and search artifacts

**Files:**
- Modify: `generate-sitemap-geo.py`
- Modify: `build-core-locales.py`
- Regenerate: `public/sitemap.xml`
- Regenerate: `public/llms.txt`
- Regenerate: `public/llms-full.txt`
- Regenerate: `public/llms-{en,zh,es,pt,ja,ko,pl}.txt`
- Regenerate: `public/pagefind/**`
- Modify: `tests/test_seo_geo.py`
- Modify: `tests/test_multilingual_sales_path.py`

- [ ] **Step 1: Add failing SEO matrix tests**

For all 49 core pages assert:

```python
expected_hreflangs = set(SUPPORTED_LOCALES) | {"x-default"}
self.assertEqual(set(parsed.hreflangs), expected_hreflangs)
self.assertEqual(parsed.canonical, canonical_url(locale, page_key))
self.assertEqual(parsed.html_lang, locale)
self.assertEqual(parsed.hreflangs["x-default"], canonical_url("en", page_key))
```

Parse sitemap XML and require exactly the 49 core URLs in reciprocal alternate clusters, while allowing current English-only blog and case-study URLs as separate non-clustered entries. Reject unsupported-language prefixes and removed localized non-core URLs.

For every core page, also assert that the title and meta description are non-empty and localized, no other core page in the same language reuses the same pair, no `LISHI` text remains, and every same-site core link resolves to one of the 49 generated files. English-only resource links are allowed only when their existing English target file is present.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest -v tests.test_multilingual_sales_path.SeoMatrixTests`

Expected: localized product alternates and the revised sitemap matrix are missing.

- [ ] **Step 3: Update sitemap and LLM generation**

Import the route contract from `site_locales.py`. Replace filename-based `LOCALIZED_PAGES` logic with the seven `CORE_ROUTES` keys. Generate every alternate from `alternates_for(page_key)` and exclude redirected URLs.

Update discovery copy to state exactly:

```text
English, Simplified Chinese, Spanish, Portuguese, Japanese, Korean, and Polish core sales pages are maintained. Technical articles, ROI, parameters, compatibility, payment, and privacy resources are maintained in English.
```

Then add this fourth generation stage to `build-core-locales.py`, immediately before `integrity-check`, and update `BuildOrchestrationTests` to expect five stages:

```python
("sitemap-llms", (PYTHON, str(ROOT / "generate-sitemap-geo.py"))),
```

- [ ] **Step 4: Generate sitemap and LLM files**

Run: `python generate-sitemap-geo.py`

Expected: exit code 0, 49 clustered core URLs, no unsupported locale URL, and no removed localized non-core URL.

- [ ] **Step 5: Rebuild Pagefind 1.5.2**

First run: `npx pagefind@1.5.2 --version`

If this would install or download Pagefind, stop and obtain dependency-install confirmation before continuing. After confirmation or when already available, run:

`npx pagefind@1.5.2 --site public`

Expected: exit code 0; language metadata only for `en`, `zh`, `es`, `pt`, `ja`, `ko`, and `pl`; no unsupported language index remains.

- [ ] **Step 6: Run SEO tests and commit**

Run: `python -m unittest -v tests.test_seo_geo tests.test_multilingual_sales_path.SeoMatrixTests`

Expected: all tests pass.

```powershell
git add generate-sitemap-geo.py build-core-locales.py public/sitemap.xml public/llms*.txt public/pagefind tests/test_seo_geo.py tests/test_multilingual_sales_path.py
git commit -m "feat: publish seven-language discovery metadata"
```

---

### Task 9: Verify inquiry localization without changing the backend

**Files:**
- Modify: `tests/test_inquiry_form_markup.py`
- Modify: `tests/test_multilingual_sales_path.py`
- No planned changes: `functions/api/inquiry.js`
- No planned changes: `workers/inquiry-mailer/src/index.mjs`

- [ ] **Step 1: Add localized form-copy assertions**

For each locale verify that the Contact page includes localized values for:

- all three step legends;
- product and recommendation options;
- PSA and mixer field labels;
- material, gas, installation, customer-type, and contact-channel options;
- consent, validation, submitting, success, failure, and reference text.

Keep these exact machine values across every locale:

```python
PRODUCT_IDS = {
    "psa-nitrogen-system",
    "integrated-mixing-cabinet",
    "mspv2-4000",
    "need-recommendation",
}
```

- [ ] **Step 2: Add a backend immutability check**

Use these implementation-start Git blob IDs as immutable references:

```text
functions/api/inquiry.js: 78668c319f498188b56e0ba5808818b5cb6c98fa
workers/inquiry-mailer/src/index.mjs: 7131347938d066f8e21929d22554874dcd2a0ab0
```

Re-read them after frontend implementation:

```powershell
git rev-parse HEAD:./functions/api/inquiry.js
git rev-parse HEAD:./workers/inquiry-mailer/src/index.mjs
```

They must remain equal to the values above. If a frontend test exposes a real backend defect, stop and request a scope decision instead of changing backend code.

- [ ] **Step 3: Run all form and backend tests**

Run: `python -m unittest -v tests.test_inquiry_form_markup`

Run: `node --test tests/*.test.mjs`

Expected: localized form tests pass and all 25 backend/security tests still pass.

- [ ] **Step 4: Commit test improvements**

```powershell
git add tests/test_inquiry_form_markup.py tests/test_multilingual_sales_path.py
git commit -m "test: verify localized inquiry journeys"
```

---

### Task 10: Run complete local verification and visual QA

**Files:**
- No planned source changes; fix only failures directly attributable to Tasks 1–9.

- [ ] **Step 1: Verify deterministic generation**

First require a clean implementation worktree with `git status --short`. Then run `python build-core-locales.py`, followed by:

```powershell
git diff --exit-code -- public README.md
```

Expected: the build succeeds and produces no tracked diff, proving a repeat run is deterministic.

- [ ] **Step 2: Run the complete automated suite**

Run: `python -m unittest discover -s tests -p 'test_*.py'`

Expected: all Python tests pass with zero failures and zero errors.

Run: `node --test tests/*.test.mjs`

Expected: all 25 Node tests pass.

- [ ] **Step 3: Inspect repository integrity**

Run: `git diff --check`

Run: `git status --short --branch`

Expected: no whitespace errors, no untracked generated files, and no unrelated source changes.

- [ ] **Step 4: Start a local server**

Run in a persistent terminal:

`python -m http.server 8123 --directory public`

If port 8123 is occupied, stop and report the owning process instead of silently changing ports. Otherwise, expect `http://localhost:8123/` to load without a 404 or 500 response.

- [ ] **Step 5: Run the route smoke matrix**

Check all 49 core routes at desktop width and verify each returns the expected localized page. At minimum, visually inspect every language homepage, all four localized product pages, About, and Contact.

- [ ] **Step 6: Run responsive visual checks**

At desktop and mobile widths, inspect:

- header alignment and product dropdown;
- language labels and current-language state;
- hero wrapping and CTA rows;
- specification cards and comparison-table overflow;
- Japanese, Korean, Polish, and Portuguese long-line wrapping;
- footer columns;
- three-step inquiry form layout, validation, Back/Continue behavior, and success/failure containers;
- browser console errors.

- [ ] **Step 7: Verify switching preserves the current page**

Test at least these mappings in both directions:

```text
/es/products/mspv2-4000-proportional-valve ↔ /ja/products/mspv2-4000-proportional-valve
/zh/contact ↔ /contact
/pt/products/mixed-gas-control-comparison ↔ /pl/products/mixed-gas-control-comparison
```

- [ ] **Step 8: Commit only direct QA fixes**

If visual QA requires CSS or copy corrections, make surgical changes, rerun Steps 1–7, and commit:

```powershell
git add public/styles.css public/styles.min.css public/i18n public/core-page-templates tests
git commit -m "fix: polish multilingual sales layouts"
```

Do not create this commit when no QA fix is needed.

---

### Task 11: Prepare the preview release and PR

**Files:**
- No planned content changes after verification.

- [ ] **Step 1: Present local verification evidence**

Report:

- Python test count and result;
- Node test count and result;
- 49-route matrix result;
- Pagefind language/page counts;
- redirect-test result;
- desktop/mobile browser result;
- final commit list;
- exact diff summary.

- [ ] **Step 2: Obtain explicit preview-deployment confirmation**

State that the next command creates a public Cloudflare Pages preview but does not change `gasmixtech.com`. Continue only after the user confirms.

- [ ] **Step 3: Deploy the preview**

Run:

`npx wrangler pages deploy public --project-name lishi-laser-website --branch feat-multilingual-core-sales-path`

Expected: Cloudflare returns one unique preview URL and the deployment succeeds.

- [ ] **Step 4: Verify preview behavior**

Check the preview homepage, all 49 core routes, representative redirects, language switching, and `/api/inquiry` GET behavior. Expected API GET response is `405 Method Not Allowed` with `Allow: POST`.

- [ ] **Step 5: Obtain immediate confirmation before a preview email test**

Prepare one fictional non-English inquiry clearly marked `PREVIEW TEST`. Before clicking Submit, identify that it will send to `sales@gasmixtech.com` and request confirmation. Submit once only after confirmation.

- [ ] **Step 6: Push and open a PR only after confirmation**

Present the branch name, commits, remote repository, and PR scope. After confirmation:

```powershell
git push -u origin feat/multilingual-core-sales-path
gh pr create --fill --base main --head feat/multilingual-core-sales-path
```

Do not merge the PR or deploy production in this task. Those actions require a separate production confirmation after the user approves the preview.

---

## Final Acceptance Checklist

- [ ] Exactly seven maintained languages are advertised: EN, ZH, ES, PT, JA, KO, PL.
- [ ] Exactly 49 core sales-path URLs exist.
- [ ] All 42 non-English core pages use professional localized copy.
- [ ] Every supported-language core link remains in the selected language.
- [ ] Language switching preserves the current page.
- [ ] Cabinet and MSPV2-4000 remain alternatives with the same core function.
- [ ] Technical values, model names, URLs, product IDs, and company identity match English.
- [ ] No legacy LISHI copy or unsupported commercial claim remains in the maintained localized path.
- [ ] The 36 obsolete localized utility pages are absent after explicit confirmation and redirect correctly.
- [ ] Unsupported language paths redirect to English without loops.
- [ ] Canonical, `hreflang`, sitemap, JSON-LD, LLM, and Pagefind checks pass.
- [ ] The inquiry backend files and Cloudflare email configuration remain unchanged.
- [ ] Full Python and Node test suites pass.
- [ ] Desktop and mobile visual checks pass.
- [ ] The preview is approved before any production merge or deployment.
