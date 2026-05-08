#!/usr/bin/env python3
"""Fix translated JSON-LD @type values back to English (Schema.org requirement)."""
import os

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"

# Mapping of translated @type values → correct English
FIXES = {
    # German
    '"KontaktPage"': '"ContactPage"',
    '"KontaktPoint"': '"ContactPoint"',
    '"Produkt"': '"Product"',
    # Italian
    '"ContattoPage"': '"ContactPage"',
    '"ContattoPoint"': '"ContactPoint"',
    '"Prodotto"': '"Product"',
    # French
    '"Produit"': '"Product"',
    # Vietnamese
    '"Hỏi đápPage"': '"FAQPage"',
    '"Liên hệPage"': '"ContactPage"',
    '"Liên hệPoint"': '"ContactPoint"',
    '"Sản phẩm"': '"Product"',
    # Russian
    '"ВопросыPage"': '"FAQPage"',
    '"КонтактыPage"': '"ContactPage"',
    '"КонтактыPoint"': '"ContactPoint"',
    '"Продукт"': '"Product"',
    # Thai
    '"ติดต่อPage"': '"ContactPage"',
    '"คำถามที่พบบ่อยPage"': '"FAQPage"',
    '"ติดต่อPoint"': '"ContactPoint"',
    '"ผลิตภัณฑ์"': '"Product"',
}

LANGS = ['de', 'it', 'fr', 'vi', 'ru', 'th']


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for bad, good in FIXES.items():
        content = content.replace(bad, good)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        # Count fixes
        fixes = sum(1 for bad in FIXES if bad in original)
        return fixes
    return 0


if __name__ == '__main__':
    total_fixes = 0
    total_files = 0
    for lang in LANGS:
        lang_dir = os.path.join(BASE, lang)
        for fname in ['index.html', 'contact.html', 'parameters.html']:
            filepath = os.path.join(lang_dir, fname)
            if os.path.exists(filepath):
                fixes = fix_file(filepath)
                if fixes > 0:
                    print(f'  {lang}/{fname}: {fixes} fixes')
                    total_fixes += fixes
                    total_files += 1
    print(f'\n{total_files} files fixed, {total_fixes} total replacements')
