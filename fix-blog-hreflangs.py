#!/usr/bin/env python3
"""Fix blog hreflang: remove non-English hreflang entries since no blog translations exist.
Keep only en (pointing to article) + x-default."""
import os, re

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public/blog"

BLOG_FILES = [
    'index.html',
    'how-to-choose-gas-mixer.html',
    'mixed-gas-vs-oxygen-comparison.html',
    'laser-cutting-gas-faq.html',
    'cutting-parameters-guide.html',
    'mixed-gas-cost-savings-case-study.html',
]


def fix_blog_hreflang(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove all non-English, non-x-default hreflang lines
    # Pattern: lines with hreflang="xx" where xx is NOT en and NOT x-default
    # These point to language homepages since no blog translations exist
    content = re.sub(
        r'  <link rel="alternate" hreflang="(?!en|x-default)[^"]+" href="https://gasmixtech\.com/[^"]+">\n',
        '', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        # Count removed lines
        removed = original.count('hreflang="') - content.count('hreflang="')
        return removed
    return 0


if __name__ == '__main__':
    total = 0
    for fname in BLOG_FILES:
        filepath = os.path.join(BASE, fname)
        removed = fix_blog_hreflang(filepath)
        if removed:
            print(f'  {fname}: removed {removed} hreflang entries')
            total += removed
    print(f'\n{total} total hreflang entries removed from {len(BLOG_FILES)} blog pages')
