#!/usr/bin/env python3
"""
build_storage_doc.py -- regenerate the "What is on Google Drive" section of STORAGE.md
from drive_url / gdrive_url fields in certificates/invariants.json.

Usage:
    python3 certificates/build_storage_doc.py

What it does:
1. Reads every drive_url / gdrive_url field in certificates/invariants.json.
2. Categorises entries: primary bundle ZIPs, Morning Star folder hierarchy,
   OperaNumerorum_Blocks folder, and individual uploaded files (addenda).
3. Replaces ONLY the "What is on Google Drive" section of STORAGE.md in-place.
   All content before and after that section is preserved verbatim.
"""

import json
import os
import sys
from datetime import datetime, timezone

CERTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CERTS_DIR, ".."))

INVARIANTS_PATH = os.path.join(CERTS_DIR, "invariants.json")
STORAGE_PATH = os.path.join(ROOT_DIR, "STORAGE.md")

SECTION_START = "## What is on Google Drive"
SECTION_END_MARKER = "## Why the split exists"

PRIMARY_BUNDLE_KEYS = [
    "bundle_all_certs",
    "bundle_morning_star",
    "bundle_clay",
    "bundle_context",
    "bundle_chain",
    "bundle_extended_theory",
    "bundle_essays",
]


def _size_str(entry: dict) -> str:
    if "size_mb_approx" in entry:
        return "~{:.0f} MB".format(entry["size_mb_approx"])
    if "size_mb" in entry:
        v = entry["size_mb"]
        return "~{:.0f} MB".format(float(v))
    if "size_bytes" in entry:
        mb = entry["size_bytes"] / (1024 * 1024)
        if mb >= 1:
            return "~{:.0f} MB".format(mb)
        return "~{:.0f} KB".format(entry["size_bytes"] / 1024)
    if "size_kb" in entry:
        return "~{} KB".format(entry["size_kb"])
    return "--"


def _local_path(entry: dict, key: str) -> str:
    fname = entry.get("file") or entry.get("output") or key
    if "/" in fname:
        return "`{}`".format(fname)
    return "`certificates/{}`".format(fname)


