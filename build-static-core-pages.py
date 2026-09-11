#!/usr/bin/env python3
"""Build the locale-aware About and Contact pages from reviewed content."""

import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path

from site_locales import SUPPORTED_LOCALES, alternates_for, canonical_url, output_path, route_for


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
TEMPLATE_DIR = PUBLIC / "core-page-templates"
CONTENT_DIR = PUBLIC / "i18n" / "core"
PAGE_KEYS = ("about", "contact")

# Presentation order preserves the approved pages; URLs still come from site_locales.py.
LANGUAGE_ORDER = ("en", "zh", "es", "ko", "ja", "pt", "pl")
LANGUAGE_NAMES = {
    "en": "English",
    "zh": "中文",
    "es": "Español",
    "ko": "한국어",
    "ja": "日本語",
    "pt": "Português",
    "pl": "Polski",
}

REQUIRED_KEYS = (
    "shared.language_label",
    "shared.home",
    "shared.products",
    "shared.applications",
    "shared.results",
    "shared.resources",
    "shared.about",
    "shared.request",
    "about.title",
    "about.description",
    "contact.title",
    "contact.description",
)

# Exact counts cover only copy intentionally reused by the approved two-page source.
# Every other translation leaf is allowed exactly once.
REUSABLE_KEYS = {
    "about.copy.contact_us": 2,
    "about.copy.deployment": 3,
    "about.copy.get_a_quote": 2,
    "about.copy.website": 2,
    "contact.copy.back": 2,
    "contact.copy.continue": 2,
    "contact.copy.laser_power": 2,
    "contact.copy.not_sure": 2,
    "contact.copy.other": 2,
    "contact.copy.select_one": 8,
    "about.title": 2,
    "contact.description": 2,
    "contact.title": 3,
    "shared.about": 3,
    "shared.applications": 2,
    "shared.copy.advantages": 2,
    "shared.copy.all_rights_reserved": 2,
    "shared.copy.application_assessment": 2,
    "shared.copy.blog": 2,
    "shared.copy.chat_on_whatsapp": 2,
    "shared.copy.compact_valve": 2,
    "shared.copy.company": 2,
    "shared.copy.compare_both_mixers": 2,
    "shared.copy.complete_machines": 2,
    "shared.copy.complete_machines_and": 2,
    "shared.copy.contact": 2,
    "shared.copy.cutting_samples": 2,
    "shared.copy.dhgate_store": 2,
    "shared.copy.email": 3,
    "shared.copy.gas_mixing_technology": 3,
    "shared.copy.how_it_works": 2,
    "shared.copy.integrated_gas_mixing_cabinet": 2,
    "shared.copy.is_an_industrial_equipment_solutions_and_service_company_focused_on_shee": 2,
    "shared.copy.laser_cutting_assist_gas_solutions": 2,
    "shared.copy.linkedin": 3,
    "shared.copy.main_navigation": 2,
    "shared.copy.mexico": 2,
    "shared.copy.mixed_gas_control": 2,
    "shared.copy.mro_parts_and_service": 2,
    "shared.copy.nitrogen_supply": 2,
    "shared.copy.parameters": 2,
    "shared.copy.parts": 2,
    "shared.copy.phone_wechat": 2,
    "shared.copy.privacy_policy": 2,
    "shared.copy.product": 2,
    "shared.copy.psa_nitrogen_generation_system": 2,
    "shared.copy.related_links": 2,
    "shared.copy.service": 5,
    "shared.copy.skip_to_content": 2,
    "shared.copy.thailand": 2,
    "shared.copy.toggle_menu": 2,
    "shared.copy.website": 2,
    "shared.copy.whatsapp": 5,
    "shared.copy.whatsapp_mexico": 2,
    "shared.copy.whatsapp_thailand": 2,
    "shared.home": 2,
    "shared.language_label": 2,
    "shared.products": 2,
    "shared.request": 2,
    "shared.resources": 2,
    "shared.results": 2,
}

ALLOWED_UNUSED_KEYS = frozenset()
ALLOWED_EMPTY_KEYS = frozenset()

