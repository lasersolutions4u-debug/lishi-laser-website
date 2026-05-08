#!/usr/bin/env python3
"""Add hreflang tags to blog article pages."""
import os, re

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public/blog"

# All 15 languages + x-default
LANGUAGES = ['en', 'zh', 'es', 'ko', 'ja', 'pt', 'tr', 'pl', 'it', 'de', 'fr', 'nl', 'ru', 'vi', 'th']

def build_hreflang_block(page_name):
    """Build hreflang block for a blog article.
    en + x-default point to the article itself.
    Other languages point to their language homepage (no blog translation exists).
    """
    lines = []
    for lang in LANGUAGES:
        if lang == 'en':
            url = f'https://gasmixtech.com/blog/{page_name}'
        else:
            url = f'https://gasmixtech.com/{lang}/'
        lines.append(f'  <link rel="alternate" hreflang="{lang}" href="{url}">')
    # x-default
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="https://gasmixtech.com/blog/{page_name}">')
    return '\n'.join(lines)

def add_hreflang(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has hreflang
    if 'hreflang="' in content:
        return False

    page_name = os.path.basename(filepath)
    hreflang_block = build_hreflang_block(page_name)

    # Insert after canonical link
    canonical_pattern = r'(<link rel="canonical" href="[^"]*">\n)'
    content = re.sub(canonical_pattern, rf'\1{hreflang_block}\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

if __name__ == '__main__':
    articles = [
        'how-to-choose-gas-mixer.html',
        'mixed-gas-vs-oxygen-comparison.html',
        'laser-cutting-gas-faq.html',
        'cutting-parameters-guide.html',
        'mixed-gas-cost-savings-case-study.html',
    ]
    for fname in articles:
        filepath = os.path.join(BASE, fname)
        if add_hreflang(filepath):
            print(f'  ✓ {fname}: added 16 hreflangs')
        else:
            print(f'  - {fname}: already has hreflangs, skipped')
    print('Done')
