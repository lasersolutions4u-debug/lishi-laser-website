#!/usr/bin/env python3
"""Generate the indexable sitemap and conservative AI-readable site summaries."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

from site_locales import (
    CORE_ROUTES,
    DOMAIN,
    SUPPORTED_LOCALES,
    alternates_for,
    canonical_url,
    output_path,
)


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "public"
LOCALE_NAMES = {
    "en": "English",
    "zh": "Simplified Chinese",
    "es": "Spanish",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "pl": "Polish",
}
CORE_PAGE_LABELS = {
    "home": "Laser cutting assist-gas systems",
    "about": "Supplier and solution-provider profile",
    "contact": "Selection support and quotation",
    "psa": "PSA nitrogen generation system",
    "cabinet": "Integrated gas mixing cabinet",
    "valve": "MSPV2-4000 proportional valve",
    "comparison": "Mixed-gas controller comparison",
}
TECHNICAL_LINKS = (
    ("Gas mixer for laser cutting", f"{DOMAIN}/"),
    ("Compatibility assessment", f"{DOMAIN}/compatibility.html"),
    ("Gas ratios and cutting parameters", f"{DOMAIN}/parameters"),
    ("ROI and cost factors", f"{DOMAIN}/roi.html"),
    ("Payment and procurement process", f"{DOMAIN}/payment.html"),
    ("Privacy policy", f"{DOMAIN}/privacy.html"),
    ("English technical articles", f"{DOMAIN}/blog/"),
    ("English case examples", f"{DOMAIN}/#samples"),
)
DISCOVERY_SCOPE = (
    "English, Simplified Chinese, Spanish, Portuguese, Japanese, Korean, and Polish "
    "core sales pages are maintained. Technical articles, ROI, parameters, "
    "compatibility, payment, and privacy resources are maintained in English."
)
SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
ENGLISH_TECHNICAL_PAGES = (
    ("compatibility.html", f"{DOMAIN}/compatibility.html"),
    ("parameters.html", f"{DOMAIN}/parameters"),
    ("roi.html", f"{DOMAIN}/roi.html"),
    ("payment.html", f"{DOMAIN}/payment.html"),
)
SUPPLIER_FACT = (
    "Jinan Euchio Machinery Co., Ltd. is the China-based supplier and solution "
    "provider operating this website. Product selection is assessed against "
    "laser power, material, thickness, assist-gas supply, pressure, flow, and "
    "integration requirements before quotation."
)


def is_indexable_html(path):
    if path.name in {"404.html", "_template.html", "privacy.html"}:
        return False
    content = path.read_text(encoding="utf-8", errors="ignore")
    return not re.search(
        r'<meta\s+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
        content,
        re.IGNORECASE,
    )


def get_english_resource_pages():
    pages = []
    for directory in ("blog", "case-studies"):
        for path in (BASE / directory).rglob("*.html"):
            if is_indexable_html(path):
                pages.append(path.relative_to(BASE).as_posix())
    return sorted(pages)


def rel_to_url(rel):
    if rel == "index.html":
        return f"{DOMAIN}/"
    if rel.endswith("/index.html"):
        rel = rel[:-10]
    return f"{DOMAIN}/{quote(rel, safe='/')}"


def generate_sitemap():
    ET.register_namespace("", SITEMAP_NAMESPACE)
    ET.register_namespace("xhtml", XHTML_NAMESPACE)
    root = ET.Element(f"{{{SITEMAP_NAMESPACE}}}urlset")

    def add_url(location, alternates=None):
        url = ET.SubElement(root, f"{{{SITEMAP_NAMESPACE}}}url")
        ET.SubElement(url, f"{{{SITEMAP_NAMESPACE}}}loc").text = location
        for hreflang, href in (alternates or {}).items():
            ET.SubElement(
                url,
                f"{{{XHTML_NAMESPACE}}}link",
                {"rel": "alternate", "hreflang": hreflang, "href": href},
            )

    for locale in SUPPORTED_LOCALES:
        for page_key in CORE_ROUTES:
            path = output_path(BASE, locale, page_key)
            if not path.is_file():
                raise FileNotFoundError(f"Missing core page: {path}")
            add_url(canonical_url(locale, page_key), alternates_for(page_key))

    for filename, location in ENGLISH_TECHNICAL_PAGES:
        path = BASE / filename
        if not path.is_file() or not is_indexable_html(path):
            raise FileNotFoundError(f"Missing indexable English technical page: {path}")
        add_url(location)

    for rel in get_english_resource_pages():
        add_url(rel_to_url(rel))

    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n"


def core_link_lines(locale="en"):
    return [
        f"- {CORE_PAGE_LABELS[page_key]}: {canonical_url(locale, page_key)}"
        for page_key in CORE_ROUTES
    ]


def technical_link_lines():
    return [f"- {name}: {url}" for name, url in TECHNICAL_LINKS]


def generate_llms_txt():
    locale_lines = [
        f"- {LOCALE_NAMES[locale]} ({locale}): {canonical_url(locale, 'home')}"
        for locale in SUPPORTED_LOCALES
    ]
    return "\n".join(
        [
            "# GasMixTech",
            f"> Official website: {DOMAIN}/",
            "> Product category: gas mixer for laser cutting.",
            f"> {SUPPLIER_FACT}",
            f"> {DISCOVERY_SCOPE}",
            "",
            "## English Core Sales Pages",
            *core_link_lines(),
            "",
            "## English Technical Resources",
            *technical_link_lines(),
            "",
            "## Maintained Languages",
            *locale_lines,
            "",
            "## Machine-Readable Resources",
            f"- Full site summary: {DOMAIN}/llms-full.txt",
            f"- Sitemap: {DOMAIN}/sitemap.xml",
            f"- Crawler policy: {DOMAIN}/robots.txt",
            "",
        ]
    )


def generate_llms_full_txt():
    return "\n".join(
        [
            "# Gas Mixer for Laser Cutting — Site Summary",
            "",
            "## What the equipment does",
            "A gas mixer for laser cutting combines nitrogen and oxygen into a controlled assist-gas mixture for compatible fiber laser cutting processes. Suitability and settings depend on the complete cutting and gas-supply conditions.",
            "",
            "## Supplier role",
            SUPPLIER_FACT,
            "",
            "## Selection inputs",
            "Provide the laser brand and power, material, thickness range, current assist gas, nitrogen and oxygen supply method, available pressure and flow, machine interface, and production objective before quotation.",
            "",
            "## How to use technical data",
            "Parameter tables are reference starting points rather than universal settings. Case results apply to the recorded machine, material, thickness, gas supply, pressure, flow, nozzle, focus, and operating conditions. Results can change when those conditions change.",
            "",
            "## Authoritative pages",
            *core_link_lines(),
            "",
            "## English technical resources",
            *technical_link_lines(),
            "",
            "## Contact",
            "- Company: Jinan Euchio Machinery Co., Ltd.",
            "- Role: China-based supplier and solution provider",
            "- Email: sales@gasmixtech.com",
            "- Phone / WeChat: +86 186 1558 4520",
            f"- Contact page: {DOMAIN}/contact",
            "",
            "## Maintained languages",
            DISCOVERY_SCOPE,
            "",
        ]
    )


def generate_locale_llms(code):
    return "\n".join(
        [
            f"# GasMixTech — {LOCALE_NAMES[code]}",
            f"> Maintained locale: {canonical_url(code, 'home')}",
            "> Product category: gas mixer for laser cutting.",
            f"> {SUPPLIER_FACT}",
            f"> {DISCOVERY_SCOPE}",
            "",
            "## Maintained Core Sales Pages",
            *core_link_lines(code),
            "",
            "## Authoritative English Technical Resources",
            *technical_link_lines(),
            "",
            f"- Full site summary: {DOMAIN}/llms-full.txt",
            f"- Sitemap: {DOMAIN}/sitemap.xml",
            "",
        ]
    )


def write_output(filename, content):
    path = BASE / filename
    path.write_text(content, encoding="utf-8")
    print(f"{filename}: written to {path}")


def main():
    sitemap = generate_sitemap()
    write_output("sitemap.xml", sitemap)
    print(f'Sitemap: {sitemap.count("<url>")} URLs')
    write_output("llms.txt", generate_llms_txt())
    write_output("llms-full.txt", generate_llms_full_txt())
    for code in SUPPORTED_LOCALES:
        write_output(f"llms-{code}.txt", generate_locale_llms(code))


if __name__ == "__main__":
    main()
