#!/usr/bin/env python3
"""Build the locale-aware About and Contact pages from reviewed content."""

import argparse
import html
import json
import re
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

# These plan-level descriptors are retained for downstream locale work. The approved
# English pages currently use more specific SEO copy, so changing output to consume
# them would violate the byte-for-byte migration contract.
REUSABLE_CONTENT_PATHS = frozenset(
    {"about.title", "about.description", "contact.description"}
)

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
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            paths.update(leaf_paths(child, child_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            paths.update(leaf_paths(child, f"{prefix}.{index}"))
    else:
        paths.add(prefix)
    return paths


class ContentTracker:
    def __init__(self, content):
        self.content = content
        self.used = {"locale"}

    def use(self, path):
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
        self.used.update(leaf_paths(value, path))
        return value

    def assert_all_used(self):
        unused = sorted(
            leaf_paths(self.content) - self.used - REUSABLE_CONTENT_PATHS
        )
        if unused:
            raise ValueError("Unused content keys: " + ", ".join(unused))


def load_content(locale, content_dir=CONTENT_DIR):
    path = Path(content_dir) / f"{locale}.json"
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Missing translation file: {path.name}") from exc
    try:
        content = json.loads(raw)
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

    rendered = PLACEHOLDER.sub(replace, template_text)
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
    return _render_page(locale, page_key, template_text, ContentTracker(content))


def template_text(page_key, template_dir=TEMPLATE_DIR):
    return (Path(template_dir) / f"{page_key}.html").read_text(encoding="utf-8")


def build_pages(locales, public_dir=PUBLIC, content_dir=CONTENT_DIR, template_dir=TEMPLATE_DIR):
    locales = parse_locales(locales)
    contents = {locale: load_content(locale, content_dir) for locale in locales}
    templates = {page_key: template_text(page_key, template_dir) for page_key in PAGE_KEYS}
    rendered_pages = {}
    for locale in locales:
        tracker = ContentTracker(contents[locale])
        for page_key in PAGE_KEYS:
            rendered_pages[(locale, page_key)] = _render_page(
                locale, page_key, templates[page_key], tracker
            )
        tracker.assert_all_used()

    public_dir = Path(public_dir)
    for (locale, page_key), rendered in rendered_pages.items():
        destination = output_path(public_dir, locale, page_key)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
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
