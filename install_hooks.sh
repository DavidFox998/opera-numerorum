#!/bin/bash
# Opera Numerorum -- install git hooks from hooks/
#
# Run once after cloning (or after pulling a new hook template):
#   bash install_hooks.sh

set -e

HOOKS_SRC="hooks"
HOOKS_DST=".git/hooks"

if [ ! -d "$HOOKS_DST" ]; then
    echo "ERROR: $HOOKS_DST not found. Are you in the repo root?"
    exit 1
fi

for hook in "$HOOKS_SRC"/*; do
    name="$(basename "$hook")"
    dest="$HOOKS_DST/$name"
    cp "$hook" "$dest"
    chmod +x "$dest"
    echo "Installed: $dest"
done

echo ""
echo "All hooks installed. Run 'git commit' to verify."
