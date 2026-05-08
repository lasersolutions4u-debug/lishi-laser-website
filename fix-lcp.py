#!/usr/bin/env python3
"""LCP optimization: add fetchpriority, width/height to hero image, preload link."""
import os, re

BASE = "/Users/joe/Nutstore Files/我的坚果云/Euchio/激光 金属成型/混合气体设备/网站/public"


def optimize_index(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Add width/height/fetchpriority to device-main.jpg img tag
    # Match: <img src="./images/device-main.jpg" or <img src="../images/device-main.jpg"
    content = re.sub(
        r'(<img src="[./]*images/device-main\.jpg" alt="[^"]*") class="hero-image">',
        r'\1 width="1280" height="1280" fetchpriority="high" class="hero-image">',
        content)

    # 2. Add preload link before </head>
    if '<link rel="preload" as="image"' not in content:
        content = content.replace(
            '</head>',
            '  <link rel="preload" as="image" href="/images/device-main.jpg" fetchpriority="high">\n</head>')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


if __name__ == '__main__':
    count = 0
    # Root index
    filepath = os.path.join(BASE, 'index.html')
    if optimize_index(filepath):
        print('  index.html')
        count += 1

    # Language subdirectory indexes
    for lang in ['zh', 'es', 'ko', 'ja', 'pt', 'tr', 'pl', 'it', 'de', 'fr', 'nl', 'ru', 'vi', 'th']:
        filepath = os.path.join(BASE, lang, 'index.html')
        if os.path.exists(filepath) and optimize_index(filepath):
            print(f'  {lang}/index.html')
            count += 1

    print(f'\n{count} files optimized')
