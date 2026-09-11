import html
import json
import re
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from site_locales import (
    CORE_ROUTES,
    LOCALIZED_LOCALES,
    SUPPORTED_LOCALES,
    UNSUPPORTED_LOCALES,
    output_path,
    route_for,
)


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
RETAINED_LANGS = SUPPORTED_LOCALES
REMOVED_LANGS = UNSUPPORTED_LOCALES + ("ar",)
LAUNCH_READY_LOCALIZED_LANGS = LOCALIZED_LOCALES
CORE_PAGES = tuple(CORE_ROUTES)
INDEXABLE_CORE_PAGES = CORE_PAGES
SWITCHER_CORE_PAGES = CORE_PAGES
COMPONENT_CLASSES = (
    "advantage-card",
    "brand-card",
    "params-card",
    "blog-post-card",
    "contact-method",
    "form-group",
    "form-row",
    "footer-links",
    "lang-option",
    "faq-item",
    "case-card",
)


def page_path(lang, page_key):
    return output_path(PUBLIC, lang, page_key)


class CorePageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors = []
        self.assets = []
        self.canonicals = []
        self.classes = Counter()
        self.form_fields = set()
        self.hreflangs = []
        self.lang_options = []
        self.ids = []
        self.section_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section":
            self.section_count += 1
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for class_name in attrs.get("class", "").split():
            self.classes[class_name] += 1
        if tag == "a" and attrs.get("href"):
            self.anchors.append(attrs["href"])
            if "lang-option" in attrs.get("class", "").split():
                self.lang_options.append((attrs.get("data-lang", ""), attrs["href"]))
        if tag in {"input", "select", "textarea"} and attrs.get("name"):
            self.form_fields.add(attrs["name"])
        if tag == "link":
            rel = attrs.get("rel", "")
            if rel == "canonical" and attrs.get("href"):
                self.canonicals.append(attrs["href"])
            if rel == "alternate" and attrs.get("hreflang"):
                self.hreflangs.append((attrs["hreflang"], attrs.get("href", "")))
            if "stylesheet" in rel and attrs.get("href"):
                self.assets.append(attrs["href"])
            if "preload" in rel and attrs.get("as") == "image" and attrs.get("href"):
                self.assets.append(attrs["href"])
        if tag == "img" and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "source" and attrs.get("srcset"):
            self.assets.extend(
                candidate.strip().split()[0]
                for candidate in attrs["srcset"].split(",")
                if candidate.strip()
            )
        if tag == "video" and attrs.get("poster"):
            self.assets.append(attrs["poster"])
        if tag == "script" and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "meta" and attrs.get("property") == "og:image" and attrs.get("content"):
            self.assets.append(attrs["content"])


def parse_page(path):
    parser = CorePageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def local_target(path, url):
    parsed = urlparse(url)
    if parsed.netloc == "gasmixtech.com":
        return PUBLIC / parsed.path.lstrip("/")
    if parsed.scheme or parsed.netloc or url.startswith(("//", "#", "mailto:", "tel:", "javascript:")):
        return None
    clean = parsed.path
    if not clean:
        return None
    return PUBLIC / clean.lstrip("/") if clean.startswith("/") else (path.parent / clean).resolve()


def target_exists(target, url):
    if target is None:
        return True
    if target.exists():
        return True
    parsed_path = urlparse(url).path
    if parsed_path.endswith("/") and (target / "index.html").exists():
        return True
    if not target.suffix and target.with_suffix(".html").exists():
        return True
    return not parsed_path


