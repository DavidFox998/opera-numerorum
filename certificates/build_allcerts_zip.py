#!/usr/bin/env python3
"""
build_allcerts_zip.py — rebuild OperaNumerorum_AllCerts.zip from all PDFs in certificates/

Usage:
    python3 certificates/build_allcerts_zip.py

What it does:
1. Collects every *.pdf in certificates/ (sorted, reproducible order).
2. Builds certificates/OperaNumerorum_AllCerts.zip (PDF files + invariants.json).
3. Computes SHA-256 of the resulting ZIP.
4. Writes sha256, size_bytes, size_mb_approx, pdf_count, generated_utc back to
   certificates/invariants.json under the "bundle_all_certs" key.
5. Patches the hardcoded fallback SHA, PDF count, and size string in
   artifacts/prime-verifier/src/pages/Certificate.tsx so the UI stays in sync.
"""

import glob
import hashlib
import json
import math
import os
import re
import sys
import zipfile
from datetime import datetime, timezone

CERTS_DIR = os.path.join(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CERTS_DIR, ".."))

ZIP_PATH = os.path.join(CERTS_DIR, "OperaNumerorum_AllCerts.zip")
INVARIANTS_PATH = os.path.join(CERTS_DIR, "invariants.json")
TSX_PATH = os.path.join(
    ROOT_DIR,
    "artifacts", "prime-verifier", "src", "pages", "Certificate.tsx"
)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_zip(pdf_paths: list[str]) -> None:
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for pdf in sorted(pdf_paths):
            arcname = os.path.join("PDFs", os.path.basename(pdf))
            zf.write(pdf, arcname)
        zf.write(INVARIANTS_PATH, "invariants.json")
    print(f"  wrote {ZIP_PATH} ({len(pdf_paths)} PDFs + invariants.json)")


def update_invariants(sha: str, size_bytes: int, pdf_count: int) -> None:
    with open(INVARIANTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    size_mb = round(size_bytes / (1024 * 1024), 1)
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    data["bundle_all_certs"] = {
        "description": f"Full certified archive: all {pdf_count} PDFs + invariants.json. Complete Opera Numerorum record.",
        "file": "OperaNumerorum_AllCerts.zip",
        "size_bytes": size_bytes,
        "size_mb_approx": size_mb,
        "sha256": sha,
        "generated_utc": now_utc,
        "pdf_count": pdf_count,
        "contents": [
            "invariants.json",
            f"PDFs/*.pdf ({pdf_count} files)"
        ]
    }

    with open(INVARIANTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"  updated invariants.json: pdf_count={pdf_count}, size_mb={size_mb}, sha={sha[:16]}...")


def patch_tsx(old_sha: str, new_sha: str, new_count: int, new_size_mb: float) -> None:
    with open(TSX_PATH, "r", encoding="utf-8") as f:
        src = f.read()

    original = src

    # 1. Replace ALL_CERTS_ZIP fallback SHA (may appear multiple times as ?? "...")
    if old_sha and old_sha != new_sha:
        src = src.replace(old_sha, new_sha)

    # 2. Patch "All N PDFs" in the section header (e.g. "All 72 PDFs")
    src = re.sub(
        r'(Full Certificate Archive \(All\s+)\d+(\s+PDFs\))',
        lambda m: f'{m.group(1)}{new_count}{m.group(2)}',
        src
    )

    # 3. Patch the "~XX MB" size annotation next to the all-certs description
    #    Only within the all-certs card (the amber-colored span near "~86 MB")
    #    We match the amber span that holds the size so we don't clobber other sizes.
    size_str = f"~{new_size_mb:.0f} MB"
    src = re.sub(
        r'(<span className="text-amber-400">~)\d+(\s*MB</span>)',
        lambda m: f'{m.group(1)}{new_size_mb:.0f}{m.group(2)}',
        src
    )

    if src == original:
        print("  Certificate.tsx: nothing changed (SHA, count, and size already current)")
        return

    with open(TSX_PATH, "w", encoding="utf-8") as f:
        f.write(src)

    changed = []
    if old_sha and old_sha != new_sha:
        changed.append(f"SHA {old_sha[:12]}...→{new_sha[:12]}...")
    changed.append(f"count→{new_count}")
    changed.append(f"size→{size_str}")
    print(f"  patched Certificate.tsx: {', '.join(changed)}")


def main() -> None:
    print("=== build_allcerts_zip.py ===")

    pdf_paths = sorted(glob.glob(os.path.join(CERTS_DIR, "*.pdf")))
    if not pdf_paths:
        print("ERROR: no PDFs found in certificates/", file=sys.stderr)
        sys.exit(1)
    print(f"  found {len(pdf_paths)} PDFs")

    # Read old SHA before rebuilding the ZIP (so we know what to replace in TSX)
    with open(INVARIANTS_PATH, "r", encoding="utf-8") as f:
        inv = json.load(f)
    old_sha = inv.get("bundle_all_certs", {}).get("sha256", "")

    print("  building ZIP …")
    build_zip(pdf_paths)

    size_bytes = os.path.getsize(ZIP_PATH)
    sha = sha256_file(ZIP_PATH)
    size_mb = round(size_bytes / (1024 * 1024), 1)
    pdf_count = len(pdf_paths)

    print(f"  SHA-256: {sha}")
    print(f"  size: {size_bytes} bytes ({size_mb} MB)")

    update_invariants(sha, size_bytes, pdf_count)
    patch_tsx(old_sha, sha, pdf_count, size_mb)

    print("=== done ===")


if __name__ == "__main__":
    main()
