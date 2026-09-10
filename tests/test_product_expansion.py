import html
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PRODUCT_DIR = PUBLIC / "products"

PAGES = {
    "psa": "psa-nitrogen-generation-system.html",
    "cabinet": "integrated-gas-mixing-cabinet.html",
    "valve": "mspv2-4000-proportional-valve.html",
    "comparison": "mixed-gas-control-comparison.html",
}

PRODUCT_IDS = {
    "psa": "psa-nitrogen-system",
    "cabinet": "integrated-mixing-cabinet",
    "valve": "mspv2-4000",
    "comparison": "need-recommendation",
}


class ProductPageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.h1_parts = []
        self.links = []
        self.images = []
        self.videos = []
        self.ids = []
        self.jsonld_blocks = []
        self._capture = None
        self._jsonld = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "title":
            self._capture = "title"
        if tag == "h1":
            self._capture = "h1"
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs)
        if tag == "link":
            self.links.append(attrs)
        if tag == "img":
            self.images.append(attrs)
        if tag in {"video", "source"}:
            self.videos.append((tag, attrs))
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self._jsonld = []

    def handle_endtag(self, tag):
        if tag == self._capture:
            self._capture = None
        if tag == "script" and self._jsonld is not None:
            self.jsonld_blocks.append("".join(self._jsonld))
            self._jsonld = None

    def handle_data(self, data):
        if self._capture == "title":
            self.title_parts.append(data)
        elif self._capture == "h1":
            self.h1_parts.append(data)
        if self._jsonld is not None:
            self._jsonld.append(data)

    @property
    def title(self):
        return " ".join("".join(self.title_parts).split())

    @property
    def h1(self):
        return " ".join("".join(self.h1_parts).split())


def page_path(name, locale="en"):
    product_dir = PRODUCT_DIR if locale == "en" else PUBLIC / locale / "products"
    return product_dir / PAGES[name]


