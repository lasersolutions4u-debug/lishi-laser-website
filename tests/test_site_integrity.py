import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from site_locales import CORE_ROUTES, SUPPORTED_LOCALES, output_path, route_for


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LANGS = ["en", "es", "zh", "ko", "ja", "pt", "pl"]
SUB_LANGS = LANGS[1:]
TRANSLATED_ABOUT_MARKERS = {
    "es": "Quiénes Somos",
    "zh": "我们是谁",
    "ko": "회사 소개",
    "ja": "私たちについて",
    "pt": "Quem Somos",
    "pl": "Kim jesteśmy",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.h1 = []
        self.h1_count = 0
        self.h2 = []
        self.anchors = []
        self.links = []
        self.images = []
        self._capture = None
        self._anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"title", "h1", "h2"}:
            self._capture = tag
        if tag == "h1":
            self.h1_count += 1
        if tag == "a":
            self._anchor = {"href": attrs.get("href", ""), "text": []}
        if tag == "link":
            self.links.append(attrs)
        if tag == "img":
            self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == self._capture:
            self._capture = None
        if tag == "a" and self._anchor is not None:
            self._anchor["text"] = " ".join("".join(self._anchor["text"]).split())
            self.anchors.append(self._anchor)
            self._anchor = None

    def handle_data(self, data):
        if self._capture:
            getattr(self, self._capture).append(data)
        if self._anchor is not None:
            self._anchor["text"].append(data)


