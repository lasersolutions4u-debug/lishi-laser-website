#!/usr/bin/env python3
"""Normalize Pagefind's generated language map for reproducible builds."""

import json
from pathlib import Path


ENTRY_PATH = Path(__file__).resolve().parent / "public" / "pagefind" / "pagefind-entry.json"


def normalize_pagefind_entry(path=ENTRY_PATH):
    entry = json.loads(path.read_text(encoding="utf-8"))
    entry["languages"] = dict(sorted(entry["languages"].items()))
    path.write_text(
        json.dumps(entry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    normalize_pagefind_entry()
