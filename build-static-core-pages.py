#!/usr/bin/env python3
"""Build the locale-aware About and Contact pages from reviewed content."""

import argparse
import html
import json
import re
from collections import Counter
from html.parser import HTMLParser
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


SENTINEL_PREFIX = "STATICCOREPLACEHOLDER"
SENTINEL = re.compile(rf"{SENTINEL_PREFIX}\d+END")
VOID_ELEMENTS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }
)
SVG_SELF_CLOSING_ELEMENTS = frozenset({"circle", "path", "polyline"})
ALLOWED_SELF_CLOSING_ELEMENTS = VOID_ELEMENTS | SVG_SELF_CLOSING_ELEMENTS


def _skip_space(value, index):
    while index < len(value) and value[index].isspace():
        index += 1
    return index


def _validate_start_tag_syntax(start_tag_text, expected_tag, locale, page_key):
    index = _skip_space(start_tag_text, 1)
    name_start = index
    while index < len(start_tag_text) and not (
        start_tag_text[index].isspace() or start_tag_text[index] in "/>"
    ):
        index += 1
    if start_tag_text[name_start:index].lower() != expected_tag:
        _raise_template_error(locale, page_key, "invalid start tag name")

    while index < len(start_tag_text):
        spaced_index = _skip_space(start_tag_text, index)
        had_space = spaced_index > index
        index = spaced_index
        if index == len(start_tag_text) - 1 and start_tag_text[index] == ">":
            return False
        if start_tag_text.startswith("/>", index) and index == len(start_tag_text) - 2:
            return True
        if index >= len(start_tag_text) or start_tag_text[index] in "/>":
            _raise_template_error(locale, page_key, "stray slash or malformed start tag")
        if not had_space:
            _raise_template_error(locale, page_key, "missing whitespace before attribute")

        name_start = index
        while index < len(start_tag_text) and not (
            start_tag_text[index].isspace()
            or start_tag_text[index] in "=<>/\"'"
        ):
            index += 1
        if index == name_start:
            _raise_template_error(locale, page_key, "invalid attribute syntax")
        after_name = index
        equals_index = _skip_space(start_tag_text, index)
        if (
            equals_index >= len(start_tag_text)
            or start_tag_text[equals_index] != "="
        ):
            index = after_name
            continue

        index = _skip_space(start_tag_text, equals_index + 1)
        if index >= len(start_tag_text):
            _raise_template_error(locale, page_key, "missing attribute value")
        if start_tag_text[index] in {'"', "'"}:
            quote = start_tag_text[index]
            index += 1
            closing_quote = start_tag_text.find(quote, index)
            if closing_quote < 0:
                _raise_template_error(locale, page_key, "unterminated attribute value")
            index = closing_quote + 1
            continue

        value_start = index
        while index < len(start_tag_text) and not (
            start_tag_text[index].isspace() or start_tag_text[index] == ">"
        ):
            if start_tag_text[index] in "\"'<=`":
                _raise_template_error(locale, page_key, "invalid unquoted attribute value")
            index += 1
        if index == value_start:
            _raise_template_error(locale, page_key, "missing attribute value")
    _raise_template_error(locale, page_key, "unterminated start tag")


def _validate_end_tag_syntax(end_tag_text, locale, page_key):
    index = _skip_space(end_tag_text, 2)
    name_start = index
    while index < len(end_tag_text) and not (
        end_tag_text[index].isspace() or end_tag_text[index] in "/>"
    ):
        index += 1
    if index == name_start:
        _raise_template_error(locale, page_key, "missing end tag name")
    index = _skip_space(end_tag_text, index)
    if index != len(end_tag_text) - 1 or end_tag_text[index] != ">":
        _raise_template_error(locale, page_key, "malformed end tag")


def _sentinel_quote(start_tag_text, sentinel):
    quote = None
    index = 0
    while index < len(start_tag_text):
        if start_tag_text.startswith(sentinel, index):
            return quote
        character = start_tag_text[index]
        if quote:
            if character == quote:
                quote = None
        elif character in {'"', "'"}:
            quote = character
        index += 1
    return None


