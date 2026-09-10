import difflib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from site_locales import (
    CORE_ROUTES,
    LOCALIZED_LOCALES,
    SUPPORTED_LOCALES,
    UNSUPPORTED_LOCALES,
    alternates_for,
    canonical_url,
    output_path,
    route_for,
)
from tests.test_product_expansion import ProductPageParser

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

PRODUCT_BUILDER_SPEC = importlib.util.spec_from_file_location(
    "build_product_pages",
    ROOT / "build-product-pages.py",
)
PRODUCT_BUILDER = importlib.util.module_from_spec(PRODUCT_BUILDER_SPEC)
PRODUCT_BUILDER_SPEC.loader.exec_module(PRODUCT_BUILDER)


class LocaleRouteContractTests(unittest.TestCase):
    def test_language_sets_are_exact_and_disjoint(self):
        self.assertEqual(SUPPORTED_LOCALES, ("en", "zh", "es", "pt", "ja", "ko", "pl"))
        self.assertEqual(LOCALIZED_LOCALES, SUPPORTED_LOCALES[1:])
        self.assertEqual(UNSUPPORTED_LOCALES, ("de", "fr", "it", "nl", "tr", "ru", "vi", "th"))
        self.assertFalse(set(SUPPORTED_LOCALES) & set(UNSUPPORTED_LOCALES))

    def test_core_route_map_is_exact(self):
        self.assertEqual(
            CORE_ROUTES,
            {
                "home": "/",
                "about": "/about",
                "contact": "/contact",
                "psa": "/products/psa-nitrogen-generation-system",
                "cabinet": "/products/integrated-gas-mixing-cabinet",
                "valve": "/products/mspv2-4000-proportional-valve",
                "comparison": "/products/mixed-gas-control-comparison",
            },
        )
        self.assertEqual(route_for("en", "valve"), "/products/mspv2-4000-proportional-valve")
        self.assertEqual(route_for("ja", "valve"), "/ja/products/mspv2-4000-proportional-valve")
        self.assertEqual(route_for("pl", "home"), "/pl/")

    def test_alternates_cover_every_supported_locale_and_x_default(self):
        expected_keys = set(SUPPORTED_LOCALES) | {"x-default"}
        for page_key in CORE_ROUTES:
            with self.subTest(page_key=page_key):
                values = alternates_for(page_key)
                self.assertEqual(set(values), expected_keys)
                for locale in SUPPORTED_LOCALES:
                    self.assertEqual(values[locale], canonical_url(locale, page_key))
                self.assertEqual(values["x-default"], canonical_url("en", page_key))

    def test_output_and_canonical_mapping(self):
        self.assertEqual(output_path(PUBLIC, "en", "contact"), PUBLIC / "contact.html")
        self.assertEqual(output_path(PUBLIC, "es", "contact"), PUBLIC / "es" / "contact.html")
        self.assertEqual(output_path(PUBLIC, "ko", "psa"), PUBLIC / "ko" / "products" / "psa-nitrogen-generation-system.html")
        self.assertEqual(canonical_url("pt", "comparison"), "https://gasmixtech.com/pt/products/mixed-gas-control-comparison")


