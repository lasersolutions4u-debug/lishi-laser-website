import json
import re
import subprocess
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
EXPECTED_CHOICE_VALUES = {
    "product": {"", *PRODUCT_IDS},
    "recommendation_branch": {"", "psa", "mixer", "both"},
    "retained_modules": {
        "air-compressor", "dryer", "filters", "air-buffer-tank",
        "nitrogen-storage", "booster", "none",
    },
    "material": {"", "carbon_steel", "stainless_steel", "aluminum", "mixed", "other"},
    "current_gas": {"", "oxygen", "nitrogen", "air", "mixed", "unknown"},
    "installation_preference": {"", "cabinet", "valve", "unsure"},
    "control_interface": {"", "analog", "modbus", "plc-custom", "unsure"},
    "preferred_channel": {"", "email", "phone", "whatsapp"},
    "customer_type": {"", "end_user", "factory", "integrator", "project_owner", "other"},
}
EXPECTED_FIELD_NAMES = {
    "product", "recommendation_branch", "target_flow", "purity", "output_pressure",
    "laser_count", "psa_laser_power", "operating_hours", "retained_modules",
    "installation_space", "laser_brand", "mixer_laser_power", "material", "thickness",
    "current_gas", "nitrogen_source", "nitrogen_inlet_pressure", "oxygen_source",
    "oxygen_inlet_pressure", "required_flow", "installation_preference", "control_interface",
    "name", "company", "country", "email", "phone", "preferred_channel",
    "customer_type", "message", "consent", "website",
}
EXPECTED_CONTROL_NAMES_BY_ID = {
    "product": "product",
    "recommendation_branch": "recommendation_branch",
    "target_flow": "target_flow",
    "purity": "purity",
    "output_pressure": "output_pressure",
    "laser_count": "laser_count",
    "psa_laser_power": "psa_laser_power",
    "operating_hours": "operating_hours",
    "installation_space": "installation_space",
    "laser_brand": "laser_brand",
    "mixer_laser_power": "mixer_laser_power",
    "material": "material",
    "thickness": "thickness",
    "current_gas": "current_gas",
    "nitrogen_source": "nitrogen_source",
    "nitrogen_inlet_pressure": "nitrogen_inlet_pressure",
    "oxygen_source": "oxygen_source",
    "oxygen_inlet_pressure": "oxygen_inlet_pressure",
    "required_flow": "required_flow",
    "installation_preference": "installation_preference",
    "control_interface": "control_interface",
    "name": "name",
    "company": "company",
    "country": "country",
    "email": "email",
    "phone": "phone",
    "preferred_channel": "preferred_channel",
    "customer_type": "customer_type",
    "message": "message",
    "consent": "consent",
    "website": "website",
}
EXPECTED_BRANCH_CONTROL_IDS = {
    "psa": {
        "target_flow",
        "purity",
        "output_pressure",
        "laser_count",
        "psa_laser_power",
        "operating_hours",
        "installation_space",
    },
    "mixer": {
        "laser_brand",
        "mixer_laser_power",
        "material",
        "thickness",
        "current_gas",
        "nitrogen_source",
        "nitrogen_inlet_pressure",
        "oxygen_source",
        "oxygen_inlet_pressure",
        "required_flow",
        "installation_preference",
        "control_interface",
    },
}
EXPECTED_STEP_BUTTON_BINDINGS = [
    ("next", "1"),
    ("back", "2"),
    ("next", "2"),
    ("back", "3"),
]
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