def parse_page(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.title = " ".join("".join(parser.title).split())
    parser.h1 = " ".join("".join(parser.h1).split())
    parser.h2 = [" ".join(text.split()) for text in parser.h2 if text.strip()]
    return parser


def header_nav_hrefs(path):
    content = path.read_text(encoding="utf-8")
    nav = re.search(
        r'<nav class="[^"]*\bnav\b[^"]*"[^>]*>(.*?)</nav>',
        content,
        re.DOTALL,
    )
    if nav is None:
        return []
    return re.findall(r'<a\b[^>]*href="([^"]+)"', nav.group(1))


def page_path(lang, filename):
    return PUBLIC / filename if lang == "en" else PUBLIC / lang / filename


class SiteIntegrityTests(unittest.TestCase):
    def test_about_pages_do_not_position_company_as_a_trading_business(self):
        trading_terms = (
            "machinery trading",
            "机械贸易",
            "comercio y servicio de maquinaria",
            "maschinenhandels- und serviceunternehmen",
            "commerce et de service de machines",
            "機械貿易",
            "торгово-сервисная",
            "handel i serwis",
            "handels- en servicebedrijf",
        )
        sources = [page_path(lang, "about.html") for lang in LANGS]
        sources.extend((ROOT / "about_locales.py", ROOT / "build-about-langs.py"))

        for source in sources:
            content = source.read_text(encoding="utf-8").casefold()
            for term in trading_terms:
                with self.subTest(source=source, term=term):
                    self.assertNotIn(term, content, f"{term!r} remains in {source}")

    def test_about_brand_section_matches_two_brand_content(self):
        brand_page_count = 0

        for lang in LANGS:
            content = page_path(lang, "about.html").read_text(encoding="utf-8")
            section = re.search(
                r'<section[^>]*id="brands"[^>]*>(.*?)</section>',
                content,
                re.DOTALL,
            )
            if section is None:
                continue

            brand_page_count += 1
            brand_section = section.group(1)
            self.assertIn('class="brand-grid"', brand_section)
            self.assertEqual(
                len(re.findall(r'class="[^"]*\bbrand-card\b[^"]*"', brand_section)),
                2,
            )
            self.assertIn('class="brand-fit-note', brand_section)

        self.assertGreater(brand_page_count, 0)

        styles = (PUBLIC / "styles.css").read_text(encoding="utf-8")
        self.assertRegex(
            styles,
            r"(?s)\.brand-grid\s*\{[^}]*grid-template-columns:\s*repeat\(2,\s*minmax\(0,\s*1fr\)\)",
        )
        self.assertRegex(
            styles,
            r"(?s)\.section-dark \.brand-card h3\s*\{[^}]*color:\s*var\(--color-text\)",
        )
        self.assertRegex(
            styles,
            r"(?s)\.brand-fit-note p\s*\{[^}]*color:\s*var\(--color-text-inverse-muted\)",
        )

    def test_about_pages_exclude_removed_compatible_brands(self):
        sources = [page_path(lang, "about.html") for lang in LANGS]
        sources.append(ROOT / "build-about-langs.py")

        for source in sources:
            content = source.read_text(encoding="utf-8")
            for brand in ("KIMLA", "MESSER"):
                with self.subTest(source=source, brand=brand):
                    self.assertNotRegex(content, rf"\b{brand}\b")

    def test_about_pages_do_not_publish_unverified_scale_claims(self):
        forbidden = re.compile(
            r"1,000\+|500\+\s+(?:installed|systems)|50\+\s+countries|30\+\s+(?:authorized\s+)?distributors",
            re.IGNORECASE,
        )
        for lang in LANGS:
            with self.subTest(lang=lang):
                content = page_path(lang, "about.html").read_text(encoding="utf-8")
                self.assertIsNone(forbidden.search(content))

    def test_legacy_localized_core_nav_keeps_about_before_contact(self):
        for lang in SUB_LANGS:
            for filename in ("about.html", "contact.html"):
                with self.subTest(lang=lang, filename=filename):
                    content = page_path(lang, filename).read_text(encoding="utf-8")
                    nav = re.search(
                        r'<nav class="[^"]*\bnav\b[^"]*"[^>]*>(.*?)</nav>',
                        content,
                        re.DOTALL,
                    )
                    self.assertIsNotNone(nav)
                    hrefs = re.findall(r'<a\b[^>]*href="([^"]+)"', nav.group(1))
                    expected_localized_links = (
                        f"/{lang}/products/psa-nitrogen-generation-system",
                        f"/{lang}/products/integrated-gas-mixing-cabinet",
                        f"/{lang}/products/mspv2-4000-proportional-valve",
                        f"/{lang}/products/mixed-gas-control-comparison",
                        f"/{lang}/#advantages",
                        f"/{lang}/#samples",
                        f"/{lang}/about",
                        f"/{lang}/contact",
                    )
                    for href in expected_localized_links:
                        self.assertEqual(hrefs.count(href), 1, hrefs)
                    about = hrefs.index(f"/{lang}/about")
                    contact = hrefs.index(f"/{lang}/contact")
                    self.assertEqual(about + 1, contact)
                    contact_anchor = re.search(
                        rf'<a\b(?=[^>]*\bhref="/{re.escape(lang)}/contact")'
                        r'(?=[^>]*\bclass="[^"]*\bnav-cta\b[^"]*")[^>]*>',
                        nav.group(1),
                    )
                    self.assertIsNotNone(contact_anchor)

    def test_all_about_pages_have_localized_content(self):
        for lang, marker in TRANSLATED_ABOUT_MARKERS.items():
            with self.subTest(lang=lang):
                page = parse_page(page_path(lang, "about.html"))
                self.assertIn(marker, page.h2)
                self.assertNotEqual(page.title, "About Us | Euchio Machinery — Sheet Metal Equipment & Service")

    def test_all_language_homepages_link_to_localized_about_page(self):
        for lang in SUB_LANGS:
            with self.subTest(lang=lang):
                page = parse_page(page_path(lang, "index.html"))
                about_links = [a for a in page.anchors if "about" in a["href"]]
                self.assertTrue(about_links)
                self.assertTrue(all(a["href"] == f"/{lang}/about" for a in about_links))

    def test_product_scope_is_consistent(self):
        forbidden = re.compile(
            r"one[- ]to[- ]two|up to two laser|two laser machines|"
            r"一拖二|最多两台|最大2台|2台のレーザー|zwei Lasermaschinen|deux machines laser|"
            r"6KW[–-]60KW machines",
            re.IGNORECASE,
        )
        offenders = []
        for path in PUBLIC.rglob("*.html"):
            match = forbidden.search(path.read_text(encoding="utf-8"))
            if match:
                offenders.append(f"{path.relative_to(PUBLIC)}: {match.group(0)}")
        self.assertEqual(offenders, [])
        self.assertRegex((PUBLIC / "index.html").read_text(encoding="utf-8"), r"One-to-Three|one-to-three")
        self.assertRegex((PUBLIC / "about.html").read_text(encoding="utf-8"), r"one-to-three")

    def test_core_sales_pages_exist_and_have_one_h1(self):
        for lang in SUPPORTED_LOCALES:
            for page_key in CORE_ROUTES:
                with self.subTest(lang=lang, page_key=page_key):
                    path = output_path(PUBLIC, lang, page_key)
                    self.assertTrue(path.is_file())
                    page = parse_page(path)
                    self.assertTrue(page.h1)
                    self.assertEqual(page.h1_count, 1)

    def test_localized_titles_are_valid_utf8_and_language_consistent(self):
        mojibake = re.compile(r"[贸莽茫陌艧谋臋膮谩]")
        for lang in SUPPORTED_LOCALES[1:]:
            for page_key in CORE_ROUTES:
                with self.subTest(lang=lang, page_key=page_key):
                    title = parse_page(output_path(PUBLIC, lang, page_key)).title
                    self.assertTrue(title)
                    self.assertFalse(mojibake.search(title), title)
        for page_key in CORE_ROUTES:
            with self.subTest(lang="ja", page_key=page_key):
                page = parse_page(output_path(PUBLIC, "ja", page_key))
                self.assertNotRegex(page.title, r"[가-힣]")
                self.assertNotRegex(page.h1, r"[가-힣]")

    def test_pretty_urls_are_used_for_canonical_hreflang_and_sitemap(self):
        expected_alternate_count = len(SUPPORTED_LOCALES) + 1
        nav_page_keys = ("about", "contact", "psa", "cabinet", "valve", "comparison")
        for lang in SUPPORTED_LOCALES:
            for page_key in CORE_ROUTES:
                with self.subTest(lang=lang, page_key=page_key):
                    path = output_path(PUBLIC, lang, page_key)
                    page = parse_page(path)
                    canonicals = [
                        link["href"]
                        for link in page.links
                        if link.get("rel") == "canonical"
                    ]
                    self.assertEqual(len(canonicals), 1)
                    self.assertEqual(urlparse(canonicals[0]).path, route_for(lang, page_key))
                    alternates = [
                        link["href"]
                        for link in page.links
                        if link.get("rel") == "alternate"
                    ]
                    self.assertEqual(len(alternates), expected_alternate_count)
                    self.assertTrue(all(not urlparse(href).path.endswith(".html") for href in alternates))
                    nav_hrefs = [urlparse(href).path for href in header_nav_hrefs(path)]
                    for nav_page_key in nav_page_keys:
                        self.assertIn(route_for(lang, nav_page_key), nav_hrefs)

        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotRegex(
            sitemap,
            r"(?:about|contact|psa-nitrogen-generation-system|integrated-gas-mixing-cabinet|"
            r"mspv2-4000-proportional-valve|mixed-gas-control-comparison)\.html",
        )

    def test_sitemap_excludes_error_pages_and_includes_all_about_pages(self):
        tree = ET.parse(PUBLIC / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [node.text for node in tree.findall("s:url/s:loc", ns)]
        self.assertNotIn("https://gasmixtech.com/404.html", locs)
        about_locs = [loc for loc in locs if loc.endswith("/about") or loc == "https://gasmixtech.com/about"]
        self.assertEqual(len(about_locs), len(LANGS))

    def test_about_factory_image_alt_text_is_localized(self):
        english_alts = {
            image.get("alt", "")
            for image in parse_page(PUBLIC / "about.html").images
            if "factory" in image.get("src", "")
        }
        for lang in SUB_LANGS:
            with self.subTest(lang=lang):
                page = parse_page(page_path(lang, "about.html"))
                factory_alts = {
                    image.get("alt", "")
                    for image in page.images
                    if "factory" in image.get("src", "")
                }
                self.assertTrue(factory_alts)
                self.assertTrue(factory_alts.isdisjoint(english_alts))


if __name__ == "__main__":
    unittest.main()
