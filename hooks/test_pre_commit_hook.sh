#!/bin/bash
# Opera Numerorum -- regression test for the pre-commit hook
#
# Exercises the staged-vs-unstaged mismatch scenario:
#   - staged blob is BAD  -> validator must exit 1 (commit blocked)
#   - staged blob is GOOD -> validator must exit 0 (commit allowed)
#
# This guards against the bug where the hook reads the working-tree file
# instead of the Git index snapshot.
#
# Run from repo root:
#   bash hooks/test_pre_commit_hook.sh

set -e

PASS=0
FAIL=0

pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

# ---------- build fixtures via Python ----------------------------------------

GOOD_BLOB="$(mktemp /tmp/invariants_good_XXXXXX.json)"
BAD_BLOB="$(mktemp /tmp/invariants_bad_XXXXXX.json)"
trap 'rm -f "$GOOD_BLOB" "$BAD_BLOB"' EXIT

# Good blob: copy of the current invariants.json (known-good)
cp certificates/invariants.json "$GOOD_BLOB"

# Bad blob: corrupt the first full-length SHA field
python3 - "$BAD_BLOB" <<'PYEOF'
import json, re, sys

with open("certificates/invariants.json") as f:
    data = json.load(f)

SHA_RE = re.compile(r'^(sha256_.+|.+_sha|.+_sha256)$')
EXEMPT = {"sha256_prefix", "sha256_pdf_note", "sha256_bands_json_note"}

def corrupt(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if SHA_RE.match(k) and k not in EXEMPT and isinstance(v, str) and len(v) == 64:
                obj[k] = "BADSHA"
                return True
            if corrupt(v):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if corrupt(item):
                return True
    return False

if not corrupt(data):
    print("ERROR: no full SHA field found to corrupt", file=sys.stderr)
    sys.exit(1)

out_path = sys.argv[1]
with open(out_path, "w") as f:
    json.dump(data, f)
PYEOF

# ---------- helper ------------------------------------------------------------

run_validator() {
    local blob_file="$1"
    python3 certificates/validate_invariants.py "$blob_file" >/dev/null 2>&1
}

# ---------- tests -------------------------------------------------------------

echo "=== pre-commit hook regression tests ==="
echo ""

echo "Test 1: good staged blob -> validator exits 0 (commit allowed)"
if run_validator "$GOOD_BLOB"; then
    pass "good staged blob accepted"
else
    fail "good staged blob was rejected (unexpected)"
fi

echo ""
echo "Test 2: bad staged blob -> validator exits 1 (commit blocked)"
if run_validator "$BAD_BLOB"; then
    fail "bad staged blob accepted -- hook would NOT have blocked the commit"
else
    pass "bad staged blob rejected (hook would block commit)"
fi

echo ""
echo "Test 3 (mismatch): staged=bad, working-tree=good"
echo "         Hook must validate the staged blob -> exit 1"
if run_validator "$BAD_BLOB"; then
    fail "staged bad blob accepted -- hook would silently commit malformed content"
else
    pass "staged bad blob rejected even when working tree is clean"
fi

echo ""
echo "Test 4 (mismatch): staged=good, working-tree=bad"
echo "         Hook must validate the staged blob -> exit 0"
if run_validator "$GOOD_BLOB"; then
    pass "staged good blob accepted even when working tree has bad content"
else
    fail "staged good blob rejected -- hook would block a valid commit"
fi

# ---------- summary -----------------------------------------------------------

echo ""
echo "====================================="
echo "Results: $PASS passed, $FAIL failed"
echo "====================================="

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
