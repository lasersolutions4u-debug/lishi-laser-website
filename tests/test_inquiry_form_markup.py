import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LOCALES = ("en", "zh", "es", "ko", "ja", "pt", "pl")
PRODUCT_IDS = {
    "psa-nitrogen-system",
    "integrated-mixing-cabinet",
    "mspv2-4000",
    "need-recommendation",
}


def contact_path(locale):
    return PUBLIC / "contact.html" if locale == "en" else PUBLIC / locale / "contact.html"


class InquiryParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.fieldsets = []
        self.legends = 0
        self.names = set()
        self.product_values = set()
        self.in_product = False
        self.scripts = []
        self.ids = set()
        self.live_regions = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "form" and attrs.get("id") == "contactForm":
            self.forms.append(attrs)
        if tag == "fieldset" and attrs.get("data-step"):
            self.fieldsets.append(attrs)
        if tag == "legend":
            self.legends += 1
        if tag in {"input", "select", "textarea"} and attrs.get("name"):
            self.names.add(attrs["name"])
        if tag == "select" and attrs.get("name") == "product":
            self.in_product = True
        if tag == "option" and self.in_product and attrs.get("value"):
            self.product_values.add(attrs["value"])
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if attrs.get("aria-live") in {"polite", "assertive"}:
            self.live_regions += 1

    def handle_endtag(self, tag):
        if tag == "select" and self.in_product:
            self.in_product = False


class InquiryFormMarkupTests(unittest.TestCase):
    def parse(self, locale):
        parser = InquiryParser()
        parser.feed(contact_path(locale).read_text(encoding="utf-8"))
        return parser

    def test_all_locales_use_same_origin_three_step_form(self):
        expected_names = None
        for locale in LOCALES:
            with self.subTest(locale=locale):
                parser = self.parse(locale)
                self.assertEqual(len(parser.forms), 1)
                self.assertEqual(parser.forms[0].get("action"), "/api/inquiry")
                self.assertEqual(parser.forms[0].get("method", "").lower(), "post")
                self.assertEqual(len(parser.fieldsets), 3)
                self.assertGreaterEqual(parser.legends, 3)
                self.assertGreaterEqual(parser.live_regions, 2)
                self.assertIn("/inquiry-form.js", parser.scripts)
                self.assertEqual(parser.product_values, PRODUCT_IDS)
                self.assertTrue({"inquiryProgress", "inquiryErrors", "inquirySuccess", "inquiryFailure"}.issubset(parser.ids))
                if expected_names is None:
                    expected_names = parser.names
                self.assertEqual(parser.names, expected_names)

    def test_form_contract_has_security_and_conditional_fields(self):
        names = self.parse("en").names
        self.assertTrue({
            "product", "recommendation_branch", "target_flow", "purity", "output_pressure",
            "laser_count", "psa_laser_power", "operating_hours", "retained_modules",
            "installation_space", "laser_brand", "mixer_laser_power", "material", "thickness",
            "current_gas", "nitrogen_source", "nitrogen_inlet_pressure", "oxygen_source",
            "oxygen_inlet_pressure", "required_flow", "installation_preference", "control_interface",
            "name", "company", "country", "email", "phone", "preferred_channel",
            "customer_type", "message", "consent", "website",
        }.issubset(names))

    def test_no_public_page_or_script_contains_web3forms_contract(self):
        offenders = []
        for path in PUBLIC.rglob("*"):
            if path.suffix.lower() not in {".html", ".js"}:
                continue
            content = path.read_text(encoding="utf-8")
            if "api.web3forms.com" in content or "access_key" in content:
                offenders.append(str(path.relative_to(PUBLIC)))
        self.assertEqual(offenders, [])

    def test_contact_pages_do_not_promise_a_24_hour_response(self):
        offenders = []
        for locale in LOCALES:
            content = contact_path(locale).read_text(encoding="utf-8")
            if re.search(r"24\s*(hours?|hrs?|小时|時間|시간|horas?|godzin)", content, re.IGNORECASE):
                offenders.append(locale)
        self.assertEqual(offenders, [])

    def test_client_submits_same_origin_json_without_browser_storage(self):
        script = (PUBLIC / "inquiry-form.js").read_text(encoding="utf-8")
        self.assertIn("fetch('/api/inquiry'", script)
        self.assertIn("application/json", script)
        self.assertNotIn("localStorage", script)
        self.assertNotIn("sessionStorage", script)
        self.assertRegex(script, r"if\s*\(result\.ok\)")
        self.assertLess(script.index("if (result.ok)"), script.index("trackLead('Contact Form')"))


if __name__ == "__main__":
    unittest.main()
