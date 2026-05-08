#!/usr/bin/env python3
"""Fix dropdown URLs and add ru/vi/th to all pages. Handles all page types."""
import os, re

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"

ALL_LANGS = [
    ('en', 'English'), ('zh', '中文'), ('es', 'Español'),
    ('ko', '한국어'), ('ja', '日本語'), ('pt', 'Português'),
    ('tr', 'Türkçe'), ('pl', 'Polski'), ('it', 'Italiano'),
    ('de', 'Deutsch'), ('fr', 'Français'), ('nl', 'Nederlands'),
    ('ru', 'Русский'), ('vi', 'Tiếng Việt'), ('th', 'ไทย'),
]

def parse_path(rel_path):
    parts = rel_path.split('/')
    if parts[0] == 'blog':
        return ('blog', None, parts[-1])
    elif len(parts) == 1:
        return ('root', None, parts[0])
    else:
        return ('subdir', parts[0], parts[1])

def detect_style(content, page_lang):
    """Detect URL style from existing lang-options."""
    for m in re.finditer(r'<a href="([^"]*)" class="lang-option[^"]*" data-lang="([^"]*)">', content):
        href, lang = m.group(1), m.group(2)
        if lang == 'en' or lang == page_lang:
            continue
        uses_rel = href.startswith('../')
        has_blog = '/blog/' in href
        return ('rel' if uses_rel else 'abs', 'blog' if has_blog else None)
    return ('abs', None)

def make_url(lang, page_lang, page_name, page_type, style, blog_suffix):
    if page_type == 'root':
        if lang == 'en':
            return '/' if page_name == 'index.html' else f'/{page_name}'
        return f'/{lang}/' if page_name == 'index.html' else f'/{lang}/{page_name}'

    elif page_type == 'subdir':
        if style == 'rel':
            if lang == 'en':
                return '../' if page_name == 'index.html' else f'../{page_name}'
            elif lang == page_lang:
                return './' if page_name == 'index.html' else f'./{page_name}'
            else:
                return f'../{lang}/' if page_name == 'index.html' else f'../{lang}/{page_name}'
        else:
            # Absolute style (build-langs.py pages)
            if lang == 'en':
                return '/' if page_name == 'index.html' else f'/{page_name}'
            elif lang == page_lang:
                return f'/{lang}/' if page_name == 'index.html' else f'/{lang}/{page_name}'
            else:
                return f'/{lang}/' if page_name == 'index.html' else f'/{lang}/{page_name}'

    elif page_type == 'blog':
        if lang == 'en':
            if blog_suffix == 'blog':
                return '/blog/' if page_name == 'index.html' else f'/blog/{page_name}'
            return '/'
        else:
            if blog_suffix == 'blog':
                return f'/{lang}/blog/' if page_name == 'index.html' else f'/{lang}/blog/{page_name}'
            return f'/{lang}/'

def build_dropdown_html(indent, page_type, page_lang, page_name, style, blog_suffix):
    lines = []
    for code, name in ALL_LANGS:
        url = make_url(code, page_lang, page_name, page_type, style, blog_suffix)
        is_active = (code == page_lang) or (page_lang is None and code == 'en')
        active = ' active' if is_active else ''
        lines.append(f'{indent}<a href="{url}" class="lang-option{active}" data-lang="{code}">{name}</a>')
    return '\n'.join(lines)

def replace_dropdown(content, page_type, page_lang, page_name):
    """Replace the entire lang-dropdown div contents."""
    # Find the lang-dropdown div
    pattern = r'(\s*)<div class="lang-dropdown"[^>]*>.*?</div>'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return content

    indent = match.group(1)
    style, blog_suffix = detect_style(content, page_lang)

    # Detect option indentation from first existing lang-option
    opt_match = re.search(r'(\s*)<a href="[^"]*" class="lang-option', content)
    option_indent = opt_match.group(1) if opt_match else indent + ' ' * 2

    new_options = build_dropdown_html(option_indent, page_type, page_lang, page_name, style, blog_suffix)

    new_dropdown = f'{indent}<div class="lang-dropdown" id="langDropdown">\n{new_options}\n{indent}</div>'

    if match.group(0) == new_dropdown:
        return content

    return content.replace(match.group(0), new_dropdown, 1)

def add_hreflangs(content):
    existing = set(m.group(1) for m in re.finditer(r'hreflang="([^"]*)"', content))
    to_add = [l for l in ['ru', 'vi', 'th'] if l not in existing]
    if not to_add:
        return content

    new_entries = ''.join(
        f'  <link rel="alternate" hreflang="{c}" href="https://gasmixtech.com/{c}/">\n'
        for c in to_add
    )
    return content.replace(
        '<link rel="alternate" hreflang="x-default"',
        new_entries + '<link rel="alternate" hreflang="x-default"'
    )

def process_file(filepath):
    rel_path = os.path.relpath(filepath, BASE)
    page_type, page_lang, page_name = parse_path(rel_path)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    if 'hreflang="x-default"' in content:
        content = add_hreflangs(content)

    if 'lang-dropdown' in content:
        content = replace_dropdown(content, page_type, page_lang, page_name)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        old_hr = original.count('hreflang="')
        new_hr = content.count('hreflang="')
        old_lo = original.count('class="lang-option')
        new_lo = content.count('class="lang-option')
        print(f"  {rel_path}: hreflangs {old_hr}→{new_hr}, lang-options {old_lo}→{new_lo}")
        return True
    else:
        print(f"  {rel_path}: no changes needed")
        return False

if __name__ == '__main__':
    changes = 0
    for root, dirs, files in os.walk(BASE):
        for f in sorted(files):
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                if process_file(filepath):
                    changes += 1
    print(f"\n{changes} files updated")
