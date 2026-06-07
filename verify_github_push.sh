#!/usr/bin/env bash
# verify_github_push.sh -- Post-push self-check for opera-numerorum
#
# Confirms that the most recent push to GitHub is accessible:
#   1. Commit SHA is reachable via the GitHub API
#   2. Every module certificate PDF returns HTTP 200 on raw.githubusercontent.com
#      (list derived from certificates/invariants.json via list_expected_pdfs.py)
#   3. certificates/invariants.json is accessible at HEAD
#
# Usage (standalone):
#   export GITHUB_PAT=<token>
#   bash verify_github_push.sh <commit_sha>
#
# When called from push_to_github.sh the SHA is passed automatically.
# Exits 0 only when ALL checks pass.

set -euo pipefail

GITHUB_USER="DavidFox998"
GITHUB_REPO="opera-numerorum"
BRANCH="main"

RAW_BASE="https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/${BRANCH}"
API_BASE="https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}"

COMMIT_SHA="${1:-}"

PASS=0
FAIL=0

ok()   { echo "  [PASS] $*"; PASS=$((PASS+1)); }
fail() { echo "  [FAIL] $*"; FAIL=$((FAIL+1)); }

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
http_status() {
    # Returns the HTTP status code for a URL.
    # Passes Authorization header when GITHUB_PAT is available.
    local url="$1"
    if [ -n "${GITHUB_PAT:-}" ]; then
        curl -s -o /dev/null -w "%{http_code}" \
             -H "Authorization: Bearer ${GITHUB_PAT}" \
             --max-time 20 \
             "$url"
    else
        curl -s -o /dev/null -w "%{http_code}" \
             --max-time 20 \
             "$url"
    fi
}

api_get() {
    local url="$1"
    if [ -n "${GITHUB_PAT:-}" ]; then
        curl -s \
             -H "Authorization: Bearer ${GITHUB_PAT}" \
             -H "Accept: application/vnd.github+json" \
             --max-time 20 \
             "$url"
    else
        curl -s \
             -H "Accept: application/vnd.github+json" \
             --max-time 20 \
             "$url"
    fi
}

echo ""
echo "==> verify_github_push.sh  (repo: ${GITHUB_USER}/${GITHUB_REPO}  branch: ${BRANCH})"
echo ""

# ---------------------------------------------------------------------------
# CHECK 1: Commit SHA is reachable
# ---------------------------------------------------------------------------
echo "-- CHECK 1: Commit SHA reachable"
if [ -z "$COMMIT_SHA" ]; then
    fail "No commit SHA provided. Pass SHA as first argument."
else
    RESPONSE=$(api_get "${API_BASE}/commits/${COMMIT_SHA}")
    REMOTE_SHA=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sha',''))" 2>/dev/null || true)
    if [ "${REMOTE_SHA}" = "${COMMIT_SHA}" ]; then
        ok "SHA ${COMMIT_SHA:0:16}... confirmed on GitHub"
    else
        # Try fetching the branch HEAD and compare
        BRANCH_RESPONSE=$(api_get "${API_BASE}/branches/${BRANCH}")
        BRANCH_SHA=$(echo "$BRANCH_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('commit',{}).get('sha',''))" 2>/dev/null || true)
        if [ "${BRANCH_SHA}" = "${COMMIT_SHA}" ]; then
            ok "SHA ${COMMIT_SHA:0:16}... confirmed as branch HEAD"
        else
            fail "SHA ${COMMIT_SHA:0:16}... not found (branch HEAD=${BRANCH_SHA:0:16}...)"
        fi
    fi
fi

# ---------------------------------------------------------------------------
# CHECK 2: Every module certificate PDF returns HTTP 200
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDF_LIST_SCRIPT="${SCRIPT_DIR}/certificates/list_expected_pdfs.py"

echo "-- CHECK 2: All certificate PDFs accessible on raw.githubusercontent.com"

if ! command -v python3 &>/dev/null; then
    fail "python3 not found -- cannot build PDF list"
