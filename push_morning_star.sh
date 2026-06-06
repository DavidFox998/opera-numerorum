#!/usr/bin/env bash
# push_morning_star.sh -- Morning Star private repo (morningstar_spacecraft)
#
# Pushes ONLY the Morning Star engineering content:
#   MORNING_STAR_REPO/   MORNING_STAR_STAGE/   M_DRAFT/   M_FINAL/
# HISTORICAL/ at the workspace root is mirrored here (in BOTH repos).
#
# Uses a clean temp-directory export so only the above directories
# are visible in the private repo.

set -euo pipefail

GITHUB_USER="DavidFox998"
GITHUB_REPO="morningstar_spacecraft"
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

echo "==> Assembling Morning Star export ..."

for DIR in MORNING_STAR_REPO MORNING_STAR_STAGE M_DRAFT M_FINAL; do
    if [ -d "$WORKSPACE_DIR/$DIR" ]; then
        echo "    including $DIR/"
        tar -cf - -C "$WORKSPACE_DIR" \
            --exclude='./__pycache__' \
            --exclude='*/__pycache__' \
            "./$DIR" | tar -xf - -C "$EXPORT_DIR"
    else
        echo "    WARNING: $DIR/ not found in workspace, skipping"
    fi
done

if [ -d "$WORKSPACE_DIR/HISTORICAL" ]; then
    echo "    including HISTORICAL/ (mirrored)"
    tar -cf - -C "$WORKSPACE_DIR" ./HISTORICAL | tar -xf - -C "$EXPORT_DIR"
else
    echo "    WARNING: HISTORICAL/ not found at workspace root, skipping"
fi

cat > "$EXPORT_DIR/README.md" << 'EOF'
# morningstar_spacecraft

**Private** -- Morning Star Engineering / BDP Phase Reversal / P vs NP Tower

This repository contains the engineering and working-draft content for the
Opera Numerorum project. It is separate from the public opera-numerorum
repo to maintain the Clay referee firewall.

## Contents

| Directory | Contents |
|-----------|----------|
| MORNING_STAR_REPO/ | Full Morning Star repo (BDP, MS tower, Lean stubs) |
| MORNING_STAR_STAGE/ | Staging area for in-progress work |
| M_DRAFT/ | Draft PDFs and working certificates |
| M_FINAL/ | Finalized engineering PDFs |
| HISTORICAL/ | Historical essays (mirrored from opera-numerorum) |

## Firewall

The opera-numerorum repo (public) contains zero BDP/Morning Star content.
Sorry-isolation: BDP_PhaseReversal.lean (23 annotated sorry-fills, P vs NP Tower only)
lives here, not in the Clay submission scope (opera-numerorum/proofs/).

Clay seal (frozen): 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9

Author: David J. Fox | ORCID 0009-0008-1290-6105
Series: Opera Numerorum / Battle Plan v1.6
EOF

echo "==> Initializing git in export directory ..."
cd "$EXPORT_DIR"
git init -q
git config user.name  "David Fox"
git config user.email "david@opera-numerorum"
git add -A

COMMIT_DATE=$(date +"%Y-%m-%d")
git commit -q -m "Morning Star -- ${COMMIT_DATE}

BDP Phase Reversal, P vs NP Tower, Morning Star engineering.
HISTORICAL/ mirrored from opera-numerorum.
Clay seal (frozen): 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9
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
    echo "NOTE: Public mathematical chain (M1-M7, proofs/) is in opera-numerorum."
    echo "      Run push_to_github.sh for that repo."
else
    echo "" >&2
    echo "FAILED: git push exited non-zero. Check the error above." >&2
    exit 1
fi