class MultilingualCoreTests(unittest.TestCase):
    def test_exact_core_page_matrix(self):
        for lang in RETAINED_LANGS:
            with self.subTest(lang=lang):
                for page_key in CORE_PAGES:
                    self.assertTrue(page_path(lang, page_key).is_file())
                if lang != "en":
                    actual = {
                        path.relative_to(PUBLIC / lang)
                        for path in (PUBLIC / lang).rglob("*.html")
                    }
                    expected = {
                        page_path(lang, page_key).relative_to(PUBLIC / lang)
                        for page_key in CORE_PAGES
                    }
                    self.assertEqual(actual, expected)

    def test_removed_language_directories_and_outputs_are_absent(self):
        for lang in REMOVED_LANGS:
            with self.subTest(lang=lang):
                self.assertFalse((PUBLIC / lang).exists())
                self.assertFalse((PUBLIC / f"llms-{lang}.txt").exists())
                pagefind_names = [path.name for path in (PUBLIC / "pagefind").rglob("*")]
                self.assertFalse(any(re.search(rf"(?:\.|_|wasm\.){lang}(?:_|\.|$)", name) for name in pagefind_names))

        removed_url = re.compile(rf"/(?:{'|'.join(REMOVED_LANGS)})/")
        for path in list(PUBLIC.rglob("*.html")) + [PUBLIC / "sitemap.xml", PUBLIC / "llms.txt", PUBLIC / "llms-full.txt"]:
            with self.subTest(path=path):
                self.assertNotRegex(path.read_text(encoding="utf-8"), removed_url)

    def test_removed_language_routes_redirect_to_english(self):
        redirects = (PUBLIC / "_redirects").read_text(encoding="utf-8").splitlines()
        rules = {line.strip() for line in redirects if line.strip() and not line.startswith("#")}
        for lang in REMOVED_LANGS:
            with self.subTest(lang=lang):
                self.assertIn(f"/{lang} / 301", rules)
                self.assertIn(f"/{lang}/ / 301", rules)
                self.assertIn(f"/{lang}/* / 301", rules)

    def test_component_counts_match_english(self):
        for filename in CORE_PAGES:
            expected = parse_page(page_path("en", filename))
            expected_counts = {name: expected.classes[name] for name in COMPONENT_CLASSES}
            for lang in RETAINED_LANGS[1:]:
                with self.subTest(lang=lang, filename=filename):
                    actual = parse_page(page_path(lang, filename))
                    self.assertEqual(actual.section_count, expected.section_count)
                    self.assertEqual(
                        {name: actual.classes[name] for name in COMPONENT_CLASSES},
                        expected_counts,
                    )

    def test_indexable_core_pages_have_full_language_switcher(self):
        expected_codes = set(RETAINED_LANGS)
        for lang in RETAINED_LANGS:
            for filename in SWITCHER_CORE_PAGES:
                with self.subTest(lang=lang, filename=filename):
                    parser = parse_page(page_path(lang, filename))
                    self.assertEqual(parser.classes["lang-option"], len(expected_codes))
                    self.assertEqual({code for code, _ in parser.lang_options}, expected_codes)

    def test_contact_form_fields_match_english(self):
        expected = parse_page(PUBLIC / "contact.html").form_fields
        self.assertTrue(expected)
        for lang in RETAINED_LANGS[1:]:
            with self.subTest(lang=lang):
                self.assertEqual(parse_page(page_path(lang, "contact")).form_fields, expected)

    def test_local_assets_resolve(self):
        broken = []
        for lang in RETAINED_LANGS:
            for filename in CORE_PAGES:
                path = page_path(lang, filename)
                for asset in parse_page(path).assets:
                    if not target_exists(local_target(path, asset), asset):
                        broken.append(f"{path.relative_to(PUBLIC)} -> {asset}")
        self.assertEqual(broken, [])

    def test_internal_links_resolve(self):
        broken = []
        for lang in RETAINED_LANGS:
            for filename in CORE_PAGES:
                path = page_path(lang, filename)
                for href in parse_page(path).anchors:
                    if not target_exists(local_target(path, href), href):
                        broken.append(f"{path.relative_to(PUBLIC)} -> {href}")
        self.assertEqual(broken, [])

    def test_localized_blog_links_use_english_blog(self):
        for lang in RETAINED_LANGS[1:]:
            for filename in CORE_PAGES:
                with self.subTest(lang=lang, filename=filename):
                    blog_links = [href for href in parse_page(page_path(lang, filename)).anchors if "/blog" in href]
                    self.assertTrue(all(href.startswith("/blog/") for href in blog_links), blog_links)

    def test_launch_ready_locales_do_not_keep_known_interface_leaks(self):
        leaked_phrases = (
            "Best for ≤2mm carbon steel",
            "Best for ≤6mm carbon steel",
            "Project owner / purchasing team",
            "Industrial equipment solutions and service for sheet metal processing",
            "Jinan, Shandong Province, China",
            "— maintenance, repair, spare parts, technical support",
            "重点市场区域合作伙伴名额开放申请。发一集装箱，建立您的市场。",
            "Asociaciones de distribuidor exclusivo disponibles en regiones selectas.",
            "선정 지역 독점 유통사 파트너십 공개.",
            "厳選された地域での独占流通パートナーシップ募集。",
            "Parcerias de distribuidor exclusivo disponíveis em regiões selecionadas.",
            "Dostępne są ekskluzywne partnerstwa dystrybucyjne w wybranych regionach.",
            "Szukasz dystrybutora?",
            "Request Assessment →",
        )
        for lang in LAUNCH_READY_LOCALIZED_LANGS:
            for filename in CORE_PAGES:
                with self.subTest(lang=lang, filename=filename):
                    content = page_path(lang, filename).read_text(encoding="utf-8")
                    for phrase in leaked_phrases:
                        self.assertNotIn(phrase, content)

    def test_polish_contact_page_has_no_legacy_mojibake(self):
        content = page_path("pl", "contact").read_text(encoding="utf-8")
        self.assertIn("Skontaktuj się", content)
        self.assertIn("Wyślij prośbę o ocenę</button>", content)
        self.assertIn('action="/api/inquiry"', content)
        self.assertNotRegex(content, r"[臋膮贸艂艣膰藕鈫娴庡閽板抄鏈烘漏偶]")

    def test_core_hreflang_set_is_exact(self):
        expected_codes = set(RETAINED_LANGS) | {"x-default"}
        for lang in RETAINED_LANGS:
            for filename in INDEXABLE_CORE_PAGES:
                with self.subTest(lang=lang, filename=filename):
                    alternates = parse_page(page_path(lang, filename)).hreflangs
                    codes = [code for code, _ in alternates]
                    self.assertEqual(len(codes), len(expected_codes))
                    self.assertEqual(set(codes), expected_codes)

    def test_english_low_value_pages_are_not_in_hreflang_clusters(self):
        for filename in ("privacy.html", "404.html"):
            with self.subTest(filename=filename):
                self.assertEqual(parse_page(PUBLIC / filename).hreflangs, [])

    def test_active_locale_core_pages_do_not_present_a_product_brand(self):
        forbidden = (
            "euchio mixed gas",
            "euchio gas mixing equipment",
            "euchio混合气",
            "euchio gas mixto",
            "euchio 혼합",
            "euchio混合ガス",
            "euchio gás misto",
            "euchio mieszanka gazowa",
            "euchio gas mixing technology",
            "dispositivo de gas mixto euchio",
            "euchio 混合ガス装置",
            "urządzenia do mieszania gazów euchio",
            "联系euchio获取混合气体设备",
            '"name": "联系euchio"',
            "euchio标志",
        )
        for lang in RETAINED_LANGS:
            for filename in CORE_PAGES:
                path = page_path(lang, filename)
                content = path.read_text(encoding="utf-8").casefold()
                with self.subTest(lang=lang, filename=filename):
                    for phrase in forbidden:
                        self.assertNotIn(phrase, content)
                    self.assertNotRegex(
                        content,
                        r'<span class="logo-brand">\s*euchio\s*</span>',
                    )
                    self.assertNotRegex(
                        content,
                        r'<div class="result-badge euchio-badge"[^>]*>.*?>\s*euchio\s*</div>',
                    )

    def test_polish_homepage_avoids_unverified_scope_and_absolute_claims(self):
        content = page_path("pl", "home").read_text(encoding="utf-8").casefold()
        forbidden = (
            "1,000+ instalacji",
            "certyfikat ce",
            "12-miesięczna gwarancja",
            "dostawa 2-4 tygodnie",
            "jedyny producent",
            "jeden-do-dwóch",
            "jedno urządzenie zasila dwa",
            "100% bezpieczne",
            "100% bezpieczeństwo",
            "zero ryzyka optycznego",
            "3× szybsze",
            "3x szybsze",
            "zero zadziorów",
            "praktycznie zerowy",
            "bezobsługowe",
            "prawdziwe dane, prawdziwa wydajność",
            "użytkowników na całym świecie",
            "doskonałymi rezultatami",
            "dla wszystkich klientów",
            "20+ countries in pipeline",
            "4 continents deployed",
            "24/7 production endurance",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, content)

    def test_canonical_urls_match_page_locale(self):
        for lang in RETAINED_LANGS:
            for page_key in INDEXABLE_CORE_PAGES:
                with self.subTest(lang=lang, page_key=page_key):
                    canonicals = parse_page(page_path(lang, page_key)).canonicals
                    self.assertEqual(len(canonicals), 1)
                    self.assertEqual(urlparse(canonicals[0]).path, route_for(lang, page_key))

    def test_jsonld_is_valid(self):
        pattern = re.compile(
            r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
            re.DOTALL | re.IGNORECASE,
        )
        for lang in RETAINED_LANGS:
            for filename in CORE_PAGES:
                path = page_path(lang, filename)
                for index, block in enumerate(pattern.findall(path.read_text(encoding="utf-8"))):
                    with self.subTest(lang=lang, filename=filename, index=index):
                        json.loads(html.unescape(block))

    def test_core_jsonld_avoids_unsupported_or_unqualified_types(self):
        pattern = re.compile(
            r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
            re.DOTALL | re.IGNORECASE,
        )
        forbidden_everywhere = {"Offer", "Review", "AggregateRating", "HowTo"}
        forbidden_on_non_product_pages = {"Product", "FAQPage"}

        def collect_types(value):
            found = set()
            if isinstance(value, dict):
                raw = value.get("@type")
                if isinstance(raw, str):
                    found.add(raw)
                for child in value.values():
                    found.update(collect_types(child))
            elif isinstance(value, list):
                for child in value:
                    found.update(collect_types(child))
            return found

        for lang in RETAINED_LANGS:
            for page_key in CORE_PAGES:
                path = page_path(lang, page_key)
                blocks = pattern.findall(path.read_text(encoding="utf-8"))
                types = set()
                for block in blocks:
                    types.update(collect_types(json.loads(html.unescape(block))))
                forbidden = set(forbidden_everywhere)
                if page_key in {"home", "about", "contact"}:
                    forbidden.update(forbidden_on_non_product_pages)
                with self.subTest(lang=lang, page_key=page_key):
                    self.assertFalse(types & forbidden, (path, types & forbidden))

    def test_english_low_value_pages_are_noindex(self):
        robots_pattern = re.compile(
            r'<meta\s+name="robots"\s+content="([^"]+)"',
            re.IGNORECASE,
        )
        for filename in ("privacy.html", "404.html"):
            path = PUBLIC / filename
            match = robots_pattern.search(path.read_text(encoding="utf-8"))
            with self.subTest(filename=filename):
                self.assertIsNotNone(match)
                self.assertEqual(match.group(1).casefold(), "noindex, follow")

    def test_no_placeholders_or_duplicate_ids(self):
        for lang in RETAINED_LANGS:
            for filename in CORE_PAGES:
                path = page_path(lang, filename)
                content = path.read_text(encoding="utf-8")
                parser = parse_page(path)
                with self.subTest(lang=lang, filename=filename):
                    self.assertNotIn("{{", content)
                    self.assertEqual(len(parser.ids), len(set(parser.ids)))

    def test_sitemap_excludes_removed_languages(self):
        tree = ET.parse(PUBLIC / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [node.text or "" for node in tree.findall("s:url/s:loc", ns)]
        for lang in REMOVED_LANGS:
            self.assertFalse(any(urlparse(loc).path.startswith(f"/{lang}/") for loc in locs))
        self.assertFalse(any(urlparse(loc).path.endswith("404") for loc in locs))


if __name__ == "__main__":
    unittest.main()
