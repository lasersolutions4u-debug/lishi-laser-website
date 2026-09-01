#!/usr/bin/env python3
"""Build reviewed English product pages from strict templates and JSON content."""

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
TEMPLATE_DIR = PUBLIC / "product-templates"
CONTENT_PATH = PUBLIC / "i18n" / "products" / "en.json"
OUTPUT_DIR = PUBLIC / "products"
DOMAIN = "https://gasmixtech.com"

PAGES = (
    ("psa", "psa-nitrogen-generation-system", "psa-nitrogen-system", "Product"),
    ("cabinet", "integrated-gas-mixing-cabinet", "integrated-mixing-cabinet", "Product"),
    ("valve", "mspv2-4000-proportional-valve", "mspv2-4000", "Product"),
    ("comparison", "mixed-gas-control-comparison", "need-recommendation", "CollectionPage"),
)

PLACEHOLDER = re.compile(r"\{\{([a-zA-Z0-9_.-]+)\}\}")


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
    return '<ul class="{}">{}</ul>'.format(
        css_class,
        "".join(f"<li>{item}</li>" for item in items),
    )


def render_specs(items):
    cards = []
    for item in items:
        note = f'<span class="spec-note">{item["note"]}</span>' if item.get("note") else ""
        cards.append(
            '<div class="spec-card">'
            f'<span class="spec-label">{item["label"]}</span>'
            f'<strong>{item["value"]}</strong>{note}'
            "</div>"
        )
    return '<div class="spec-grid">' + "".join(cards) + "</div>"


def render_cards(items, css_class="engineering-card-grid"):
    cards = []
    for item in items:
        eyebrow = f'<span class="card-kicker">{item["kicker"]}</span>' if item.get("kicker") else ""
        meta = f'<p class="card-meta">{item["meta"]}</p>' if item.get("meta") else ""
        cards.append(
            '<article class="engineering-card">'
            f"{eyebrow}<h3>{item['title']}</h3><p>{item['text']}</p>{meta}"
            "</article>"
        )
    return f'<div class="{css_class}">' + "".join(cards) + "</div>"


def render_faq(items):
    return '<div class="product-faq">' + "".join(
        '<details class="faq-item">'
        f'<summary>{item["question"]}</summary>'
        f'<div class="faq-answer"><p>{item["answer"]}</p></div>'
        "</details>"
        for item in items
    ) + "</div>"


def render_comparison_rows(items):
    return "".join(
        "<tr>"
        f'<th scope="row">{item["factor"]}</th>'
        f'<td>{item["cabinet"]}</td>'
        f'<td>{item["valve"]}</td>'
        "</tr>"
        for item in items
    )


def render_template(template, resolver, source_name):
    def replace(match):
        key = match.group(1)
        value = resolver(key)
        if not isinstance(value, str):
            raise TypeError(f"{source_name}: placeholder {key} must resolve to a string")
        return value

    rendered = PLACEHOLDER.sub(replace, template)
    unresolved = PLACEHOLDER.findall(rendered)
    if unresolved:
        raise ValueError(f"{source_name}: unresolved placeholders: {unresolved}")
    return rendered


