#!/usr/bin/env python3
"""Build reviewed product pages from strict templates and locale JSON content."""

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from site_locales import SUPPORTED_LOCALES, alternates_for, canonical_url, output_path, route_for


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
TEMPLATE_DIR = PUBLIC / "product-templates"
CONTENT_DIR = PUBLIC / "i18n" / "products"
DOMAIN = canonical_url("en", "home").rstrip("/")

PAGES = (
    ("psa", "psa-nitrogen-generation-system", "psa-nitrogen-system", "Product"),
    ("cabinet", "integrated-gas-mixing-cabinet", "integrated-mixing-cabinet", "Product"),
    ("valve", "mspv2-4000-proportional-valve", "mspv2-4000", "Product"),
    ("comparison", "mixed-gas-control-comparison", "need-recommendation", "CollectionPage"),
)

PLACEHOLDER = re.compile(r"\{\{([a-zA-Z0-9_.-]+)\}\}")
TECHNICAL_TOKEN = re.compile(
    r"https?://[^\s\"'<>]+"
    r"|(?<![A-Za-z0-9])NPN/PNP(?![A-Za-z0-9])"
    r"|(?<![A-Za-z0-9_<])/(?:[A-Za-z0-9._~!$&'()*+,;=:@%-]+/?)+"
    r"|#[A-Za-z][A-Za-z0-9_-]*"
    r"|(?<![A-Za-z0-9_])(?=[A-Za-z0-9_/-]*[A-Za-z])(?=[A-Za-z0-9_/-]*\d)"
    r"[A-Za-z][A-Za-z0-9_/-]*(?![A-Za-z0-9_])"
    r"|(?<![A-Za-z0-9])(?:N[₂2]\s*/\s*O[₂2]|N[₂2]|O[₂2])(?![A-Za-z0-9])"
    r"|(?<![A-Za-z0-9_])\d+(?:\.\d+)?(?:\s*[–—-]\s*\d+(?:\.\d+)?)?"
    r"(?![A-Za-z0-9_])"
    r"|(?<![A-Za-z0-9])(?:Nm³/h|m³/h|L/min|MPa|kPa|bar|kg|mm|ms|kW|V|ft|m)"
    r"(?![A-Za-z0-9])|%"
    r"|[×≤≥±]"
)

HREF_ATTRIBUTE = re.compile(
    r"(?P<prefix>(?<![-\w])href\s*=\s*)"
    r"(?:\"(?P<double>[^\"]*)\"|'(?P<single>[^']*)'|(?P<bare>[^\s>]+))",
    re.IGNORECASE,
)

ALLOWED_BR_CONTENT_PATHS = {
    "pages.cabinet.silhouette_label",
    "pages.comparison.hero_cabinet_title",
    "pages.comparison.hero_valve_title",
}

IMMUTABLE_CONTENT_FIELDS = {
    "anchor",
    "href",
    "id",
    "key",
    "media_index",
    "model",
    "og_image",
    "src",
    "url",
}

LANGUAGE_NAMES = {
    "en": "English",
    "zh": "中文",
    "es": "Español",
    "pt": "Português",
    "ja": "日本語",
    "ko": "한국어",
    "pl": "Polski",
}


class SafeMarkup(str):
    pass


def content_path(locale):
    return CONTENT_DIR / f"{locale}.json"


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
        self.used = set()

    def use(self, path):
        value = self.peek(path)
        self.used.update(leaf_paths(value, path))
        return value

    def peek(self, path):
        value = self.content
        for part in path.split("."):
            if isinstance(value, list):
                value = value[int(part)]
            else:
                if part not in value:
                    raise KeyError(f"Missing content key: {path}")
                value = value[part]
        return value

    def assert_all_used(self):
        unused = sorted(leaf_paths(self.content) - self.used)
        if unused:
            raise ValueError("Unused content keys: " + ", ".join(unused))


def render_list(items, css_class="engineering-list"):
    return SafeMarkup('<ul class="{}">{}</ul>'.format(
        html.escape(css_class, quote=True),
        "".join(f"<li>{html.escape(item, quote=True)}</li>" for item in items),
    ))


def render_specs(items):
    cards = []
    for item in items:
        note = (
            f'<span class="spec-note">{html.escape(item["note"], quote=True)}</span>'
            if item.get("note")
            else ""
        )
        cards.append(
            '<div class="spec-card">'
            f'<span class="spec-label">{html.escape(item["label"], quote=True)}</span>'
            f'<strong>{html.escape(item["value"], quote=True)}</strong>{note}'
            "</div>"
        )
    return SafeMarkup('<div class="spec-grid">' + "".join(cards) + "</div>")


