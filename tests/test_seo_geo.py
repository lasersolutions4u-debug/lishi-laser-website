import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

from site_locales import (
    CORE_ROUTES,
    DOMAIN,
    SUPPORTED_LOCALES,
    UNSUPPORTED_LOCALES,
    alternates_for,
    canonical_url,
)


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CORE = {
    "index.html": (
        "Laser Cutting Assist-Gas Systems | GasMixTech",
        "Build the assist-gas system around your laser process",
        "Configure on-site nitrogen supply and select one N₂/O₂ mixed-gas controller for a reviewed laser cutting application.",
    ),
    "about.html": (
        "Gas Mixing Device Supplier in China | About Us",
        "A China-Based Gas Mixing Device Supplier and Solution Provider",
        "Learn how Jinan Euchio Machinery Co., Ltd. supports laser-cutting gas mixer selection, integration, delivery, and after-sales coordination from China.",
    ),
    "compatibility.html": (
        "Laser Cutting Gas Mixer Compatibility Guide",
        "Check Laser Cutting Gas Mixer Compatibility",
        "Check whether a fiber laser, material, thickness range, gas supply, pressure, and flow requirements are suitable for a laser cutting gas mixer.",
    ),
    "parameters.html": (
        "Gas Mixer for Laser Cutting: Ratios & Parameters",
        "Gas Mixer Ratios and Laser Cutting Parameters",
        "Review reference gas ratios and laser cutting parameters with the process conditions needed before applying them to another machine or material.",
    ),
    "roi.html": (
        "Laser Cutting Gas Mixer ROI & Cost Factors",
        "Evaluate Laser Cutting Gas Mixer ROI",
        "Evaluate laser cutting gas mixer ROI using gas consumption, cycle time, edge finishing, labor, utilization, and local operating costs.",
    ),
    "payment.html": (
        "How to Buy a Gas Mixer from China | Payment Guide",
        "How to Buy a Gas Mixer from China",
        "Understand how to buy a gas mixer from China, including assessment, quotation, proforma invoice, bank verification, payment, and delivery coordination.",
    ),
    "contact.html": (
        "Contact a Laser Cutting Gas Mixer Supplier in China",
        "Discuss Your Laser Cutting Gas Mixing Requirements",
        "Contact a China-based laser cutting gas mixer supplier for compatibility assessment, selection support, integration questions, and quotation.",
    ),
    "privacy.html": (
        "Privacy Policy | GasMixTech",
        "Privacy Policy",
        "Read the GasMixTech privacy policy and learn how inquiry and website data are collected, used, and protected.",
    ),
    "404.html": (
        "Page Not Found | GasMixTech",
        "Page Not Found",
        "The requested GasMixTech page could not be found. Return to the laser cutting gas mixer guide or contact the supplier for help.",
    ),
}
ACTIVE_LANGS = SUPPORTED_LOCALES
REMOVED_LANGS = (*UNSUPPORTED_LOCALES, "ar")
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
DISCOVERY_SCOPE = (
    "English, Simplified Chinese, Spanish, Portuguese, Japanese, Korean, and Polish "
    "core sales pages are maintained. Technical articles, ROI, parameters, "
    "compatibility, payment, and privacy resources are maintained in English."
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
            title, h1, description = CORE[filename]
            with self.subTest(filename=filename):
                page = parse(PUBLIC / filename)
                self.assertEqual(page.title, title)
                self.assertEqual(page.h1, h1)
                self.assertEqual(page.meta.get("description"), description)

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
            "privacy.html": set(),
            "404.html": set(),
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
        ns = {
            "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        entries = {}
        for node in tree.findall("s:url", ns):
            loc = node.findtext("s:loc", namespaces=ns)
            alternates = {
                link.attrib["hreflang"]: link.attrib["href"]
                for link in node.findall("xhtml:link", ns)
            }
            entries[loc] = alternates

        expected_core = {
            canonical_url(locale, page_key)
            for locale in SUPPORTED_LOCALES
            for page_key in CORE_ROUTES
        }
        clustered = {url for url, alternates in entries.items() if alternates}
        self.assertEqual(clustered, expected_core)
        self.assertEqual(len(clustered), 49)
        for locale in SUPPORTED_LOCALES:
            for page_key in CORE_ROUTES:
                url = canonical_url(locale, page_key)
                with self.subTest(locale=locale, page_key=page_key):
                    self.assertEqual(entries[url], alternates_for(page_key))

        standalone = set(entries) - expected_core
        expected_standalone = set()
        for directory in ("blog", "case-studies"):
            for path in (PUBLIC / directory).rglob("*.html"):
                page = parse(path)
                if "noindex" in page.meta.get("robots", "").casefold():
                    continue
                relative = path.relative_to(PUBLIC).as_posix()
                if relative.endswith("/index.html"):
                    expected_standalone.add(f"{DOMAIN}/{relative[:-10]}")
                else:
                    expected_standalone.add(f"{DOMAIN}/{relative}")
        self.assertEqual(standalone, expected_standalone)
        self.assertTrue(all(not entries[url] for url in standalone))

        locs = list(entries)
        self.assertFalse(any("privacy" in loc or "404" in loc for loc in locs))
        self.assertFalse(any(f"/{lang}/" in loc for lang in REMOVED_LANGS for loc in locs))
        for locale in SUPPORTED_LOCALES[1:]:
            for legacy in ("compatibility", "parameters", "roi", "payment", "privacy", "404"):
                self.assertFalse(any(f"/{locale}/{legacy}" in loc for loc in locs))
        self.assertEqual(tree.findall("s:url/s:lastmod", ns), [])

    def test_discovery_files_state_exact_maintained_scope(self):
        filenames = ("llms.txt", "llms-full.txt") + tuple(
            f"llms-{locale}.txt" for locale in SUPPORTED_LOCALES
        )
        for filename in filenames:
            with self.subTest(filename=filename):
                content = (PUBLIC / filename).read_text(encoding="utf-8")
                self.assertIn(DISCOVERY_SCOPE, content)
                self.assertNotIn("LISHI", content.upper())

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

    def test_legacy_privacy_generator_is_disabled(self):
        content = (PUBLIC / "build-privacy.js").read_text(encoding="utf-8")
        self.assertIn("LEGACY PRIVACY GENERATOR DISABLED", content)
        self.assertIn("throw new Error", content)

    def test_blog_and_case_metadata_do_not_present_a_product_brand(self):
        paths = list((PUBLIC / "blog").glob("*.html"))
        paths += list((PUBLIC / "case-studies").glob("*.html"))
        for path in paths:
            page = parse(path)
            metadata = f"{page.title}\n{page.meta.get('description', '')}".casefold()
            self.assertNotIn("euchio mixed gas", metadata, path)
            self.assertNotIn("sagemro mixed gas", metadata, path)

    def test_english_content_uses_neutral_site_identity_and_no_exclusivity_claims(self):
        paths = [PUBLIC / "index.html", PUBLIC / "_template.html"]
        paths += list((PUBLIC / "blog").glob("*.html"))
        paths += list((PUBLIC / "case-studies").glob("*.html"))
        forbidden = (
            "euchio mixed gas",
            "euchio gas mixing equipment",
            "one euchio mixing station",
            "every euchio device",
            "the euchio route",
            "1 × euchio",
            "only multi-machine gas solution",
            "only solution",
            "euchio gas mixing technology",
            "only option that consistently",
            "euchio mixing station",
        )
        for path in paths:
            content = path.read_text(encoding="utf-8").casefold()
            with self.subTest(path=path):
                for phrase in forbidden:
                    self.assertNotIn(phrase, content)
                self.assertNotRegex(
                    content,
                    r'<span class="logo-brand">\s*euchio\s*</span>',
                )

    def test_comparison_and_faq_articles_avoid_unqualified_superlatives(self):
        paths = (
            PUBLIC / "blog" / "mixed-gas-vs-oxygen-comparison.html",
            PUBLIC / "blog" / "laser-cutting-gas-faq.html",
        )
        forbidden = (
            "only option that consistently",
            "best all-around",
            "fastest cutting speed",
            "cleanest edge",
            "lowest total operating cost",
            "lowest total cost of ownership",
            "2.5–7×",
            "2.5× to 7×",
            "zero burrs",
            "near-zero electricity",
            "consistently cuts",
            "maintenance and contamination risks entirely",
        )
        for path in paths:
            content = path.read_text(encoding="utf-8").casefold()
            with self.subTest(path=path):
                for phrase in forbidden:
                    self.assertNotIn(phrase, content)

    def test_english_guides_avoid_unqualified_roi_and_performance_promises(self):
        forbidden = (
            "near-zero electricity",
            "recoup their investment within",
            "payback is typically",
            "typically under 6 months",
            "lowest total cost across the board",
            "eliminates that cost entirely",
            "eliminates the grinding bottleneck entirely",
            "3× faster cutting with burr-free",
            "2.5-7× faster cutting",
            "2.5-7× speed increase",
            "33% less nitrogen",
            "127% above the world average",
            "model your exact savings",
            "pays for itself within",
            "after that, it's pure profit",
            "mixed gas users report 30–35%",
            "reduces nitrogen consumption by roughly 33%",
            "every installation we've done",
            "mixed gas eliminates burrs",
            "mixed gas 2.5–5× faster",
            "annual profit increase</td>",
            "optimized cutting on <em>every</em> material",
            "3x different output",
            "burr-free edges are achievable",
            "better choice on every metric",
            "no laser modifications required",
            "takes 1–2 hours",
            "cuts nitrogen consumption by 33%",
            "advantage is largest at 4–16mm",
            "2 kwh/day consumption vs a compressor's 240+ kwh/day",
            "effectively multiplies your existing laser capacity",
            "show you exactly what switching would save",
            "solves all three problems",
            "accelerate cutting by 30-50%",
            "zero oil or moisture",
            "comes out ahead for any shop",
            "case for mixed gas is overwhelming",
            "all respond well to mixed gas",
            "measurable improvements on stainless and aluminum starting at 6kw",
            "sweet spot is 12kw",
            "thousands of sheet metal fabricators",
            "the gas is the ceiling",
            "mixed gas removes that ceiling",
            "the data doesn't lie",
            "they're using better gas",
            "40-60% of their laser's true capability",
        )
        for path in (PUBLIC / "blog").glob("*.html"):
            content = path.read_text(encoding="utf-8").casefold()
            with self.subTest(path=path):
                for phrase in forbidden:
                    self.assertNotIn(phrase, content)

    def test_rewritten_comparison_guides_do_not_publish_hidden_faq_schema(self):
        for filename in (
            "assist-gas-complete-guide.html",
            "nitrogen-vs-mixed-gas-comparison.html",
        ):
            path = PUBLIC / "blog" / filename
            page = parse(path)
            values = [json.loads(raw) for raw in page.jsonld]
            types = set().union(*(schema_types(value) for value in values))
            self.assertNotIn("FAQPage", types, path)

    def test_homepage_generation_sources_are_safe_to_rebuild(self):
        template = (PUBLIC / "_template.html").read_text(encoding="utf-8").casefold()
        sources = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in (PUBLIC / "i18n").glob("*.json")
        ]
        en_source = json.loads((PUBLIC / "i18n" / "en.json").read_text(encoding="utf-8"))
        en_serialized = json.dumps(en_source, ensure_ascii=False).casefold()
        serialized = json.dumps(sources, ensure_ascii=False).casefold()
        for phrase in (
            "euchio gas mixing equipment",
            '<span class="logo-brand">euchio</span>',
            "real cutting speed data from end users worldwide",
            "$2,000+/year",
            "$5,000-50,000",
            "optimal carbon steel cutting thickness range",
            "no embellishment",
            "zero compromise",
            "zero burn-through",
            'data-target="20"',
            "continents deployed",
            "production endurance",
            "\n              euchio\n",
        ):
            self.assertNotIn(phrase, template + "\n" + en_serialized)
        for phrase in (
            "euchio mixed gas",
            "euchio混合气",
            "euchio gas mixto",
            "euchio 혼합",
            "euchio混合ガス",
            "euchio gás misto",
        ):
            self.assertNotIn(phrase, serialized)

        locale_risk_phrases = (
            "提升3倍", "3× más rápido", "3× faster", "3倍速", "3x mais rápido",
            "33%", "33–50%", "33~50%", "33〜50%",
            "100%安全", "100% seguro", "100% safe",
            "distribuidor exclusivo", "독점 유통",
            "一台设备可同时支持最多三台", "un equipo admite hasta tres máquinas láser simultáneamente",
            "하나의 장치로 최대 세 대의 레이저 장비를 동시에 지원합니다",
            "1台の装置で最大3台のレーザー機を同時にサポートします",
            "um equipamento suporta simultaneamente até três máquinas laser",
            "メンテナンスフリーです", "24時間あたり2kwhだけです",
            "大洲已部署", "continentes desplegados", "전개된 대륙", "展開済み大陸", "continentes implementados",
            "$5,000-50,000", "$5,000–$50,000", "$5.000-50.000", "$5.000–$50.000",
        )
        for phrase in locale_risk_phrases:
            self.assertNotIn(phrase.casefold(), serialized)

    def test_blog_index_metadata_and_h1(self):
        page = parse(PUBLIC / "blog" / "index.html")
        self.assertEqual(page.title, "Laser Cutting Gas Mixer Guides | GasMixTech")
        self.assertEqual(page.h1, "Laser Cutting Gas Mixer Guides")
        self.assertEqual(
            page.meta.get("description"),
            "Read practical guides on laser cutting assist gases, gas mixer selection, compatibility, parameters, comparisons, and ROI evaluation.",
        )

    def test_article_schema_uses_legal_company_entity(self):
        paths = [path for path in (PUBLIC / "blog").glob("*.html") if path.name != "index.html"]
        paths += list((PUBLIC / "case-studies").glob("*.html"))
        for path in paths:
            page = parse(path)
            values = [json.loads(raw) for raw in page.jsonld]
            articles = []
            for value in values:
                nodes = value.get("@graph", []) if isinstance(value, dict) and "@graph" in value else [value]
                articles.extend(node for node in nodes if isinstance(node, dict) and node.get("@type") == "Article")
            self.assertTrue(articles, path)
            article = articles[0]
            self.assertEqual(article.get("author", {}).get("name"), "Jinan Euchio Machinery Co., Ltd.", path)
            self.assertEqual(article.get("publisher", {}).get("name"), "Jinan Euchio Machinery Co., Ltd.", path)
            self.assertEqual(article.get("dateModified"), "2026-08-05", path)

    def test_articles_offer_a_core_next_step(self):
        paths = [path for path in (PUBLIC / "blog").glob("*.html") if path.name != "index.html"]
        paths += list((PUBLIC / "case-studies").glob("*.html"))
        destinations = ("/compatibility.html", "/parameters", "/roi.html", "/contact", "/#samples")
        for path in paths:
            html = path.read_text(encoding="utf-8")
            self.assertTrue(any(f'href="{destination}"' in html for destination in destinations), path)

    def test_case_breadcrumbs_return_to_existing_samples_section(self):
        for path in (PUBLIC / "case-studies").glob("*.html"):
            html = path.read_text(encoding="utf-8")
            self.assertNotIn("https://gasmixtech.com/#case-studies", html, path)
            self.assertIn("https://gasmixtech.com/#samples", html, path)


if __name__ == "__main__":
    unittest.main()
