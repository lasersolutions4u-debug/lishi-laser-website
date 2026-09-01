#!/usr/bin/env python3
"""Add about.html URLs to sitemap.xml for all 15 languages."""
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
SITEMAP = os.path.join(BASE, 'sitemap.xml')

LANGS = ['en', 'zh', 'es', 'ko', 'ja', 'pt', 'pl']

def build_hreflang_block(page):
    """Build hreflang alternate links for a page."""
    lines = []
    for lang in LANGS:
        if lang == 'en':
            url = f'https://gasmixtech.com/{page}'
        else:
            url = f'https://gasmixtech.com/{lang}/{page}'
        lines.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{url}" />')
    # x-default
    url = f'https://gasmixtech.com/{page}'
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url}" />')
    return '\n'.join(lines)

def main():
    with open(SITEMAP, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if about.html is already in sitemap
    if 'about.html' in content:
        print("about.html already in sitemap, skipping.")
        return

    # Build about.html URL entries
    about_entries = []
    for lang in LANGS:
        if lang == 'en':
            loc = 'https://gasmixtech.com/about.html'
        else:
            loc = f'https://gasmixtech.com/{lang}/about.html'

        hreflang = build_hreflang_block('about.html')
        entry = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>2026-07-13</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
{hreflang}
  </url>"""
        about_entries.append(entry)

    # Insert before </urlset>
    insert_block = '\n'.join(about_entries) + '\n'
    content = content.replace('</urlset>', insert_block + '</urlset>')

    with open(SITEMAP, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Added {len(LANGS)} about.html entries to sitemap.xml")

if __name__ == '__main__':
    main()
