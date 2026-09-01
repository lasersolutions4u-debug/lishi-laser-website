#!/usr/bin/env python3
"""Generate the indexable sitemap and conservative AI-readable site summaries."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "public"
DOMAIN = "https://gasmixtech.com"
LANGS = ("en", "zh", "es", "ko", "ja", "pt", "pl")
LOCALES = (
    ("en", "English", "/"),
    ("zh", "Chinese", "/zh/"),
    ("es", "Spanish", "/es/"),
    ("ko", "Korean", "/ko/"),
    ("ja", "Japanese", "/ja/"),
    ("pt", "Portuguese", "/pt/"),
    ("pl", "Polish", "/pl/"),
)
PRETTY_PAGES = {"about.html", "contact.html", "parameters.html"}
LOCALIZED_PAGES = {
    "index.html",
    "about.html",
    "contact.html",
    "parameters.html",
    "compatibility.html",
    "roi.html",
    "payment.html",
}
CORE_LINKS = (
    ("Gas mixer for laser cutting", f"{DOMAIN}/"),
    ("Supplier and solution-provider profile", f"{DOMAIN}/about"),
    ("Compatibility assessment", f"{DOMAIN}/compatibility.html"),
    ("Gas ratios and cutting parameters", f"{DOMAIN}/parameters"),
    ("ROI and cost factors", f"{DOMAIN}/roi.html"),
    ("Payment and procurement process", f"{DOMAIN}/payment.html"),
    ("Selection support and quotation", f"{DOMAIN}/contact"),
    ("English technical articles", f"{DOMAIN}/blog/"),
    ("English case examples", f"{DOMAIN}/#samples"),
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


def get_all_pages():
    pages = []
    for path in BASE.rglob("*.html"):
        rel_parts = path.relative_to(BASE).parts
        if any(part in {"pagefind", ".wrangler"} for part in rel_parts):
            continue
        if is_indexable_html(path):
            pages.append(path.relative_to(BASE).as_posix())
    return sorted(pages)


def rel_to_url(rel):
    if rel == "index.html":
        return f"{DOMAIN}/"
    if rel.endswith("/index.html"):
        return f"{DOMAIN}/{rel[:-10]}"
    if Path(rel).name in PRETTY_PAGES:
        return f"{DOMAIN}/{rel[:-5]}"
    return f"{DOMAIN}/{rel}"


def localized_rel(lang, filename):
    return filename if lang == "en" else f"{lang}/{filename}"


def alternate_group(rel):
    parts = rel.split("/")
    filename = parts[-1]
    is_core_location = len(parts) == 1 or (len(parts) == 2 and parts[0] in LANGS[1:])
    if is_core_location and filename in LOCALIZED_PAGES:
        return {lang: localized_rel(lang, filename) for lang in LANGS}
    return None


def generate_sitemap():
    pages = get_all_pages()
    page_set = set(pages)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for rel in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{rel_to_url(rel)}</loc>")
        alternates = alternate_group(rel)
        if alternates:
            for lang in LANGS:
                alternate_rel = alternates[lang]
                if alternate_rel in page_set:
                    lines.append(
                        f'    <xhtml:link rel="alternate" hreflang="{lang}" '
                        f'href="{rel_to_url(alternate_rel)}" />'
                    )
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" '
                f'href="{rel_to_url(alternates["en"])}" />'
            )
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def link_lines():
    return [f"- {name}: {url}" for name, url in CORE_LINKS]


def generate_llms_txt():
    locale_lines = [f"- {label} ({code}): {DOMAIN}{path}" for code, label, path in LOCALES]
    return "\n".join(
        [
            "# GasMixTech",
            f"> Official website: {DOMAIN}/",
            "> Product category: gas mixer for laser cutting.",
            f"> {SUPPLIER_FACT}",
            "",
            "## Core Pages",
            *link_lines(),
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
            *link_lines(),
            "",
            "## Contact",
            "- Company: Jinan Euchio Machinery Co., Ltd.",
            "- Role: China-based supplier and solution provider",
            "- Email: sales@gasmixtech.com",
            "- Phone / WeChat: +86 186 1558 4520",
            f"- Contact page: {DOMAIN}/contact",
            "",
            "## Maintained languages",
            "English, Chinese, Spanish, Korean, Japanese, Portuguese, and Polish core pages are maintained. Technical articles and case examples are maintained in English.",
            "",
        ]
    )


def generate_locale_llms(code, label, path):
    return "\n".join(
        [
            f"# GasMixTech — {label}",
            f"> Maintained locale: {DOMAIN}{path}",
            "> Product category: gas mixer for laser cutting.",
            f"> {SUPPLIER_FACT}",
            "",
            "## Authoritative English Resources",
            *link_lines(),
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
    for code, label, path in LOCALES:
        write_output(f"llms-{code}.txt", generate_locale_llms(code, label, path))


if __name__ == "__main__":
    main()
