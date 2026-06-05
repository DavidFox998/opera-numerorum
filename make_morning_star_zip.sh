#!/usr/bin/env bash
# make_morning_star_zip.sh
# Opera Numerorum -- Rebuild MorningStar_Complete_2026_06_04.zip from the
# canonical file list in one step.  To add a new PDF, append it to FILES below.
#
# Usage:
#   bash make_morning_star_zip.sh
#
# Output:
#   certificates/MorningStar_Complete_2026_06_04.zip  (overwritten)
#   SHA-256 printed to stdout and recorded in certificates/invariants.json

set -e

CERT="certificates"
OUT="$CERT/MorningStar_Complete_2026_06_04.zip"
INVARIANTS="$CERT/invariants.json"

# -----------------------------------------------------------------------
# Canonical file list.  All paths are relative to $CERT/.
# To add a file: append one line here; nothing else needs to change.
# -----------------------------------------------------------------------
FILES=(
    # Field Report variants (three layouts)
    Field_Report_Morningstar.pdf
    Field_Report_1pp.pdf
    Field_Report_2pp.pdf

    # Friends & Family summary
    FriendsFamily_MorningStar.pdf

    # Morning Star module certificates (M8 series)
    Module_M8A_Audit.pdf
    Module_M8C_ZoeMstar.pdf
    Module_M8D_Resonator.pdf
    Module_M8F_LeanProtocol.pdf
    Module_M8G_Provenance.pdf
    Module_M8G_Correction.pdf
    Module_M8H_G_Amplifier.pdf
    Module_M8I_Wormhole.pdf
    Module_M8J_OQ2_Closure.pdf
    Module_M8K_FTL_Morningstar.pdf
    Module_M8L_MorningStar_Ops.pdf
    Module_M8M_MorningStar_Physics.pdf
    Module_M8N_EEQC_v14.pdf
    Module_M8O_L5_Gates.pdf
    Module_M8P_L6_Clock.pdf
    Module_M8Q_L7_System.pdf

    # Module 24 certificate (H4 Refraction Map)
    Module_24_Certificate.pdf

    # Engineering summary
    MorningStar_Engineering_Summary.pdf
)

# -----------------------------------------------------------------------
# Pre-flight: confirm every listed file exists before touching the ZIP.
# -----------------------------------------------------------------------
echo "=== Pre-flight check ==="
MISSING=0
for f in "${FILES[@]}"; do
    if [ ! -f "$CERT/$f" ]; then
        echo "MISSING  $CERT/$f"
        MISSING=$((MISSING + 1))
    else
        echo "OK       $CERT/$f"
    fi
done

if [ "$MISSING" -gt 0 ]; then
    echo ""
    echo "ERROR: $MISSING file(s) missing -- ZIP not rebuilt."
    exit 1
fi

# -----------------------------------------------------------------------
# Build the ZIP with Python's zipfile (always available; no zip binary needed).
# Files are stored with bare filenames, no directory prefix.
# -----------------------------------------------------------------------
echo ""
echo "=== Building $OUT ==="

# Pass the file list to Python via a newline-delimited string.
FILE_LIST=$(printf "%s\n" "${FILES[@]}")

python3 - <<PYEOF
import zipfile, os, hashlib, sys

cert_dir = "$CERT"
out_path = "$OUT"
files    = """$FILE_LIST""".strip().splitlines()

with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for name in files:
        src = os.path.join(cert_dir, name)
        zf.write(src, arcname=name)
        print(f"  added  {name}")

size = os.path.getsize(out_path)
with open(out_path, "rb") as fh:
    sha = hashlib.sha256(fh.read()).hexdigest()

print(f"\nSHA-256 : {sha}")
print(f"Size    : {size} bytes  ({size // 1024 // 1024} MB approx)")
print(f"Files   : {len(files)}")

# Write results to a temp file so the shell can read them back.
with open("/tmp/_ms_zip_result.txt", "w") as tmp:
    tmp.write(f"{sha}\n{size}\n{len(files)}\n")
PYEOF

# Read results back for the invariants update.
SHA=$(sed -n '1p' /tmp/_ms_zip_result.txt)
SIZE=$(sed -n '2p' /tmp/_ms_zip_result.txt)
NFILES=$(sed -n '3p' /tmp/_ms_zip_result.txt)

# -----------------------------------------------------------------------
# Update invariants.json
# -----------------------------------------------------------------------
echo ""
echo "=== Updating $INVARIANTS ==="
python3 - <<PYEOF
import json, datetime

path = "$INVARIANTS"
with open(path) as f:
    inv = json.load(f)

inv["bundle_morning_star"] = {
    "description": (
        "Morning Star complete bundle: all Morning Star PDFs + engineering summary"
        " + field reports (includes Field_Report_Morningstar.pdf,"
        " Field_Report_1pp.pdf, Field_Report_2pp.pdf)."
    ),
    "file": "MorningStar_Complete_2026_06_04.zip",
    "sha256": "$SHA",
    "size_bytes": int("$SIZE"),
    "file_count": int("$NFILES"),
    "generated_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "builder": "make_morning_star_zip.sh",
}

with open(path, "w") as f:
    json.dump(inv, f, indent=2)

print("invariants.json updated.")
PYEOF

echo ""
echo "=== Done ==="
echo "$OUT"
echo "SHA-256 : $SHA"
