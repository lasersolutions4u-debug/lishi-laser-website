#!/usr/bin/env python3
"""Build and validate the maintained multilingual core sales path."""

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PYTHON = str(Path(sys.executable).resolve())
_node = shutil.which("node")
if _node is None:
    raise RuntimeError("Node.js executable was not found on PATH")
NODE = str(Path(_node).resolve())

STAGES = (
    ("homepages", (NODE, str(ROOT / "public" / "build-i18n.js"))),
    ("about-contact", (PYTHON, str(ROOT / "build-static-core-pages.py"))),
    ("products", (PYTHON, str(ROOT / "build-product-pages.py"))),
    (
        "integrity-check",
        (PYTHON, "-m", "unittest", "-v", "tests.test_multilingual_sales_path"),
    ),
)


def main():
    for name, command in STAGES:
        print(f"[{name}]", flush=True)
        subprocess.run(list(command), cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
