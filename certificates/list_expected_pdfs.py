#!/usr/bin/env python3
"""
list_expected_pdfs.py -- Emit every PDF path expected on GitHub.

Strategy (three passes, no existence filter):

  Pass 1 (generic scan): collect every string value ending in ".pdf" from
    certificates/invariants.json that starts with "certificates/".
    This covers pdf_file, file, pdf, pdf_path, output, historical, path,
    name, and any future key names.  Paths with attached_assets/, stale
    root-level names, or timestamped upload filenames are excluded by the
    prefix filter.

  Pass 2 (hardcoded supplement): add the ~18 entries that carry sha256_pdf
    in invariants.json but store no "certificates/" path string at all
    (Modules 1-8, 25, 26, plus several named certificates whose paths are
    implied by convention).  These are included unconditionally if the
    top-level invariants key exists and has sha256_pdf.

  Pass 3 (root-level exceptions): a small fixed set of repo-root PDFs
    that are legitimately outside the certificates/ directory.

NOTE: No existence filter.  A cert that is expected (registered in
invariants.json or hardcoded here) should be verified on GitHub regardless
of whether it currently exists on the local disk.  A missing cert will
return HTTP 404 and correctly fail the post-push check.

Output: one repo-relative path per line, de-duplicated, sorted.
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INVARIANTS = os.path.join(SCRIPT_DIR, "invariants.json")

# Entries with sha256_pdf in invariants.json whose PDF path is implied by
# convention rather than stored as a "certificates/..." string in the tree.
HARDCODED = {
    "module_1":                     "certificates/Module_1_Certificate.pdf",
    "module_2":                     "certificates/Module_2_Certificate.pdf",
    "module_3":                     "certificates/Module_3_Certificate.pdf",
    "module_4":                     "certificates/Module_4_Certificate.pdf",
    "module_5":                     "certificates/Module_5_Certificate.pdf",
    "module_6":                     "certificates/Module_6_Certificate.pdf",
    "module_7":                     "certificates/Module_7_Certificate.pdf",
    "module_8":                     "certificates/Module_8_Certificate.pdf",
    "module_24":                    "certificates/Module_24_Certificate.pdf",
    "module_25":                    "certificates/Module_25_Certificate.pdf",
    "chronarithmetica":             "certificates/Chronarithmetica_Certificate.pdf",
    "module_26":                    "certificates/Module_26_Certificate.pdf",
    "z_tower_v3":                   "certificates/Z_Protocol_Tower_v3.pdf",
    "rh_tower":                     "certificates/RH_Tower_Certificate.pdf",
    "ms_tower":                     "certificates/MS_Tower_Certificate.pdf",
    "bands_269":                    "certificates/Bands_269_Certificate.pdf",
    "morningstar_engineering_spec": "certificates/MorningStar_Engineering_Spec_V1.pdf",
    # wall256 stores "Wall256_YM_Report.pdf" (no prefix) in the json;
    # the actual file lives under certificates/.
    "wall256_ym_report":            "certificates/Wall256_YM_Report.pdf",
}

# Root-level PDFs that are registered in invariants.json and are expected
# to live at the repo root (not under certificates/).
ROOT_PDFS = [
    "OperaNumerorum_Complete.pdf",
]


def collect_pdf_strings(obj, found=None):
    """Collect every string value ending in '.pdf' that starts with 'certificates/'."""
    if found is None:
        found = set()
    if isinstance(obj, str):
        if obj.endswith(".pdf") and obj.startswith("certificates/"):
            found.add(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            collect_pdf_strings(v, found)
    elif isinstance(obj, list):
        for item in obj:
            collect_pdf_strings(item, found)
    return found


def main():
    with open(INVARIANTS) as f:
        data = json.load(f)

    found = set()

    # Pass 1: generic scan — every "certificates/...pdf" string in the tree.
    collect_pdf_strings(data, found=found)

    # Pass 2: hardcoded supplement for sha256_pdf entries with no path string.
    for key, path in HARDCODED.items():
        if key in data and isinstance(data[key], dict) and "sha256_pdf" in data[key]:
            found.add(path)

    # Pass 3: known root-level expected PDFs.
    for path in ROOT_PDFS:
        found.add(path)

    for path in sorted(found):
        print(path)


if __name__ == "__main__":
    main()
