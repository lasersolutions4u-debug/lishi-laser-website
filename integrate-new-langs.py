#!/usr/bin/env python3
"""Add ru/vi/th hreflang and lang-option to all HTML pages."""
import os, re, sys

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"

NEW_LANGS = [
    ('ru', 'Русский'),
    ('vi', 'Tiếng Việt'),
    ('th', 'ไทย'),
]

def get_url_prefix(rel_path):
    """Determine hreflang URL prefix based on file location."""
    # rel_path like 'index.html', 'es/index.html', 'blog/index.html'
    parts = rel_path.split('/')
    if len(parts) == 1:
        # Root level: index.html, contact.html, parameters.html
        return 'https://gasmixtech.com/'
    elif parts[0] == 'blog':
        # Blog pages — skip hreflang for now (they have none)
        return None
    else:
        # Subdirectory pages: es/index.html, zh/contact.html, etc.
        return 'https://gasmixtech.com/'

def get_dropdown_url_prefix(rel_path):
    """Determine dropdown URL prefix."""
    parts = rel_path.split('/')
    if len(parts) == 1:
        return '/'
    elif parts[0] == 'blog':
        return '/blog/'
    else:
        return '/'

def insert_hreflangs(content, rel_path):
    """Insert ru/vi/th hreflang entries before x-default."""
    url_prefix = get_url_prefix(rel_path)
    if url_prefix is None:
        return content  # blog pages — skip hreflang

    # Build new hreflang entries
    indent = '  '  # default 2-space indent for hreflang lines
    new_entries = ''
    for code, _ in NEW_LANGS:
        # Check if already exists
        if f'hreflang="{code}"' not in content:
            new_entries += f'{indent}<link rel="alternate" hreflang="{code}" href="{url_prefix}{code}/">\n'

    if not new_entries:
        return content

    # Insert before x-default (which is always the last hreflang)
    # Pattern: the line before x-default
    xdefault_pattern = r'(<link rel="alternate" hreflang="x-default")'
    replacement = new_entries + r'\1'
    content = re.sub(xdefault_pattern, replacement, content)
    return content

def insert_lang_options(content, rel_path):
    """Insert ru/vi/th lang-options after nl entry."""
    url_prefix = get_dropdown_url_prefix(rel_path)

    # Find the nl lang-option line and its indentation
    nl_pattern = r'(\s*)<a href="([^"]*nl/)" class="lang-option" data-lang="nl">Nederlands</a>'
    match = re.search(nl_pattern, content)
    if not match:
        print(f"  WARNING: nl lang-option not found in {rel_path}")
        return content

    indent = match.group(1)
    nl_full = match.group(0)

    new_entries = ''
    for code, name in NEW_LANGS:
        if f'data-lang="{code}"' not in content:
            new_entries += f'{indent}<a href="{url_prefix}{code}/" class="lang-option" data-lang="{code}">{name}</a>\n'

    if not new_entries:
        return content

    content = content.replace(nl_full, nl_full + '\n' + new_entries.rstrip('\n'))
    return content

def process_file(filepath):
    rel_path = os.path.relpath(filepath, BASE)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = insert_hreflangs(content, rel_path)
    content = insert_lang_options(content, rel_path)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        # Count
        old_hr = len(re.findall(r'hreflang="[^"]*"', original))
        new_hr = len(re.findall(r'hreflang="[^"]*"', content))
        old_lo = len(re.findall(r'class="lang-option"', original))
        new_lo = len(re.findall(r'class="lang-option"', content))
        print(f"  {rel_path}: hreflangs {old_hr}→{new_hr}, lang-options {old_lo}→{new_lo}")
        return True
    else:
        print(f"  {rel_path}: no changes needed")
        return False

if __name__ == '__main__':
    changes = 0
    for root, dirs, files in os.walk(BASE):
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                if process_file(filepath):
                    changes += 1

    print(f"\n{changes} files updated")
