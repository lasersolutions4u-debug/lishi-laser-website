import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LANGS = ["en", "es", "zh", "ko", "ja", "pt", "tr", "pl", "it", "de", "fr", "nl", "ru", "vi", "th"]
SUB_LANGS = LANGS[1:]
TRANSLATED_ABOUT_MARKERS = {
    "es": "Quiénes Somos",
    "zh": "我们是谁",
    "ko": "회사 소개",
    "ja": "私たちについて",
    "pt": "Quem Somos",
    "tr": "Biz Kimiz",
    "pl": "Kim jesteśmy",
    "it": "Chi Siamo",
    "de": "Wer wir sind",
    "fr": "Qui Nous Sommes",
    "nl": "Wie Wij Zijn",
    "ru": "Кто мы",
    "vi": "Chúng Tôi Là Ai",
    "th": "เราเป็นใคร",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.h1 = []
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
    nav = re.search(r'<nav class="nav"[^>]*>(.*?)</nav>', content, re.DOTALL)
    if nav is None:
        return []
    return re.findall(r'<a\b[^>]*href="([^"]+)"', nav.group(1))


def page_path(lang, filename):
    return PUBLIC / filename if lang == "en" else PUBLIC / lang / filename


class SiteIntegrityTests(unittest.TestCase):
    def test_about_nav_is_after_parameters_and_immediately_before_contact(self):
        for lang in LANGS:
            for filename in ("index.html", "about.html", "parameters.html", "contact.html"):
                with self.subTest(lang=lang, filename=filename):
                    hrefs = header_nav_hrefs(page_path(lang, filename))
                    parameter_matches = [i for i, href in enumerate(hrefs) if "parameters" in href]
                    about_matches = [i for i, href in enumerate(hrefs) if "about" in href]
                    contact_matches = [i for i, href in enumerate(hrefs) if "contact" in href]
                    self.assertEqual(len(parameter_matches), 1, hrefs)
                    self.assertEqual(len(about_matches), 1, hrefs)
                    self.assertEqual(len(contact_matches), 1, hrefs)
                    parameters = parameter_matches[0]
                    about = about_matches[0]
                    contact = contact_matches[0]
                    self.assertLess(parameters, about)
                    self.assertEqual(about + 1, contact)

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

    def test_parameter_and_contact_pages_have_one_h1(self):
        for lang in LANGS:
            for filename in ("parameters.html", "contact.html"):
                with self.subTest(lang=lang, filename=filename):
                    page = parse_page(page_path(lang, filename))
                    self.assertTrue(page.h1)

    def test_localized_titles_are_valid_utf8_and_language_consistent(self):
        mojibake = re.compile(r"[贸莽茫陌艧谋臋膮谩]")
        for lang in SUB_LANGS:
            for filename in ("parameters.html", "contact.html"):
                with self.subTest(lang=lang, filename=filename):
                    title = parse_page(page_path(lang, filename)).title
                    self.assertFalse(mojibake.search(title), title)
        self.assertNotRegex(parse_page(page_path("ja", "parameters.html")).title, r"[가-힣]")
        self.assertNotRegex(parse_page(page_path("ja", "parameters.html")).h1, r"[가-힣]")
        for lang in ("it", "de", "fr"):
            title = parse_page(page_path(lang, "contact.html")).title
            self.assertNotRegex(title, r"\bGet\b.*\bQuote\b")

    def test_pretty_urls_are_used_for_canonical_hreflang_and_sitemap(self):
        for lang in LANGS:
            prefix = "" if lang == "en" else f"/{lang}"
            for filename in ("about.html", "parameters.html", "contact.html"):
                with self.subTest(lang=lang, filename=filename):
                    page = parse_page(page_path(lang, filename))
                    canonical = next(link["href"] for link in page.links if link.get("rel") == "canonical")
                    self.assertEqual(urlparse(canonical).path, f"{prefix}/{filename.removesuffix('.html')}")
                    alternates = [link["href"] for link in page.links if link.get("rel") == "alternate"]
                    self.assertTrue(alternates)
                    self.assertTrue(all(not urlparse(href).path.endswith(".html") for href in alternates))

        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotRegex(sitemap, r"(?:about|parameters|contact)\.html")

    def test_sitemap_excludes_error_pages_and_includes_all_about_pages(self):
        tree = ET.parse(PUBLIC / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [node.text for node in tree.findall("s:url/s:loc", ns)]
        self.assertNotIn("https://gasmixtech.com/404.html", locs)
        about_locs = [loc for loc in locs if loc.endswith("/about") or loc == "https://gasmixtech.com/about"]
        self.assertEqual(len(about_locs), 15)

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
