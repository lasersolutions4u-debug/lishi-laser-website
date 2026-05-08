#!/usr/bin/env python3
"""Fix OG image paths: /{lang}/images/ → /images/ in build-langs-generated pages."""
import os, re

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"
AFFECTED = ['pl', 'vi', 'it', 'ru', 'nl', 'de', 'fr', 'th', 'tr']


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    # Fix: https://gasmixtech.com/{lang}/images/ → https://gasmixtech.com/images/
    content = re.sub(r'https://gasmixtech\.com/(pl|vi|it|ru|nl|de|fr|th|tr)/images/',
                     'https://gasmixtech.com/images/', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0


if __name__ == '__main__':
    total = 0
    for lang in AFFECTED:
        lang_dir = os.path.join(BASE, lang)
        for fname in ['index.html', 'contact.html', 'parameters.html']:
            filepath = os.path.join(lang_dir, fname)
            if os.path.exists(filepath) and fix_file(filepath):
                print(f'  {lang}/{fname}')
                total += 1
    print(f'\n{total} files fixed')
