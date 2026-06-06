#!/usr/bin/env bash
# release.sh -- Opera Numerorum full-release alias
#
# Sequences all four release steps in order:
#   1. verify_all.sh          -- SHA chain verification + field report
#   2. push_to_github.sh      -- push public opera-numerorum repo
#   3. push_morning_star.sh   -- push private morningstar_spacecraft repo
#   4. generate_firewall_report.py -- rebuild CMI referee firewall report
#
# Writes a timestamped entry to RELEASE_LOG.txt after each run.
# Exits 0 only when all four steps pass.
#
# Usage:
#   export GITHUB_PAT=<your_token>
#   bash release.sh
#
# Flags:
#   --no-push     Skip both push steps (verify + firewall report only)
#   --no-firewall Skip the firewall report rebuild
#   --dry-run     Print what would run; execute nothing

set -euo pipefail

# ── parse flags ───────────────────────────────────────────────────────────────
NO_PUSH=0
NO_FIREWALL=0
DRY_RUN=0

for arg in "$@"; do
    case "$arg" in
        --no-push)     NO_PUSH=1 ;;
        --no-firewall) NO_FIREWALL=1 ;;
        --dry-run)     DRY_RUN=1 ;;
        *)
            echo "Unknown flag: $arg" >&2
            echo "Usage: bash release.sh [--no-push] [--no-firewall] [--dry-run]" >&2
            exit 1
            ;;
    esac
done

WORKSPACE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RELEASE_LOG="$WORKSPACE_DIR/RELEASE_LOG.txt"
RELEASE_TS=$(date +"%Y-%m-%d %H:%M:%S UTC" --utc 2>/dev/null || date +"%Y-%m-%d %H:%M:%S")

STEP_VERIFY="SKIPPED"
STEP_GITHUB="SKIPPED"
STEP_MORNINGSTAR="SKIPPED"
STEP_FIREWALL="SKIPPED"
COMMIT_GITHUB=""
COMMIT_MORNINGSTAR=""

SEP="========================================================================"
SEP2="------------------------------------------------------------------------"

echo ""
echo "$SEP"
echo "  Opera Numerorum -- Full Release"
echo "  $RELEASE_TS"
echo "$SEP"
echo ""

if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY RUN] Would execute:"
    echo "  1. bash verify_all.sh"
    if [ "$NO_PUSH" -eq 0 ]; then
        echo "  2. bash push_to_github.sh"
        echo "  3. bash push_morning_star.sh"
    else
        echo "  2. push_to_github.sh     [SKIPPED: --no-push]"
        echo "  3. push_morning_star.sh  [SKIPPED: --no-push]"
    fi
    if [ "$NO_FIREWALL" -eq 0 ]; then
        echo "  4. python3 generate_firewall_report.py"
    else
        echo "  4. generate_firewall_report.py  [SKIPPED: --no-firewall]"
    fi
    echo ""
    echo "No actions taken (--dry-run)."
    exit 0
fi

# ── Step 1: verify_all.sh ─────────────────────────────────────────────────────
echo "$SEP2"
echo "STEP 1/4 -- SHA chain verification + field report (verify_all.sh)"
echo "$SEP2"
set +e
bash "$WORKSPACE_DIR/verify_all.sh"
VERIFY_EXIT=$?
set -e

if [ "$VERIFY_EXIT" -eq 0 ]; then
    STEP_VERIFY="PASS"
    echo ""
    echo "STEP 1: PASS"
else
    STEP_VERIFY="FAIL (exit $VERIFY_EXIT)"
    echo ""
    echo "STEP 1: FAIL (exit $VERIFY_EXIT) -- SHA chain broken or field report failed."
    echo "        Aborting release. Fix verify_all.sh errors before pushing."
    # Write partial log entry and exit
    {
        echo ""
        echo "[$RELEASE_TS]"
        echo "  STEP 1 verify_all.sh    : $STEP_VERIFY"
        echo "  STEP 2 push_to_github   : ABORTED"
        echo "  STEP 3 push_morning_star: ABORTED"
        echo "  STEP 4 firewall_report  : ABORTED"
        echo "  OVERALL                 : FAIL"
    } >> "$RELEASE_LOG"
    echo ""
    echo "Partial release log appended to: $RELEASE_LOG"
    exit 1
fi

echo ""

# ── Step 2: push_to_github.sh ─────────────────────────────────────────────────
echo "$SEP2"
echo "STEP 2/4 -- Push public opera-numerorum repo (push_to_github.sh)"
echo "$SEP2"

if [ "$NO_PUSH" -eq 1 ]; then
    echo "SKIPPED (--no-push)"
    STEP_GITHUB="SKIPPED"