def render_cards(items, css_class="engineering-card-grid"):
    cards = []
    for item in items:
        eyebrow = (
            f'<span class="card-kicker">{html.escape(item["kicker"], quote=True)}</span>'
            if item.get("kicker")
            else ""
        )
        meta = (
            f'<p class="card-meta">{html.escape(item["meta"], quote=True)}</p>'
            if item.get("meta")
            else ""
        )
        cards.append(
            '<article class="engineering-card">'
            f"{eyebrow}<h3>{html.escape(item['title'], quote=True)}</h3>"
            f"<p>{html.escape(item['text'], quote=True)}</p>{meta}"
            "</article>"
        )
    return SafeMarkup(
        f'<div class="{html.escape(css_class, quote=True)}">' + "".join(cards) + "</div>"
    )


def render_faq(items):
    return SafeMarkup('<div class="product-faq">' + "".join(
        '<details class="faq-item">'
        f'<summary>{html.escape(item["question"], quote=True)}</summary>'
        f'<div class="faq-answer"><p>{html.escape(item["answer"], quote=True)}</p></div>'
        "</details>"
        for item in items
    ) + "</div>")


def render_comparison_rows(items):
    return SafeMarkup("".join(
        "<tr>"
        f'<th scope="row">{html.escape(item["factor"], quote=True)}</th>'
        f'<td>{html.escape(item["cabinet"], quote=True)}</td>'
        f'<td>{html.escape(item["valve"], quote=True)}</td>'
        "</tr>"
        for item in items
    ))


def render_content_value(value, path, locale):
    if path not in ALLOWED_BR_CONTENT_PATHS:
        return value
    parts = value.split("<br>")
    if any("<" in part or ">" in part for part in parts):
        raise ValueError(f"Unsafe HTML markup: {locale}: {path}")
    return SafeMarkup("<br>".join(html.escape(part, quote=True) for part in parts))


def render_template(template, resolver, source_name):
    def replace(match):
        key = match.group(1)
        value = resolver(key)
        if not isinstance(value, str):
            raise TypeError(f"{source_name}: placeholder {key} must resolve to a string")
        if isinstance(value, SafeMarkup):
            return value
        return html.escape(value, quote=True)

    rendered = PLACEHOLDER.sub(replace, template)
    if "{{" in rendered or "}}" in rendered:
        raise ValueError(f"{source_name}: unresolved template markers")
    return rendered


def build_schema(
    page,
    page_type,
    canonical,
    image_url,
    faq_items,
    product_id,
    locale,
    breadcrumb_home,
    breadcrumb_products,
):
    graph = [
        {
            "@type": page_type,
            "@id": f"{canonical}#webpage",
            "url": canonical,
            "name": page["title"],
            "description": page["description"],
            "inLanguage": locale,
            "image": image_url,
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": breadcrumb_home,
                    "item": canonical_url(locale, "home"),
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": breadcrumb_products,
                    "item": f'{canonical_url(locale, "home")}#products',
                },
                {"@type": "ListItem", "position": 3, "name": page["short_name"], "item": canonical},
            ],
        },
        {
            "@type": "FAQPage",
            "inLanguage": locale,
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
                }
                for item in faq_items
            ],
        },
    ]
    if page_type == "Product":
        graph[0].update(
            {
                "name": page["product_name"],
                "category": page["category"],
                "model": page.get("model", product_id),
            }
        )
    if product_id == "mspv2-4000":
        graph.append(
            {
                "@type": "VideoObject",
                "name": page["video_name"],
                "description": page["video_description"],
                "thumbnailUrl": f"{DOMAIN}/images/products/mspv2-4000/mspv2-4000-angle-02.png",
                "contentUrl": f"{DOMAIN}/images/products/mspv2-4000/mspv2-4000-360.webm",
                "uploadDate": "2026-08-25",
                "inLanguage": locale,
            }
        )
    serialized = json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        indent=2,
    )
    return SafeMarkup(serialized.replace("<", "\\u003c"))


def render_hreflangs(alternates):
    return SafeMarkup("\n".join(
        f'  <link rel="alternate" hreflang="{locale}" href="{url}">'
        for locale, url in alternates.items()
    ))


def render_language_menu(page_key, current_locale):
    return SafeMarkup("\n".join(
        f'          <a href="{route_for(locale, page_key)}" '
        f'class="lang-option{" active" if locale == current_locale else ""}" '
        f'data-lang="{locale}">{LANGUAGE_NAMES[locale]}</a>'
        for locale in SUPPORTED_LOCALES
    ))