def build_schema(page, page_type, canonical, image_url, faq_items, product_id):
    graph = [
        {
            "@type": page_type,
            "@id": f"{canonical}#webpage",
            "url": canonical,
            "name": page["title"],
            "description": page["description"],
            "inLanguage": "en",
            "image": image_url,
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
                {"@type": "ListItem", "position": 2, "name": "Products", "item": f"{DOMAIN}/#products"},
                {"@type": "ListItem", "position": 3, "name": page["short_name"], "item": canonical},
            ],
        },
        {
            "@type": "FAQPage",
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
                "inLanguage": "en",
            }
        )
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{page.description}}">
  <title>{{page.title}}</title>
  <link rel="canonical" href="{{route.canonical}}">
  <link rel="alternate" hreflang="en" href="{{route.canonical}}">
  <link rel="alternate" hreflang="x-default" href="{{route.canonical}}">
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
      <a href="/" class="logo" aria-label="{{shared.home_aria}}">
        <picture><source srcset="/images/logo.webp" type="image/webp"><img src="/images/logo.png" alt="{{shared.logo_alt}}"></picture>
        <span class="logo-text"><span class="logo-brand">{{shared.brand}}</span><span class="logo-tagline">{{shared.tagline}}</span></span>
      </a>
      <nav class="nav product-nav" id="nav" role="navigation" aria-label="{{shared.nav_aria}}">
        <div class="product-nav-group">
          <button class="product-menu-button" id="productMenuButton" type="button" aria-expanded="false" aria-controls="productMenu">{{shared.nav_products}} <span aria-hidden="true">⌄</span></button>
          <div class="product-menu" id="productMenu">
            <div><span class="product-menu-label">{{shared.nav_nitrogen_supply}}</span><a href="/products/psa-nitrogen-generation-system">{{shared.nav_psa}}</a></div>
            <div><span class="product-menu-label">{{shared.nav_mixed_control}}</span><a href="/products/integrated-gas-mixing-cabinet">{{shared.nav_cabinet}}</a><a href="/products/mspv2-4000-proportional-valve">{{shared.nav_valve}}</a><a href="/products/mixed-gas-control-comparison">{{shared.nav_compare}}</a></div>
          </div>
        </div>
        <a href="/#applications">{{shared.nav_applications}}</a>
        <a href="/#samples">{{shared.nav_results}}</a>
        <a href="/blog/">{{shared.nav_resources}}</a>
        <a href="/about">{{shared.nav_about}}</a>
        <a href="{{route.contact}}" class="nav-cta">{{shared.nav_request}}</a>
      </nav>
      <div class="lang-switch" id="langSwitch">
        <button class="lang-btn" id="langBtn" type="button"><span class="lang-current">EN</span><span class="lang-sep">|</span><span class="lang-arrow">▼</span></button>
        <div class="lang-dropdown" id="langDropdown">
          <a href="{{route.canonical_path}}" class="lang-option active" data-lang="en">English</a>
          <a href="{{route.canonical_path}}" class="lang-option" data-lang="zh">中文</a>
          <a href="{{route.canonical_path}}" class="lang-option" data-lang="es">Español</a>
          <a href="{{route.canonical_path}}" class="lang-option" data-lang="ko">한국어</a>
          <a href="{{route.canonical_path}}" class="lang-option" data-lang="ja">日本語</a>
          <a href="{{route.canonical_path}}" class="lang-option" data-lang="pt">Português</a>
          <a href="{{route.canonical_path}}" class="lang-option" data-lang="pl">Polski</a>
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
        <div class="footer-links"><h4>{{shared.footer_products}}</h4><ul><li><a href="/products/psa-nitrogen-generation-system">{{shared.nav_psa}}</a></li><li><a href="/products/integrated-gas-mixing-cabinet">{{shared.nav_cabinet}}</a></li><li><a href="/products/mspv2-4000-proportional-valve">{{shared.nav_valve}}</a></li><li><a href="/products/mixed-gas-control-comparison">{{shared.nav_compare}}</a></li></ul></div>
        <div class="footer-links"><h4>{{shared.footer_contact}}</h4><ul><li><a href="mailto:sales@gasmixtech.com">sales@gasmixtech.com</a></li><li><a href="/contact">{{shared.nav_request}}</a></li><li><a href="/privacy.html">{{shared.footer_privacy}}</a></li></ul></div>
      </div>
      <div class="footer-bottom"><p>© 2026 Jinan Euchio Machinery Co., Ltd.</p></div>
    </div>
  </footer>
  <script src="/script.min.js?v=20260901-1"></script>
</body>
</html>
"""


def main():
    content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    if content.get("locale") != "en":
        raise ValueError("English product build requires locale=en")
    tracker = ContentTracker(content)
    tracker.use("locale")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_paths = set()
    for page_key, slug, product_id, page_type in PAGES:
        template_path = TEMPLATE_DIR / f"{slug}.html"
        if not template_path.is_file():
            raise FileNotFoundError(template_path)
        page_path = f"pages.{page_key}"
        page = tracker.peek(page_path)
        canonical_path = f"/products/{slug}"
        canonical = f"{DOMAIN}{canonical_path}"
        output_path = OUTPUT_DIR / f"{slug}.html"
        if output_path in output_paths:
            raise ValueError(f"Duplicate output path: {output_path}")
        output_paths.add(output_path)

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
        schema = build_schema(page, page_type, canonical, image_url, page["faq"], product_id)
        route = {
            "canonical": canonical,
            "canonical_path": canonical_path,
            "contact": f"/contact?product={product_id}",
            "og_image": image_url,
        }

        def resolve_fragment(key):
            if key.startswith("page."):
                return tracker.use(f"{page_path}.{key[5:]}")
            if key.startswith("shared."):
                return tracker.use(key)
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
            template_path.name,
        )

        shell_values = {
            "page.body": fragment,
            "schema.graph": schema,
        }

        def resolve_shell(key):
            if key in shell_values:
                return shell_values[key]
            if key.startswith("page."):
                return tracker.use(f"{page_path}.{key[5:]}")
            if key.startswith("shared."):
                return tracker.use(key)
            if key.startswith("route."):
                return route[key[6:]]
            raise KeyError(f"Unsupported shell key: {key}")

        rendered = render_template(SHELL, resolve_shell, "product shell")
        output_path.write_text(rendered, encoding="utf-8")
        print(f"built: {output_path.relative_to(ROOT)}")

    tracker.assert_all_used()


if __name__ == "__main__":
    main()
