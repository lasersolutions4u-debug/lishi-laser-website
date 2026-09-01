#!/usr/bin/env python3
"""Replace hero image with 360 rotation video in all multilingual index.html files."""
import os, re

BASE = os.path.join(os.path.dirname(__file__), 'public')

files_to_update = [
    'de/index.html', 'fr/index.html', 'it/index.html', 'nl/index.html',
    'pl/index.html', 'ru/index.html', 'th/index.html', 'tr/index.html',
    'vi/index.html', 'blog/index.html'
]

updated = 0
for relpath in files_to_update:
    fpath = os.path.join(BASE, relpath)
    if not os.path.exists(fpath):
        print(f'  SKIP (not found): {relpath}')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'device-360-rotation' in content:
        print(f'  SKIP (already has video): {relpath}')
        continue

    # Determine the relative image path prefix
    # Pages in /{lang}/ use ../images/, blog/index.html uses ./images/ or ../images/
    if relpath.startswith('blog/'):
        img_prefix = '../images'
    else:
        img_prefix = '../images'

    # Find the hero image tag: <img src="../images/device-main.jpg?v=20260713" alt="..." class="hero-image">
    # or <img src="./images/device-main.jpg?v=20260713" alt="..." class="hero-image">
    pattern = r'<img src="[^"]*device-main\.jpg[^"]*"\s+alt="([^"]*)"\s+class="hero-image">'

    match = re.search(pattern, content)
    if not match:
        # Try alternate pattern (class before alt)
        pattern2 = r'<img src="[^"]*device-main\.jpg[^"]*"\s+class="hero-image"\s+alt="([^"]*)">'
        match = re.search(pattern2, content)

    if not match:
        # Try without alt
        pattern3 = r'<img src="[^"]*device-main\.jpg[^"]*"[^>]*class="hero-image"[^>]*>'
        match3 = re.search(pattern3, content)
        if match3:
            alt_text = 'EUCHIO Mixed Gas Device - 360 Degree Rotation View'
            old_tag = match3.group(0)
        else:
            print(f'  ERROR (no hero img found): {relpath}')
            continue
    else:
        alt_text = match.group(1)
        old_tag = match.group(0)

    # Build the new video tag
    new_tag = f'''<div style="position: relative; display: inline-block;">
            <video class="hero-image" autoplay muted loop playsinline preload="auto" poster="{img_prefix}/device-main.jpg?v=20260713" aria-label="{alt_text}">
              <source src="{img_prefix}/device-360-rotation.webm" type="video/webm">
              <source src="{img_prefix}/device-360-rotation.mp4" type="video/mp4">
              <img src="{img_prefix}/device-360-rotation.gif" alt="{alt_text}" class="hero-image">
            </video>
            <span style="position: absolute; top: 12px; right: 12px; background: rgba(220, 38, 38, 0.9); color: white; font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 50px; letter-spacing: 0.5px; pointer-events: none; z-index: 2;">360°</span>
          </div>'''

    # Replace the old img tag with the new video tag
    content = content.replace(old_tag, new_tag)

    # Also need to wrap in the hero-visual div properly
    # The old structure is: <div class="hero-visual">\n  <img ...>\n</div>
    # New structure: <div class="hero-visual">\n  <div style="position: relative...">...</div>\n</div>
    # The replacement above should handle this since we're replacing the img with a div

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    updated += 1
    print(f'  UPDATED: {relpath}')

print(f'\nDone! Updated {updated} files.')