else
    # Build the list of expected PDF paths (repo-relative).
    mapfile -t PDF_PATHS < <(python3 "$PDF_LIST_SCRIPT" 2>/dev/null)
    PDF_COUNT="${#PDF_PATHS[@]}"

    if [ "$PDF_COUNT" -eq 0 ]; then
        fail "list_expected_pdfs.py returned no paths -- check invariants.json"
    else
        echo "     Checking ${PDF_COUNT} PDFs in parallel (max 20 concurrent)..."

        # Temp directory for per-file result files.
        TMPDIR_PDF=$(mktemp -d)
        trap 'rm -rf "$TMPDIR_PDF"' EXIT

        # Semaphore: keep at most MAX_JOBS background jobs running.
        MAX_JOBS=20
        running=0

        check_one_pdf() {
            local rel_path="$1"
            local url="${RAW_BASE}/${rel_path}"
            local status
            if [ -n "${GITHUB_PAT:-}" ]; then
                status=$(curl -s -o /dev/null -w "%{http_code}" \
                              -H "Authorization: Bearer ${GITHUB_PAT}" \
                              --max-time 15 \
                              "$url")
            else
                status=$(curl -s -o /dev/null -w "%{http_code}" \
                              --max-time 15 \
                              "$url")
            fi
            echo "${status} ${rel_path}"
        }
        export -f check_one_pdf
        export GITHUB_PAT RAW_BASE

        # Run checks with bounded parallelism.
        for rel_path in "${PDF_PATHS[@]}"; do
            # Slot the task into a result file named after the index.
            result_file="${TMPDIR_PDF}/$(echo "$rel_path" | tr '/' '_').result"
            check_one_pdf "$rel_path" > "$result_file" &
            running=$((running + 1))
            if [ "$running" -ge "$MAX_JOBS" ]; then
                wait -n 2>/dev/null || wait
                running=$((running - 1))
            fi
        done
        wait  # drain remaining jobs

        # Tally results — accumulate directly into PASS/FAIL (no double-add).
        # Print [PASS]/[FAIL] per file for full traceability.
        PDF_FAIL=0
        PDF_PASS=0
        for rel_path in "${PDF_PATHS[@]}"; do
            result_file="${TMPDIR_PDF}/$(echo "$rel_path" | tr '/' '_').result"
            if [ -f "$result_file" ]; then
                read -r status name < "$result_file"
                if [ "$status" = "200" ]; then
                    echo "  [PASS] ${name}  HTTP 200"
                    PDF_PASS=$((PDF_PASS + 1))
                    PASS=$((PASS + 1))
                else
                    echo "  [FAIL] ${name}  HTTP ${status}"
                    PDF_FAIL=$((PDF_FAIL + 1))
                    FAIL=$((FAIL + 1))
                fi
            else
                echo "  [FAIL] ${rel_path}  (no result file)"
                PDF_FAIL=$((PDF_FAIL + 1))
                FAIL=$((FAIL + 1))
            fi
        done

        echo "     --- ${PDF_PASS} passed, ${PDF_FAIL} failed (${PDF_COUNT} checked) ---"
    fi
fi

# ---------------------------------------------------------------------------
# CHECK 3: certificates/invariants.json accessible at HEAD
# ---------------------------------------------------------------------------
echo "-- CHECK 3: certificates/invariants.json accessible"
INV_URL="${RAW_BASE}/certificates/invariants.json"
INV_STATUS=$(http_status "$INV_URL")
if [ "$INV_STATUS" = "200" ]; then
    ok "certificates/invariants.json HTTP ${INV_STATUS}"
else
    fail "certificates/invariants.json HTTP ${INV_STATUS}  (${INV_URL})"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "==> Results: ${PASS} PASS  |  ${FAIL} FAIL"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "VERIFICATION FAILED -- ${FAIL} check(s) did not pass." >&2
    exit 1
else
    echo "VERIFICATION PASSED -- all checks confirmed on GitHub."
    exit 0
fi