SHELL = """<!DOCTYPE html>
<html lang="{{locale.code}}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{page.description}}">
  <title>{{page.title}}</title>
  <link rel="canonical" href="{{route.canonical}}">
{{route.hreflangs}}
  <meta property="og:title" content="{{page.title}}">
  <meta property="og:description" content="{{page.description}}">
  <meta property="og:image" content="{{route.og_image}}">
  <meta property="og:url" content="{{route.canonical}}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="stylesheet" href="/styles.css?v=20260901-product-pages">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
  <script type="application/ld+json">
{{schema.graph}}
  </script>
</head>
<body class="product-page">
  <a href="#main" class="skip-link">{{shared.skip_to_content}}</a>
  <header class="header product-header">
    <div class="container header-inner">
      <a href="{{route.home}}" class="logo" aria-label="{{shared.home_aria}}">
        <picture><source srcset="/images/logo.webp" type="image/webp"><img src="/images/logo.png" alt="{{shared.logo_alt}}"></picture>
        <span class="logo-text"><span class="logo-brand">{{shared.brand}}</span><span class="logo-tagline">{{shared.tagline}}</span></span>
      </a>
      <nav class="nav product-nav" id="nav" role="navigation" aria-label="{{shared.nav_aria}}">
        <div class="product-nav-group">
          <button class="product-menu-button" id="productMenuButton" type="button" aria-expanded="false" aria-controls="productMenu">{{shared.nav_products}} <span aria-hidden="true">⌄</span></button>
          <div class="product-menu" id="productMenu">
            <div><span class="product-menu-label">{{shared.nav_nitrogen_supply}}</span><a href="{{route.psa}}">{{shared.nav_psa}}</a></div>
            <div><span class="product-menu-label">{{shared.nav_mixed_control}}</span><a href="{{route.cabinet}}">{{shared.nav_cabinet}}</a><a href="{{route.valve}}">{{shared.nav_valve}}</a><a href="{{route.comparison}}">{{shared.nav_compare}}</a></div>
          </div>
        </div>
        <a href="{{route.home}}#applications">{{shared.nav_applications}}</a>
        <a href="{{route.home}}#samples">{{shared.nav_results}}</a>
        <a href="/blog/">{{shared.nav_resources}}</a>
        <a href="{{route.about}}">{{shared.nav_about}}</a>
        <a href="{{route.contact}}" class="nav-cta">{{shared.nav_request}}</a>
      </nav>
      <div class="lang-switch" id="langSwitch">
        <button class="lang-btn" id="langBtn" type="button"><span class="lang-current">{{locale.label}}</span><span class="lang-sep">|</span><span class="lang-arrow">▼</span></button>
        <div class="lang-dropdown" id="langDropdown">
{{locale.menu}}
        </div>
      </div>
      <button class="mobile-toggle" id="mobileToggle" aria-label="{{shared.mobile_aria}}">☰</button>
    </div>
  </header>
  <main id="main">
{{page.body}}
  </main>
  <footer class="footer product-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand"><span class="logo-brand">{{shared.brand}}</span><p>{{shared.footer_intro}}</p></div>
        <div class="footer-links"><h4>{{shared.footer_products}}</h4><ul><li><a href="{{route.psa}}">{{shared.nav_psa}}</a></li><li><a href="{{route.cabinet}}">{{shared.nav_cabinet}}</a></li><li><a href="{{route.valve}}">{{shared.nav_valve}}</a></li><li><a href="{{route.comparison}}">{{shared.nav_compare}}</a></li></ul></div>
        <div class="footer-links"><h4>{{shared.footer_contact}}</h4><ul><li><a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a></li><li><a href="{{route.contact}}">{{shared.nav_request}}</a></li><li><a href="/privacy.html">{{shared.footer_privacy}}</a></li></ul></div>
      </div>
      <div class="footer-bottom"><p>© 2026 Jinan Euchio Machinery Co., Ltd.</p></div>
    </div>
  </footer>
  <script src="/script.min.js?v=20260901-1"></script>
</body>
</html>
"""


def load_content(locale, content_dir):
    path = content_path(locale) if content_dir == CONTENT_DIR else content_dir / f"{locale}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Missing translation file: {path.name}")
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid translation JSON: {path.name}") from error
    if not isinstance(content, dict):
        raise ValueError(f"Invalid translation root: {path.name}")
    if content.get("locale") != locale:
        raise ValueError(f"Translation locale mismatch: {path.name}")
    return content


def technical_tokens(value):
    return tuple(match.group(0) for match in TECHNICAL_TOKEN.finditer(value))


