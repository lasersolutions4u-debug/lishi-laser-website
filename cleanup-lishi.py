#!/usr/bin/env python3
"""
Comprehensive cleanup script:
1. Rename euchio-logo.png/webp -> logo.png/webp
2. Replace all 'euchio-logo' references with 'logo' in all files
3. Replace '?v=20260622-noeuchio' with '?v=20260713'
4. Remove/replace any remaining 'EUCHIO' text in HTML files
5. Replace smart-hoist.com links with sagemro.com and dhgate links
6. Rebuild multilingual about pages from updated English about.html
"""

import os
import re
import shutil
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(BASE, "public")

# --- Step 1: Rename image files ---
print("=== Step 1: Renaming image files ===")
for ext in ['.png', '.webp']:
    old = os.path.join(PUBLIC, "images", f"euchio-logo{ext}")
    new = os.path.join(PUBLIC, "images", f"logo{ext}")
    if os.path.exists(old):
        shutil.copy2(old, new)
        print(f"  Copied: euchio-logo{ext} -> logo{ext}")
        os.remove(old)
        print(f"  Deleted: euchio-logo{ext}")

# --- Step 2-5: Process all HTML, JS, JSON files ---
print("\n=== Step 2-5: Processing all files ===")

# Collect all files to process
file_patterns = [
    os.path.join(PUBLIC, "*.html"),
    os.path.join(PUBLIC, "*.js"),
    os.path.join(PUBLIC, "*.json"),
    os.path.join(PUBLIC, "*.xml"),
    os.path.join(PUBLIC, "*.txt"),
    os.path.join(PUBLIC, "**", "*.html"),
    os.path.join(PUBLIC, "**", "*.js"),
    os.path.join(PUBLIC, "**", "*.json"),
]

processed_files = set()
for pattern in file_patterns:
    for f in glob.glob(pattern, recursive=True):
        processed_files.add(f)

stats = {'euchio-logo': 0, 'noeuchio': 0, 'euchio_text': 0, 'smart_hoist': 0, 'total_files': 0}

for filepath in sorted(processed_files):
    if not os.path.isfile(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # 2. Replace euchio-logo with logo (image file references)
    if 'euchio-logo' in content:
        content = content.replace('euchio-logo', 'logo')
        stats['euchio-logo'] += 1
        changed = True

    # 3. Replace ?v=20260622-noeuchio with ?v=20260713
    if 'noeuchio' in content:
        content = content.replace('?v=20260622-noeuchio', '?v=20260713')
        content = content.replace('noeuchio', '20260713')
        stats['noeuchio'] += 1
        changed = True

    # 4. Replace EUCHIO text references (case insensitive)
    # Only do text replacements, not in about.html (already rewritten)
    if 'EUCHIO' in content or 'EUCHIO' in content or 'EUCHIO' in content:
        # Replace various forms
        content = content.replace('EUCHIO', 'EUCHIO')
        content = content.replace('EUCHIO', 'EUCHIO')
        content = content.replace('EUCHIO', 'EUCHIO')
        content = content.replace('EUCHIO', 'EUCHIO')
        content = content.replace('EUCHIO', 'EUCHIO')
        stats['euchio_text'] += 1
        changed = True

    # 5. Replace smart-hoist links with SAGEMRO/DHgate
    if 'smart-hoist' in content:
        # Replace the footer "Related Pages" section
        content = content.replace(
            '<li><a href="https://www.smart-hoist.com" target="_blank" rel="noopener">Smart Hoist</a></li>',
            '<li><a href="https://www.sagemro.com" target="_blank" rel="noopener">SAGEMRO</a></li>\n            <li><a href="https://www.dhgate.com/store/22325464" target="_blank" rel="noopener">DHgate Store</a></li>'
        )
        # Also handle variations
        content = content.replace(
            'https://www.smart-hoist.com',
            'https://www.sagemro.com'
        )
        content = content.replace('Smart Hoist', 'SAGEMRO')
        stats['smart_hoist'] += 1
        changed = True

    # Replace "EUCHIO is the mixed gas technology brand" footer text if present
    content = content.replace(
        'EUCHIO is the mixed gas technology brand of Euchio Machinery',
        'EUCHIO is the gas mixing technology brand of Euchio Machinery'
    )
    content = content.replace(
        'EUCHIO is Euchio\'s mixed gas technology brand',
        'EUCHIO is the gas mixing technology brand of Euchio Machinery'
    )

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['total_files'] += 1
        relpath = os.path.relpath(filepath, PUBLIC)
        print(f"  Updated: {relpath}")

print(f"\n=== Summary ===")
print(f"  Files with euchio-logo refs: {stats['euchio-logo']}")
print(f"  Files with noeuchio refs: {stats['noeuchio']}")
print(f"  Files with EUCHIO text: {stats['euchio_text']}")
print(f"  Files with smart-hoist: {stats['smart_hoist']}")
print(f"  Total files updated: {stats['total_files']}")

# --- Step 6: Verify no remaining references ---
print("\n=== Verification: searching for remaining references ===")
remaining = 0
for filepath in sorted(processed_files):
    if not os.path.isfile(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'euchio' in content.lower():
        # Find the actual matches
        for i, line in enumerate(content.split('\n'), 1):
            if 'euchio' in line.lower():
                relpath = os.path.relpath(filepath, PUBLIC)
                print(f"  REMAINING: {relpath}:{i}: {line.strip()[:120]}")
                remaining += 1
if remaining == 0:
    print("  No remaining 'euchio' references found!")
else:
    print(f"  {remaining} remaining references found (review above)")

print("\nDone!")
