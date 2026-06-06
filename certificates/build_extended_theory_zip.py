#!/usr/bin/env python3
"""
build_extended_theory_zip.py — build ExtendedTheory_YYYY_MM_DD.zip from Block 5 PDFs

Usage:
    python3 certificates/build_extended_theory_zip.py

What it does:
1. Collects the Block 5 PDFs (M8A-M25, M10, BDP) from certificates/.
2. Builds certificates/ExtendedTheory_<date>.zip.
3. Computes SHA-256 of the resulting ZIP.
4. Writes bundle_extended_theory into certificates/invariants.json.
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
ZIP_FILENAME = f"ExtendedTheory_{DATE_TAG}.zip"
ZIP_PATH = os.path.join(CERTS_DIR, ZIP_FILENAME)

BLOCK5_FILES = [
    "Module_M8A_Audit.pdf",
    "Module_M8C_ZoeMstar.pdf",
    "Module_M8D_Resonator.pdf",
    "Module_M8F_LeanProtocol.pdf",
    "Module_M8G_Provenance.pdf",
    "Module_M8G_Correction.pdf",
    "Module_M8H_G_Amplifier.pdf",
    "Module_M8I_Wormhole.pdf",
    "Module_M8J_OQ2_Closure.pdf",
    "Module_9_All_140.pdf",
    "Module_9_Certificate.pdf",
    "Module_10_Genus33.pdf",
    "Module_14_S4_Quaternions.pdf",
    "Module_15_Delta_Boost.pdf",
    "Module_16_c_Bridge.pdf",
    "Module_17_Cert_Patch.pdf",
    "Module_18_Resonance_Ladder.pdf",
    "Module_19_p6_Prediction.pdf",
    "Module_20_p7_Prediction.pdf",
    "Module_21_H4_Invariant.pdf",
    "Module_22_MStar_Definition.pdf",
    "Module_23_BSD_J0_143.pdf",
    "Module_24_Certificate.pdf",
    "Module_25_Certificate.pdf",
    "Module_25B_Certificate.pdf",
    "Module_BDP_PhaseReversal.pdf",
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

    data["bundle_extended_theory"] = {
        "description": f"Extended Theory block M8A-M25, M10, BDP: {file_count} PDFs.",
        "file": ZIP_FILENAME,
        "size_bytes": size_bytes,
        "sha256": sha,
        "generated_utc": now_utc,
        "pdf_count": file_count,
        "drive_url": data.get("bundle_extended_theory", {}).get("drive_url", ""),
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

    # Update zipFile fn for Block 5 — match the zipFile prop near "ExtendedTheory_"
    src = re.sub(
        r'(zipFile=\{\{ fn: ")ExtendedTheory_\d{4}_\d{2}_\d{2}\.zip(")',
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
    print("=== build_extended_theory_zip.py ===")

    pdf_paths = []
    missing = []
    for fn in BLOCK5_FILES:
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
    old_sha = inv.get("bundle_extended_theory", {}).get("sha256", "")

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
    print(f"  invariants.json -> bundle_extended_theory -> drive_url")


if __name__ == "__main__":
    main()