LABEL_KEYS_BY_ID = {
    "product": "solution_or_product_interest",
    "recommendation_branch": "which_supply_area_should_we_assess",
    "target_flow": "target_nitrogen_flow",
    "purity": "required_purity",
    "output_pressure": "output_pressure",
    "laser_count": "number_of_lasers",
    "psa_laser_power": "laser_power",
    "operating_hours": "operating_hours",
    "installation_space": "available_installation_space",
    "laser_brand": "laser_brand_model",
    "mixer_laser_power": "laser_power",
    "material": "main_material",
    "thickness": "thickness_range",
    "current_gas": "current_assist_gas",
    "nitrogen_source": "nitrogen_source",
    "nitrogen_inlet_pressure": "nitrogen_inlet_pressure",
    "oxygen_source": "oxygen_source",
    "oxygen_inlet_pressure": "oxygen_inlet_pressure",
    "required_flow": "required_mixed_gas_flow",
    "installation_preference": "installation_preference",
    "control_interface": "control_interface",
    "name": "full_name",
    "company": "company",
    "country": "country_region",
    "email": "business_email",
    "phone": "phone_whatsapp",
    "preferred_channel": "preferred_contact_channel",
    "customer_type": "customer_type",
    "message": "project_details",
}
OPTION_KEYS_BY_SELECT = {
    "product": {
        "": "select_one",
        "psa-nitrogen-system": "psa_nitrogen_generation_system",
        "integrated-mixing-cabinet": "integrated_gas_mixing_cabinet",
        "mspv2-4000": ("MSPV2-4000", "proportional_valve_2"),
        "need-recommendation": "help_me_choose",
    },
    "recommendation_branch": {
        "": "select_one",
        "psa": "nitrogen_generation",
        "mixer": "mixed_gas_control",
        "both": "both",
    },
    "material": {
        "": "select_one",
        "carbon_steel": "carbon_steel",
        "stainless_steel": "stainless_steel",
        "aluminum": "aluminum",
        "mixed": "mixed_materials",
        "other": "other",
    },
    "current_gas": {
        "": "select_one",
        "oxygen": "oxygen",
        "nitrogen": "nitrogen",
        "air": "compressed_air",
        "mixed": "mixed_gas",
        "unknown": "not_sure",
    },
    "installation_preference": {
        "": "select_one",
        "cabinet": "integrated_cabinet",
        "valve": "proportional_valve",
        "unsure": "need_recommendation",
    },
    "control_interface": {
        "": "select_one",
        "analog": "analog",
        "modbus": "modbus",
        "plc-custom": "custom_plc",
        "unsure": "not_sure",
    },
    "preferred_channel": {
        "": "select_one",
        "email": ("shared", "email"),
        "phone": "phone",
        "whatsapp": ("shared", "whatsapp"),
    },
    "customer_type": {
        "": "select_one",
        "end_user": "end_user",
        "factory": "factory",
        "integrator": "system_integrator",
        "project_owner": "project_purchasing_team",
        "other": "other",
    },
}
JOURNEY_TEXT_KEYS = {
    "modules_already_available",
    "air_compressor",
    "air_dryer",
    "filters",
    "air_buffer_tank",
    "nitrogen_storage",
    "booster",
    "none",
    "continue",
    "back",
    "review_summary",
    "send_assessment_request",
    "i_agree_that",
    "may_use_these_details_to_evaluate_and_respond_to_this_inquiry",
    "request_received",
    "your_project_information_was_delivered_to_the_sales_team",
    "the_form_could_not_be_delivered",
    "your_entries_are_still_on_this_page_please_retry_or_contact_us_directly",
    "reference",
}
EXPECTED_BACKEND_BLOBS = {
    "functions/api/inquiry.js": "78668c319f498188b56e0ba5808818b5cb6c98fa",
    "workers/inquiry-mailer/src/index.mjs": "7131347938d066f8e21929d22554874dcd2a0ab0",
}
INQUIRY_DATA_ATTRIBUTES = {
    "data-inquiry-form",
    "data-sending",
    "data-required-message",
    "data-step",
    "data-recommendation-only",
    "data-next",
    "data-branch",
    "data-required-group",
    "data-required",
    "data-msp-only",
    "data-back",
    "data-template",
    "data-progress-text",
    "data-progress-bar",
    "data-inquiry-reference",
}
EXPECTED_MACHINE_DATA_ATTRIBUTES = {
    "data-inquiry-form": [None],
    "data-step": ["1", "2", "3"],
    "data-recommendation-only": [None],
    "data-next": [None, None],
    "data-branch": ["psa", "mixer"],
    "data-required-group": ["retained_modules"],
    "data-required": [None] * 19,
    "data-msp-only": [None],
    "data-back": [None, None],
    "data-progress-text": [None],
    "data-progress-bar": [None],
    "data-inquiry-reference": [None],
}


def contact_path(locale):
    return PUBLIC / "contact.html" if locale == "en" else PUBLIC / locale / "contact.html"


def normalize_text(value):
    return " ".join(value.split())


class InquiryParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.fieldsets = []
        self.legends = 0
        self.names = set()
        self.product_values = set()
        self.current_select = None
        self.choice_values = {}
        self.scripts = []
        self.ids = set()
        self.id_counts = {}
        self.live_regions = 0
        self.controls = {}
        self.honeypots = 0
        self.attrs_by_id = {}
        self.legend_texts = []
        self.label_texts = {}
        self.option_texts = {}
        self.region_texts = {}
        self.form_text = []
        self.form_text_nodes = set()
        self.consent_text = ""
        self.in_form = False
        self.captures = []
        self.inquiry_data_attributes = {
            name: [] for name in INQUIRY_DATA_ATTRIBUTES
        }
        self.element_stack = []
        self.branch_control_ids = {"psa": set(), "mixer": set()}
        self.branch_choice_values = {"psa": {}, "mixer": {}}
        self.step_button_bindings = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in INQUIRY_DATA_ATTRIBUTES:
            if name in attrs:
                self.inquiry_data_attributes[name].append(attrs[name])
        if attrs.get("id"):
            self.ids.add(attrs["id"])
            self.id_counts[attrs["id"]] = self.id_counts.get(attrs["id"], 0) + 1
            self.attrs_by_id[attrs["id"]] = attrs
        if tag == "form" and attrs.get("id") == "contactForm":
            self.forms.append(attrs)
            self.in_form = True
        if tag == "fieldset" and attrs.get("data-step"):
            self.fieldsets.append(attrs)
        if tag == "legend":
            self.legends += 1
        if tag in {"input", "select", "textarea"} and attrs.get("name"):
            self.names.add(attrs["name"])
            if attrs.get("id"):
                self.controls[attrs["id"]] = attrs
        if "inquiry-honeypot" in attrs.get("class", "").split():
            self.honeypots += 1
        if tag == "select" and attrs.get("name"):
            self.current_select = attrs["name"]
            self.choice_values.setdefault(self.current_select, set())
        if tag == "legend":
            self.captures.append((tag, "legend", None, []))
        if tag == "label" and attrs.get("for"):
            self.captures.append((tag, "label", attrs["for"], []))
        if tag == "label" and "inquiry-consent" in attrs.get("class", "").split():
            self.captures.append((tag, "consent", None, []))
        if tag == "option" and self.current_select and "value" in attrs:
            self.captures.append(
                (tag, "option", (self.current_select, attrs["value"]), [])
            )
        if attrs.get("id") in {"inquiryProgress", "inquirySuccess", "inquiryFailure"}:
            self.captures.append((tag, "region", attrs["id"], []))
        if tag == "option" and self.current_select and "value" in attrs:
            self.choice_values[self.current_select].add(attrs["value"])
            if self.current_select == "product" and attrs["value"]:
                self.product_values.add(attrs["value"])
        if (
            tag == "input"
            and attrs.get("type") in {"checkbox", "radio"}
            and attrs.get("name")
            and "value" in attrs
        ):
            self.choice_values.setdefault(attrs["name"], set()).add(attrs["value"])
        current_step = next(
            (
                ancestor_attrs["data-step"]
                for _ancestor_tag, ancestor_attrs in reversed(self.element_stack)
                if "data-step" in ancestor_attrs
            ),
            None,
        )
        current_branch = next(
            (
                ancestor_attrs["data-branch"]
                for _ancestor_tag, ancestor_attrs in reversed(self.element_stack)
                if "data-branch" in ancestor_attrs
            ),
            None,
        )
        if tag in {"input", "select", "textarea"} and current_branch in self.branch_control_ids:
            if attrs.get("id"):
                self.branch_control_ids[current_branch].add(attrs["id"])
            if attrs.get("name") and "value" in attrs:
                self.branch_choice_values[current_branch].setdefault(
                    attrs["name"], set()
                ).add(attrs["value"])
        if tag == "button" and current_step:
            if "data-next" in attrs:
                self.step_button_bindings.append(("next", current_step))
            if "data-back" in attrs:
                self.step_button_bindings.append(("back", current_step))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if attrs.get("aria-live") in {"polite", "assertive"}:
            self.live_regions += 1
        if tag not in VOID_ELEMENTS:
            self.element_stack.append((tag, attrs))

    def handle_endtag(self, tag):
        for index in range(len(self.captures) - 1, -1, -1):
            capture_tag, kind, key, chunks = self.captures[index]
            if capture_tag != tag:
                continue
            self.captures.pop(index)
            value = normalize_text("".join(chunks))
            if kind == "legend":
                self.legend_texts.append(value)
            elif kind == "label":
                self.label_texts[key] = value
            elif kind == "option":
                select_name, option_value = key
                self.option_texts.setdefault(select_name, {})[option_value] = value
            elif kind == "consent":
                self.consent_text = value
            else:
                self.region_texts[key] = value
            break
        if tag == "select":
            self.current_select = None
        if tag == "form" and self.in_form:
            self.in_form = False
        for index in range(len(self.element_stack) - 1, -1, -1):
            if self.element_stack[index][0] == tag:
                del self.element_stack[index:]
                break

    def handle_data(self, data):
        if self.in_form:
            self.form_text.append(data)
            if normalize_text(data):
                self.form_text_nodes.add(normalize_text(data))
        for _tag, _kind, _key, chunks in self.captures:
            chunks.append(data)


