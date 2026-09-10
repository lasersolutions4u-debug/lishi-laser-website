import json
import subprocess
import unittest
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

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


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


class HomepageGenerationTests(unittest.TestCase):
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
        result = subprocess.run(
            [
                "node",
                "-e",
                "const { replacePlaceholders } = require('./public/build-i18n.js'); "
                "replacePlaceholders('{{missing.required.key}}', {});",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing translation key: missing.required.key", result.stderr)

    def test_javascript_supported_locales_match_python_contract(self):
        result = subprocess.run(
            [
                "node",
                "-e",
                "const { SUPPORTED_LOCALES } = require('./public/build-i18n.js'); "
                "process.stdout.write(JSON.stringify(SUPPORTED_LOCALES));",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(tuple(json.loads(result.stdout)), SUPPORTED_LOCALES)

    def test_repeatable_locale_option_builds_only_selected_homepages(self):
        result = subprocess.run(
            ["node", "public/build-i18n.js", "--locale", "en", "--locale", "zh"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("en/index.html (root)", result.stdout)
        self.assertIn("zh/index.html", result.stdout)
        self.assertNotIn("es/index.html", result.stdout)

    def test_unknown_locale_fails_with_clear_error(self):
        result = subprocess.run(
            ["node", "public/build-i18n.js", "--locale", "xx"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported locale: xx", result.stderr)

    def test_missing_locale_translation_file_fails_closed(self):
        result = subprocess.run(
            ["node", "public/build-i18n.js", "--locale", "pl"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing translation file: pl.json", result.stderr)