def immutable_content_path(path):
    field = path.rsplit(".", 1)[-1]
    return field in IMMUTABLE_CONTENT_FIELDS or field.endswith(
        ("_anchor", "_href", "_id", "_path", "_src", "_url")
    )


def explicit_technical_value_path(path):
    parts = path.split(".")
    field = parts[-1]
    collections = {"cases", "configurations", "specs"}
    if field == "value" and collections.intersection(parts[:-1]):
        return True
    return field.endswith("_value") and field.startswith(("case_", "config_"))


def validate_technical_content(content, english_content, locale, path=""):
    if isinstance(english_content, dict):
        if not isinstance(content, dict):
            raise ValueError(f"Technical structure mismatch: {locale}: {path or '<root>'}")
        missing = english_content.keys() - content.keys()
        if missing:
            missing_path = f"{path}.{sorted(missing)[0]}" if path else sorted(missing)[0]
            raise KeyError(f"Missing content key: {missing_path} (locale {locale})")
        if content.keys() - english_content.keys():
            raise ValueError(f"Technical structure mismatch: {locale}: {path or '<root>'}")
        for key, english_value in english_content.items():
            child_path = f"{path}.{key}" if path else key
            validate_technical_content(content[key], english_value, locale, child_path)
        return

    if isinstance(english_content, list):
        if not isinstance(content, list) or len(content) != len(english_content):
            raise ValueError(f"Technical structure mismatch: {locale}: {path}")
        for index, english_value in enumerate(english_content):
            validate_technical_content(content[index], english_value, locale, f"{path}.{index}")
        return

    if type(content) is not type(english_content):
        raise ValueError(f"Technical structure mismatch: {locale}: {path}")

    if path == "locale":
        return
    if isinstance(english_content, str):
        if (immutable_content_path(path) or explicit_technical_value_path(path)) and content != english_content:
            raise ValueError(f"Technical content mismatch: {locale}: {path}")
        if technical_tokens(content) != technical_tokens(english_content):
            raise ValueError(f"Technical token mismatch: {locale}: {path}")
    elif content != english_content:
        raise ValueError(f"Technical content mismatch: {locale}: {path}")


def validate_comparison_row_keys(content, locale):
    rows = content["pages"]["comparison"]["comparison_rows"]
    seen = set()
    for index, row in enumerate(rows):
        path = f"pages.comparison.comparison_rows.{index}.key"
        key = row.get("key")
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"Invalid stable key: {locale}: {path}")
        if key in seen:
            raise ValueError(f"Duplicate stable key: {locale}: {path}")
        seen.add(key)


def href_value(match):
    return match.group("double") or match.group("single") or match.group("bare")


def same_site_product_url(value, english_routes):
    decoded = html.unescape(value)
    parsed = urlsplit(decoded)
    if parsed.netloc:
        if parsed.netloc.lower() != "gasmixtech.com" or parsed.scheme not in (
            "",
            "http",
            "https",
        ):
            return None
    elif parsed.scheme or not decoded.startswith("/"):
        return None
    if parsed.path not in english_routes:
        return None
    return parsed


def localize_fragment_routes(fragment, route, locale):
    english_routes = {
        route_for("en", page_key): route[page_key]
        for page_key in ("psa", "cabinet", "valve", "comparison")
    }

    def rewrite(match):
        value = href_value(match)
        parsed = same_site_product_url(value, english_routes)
        if parsed is None:
            return match.group(0)
        if urlsplit(value).path != parsed.path:
            return match.group(0)
        rewritten = parsed._replace(path=english_routes[parsed.path]).geturl()
        if match.group("double") is not None:
            return f'{match.group("prefix")}"{html.escape(rewritten, quote=True)}"'
        if match.group("single") is not None:
            return f"{match.group('prefix')}'{html.escape(rewritten, quote=True)}'"
        return f"{match.group('prefix')}{html.escape(rewritten, quote=True)}"

    fragment = HREF_ATTRIBUTE.sub(rewrite, fragment)

    if locale != "en":
        for match in HREF_ATTRIBUTE.finditer(fragment):
            parsed = same_site_product_url(href_value(match), english_routes)
            if parsed is not None:
                raise ValueError(f"Unlocalized product route: {locale}: {parsed.path}")
    return fragment


