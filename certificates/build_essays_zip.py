#!/usr/bin/env python3
"""
build_essays_zip.py — build Essays_Appendices_YYYY_MM_DD.zip from Block 6 PDFs

Usage:
    python3 certificates/build_essays_zip.py

What it does:
1. Collects the Block 6 PDFs (Essays & Appendices) from certificates/.
2. Builds certificates/Essays_Appendices_<date>.zip.
3. Computes SHA-256 of the resulting ZIP.
4. Writes bundle_essays into certificates/invariants.json.
5. Patches the fallback SHA and zipFile props in Certificate.tsx.
"""

import hashlib
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timezone

CERTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CERTS_DIR, ".."))
INVARIANTS_PATH = os.path.join(CERTS_DIR, "invariants.json")
TSX_PATH = os.path.join(
    ROOT_DIR, "artifacts", "prime-verifier", "src", "pages", "Certificate.tsx"
)

DATE_TAG = datetime.now(timezone.utc).strftime("%Y_%m_%d")
ZIP_FILENAME = f"Essays_Appendices_{DATE_TAG}.zip"
ZIP_PATH = os.path.join(CERTS_DIR, ZIP_FILENAME)

BLOCK6_FILES = [
    "Essay_TimeMachine_p5.pdf",
    "OperaNumerorum_Preface.pdf",
    "Addendum_A1_Complete_Sieve.pdf",
    "Wall256_YM_Report.pdf",
    "Error_Symmetry_Essay.pdf",
    "Canonical_Paper_Corrected.pdf",
    "OperaNumerorum_ArchiveMap.pdf",
    "FriendsFamily_MillennialMath.pdf",
    "Tendon_A_Certificate.pdf",
    "Tendon_B_Certificate.pdf",
]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_zip(pdf_paths: list[str]) -> None:
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for pdf in pdf_paths:
            arcname = os.path.basename(pdf)
            zf.write(pdf, arcname)
    print(f"  wrote {ZIP_PATH} ({len(pdf_paths)} PDFs)")


def update_invariants(sha: str, size_bytes: int, file_count: int) -> None:
    with open(INVARIANTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    data["bundle_essays"] = {
        "description": f"Essays and Appendices block: {file_count} PDFs.",
        "file": ZIP_FILENAME,
        "size_bytes": size_bytes,
        "sha256": sha,
        "generated_utc": now_utc,
        "pdf_count": file_count,
        "drive_url": data.get("bundle_essays", {}).get("drive_url", ""),
    }

    with open(INVARIANTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"  updated invariants.json: pdf_count={file_count}, size={size_bytes}, sha={sha[:16]}...")


def patch_tsx(old_sha: str, new_sha: str, new_filename: str) -> None:
    with open(TSX_PATH, "r", encoding="utf-8") as f:
        src = f.read()

    original = src

    if old_sha and old_sha != new_sha:
        src = src.replace(old_sha, new_sha)

    # Update zipFile fn for Block 6 — match the zipFile prop near "Essays_Appendices_"
    src = re.sub(
        r'(zipFile=\{\{ fn: ")Essays_Appendices_\d{4}_\d{2}_\d{2}\.zip(")',
        lambda m: f'{m.group(1)}{new_filename}{m.group(2)}',
        src,
    )

    if src == original:
        print("  Certificate.tsx: nothing changed (SHA already current)")
        return

    with open(TSX_PATH, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"  patched Certificate.tsx: SHA ...{new_sha[:12]}..., file={new_filename}")


def main() -> None:
    print("=== build_essays_zip.py ===")

    pdf_paths = []
    missing = []
    for fn in BLOCK6_FILES:
        p = os.path.join(CERTS_DIR, fn)
        if os.path.exists(p):
            pdf_paths.append(p)
        else:
            missing.append(fn)
            print(f"  WARNING: missing {fn}", file=sys.stderr)

    if not pdf_paths:
        print("ERROR: no PDFs found", file=sys.stderr)
        sys.exit(1)

    print(f"  found {len(pdf_paths)} PDFs ({len(missing)} missing)")

    with open(INVARIANTS_PATH, "r", encoding="utf-8") as f:
        inv = json.load(f)
    old_sha = inv.get("bundle_essays", {}).get("sha256", "")

    print("  building ZIP ...")
    build_zip(pdf_paths)

    size_bytes = os.path.getsize(ZIP_PATH)
    sha = sha256_file(ZIP_PATH)
    print(f"  SHA-256: {sha}")
    print(f"  size: {size_bytes} bytes")

    update_invariants(sha, size_bytes, len(pdf_paths))
    patch_tsx(old_sha, sha, ZIP_FILENAME)

    print("=== done ===")
    print()
    print("Next step: upload the ZIP to Google Drive and add the drive_url to")
    print(f"  invariants.json -> bundle_essays -> drive_url")


if __name__ == "__main__":
    main()