PLACEHOLDER = re.compile(r"\{\{(?P<kind>text|attr|json|safe):(?P<key>[a-zA-Z0-9_.-]+)\}\}")


class SafeMarkup(str):
    """Markup assembled exclusively from trusted routing data."""


def parse_locales(values):
    locales = tuple(values) if values else SUPPORTED_LOCALES
    unknown = sorted(set(locales) - set(SUPPORTED_LOCALES))
    if unknown:
        raise ValueError("Unsupported locale: " + ", ".join(unknown))
    duplicates = sorted(locale for locale in set(locales) if locales.count(locale) > 1)
    if duplicates:
        raise ValueError("Duplicate locale: " + ", ".join(duplicates))
    return locales


def leaf_paths(value, prefix=""):
    paths = set()
    if isinstance(value, dict):
        if not value and prefix:
            paths.add(prefix)
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            paths.update(leaf_paths(child, child_prefix))
    elif isinstance(value, list):
        if not value and prefix:
            paths.add(prefix)
        for index, child in enumerate(value):
            paths.update(leaf_paths(child, f"{prefix}.{index}"))
    else:
        paths.add(prefix)
    return paths


class ContentTracker:
    def __init__(self, content):
        self.content = content
        self.used = Counter({"locale": 1})

    def peek(self, path):
        value = self.content
        for part in path.split("."):
            if isinstance(value, list):
                try:
                    value = value[int(part)]
                except (IndexError, ValueError) as exc:
                    raise KeyError(f"Missing content key: {path}") from exc
            else:
                if not isinstance(value, dict) or part not in value:
                    raise KeyError(f"Missing content key: {path}")
                value = value[part]
        return value

    def use(self, path):
        value = self.peek(path)
        self.used.update(leaf_paths(value, path))
        return value

    def validate_required(self):
        for path in REQUIRED_KEYS:
            value = self.peek(path)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Required content key must be a non-empty string: {path}"
                )

    def validate_non_empty(self):
        for path in sorted(leaf_paths(self.content)):
            value = self.peek(path)
            if (
                isinstance(value, str)
                and not value.strip()
                and path not in ALLOWED_EMPTY_KEYS
            ):
                raise ValueError(
                    f"Translation content key must be a non-empty string: {path}"
                )

    def assert_usage(self):
        leaves = leaf_paths(self.content)
        unused = sorted(
            path
            for path in leaves
            if self.used[path] == 0 and path not in ALLOWED_UNUSED_KEYS
        )
        if unused:
            details = ", ".join(
                f"{path} (actual 0, allowed {REUSABLE_KEYS.get(path, 1)})"
                for path in unused
            )
            raise ValueError("Unused content keys: " + details)
        for path in sorted(leaves):
            actual = self.used[path]
            allowed = REUSABLE_KEYS.get(path, 1)
            if path in ALLOWED_UNUSED_KEYS and actual == 0:
                continue
            if actual != allowed:
                raise ValueError(
                    f"Invalid content key usage: {path}: actual {actual}, allowed {allowed}"
                )


class DuplicateTranslationKey(ValueError):
    def __init__(self, key):
        self.key = key
        super().__init__(key)


def _reject_duplicate_keys(pairs):
    value = {}
    for key, child in pairs:
        if key in value:
            raise DuplicateTranslationKey(key)
        value[key] = child
    return value


def load_content(locale, content_dir=CONTENT_DIR):
    path = Path(content_dir) / f"{locale}.json"
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Missing translation file: {path.name}") from exc
    try:
        content = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except DuplicateTranslationKey as exc:
        raise ValueError(f"Duplicate translation key in {path.name}: {exc.key}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid translation JSON: {path.name}") from exc
    if not isinstance(content, dict):
        raise ValueError(f"Invalid translation root: {path.name}")
    if content.get("locale") != locale:
        raise ValueError(f"Translation locale mismatch: {path.name}")
    return content


def _json_string(value):
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def _escape_attribute(value):
    return html.escape(value, quote=False).replace('"', "&quot;")


def _normalize_newlines(value):
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _raise_context_error(locale, page_key, match, detail):
    raise ValueError(
        f"Invalid placeholder context: {locale}/{page_key}: "
        f"{match.group('kind')}:{match.group('key')}: {detail}"
    )


