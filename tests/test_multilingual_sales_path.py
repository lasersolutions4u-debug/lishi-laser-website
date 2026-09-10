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