def parse_inquiry_html(html):
    parser = InquiryParser()
    parser.feed(html)
    return parser


def assert_inquiry_contract(test_case, html):
    parser = parse_inquiry_html(html)
    test_case.assertEqual(len(parser.forms), 1)
    form = parser.forms[0]
    test_case.assertEqual(form.get("action"), "/api/inquiry")
    test_case.assertEqual(form.get("method", "").lower(), "post")
    test_case.assertIn("data-inquiry-form", form)
    test_case.assertIn("data-sending", form)
    test_case.assertIn("data-required-message", form)
    test_case.assertIn("novalidate", form)
    test_case.assertEqual([fieldset["data-step"] for fieldset in parser.fieldsets], ["1", "2", "3"])
    test_case.assertGreaterEqual(parser.legends, 3)
    test_case.assertGreaterEqual(parser.live_regions, 2)
    test_case.assertIn("/inquiry-form.js", parser.scripts)
    test_case.assertEqual(parser.product_values, PRODUCT_IDS)
    test_case.assertEqual(parser.choice_values, EXPECTED_CHOICE_VALUES)
    test_case.assertEqual(parser.names, EXPECTED_FIELD_NAMES)
    test_case.assertEqual(
        {control_id: attrs["name"] for control_id, attrs in parser.controls.items()},
        EXPECTED_CONTROL_NAMES_BY_ID,
    )
    test_case.assertEqual(parser.branch_control_ids, EXPECTED_BRANCH_CONTROL_IDS)
    test_case.assertEqual(
        parser.branch_choice_values,
        {
            "psa": {"retained_modules": EXPECTED_CHOICE_VALUES["retained_modules"]},
            "mixer": {},
        },
    )
    test_case.assertEqual(parser.step_button_bindings, EXPECTED_STEP_BUTTON_BINDINGS)
    for attribute, expected_values in EXPECTED_MACHINE_DATA_ATTRIBUTES.items():
        test_case.assertCountEqual(
            parser.inquiry_data_attributes[attribute],
            expected_values,
            attribute,
        )
    test_case.assertTrue({
        "inquiryProgress", "inquiryErrors", "inquiryReview", "inquirySuccess", "inquiryFailure",
    }.issubset(parser.ids))
    for element_id in {
        "contactForm", "inquiryProgress", "inquiryErrors", "inquiryReview",
        "inquirySuccess", "inquiryFailure",
    }:
        test_case.assertEqual(parser.id_counts.get(element_id), 1, element_id)
    for attribute in {"data-sending", "data-required-message", "data-template"}:
        test_case.assertEqual(
            len(parser.inquiry_data_attributes[attribute]),
            1,
            attribute,
        )
    test_case.assertEqual(parser.honeypots, 1)
    test_case.assertEqual(parser.controls["website"].get("autocomplete"), "off")
    test_case.assertEqual(parser.controls["website"].get("tabindex"), "-1")
    test_case.assertIn("required", parser.controls["consent"])
    for control_id in ("product", "name", "company", "country", "email", "phone", "preferred_channel", "customer_type", "message"):
        test_case.assertIn("required", parser.controls[control_id], control_id)
    for control_id in ("target_flow", "purity", "output_pressure", "laser_count", "psa_laser_power", "operating_hours", "installation_space", "laser_brand", "mixer_laser_power", "material", "thickness", "current_gas", "nitrogen_source", "nitrogen_inlet_pressure", "oxygen_source", "oxygen_inlet_pressure", "required_flow", "installation_preference", "control_interface"):
        test_case.assertIn("data-required", parser.controls[control_id], control_id)
        test_case.assertIn("disabled", parser.controls[control_id], control_id)
    test_case.assertNotIn("api.web3forms.com", html)
    test_case.assertNotIn("access_key", html)
    return parser


