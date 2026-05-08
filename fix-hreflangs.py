#!/usr/bin/env python3
"""Fix corrupted hreflang URLs like /it/ja/ → /it/ or /it/ja/contact.html → /it/contact.html."""
import os, re

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"

# Pattern: hreflang URL that has a second language code in the path
# e.g., /it/ja/ → /it/, /de/ko/parameters.html → /de/parameters.html, /nl/ja/contact.html → /nl/contact.html
LANG_CODES = 'en|zh|es|ko|ja|pt|tr|pl|it|de|fr|nl|ru|vi|th'

def fix_file(filepath):
    rel_path = os.path.relpath(filepath, BASE)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix subpage URLs: /it/ja/contact.html → /it/contact.html
    pattern1 = rf'(hreflang="({LANG_CODES})" href="https://gasmixtech\.com/\2/)({LANG_CODES})(/[^"]*")'
    content = re.sub(pattern1, r'\1\4', content)

    # Fix index URLs: /it/ja/" → /it/"
    pattern2 = rf'(hreflang="({LANG_CODES})" href="https://gasmixtech\.com/\2/)({LANG_CODES})/(")'
    content = re.sub(pattern2, r'\1\4', content)

    if content != original:
        # Count fixes
        old = re.findall(r'hreflang="[^"]*" href="[^"]*"', original)
        new = re.findall(r'hreflang="[^"]*" href="[^"]*"', content)
        fixed = sum(1 for o, n in zip(old, new) if o != n)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {rel_path}: fixed {fixed} URLs")
        return True
    return False

if __name__ == '__main__':
    changes = 0
    for root, dirs, files in os.walk(BASE):
        for f in sorted(files):
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                if fix_file(filepath):
                    changes += 1
    print(f"\n{changes} files updated")
