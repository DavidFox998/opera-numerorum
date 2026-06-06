#!/usr/bin/env bash
set -euo pipefail

GITHUB_USER="DavidFox998"
GITHUB_REPO="opera-numerorum"
BRANCH="main"

if [ -z "${GITHUB_PAT:-}" ]; then
    echo "ERROR: GITHUB_PAT environment variable is not set." >&2
    echo "Set it with:  export GITHUB_PAT=<your_personal_access_token>" >&2
    exit 1
fi

REMOTE_URL="https://${GITHUB_USER}:${GITHUB_PAT}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

echo "==> Configuring remote origin ..."
if git remote get-url origin &>/dev/null; then
    git remote set-url origin "$REMOTE_URL"
else
    git remote add origin "$REMOTE_URL"
fi

echo "==> Ensuring branch is named '${BRANCH}' ..."
git branch -M "$BRANCH"

echo "==> Pushing to github.com/${GITHUB_USER}/${GITHUB_REPO} (--force) ..."
if git push --force -u origin "$BRANCH"; then
    LOCAL_SHA=$(git rev-parse HEAD)
    echo ""
    echo "SUCCESS: branch '${BRANCH}' pushed to GitHub."
    echo "  Commit SHA : ${LOCAL_SHA}"
    echo "  URL        : https://github.com/${GITHUB_USER}/${GITHUB_REPO}/commit/${LOCAL_SHA}"
else
    echo "" >&2
    echo "FAILED: git push exited non-zero. Check the error above." >&2
    exit 1
fi
