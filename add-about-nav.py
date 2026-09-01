#!/usr/bin/env python3
"""
Add About link to navigation and footer of all existing multilingual pages.
Works on: index, parameters, contact pages in all 14 non-English languages.
"""
import os, re, glob

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

LANGS = ['zh', 'es', 'ko', 'ja', 'pt', 'pl']

# Nav label translations
NAV_ABOUT = {
    'zh': '关于我们', 'es': 'Acerca de', 'ko': '소개', 'ja': '会社概要',
    'pt': 'Sobre', 'tr': 'Hakkımızda', 'pl': 'O nas', 'it': 'Chi siamo',
    'de': 'Über uns', 'fr': 'À propos', 'nl': 'Over ons', 'ru': 'О нас',
    'vi': 'Giới thiệu', 'th': 'เกี่ยวกับ',
}

FOOTER_ABOUT = {
    'zh': '关于我们', 'es': 'Sobre Nosotros', 'ko': '회사 소개', 'ja': '会社概要',
    'pt': 'Sobre Nós', 'tr': 'Hakkımızda', 'pl': 'O nas', 'it': 'Chi siamo',
    'de': 'Über uns', 'fr': 'À propos de nous', 'nl': 'Over ons', 'ru': 'О нас',
    'vi': 'Giới thiệu', 'th': 'เกี่ยวกับเรา',
}

PAGES = ['index.html', 'parameters.html', 'contact.html']

def add_about_to_nav(content, lang, page_type):
    """Add About link after Home link in navigation."""
    p = lang
    about_label = NAV_ABOUT[lang]
    about_url = f'/{p}/about'

    # Pattern 1: parameters/contact pages have <a href="/{lang}/">Label</a>
    # Pattern 2: index pages have <a href="#home" class="active">Label</a> or similar

    # For subdirectory pages (parameters, contact):
    # Insert after the Home link
    home_pattern = f'<a href="/{p}/">'
    if home_pattern in content and f'href="{about_url}"' not in content:
        # Find the first occurrence (nav, not footer logo)
        # Insert About link after the closing </a> of Home
        idx = content.find(home_pattern)
        if idx != -1:
            # Find the end of the Home </a> tag
            end_idx = content.find('</a>', idx) + 4
            # Insert About link
            about_link = f'\n        <a href="{about_url}">{about_label}</a>'
            content = content[:end_idx] + about_link + content[end_idx:]

    return content

def add_about_to_footer(content, lang):
    """Add About Us link to footer Product section."""
    p = lang
    about_label = FOOTER_ABOUT[lang]
    about_url = f'/{p}/about'

    # Find footer Product section - look for the first footer-links ul
    # Pattern: <h4>Product</h4> or translated equivalent, then <ul class="footer-links">
    # We'll insert after the first <li> in the first footer-links ul

    if f'href="{about_url}"' in content:
        return content  # Already has about link

    # Find the footer-links ul and insert About as first item
    # Look for pattern: <ul class="footer-links">\n            <li>
    pattern = r'(<ul class="footer-links">\s*)<li>'
    replacement = rf'\1<li><a href="{about_url}">{about_label}</a></li>\n            <li>'
    content = re.sub(pattern, replacement, content, count=1)

    return content

def main():
    updated = 0
    for lang in LANGS:
        for page in PAGES:
            filepath = os.path.join(BASE, lang, page)
            if not os.path.exists(filepath):
                print(f"  Skip (not found): {lang}/{page}")
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content
            page_type = 'index' if page == 'index.html' else page.replace('.html', '')

            content = add_about_to_nav(content, lang, page_type)
            content = add_about_to_footer(content, lang)

            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
                print(f"  Updated: {lang}/{page}")
            else:
                print(f"  No change: {lang}/{page}")

    print(f"\nDone! Updated {updated} files.")

if __name__ == '__main__':
    main()