def _raise_template_error(locale, page_key, detail):
    raise ValueError(f"Invalid template context: {locale}/{page_key}: {detail}")


def _tag_has_attribute(tag_text, name, value=None):
    match = re.search(
        rf"\b{re.escape(name)}\s*=\s*([\"'])(?P<value>.*?)\1",
        tag_text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return False
    if value is None:
        return True
    return match.group("value") == value


def _is_language_menu_tag(tag_text):
    class_match = re.search(
        r"\bclass\s*=\s*([\"'])(?P<value>.*?)\1",
        tag_text,
        re.IGNORECASE | re.DOTALL,
    )
    return bool(
        class_match
        and "lang-dropdown" in class_match.group("value").split()
        and _tag_has_attribute(tag_text, "id", "langDropdown")
    )


def _scan_template_contexts(template_text, locale, page_key):
    placeholder_starts = {match.start() for match in PLACEHOLDER.finditer(template_text)}
    contexts = {}
    state = "data"
    quote = None
    attribute_name = None
    tag_start = None
    raw_open_tag = None
    closing_raw_tag = None
    in_head = False
    div_stack = []
    index = 0
    lowered = template_text.lower()

    while index < len(template_text):
        if index in placeholder_starts:
            placeholder_state = "attribute" if state == "tag" and quote else state
            contexts[index] = {
                "state": placeholder_state,
                "quote": quote,
                "attribute_name": attribute_name,
                "raw_open_tag": raw_open_tag,
                "in_head": in_head,
                "in_language_menu": bool(div_stack and div_stack[-1]),
            }

        if state == "comment":
            if template_text.startswith("-->", index):
                state = "data"
                index += 3
            else:
                index += 1
            continue

        if state in {"script", "style"}:
            closing = f"</{state}"
            if lowered.startswith(closing, index):
                boundary = index + len(closing)
                if boundary < len(template_text) and not (
                    template_text[boundary].isspace() or template_text[boundary] == ">"
                ):
                    index += 1
                    continue
                closing_raw_tag = state
                state = "tag"
                tag_start = index
                quote = None
                attribute_name = None
                index += 1
            else:
                index += 1
            continue

        if state == "data":
            if template_text.startswith("<!--", index):
                state = "comment"
                index += 4
                continue
            if template_text[index] == "<":
                state = "tag"
                tag_start = index
                quote = None
                attribute_name = None
            index += 1
            continue

        character = template_text[index]
        if quote:
            if character == quote:
                quote = None
                attribute_name = None
            index += 1
            continue
        if character in {'"', "'"}:
            before_quote = template_text[tag_start + 1 : index]
            attribute_match = re.search(
                r"(?:^|\s)(?P<name>[^\s=<>/]+)\s*=\s*$", before_quote
            )
            if not attribute_match:
                _raise_template_error(locale, page_key, "quote outside an attribute value")
            quote = character
            attribute_name = attribute_match.group("name")
            index += 1
            continue
        if character == "<":
            _raise_template_error(locale, page_key, "unexpected < inside a tag")
        if character != ">":
            index += 1
            continue

        tag_text = template_text[tag_start : index + 1]
        tag_match = re.match(
            r"<\s*(?P<closing>/)?\s*(?P<name>[a-zA-Z][a-zA-Z0-9:-]*)\b",
            tag_text,
        )
        if not tag_match:
            if not re.match(r"<\s*[!?]", tag_text):
                _raise_template_error(locale, page_key, "unrecognized tag boundary")
            state = "data"
            index += 1
            continue

        name = tag_match.group("name").lower()
        closing = bool(tag_match.group("closing"))
        self_closing = tag_text.rstrip().endswith("/>")
        if closing_raw_tag:
            if not closing or name != closing_raw_tag:
                _raise_template_error(locale, page_key, f"invalid {closing_raw_tag} closing tag")
            closing_raw_tag = None
            raw_open_tag = None
            state = "data"
        elif closing and name in {"script", "style"}:
            _raise_template_error(locale, page_key, f"unexpected closing {name} tag")
        elif not closing and name in {"script", "style"}:
            if self_closing:
                _raise_template_error(locale, page_key, f"self-closing {name} tag")
            raw_open_tag = tag_text
            state = name
        else:
            state = "data"

        if name == "head":
            if closing:
                if not in_head:
                    _raise_template_error(locale, page_key, "unexpected closing head tag")
                in_head = False
            elif not self_closing:
                if in_head:
                    _raise_template_error(locale, page_key, "nested head tag")
                in_head = True
        elif name == "div":
            if closing:
                if not div_stack:
                    _raise_template_error(locale, page_key, "unexpected closing div tag")
                div_stack.pop()
            elif not self_closing:
                div_stack.append(_is_language_menu_tag(tag_text))
        index += 1

    if state != "data":
        _raise_template_error(locale, page_key, f"unterminated {state} context")
    if quote:
        _raise_template_error(locale, page_key, "unterminated attribute value")
    if in_head:
        _raise_template_error(locale, page_key, "unterminated head tag")
    if div_stack:
        _raise_template_error(locale, page_key, "unterminated div tag")
    return contexts


def _validate_placeholder_contexts(template_text, locale, page_key):
    contexts = _scan_template_contexts(template_text, locale, page_key)
    for match in PLACEHOLDER.finditer(template_text):
        kind = match.group("kind")
        key = match.group("key")
        context = contexts[match.start()]
        state = context["state"]

        if state == "attribute":
            if kind != "attr":
                _raise_context_error(
                    locale, page_key, match, "only attr placeholders are allowed in attributes"
                )
            if context["quote"] != '"' or not context["attribute_name"]:
                _raise_context_error(
                    locale,
                    page_key,
                    match,
                    "Attribute placeholder requires double-quoted attribute context",
                )
            continue
        if state in {"tag", "comment"}:
            _raise_context_error(
                locale, page_key, match, f"placeholders cannot appear in {state} context"
            )
        if kind == "attr":
            _raise_context_error(
                locale,
                page_key,
                match,
                "Attribute placeholder requires double-quoted attribute context",
            )
        if kind == "text":
            if state in {"script", "style"}:
                _raise_context_error(
                    locale, page_key, match, "text placeholders cannot appear in script or style"
                )
            continue
        if kind == "json":
            if state != "script" or not _tag_has_attribute(
                context["raw_open_tag"], "type", "application/ld+json"
            ):
                _raise_context_error(
                    locale,
                    page_key,
                    match,
                    "json placeholders require application/ld+json script content",
                )
            continue
        if state in {"script", "style"}:
            _raise_context_error(
                locale, page_key, match, "safe placeholders cannot appear in script or style"
            )
        if key in {"hreflang_links", "__hreflang_links"}:
            if not context["in_head"]:
                _raise_context_error(
                    locale, page_key, match, "hreflang markup must be a direct head block"
                )
            continue
        if key in {"language_menu", "__language_menu"}:
            if not context["in_language_menu"]:
                _raise_context_error(
                    locale, page_key, match, "language menu markup requires langDropdown block"
                )
            continue
        _raise_context_error(locale, page_key, match, "safe block is not approved")


def _language_menu(locale, page_key):
    if set(LANGUAGE_ORDER) != set(SUPPORTED_LOCALES):
        raise ValueError("Language presentation order does not match supported locales")
    links = []
    for option_locale in LANGUAGE_ORDER:
        active = " active" if option_locale == locale else ""
        links.append(
            f'<a href="{_escape_attribute(route_for(option_locale, page_key))}" '
            f'class="lang-option{active}" data-lang="{option_locale}">'
            f'{html.escape(LANGUAGE_NAMES[option_locale], quote=False)}</a>'
        )
    return SafeMarkup("\n          ".join(links))


def _hreflang_links(page_key):
    alternates = alternates_for(page_key)
    order = (*LANGUAGE_ORDER, "x-default")
    return SafeMarkup(
        "\n  ".join(
            f'<link rel="alternate" hreflang="{locale}" href="{_escape_attribute(alternates[locale])}">'
            for locale in order
        )
    )


def _system_values(locale, page_key):
    home = route_for(locale, "home")
    asset_prefix = "./" if locale == "en" else "../"
    values = {
        "__html_lang": locale,
        "__canonical_url": canonical_url(locale, page_key),
        "__schema_page_id": f"{canonical_url(locale, page_key)}#webpage",
        "__home_url": canonical_url(locale, "home"),
        "__hreflang_links": _hreflang_links(page_key),
        "__language_menu": _language_menu(locale, page_key),
        "hreflang_links": _hreflang_links(page_key),
        "language_menu": _language_menu(locale, page_key),
        "__asset_prefix": asset_prefix,
        "__route_home": home,
        "__route_home_principle": f"{home}#principle",
        "__route_home_advantages": f"{home}#advantages",
        "__route_home_samples": f"{home}#samples",
        "__route_about": route_for(locale, "about"),
        "__route_contact": route_for(locale, "contact"),
        "__route_psa": route_for(locale, "psa"),
        "__route_cabinet": route_for(locale, "cabinet"),
        "__route_valve": route_for(locale, "valve"),
        "__route_comparison": route_for(locale, "comparison"),
    }
    return values


def _render_page(locale, page_key, template_text, tracker):
    template_text = _normalize_newlines(template_text)
    _validate_placeholder_contexts(template_text, locale, page_key)
    system_values = _system_values(locale, page_key)

    def replace(match):
        kind = match.group("kind")
        key = match.group("key")
        if key.startswith("__") or (kind == "safe" and key in system_values):
            if key not in system_values:
                raise KeyError(f"Unknown generated value: {key}")
            value = system_values[key]
        else:
            value = tracker.use(key)
        if not isinstance(value, str):
            raise TypeError(f"{locale}/{page_key}: {key} must resolve to a string")
        if kind == "safe":
            if not isinstance(value, SafeMarkup):
                raise ValueError(f"Unsafe markup source: {key}")
            return value
        if kind == "text":
            return html.escape(value, quote=False)
        if kind == "attr":
            return _escape_attribute(value)
        return _json_string(value)

    rendered = _normalize_newlines(PLACEHOLDER.sub(replace, template_text))
    if "{{" in rendered or "}}" in rendered:
        raise ValueError(f"{locale}/{page_key}: unresolved placeholder")
    return rendered


def render_page(locale, page_key, template_text, content):
    if locale not in SUPPORTED_LOCALES:
        raise ValueError(f"Unsupported locale: {locale}")
    if page_key not in PAGE_KEYS:
        raise ValueError(f"Unsupported page: {page_key}")
    if not isinstance(content, dict):
        raise ValueError("Invalid translation root")
    if content.get("locale") != locale:
        raise ValueError(f"Translation locale mismatch: {locale}")
    tracker = ContentTracker(content)
    tracker.validate_non_empty()
    return _render_page(locale, page_key, template_text, tracker)


def template_text(page_key, template_dir=TEMPLATE_DIR):
    return (Path(template_dir) / f"{page_key}.html").read_text(encoding="utf-8")


def build_pages(locales, public_dir=PUBLIC, content_dir=CONTENT_DIR, template_dir=TEMPLATE_DIR):
    locales = parse_locales(locales)
    contents = {locale: load_content(locale, content_dir) for locale in locales}
    templates = {page_key: template_text(page_key, template_dir) for page_key in PAGE_KEYS}
    rendered_pages = {}
    for locale in locales:
        tracker = ContentTracker(contents[locale])
        tracker.validate_required()
        tracker.validate_non_empty()
        for page_key in PAGE_KEYS:
            rendered_pages[(locale, page_key)] = _render_page(
                locale, page_key, templates[page_key], tracker
            )
        tracker.assert_usage()

    public_dir = Path(public_dir)
    for (locale, page_key), rendered in rendered_pages.items():
        destination = output_path(public_dir, locale, page_key)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
    return tuple(rendered_pages)


def build_locale(locale):
    return build_pages((locale,))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", action="append", help="Locale to build (repeatable)")
    args = parser.parse_args()
    try:
        build_pages(parse_locales(args.locale))
    except (FileNotFoundError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
