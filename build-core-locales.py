#!/usr/bin/env python3
"""Build and validate the maintained multilingual core sales path."""

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def resolve_stages():
    node_path = shutil.which("node")
    if node_path is None:
        raise RuntimeError("Node.js executable was not found on PATH")
    node = str(Path(node_path).resolve())
    python = str(Path(sys.executable).resolve())
    return (
        ("homepages", (node, str(ROOT / "public" / "build-i18n.js"))),
        ("about-contact", (python, str(ROOT / "build-static-core-pages.py"))),
        ("products", (python, str(ROOT / "build-product-pages.py"))),
        (
            "integrity-check",
            (python, "-m", "unittest", "-v", "tests.test_multilingual_sales_path"),
        ),
    )


def main():
    for name, command in resolve_stages():
        print(f"[{name}]", flush=True)
        subprocess.run(list(command), cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
