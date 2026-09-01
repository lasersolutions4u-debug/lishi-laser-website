#!/usr/bin/env python3
"""Replace the obsolete Footer company description across generated pages."""

from pathlib import Path


PUBLIC = Path(__file__).resolve().parent / "public"
OLD = "Jinan Euchio Machinery Co., Ltd. — machinery trading and service for sheet metal processing equipment. Operating EUCHIO (complete machines) and SAGEMRO (MRO parts & service) brands for overseas industrial customers."
PREVIOUS = "Jinan Euchio Machinery Co., Ltd. — industrial equipment solutions and service for sheet metal processing. Operating EUCHIO (complete machines) and SAGEMRO (MRO parts & service) brands for overseas industrial customers."
NEW = "Jinan Euchio Machinery Co., Ltd. is an industrial equipment solutions and service company focused on sheet metal processing. We provide practical equipment, gas mixing technology, application assessment, technical coordination, and long-term support for overseas industrial customers through EUCHIO complete machines and SAGEMRO MRO parts and service."


changed = []
for path in sorted(PUBLIC.rglob("*.html")):
    content = path.read_text(encoding="utf-8")
    if OLD not in content and PREVIOUS not in content:
        continue
    content = content.replace(OLD, NEW).replace(PREVIOUS, NEW)
    path.write_text(content, encoding="utf-8", newline="")
    changed.append(path.relative_to(PUBLIC).as_posix())

print(f"Updated Footer intro in {len(changed)} files.")
for path in changed:
    print(path)