class TemplateContextValidator(HTMLParser):
    def __init__(self, locale, page_key, placeholders):
        super().__init__(convert_charrefs=False)
        self.locale = locale
        self.page_key = page_key
        self.placeholders = placeholders
        self.seen = set()
        self.stack = []

    def _attributes(self, attrs):
        values = {}
        for name, value in attrs:
            if name in values:
                _raise_template_error(
                    self.locale, self.page_key, f"Duplicate HTML attribute: {name}"
                )
            values[name] = value
        return values

    def _matches(self, value):
        return SENTINEL.findall(value or "")

    def _match(self, sentinel):
        if sentinel not in self.placeholders or sentinel in self.seen:
            _raise_template_error(self.locale, self.page_key, "ambiguous placeholder sentinel")
        self.seen.add(sentinel)
        return self.placeholders[sentinel]

    def _validate_attribute_placeholder(self, sentinel, start_tag_text):
        match = self._match(sentinel)
        if match.group("kind") != "attr":
            _raise_context_error(
                self.locale,
                self.page_key,
                match,
                "only attr placeholders are allowed in attributes",
            )
        if _sentinel_quote(start_tag_text, sentinel) != '"':
            _raise_context_error(
                self.locale,
                self.page_key,
                match,
                "Attribute placeholder requires double-quoted attribute context",
            )

    def _validate_data_placeholder(self, sentinel):
        match = self._match(sentinel)
        kind = match.group("kind")
        key = match.group("key")
        parent = self.stack[-1] if self.stack else None
        parent_tag = parent["tag"] if parent else None

        if kind == "attr":
            _raise_context_error(
                self.locale,
                self.page_key,
                match,
                "Attribute placeholder requires double-quoted attribute context",
            )
        if kind == "text":
            if parent_tag in {"script", "style"}:
                _raise_context_error(
                    self.locale,
                    self.page_key,
                    match,
                    "text placeholders cannot appear in script or style",
                )
            return
        if kind == "json":
            if not (
                parent_tag == "script"
                and parent["attrs"].get("type") == "application/ld+json"
            ):
                _raise_context_error(
                    self.locale,
                    self.page_key,
                    match,
                    "json placeholders require application/ld+json script content",
                )
            return
        if parent_tag in {"script", "style"}:
            _raise_context_error(
                self.locale,
                self.page_key,
                match,
                "safe placeholders cannot appear in script or style",
            )
        if key in {"hreflang_links", "__hreflang_links"} and parent_tag == "head":
            return
        if key in {"language_menu", "__language_menu"} and parent_tag == "div":
            classes = (parent["attrs"].get("class") or "").split()
            if "lang-dropdown" in classes and parent["attrs"].get("id") == "langDropdown":
                return
        _raise_context_error(self.locale, self.page_key, match, "safe block is not approved")

    def _start(self, tag, attrs, self_closing=False):
        values = self._attributes(attrs)
        start_tag_text = self.get_starttag_text() or ""
        raw_self_closing = _validate_start_tag_syntax(
            start_tag_text, tag, self.locale, self.page_key
        )
        if raw_self_closing != self_closing:
            _raise_template_error(self.locale, self.page_key, "ambiguous self-closing tag")
        for _, value in attrs:
            for sentinel in self._matches(value):
                self._validate_attribute_placeholder(sentinel, start_tag_text)
        if self_closing:
            if tag not in ALLOWED_SELF_CLOSING_ELEMENTS:
                _raise_template_error(
                    self.locale, self.page_key, f"disallowed self-closing element: {tag}"
                )
            return
        if tag not in VOID_ELEMENTS:
            self.stack.append({"tag": tag, "attrs": values})

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, self_closing=True)

    def parse_endtag(self, index):
        end = self.rawdata.find(">", index + 2)
        if end < 0:
            return -1
        _validate_end_tag_syntax(
            self.rawdata[index : end + 1], self.locale, self.page_key
        )
        return super().parse_endtag(index)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]["tag"] != tag:
            expected = self.stack[-1]["tag"] if self.stack else "none"
            _raise_template_error(
                self.locale,
                self.page_key,
                f"unexpected closing element: {tag}; expected {expected}",
            )
        self.stack.pop()

    def handle_data(self, data):
        for sentinel in self._matches(data):
            self._validate_data_placeholder(sentinel)

    def handle_comment(self, data):
        for sentinel in self._matches(data):
            match = self._match(sentinel)
            _raise_context_error(
                self.locale, self.page_key, match, "placeholders cannot appear in comments"
            )

    def handle_decl(self, decl):
        if self._matches(decl):
            _raise_template_error(self.locale, self.page_key, "placeholder in declaration")

    def handle_pi(self, data):
        if self._matches(data):
            _raise_template_error(self.locale, self.page_key, "placeholder in instruction")

    def unknown_decl(self, data):
        if self._matches(data):
            _raise_template_error(self.locale, self.page_key, "placeholder in declaration")

    def finish(self):
        if self.rawdata:
            _raise_template_error(self.locale, self.page_key, "unterminated HTML construct")
        self.close()
        if self.stack:
            _raise_template_error(
                self.locale,
                self.page_key,
                "unclosed HTML elements: " + ", ".join(frame["tag"] for frame in self.stack),
            )
        missing = set(self.placeholders) - self.seen
        if missing:
            _raise_template_error(self.locale, self.page_key, "placeholder crossed HTML context")


def _validate_placeholder_contexts(template_text, locale, page_key):
    if SENTINEL_PREFIX in template_text:
        _raise_template_error(locale, page_key, "reserved placeholder sentinel in template")
    placeholders = {}

    def replace(match):
        sentinel = f"{SENTINEL_PREFIX}{len(placeholders)}END"
        placeholders[sentinel] = match
        return sentinel

    validation_text = PLACEHOLDER.sub(replace, template_text)
    validator = TemplateContextValidator(locale, page_key, placeholders)
    validator.feed(validation_text)
    validator.finish()


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
