#!/usr/bin/env bash
# verify_github_push.sh -- Post-push self-check for opera-numerorum
#
# Confirms that the most recent push to GitHub is accessible:
#   1. Commit SHA is reachable via the GitHub API
#   2. Z_Protocol_Tower_v3.pdf returns HTTP 200 on raw.githubusercontent.com
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
# CHECK 2: Z_Protocol_Tower_v3.pdf returns HTTP 200
# ---------------------------------------------------------------------------
echo "-- CHECK 2: Z_Protocol_Tower_v3.pdf accessible"
PDF_URL="${RAW_BASE}/certificates/Z_Protocol_Tower_v3.pdf"
PDF_STATUS=$(http_status "$PDF_URL")
if [ "$PDF_STATUS" = "200" ]; then
    ok "Z_Protocol_Tower_v3.pdf HTTP ${PDF_STATUS}"
else
    fail "Z_Protocol_Tower_v3.pdf HTTP ${PDF_STATUS}  (${PDF_URL})"
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