def build_section(inv: dict) -> str:
    lines = []

    lines.append("## What is on Google Drive (gitignored -- too large for GitHub)")
    lines.append("")
    lines.append("These files are listed in `.gitignore` under the heading")
    lines.append("`# Large ZIP archives (stored on Google Drive -- too big for GitHub)`.")
    lines.append("Their SHAs and Drive URLs are also recorded in `certificates/invariants.json`.")
    lines.append("")

    # ── Primary deliverable archives ─────────────────────────────────────────
    lines.append("### Primary deliverable archives")
    lines.append("")
    lines.append("| Local path | Size | Drive URL |")
    lines.append("|------------|------|-----------|")

    seen_urls = set()
    for key in PRIMARY_BUNDLE_KEYS:
        entry = inv.get(key)
        if not entry:
            continue
        url = entry.get("drive_url") or entry.get("gdrive_url") or ""
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        local = _local_path(entry, key)
        size = _size_str(entry)
        lines.append("| {} | {} | {} |".format(local, size, url))

    lines.append("")

    # ── Morning Star structured folder ────────────────────────────────────────
    ms = inv.get("gdrive_morning_star", {})
    ms_parent = ms.get("parent_folder", {})
    ms_folders = ms.get("folders", {})

    if ms_parent or ms_folders:
        lines.append("### Morning Star structured folder on Google Drive")
        lines.append("")
        lines.append(
            "The Morning Star content (zero-sorry PDFs, Lean proofs, manifests) is"
        )
        lines.append("organised into act-level subfolders under a parent folder:")
        lines.append("")
        lines.append("| Folder | Drive URL |")
        lines.append("|--------|-----------|")

        if ms_parent:
            pname = ms_parent.get("name", "MORNING_STAR_20260606")
            purl = ms_parent.get("url", "--")
            lines.append("| `{}` (parent) | {} |".format(pname, purl))

        for fname, fdata in ms_folders.items():
            fid = fdata.get("id", "")
            furl = (
                "https://drive.google.com/drive/folders/{}".format(fid) if fid else "--"
            )
            pdf_count = fdata.get("pdfs", 0)
            contains = fdata.get("contains", [])
            if pdf_count:
                label = "{} ({} PDFs)".format(fname, pdf_count)
            elif contains:
                short = " + ".join(contains[:2])
                label = "{} ({}{})".format(
                    fname, short, "..." if len(contains) > 2 else ""
                )
            else:
                label = fname
            lines.append("| `{}` | {} |".format(label, furl))

        lines.append("")

    # ── OperaNumerorum_Blocks structured folder ───────────────────────────────
    blocks = inv.get("gdrive_blocks", {})
    blocks_parent = blocks.get("parent_folder", {})
    blocks_data = blocks.get("blocks", {})

    if blocks_parent or blocks_data:
        lines.append("### OperaNumerorum_Blocks structured folder on Google Drive")
        lines.append("")
        lines.append("| Folder / File | Drive URL |")
        lines.append("|---------------|-----------|")

        if blocks_parent:
            bpname = blocks_parent.get("name", "OperaNumerorum_Blocks_20260606")
            bpurl = blocks_parent.get("url", "--")
            lines.append("| `{}` (parent) | {} |".format(bpname, bpurl))

        for bname, bdata in blocks_data.items():
            bfile = bdata.get("file", "")
            fid = bdata.get("file_id", "")
            if bfile and fid:
                file_url = "https://drive.google.com/file/d/{}".format(fid)
                lines.append("| `{}/{}` | {} |".format(bname, bfile, file_url))
            else:
                burl = bdata.get("folder_url", "--")
                lines.append("| `{}` | {} |".format(bname, burl))

        lines.append("")

    # ── Individual files uploaded to Drive (addenda) ──────────────────────────
    addenda = ms.get("addenda", [])

    # Gather any top-level individual files (non-bundle entries with drive/gdrive url)
    individual_entries = []

    eng_spec = inv.get("morningstar_engineering_spec", {})
    eng_url = eng_spec.get("gdrive_url") or eng_spec.get("drive_url") or ""
    if eng_url and eng_url not in seen_urls:
        seen_urls.add(eng_url)
        eng_file = os.path.basename(
            eng_spec.get("output", "MorningStar_Engineering_Spec_V1.pdf")
        )
        individual_entries.append({"file": eng_file, "drive_url": eng_url})

    if individual_entries or addenda:
        lines.append("### Individual files uploaded to Drive (addenda)")
        lines.append("")
        lines.append("| File | Drive URL |")
        lines.append("|------|-----------|")

        for item in individual_entries:
            lines.append("| `{}` | {} |".format(item["file"], item["drive_url"]))

        for item in addenda:
            fname = item.get("file", "--")
            url = item.get("drive_url", "--")
            lines.append("| `{}` | {} |".format(fname, url))

        lines.append("")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines.append(
        "*Section auto-generated by `certificates/build_storage_doc.py` -- "
        "last updated {}.*".format(now)
    )
    lines.append("")

    return "\n".join(lines)


def update_storage_md(new_section: str) -> None:
    with open(STORAGE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find(SECTION_START)
    if start_idx == -1:
        print(
            "ERROR: section '{}' not found in STORAGE.md".format(SECTION_START),
            file=sys.stderr,
        )
        sys.exit(1)

    # Find the separator + end-marker sequence that closes the section
    separator_plus_end = "\n---\n\n" + SECTION_END_MARKER
    sep_idx = content.find(separator_plus_end, start_idx)
    if sep_idx == -1:
        # Fallback: find just the end marker
        end_idx = content.find(SECTION_END_MARKER, start_idx)
        if end_idx == -1:
            print(
                "ERROR: end marker '{}' not found in STORAGE.md".format(
                    SECTION_END_MARKER
                ),
                file=sys.stderr,
            )
            sys.exit(1)
        replace_end = end_idx
    else:
        # sep_idx points to the \n before ---; keep that boundary
        replace_end = sep_idx

    before = content[:start_idx]
    after = content[replace_end:]  # starts with \n---\n\n## Why the split exists...

    new_content = before + new_section + after

    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("  updated STORAGE.md")


def main() -> None:
    print("=== build_storage_doc.py ===")

    with open(INVARIANTS_PATH, "r", encoding="utf-8") as f:
        inv = json.load(f)
    print("  loaded invariants.json")

    new_section = build_section(inv)
    update_storage_md(new_section)

    print("=== done ===")


if __name__ == "__main__":
    main()