def read_page(testcase, name, locale="en"):
    path = page_path(name, locale)
    testcase.assertTrue(path.is_file(), f"Missing product page: {path}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def parse_page(testcase, name, locale="en"):
    parser = ProductPageParser()
    parser.feed(read_page(testcase, name, locale))
    return parser


def collect_types(value):
    found = set()
    if isinstance(value, dict):
        raw_type = value.get("@type")
        if isinstance(raw_type, str):
            found.add(raw_type)
        elif isinstance(raw_type, list):
            found.update(item for item in raw_type if isinstance(item, str))
        for child in value.values():
            found.update(collect_types(child))
    elif isinstance(value, list):
        for child in value:
            found.update(collect_types(child))
    return found


class ProductExpansionTests(unittest.TestCase):
    def test_english_product_pages_exist(self):
        for name in PAGES:
            with self.subTest(name=name):
                self.assertTrue(page_path(name).is_file())

    def test_mixer_pages_state_same_function_and_alternative_choice(self):
        content = read_page(self, "comparison").casefold()
        self.assertIn("same core function", content)
        self.assertRegex(content, r"choose (?:one|between)")
        for forbidden in ("cabinet feeds valve", "valve feeds cabinet", "use both mixers"):
            self.assertNotIn(forbidden, content)

    def test_psa_relationship_is_optional_upstream_supply(self):
        content = read_page(self, "psa").casefold()
        self.assertIn("pure nitrogen cutting", content)
        self.assertIn("upstream nitrogen source", content)
        self.assertIn("optional", content)
        self.assertNotIn("psa is required", content)
        self.assertNotIn("psa is mandatory", content)

    def test_psa_layout_is_presented_as_a_compact_six_kw_reference_case(self):
        content = read_page(self, "psa")
        styles = (PUBLIC / "styles.css").read_text(encoding="utf-8")

        self.assertIn('class="psa-reference-case"', content)
        for value in ("6 kW", "40 Nm³/h", "99.99%", "2.0 MPa", "10.17 × 1.60 m"):
            with self.subTest(value=value):
                self.assertIn(value, content)
        for detail in ("Weight 600KG", "Weight 87KG", "Weight 1570KG", "Weight 860KG"):
            with self.subTest(detail=detail):
                self.assertNotIn(detail, content)
        self.assertRegex(styles, r"\.psa-case-drawing\s*\{[^}]*overflow:\s*hidden")

    def test_psa_hero_uses_a_balanced_copy_and_system_panel_layout(self):
        content = read_page(self, "psa")
        styles = (PUBLIC / "styles.css").read_text(encoding="utf-8")
        hero = re.search(
            r'<section class="product-hero product-hero--nitrogen">.*?</section>',
            content,
            re.DOTALL,
        )

        self.assertIsNotNone(hero)
        hero_content = hero.group(0) if hero else ""
        self.assertIn("COMPLETE SYSTEM PATH", hero_content)
        self.assertRegex(
            styles,
            r"\.product-hero--nitrogen \.product-hero-grid\s*\{[^}]*max-width:\s*1440px[^}]*grid-template-columns:",
        )
        self.assertRegex(
            styles,
            r"\.product-hero--nitrogen \.product-actions\s*\{[^}]*flex-wrap:\s*nowrap",
        )
        self.assertRegex(
            styles,
            r"\.product-hero--nitrogen \.product-actions \.btn\s*\{[^}]*white-space:\s*nowrap",
        )
        self.assertRegex(
            styles,
            r"(?s)@media \(max-width: 768px\).*?\.product-hero--nitrogen \.product-actions\s*\{[^}]*flex-direction:\s*column",
        )

    def test_product_specs_stay_with_their_owner(self):
        cabinet = read_page(self, "cabinet")
        valve = read_page(self, "valve")
        psa = read_page(self, "psa")

        for value in ("800 × 350 × 1100", "90 kg", "200 m³/h", "20–25 bar", "12–16 bar"):
            with self.subTest(page="cabinet", value=value):
                self.assertIn(value, cabinet)
        for value in ("120 × 118 × 106", "2.43 kg", "200 ms", "0–5000 L/min", "3–64%", "24 V"):
            with self.subTest(page="valve", value=value):
                self.assertIn(value, valve)
        for value in ("40 Nm³/h", "75 Nm³/h", "99.99%", "2.0 MPa", "reference configuration"):
            with self.subTest(page="psa", value=value):
                self.assertIn(value, psa)

        self.assertNotIn("800 × 350 × 1100", valve)
        self.assertNotIn("2.43 kg", cabinet)

    def test_no_unverified_commercial_or_schema_claims(self):
        forbidden_copy = re.compile(
            r"\b(?:in stock|delivery in \d+|ships? in \d+|guaranteed|best on the market|"
            r"ce[- ]certified|ce certification)\b",
            re.IGNORECASE,
        )
        forbidden_schema = {"Offer", "Review", "AggregateRating"}

        for name in PAGES:
            with self.subTest(name=name):
                content = read_page(self, name)
                self.assertIsNone(forbidden_copy.search(content))
                parser = parse_page(self, name)
                types = set()
                for block in parser.jsonld_blocks:
                    types.update(collect_types(json.loads(html.unescape(block))))
                self.assertFalse(types & forbidden_schema)

    def test_cta_contract(self):
        for name, product_id in PRODUCT_IDS.items():
            with self.subTest(name=name):
                parser = parse_page(self, name)
                hrefs = [link.get("href", "") for link in parser.links]
                self.assertIn(f"/contact?product={product_id}", hrefs)

        psa_hrefs = [link.get("href", "") for link in parse_page(self, "psa").links]
        cabinet_hrefs = [link.get("href", "") for link in parse_page(self, "cabinet").links]
        valve_hrefs = [link.get("href", "") for link in parse_page(self, "valve").links]

        self.assertFalse(any("dhgate.com" in href for href in psa_hrefs))
        self.assertIn(
            "https://www.dhgate.com/product/integrated-gas-mixing-regulation-cabinet/1111142341.html",
            cabinet_hrefs,
        )
        self.assertIn("https://www.dhgate.com/store/22325464", valve_hrefs)
        self.assertNotIn(
            "https://www.dhgate.com/product/integrated-gas-mixing-regulation-cabinet/1111142341.html",
            valve_hrefs,
        )

    def test_product_pages_have_one_h1_unique_ids_and_accessible_product_menu(self):
        for name in PAGES:
            with self.subTest(name=name):
                content = read_page(self, name)
                parser = parse_page(self, name)
                self.assertTrue(parser.title)
                self.assertTrue(parser.h1)
                self.assertEqual(len(re.findall(r"<h1\b", content, re.IGNORECASE)), 1)
                self.assertEqual(len(parser.ids), len(set(parser.ids)))
                self.assertRegex(content, r'<button[^>]+aria-expanded="false"[^>]+aria-controls="productMenu"')
                self.assertIn('id="productMenu"', content)

    def test_product_pages_have_pretty_canonical_and_valid_jsonld(self):
        expected_types = {
            "psa": {"Product", "BreadcrumbList"},
            "cabinet": {"Product", "BreadcrumbList"},
            "valve": {"Product", "BreadcrumbList", "VideoObject"},
            "comparison": {"CollectionPage", "BreadcrumbList"},
        }
        titles = set()
        for name, filename in PAGES.items():
            with self.subTest(name=name):
                parser = parse_page(self, name)
                titles.add(parser.title)
                canonicals = [
                    link.get("href", "")
                    for link in parser.links
                    if link.get("rel") == "canonical"
                ]
                self.assertEqual(
                    canonicals,
                    [f"https://gasmixtech.com/products/{filename.removesuffix('.html')}"],
                )
                types = set()
                for block in parser.jsonld_blocks:
                    types.update(collect_types(json.loads(html.unescape(block))))
                self.assertTrue(expected_types[name] <= types, (name, types))
        self.assertEqual(len(titles), len(PAGES))

    def test_product_media_and_internal_links_resolve(self):
        broken = []
        for name in PAGES:
            path = page_path(name)
            parser = parse_page(self, name)
            for image in parser.images:
                self.assertTrue(image.get("alt", "").strip(), (name, image))
                src = image.get("src", "")
                if src.startswith("/") and not (PUBLIC / src.lstrip("/")).is_file():
                    broken.append((name, src))
            for _, attrs in parser.videos:
                src = attrs.get("src") or attrs.get("srcset")
                if src and src.startswith("/") and not (PUBLIC / src.lstrip("/")).is_file():
                    broken.append((name, src))
            for link in parser.links:
                href = link.get("href", "")
                if "lang-option" in link.get("class", "").split():
                    continue
                parsed = urlparse(href)
                if parsed.scheme or parsed.netloc or href.startswith(("#", "mailto:", "tel:")):
                    continue
                target_path = parsed.path
                if not target_path or target_path == "/contact":
                    continue
                target = PUBLIC / target_path.lstrip("/")
                if target.exists() or target.with_suffix(".html").is_file():
                    continue
                broken.append((name, href))
        self.assertEqual(broken, [])

    def test_comparison_table_and_valve_video_have_responsive_contract(self):
        comparison = read_page(self, "comparison")
        valve = read_page(self, "valve")
        self.assertIn('class="comparison-scroll"', comparison)
        self.assertRegex(valve, r'<video\b[^>]*preload="none"')
        self.assertIn("prefers-reduced-motion", (PUBLIC / "styles.css").read_text(encoding="utf-8"))

    def test_homepage_explains_the_two_stage_product_decision(self):
        content = (PUBLIC / "index.html").read_text(encoding="utf-8")
        folded = content.casefold()
        self.assertIn("optional upstream", folded)
        self.assertIn("same core function", folded)
        self.assertRegex(folded, r"choose (?:one|between)")
        for filename in PAGES.values():
            with self.subTest(filename=filename):
                self.assertIn(f"/products/{filename.removesuffix('.html')}", content)

    def test_homepage_hero_uses_a_native_system_visual_not_a_psa_document_image(self):
        content = (PUBLIC / "index.html").read_text(encoding="utf-8")
        hero = re.search(r'<section class="hero portfolio-hero".*?</section>', content, re.DOTALL)
        self.assertIsNotNone(hero)
        hero_content = hero.group(0) if hero else ""
        self.assertIn('class="portfolio-system-visual"', hero_content)
        self.assertNotIn("psa-nitrogen-system-process.png", hero_content)
        self.assertNotRegex(hero_content, r"<img\b")

    def test_homepage_routes_the_product_family_instead_of_repeating_cabinet_sales_content(self):
        content = (PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('class="roi-calculator"', content)
        self.assertNotIn('class="air-pain-section"', content)
        self.assertNotIn('class="params-grid"', content)
        self.assertNotIn("youtube.com/embed/", content)
        self.assertIn('href="/roi"', content)
        self.assertIn('href="/parameters"', content)
        self.assertIn('href="/products/integrated-gas-mixing-cabinet#cabinet-evidence"', content)
        self.assertNotIn(
            "https://www.dhgate.com/product/integrated-gas-mixing-regulation-cabinet/1111142341.html",
            content,
        )

    def test_roi_page_owns_the_mixed_gas_calculator_and_air_cost_analysis(self):
        content = (PUBLIC / "roi.html").read_text(encoding="utf-8")
        self.assertIn('class="roi-calculator"', content)
        self.assertIn('class="air-pain-section"', content)

    def test_cabinet_page_owns_the_existing_cutting_video_evidence(self):
        content = read_page(self, "cabinet")
        for video_id in (
            "z3vfXdCFPlk",
            "qoZ6I6AfsTw",
            "eNiaCFzuyU4",
            "tC23EJnQKTg",
            "Qw_p7xVhA-M",
            "IIRhLio9xxg",
        ):
            with self.subTest(video_id=video_id):
                self.assertIn(f"youtube.com/embed/{video_id}", content)
        self.assertIn('href="/roi"', content)
        self.assertIn('href="/parameters"', content)

    def test_english_core_navigation_exposes_the_product_family(self):
        core_pages = (
            "index.html",
            "about.html",
            "parameters.html",
            "compatibility.html",
            "contact.html",
            "payment.html",
            "roi.html",
        )
        product_routes = {
            "/products/psa-nitrogen-generation-system",
            "/products/integrated-gas-mixing-cabinet",
            "/products/mspv2-4000-proportional-valve",
            "/products/mixed-gas-control-comparison",
        }
        for filename in core_pages:
            with self.subTest(filename=filename):
                content = (PUBLIC / filename).read_text(encoding="utf-8")
                header = re.search(r"<header\b.*?</header>", content, re.DOTALL | re.IGNORECASE)
                self.assertIsNotNone(header)
                header_content = header.group(0) if header else ""
                self.assertIn('id="productMenuButton"', header_content)
                self.assertIn('aria-controls="productMenu"', header_content)
                self.assertTrue(product_routes <= set(re.findall(r'href="([^"]+)"', header_content)))
                self.assertRegex(header_content, r'href="/(?:contact|contact\.html)[^"]*"[^>]*class="nav-cta"')


if __name__ == "__main__":
    unittest.main()
