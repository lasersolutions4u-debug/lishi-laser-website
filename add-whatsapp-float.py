#!/usr/bin/env python3
"""Add the shared WhatsApp floating button to HTML pages that do not have it."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
LANGS = {"en", "es", "zh", "ko", "ja", "pt", "tr", "pl", "it", "de", "fr", "nl", "ru", "vi", "th"}
BUTTON_RE = re.compile(r'<a href="https://wa\.me/525572080065" class="whatsapp-float".*?</a>', re.DOTALL)


def read_text(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text(path, content):
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(content)


def language_for(path):
    relative = path.relative_to(PUBLIC)
    return relative.parts[0] if len(relative.parts) > 1 and relative.parts[0] in LANGS else "en"


def button_for(language):
    source = PUBLIC / "about.html" if language == "en" else PUBLIC / language / "about.html"
    match = BUTTON_RE.search(read_text(source))
    if not match:
        raise RuntimeError(f"WhatsApp floating button not found in {source}")
    return match.group(0)


def add_button(path, button):
    content = read_text(path)
    if 'class="whatsapp-float"' in content:
        return False
    if "</body>" not in content:
        raise RuntimeError(f"Missing </body> in {path}")
    newline = "\r\n" if "\r\n" in content else "\n"
    content = content.replace("</body>", f"{newline}{button.replace(chr(10), newline)}{newline}</body>", 1)
    write_text(path, content)
    return True


def main():
    buttons = {language: button_for(language) for language in LANGS}
    changed = []
    for path in sorted(PUBLIC.rglob("*.html")):
        if add_button(path, buttons[language_for(path)]):
            changed.append(path.relative_to(ROOT).as_posix())
    print(f"Added WhatsApp floating button to {len(changed)} files.")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
