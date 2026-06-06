#!/bin/bash
# Battle Plan v1.6 - Master Manifest
# Exits 1 if any SHA mismatch

set -e

# --- Pre-flight: verify all stdout SHAs recorded in invariants.json ---
echo "=== invariants.json SHA pre-flight ==="
python3 certificates/check_invariants.py
echo ""

declare -A SHAS=(
  [m1.out]="63ef870a78766619327e99b68683bceff8c8ef9a525298756c77c8378fd2c291"
  [m2.out]="3716c7dbb32524074b8fffb65eea45069c8b568a31dc73706405116b84029a83"
  [m3.out]="e687bb09a55e4eda198d4c5b24d03b7579f93bba27184a61fec7cbe29a83d044"
  [m4.out]="b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed"
  [m5.out]="9df98a3970acbb6942770a6cdd42fb21b009f9a5f45a222dd963e98ba4cb7a13"
  [m6.out]="ec9fa8c3aad478312c7e0d7373904dc3407eb5e9f4c19a011e3ca2ccb84da9fb"
)

i=1
for file in m1.out m2.out m3.out m4.out m5.out m6.out; do
  echo -n "[$i/6] $file SHA: ${SHAS[$file]}... "
  echo "${SHAS[$file]}  $file" | sha256sum -c --status
  echo "PASS"
  ((i++))
done

echo ""
echo "Concatenating 6 outputs..."
MANIFEST_SHA=$(cat m1.out m2.out m3.out m4.out m5.out m6.out | sha256sum | awk '{print $1}')
echo "$MANIFEST_SHA  (M1-M6 manifest)"
echo ""
echo "All 6 modules verified. DAG intact. MANIFEST LOCKED."
echo ""

# --- Field Report pre-flight checks ---
FIELD_REPORT_SCRIPT="certificates/build_field_report.py"
FIELD_REPORT_ASSETS="attached_assets"
FIELD_REPORT_SKIP=0

echo "=== Field Report pre-flight ==="
if [ ! -f "$FIELD_REPORT_SCRIPT" ]; then
  echo "WARNING: $FIELD_REPORT_SCRIPT not found -- skipping field report build."
  FIELD_REPORT_SKIP=1
fi
if [ ! -d "$FIELD_REPORT_ASSETS" ]; then
  echo "WARNING: $FIELD_REPORT_ASSETS/ directory not found -- skipping field report build."
  FIELD_REPORT_SKIP=1
fi
if ! python3 -c "import reportlab" 2>/dev/null; then
  echo "WARNING: Python package 'reportlab' is not installed -- skipping field report build."
  echo "         Install with: pip install reportlab"
  FIELD_REPORT_SKIP=1
fi

if [ "$FIELD_REPORT_SKIP" -eq 0 ]; then
  echo "Pre-flight OK. Proceeding with field report build."
  echo ""
  echo "=== Rebuilding Field Report variants ==="
  set +e
  bash make_field_report.sh
  FIELD_REPORT_EXIT=$?
  set -e
  if [ "$FIELD_REPORT_EXIT" -ne 0 ]; then
    echo ""
    echo "WARNING: make_field_report.sh exited with code $FIELD_REPORT_EXIT -- field report may be incomplete."
    FIELD_REPORT_SKIP=1
  fi
else
  echo "Field report step skipped."
fi

echo ""
echo "=== Full chain summary ==="
for file in m1.out m2.out m3.out m4.out m5.out m6.out; do
  echo "  $file  $(sha256sum "$file" | awk '{print $1}')"
done
echo "  manifest      $MANIFEST_SHA"
SHA_1PP=$(sha256sum certificates/Field_Report_1pp.pdf 2>/dev/null | awk '{print $1}')
SHA_2PP=$(sha256sum certificates/Field_Report_2pp.pdf 2>/dev/null | awk '{print $1}')
echo "  FR-1pp        ${SHA_1PP:-<not built>}"
echo "  FR-2pp        ${SHA_2PP:-<not built>}"

if [ "$FIELD_REPORT_SKIP" -ne 0 ]; then
  echo ""
  echo "EXIT 1: Field report step was skipped or failed (M1-M6 chain is intact)."
  exit 1
fi
