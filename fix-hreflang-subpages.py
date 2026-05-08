#!/usr/bin/env python3
"""Fix ru/vi/th hreflang URLs in contact.html and parameters.html pages.
These were pointing to /{lang}/ (homepage) instead of /{lang}/contact.html or /{lang}/parameters.html.
"""
import os

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"


def fix_file(filepath, page_type):
    """Fix ru/vi/th hreflang in a contact.html or parameters.html file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for lang in ['ru', 'vi', 'th']:
        old = f'hreflang="{lang}" href="https://gasmixtech.com/{lang}/"'
        new = f'hreflang="{lang}" href="https://gasmixtech.com/{lang}/{page_type}"'
        content = content.replace(old, new)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 3  # 3 fixes per file
    return 0


if __name__ == '__main__':
    total = 0
    for root, dirs, files in os.walk(BASE):
        for fname in sorted(files):
            if fname == 'contact.html':
                fixes = fix_file(os.path.join(root, fname), 'contact.html')
            elif fname == 'parameters.html':
                fixes = fix_file(os.path.join(root, fname), 'parameters.html')
            else:
                continue
            if fixes:
                rel = os.path.relpath(os.path.join(root, fname), BASE)
                print(f'  {rel}: {fixes} fixes')
                total += fixes
    print(f'\n{total} total fixes')
