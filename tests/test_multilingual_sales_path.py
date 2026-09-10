import difflib
import json
import shutil
import subprocess
import tempfile
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
