from collections import Counter
import difflib
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
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
from tests.test_inquiry_form_markup import assert_inquiry_contract

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

PRODUCT_BUILDER_SPEC = importlib.util.spec_from_file_location(
    "build_product_pages",
    ROOT / "build-product-pages.py",
)
PRODUCT_BUILDER = importlib.util.module_from_spec(PRODUCT_BUILDER_SPEC)
PRODUCT_BUILDER_SPEC.loader.exec_module(PRODUCT_BUILDER)

CORE_BUILDER_PATH = ROOT / "build-static-core-pages.py"
APPROVED_CORE_PAGE_SHA256 = {
    "about": "6e1778c87ce105001c4ec9fa99715de8a0a78adf258e5c5a5c83cc71fc806e06",
    "contact": "6aae65975ba8daab26a459afb7ea82933ec7080db7bce07b2cf3d78d2de1a140",
}


def load_core_builder():
    spec = importlib.util.spec_from_file_location("build_static_core_pages", CORE_BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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

    def test_english_comparison_row_key_cannot_be_empty(self):
        def empty_stable_key(data):
            data["pages"]["comparison"]["comparison_rows"][0]["key"] = ""

        self.write_content("en", empty_stable_key)
        english_output = output_path(self.fixture_public, "en", "comparison")
        english_output.parent.mkdir(parents=True, exist_ok=True)
        english_output.write_text("unchanged english", encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError,
            r"Invalid stable key: en: pages\.comparison\.comparison_rows\.0\.key",
        ):
            self.build(("en",))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

    def test_english_comparison_row_keys_must_be_unique(self):
        def duplicate_stable_key(data):
            rows = data["pages"]["comparison"]["comparison_rows"]
            rows[1]["key"] = rows[0]["key"]

        self.write_content("en", duplicate_stable_key)
        english_output = output_path(self.fixture_public, "en", "comparison")
        english_output.parent.mkdir(parents=True, exist_ok=True)
        english_output.write_text("unchanged english", encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError,
            r"Duplicate stable key: en: pages\.comparison\.comparison_rows\.1\.key",
        ):
            self.build(("en",))

        self.assertEqual(english_output.read_text(encoding="utf-8"), "unchanged english")

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

    def test_same_site_absolute_product_routes_localize_without_touching_external_links(self):
        self.write_content("en")
        self.write_content("ja")
        template_dir = self.fixture_root / "product-templates"
        shutil.copytree(PUBLIC / "product-templates", template_dir)
        template_path = template_dir / "mixed-gas-control-comparison.html"
        english_path = route_for("en", "comparison")
        localized_path = route_for("ja", "comparison")
        suffix = "?source=fixture#selection"
        template_path.write_text(
            template_path.read_text(encoding="utf-8")
            + f'''\n<a href="https://gasmixtech.com{english_path}">absolute</a>
<a href="https://gasmixtech.com{english_path}{suffix}">absolute suffix</a>
<a href="//gasmixtech.com{english_path}">protocol relative</a>
<a href="//gasmixtech.com{english_path}{suffix}">protocol relative suffix</a>
<a href="https://example.com{english_path}{suffix}">external</a>
<a href="mailto:sales@gasmixtech.com">email</a>
<a href="https://www.dhgate.com/store/21807795">DHgate</a>\n''',
            encoding="utf-8",
        )

        self.build(("ja",), template_dir=template_dir)

        rendered = output_path(self.fixture_public, "ja", "comparison").read_text(
            encoding="utf-8"
        )
        self.assertIn(f'href="https://gasmixtech.com{localized_path}"', rendered)
        self.assertIn(
            f'href="https://gasmixtech.com{localized_path}{suffix}"', rendered
        )
        self.assertIn(f'href="//gasmixtech.com{localized_path}"', rendered)
        self.assertIn(
            f'href="//gasmixtech.com{localized_path}{suffix}"', rendered
        )
        self.assertIn(
            f'href="https://example.com{english_path}{suffix}"', rendered
        )
        self.assertIn('href="mailto:sales@gasmixtech.com"', rendered)
        self.assertIn('href="https://www.dhgate.com/store/21807795"', rendered)

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


class StaticCoreRendererTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_core_builder()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temp_dir.name)
        self.fixture_public = self.fixture_root / "public"
        self.fixture_content = self.fixture_public / "i18n" / "core"
        self.fixture_templates = self.fixture_public / "core-page-templates"
        self.fixture_content.mkdir(parents=True)
        shutil.copytree(PUBLIC / "core-page-templates", self.fixture_templates)
        self.english_content = json.loads(
            (PUBLIC / "i18n" / "core" / "en.json").read_text(encoding="utf-8")
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_content(self, locale, data=None):
        content = json.loads(json.dumps(data or self.english_content))
        content["locale"] = locale
        (self.fixture_content / f"{locale}.json").write_text(
            json.dumps(content, ensure_ascii=False), encoding="utf-8"
        )
        return content

    def build(self, locales):
        return self.builder.build_pages(
            locales,
            public_dir=self.fixture_public,
            content_dir=self.fixture_content,
            template_dir=self.fixture_templates,
        )

    def test_real_english_pages_render_complete_locale_contract(self):
        self.write_content("en")
        self.build(("en",))

        for page_key in ("about", "contact"):
            with self.subTest(page_key=page_key):
                rendered = output_path(self.fixture_public, "en", page_key).read_text(encoding="utf-8")
                self.assertNotIn("{{", rendered)
                self.assertNotIn("}}", rendered)
                self.assertEqual(len(re.findall(r"<h1(?:\s[^>]*)?>", rendered)), 1)
                self.assertEqual(rendered.count('class="lang-option'), len(SUPPORTED_LOCALES))
                self.assertEqual(rendered.count('class="lang-option active"'), 1)
                self.assertIn('<html lang="en">', rendered)
                self.assertEqual(
                    rendered.count(f'<link rel="canonical" href="{canonical_url("en", page_key)}">'),
                    1,
                )
                for alternate_locale, url in alternates_for(page_key).items():
                    self.assertEqual(
                        rendered.count(
                            f'<link rel="alternate" hreflang="{alternate_locale}" href="{url}">'
                        ),
                        1,
                    )
                for option_locale in SUPPORTED_LOCALES:
                    active = " active" if option_locale == "en" else ""
                    self.assertIn(
                        f'href="{route_for(option_locale, page_key)}" '
                        f'class="lang-option{active}" data-lang="{option_locale}"',
                        rendered,
                    )

        contact_html = output_path(self.fixture_public, "en", "contact").read_text(encoding="utf-8")
        assert_inquiry_contract(self, contact_html)

    def test_real_english_templates_rebuild_approved_pages_byte_for_byte(self):
        self.write_content("en")
        self.build(("en",))

        for page_key in ("about", "contact"):
            with self.subTest(page_key=page_key):
                expected = output_path(PUBLIC, "en", page_key).read_bytes().replace(
                    b"\r\n", b"\n"
                )
                actual = output_path(self.fixture_public, "en", page_key).read_bytes()
                self.assertEqual(actual, expected)
                self.assertNotIn(b"\r\n", actual)
                self.assertEqual(
                    hashlib.sha256(actual).hexdigest(),
                    APPROVED_CORE_PAGE_SHA256[page_key],
                )

    def test_lf_and_crlf_template_inputs_render_and_build_identically(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        template_lf = '<div title="{{attr:shared.home}}">{{text:shared.home}}</div>\n'
        template_crlf = template_lf.replace("\n", "\r\n")
        self.assertEqual(
            self.builder.render_page("en", "about", template_lf, content),
            self.builder.render_page("en", "about", template_crlf, content),
        )

        self.write_content("en")
        outputs = []
        for newline, suffix in (("\n", "lf"), ("\r\n", "crlf")):
            template_dir = self.fixture_root / f"templates-{suffix}"
            template_dir.mkdir()
            for page_key in ("about", "contact"):
                template = (PUBLIC / "core-page-templates" / f"{page_key}.html").read_text(
                    encoding="utf-8"
                )
                with (template_dir / f"{page_key}.html").open(
                    "w", encoding="utf-8", newline=""
                ) as handle:
                    handle.write(template.replace("\r\n", "\n").replace("\n", newline))
            public_dir = self.fixture_root / f"output-{suffix}"
            self.builder.build_pages(
                ("en",),
                public_dir=public_dir,
                content_dir=self.fixture_content,
                template_dir=template_dir,
            )
            page_bytes = tuple(
                output_path(public_dir, "en", page_key).read_bytes()
                for page_key in ("about", "contact")
            )
            for rendered in page_bytes:
                self.assertNotIn(b"\r\n", rendered)
            outputs.append(page_bytes)

        self.assertEqual(outputs[0], outputs[1])

    def test_all_translation_leaves_must_be_used_before_writing(self):
        content = self.write_content("en")
        content["contact"]["unused_fixture"] = "must fail"
        self.write_content("en", content)
        destination = output_path(self.fixture_public, "en", "about")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("unchanged", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, r"Unused content keys: contact\.unused_fixture"):
            self.build(("en",))

        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
        self.assertFalse(output_path(self.fixture_public, "en", "contact").exists())

    def test_non_reusable_translation_key_must_be_used_exactly_once(self):
        self.write_content("en")
        template_path = self.fixture_templates / "about.html"
        template_path.write_text(
            template_path.read_text(encoding="utf-8")
            + "\n<p>{{text:about.copy.who_we_are}}</p>\n",
            encoding="utf-8",
        )
        destination = output_path(self.fixture_public, "en", "about")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("unchanged", encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError,
            r"Invalid content key usage: about\.copy\.who_we_are: actual 2, allowed 1",
        ):
            self.build(("en",))

        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
        self.assertFalse(output_path(self.fixture_public, "en", "contact").exists())

    def test_reusable_translation_key_has_an_exact_allowed_count(self):
        self.assertEqual(self.builder.REUSABLE_KEYS["contact.copy.select_one"], 8)
        self.write_content("en")
        self.build(("en",))

        template_path = self.fixture_templates / "contact.html"
        template_path.write_text(
            template_path.read_text(encoding="utf-8")
            + "\n<p>{{text:contact.copy.select_one}}</p>\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            ValueError,
            r"Invalid content key usage: contact\.copy\.select_one: actual 9, allowed 8",
        ):
            self.build(("en",))

    def test_required_key_still_fails_when_the_templates_do_not_use_it(self):
        self.write_content("en")
        template_path = self.fixture_templates / "about.html"
        template = template_path.read_text(encoding="utf-8")
        for placeholder in (
            "{{text:about.title}}",
            "{{attr:about.title}}",
            "{{json:about.title}}",
        ):
            template = template.replace(placeholder, "Gas Mixing Device Supplier in China | About Us")
        template_path.write_text(template, encoding="utf-8")
        destination = output_path(self.fixture_public, "en", "about")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("unchanged", encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError,
            r"Unused content keys: about\.title \(actual 0, allowed \d+\)",
        ):
            self.build(("en",))

        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
        self.assertFalse(output_path(self.fixture_public, "en", "contact").exists())

    def test_missing_translation_key_fails_without_writes(self):
        content = self.write_content("en")
        del content["shared"]["products"]
        self.write_content("en", content)
        destination = output_path(self.fixture_public, "en", "about")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("unchanged", encoding="utf-8")

        with self.assertRaisesRegex(KeyError, r"Missing content key: shared\.products"):
            self.build(("en",))

        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
        self.assertFalse(output_path(self.fixture_public, "en", "contact").exists())

    def test_required_core_keys_must_exist_as_non_empty_strings(self):
        required_paths = (
            "shared.language_label", "shared.home", "shared.products",
            "shared.applications", "shared.results", "shared.resources",
            "shared.about", "shared.request", "about.title", "about.description",
            "contact.title", "contact.description",
        )
        for path in required_paths:
            for replacement in (None, "", "   ", []):
                with self.subTest(path=path, replacement=replacement):
                    content = json.loads(json.dumps(self.english_content))
                    parent = content
                    parts = path.split(".")
                    for part in parts[:-1]:
                        parent = parent[part]
                    if replacement is None:
                        del parent[parts[-1]]
                    else:
                        parent[parts[-1]] = replacement
                    self.write_content("en", content)
                    destination = output_path(self.fixture_public, "en", "about")
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text("unchanged", encoding="utf-8")
                    with self.assertRaisesRegex(
                        (KeyError, ValueError),
                        rf"Required content key.*{re.escape(path)}|Missing content key: {re.escape(path)}",
                    ):
                        self.build(("en",))
                    self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")

    def test_unknown_empty_and_scalar_content_structures_fail_without_writes(self):
        for value in ({}, [], "unexpected"):
            with self.subTest(value=value):
                content = json.loads(json.dumps(self.english_content))
                content["contact"]["unknown_fixture"] = value
                self.write_content("en", content)
                destination = output_path(self.fixture_public, "en", "about")
                contact_destination = output_path(self.fixture_public, "en", "contact")
                contact_destination.unlink(missing_ok=True)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text("unchanged", encoding="utf-8")
                with self.assertRaisesRegex(
                    ValueError, r"Unused content keys: contact\.unknown_fixture"
                ):
                    self.build(("en",))
                self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
                self.assertFalse(contact_destination.exists())

    def test_every_translation_string_must_be_non_empty(self):
        content = json.loads(json.dumps(self.english_content))
        content["about"]["copy"]["who_we_are"] = "   "
        self.write_content("en", content)
        destination = output_path(self.fixture_public, "en", "about")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("unchanged", encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError,
            r"Translation content key must be a non-empty string: about\.copy\.who_we_are",
        ):
            self.build(("en",))

        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
        self.assertFalse(output_path(self.fixture_public, "en", "contact").exists())

        with self.assertRaisesRegex(
            ValueError,
            r"Translation content key must be a non-empty string: shared\.home",
        ):
            self.builder.render_page(
                "en",
                "about",
                "<p>{{text:shared.home}}</p>",
                {"locale": "en", "shared": {"home": ""}},
            )

    def test_bad_translation_files_fail_closed(self):
        cases = (
            ("{invalid", "Invalid translation JSON: en.json"),
            (json.dumps([]), "Invalid translation root: en.json"),
            (json.dumps({"locale": "zh"}), "Translation locale mismatch: en.json"),
        )
        for raw, message in cases:
            with self.subTest(message=message):
                (self.fixture_content / "en.json").write_text(raw, encoding="utf-8")
                destination = output_path(self.fixture_public, "en", "about")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text("unchanged", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, re.escape(message)):
                    self.build(("en",))
                self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
                self.assertFalse(output_path(self.fixture_public, "en", "contact").exists())

    def test_duplicate_json_object_key_fails_without_writes(self):
        source = (PUBLIC / "i18n" / "core" / "en.json").read_text(encoding="utf-8")
        cases = (
            (
                source.replace('"locale": "en"', '"locale": "en",\n  "locale": "en"', 1),
                "locale",
            ),
            (
                source.replace('"home": "Home"', '"home": "Home",\n    "home": "Home"', 1),
                "home",
            ),
        )
        for raw, duplicate_key in cases:
            with self.subTest(duplicate_key=duplicate_key):
                (self.fixture_content / "en.json").write_text(raw, encoding="utf-8")
                destination = output_path(self.fixture_public, "en", "about")
                contact_destination = output_path(self.fixture_public, "en", "contact")
                contact_destination.unlink(missing_ok=True)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text("unchanged", encoding="utf-8")

                with self.assertRaisesRegex(
                    ValueError,
                    rf"Duplicate translation key in en\.json: {duplicate_key}",
                ):
                    self.build(("en",))

                self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")
                self.assertFalse(contact_destination.exists())

    def test_missing_translation_file_fails_without_writes(self):
        destination = output_path(self.fixture_public, "en", "about")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("unchanged", encoding="utf-8")

        with self.assertRaisesRegex(FileNotFoundError, "en.json"):
            self.build(("en",))

        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")

    def test_text_attributes_and_jsonld_escape_translation_content(self):
        payload = 'Consult "A&B" <unsafe> </script>'
        content = {"locale": "en", "shared": {"home": payload}}
        template = (
            '<head>{{safe:hreflang_links}}'
            '<script type="application/ld+json">{"name":{{json:shared.home}}}</script>'
            '</head><body><p>{{text:shared.home}}</p>'
            '<div title="{{attr:shared.home}}"></div>'
            '<div class="lang-dropdown" id="langDropdown">{{safe:language_menu}}</div>'
            '</body>'
        )

        rendered = self.builder.render_page("en", "about", template, content)

        self.assertIn('Consult "A&amp;B" &lt;unsafe&gt; &lt;/script&gt;', rendered)
        self.assertIn('title="Consult &quot;A&amp;B&quot; &lt;unsafe&gt; &lt;/script&gt;"', rendered)
        json_text = re.search(
            r'<script type="application/ld\+json">(.*?)</script>', rendered
        ).group(1)
        self.assertEqual(json.loads(json_text)["name"], payload)
        self.assertNotIn("<unsafe>", rendered)
        self.assertNotIn("</script></script>", rendered)

    def test_placeholder_types_are_accepted_only_in_their_approved_contexts(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        accepted = (
            '<p>{{text:shared.home}}</p>',
            '<div title="{{attr:shared.home}}"></div>',
            '<script type="application/ld+json">{"name":{{json:shared.home}}}</script>',
            '<head>{{safe:hreflang_links}}</head>',
            '<div class="lang-dropdown" id="langDropdown">{{safe:language_menu}}</div>',
        )
        for template in accepted:
            with self.subTest(accepted=template):
                rendered = self.builder.render_page("en", "about", template, content)
                self.assertNotIn("{{", rendered)

        rejected = (
            '<div title="{{text:shared.home}}"></div>',
            '<div title="{{json:shared.home}}"></div>',
            '<div title="{{safe:language_menu}}"></div>',
            '<p>{{attr:shared.home}}</p>',
            '<p>{{json:shared.home}}</p>',
            '<script>{{text:shared.home}}</script>',
            '<style>{{text:shared.home}}</style>',
            '<script type="application/ld+json">{{safe:language_menu}}</script>',
            '<script type="text/javascript">{{json:shared.home}}</script>',
            '<scripture type="application/ld+json">{{json:shared.home}}</scripture>',
            '<p>{{safe:hreflang_links}}</p>',
        )
        for template in rejected:
            with self.subTest(rejected=template):
                with self.assertRaisesRegex(ValueError, "placeholder context"):
                    self.builder.render_page("en", "about", template, content)

    def test_text_placeholder_in_attribute_is_rejected_before_payload_rendering(self):
        payload = 'x" onmouseover="alert(1)'
        with self.assertRaisesRegex(ValueError, "placeholder context"):
            self.builder.render_page(
                "en",
                "about",
                '<div title="{{text:shared.home}}"></div>',
                {"locale": "en", "shared": {"home": payload}},
            )

    def test_greater_than_inside_an_attribute_cannot_hide_text_placeholder_context(self):
        payload = 'x" onmouseover="alert(1)'
        with self.assertRaisesRegex(ValueError, "placeholder context"):
            self.builder.render_page(
                "en",
                "about",
                '<div data-note=">" title="{{text:shared.home}}"></div>',
                {"locale": "en", "shared": {"home": payload}},
            )

    def test_quoted_angle_brackets_do_not_change_attribute_or_text_context(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        for quoted_note in ('data-note="> <"', "data-note='> <'"):
            with self.subTest(quoted_note=quoted_note):
                with self.assertRaisesRegex(ValueError, "placeholder context"):
                    self.builder.render_page(
                        "en",
                        "about",
                        f'<div {quoted_note} title="{{{{text:shared.home}}}}"></div>',
                        content,
                    )
                rendered = self.builder.render_page(
                    "en",
                    "about",
                    f'<div {quoted_note} title="{{{{attr:shared.home}}}}">'
                    "{{text:shared.home}}</div>",
                    content,
                )
                self.assertIn('title="Home">Home</div>', rendered)

    def test_comments_raw_text_and_malformed_templates_are_fail_closed(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        try:
            valid_json = self.builder.render_page(
                "en",
                "about",
                '<script data-note="> <" type="application/ld+json">'
                '{"name":{{json:shared.home}}}</script>',
                content,
            )
        except ValueError as exc:
            self.fail(f"Quoted angle bracket changed the script context: {exc}")
        json_text = valid_json.split('type="application/ld+json">', 1)[1].rsplit(
            "</script>", 1
        )[0]
        self.assertEqual(json.loads(json_text)["name"], "Home")
        self.assertEqual(
            self.builder.render_page(
                "en",
                "about",
                '<div data-note="> <">{{text:shared.home}}</div>',
                content,
            ),
            '<div data-note="> <">Home</div>',
        )

        rejected = (
            '<!-- note > {{text:shared.home}} -->',
            '<script data-note="> <">{{text:shared.home}}</script>',
            "<style data-note='> <'>{{text:shared.home}}</style>",
            '<div title="unterminated>{{attr:shared.home}}</div>',
            '<div title="unterminated',
            '<!-- unterminated',
            '<script type="application/ld+json">{"name":"unterminated"}',
            '<style>unterminated',
        )
        for template in rejected:
            with self.subTest(template=template):
                with self.assertRaisesRegex(ValueError, "template context|placeholder context"):
                    self.builder.render_page("en", "about", template, content)

    def test_json_context_uses_the_parsed_script_type_attribute(self):
        template = (
            "<script data-note='type=\"application/ld+json\"' "
            'type="text/javascript">{{json:shared.home}}</script>'
        )
        with self.assertRaisesRegex(ValueError, "placeholder context"):
            self.builder.render_page(
                "en",
                "about",
                template,
                {"locale": "en", "shared": {"home": "Home"}},
            )

    def test_safe_menu_context_uses_parsed_class_and_id_attributes(self):
        template = (
            "<div data-note='class=\"lang-dropdown\" id=\"langDropdown\"'>"
            "{{safe:language_menu}}</div>"
        )
        with self.assertRaisesRegex(ValueError, "placeholder context"):
            self.builder.render_page(
                "en",
                "about",
                template,
                {"locale": "en", "shared": {"home": "Home"}},
            )

    def test_duplicate_context_attributes_are_rejected(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        templates = (
            '<script type="application/ld+json" type="application/ld+json">'
            "{{json:shared.home}}</script>",
            '<div class="lang-dropdown" class="lang-dropdown" id="langDropdown">'
            "{{safe:language_menu}}</div>",
            '<div class="lang-dropdown" id="langDropdown" id="langDropdown">'
            "{{safe:language_menu}}</div>",
        )
        for template in templates:
            with self.subTest(template=template):
                with self.assertRaisesRegex(ValueError, "Duplicate HTML attribute"):
                    self.builder.render_page("en", "about", template, content)

    def test_every_non_void_element_must_close_in_stack_order(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        templates = (
            "<p>{{text:shared.home}}",
            "</span><p>{{text:shared.home}}</p>",
            "<p><span>{{text:shared.home}}</p></span>",
        )
        for template in templates:
            with self.subTest(template=template):
                with self.assertRaisesRegex(ValueError, "template context"):
                    self.builder.render_page("en", "about", template, content)

    def test_hreflang_safe_block_requires_head_as_direct_parent(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        with self.assertRaisesRegex(ValueError, "placeholder context"):
            self.builder.render_page(
                "en",
                "about",
                "<head><div>{{safe:hreflang_links}}</div></head>",
                content,
            )

    def test_malformed_tag_syntax_fails_before_rendering_or_writing(self):
        self.write_content("en")
        template_path = self.fixture_templates / "about.html"
        original = template_path.read_text(encoding="utf-8")
        malformed = (
            '<div/>{{text:shared.home}}',
            '<p>{{text:shared.home}}</p junk>',
            '<p / junk>{{text:shared.home}}</p>',
        )
        for suffix in malformed:
            with self.subTest(suffix=suffix):
                template_path.write_text(original + suffix, encoding="utf-8")
                about_output = output_path(self.fixture_public, "en", "about")
                contact_output = output_path(self.fixture_public, "en", "contact")
                about_output.parent.mkdir(parents=True, exist_ok=True)
                about_output.write_text("unchanged about", encoding="utf-8")
                contact_output.write_text("unchanged contact", encoding="utf-8")

                with self.assertRaisesRegex(ValueError, "template context"):
                    self.build(("en",))

                self.assertEqual(about_output.read_text(encoding="utf-8"), "unchanged about")
                self.assertEqual(contact_output.read_text(encoding="utf-8"), "unchanged contact")

    def test_bogus_template_tokens_fail_before_rendering_or_writing(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        malformed = (
            "< p>{{text:shared.home}}</ p>",
            "<1>{{text:shared.home}}</1>",
            "<!oops>{{text:shared.home}}",
            "<?oops>{{text:shared.home}}",
        )
        for template in malformed:
            with self.subTest(template=template):
                with self.assertRaisesRegex(ValueError, "malformed template syntax"):
                    self.builder.render_page("en", "about", template, content)

        self.write_content("en")
        template_path = self.fixture_templates / "about.html"
        original = template_path.read_text(encoding="utf-8")
        for suffix in malformed:
            with self.subTest(build_suffix=suffix):
                template_path.write_text(original + suffix, encoding="utf-8")
                about_output = output_path(self.fixture_public, "en", "about")
                contact_output = output_path(self.fixture_public, "en", "contact")
                about_output.parent.mkdir(parents=True, exist_ok=True)
                about_output.write_text("unchanged about", encoding="utf-8")
                contact_output.write_text("unchanged contact", encoding="utf-8")

                with self.assertRaisesRegex(ValueError, "malformed template syntax"):
                    self.build(("en",))

                self.assertEqual(about_output.read_text(encoding="utf-8"), "unchanged about")
                self.assertEqual(contact_output.read_text(encoding="utf-8"), "unchanged contact")

    def test_escaped_less_than_and_json_unicode_escape_are_valid_data(self):
        rendered = self.builder.render_page(
            "en",
            "about",
            '<p>&lt; {{text:shared.home}}</p>'
            '<script type="application/ld+json">'
            '{"marker":"\\u003c","name":{{json:shared.home}}}</script>',
            {"locale": "en", "shared": {"home": "Home"}},
        )
        self.assertIn("<p>&lt; Home</p>", rendered)
        self.assertEqual(
            json.loads(rendered.split('<script type="application/ld+json">', 1)[1]
                       .split("</script>", 1)[0])["marker"],
            "<",
        )

    def test_only_normalized_html_doctype_declarations_are_allowed(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        rendered = self.builder.render_page(
            "en",
            "about",
            "<!doctype\n  HTML><p>{{text:shared.home}}</p>",
            content,
        )
        self.assertEqual(rendered, "<!doctype\n  HTML><p>Home</p>")

        for declaration in ("<!DOCTYPE svg>", "<![CDATA[oops]]>", "<![oops]>"):
            with self.subTest(declaration=declaration):
                with self.assertRaisesRegex(ValueError, "malformed template syntax"):
                    self.builder.render_page(
                        "en",
                        "about",
                        declaration + "<p>{{text:shared.home}}</p>",
                        content,
                    )

    def test_slashes_in_attribute_values_and_svg_self_closing_tags_are_valid(self):
        rendered = self.builder.render_page(
            "en",
            "about",
            '<div data-path="/products/a/b">{{text:shared.home}}'
            '<svg><path d="M0/1" /></svg></div>',
            {"locale": "en", "shared": {"home": "Home"}},
        )
        self.assertIn('data-path="/products/a/b">Home', rendered)

    def test_single_quote_payload_cannot_create_a_new_attribute(self):
        payload = "x' onmouseover='alert(1)"
        rendered = self.builder.render_page(
            "en",
            "about",
            '<div title="{{attr:shared.home}}"></div>',
            {"locale": "en", "shared": {"home": payload}},
        )

        class AttributeParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.attrs = None

            def handle_starttag(self, tag, attrs):
                if tag == "div":
                    self.attrs = dict(attrs)

        parser = AttributeParser()
        parser.feed(rendered)
        self.assertEqual(parser.attrs, {"title": payload})
        self.assertNotIn("onmouseover", parser.attrs)

    def test_attribute_placeholders_require_double_quoted_attribute_context(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        for template in (
            "<div>{{attr:shared.home}}</div>",
            "<div title='{{attr:shared.home}}'></div>",
        ):
            with self.subTest(template=template):
                with self.assertRaisesRegex(
                    ValueError, "Attribute placeholder requires double-quoted attribute context"
                ):
                    self.builder.render_page("en", "about", template, content)

    def test_about_hours_label_is_translated_without_moving_the_technical_value(self):
        template = (PUBLIC / "core-page-templates" / "about.html").read_text(encoding="utf-8")
        content = json.loads((PUBLIC / "i18n" / "core" / "en.json").read_text(encoding="utf-8"))
        self.assertNotIn("24 Hours", template)
        self.assertIn("2 kWh", template)
        self.assertIn("24 ", template)
        self.assertEqual(content["about"]["copy"]["hours"], "Hours")

    def test_translation_html_is_not_treated_as_safe_markup(self):
        content = {"locale": "en", "shared": {"home": "Line one<br>Line two"}}
        rendered = self.builder.render_page(
            "en", "about", "<p>{{text:shared.home}}</p>", content
        )
        self.assertEqual(rendered, "<p>Line one&lt;br&gt;Line two</p>")

    def test_unresolved_or_unknown_placeholders_fail(self):
        content = {"locale": "en", "shared": {"home": "Home"}}
        for template in ("{{text:missing.key}}", "{{ unknown }}", "{{safe:unknown_block}}"):
            with self.subTest(template=template):
                with self.assertRaises((KeyError, ValueError)):
                    self.builder.render_page("en", "about", template, content)

    def test_batch_validation_happens_before_any_output_is_written(self):
        self.write_content("en")
        (self.fixture_content / "zh.json").write_text("{invalid", encoding="utf-8")
        destination = output_path(self.fixture_public, "en", "about")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("unchanged", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Invalid translation JSON: zh.json"):
            self.build(("en", "zh"))

        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")

    def test_parse_locales_defaults_and_rejects_unknown_or_duplicate_values(self):
        self.assertEqual(self.builder.parse_locales(None), SUPPORTED_LOCALES)
        self.assertEqual(self.builder.parse_locales(["en", "ja"]), ("en", "ja"))
        with self.assertRaisesRegex(ValueError, "Unsupported locale: xx"):
            self.builder.parse_locales(["xx"])
        with self.assertRaisesRegex(ValueError, "Duplicate locale: en"):
            self.builder.parse_locales(["en", "en"])


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


class TranslationDataTests(unittest.TestCase):
    LOCALES = ("zh", "es", "pt", "ja", "ko", "pl")
    DATASETS = {
        "homepage": Path("i18n") / "{locale}.json",
        "core": Path("i18n") / "core" / "{locale}.json",
        "products": Path("i18n") / "products" / "{locale}.json",
    }
    LEGAL_COMPANY_NAME = "Jinan Euchio Machinery Co., Ltd."
    CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
    EMAIL_FACT = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    PHONE_FACT = re.compile(r"(?<!\w)\+\d[\d ()-]{6,}\d")
    YEAR_FACT = re.compile(r"(?<!\d)(?:19|20)\d{2}(?!\d)")
    RUNTIME_PLACEHOLDER = re.compile(r"(?<!\{)\{([A-Za-z_][A-Za-z0-9_]*)\}(?!\})")
    TECHNICAL_FACT = re.compile(
        r"https?://[^\s\"'<>]+"
        r"|(?<![A-Za-z0-9_<³])/(?:[A-Za-z0-9._~!$&'()*+,;=:@%-]+/?)+"
        r"|(?<![A-Za-z0-9_])(?=[A-Za-z0-9_/-]*[A-Za-z])(?=[A-Za-z0-9_/-]*\d)"
        r"[A-Za-z][A-Za-z0-9_/-]*(?![A-Za-z0-9_])"
        r"|(?<![A-Za-z0-9])(?:NPN/PNP|N[₂2]\s*/\s*O[₂2]|N[₂2]|O[₂2])(?![A-Za-z0-9])"
        r"|(?<![A-Za-z0-9_.])[-+]?\d+(?:[.,]\d+)?(?:\s*[‐‑‒–—−-]\s*[-+]?\d+(?:[.,]\d+)?)?\s*"
        r"(?:Nm³/h|m³/h|L/min|m/min|MPa|kPa|bar|kg|mm|ms|kW|MW|V|ft|m|%)(?![A-Za-z0-9_])"
        r"|(?<![A-Za-z0-9_.])\d+(?:[.,]\d+)?(?![A-Za-z0-9_.])"
        r"|[×≤≥±]",
        re.IGNORECASE,
    )
    BARE_TECHNICAL_UNIT = re.compile(
        r"(?:Nm³/h|m³/h|L/min|m/min|MPa|kPa|bar|kg|mm|ms|kW|MW|V|ft|m|%)"
    )
    IMMUTABLE_FIELDS = frozenset(
        {"anchor", "href", "id", "key", "media_index", "model", "og_image", "src", "url"}
    )
    GLOBAL_UNTRANSLATED_TERMS = (
        "Jinan Euchio Machinery Co., Ltd.",
        "GasMixTech",
        "MSPV2-4000",
        "MSPV2_4000",
        "NPN/PNP",
        "N₂/O₂",
        "SAGEMRO",
        "WhatsApp",
        "LinkedIn",
        "DHgate",
        "Modbus",
        "Nm³/h",
        "m³/h",
        "L/min",
        "m/min",
        "MPa",
        "kPa",
        "PSA",
        "OEM",
        "MRO",
        "PLC",
        "ROI",
        "FAQ",
        "VS",
        "USD",
        "N₂",
        "O₂",
        "bar",
        "kg",
        "mm",
        "ms",
        "kW",
        "MW",
        "V",
        "ft",
        "m",
        "%",
    )
    LOCALE_UNTRANSLATED_TERMS = {
        "zh": (),
        "es": ("Blog", "Factor"),
        "pt": ("Blog",),
        "ja": (),
        "ko": (),
        "pl": ("Blog",),
    }
    ALLOWED_UNTRANSLATED_TERMS = {
        "zh": GLOBAL_UNTRANSLATED_TERMS,
        "es": GLOBAL_UNTRANSLATED_TERMS + LOCALE_UNTRANSLATED_TERMS["es"],
        "pt": GLOBAL_UNTRANSLATED_TERMS + LOCALE_UNTRANSLATED_TERMS["pt"],
        "ja": GLOBAL_UNTRANSLATED_TERMS,
        "ko": GLOBAL_UNTRANSLATED_TERMS,
        "pl": GLOBAL_UNTRANSLATED_TERMS + LOCALE_UNTRANSLATED_TERMS["pl"],
    }
    PREFERRED_TERMS = {
        "zh": {
            "assist gas": "辅助气体",
            "PSA nitrogen generation system": "PSA 制氮系统",
            "integrated gas mixing cabinet": "一体式混气柜",
            "proportional valve": "比例阀",
            "inlet pressure": "入口压力",
            "flow rate": "流量",
            "retrofit": "改造集成",
        },
        "es": {
            "assist gas": "gas de asistencia",
            "PSA nitrogen generation system": "sistema PSA de generación de nitrógeno",
            "integrated gas mixing cabinet": "armario integrado de mezcla de gases",
            "proportional valve": "válvula proporcional",
            "inlet pressure": "presión de entrada",
            "flow rate": "caudal",
            "retrofit": "modernización",
        },
        "pt": {
            "assist gas": "gás de assistência",
            "PSA nitrogen generation system": "sistema PSA de geração de nitrogênio",
            "integrated gas mixing cabinet": "gabinete integrado de mistura de gases",
            "proportional valve": "válvula proporcional",
            "inlet pressure": "pressão de entrada",
            "flow rate": "vazão",
            "retrofit": "modernização",
        },
        "ja": {
            "assist gas": "アシストガス",
            "PSA nitrogen generation system": "PSA窒素発生システム",
            "integrated gas mixing cabinet": "一体型ガス混合キャビネット",
            "proportional valve": "比例弁",
            "inlet pressure": "入口圧力",
            "flow rate": "流量",
            "retrofit": "レトロフィット",
        },
        "ko": {
            "assist gas": "보조 가스",
            "PSA nitrogen generation system": "PSA 질소 발생 시스템",
            "integrated gas mixing cabinet": "통합 가스 혼합 캐비닛",
            "proportional valve": "비례 밸브",
            "inlet pressure": "입구 압력",
            "flow rate": "유량",
            "retrofit": "개조 통합",
        },
        "pl": {
            "assist gas": "gaz pomocniczy",
            "PSA nitrogen generation system": "system wytwarzania azotu PSA",
            "integrated gas mixing cabinet": "zintegrowana szafa mieszania gazów",
            "proportional valve": "zawór proporcjonalny",
            "inlet pressure": "ciśnienie wlotowe",
            "flow rate": "natężenie przepływu",
            "retrofit": "modernizacja",
        },
    }
    TERM_PATHS = (
        ("assist gas", "homepage", "hero.badge"),
        (
            "PSA nitrogen generation system",
            "homepage",
            "principle.flow1Title",
        ),
        (
            "integrated gas mixing cabinet",
            "homepage",
            "principle.flow3Title",
        ),
        ("proportional valve", "core", "contact.copy.proportional_valve"),
        ("inlet pressure", "core", "contact.copy.oxygen_inlet_pressure"),
        ("flow rate", "core", "contact.copy.required_mixed_gas_flow"),
        ("retrofit", "homepage", "principle.flow4Desc"),
    )
    FORBIDDEN_CLAIM_PATTERNS = {
        "*": (
            r"\b(?:over|more than)\s+\d+[\d,]*\s+(?:installations?|systems? installed)\b",
            r"\b\d+[\d,]*\+\s+(?:installations?|installed systems?)\b",
            r"\b(?:ce|iso(?:\s*\d+)?)\s+certified\b",
            r"\b(?:delivery|ships?)\s+(?:within|in)\s+\d+\s+days?\b",
            r"\b(?:\d+[- ]year|lifetime) warranty\b",
            r"\b(?:exclusive technology|only supplier|best in the world|guaranteed results|100% compatible)\b",
            r"\b(?:integrated )?(?:gas mixing )?cabinet.{0,50}(?:mspv2[_-]?4000|(?:proportional )?valve).{0,40}(?:are installed in series|are installed together)\b",
        ),
        "zh": (
            r"(?:(?:已安装|装机)\s*\d+[\d,]*\+?\s*(?:套|台)|已有\s*\d+[\d,]*\+?\s*(?:套|台).{0,8}安装)",
            r"(?:CE|ISO\s*\d*)\s*认证(?:产品|设备)?",
            r"(?:\d+\s*天内?(?:交货|发货)|(?:明确)?交期(?:为|[:：])?\s*\d+\s*天)",
            r"(?:(?:\d+|[一二三四五六七八九十]+)\s*年|终身)(?:保修|质保)",
            r"(?:独家技术|唯一供应商|世界最佳|行业最佳|保证结果|结果保证|100%\s*兼容)",
            r"(?:混气柜|气体混合柜).{0,12}(?:比例阀|阀).{0,12}(?:串联|同时安装)",
        ),
        "es": (
            r"(?:más de )?\d+[\d.]* instalaciones",
            r"(?:certificad[oa] (?:ce|iso(?:\s*\d+)?)|certificación (?:ce|iso(?:\s*\d+)?))",
            r"(?:entrega en \d+ días|plazo de entrega\s*[:：]?\s*\d+ días)",
            r"garantía (?:de por vida|de \d+ años)",
            r"(?:tecnología exclusiva|único proveedor|proveedor único|mejor del mundo|resultados garantizados|100\s*% compatible)",
            r"(?:armario|gabinete).{0,30}válvula.{0,30}(?:se instalan en serie|se instalan juntos|instalados? juntos?)",
        ),
        "pt": (
            r"(?:mais de )?\d+[\d.]* instalações",
            r"(?:certificad[oa] (?:ce|iso(?:\s*\d+)?)|certificação (?:ce|iso(?:\s*\d+)?))",
            r"(?:entrega em \d+ dias|prazo de entrega(?: de)?\s*\d+ dias)",
            r"(?:garantia (?:vitalícia|de \d+ anos)|\d+ anos de garantia)",
            r"(?:tecnologia exclusiva|único fornecedor|fornecedor único|melhor do mundo|resultados garantidos|100\s*% compatível)",
            r"gabinete.{0,30}válvula.{0,30}(?:instalad[oa]s? em série|instalad[oa]s? juntos?)",
        ),
        "ja": (
            r"\d+[\d,]*\+?\s*(?:台|件)(?:以上)?(?:の)?導入実績",
            r"(?:CE|ISO\s*\d*)認証(?:取得済み|済み)?",
            r"(?:\d+日(?:以内|で)に?(?:納品|発送)|納期は?\s*\d+日)",
            r"(?:\d+年|永久)保証",
            r"(?:独占技術|唯一の(?:サプライヤー|供給者)|世界最高|結果(?:を)?保証|100%\s*互換)",
            r"キャビネット.{0,20}バルブ.{0,20}(?:直列|同時に設置)",
        ),
        "ko": (
            r"\d+[\d,]*\+?\s*(?:대|건)(?:\s*이상(?:의)?)?\s*설치 실적",
            r"(?:CE|ISO\s*\d*)\s*인증(?:\s*(?:완료|취득))?",
            r"(?:\d+일\s*이내\s*(?:납품|발송)|납기는?\s*\d+일)",
            r"(?:\d+년|평생)\s*보증",
            r"(?:독점 기술|유일한 공급업체|세계 최고|결과(?:를)?\s*보장|100%\s*호환)",
            r"캐비닛.{0,20}밸브.{0,20}(?:직렬로|함께)\s*설치",
        ),
        "pl": (
            r"(?:ponad )?\d+[\d.]* instalacji",
            r"(?:certyfikowan[yae] (?:ce|iso(?:\s*\d+)?)|certyfikat(?:em|u)? (?:ce|iso(?:\s*\d+)?))",
            r"(?:dostaw[ay] w ciągu \d+ dni|termin dostawy\s*[:：]?\s*\d+ dni)",
            r"(?:\d+[- ]letnia gwarancja|\d+ lata gwarancji|dożywotnia gwarancja)",
            r"(?:wyłączna technologia|jedyny dostawca|najlepszy na świecie|gwarantowane wyniki|100\s*% kompatybiln)",
            r"szafa.{0,30}zawór.{0,30}(?:instalowane szeregowo|instalowane razem)",
        ),
    }
    CLAIM_NEGATION_PATTERNS = {
        "*": r"\b(?:not|without)\b",
        "zh": r"(?:不|未|没有|并非|无需|无须)",
        "es": r"\b(?:no|sin)\b",
        "pt": r"\b(?:não|sem)\b",
        "ja": r"(?:ない|ありません|未取得|なく)",
        "ko": r"(?:않|없|아닙니다)",
        "pl": r"\b(?:nie|bez)\b",
    }
    CLAIM_SENTENCE_SPLIT = re.compile(r"[。！？!?；;\r\n]+|(?<!\d)\.(?!\d)")
    CLAIM_CLAUSE_SPLIT = {
        "zh": re.compile(r"(?<!\d)[,，](?!\d)|(?:但(?:是)?|不过)"),
        "es": re.compile(r"(?<!\d)[,，](?!\d)|\bpero\b", re.IGNORECASE),
        "pt": re.compile(r"(?<!\d)[,，](?!\d)|\b(?:mas|porém)\b", re.IGNORECASE),
        "ja": re.compile(r"(?<!\d)[,，](?!\d)|(?:だ?が|しかし)"),
        "ko": re.compile(r"(?<!\d)[,，](?!\d)|(?:하지만|그러나)"),
        "pl": re.compile(r"(?<!\d)[,，](?!\d)|\bale\b", re.IGNORECASE),
    }
    CLAIM_POSTPOSED_NEGATION = {
        "zh": re.compile(r"^\s*(?:尚?未|不|没有|并非|无需|无须)"),
        "ja": re.compile(
            r"^\s*(?:に?は|が|を)?\s*(?:(?:設置|取得|保証)?し)?(?:ない|ありません|未取得|なく)"
        ),
        "ko": re.compile(
            r"^\s*(?:이|가|은|는|을|를)?\s*(?:하지\s*)?(?:않|없|아닙니다)"
        ),
    }

    def _translation_path(self, dataset, locale):
        return PUBLIC / Path(str(self.DATASETS[dataset]).format(locale=locale))

    def _load_json(self, path, locale, dataset):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            self.fail(f"{locale}/{dataset}: invalid JSON in {path.name}: {error}")
        self.assertIsInstance(data, dict, f"{locale}/{dataset}: JSON root must be an object")
        return data

    def _walk(self, value, path=""):
        yield path, value
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                yield from self._walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                yield from self._walk(child, f"{path}.{index}")

    def _value_at(self, data, path, locale, dataset):
        value = data
        try:
            for part in path.split("."):
                value = value[int(part)] if isinstance(value, list) else value[part]
        except (IndexError, KeyError, TypeError, ValueError):
            self.fail(f"{locale}/{dataset}/{path}: missing or invalid translation path")
        return value

    def _leaf_paths(self, value, path=""):
        if isinstance(value, dict):
            if not value:
                return {path}
            paths = set()
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                paths.update(self._leaf_paths(child, child_path))
            return paths
        if isinstance(value, list):
            if not value:
                return {path}
            paths = set()
            for index, child in enumerate(value):
                paths.update(self._leaf_paths(child, f"{path}.{index}"))
            return paths
        return {path}

    def _is_immutable_path(self, path):
        field = path.rsplit(".", 1)[-1]
        return field in self.IMMUTABLE_FIELDS or field.endswith(
            ("_anchor", "_href", "_id", "_path", "_src", "_url")
        )

    def _is_explicit_technical_value_path(self, path):
        parts = path.split(".")
        field = parts[-1]
        if field == "value" and {"cases", "configurations", "specs"}.intersection(parts[:-1]):
            return True
        return field.endswith("_value") and field.startswith(("case_", "config_"))

    def _technical_facts(self, value):
        facts = []
        for match in self.TECHNICAL_FACT.finditer(value):
            fact = match.group(0)
            if not fact.startswith(("http://", "https://", "/")):
                fact = re.sub(r"\s+", "", fact)
                fact = fact.translate(str.maketrans("‐‑‒–—−", "------"))
                fact = re.sub(r"(?<=\d),(?=\d)", ".", fact)
            facts.append(fact)
        return Counter(facts)

    def _is_bare_technical_unit(self, value):
        return bool(self.BARE_TECHNICAL_UNIT.fullmatch(value.strip()))

    def _runtime_placeholders(self, value):
        return Counter(self.RUNTIME_PLACEHOLDER.findall(value))

    def _assert_recursive_schema(self, locale, dataset, english, localized, path=""):
        location = path or "<root>"
        self.assertIs(
            type(localized),
            type(english),
            f"{locale}/{dataset}/{location}: type differs from English",
        )
        if isinstance(english, dict):
            self.assertTrue(localized, f"{locale}/{dataset}/{location}: empty object is forbidden")
            missing = sorted(english.keys() - localized.keys())
            extra = sorted(localized.keys() - english.keys())
            self.assertEqual(
                (missing, extra),
                ([], []),
                f"{locale}/{dataset}/{location}: missing keys={missing}, extra keys={extra}",
            )
            for key, english_child in english.items():
                child_path = f"{path}.{key}" if path else key
                self._assert_recursive_schema(
                    locale, dataset, english_child, localized[key], child_path
                )
        elif isinstance(english, list):
            self.assertTrue(localized, f"{locale}/{dataset}/{location}: empty list is forbidden")
            self.assertEqual(
                len(localized),
                len(english),
                f"{locale}/{dataset}/{location}: list length/order contract differs from English",
            )
            for index, english_child in enumerate(english):
                self._assert_recursive_schema(
                    locale, dataset, english_child, localized[index], f"{path}.{index}"
                )

    def _assert_safe_strings(self, locale, dataset, english, localized):
        for path, value in self._walk(localized):
            if isinstance(value, (dict, list)):
                self.assertTrue(value, f"{locale}/{dataset}/{path}: empty container is forbidden")
            elif isinstance(value, str):
                self.assertTrue(value.strip(), f"{locale}/{dataset}/{path}: empty string is forbidden")
                self.assertIsNone(
                    self.CONTROL_CHARACTERS.search(value),
                    f"{locale}/{dataset}/{path}: control character is forbidden",
                )
                self.assertNotIn("{{", value, f"{locale}/{dataset}/{path}: unresolved '{{{{' marker")
                self.assertNotIn("}}", value, f"{locale}/{dataset}/{path}: unresolved '}}}}' marker")

        for path, english_value in self._walk(english):
            if not isinstance(english_value, str):
                continue
            localized_value = self._value_at(localized, path, locale, dataset)
            self.assertIsInstance(
                localized_value,
                str,
                f"{locale}/{dataset}/{path}: type differs from English string",
            )
            self.assertEqual(
                self._runtime_placeholders(localized_value),
                self._runtime_placeholders(english_value),
                f"{locale}/{dataset}/{path}: runtime placeholder multiset differs from English",
            )

    def _assert_critical_facts(self, locale, dataset, english, localized):
        english_leaves = self._leaf_paths(english)
        localized_leaves = self._leaf_paths(localized)
        self.assertEqual(
            localized_leaves,
            english_leaves,
            f"{locale}/{dataset}: leaf paths differ from English",
        )

        for path, english_value in self._walk(english):
            if isinstance(english_value, (dict, list)):
                continue
            localized_value = self._value_at(localized, path, locale, dataset)
            if path == "locale":
                self.assertEqual(
                    localized_value,
                    locale,
                    f"{locale}/{dataset}/locale: locale identity must match filename",
                )
                continue
            if self._is_immutable_path(path) or self._is_explicit_technical_value_path(path):
                self.assertEqual(
                    localized_value,
                    english_value,
                    f"{locale}/{dataset}/{path}: immutable fact differs from English",
                )
            if not isinstance(english_value, str):
                self.assertEqual(
                    localized_value,
                    english_value,
                    f"{locale}/{dataset}/{path}: machine value differs from English",
                )
                continue
            self.assertIsInstance(
                localized_value,
                str,
                f"{locale}/{dataset}/{path}: type differs from English string",
            )
            if self._is_bare_technical_unit(english_value):
                self.assertEqual(
                    localized_value,
                    english_value,
                    f"{locale}/{dataset}/{path}: bare technical unit differs from English",
                )
            self.assertEqual(
                self._technical_facts(localized_value),
                self._technical_facts(english_value),
                f"{locale}/{dataset}/{path}: technical fact multiset differs from English",
            )
            for pattern, fact_name in (
                (self.EMAIL_FACT, "email"),
                (self.PHONE_FACT, "phone"),
                (self.YEAR_FACT, "year"),
            ):
                self.assertEqual(
                    tuple(pattern.findall(localized_value)),
                    tuple(pattern.findall(english_value)),
                    f"{locale}/{dataset}/{path}: {fact_name} fact differs from English",
                )
            if self.LEGAL_COMPANY_NAME in english_value:
                self.assertIn(
                    self.LEGAL_COMPANY_NAME,
                    localized_value,
                    f"{locale}/{dataset}/{path}: company legal name must remain exact",
                )

        if dataset == "products":
            try:
                PRODUCT_BUILDER.validate_comparison_row_keys(localized, locale)
            except (KeyError, TypeError, ValueError) as error:
                self.fail(f"{locale}/{dataset}: comparison stable-key validation failed: {error}")
            english_keys = tuple(
                row["key"] for row in english["pages"]["comparison"]["comparison_rows"]
            )
            localized_keys = tuple(
                row["key"] for row in localized["pages"]["comparison"]["comparison_rows"]
            )
            self.assertEqual(
                localized_keys,
                english_keys,
                f"{locale}/{dataset}: comparison stable-key order differs from English",
            )

    def _is_question_path(self, path):
        parts = path.split(".")
        field = parts[-1].lower()
        return field == "question" or (
            bool(re.fullmatch(r"q\d+", field)) and "faq" in (part.lower() for part in parts[:-1])
        )

    def _claim_clauses(self, locale, value):
        for sentence in filter(None, self.CLAIM_SENTENCE_SPLIT.split(value)):
            yield from filter(None, self.CLAIM_CLAUSE_SPLIT[locale].split(sentence))

    def _claim_is_negated(self, locale, clause, match):
        negation_patterns = (
            self.CLAIM_NEGATION_PATTERNS["*"],
            self.CLAIM_NEGATION_PATTERNS[locale],
        )
        if any(re.search(pattern, match.group(0), re.IGNORECASE) for pattern in negation_patterns):
            return True
        before = clause[: match.start()]
        if any(re.search(pattern, before, re.IGNORECASE) for pattern in negation_patterns):
            return True
        postposed = self.CLAIM_POSTPOSED_NEGATION.get(locale)
        return bool(postposed and postposed.search(clause[match.end() :]))

    def _assert_brand_and_claim_boundaries(self, locale, dataset, english, localized):
        for path, value in self._walk(localized):
            if not isinstance(value, str):
                continue
            self.assertIsNone(
                re.search(
                    r"(?<![A-Za-z0-9])lishi(?:\s+laser)?(?![A-Za-z0-9])",
                    value,
                    re.IGNORECASE,
                ),
                f"{locale}/{dataset}/{path}: legacy LISHI branding is forbidden",
            )
            if self._is_question_path(path):
                continue
            for clause in self._claim_clauses(locale, value):
                for pattern in (
                    self.FORBIDDEN_CLAIM_PATTERNS["*"]
                    + self.FORBIDDEN_CLAIM_PATTERNS[locale]
                ):
                    for match in re.finditer(pattern, clause, re.IGNORECASE):
                        if not self._claim_is_negated(locale, clause, match):
                            context_start = max(0, match.start() - 48)
                            context_end = min(len(clause), match.end() + 48)
                            context = clause[context_start:context_end].strip()
                            self.fail(
                                f"{locale}/{dataset}/{path}: unverified claim "
                                f"matched text={match.group(0)!r}, context={context!r}"
                            )

    def _english_value_is_allowlisted(self, locale, value):
        remainder = re.sub(r"<[^>]*>", " ", value)
        for term in sorted(self.ALLOWED_UNTRANSLATED_TERMS[locale], key=len, reverse=True):
            remainder = re.sub(re.escape(term), " ", remainder, flags=re.IGNORECASE)
        remainder = re.sub(r"\b(?=[A-Za-z0-9_-]*\d)[A-Za-z][A-Za-z0-9_-]*\b", " ", remainder)
        remainder = re.sub(r"[\d\s\W_]+", "", remainder, flags=re.UNICODE)
        return not re.search(r"[A-Za-z]", remainder)

    def _is_placeholder_only(self, value):
        remainder = self.RUNTIME_PLACEHOLDER.sub(" ", re.sub(r"<[^>]*>", " ", value))
        return not re.sub(r"[\s\W_]+", "", remainder, flags=re.UNICODE)

    def _assert_no_english_ui_residue(self, locale, dataset, english, localized):
        for path, english_value in self._walk(english):
            if not isinstance(english_value, str):
                continue
            if path == "locale" or self._is_immutable_path(path):
                continue
            if self._is_explicit_technical_value_path(path):
                continue
            localized_value = self._value_at(localized, path, locale, dataset)
            self.assertIsInstance(
                localized_value,
                str,
                f"{locale}/{dataset}/{path}: type differs from English string",
            )
            if localized_value != english_value:
                continue
            if self._is_placeholder_only(english_value):
                continue
            self.assertTrue(
                self._english_value_is_allowlisted(locale, english_value),
                f"{locale}/{dataset}/{path}: translatable text is unchanged from English: {english_value!r}",
            )

    def _assert_preferred_terms(self, locale, dataset, english, localized):
        for concept, term_dataset, path in self.TERM_PATHS:
            if term_dataset != dataset:
                continue
            english_value = self._value_at(english, path, "en", dataset)
            self.assertIsInstance(
                english_value,
                str,
                f"English terminology anchor is not text: {dataset}/{path}",
            )
            localized_value = self._value_at(localized, path, locale, dataset)
            self.assertIsInstance(
                localized_value,
                str,
                f"{locale}/{dataset}/{path}: type differs from English string",
            )
            expected = self.PREFERRED_TERMS[locale][concept]
            self.assertIn(
                expected.casefold(),
                localized_value.casefold(),
                f"{locale}/{dataset}/{path}: expected preferred term {expected!r}",
            )

    def assert_locale_dataset(self, locale):
        self.assertIn(locale, self.LOCALES)
        for dataset in self.DATASETS:
            english_path = self._translation_path(dataset, "en")
            localized_path = self._translation_path(dataset, locale)
            self.assertTrue(english_path.is_file(), f"English baseline missing: {english_path}")

            with self.subTest(locale=locale, dataset=dataset, check="file"):
                self.assertTrue(
                    localized_path.is_file(),
                    f"{locale}/{dataset}: missing translation file {localized_path}",
                )
            if not localized_path.is_file():
                continue

            english = self._load_json(english_path, "en", dataset)
            localized = self._load_json(localized_path, locale, dataset)
            checks = (
                ("recursive schema", self._assert_recursive_schema),
                ("safe strings", self._assert_safe_strings),
                ("critical facts", self._assert_critical_facts),
                ("brand and claims", self._assert_brand_and_claim_boundaries),
                ("English UI residue", self._assert_no_english_ui_residue),
                ("preferred terminology", self._assert_preferred_terms),
            )
            for check_name, check in checks:
                with self.subTest(locale=locale, dataset=dataset, check=check_name):
                    check(locale, dataset, english, localized)

    def test_00_locale_order_is_exact(self):
        self.assertEqual(self.LOCALES, ("zh", "es", "pt", "ja", "ko", "pl"))
        self.assertEqual(tuple(self.PREFERRED_TERMS), self.LOCALES)

    def test_01_zh_translation_data_contract(self):
        self.assert_locale_dataset("zh")

    def test_02_es_translation_data_contract(self):
        self.assert_locale_dataset("es")

    def test_03_pt_translation_data_contract(self):
        self.assert_locale_dataset("pt")

    def test_04_ja_translation_data_contract(self):
        self.assert_locale_dataset("ja")

    def test_05_ko_translation_data_contract(self):
        self.assert_locale_dataset("ko")

    def test_06_pl_translation_data_contract(self):
        self.assert_locale_dataset("pl")


class TranslationGuardRuleTests(unittest.TestCase):
    CLAIM_FIXTURES = {
        "zh": {
            "forbidden": (
                "已有 500 套安装案例",
                "CE 认证设备",
                "7 天内交货",
                "5 年保修",
                "独家技术，保证结果",
                "混气柜与比例阀串联安装",
                "混气柜与比例阀同时安装",
            ),
            "disclaimer": "混气柜与比例阀不是串联组件，不应同时安装。",
        },
        "es": {
            "forbidden": (
                "Más de 500 instalaciones",
                "Equipo certificado CE",
                "Entrega en 7 días",
                "Garantía de 5 años",
                "La mejor del mundo con resultados garantizados",
                "El armario y la válvula se instalan en serie",
                "El armario y la válvula se instalan juntos",
            ),
            "disclaimer": "No son componentes en serie y no deben instalarse juntos.",
        },
        "pt": {
            "forbidden": (
                "Mais de 500 instalações",
                "Equipamento certificado CE",
                "Entrega em 7 dias",
                "Garantia de 5 anos",
                "A melhor do mundo com resultados garantidos",
                "O gabinete e a válvula são instalados em série",
                "O gabinete e a válvula são instalados juntos",
            ),
            "disclaimer": "Não são componentes em série e não devem ser instalados juntos.",
        },
        "ja": {
            "forbidden": (
                "500台以上の導入実績",
                "CE認証済み",
                "7日以内に納品",
                "5年保証",
                "世界最高、結果保証",
                "キャビネットとバルブを直列に設置",
                "キャビネットとバルブを同時に設置",
            ),
            "disclaimer": "直列部品ではなく、同時に設置しません。",
        },
        "ko": {
            "forbidden": (
                "500대 이상의 설치 실적",
                "CE 인증 완료",
                "7일 이내 납품",
                "5년 보증",
                "세계 최고, 결과 보장",
                "캐비닛과 밸브를 직렬로 설치",
                "캐비닛과 밸브를 함께 설치",
            ),
            "disclaimer": "직렬 구성품이 아니며 함께 설치하지 않습니다.",
        },
        "pl": {
            "forbidden": (
                "Ponad 500 instalacji",
                "Urządzenie certyfikowane CE",
                "Dostawa w ciągu 7 dni",
                "5-letnia gwarancja",
                "Najlepszy na świecie, gwarantowane wyniki",
                "Szafa i zawór są instalowane szeregowo",
                "Szafa i zawór są instalowane razem",
            ),
            "disclaimer": "To nie są elementy szeregowe i nie należy instalować ich razem.",
        },
    }
    CLAIM_REVIEW_FIXTURES = {
        "zh": {
            "forbidden": (
                "本设备已取得CE认证",
                "提供3年质保",
                "提供五年质保",
                "明确交期为7天",
                "行业唯一供应商，保证结果",
                "已有500套安装案例",
                "一体式混气柜与比例阀同时安装",
            ),
            "allowed": (
                "本设备未取得CE认证",
                "本设备无需取得CE认证",
                "混气柜与比例阀不串联安装",
            ),
        },
        "es": {
            "forbidden": (
                "Equipo con certificación CE",
                "Garantía de 3 años",
                "Plazo de entrega: 7 días",
                "Proveedor único con resultados garantizados",
                "500 instalaciones completadas",
                "El armario y la válvula se instalan juntos",
            ),
            "allowed": (
                "Equipo sin certificación CE",
                "El armario y la válvula no se instalan en serie",
            ),
        },
        "pt": {
            "forbidden": (
                "Equipamento com certificação CE",
                "3 anos de garantia",
                "Prazo de entrega de 7 dias",
                "Fornecedor único com resultados garantidos",
                "500 instalações concluídas",
                "O gabinete e a válvula são instalados juntos",
            ),
            "allowed": (
                "Equipamento sem certificação CE",
                "O gabinete e a válvula não são instalados em série",
            ),
        },
        "ja": {
            "forbidden": (
                "CE認証取得済み",
                "3年保証",
                "納期は7日",
                "唯一の供給者で結果を保証",
                "500台の導入実績",
                "キャビネットとバルブを同時に設置",
            ),
            "allowed": (
                "CE認証は未取得です",
                "キャビネットとバルブを直列には設置しない",
            ),
        },
        "ko": {
            "forbidden": (
                "CE 인증 취득",
                "3년 보증",
                "납기는 7일",
                "유일한 공급업체이며 결과를 보장",
                "500대 설치 실적",
                "캐비닛과 밸브를 함께 설치",
            ),
            "allowed": (
                "CE 인증이 없습니다",
                "캐비닛과 밸브는 직렬 구성품이 아닙니다",
            ),
        },
        "pl": {
            "forbidden": (
                "Urządzenie ma certyfikat CE",
                "Urządzenie z certyfikatem CE",
                "3 lata gwarancji",
                "Termin dostawy: 7 dni",
                "Jedyny dostawca z gwarantowanymi wynikami",
                "500 instalacji zakończonych",
                "Szafa i zawór są instalowane razem",
            ),
            "allowed": (
                "Urządzenie bez certyfikatu CE",
                "Szafa i zawór nie są instalowane szeregowo",
            ),
        },
    }

    def setUp(self):
        self.guard = TranslationDataTests("test_00_locale_order_is_exact")

    def assert_guard_failure(self, callback):
        with self.assertRaises(AssertionError):
            callback()

    def test_fact_guard_rejects_changed_number_and_unit(self):
        self.assert_guard_failure(
            lambda: self.guard._assert_critical_facts(
                "es", "fixture", {"measurement": "Power 20kW"}, {"measurement": "Potencia 999MW"}
            )
        )

    def test_fact_guard_allows_translated_pressure_and_flow_to_change_order(self):
        english = {"measurement": "Pressure 20 bar; flow 200 m³/h"}
        localized = {"measurement": "Caudal 200 m³/h; presión 20 bar"}
        self.guard._assert_critical_facts("es", "fixture", english, localized)

    def test_fact_guard_recognizes_supported_units_with_or_without_spaces(self):
        english = {
            "measurement": (
                "20kW; 1.5 MPa; 100kPa; 25 bar; 90kg; 1100 mm; 10.17ft; "
                "200ms; 24 V; 95%; 5000 L/min; 200m³/h; 12 m/min"
            )
        }
        localized = {
            "measurement": (
                "200 m³/h; 5000L/min; 95 %; 24V; 200 ms; 10.17 ft; "
                "1100mm; 90 kg; 25bar; 100 kPa; 1.5MPa; 20 kW; 12m/min"
            )
        }
        self.guard._assert_critical_facts("es", "fixture", english, localized)

    def test_fact_guard_allows_cjk_adjacent_measurements(self):
        english = {"measurement": "Thickness 20 mm; output 20 kW; flow 200 m³/h"}
        localized_values = {
            "zh": "厚度20mm；出力20kW；流量200 m³/h",
            "ja": "厚さ20mm、出力20kW、流量200 m³/h",
            "ko": "두께20mm, 출력20kW, 유량200 m³/h",
        }
        for locale, value in localized_values.items():
            with self.subTest(locale=locale):
                self.guard._assert_critical_facts(
                    locale, "fixture", english, {"measurement": value}
                )

    def test_fact_guard_normalizes_decimal_separator_and_range_dash(self):
        self.guard._assert_critical_facts(
            "es",
            "fixture",
            {"measurement": "Pressure 1.5–1.6 MPa"},
            {"measurement": "Presión 1,5-1,6 MPa"},
        )

    def test_fact_guard_preserves_unit_and_model_case(self):
        for english_value, localized_value in (
            ("Pressure 1.5 MPa", "Presión 1,5 mPa"),
            ("Power 20 kW", "Potencia 20 MW"),
            ("Power 20 kW", "Potencia 20 KW"),
            ("Use model MSPV2_4000", "Usar modelo MSPv2_4000"),
        ):
            with self.subTest(localized=localized_value):
                self.assert_guard_failure(
                    lambda english_value=english_value, localized_value=localized_value: self.guard._assert_critical_facts(
                        "es",
                        "fixture",
                        {"measurement": english_value},
                        {"measurement": localized_value},
                    )
                )

    def test_fact_guard_does_not_extract_hour_suffix_as_path(self):
        facts = self.guard._technical_facts("Flow unit m³/h; measured 200 m³/h")
        self.assertNotIn("/h", facts)
        self.assertEqual(facts["200m³/h"], 1)

    def test_fact_guard_preserves_bare_unit_values(self):
        for english, localized in (
            ({"speedUnit": "m/min"}, {"speedUnit": "km/h"}),
            ({"flow_unit": "m³/h"}, {"flow_unit": "L/min"}),
            ({"unit": "MPa"}, {"unit": "mPa"}),
        ):
            with self.subTest(english=english, localized=localized):
                self.assert_guard_failure(
                    lambda english=english, localized=localized: self.guard._assert_critical_facts(
                        "es", "fixture", english, localized
                    )
                )
        self.guard._assert_critical_facts(
            "es", "fixture", {"flow_unit": "m³/h"}, {"flow_unit": "m³/h"}
        )

    def test_fact_guard_is_independent_of_product_builder_validation(self):
        english = {"measurement": "Pressure 20 bar"}
        localized = {"measurement": "Presión 20 bar"}
        with mock.patch.object(
            PRODUCT_BUILDER,
            "validate_technical_content",
            side_effect=AssertionError("production validator must not decide this contract"),
        ), mock.patch.object(
            PRODUCT_BUILDER,
            "technical_tokens",
            side_effect=AssertionError("production tokenizer must not decide this contract"),
        ):
            self.guard._assert_critical_facts("es", "fixture", english, localized)

    def test_fact_guard_keeps_identity_and_explicit_technical_values_exact(self):
        for field in ("model", "id", "url", "key"):
            with self.subTest(field=field):
                self.assert_guard_failure(
                    lambda field=field: self.guard._assert_critical_facts(
                        "es", "fixture", {field: "stable-value"}, {field: "changed-value"}
                    )
                )
        self.assert_guard_failure(
            lambda: self.guard._assert_critical_facts(
                "es",
                "fixture",
                {"specs": [{"value": "Analog + NPN/PNP"}]},
                {"specs": [{"value": "Analógico + NPN/PNP"}]},
            )
        )

    def test_runtime_placeholder_guard_rejects_missing_and_extra_placeholders(self):
        english = {"message": "Step {current} of {total}"}
        for localized in (
            "Paso {current}",
            "Paso {current} de {total} ({extra})",
            "Paso {current} de {total} / {total}",
        ):
            with self.subTest(localized=localized):
                with self.assertRaisesRegex(
                    AssertionError,
                    r"es/fixture/message: runtime placeholder multiset differs",
                ):
                    self.guard._assert_safe_strings(
                        "es", "fixture", english, {"message": localized}
                    )

    def test_runtime_placeholder_guard_allows_reordered_placeholders(self):
        english = {"message": "Step {current} of {total}"}
        localized = {"message": "De {total}: paso {current}"}
        self.guard._assert_safe_strings("es", "fixture", english, localized)

    def test_lishi_guard_detects_cjk_adjacent_brand(self):
        self.assert_guard_failure(
            lambda: self.guard._assert_brand_and_claim_boundaries(
                "zh", "fixture", {}, {"text": "禁止LISHI品牌残留"}
            )
        )

    def test_claim_guard_rejects_english_serial_installation_but_not_negation(self):
        self.assert_guard_failure(
            lambda: self.guard._assert_brand_and_claim_boundaries(
                "es",
                "fixture",
                {},
                {"text": "The integrated cabinet and proportional valve are installed in series."},
            )
        )
        self.guard._assert_brand_and_claim_boundaries(
            "es",
            "fixture",
            {},
            {"text": "The integrated cabinet and proportional valve are not installed together."},
        )

    def test_six_locale_claim_guard_positive_and_disclaimer_fixtures(self):
        for locale, fixtures in self.CLAIM_FIXTURES.items():
            for text in fixtures["forbidden"]:
                with self.subTest(locale=locale, kind="forbidden", text=text):
                    self.assert_guard_failure(
                        lambda locale=locale, text=text: self.guard._assert_brand_and_claim_boundaries(
                            locale, "fixture", {}, {"text": text}
                        )
                    )
            with self.subTest(locale=locale, kind="disclaimer"):
                self.guard._assert_brand_and_claim_boundaries(
                    locale, "fixture", {}, {"text": fixtures["disclaimer"]}
                )

    def test_claim_guard_review_examples_respect_local_negation_context(self):
        for locale, fixtures in self.CLAIM_REVIEW_FIXTURES.items():
            for text in fixtures["forbidden"]:
                with self.subTest(locale=locale, kind="forbidden", text=text):
                    self.assert_guard_failure(
                        lambda locale=locale, text=text: self.guard._assert_brand_and_claim_boundaries(
                            locale, "fixture", {}, {"text": text}
                        )
                    )
            for text in fixtures["allowed"]:
                with self.subTest(locale=locale, kind="allowed", text=text):
                    self.guard._assert_brand_and_claim_boundaries(
                        locale, "fixture", {}, {"text": text}
                    )

    def test_claim_negation_does_not_cross_sentence_boundaries(self):
        mixed_sentences = {
            "zh": "无须维护。设备已取得CE认证。",
            "es": "No requiere mantenimiento. Equipo con certificación CE.",
            "pt": "Não requer manutenção. Equipamento com certificação CE.",
            "ja": "メンテナンスは必要ありません。CE認証取得済み。",
            "ko": "유지보수가 필요 없습니다. CE 인증 취득.",
            "pl": "Konserwacja nie jest wymagana. Urządzenie ma certyfikat CE.",
        }
        for locale, text in mixed_sentences.items():
            with self.subTest(locale=locale):
                self.assert_guard_failure(
                    lambda locale=locale, text=text: self.guard._assert_brand_and_claim_boundaries(
                        locale, "fixture", {}, {"text": text}
                    )
                )

    def test_claim_negation_does_not_cross_contrast_clause_boundaries(self):
        mixed_clauses = {
            "zh": "设备已取得CE认证，但不需要维护。",
            "es": "Equipo con certificación CE, pero no requiere mantenimiento.",
            "pt": "Equipamento com certificação CE, mas não requer manutenção.",
            "ja": "CE認証取得済みだが、メンテナンスは必要ありません。",
            "ko": "CE 인증 취득, 하지만 유지보수가 필요 없습니다.",
            "pl": "Urządzenie ma certyfikat CE, ale nie wymaga konserwacji.",
        }
        for locale, text in mixed_clauses.items():
            with self.subTest(locale=locale):
                self.assert_guard_failure(
                    lambda locale=locale, text=text: self.guard._assert_brand_and_claim_boundaries(
                        locale, "fixture", {}, {"statement": text}
                    )
                )

    def test_claim_guard_allows_same_clause_negated_guarantees(self):
        negated_guarantees = {
            "zh": "我们不保证结果。",
            "es": "No son resultados garantizados.",
            "pt": "Não são resultados garantidos.",
            "ja": "結果を保証しない。",
            "ko": "결과를 보장하지 않습니다.",
            "pl": "To nie są gwarantowane wyniki.",
        }
        for locale, text in negated_guarantees.items():
            with self.subTest(locale=locale):
                self.guard._assert_brand_and_claim_boundaries(
                    locale, "fixture", {}, {"statement": text}
                )

    def test_claim_guard_skips_questions_but_not_answers(self):
        questions = {
            "zh": "混气柜与比例阀是否同时安装？",
            "es": "¿El armario y la válvula se instalan juntos?",
            "pt": "O gabinete e a válvula são instalados juntos?",
            "ja": "キャビネットとバルブを同時に設置しますか？",
            "ko": "캐비닛과 밸브를 함께 설치합니까?",
            "pl": "Czy szafa i zawór są instalowane razem?",
        }
        for locale, text in questions.items():
            with self.subTest(locale=locale, field="question"):
                self.guard._assert_brand_and_claim_boundaries(
                    locale,
                    "fixture",
                    {},
                    {"pages": {"sample": {"faq": [{"question": text}]}}},
                )
            with self.subTest(locale=locale, field="answer"):
                self.assert_guard_failure(
                    lambda locale=locale, text=text: self.guard._assert_brand_and_claim_boundaries(
                        locale,
                        "fixture",
                        {},
                        {"pages": {"sample": {"faq": [{"answer": text.rstrip("?？")}]}}},
                    )
                )
        self.guard._assert_brand_and_claim_boundaries(
            "zh", "fixture", {}, {"faq": {"q1": questions["zh"]}}
        )

    def test_claim_failure_names_matched_text_and_context(self):
        text = "FAR_PREFIX_MARKER " + ("details " * 20) + "Equipo con certificación CE."
        with self.assertRaises(AssertionError) as caught:
            self.guard._assert_brand_and_claim_boundaries(
                "es", "fixture", {}, {"statement": text}
            )
        message = str(caught.exception)
        self.assertIn("certificación CE", message)
        self.assertIn("context", message)
        self.assertNotIn("FAR_PREFIX_MARKER", message)

    def test_english_allowlist_has_global_and_locale_specific_layers(self):
        for locale in self.guard.LOCALES:
            for value in (
                "WhatsApp",
                "LinkedIn",
                "Modbus",
                "GasMixTech",
                "PSA",
                "DHgate",
                "20 kW",
                "12 m/min",
                "VS",
            ):
                with self.subTest(locale=locale, value=value):
                    self.assertTrue(self.guard._english_value_is_allowlisted(locale, value))
        for locale in ("es", "pt", "pl"):
            with self.subTest(locale=locale, value="Blog"):
                self.assertTrue(self.guard._english_value_is_allowlisted(locale, "Blog"))
        self.assertTrue(self.guard._english_value_is_allowlisted("es", "Factor"))
        for value in ("Request a Solution", "Send assessment request"):
            with self.subTest(value=value):
                self.assertFalse(self.guard._english_value_is_allowlisted("es", value))

    def test_english_ui_guard_rejects_sentence_but_allows_locale_specific_term(self):
        self.assert_guard_failure(
            lambda: self.guard._assert_no_english_ui_residue(
                "es",
                "homepage",
                {"hero": {"title": "Request a Solution"}},
                {"hero": {"title": "Request a Solution"}},
            )
        )
        self.guard._assert_no_english_ui_residue(
            "es",
            "core",
            {"shared": {"copy": {"blog": "Blog"}}},
            {"shared": {"copy": {"blog": "Blog"}}},
        )

    def test_english_residue_guard_checks_every_translatable_string_leaf(self):
        cases = (
            (
                "homepage",
                {
                    "principle": {
                        "flow1Desc": (
                            "Generate nitrogen on site when the required flow, purity, pressure "
                            "and operating profile justify a dedicated source."
                        )
                    }
                },
            ),
            (
                "core",
                {"about": {"copy": {"ready_to_upgrade_your_laser_cutting": "Ready to Upgrade Your Laser Cutting?"}}},
            ),
        )
        for dataset, english in cases:
            with self.subTest(dataset=dataset):
                self.assert_guard_failure(
                    lambda dataset=dataset, english=english: self.guard._assert_no_english_ui_residue(
                        "es", dataset, english, json.loads(json.dumps(english))
                    )
                )

        for english in (
            {"progress": "{current} / {total}"},
            {"model": "MSPV2-4000"},
            {"speedUnit": "m/min"},
        ):
            with self.subTest(allowlisted=english):
                self.guard._assert_no_english_ui_residue(
                    "es", "fixture", english, json.loads(json.dumps(english))
                )

    def test_wrong_leaf_types_fail_with_path_in_all_followup_checks(self):
        english = {"hero": {"title": "Request a Solution"}}
        localized = {"hero": {"title": 7}}
        for check in (
            self.guard._assert_safe_strings,
            self.guard._assert_critical_facts,
            self.guard._assert_no_english_ui_residue,
        ):
            with self.subTest(check=check.__name__):
                try:
                    check("es", "fixture", english, localized)
                except AssertionError as error:
                    self.assertIn("es/fixture/hero.title", str(error))
                except Exception as error:
                    self.fail(
                        f"{check.__name__} raised {type(error).__name__} instead of AssertionError: {error}"
                    )
                else:
                    self.fail(f"{check.__name__} accepted a wrong leaf type")

        try:
            self.guard._assert_preferred_terms(
                "es",
                "homepage",
                {"hero": {"badge": "assist gas"}},
                {"hero": {"badge": 7}},
            )
        except AssertionError as error:
            self.assertIn("es/homepage/hero.badge", str(error))
        except Exception as error:
            self.fail(
                f"preferred terms raised {type(error).__name__} instead of AssertionError: {error}"
            )
        else:
            self.fail("preferred terms accepted a wrong leaf type")

    def test_missing_path_is_an_assertion_failure_not_key_error(self):
        english = {"hero": {"title": "Request a Solution"}}
        localized = {"hero": {}}
        try:
            self.guard._assert_no_english_ui_residue("es", "fixture", english, localized)
        except AssertionError as error:
            self.assertIn("es/fixture/hero.title", str(error))
        except Exception as error:
            self.fail(f"missing path raised {type(error).__name__} instead of AssertionError: {error}")
        else:
            self.fail("missing path did not fail")
