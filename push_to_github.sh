#!/usr/bin/env bash
# push_to_github.sh -- Opera Numerorum public repo (opera-numerorum)
#
# Pushes ONLY the certified mathematical content via GitHub Git Tree API.
# No temp-directory disk usage -- avoids disk quota on large workspaces.
#
# Excluded from this push:
#   AUREUM_REPO/  AUREUM_STAGE/  M_DRAFT/  M_FINAL/  (Aureum content)
#   .cache/  .pythonlibs/  node_modules/  .pnpm-store/  (build infra)
#   attached_assets/  HISTORICAL/  .local/  artifacts/  lib/  scripts/
#   *.tar.gz  M_FINAL.zip  MORNING_STAR_REPO.tar.gz  (large archives)
#   certificates/OperaNumerorum_AllCerts.zip  (goes as release asset instead)
#
# Large ZIPs (>50MB) cannot be committed to the repo via API but ARE
# uploaded as GitHub release assets when --release is passed.
#
# Usage:
#   bash push_to_github.sh              # push only
#   bash push_to_github.sh --release    # push + create tag v1.6.0 + release assets
#   bash push_to_github.sh --dry-run    # list files without pushing
#   bash push_to_github.sh --release --tag v1.6.1   # custom tag

set -euo pipefail

WORKSPACE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "${GITHUB_PAT:-}" ]; then
    echo "ERROR: GITHUB_PAT environment variable is not set." >&2
    exit 1
fi

python3 "$WORKSPACE_DIR/push_to_github_api.py" "$@"