class InquiryFormMarkupTests(unittest.TestCase):
    def parse(self, locale):
        return parse_inquiry_html(contact_path(locale).read_text(encoding="utf-8"))

    def expected_copy(self, data, key_spec):
        if isinstance(key_spec, tuple):
            if key_spec[0] == "shared":
                return data["shared"]["copy"][key_spec[1]]
            prefix, contact_key = key_spec
            return prefix + data["contact"]["copy"][contact_key]
        return data["contact"]["copy"][key_spec]

    def assert_localized_journey(self, parser, data, english, locale):
        copy = data["contact"]["copy"]
        english_copy = english["contact"]["copy"]

        self.assertEqual(
            parser.legend_texts,
            [
                copy["01_choose_a_solution"],
                copy["02_operating_conditions"],
                copy["03_contact_and_review"],
            ],
        )
        for control_id, copy_key in LABEL_KEYS_BY_ID.items():
            self.assertEqual(
                parser.label_texts[control_id],
                normalize_text(copy[copy_key]),
                f"{locale}:{control_id}",
            )

        for select_name, option_specs in OPTION_KEYS_BY_SELECT.items():
            expected_options = {
                value: normalize_text(self.expected_copy(data, key_spec))
                for value, key_spec in option_specs.items()
            }
            self.assertEqual(
                parser.option_texts[select_name],
                expected_options,
                f"{locale}:{select_name}",
            )

        form = parser.forms[0]
        self.assertEqual(form["data-sending"], copy["sending"])
        self.assertEqual(
            form["data-required-message"],
            copy["please_complete_the_required_fields_in_this_step"],
        )
        self.assertEqual(
            parser.attrs_by_id["inquiryProgress"]["data-template"],
            copy["step_current_of_3"],
        )
        self.assertIn(normalize_text(copy["step_1_of_3"]), parser.region_texts["inquiryProgress"])

        form_text = normalize_text(" ".join(parser.form_text))
        for copy_key in JOURNEY_TEXT_KEYS - {
            "request_received",
            "your_project_information_was_delivered_to_the_sales_team",
            "the_form_could_not_be_delivered",
            "your_entries_are_still_on_this_page_please_retry_or_contact_us_directly",
            "reference",
        }:
            self.assertIn(normalize_text(copy[copy_key]), form_text, f"{locale}:{copy_key}")
        expected_consent = normalize_text(
            copy["i_agree_that"]
            + "Jinan Euchio Machinery Co., Ltd."
            + copy["may_use_these_details_to_evaluate_and_respond_to_this_inquiry"]
        )
        self.assertEqual(parser.consent_text, expected_consent)
        for copy_key in {
            "request_received",
            "your_project_information_was_delivered_to_the_sales_team",
            "reference",
        }:
            self.assertIn(
                normalize_text(copy[copy_key]),
                parser.region_texts["inquirySuccess"],
                f"{locale}:{copy_key}",
            )
        for copy_key in {
            "the_form_could_not_be_delivered",
            "your_entries_are_still_on_this_page_please_retry_or_contact_us_directly",
        }:
            self.assertIn(
                normalize_text(copy[copy_key]),
                parser.region_texts["inquiryFailure"],
                f"{locale}:{copy_key}",
            )

        if locale == "en":
            return
        translated_contact_keys = set(LABEL_KEYS_BY_ID.values()) | JOURNEY_TEXT_KEYS | {
            "01_choose_a_solution",
            "02_operating_conditions",
            "03_contact_and_review",
            "sending",
            "please_complete_the_required_fields_in_this_step",
            "step_current_of_3",
        }
        for option_specs in OPTION_KEYS_BY_SELECT.values():
            translated_contact_keys.update(
                key_spec if isinstance(key_spec, str) else key_spec[1]
                for key_spec in option_specs.values()
                if not (isinstance(key_spec, tuple) and key_spec[0] == "shared")
            )
        for copy_key in translated_contact_keys - {"modbus"}:
            self.assertNotEqual(
                normalize_text(copy[copy_key]),
                normalize_text(english_copy[copy_key]),
                f"English residual in {locale}:contact.copy.{copy_key}",
            )
        form_node_keys = JOURNEY_TEXT_KEYS - {
            "i_agree_that",
            "may_use_these_details_to_evaluate_and_respond_to_this_inquiry",
            "request_received",
            "your_project_information_was_delivered_to_the_sales_team",
            "the_form_could_not_be_delivered",
            "your_entries_are_still_on_this_page_please_retry_or_contact_us_directly",
            "reference",
        }
        for copy_key in form_node_keys:
            self.assertNotIn(
                normalize_text(english_copy[copy_key]),
                parser.form_text_nodes,
                f"English residual in rendered {locale} form: {copy_key}",
            )
        english_consent = normalize_text(
            english_copy["i_agree_that"]
            + "Jinan Euchio Machinery Co., Ltd."
            + english_copy["may_use_these_details_to_evaluate_and_respond_to_this_inquiry"]
        )
        self.assertNotEqual(parser.consent_text, english_consent)
        for copy_key in {
            "request_received",
            "your_project_information_was_delivered_to_the_sales_team",
            "reference",
        }:
            self.assertNotIn(
                normalize_text(english_copy[copy_key]),
                parser.region_texts["inquirySuccess"],
                f"English residual in rendered {locale} success state: {copy_key}",
            )
        for copy_key in {
            "the_form_could_not_be_delivered",
            "your_entries_are_still_on_this_page_please_retry_or_contact_us_directly",
        }:
            self.assertNotIn(
                normalize_text(english_copy[copy_key]),
                parser.region_texts["inquiryFailure"],
                f"English residual in rendered {locale} failure state: {copy_key}",
            )
        self.assertNotEqual(
            normalize_text(data["shared"]["copy"]["email"]),
            normalize_text(english["shared"]["copy"]["email"]),
            f"English residual in {locale}:shared.copy.email",
        )

    def test_all_locales_use_same_origin_three_step_form(self):
        expected_names = None
        for locale in LOCALES:
            with self.subTest(locale=locale):
                parser = assert_inquiry_contract(
                    self, contact_path(locale).read_text(encoding="utf-8")
                )
                if expected_names is None:
                    expected_names = parser.names
                self.assertEqual(parser.names, expected_names)

    def test_form_contract_has_security_and_conditional_fields(self):
        names = self.parse("en").names
        self.assertEqual(names, EXPECTED_FIELD_NAMES)

    def test_contract_rejects_swapped_control_name_bindings(self):
        html = contact_path("en").read_text(encoding="utf-8")
        mutated = html.replace('name="target_flow"', 'name="__purity__"', 1)
        mutated = mutated.replace('name="purity"', 'name="target_flow"', 1)
        mutated = mutated.replace('name="__purity__"', 'name="purity"', 1)
        with self.assertRaises(AssertionError):
            assert_inquiry_contract(self, mutated)

    def test_contract_rejects_swapped_branch_bindings(self):
        html = contact_path("en").read_text(encoding="utf-8")
        mutated = html.replace('data-branch="psa"', 'data-branch="__mixer__"', 1)
        mutated = mutated.replace('data-branch="mixer"', 'data-branch="psa"', 1)
        mutated = mutated.replace('data-branch="__mixer__"', 'data-branch="mixer"', 1)
        with self.assertRaises(AssertionError):
            assert_inquiry_contract(self, mutated)

    def test_all_locales_render_the_complete_localized_inquiry_journey(self):
        english = json.loads((PUBLIC / "i18n" / "core" / "en.json").read_text(encoding="utf-8"))
        for locale in LOCALES:
            with self.subTest(locale=locale):
                data = json.loads(
                    (PUBLIC / "i18n" / "core" / f"{locale}.json").read_text(encoding="utf-8")
                )
                parser = self.parse(locale)
                self.assert_localized_journey(parser, data, english, locale)

    def test_inquiry_backend_files_remain_byte_for_byte_immutable(self):
        for relative_path, expected_blob in EXPECTED_BACKEND_BLOBS.items():
            with self.subTest(path=relative_path):
                actual_blob = subprocess.check_output(
                    ["git", "hash-object", "--", relative_path],
                    cwd=ROOT,
                    text=True,
                ).strip()
                self.assertEqual(actual_blob, expected_blob)

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