class ProductRouteTests(unittest.TestCase):
    PRODUCT_PAGE_KEYS = ("psa", "cabinet", "valve", "comparison")

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temp_dir.name)
        self.fixture_public = self.fixture_root / "public"
        self.fixture_content = self.fixture_public / "i18n" / "products"
        self.fixture_content.mkdir(parents=True)
        self.english_content = json.loads(
            (PUBLIC / "i18n" / "products" / "en.json").read_text(encoding="utf-8")
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_content(self, locale, mutate=None):
        data = json.loads(json.dumps(self.english_content))
        data["locale"] = locale
        if mutate:
            mutate(data)
        (self.fixture_content / f"{locale}.json").write_text(
            json.dumps(data, ensure_ascii=False),
            encoding="utf-8",
        )

    def build(self, locales, template_dir=None):
        return PRODUCT_BUILDER.build_pages(
            locales,
            public_dir=self.fixture_public,
            content_dir=self.fixture_content,
            template_dir=template_dir or PUBLIC / "product-templates",
        )

    def assert_fact_drift_fails_without_writes(self, mutate, error_pattern):
        self.write_content("en")
        self.write_content("ja")
        self.write_content("zh", mutate)
        english_output = output_path(self.fixture_public, "en", "psa")
        japanese_output = output_path(self.fixture_public, "ja", "valve")
        for path, sentinel in (
            (english_output, "unchanged english"),
            (japanese_output, "unchanged japanese"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(sentinel, encoding="utf-8")

        with self.assertRaisesRegex(ValueError, error_pattern):
            self.build(("en", "ja", "zh"))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")
        self.assertEqual(japanese_output.read_text(encoding="utf-8"), "unchanged japanese")
        self.assertFalse(output_path(self.fixture_public, "zh", "psa").exists())

    def test_all_24_localized_product_pages_exist(self):
        missing = [
            str(output_path(PUBLIC, locale, page_key).relative_to(PUBLIC))
            for locale in LOCALIZED_LOCALES
            for page_key in self.PRODUCT_PAGE_KEYS
            if not output_path(PUBLIC, locale, page_key).is_file()
        ]

        self.assertEqual(missing, [])

    def test_parse_locales_defaults_to_contract_and_rejects_unknown_values(self):
        self.assertEqual(PRODUCT_BUILDER.parse_locales(None), SUPPORTED_LOCALES)
        self.assertEqual(PRODUCT_BUILDER.parse_locales(["en", "ja"]), ("en", "ja"))
        with self.assertRaisesRegex(ValueError, "Unsupported locale: xx, yy"):
            PRODUCT_BUILDER.parse_locales(["yy", "xx"])

    def test_duplicate_locale_fails_without_writing(self):
        self.write_content("en")
        english_output = output_path(self.fixture_public, "en", "psa")
        english_output.parent.mkdir(parents=True)
        english_output.write_text("unchanged english", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Duplicate locale: en"):
            self.build(("en", "en"))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

    def test_localized_build_sets_routes_hreflangs_language_menu_and_schema(self):
        self.write_content("en")

        def localize(data):
            data["shared"]["home_aria"] = "ホーム"
            data["shared"]["nav_products"] = "製品"
            data["pages"]["valve"]["short_name"] = "MSPV2_4000 比例弁"

        self.write_content("ja", localize)
        self.build(("ja",))

        path = output_path(self.fixture_public, "ja", "valve")
        rendered = path.read_text(encoding="utf-8")
        self.assertRegex(rendered, r'<html lang="ja">')
        self.assertEqual(
            rendered.count(
                '<link rel="canonical" href="https://gasmixtech.com/ja/products/mspv2-4000-proportional-valve">'
            ),
            1,
        )
        for alternate_locale, url in alternates_for("valve").items():
            with self.subTest(alternate_locale=alternate_locale):
                self.assertEqual(
                    rendered.count(
                        f'<link rel="alternate" hreflang="{alternate_locale}" href="{url}">'
                    ),
                    1,
                )

        self.assertEqual(rendered.count('class="lang-option'), len(SUPPORTED_LOCALES))
        self.assertEqual(rendered.count('class="lang-option active"'), 1)
        for option_locale in SUPPORTED_LOCALES:
            active = " active" if option_locale == "ja" else ""
            self.assertIn(
                f'href="{route_for(option_locale, "valve")}" '
                f'class="lang-option{active}" data-lang="{option_locale}"',
                rendered,
            )

        for page_key in ("home", "about", *self.PRODUCT_PAGE_KEYS):
            self.assertIn(f'href="{route_for("ja", page_key)}', rendered)
        self.assertIn('href="/ja/contact?product=mspv2-4000"', rendered)
        self.assertNotIn('href="/products/mixed-gas-control-comparison"', rendered)
        self.assertNotIn("window.location", rendered)

        parser = ProductPageParser()
        parser.feed(rendered)
        graph = json.loads(parser.jsonld_blocks[0])["@graph"]
        webpage = next(item for item in graph if item["@type"] == "Product")
        video = next(item for item in graph if item["@type"] == "VideoObject")
        faq = next(item for item in graph if item["@type"] == "FAQPage")
        breadcrumb = next(item for item in graph if item["@type"] == "BreadcrumbList")
        self.assertEqual(webpage["inLanguage"], "ja")
        self.assertEqual(video["inLanguage"], "ja")
        self.assertEqual(faq["inLanguage"], "ja")
        self.assertEqual(webpage["url"], canonical_url("ja", "valve"))
        self.assertEqual(
            [item["name"] for item in breadcrumb["itemListElement"]],
            ["ホーム", "製品", "MSPV2_4000 比例弁"],
        )

    def test_single_locale_build_writes_only_selected_product_pages(self):
        self.write_content("en")
        self.write_content("ja")
        english_output = output_path(self.fixture_public, "en", "psa")
        english_output.parent.mkdir(parents=True)
        english_output.write_text("unchanged english", encoding="utf-8")

        self.build(("ja",))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")
        self.assertTrue(output_path(self.fixture_public, "ja", "psa").is_file())
        self.assertFalse(output_path(self.fixture_public, "zh", "psa").exists())

    def test_missing_translation_file_fails_without_partial_writes(self):
        self.write_content("en")
        english_output = output_path(self.fixture_public, "en", "psa")
        english_output.parent.mkdir(parents=True)
        english_output.write_text("unchanged english", encoding="utf-8")

        with self.assertRaisesRegex(FileNotFoundError, "zh.json"):
            self.build(("en", "zh"))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

    def test_invalid_json_fails_without_partial_writes(self):
        self.write_content("en")
        (self.fixture_content / "zh.json").write_text("{invalid", encoding="utf-8")
        english_output = output_path(self.fixture_public, "en", "psa")
        english_output.parent.mkdir(parents=True)
        english_output.write_text("unchanged english", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Invalid translation JSON: zh.json"):
            self.build(("en", "zh"))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

    def test_non_object_translation_roots_fail_without_partial_writes(self):
        for root_value in (None, [], "translation"):
            with self.subTest(root_value=root_value):
                self.write_content("en")
                (self.fixture_content / "zh.json").write_text(
                    json.dumps(root_value), encoding="utf-8"
                )
                english_output = output_path(self.fixture_public, "en", "psa")
                english_output.parent.mkdir(parents=True, exist_ok=True)
                english_output.write_text("unchanged english", encoding="utf-8")

                with self.assertRaisesRegex(ValueError, "Invalid translation root: zh.json"):
                    self.build(("en", "zh"))

                self.assertEqual(
                    english_output.read_text(encoding="utf-8"), "unchanged english"
                )

    def test_missing_key_fails_without_partial_writes(self):
        self.write_content("en")

        def remove_key(data):
            del data["pages"]["valve"]["h1"]

        self.write_content("zh", remove_key)
        english_output = output_path(self.fixture_public, "en", "psa")
        english_output.parent.mkdir(parents=True)
        english_output.write_text("unchanged english", encoding="utf-8")

        with self.assertRaisesRegex(KeyError, "Missing content key: pages.valve.h1"):
            self.build(("en", "zh"))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

    def test_translated_model_cannot_change_technical_identity(self):
        def change_model(data):
            data["pages"]["valve"]["model"] = "翻译型号"

        self.assert_fact_drift_fails_without_writes(
            change_model,
            r"Technical content mismatch: zh: pages\.valve\.model",
        )

    def test_spec_note_technical_tokens_cannot_drift(self):
        def change_note_purity(data):
            data["pages"]["psa"]["specs"][0]["note"] = "95% nitrogen, boosted to 2.0 MPa"

        self.assert_fact_drift_fails_without_writes(
            change_note_purity,
            r"Technical token mismatch: zh: pages\.psa\.specs\.0\.note",
        )

    def test_text_only_spec_value_cannot_drift(self):
        def change_interface(data):
            data["pages"]["valve"]["specs"][7]["value"] = "Digital only"

        self.assert_fact_drift_fails_without_writes(
            change_interface,
            r"Technical content mismatch: zh: pages\.valve\.specs\.7\.value",
        )

    def test_approved_slash_technical_identifier_cannot_drift(self):
        def change_interface_identifier(data):
            data["pages"]["comparison"]["comparison_rows"][6]["valve"] = (
                "Analog input/output and relay digital interfaces"
            )

        self.assert_fact_drift_fails_without_writes(
            change_interface_identifier,
            r"Technical token mismatch: zh: pages\.comparison\.comparison_rows\.6\.valve",
        )

    def test_narrative_measurement_unit_cannot_drift(self):
        def change_footprint_unit(data):
            data["pages"]["psa"]["footprint_caption"] = (
                "Reference footprint: approximately 10.17 × 1.60 ft. "
                "Final footprint and module positions depend on the confirmed supply scope and site conditions."
            )

        self.assert_fact_drift_fails_without_writes(
            change_footprint_unit,
            r"Technical token mismatch: zh: pages\.psa\.footprint_caption",
        )

    def test_comparison_row_technical_values_cannot_drift(self):
        def change_dimensions(data):
            data["pages"]["comparison"]["comparison_rows"][2]["cabinet"] = "900 × 350 × 1100 mm"

        self.assert_fact_drift_fails_without_writes(
            change_dimensions,
            r"Technical token mismatch: zh: pages\.comparison\.comparison_rows\.2\.cabinet",
        )

    def test_technical_token_order_cannot_drift(self):
        def reorder_dimensions(data):
            data["pages"]["comparison"]["comparison_rows"][2]["cabinet"] = "1100 × 350 × 800 mm"

        self.assert_fact_drift_fails_without_writes(
            reorder_dimensions,
            r"Technical token mismatch: zh: pages\.comparison\.comparison_rows\.2\.cabinet",
        )

    def test_spec_items_cannot_be_appended(self):
        def append_spec(data):
            data["pages"]["cabinet"]["specs"].append(
                {"label": "Invented", "value": "999 bar", "note": "Invented setting"}
            )

        self.assert_fact_drift_fails_without_writes(
            append_spec,
            r"Technical structure mismatch: zh: pages\.cabinet\.specs",
        )

    def test_comparison_rows_cannot_be_deleted(self):
        def delete_row(data):
            del data["pages"]["comparison"]["comparison_rows"][2]

        self.assert_fact_drift_fails_without_writes(
            delete_row,
            r"Technical structure mismatch: zh: pages\.comparison\.comparison_rows",
        )

    def test_tokenless_comparison_rows_cannot_be_reordered(self):
        def swap_rows(data):
            rows = data["pages"]["comparison"]["comparison_rows"]
            rows[6], rows[7] = rows[7], rows[6]

        self.assert_fact_drift_fails_without_writes(
            swap_rows,
            r"Technical content mismatch: zh: pages\.comparison\.comparison_rows\.6\.key",
        )

    def test_spaced_placeholder_marker_fails_without_writes(self):
        def insert_marker(data):
            data["pages"]["cabinet"]["fit_title"] = "{{ page.title }}"

        self.assert_fact_drift_fails_without_writes(
            insert_marker,
            r"unresolved template markers",
        )

    def test_unknown_placeholder_marker_fails_without_writes(self):
        def insert_marker(data):
            data["pages"]["cabinet"]["fit_title"] = "{{unknown.key}}"

        self.assert_fact_drift_fails_without_writes(
            insert_marker,
            r"unresolved template markers",
        )

    def test_illegal_placeholder_marker_fails_without_writes(self):
        def insert_marker(data):
            data["pages"]["cabinet"]["fit_title"] = "{{page:title}}"

        self.assert_fact_drift_fails_without_writes(
            insert_marker,
            r"unresolved template markers",
        )

    def test_translation_text_is_safe_in_html_attributes_body_and_jsonld(self):
        self.write_content("en")
        payload = 'Consult "A&B" <unsafe> </script>'

        def add_special_characters(data):
            data["pages"]["cabinet"]["description"] += " " + payload
            data["pages"]["cabinet"]["fit_text"] += " " + payload
            data["pages"]["cabinet"]["cards"][0]["text"] += " " + payload

        self.write_content("zh", add_special_characters)
        self.build(("zh",))

        rendered = output_path(self.fixture_public, "zh", "cabinet").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("<unsafe>", rendered)
        self.assertEqual(rendered.count("</script>"), 2)
        self.assertIn("&quot;A&amp;B&quot; &lt;unsafe&gt; &lt;/script&gt;", rendered)

        class MetadataParser(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.descriptions = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "meta" and attrs.get("name") == "description":
                    self.descriptions.append(attrs.get("content"))

        metadata = MetadataParser()
        metadata.feed(rendered)
        expected_description = self.english_content["pages"]["cabinet"]["description"] + " " + payload
        self.assertEqual(metadata.descriptions, [expected_description])

        parser = ProductPageParser()
        parser.feed(rendered)
        graph = json.loads(parser.jsonld_blocks[0])["@graph"]
        webpage = next(item for item in graph if item["@type"] == "Product")
        self.assertEqual(webpage["description"], expected_description)

    def test_only_br_is_allowed_in_whitelisted_content_fields(self):
        def inject_markup(data):
            data["pages"]["cabinet"]["silhouette_label"] = "PACKAGED<br><em>CONTROL</em>"

        self.assert_fact_drift_fails_without_writes(
            inject_markup,
            r"Unsafe HTML markup: zh: pages\.cabinet\.silhouette_label",
        )

    def test_all_product_fragments_localize_single_quoted_routes_with_query_and_hash(self):
        self.write_content("en")
        self.write_content("ja")
        template_dir = self.fixture_root / "product-templates"
        shutil.copytree(PUBLIC / "product-templates", template_dir)
        english_route = route_for("en", "comparison")
        localized_route = route_for("ja", "comparison")
        suffix = "?source=fixture#selection"
        for template_path in template_dir.glob("*.html"):
            template_path.write_text(
                template_path.read_text(encoding="utf-8")
                + f"\n<a href='{english_route}{suffix}'>fixture route</a>\n",
                encoding="utf-8",
            )

        self.build(("ja",), template_dir=template_dir)

        for page_key in self.PRODUCT_PAGE_KEYS:
            with self.subTest(page_key=page_key):
                rendered = output_path(self.fixture_public, "ja", page_key).read_text(
                    encoding="utf-8"
                )
                self.assertIn(f"href='{localized_route}{suffix}'", rendered)
                self.assertNotIn(f"href='{english_route}", rendered)

    def test_encoded_residual_english_product_route_fails_without_writes(self):
        self.write_content("en")
        self.write_content("ja")
        template_dir = self.fixture_root / "product-templates"
        shutil.copytree(PUBLIC / "product-templates", template_dir)
        template_path = template_dir / "psa-nitrogen-generation-system.html"
        template_path.write_text(
            template_path.read_text(encoding="utf-8")
            + '\n<a href="&#47;products/mixed-gas-control-comparison">fixture route</a>\n',
            encoding="utf-8",
        )
        english_output = output_path(self.fixture_public, "en", "psa")
        japanese_output = output_path(self.fixture_public, "ja", "psa")
        for path, sentinel in (
            (english_output, "unchanged english"),
            (japanese_output, "unchanged japanese"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(sentinel, encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError,
            r"Unlocalized product route: ja: /products/mixed-gas-control-comparison",
        ):
            self.build(("en", "ja"), template_dir=template_dir)

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")
        self.assertEqual(japanese_output.read_text(encoding="utf-8"), "unchanged japanese")

    def test_cli_unknown_locale_exits_nonzero_with_clear_error(self):
        result = subprocess.run(
            ["python", "build-product-pages.py", "--locale", "xx"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported locale: xx", result.stderr)


class HomepageGenerationTests(unittest.TestCase):
    MINIMAL_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="canonical" href="https://gasmixtech.com/">
  <meta property="og:url" content="https://gasmixtech.com/">
</head>
<body>
  <a href="/contact">Contact</a>
  <span class="lang-current">EN</span>
  <a href="/" class="lang-option active" data-lang="en">English</a>
  <a href="/zh/" class="lang-option" data-lang="zh">中文</a>
  <a href="/es/" class="lang-option" data-lang="es">Español</a>
  <a href="/pt/" class="lang-option" data-lang="pt">Português</a>
  <a href="/ja/" class="lang-option" data-lang="ja">日本語</a>
  <a href="/ko/" class="lang-option" data-lang="ko">한국어</a>
  <a href="/pl/" class="lang-option" data-lang="pl">Polski</a>
  <p>{{message}}</p>
</body>
</html>
"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temp_dir.name)
        self.fixture_public = self.fixture_root / "public"
        self.fixture_i18n = self.fixture_public / "i18n"
        self.fixture_i18n.mkdir(parents=True)
        shutil.copy2(PUBLIC / "build-i18n.js", self.fixture_public / "build-i18n.js")
        (self.fixture_public / "_template.html").write_text(self.MINIMAL_TEMPLATE, encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_translation(self, locale, data=None):
        content = json.dumps(data if data is not None else {"message": locale})
        (self.fixture_i18n / f"{locale}.json").write_text(content, encoding="utf-8")

    def write_output(self, locale, content):
        path = self.fixture_public / "index.html" if locale == "en" else self.fixture_public / locale / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_node(self, *args):
        return subprocess.run(
            ["node", "public/build-i18n.js", *args],
            cwd=self.fixture_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def run_node_eval(self, script):
        return subprocess.run(
            ["node", "-e", script],
            cwd=self.fixture_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def create_real_source_fixture(self, root):
        fixture_public = root / "public"
        fixture_i18n = fixture_public / "i18n"
        fixture_i18n.mkdir(parents=True)
        shutil.copy2(PUBLIC / "build-i18n.js", fixture_public / "build-i18n.js")
        shutil.copy2(PUBLIC / "_template.html", fixture_public / "_template.html")
        for locale in SUPPORTED_LOCALES:
            source = PUBLIC / "i18n" / f"{locale}.json"
            if source.exists():
                shutil.copy2(source, fixture_i18n / source.name)
        return fixture_public

    def assert_matches_committed_homepage(self, fixture_public, locale):
        actual = output_path(fixture_public, locale, "home").read_text(encoding="utf-8")
        expected = output_path(PUBLIC, locale, "home").read_text(encoding="utf-8")
        if actual != expected:
            difference = "".join(
                list(
                    difflib.unified_diff(
                        expected.splitlines(keepends=True),
                        actual.splitlines(keepends=True),
                        fromfile=f"committed/{locale}",
                        tofile=f"rebuilt/{locale}",
                        n=1,
                    )
                )[:80]
            )
            self.fail(f"Rebuilt {locale} homepage differs from committed output:\n{difference}")

    def test_generated_homepages_have_complete_locale_aware_core_links(self):
        core_page_keys = ("about", "contact", "psa", "cabinet", "valve", "comparison")

        for locale in SUPPORTED_LOCALES:
            with self.subTest(locale=locale):
                html = output_path(PUBLIC, locale, "home").read_text(encoding="utf-8")
                self.assertNotIn("{{", html)
                self.assertEqual(html.count('class="lang-option'), 7)
                for page_key in core_page_keys:
                    self.assertIn(f'href="{route_for(locale, page_key)}', html)
                    if locale != "en":
                        self.assertNotIn(f'href="{CORE_ROUTES[page_key]}', html)

    def test_missing_translation_key_fails_closed(self):
        result = self.run_node_eval(
            "const { replacePlaceholders } = require('./public/build-i18n.js'); "
            "replacePlaceholders('{{missing.required.key}}', {});"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing translation key: missing.required.key", result.stderr)

    def test_javascript_supported_locales_match_python_contract(self):
        result = self.run_node_eval(
            "const { SUPPORTED_LOCALES } = require('./public/build-i18n.js'); "
            "process.stdout.write(JSON.stringify(SUPPORTED_LOCALES));"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(tuple(json.loads(result.stdout)), SUPPORTED_LOCALES)

    def test_generated_switcher_marks_current_locale_and_keeps_all_links(self):
        for locale in SUPPORTED_LOCALES:
            self.write_translation(locale)

        result = self.run_node()

        self.assertEqual(result.returncode, 0, result.stderr)
        for locale in SUPPORTED_LOCALES:
            with self.subTest(locale=locale):
                html = output_path(self.fixture_public, locale, "home").read_text(encoding="utf-8")
                self.assertIn(f'<span class="lang-current">{locale.upper()}</span>', html)
                self.assertEqual(html.count('class="lang-option'), len(SUPPORTED_LOCALES))
                self.assertEqual(html.count('class="lang-option active"'), 1)
                for option_locale in SUPPORTED_LOCALES:
                    active = " active" if option_locale == locale else ""
                    expected = (
                        f'href="{route_for(option_locale, "home")}" '
                        f'class="lang-option{active}" data-lang="{option_locale}"'
                    )
                    self.assertIn(expected, html)

    def test_real_sources_rebuild_each_existing_homepage_exactly(self):
        generated_locales = SUPPORTED_LOCALES[:-1]
        for locale in generated_locales:
            with self.subTest(locale=locale), tempfile.TemporaryDirectory() as temp_dir:
                fixture_root = Path(temp_dir)
                fixture_public = self.create_real_source_fixture(fixture_root)

                result = subprocess.run(
                    ["node", "public/build-i18n.js", "--locale", locale],
                    cwd=fixture_root,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_matches_committed_homepage(fixture_public, locale)

    def test_real_sources_batch_rebuild_existing_homepages_exactly(self):
        generated_locales = SUPPORTED_LOCALES[:-1]
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_root = Path(temp_dir)
            fixture_public = self.create_real_source_fixture(fixture_root)
            args = [value for locale in generated_locales for value in ("--locale", locale)]

            result = subprocess.run(
                ["node", "public/build-i18n.js", *args],
                cwd=fixture_root,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            for locale in generated_locales:
                with self.subTest(locale=locale):
                    self.assert_matches_committed_homepage(fixture_public, locale)

    def test_adjust_paths_respects_core_route_boundaries(self):
        result = self.run_node_eval(
            "const { adjustPaths } = require('./public/build-i18n.js'); "
            "const input = ["
            "'<a href=\"/contact\">exact</a>',"
            "'<a href=\"/contact?topic=quote\">query</a>',"
            "'<a href=\"/contact#form\">hash</a>',"
            "'<a href=\"/contact-us\">prefix</a>',"
            "'<a href=\"/products/mixed-gas-control-comparison-v2\">versioned</a>',"
            "'<a href=\"/ja/contact\">localized</a>'"
            "].join('\\n'); "
            "const once = adjustPaths(input, 'ja'); "
            "process.stdout.write(JSON.stringify({ once, twice: adjustPaths(once, 'ja') }));"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout)
        self.assertIn('href="/ja/contact"', values["once"])
        self.assertIn('href="/ja/contact?topic=quote"', values["once"])
        self.assertIn('href="/ja/contact#form"', values["once"])
        self.assertIn('href="/contact-us"', values["once"])
        self.assertIn('href="/products/mixed-gas-control-comparison-v2"', values["once"])
        self.assertEqual(values["once"], values["twice"])

    def test_single_locale_build_writes_only_selected_output(self):
        self.write_translation("ja")
        english_output = self.write_output("en", "unchanged english")

        result = self.run_node("--locale", "ja")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")
        self.assertIn("ja", (self.fixture_public / "ja" / "index.html").read_text(encoding="utf-8"))
        self.assertFalse((self.fixture_public / "zh" / "index.html").exists())

    def test_repeatable_locale_option_writes_only_selected_homepages(self):
        self.write_translation("en")
        self.write_translation("zh")
        spanish_output = self.write_output("es", "unchanged spanish")

        result = self.run_node("--locale", "en", "--locale", "zh")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("en", (self.fixture_public / "index.html").read_text(encoding="utf-8"))
        self.assertIn("zh", (self.fixture_public / "zh" / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(spanish_output.read_text(encoding="utf-8"), "unchanged spanish")

    def test_unknown_locale_fails_with_clear_error(self):
        english_output = self.write_output("en", "unchanged english")

        result = self.run_node("--locale", "xx")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported locale: xx", result.stderr)
        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

    def test_locale_option_requires_a_value(self):
        english_output = self.write_output("en", "unchanged english")

        result = self.run_node("--locale")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing value for --locale", result.stderr)
        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

    def test_missing_locale_translation_file_fails_closed(self):
        polish_output = self.write_output("pl", "unchanged polish")

        result = self.run_node("--locale", "pl")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing translation file: pl.json", result.stderr)
        self.assertEqual(polish_output.read_text(encoding="utf-8"), "unchanged polish")

    def test_missing_key_does_not_write_partial_outputs(self):
        self.write_translation("en")
        self.write_translation("zh", {})
        english_output = self.write_output("en", "unchanged english")

        result = self.run_node("--locale", "en", "--locale", "zh")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing translation key: message", result.stderr)
        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")
        self.assertFalse((self.fixture_public / "zh" / "index.html").exists())

    def test_invalid_json_does_not_write_partial_outputs(self):
        self.write_translation("en")
        (self.fixture_i18n / "zh.json").write_text("{invalid", encoding="utf-8")
        english_output = self.write_output("en", "unchanged english")

        result = self.run_node("--locale", "en", "--locale", "zh")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid translation JSON: zh.json", result.stderr)
        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")
        self.assertFalse((self.fixture_public / "zh" / "index.html").exists())
