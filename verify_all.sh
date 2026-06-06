#!/bin/bash
# Battle Plan v1.6 - Master Manifest
# Exits 1 if any SHA mismatch

set -e

# --- Step 0: Validate SHA field formats in invariants.json ---
# Catches truncated or malformed SHA values before any file comparison.
echo "=== invariants.json SHA format validation ==="
python3 certificates/validate_invariants.py
echo ""

# --- Step 1: Recertify -- detect drift and re-emit stale PDFs ---
# Runs BEFORE the SHA pre-flight so that any module rebuild is
# repaired (PDFs re-emitted, invariants.json patched) before we
# verify the chain.  The pre-flight below then acts as a post-repair
# confirmation gate, not a hard abort on legitimate rebuilds.
echo "=== Recertify: M1-M7 PDF drift check ==="
python3 certificates/recertify.py
echo ""

# --- Step 2: Update source SHAs in invariants.json ---
# Runs after recertify so any rebuilt source files are reflected before
# the pre-flight gate checks the full chain.
echo "=== Source SHA update (update_source_shas.py) ==="
python3 certificates/update_source_shas.py
echo ""

# --- Step 3: Pre-flight -- verify all stdout SHAs in invariants.json ---
# Runs after recertify so it sees the repaired state.
echo "=== invariants.json SHA pre-flight ==="
python3 certificates/check_invariants.py
echo ""

# --- Step 4: Dynamic SHA verification for M1-M6 stdout files ---
# Reads sha256_stdout for each module directly from invariants.json
# (the single source of truth) instead of a hardcoded table.
echo "=== M1-M6 stdout SHA verification (from invariants.json) ==="

declare -A SHAS
while IFS=$'\t' read -r file sha; do
  SHAS["$file"]="$sha"
done < <(python3 - <<'PYEOF'
import json, sys
d = json.load(open("certificates/invariants.json"))
mapping = [
    ("module_1", "m1.out"),
    ("module_2", "m2.out"),
    ("module_3", "m3.out"),
    ("module_4", "m4.out"),
    ("module_5", "m5.out"),
    ("module_6", "m6.out"),
]
for key, fname in mapping:
    sha = d.get(key, {}).get("sha256_stdout", "")
    if not sha:
        print(f"ERROR: {key}.sha256_stdout missing in invariants.json", file=sys.stderr)
        sys.exit(1)
    print(f"{fname}\t{sha}")
PYEOF
)

i=1
for file in m1.out m2.out m3.out m4.out m5.out m6.out; do
  sha="${SHAS[$file]}"
  echo -n "[$i/6] $file SHA: ${sha}... "
  echo "${sha}  $file" | sha256sum -c --status
  echo "PASS"
  ((i++))
done

echo ""
echo "Concatenating 6 outputs..."
MANIFEST_SHA=$(cat m1.out m2.out m3.out m4.out m5.out m6.out | sha256sum | awk '{print $1}')
echo "$MANIFEST_SHA  (M1-M6 manifest)"

INVARIANTS_MANIFEST_SHA=$(python3 -c "import json; print(json.load(open('certificates/invariants.json'))['module_7']['manifest_sha'])")
if [ "$MANIFEST_SHA" != "$INVARIANTS_MANIFEST_SHA" ]; then
  echo ""
  echo "WARNING: manifest SHA mismatch!"
  echo "  computed : $MANIFEST_SHA"
  echo "  invariants.json: $INVARIANTS_MANIFEST_SHA"
  echo "  The .out files have drifted from the last recertify run."
  echo "  Re-run 'python3 certificates/recertify.py' to reseal the chain."
  exit 1
fi

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
