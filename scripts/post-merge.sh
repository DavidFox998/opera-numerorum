#!/bin/bash
set -e
pnpm install --frozen-lockfile
pnpm --filter db push

# Guard against silent Lean proof drift. Fails the merge if `lean-proof/**`
# changed in a way that breaks the axiom-debt check or leaves VERIFY.txt stale.
# When `lake` is unavailable the check prints a visible warning and exits 0
# so merges aren't blocked in environments without a Lean toolchain.
./scripts/check-lean-proof.sh
