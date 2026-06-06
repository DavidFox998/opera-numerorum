#!/usr/bin/env bash
# push_to_github.sh -- Opera Numerorum public repo (opera-numerorum)
#
# Pushes ONLY the certified mathematical content.
# Excluded from this push (live in morningstar_spacecraft instead):
#   MORNING_STAR_REPO/   MORNING_STAR_STAGE/   M_DRAFT/   M_FINAL/
# HISTORICAL/ at the workspace root is included in BOTH repos.
#
# Uses a clean temp-directory export so exclusions are guaranteed
# regardless of workspace git state.

set -euo pipefail

GITHUB_USER="DavidFox998"
GITHUB_REPO="opera-numerorum"
BRANCH="main"

WORKSPACE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "${GITHUB_PAT:-}" ]; then
    echo "ERROR: GITHUB_PAT environment variable is not set." >&2
    echo "Set it with:  export GITHUB_PAT=<your_personal_access_token>" >&2
    exit 1
fi

REMOTE_URL="https://${GITHUB_USER}:${GITHUB_PAT}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

EXPORT_DIR=$(mktemp -d)
trap 'rm -rf "$EXPORT_DIR"' EXIT

echo "==> Assembling clean export (excluding Morning Star content) ..."
cd "$WORKSPACE_DIR"
tar -cf - \
    --exclude='./.git' \
    --exclude='./MORNING_STAR_REPO' \
    --exclude='./MORNING_STAR_STAGE' \
    --exclude='./M_DRAFT' \
    --exclude='./M_FINAL' \
    --exclude='./node_modules' \
    --exclude='./.pnpm-store' \
    --exclude='./__pycache__' \
    --exclude='./.local' \
    --exclude='./artifacts' \
    --exclude='./lib' \
    --exclude='./scripts' \
    --exclude='./CLAY_REPO.tar.gz' \
    --exclude='./MORNING_STAR_REPO.tar.gz' \
    --exclude='./certificates/OperaNumerorum_AllCerts.zip' \
    --exclude='./certificates/Opera_Numerorum_All_Certs_2026_06_04.zip' \
    --exclude='./certificates/MorningStar_Complete_2026_06_04.zip' \
    . | tar -xf - -C "$EXPORT_DIR"

echo "==> Initializing git in export directory ..."
cd "$EXPORT_DIR"
git init -q
git config user.name  "David Fox"
git config user.email "david@opera-numerorum"
git add -A

COMMIT_DATE=$(date +"%Y-%m-%d")
git commit -q -m "Opera Numerorum -- ${COMMIT_DATE}

Certified mathematical chain: M1-M7 manifest, RH/BSD/NS/MS/PvsNP towers.
Clay seal (frozen): 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9
Morning Star engineering content lives in separate private repo (morningstar_spacecraft).
Author: David J. Fox | ORCID 0009-0008-1290-6105"

echo "==> Pushing to github.com/${GITHUB_USER}/${GITHUB_REPO} (--force) ..."
git remote add origin "$REMOTE_URL"
if git push --force -u origin "$BRANCH"; then
    LOCAL_SHA=$(git rev-parse HEAD)
    echo ""
    echo "SUCCESS: branch '${BRANCH}' pushed to GitHub."
    echo "  Commit SHA : ${LOCAL_SHA}"
    echo "  URL        : https://github.com/${GITHUB_USER}/${GITHUB_REPO}/commit/${LOCAL_SHA}"
    echo ""
    echo "NOTE: Morning Star content (MORNING_STAR_REPO/ MORNING_STAR_STAGE/ M_DRAFT/ M_FINAL/)"
    echo "      was NOT pushed here. Run push_morning_star.sh for that repo."
else
    echo "" >&2
    echo "FAILED: git push exited non-zero. Check the error above." >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Post-push self-check (skipped with SKIP_VERIFY=1)
# ---------------------------------------------------------------------------
if [ "${SKIP_VERIFY:-0}" != "1" ]; then
    VERIFY_SCRIPT="${WORKSPACE_DIR}/verify_github_push.sh"
    if [ -x "$VERIFY_SCRIPT" ]; then
        echo "==> Running post-push verification ..."
        # GitHub's API may take a few seconds to index a fresh force-push.
        sleep 5
        bash "$VERIFY_SCRIPT" "$LOCAL_SHA" || {
            echo "" >&2
            echo "WARNING: Post-push verification reported failures." >&2
            echo "         The push itself succeeded; run verify_github_push.sh manually to re-check." >&2
            # Do not exit non-zero here — the push completed; verification is advisory.
        }
    else
        echo "NOTE: verify_github_push.sh not found or not executable; skipping post-push check."
    fi
fi
