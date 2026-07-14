#!/usr/bin/env python3
"""
Fix broken logo in multilingual subdirectory pages.

Root cause: build-about-langs.py replaces src="./images/" -> src="../images/"
but missed srcset="./images/" -> srcset="../images/". Modern browsers that
support WebP load the <source srcset> first, which points to a non-existent
/{lang}/images/logo.webp, causing the logo to break.

This script:
1. Fixes all already-generated multilingual HTML files
2. Also fixes contact.html and parameters.html in language subdirs
"""

import os
import re

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

# Language subdirectories
LANGS = ["zh", "es", "ko", "ja", "pt", "tr", "pl", "it", "de", "fr", "nl", "ru", "vi", "th"]

# File types to fix in language subdirs
HTML_FILES = ["about.html", "contact.html", "parameters.html", "privacy.html", "index.html"]

fixed_count = 0

for lang in LANGS:
    lang_dir = os.path.join(PUBLIC_DIR, lang)
    if not os.path.isdir(lang_dir):
        continue
    
    for html_file in HTML_FILES:
        filepath = os.path.join(lang_dir, html_file)
        if not os.path.isfile(filepath):
            continue
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original = content
        
        # Fix: srcset="./images/ -> srcset="../images/
        content = content.replace('srcset="./images/', 'srcset="../images/')
        
        # Also fix any remaining srcset="/images/ -> srcset="../images/ (shouldn't happen but just in case)
        content = content.replace('srcset="/images/', 'srcset="../images/')
        
        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            fixed_count += 1
            print(f"  Fixed: {lang}/{html_file}")

print(f"\nTotal files fixed: {fixed_count}")