else
    set +e
    GITHUB_OUT=$(bash "$WORKSPACE_DIR/push_to_github.sh" 2>&1)
    GITHUB_EXIT=$?
    set -e
    echo "$GITHUB_OUT"

    if [ "$GITHUB_EXIT" -eq 0 ]; then
        STEP_GITHUB="PASS"
        COMMIT_GITHUB=$(echo "$GITHUB_OUT" | grep "Commit SHA" | awk '{print $NF}' || true)
        echo ""
        echo "STEP 2: PASS  (commit: ${COMMIT_GITHUB:-unknown})"
    else
        STEP_GITHUB="FAIL (exit $GITHUB_EXIT)"
        echo ""
        echo "STEP 2: FAIL -- push_to_github.sh exited $GITHUB_EXIT"
        echo "        Continuing to morning star push..."
    fi
fi

echo ""

# ── Step 3: push_morning_star.sh ──────────────────────────────────────────────
echo "$SEP2"
echo "STEP 3/4 -- Push private morningstar_spacecraft repo (push_morning_star.sh)"
echo "$SEP2"

if [ "$NO_PUSH" -eq 1 ]; then
    echo "SKIPPED (--no-push)"
    STEP_MORNINGSTAR="SKIPPED"
else
    set +e
    MS_OUT=$(bash "$WORKSPACE_DIR/push_morning_star.sh" 2>&1)
    MS_EXIT=$?
    set -e
    echo "$MS_OUT"

    if [ "$MS_EXIT" -eq 0 ]; then
        STEP_MORNINGSTAR="PASS"
        COMMIT_MORNINGSTAR=$(echo "$MS_OUT" | grep "Commit SHA" | awk '{print $NF}' || true)
        echo ""
        echo "STEP 3: PASS  (commit: ${COMMIT_MORNINGSTAR:-unknown})"
    else
        STEP_MORNINGSTAR="FAIL (exit $MS_EXIT)"
        echo ""
        echo "STEP 3: FAIL -- push_morning_star.sh exited $MS_EXIT"
        echo "        Continuing to firewall report..."
    fi
fi

echo ""

# ── Step 4: generate_firewall_report.py ───────────────────────────────────────
echo "$SEP2"
echo "STEP 4/4 -- Rebuild CMI referee firewall report (generate_firewall_report.py)"
echo "$SEP2"

if [ "$NO_FIREWALL" -eq 1 ]; then
    echo "SKIPPED (--no-firewall)"
    STEP_FIREWALL="SKIPPED"
else
    set +e
    python3 "$WORKSPACE_DIR/generate_firewall_report.py"
    FIREWALL_EXIT=$?
    set -e

    if [ "$FIREWALL_EXIT" -eq 0 ]; then
        STEP_FIREWALL="PASS"
        echo ""
        echo "STEP 4: PASS"
    else
        STEP_FIREWALL="FAIL (exit $FIREWALL_EXIT)"
        echo ""
        echo "STEP 4: FAIL -- generate_firewall_report.py exited $FIREWALL_EXIT"
    fi
fi

echo ""

# ── Summary ───────────────────────────────────────────────────────────────────
echo "$SEP"
echo "  RELEASE SUMMARY -- $RELEASE_TS"
echo "$SEP"
echo "  STEP 1  verify_all.sh          : $STEP_VERIFY"
echo "  STEP 2  push_to_github.sh      : $STEP_GITHUB"
if [ -n "$COMMIT_GITHUB" ]; then
    echo "          opera-numerorum commit : $COMMIT_GITHUB"
fi
echo "  STEP 3  push_morning_star.sh   : $STEP_MORNINGSTAR"
if [ -n "$COMMIT_MORNINGSTAR" ]; then
    echo "          morningstar commit     : $COMMIT_MORNINGSTAR"
fi
echo "  STEP 4  firewall_report.py     : $STEP_FIREWALL"

# Determine overall pass/fail
OVERALL="PASS"
for STATUS in "$STEP_VERIFY" "$STEP_GITHUB" "$STEP_MORNINGSTAR" "$STEP_FIREWALL"; do
    if [[ "$STATUS" == FAIL* ]]; then
        OVERALL="FAIL"
        break
    fi
done

echo ""
echo "  OVERALL                        : $OVERALL"
echo "$SEP"
echo ""

# ── Append to release log ──────────────────────────────────────────────────────
{
    echo ""
    echo "[$RELEASE_TS]"
    echo "  STEP 1 verify_all.sh    : $STEP_VERIFY"
    echo "  STEP 2 push_to_github   : $STEP_GITHUB"
    if [ -n "$COMMIT_GITHUB" ]; then
        echo "         opera-numerorum  : $COMMIT_GITHUB"
    fi
    echo "  STEP 3 push_morning_star: $STEP_MORNINGSTAR"
    if [ -n "$COMMIT_MORNINGSTAR" ]; then
        echo "         morningstar      : $COMMIT_MORNINGSTAR"
    fi
    echo "  STEP 4 firewall_report  : $STEP_FIREWALL"
    echo "  OVERALL                 : $OVERALL"
} >> "$RELEASE_LOG"

echo "Release log appended to: $RELEASE_LOG"
echo ""

if [ "$OVERALL" = "FAIL" ]; then
    exit 1
fi