def render_locale(locale, content, english_content, public_dir, template_dir):
    if locale != "en":
        validate_technical_content(content, english_content, locale)
    tracker = ContentTracker(content)
    tracker.use("locale")

    rendered_pages = []
    destinations = set()
    for page_key, slug, product_id, page_type in PAGES:
        template_path = template_dir / f"{slug}.html"
        if not template_path.is_file():
            raise FileNotFoundError(template_path)
        page_path = f"pages.{page_key}"
        page = tracker.peek(page_path)
        destination = output_path(public_dir, locale, page_key)
        if destination in destinations:
            raise ValueError(f"Duplicate output path: {destination}")
        destinations.add(destination)

        block_renderers = {
            "specs": lambda: render_specs(tracker.use(f"{page_path}.specs")),
            "cards": lambda: render_cards(tracker.use(f"{page_path}.cards")),
            "secondary_cards": lambda: render_cards(tracker.use(f"{page_path}.secondary_cards")),
            "checklist": lambda: render_list(tracker.use(f"{page_path}.checklist")),
            "faq": lambda: render_faq(tracker.use(f"{page_path}.faq")),
            "comparison_rows": lambda: render_comparison_rows(tracker.use(f"{page_path}.comparison_rows")),
        }
        image_path = tracker.use(f"{page_path}.og_image")
        image_url = f"{DOMAIN}{image_path}"
        schema_fields = ["title", "description", "short_name", "faq"]
        if page_type == "Product":
            schema_fields.extend(["product_name", "category", "model"])
        if product_id == "mspv2-4000":
            schema_fields.extend(["video_name", "video_description"])
        for field in schema_fields:
            tracker.use(f"{page_path}.{field}")
        route = {
            "canonical": canonical_url(locale, page_key),
            "canonical_path": route_for(locale, page_key),
            "contact": f'{route_for(locale, "contact")}?product={product_id}',
            "home": route_for(locale, "home"),
            "about": route_for(locale, "about"),
            "psa": route_for(locale, "psa"),
            "cabinet": route_for(locale, "cabinet"),
            "valve": route_for(locale, "valve"),
            "comparison": route_for(locale, "comparison"),
            "hreflangs": render_hreflangs(alternates_for(page_key)),
            "og_image": image_url,
        }
        schema = build_schema(
            page,
            page_type,
            route["canonical"],
            image_url,
            page["faq"],
            product_id,
            locale,
            tracker.use("shared.home_aria"),
            tracker.use("shared.nav_products"),
        )

        def translated(path):
            return render_content_value(tracker.use(path), path, locale)

        def resolve_fragment(key):
            if key.startswith("page."):
                path = f"{page_path}.{key[5:]}"
                return translated(path)
            if key.startswith("shared."):
                return translated(key)
            if key.startswith("blocks."):
                block_name = key[7:]
                if block_name not in block_renderers:
                    raise KeyError(f"Unsupported content block: {block_name}")
                return block_renderers[block_name]()
            if key.startswith("route."):
                return route[key[6:]]
            raise KeyError(f"Unsupported template key: {key}")

        fragment = render_template(
            template_path.read_text(encoding="utf-8"),
            resolve_fragment,
            f"{locale} {template_path.name}",
        )
        fragment = localize_fragment_routes(fragment, route, locale)

        shell_values = {
            "page.body": SafeMarkup(fragment),
            "schema.graph": schema,
            "locale.code": locale,
            "locale.label": locale.upper(),
            "locale.menu": render_language_menu(page_key, locale),
        }

        def resolve_shell(key):
            if key in shell_values:
                return shell_values[key]
            if key.startswith("page."):
                path = f"{page_path}.{key[5:]}"
                return translated(path)
            if key.startswith("shared."):
                return translated(key)
            if key.startswith("route."):
                return route[key[6:]]
            raise KeyError(f"Unsupported shell key: {key}")

        rendered = render_template(SHELL, resolve_shell, f"{locale} product shell")
        rendered_pages.append((destination, rendered))

    tracker.assert_all_used()
    return rendered_pages


def build_pages(locales, public_dir=PUBLIC, content_dir=CONTENT_DIR, template_dir=TEMPLATE_DIR):
    locales = parse_locales(locales)
    english_content = load_content("en", content_dir)
    validate_comparison_row_keys(english_content, "en")
    pending = []
    for locale in locales:
        content = english_content if locale == "en" else load_content(locale, content_dir)
        pending.extend(
            render_locale(locale, content, english_content, public_dir, template_dir)
        )

    for destination, rendered in pending:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
    return tuple(destination for destination, _ in pending)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locale", action="append", dest="locales")
    args = parser.parse_args(argv)
    try:
        locales = parse_locales(args.locales)
    except ValueError as error:
        parser.error(str(error))
    for destination in build_pages(locales):
        try:
            display_path = destination.relative_to(ROOT)
        except ValueError:
            display_path = destination
        print(f"built: {display_path}")


if __name__ == "__main__":
    main()
