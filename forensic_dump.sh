#!/usr/bin/env bash
# FULL FORENSIC DUMP — runs durably as a workflow (no 2-min shell cap).
# Honest deviations from the literal request, forced by the environment:
#   * manifest uses one `find -printf` process (the scripted per-file `ls -la`
#     would fork ~161k subprocesses); same fields, nothing filtered.
#   * archive uses zstd -T0 (gzip cannot finish ~9-10GB inside any single
#     shell step); NO repo content is excluded.
#   * the only things kept OUT of the tar are the generated output artifacts
#     themselves (the tar, the 3GB bundle which is a redundant copy of .git,
#     the live log + done-marker) — excluding outputs from themselves, not content.
set -uo pipefail
cd /home/runner/workspace

LOG=forensic_dump.log
: > "$LOG"
rm -f FORENSIC_DONE FORENSIC_FAILED

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
say() { echo "[$(ts)] $*" | tee -a "$LOG"; }

TAR=TheoremaAureum143_EVERYTHING_2026-06-03.tar.zst
BUNDLE=TheoremaAureum143_FULL_HISTORY_2026-06-03.bundle
MANIFEST=FORENSIC_MANIFEST_2026-06-03.txt
GITLOG=GIT_HISTORY_2026-06-03.txt

say "FORENSIC DUMP START"

# 0. clean stale lock from the previously killed bundle
rm -f "$BUNDLE".lock "$BUNDLE" "$TAR" "$TAR".sha512 "$BUNDLE".sha512 2>/dev/null
say "cleared stale lock / prior partial outputs"

# 1. MANIFEST (full tree, single process)
say "manifest: building full file tree ..."
{
  echo "FORENSIC_MANIFEST_2026-06-03"
  echo "Date: $(ts)"
  echo "Contents: COMPLETE REPO + .git + .local + .lake + node_modules + all hidden files (NO content exclusions)"
  echo "Purpose: Full migration + preservation"
  echo "Workspace root: /home/runner/workspace"
  echo "METHOD NOTE: per-file listing produced by ONE 'find -printf' process"
  echo "  (fields: perms owner group size mtime path). The scripted"
  echo "  'find -exec ls -la {} ;' would fork ~161k subprocesses and exceed every"
  echo "  shell time limit; this is the same data, faster. Nothing filtered."
  echo ""
  echo "=== FULL FILE TREE (every file, no exclusions) ==="
} > "$MANIFEST"
find . -type f -printf '%M %u %g %10s %TY-%Tm-%Td %TH:%TM %p\n' >> "$MANIFEST" 2>/dev/null
say "manifest: $(wc -l < "$MANIFEST") lines"

# 2. GIT HISTORY graph (all branches)
say "git log --all --oneline --graph ..."
git --no-optional-locks log --all --oneline --graph > "$GITLOG" 2>&1
say "git history: $(wc -l < "$GITLOG") lines"

# 3. GIT BUNDLE — complete history, every branch
say "git bundle create --all (this is the ~3GB step) ..."
if git --no-optional-locks bundle create "$BUNDLE" --all >> "$LOG" 2>&1; then
  say "bundle done: $(ls -la "$BUNDLE" | awk '{print $5}') bytes"
else
  say "ERROR: git bundle failed"; touch FORENSIC_FAILED; exit 1
fi

# 4. TAR EVERYTHING via zstd -T0, written directly to the workspace disk
#    (/tmp has a ~3GB quota; workspace has 200G+ free). The tar excludes itself
#    by name to avoid self-inclusion.
say "tar everything via zstd -T0 -> workspace ..."
rm -f "$TAR"
if tar -I 'zstd -T0 -3' \
      --exclude="./$TAR" \
      --exclude="./$BUNDLE" \
      --exclude="./$LOG" \
      --exclude=./FORENSIC_DONE \
      --exclude=./FORENSIC_FAILED \
      -cf "./$TAR" -C /home/runner/workspace . >> "$LOG" 2>&1; then
  say "tar done: $(ls -la "$TAR" | awk '{print $5}') bytes"
else
  rc=$?
  # tar exit 1 = "some files differ/changed" (harmless warnings); 2 = fatal
  if [ "$rc" = "1" ] && [ -f "./$TAR" ]; then
    say "tar finished with warnings (rc=1, benign file-changed); kept: $(ls -la "$TAR" | awk '{print $5}') bytes"
  else
    say "ERROR: tar failed rc=$rc"; rm -f "./$TAR"; touch FORENSIC_FAILED; exit 1
  fi
fi

# 5. SHA512 SEALS
say "sha512 seals ..."
sha512sum "$TAR" > "$TAR".sha512
sha512sum "$BUNDLE" > "$BUNDLE".sha512
say "seals written"

# 6. HANDOFF SUMMARY
HANDOFF=FORENSIC_HANDOFF_2026-06-03.txt
{
  echo "=== FORENSIC DUMP COMPLETE — $(ts) ==="
  echo "Workspace: /home/runner/workspace"
  echo ""
  echo "Deliverables:"
  echo "1. $TAR"
  echo "2. $TAR.sha512"
  echo "3. $BUNDLE"
  echo "4. $BUNDLE.sha512"
  echo "5. $MANIFEST"
  echo "   (+ $GITLOG, + this handoff)"
  echo ""
  echo "Sizes:"
  ls -la "$TAR" "$TAR".sha512 "$BUNDLE" "$BUNDLE".sha512 "$MANIFEST" "$GITLOG"
  echo ""
  echo "SHA512:"
  cat "$TAR".sha512 "$BUNDLE".sha512
  echo ""
  echo "=== MIGRATION / RESTORE INSTRUCTIONS ==="
  echo "Archive is zstd-compressed (gzip cannot finish ~9-10GB in one shell step here)."
  echo "1. Verify seals:   sha512sum -c $TAR.sha512 $BUNDLE.sha512"
  echo "2. Extract all:    tar --use-compress-program=unzstd -xf $TAR"
  echo "                   (or: zstd -d $TAR -o ${TAR%.zst} && tar -xf ${TAR%.zst})"
  echo "3. The extracted tree already contains a complete .git (all branches/blame),"
  echo "   so it IS a working clone. The separate bundle is an independent copy of"
  echo "   the full history; restore it with:"
  echo "      git clone $BUNDLE restored_repo"
  echo ""
  echo "=== HONESTY NOTES (items in the original request that do NOT exist on disk) ==="
  echo "The following were named in the dump request but are ABSENT from the workspace,"
  echo "so they are not (and cannot be) in this archive — nothing was fabricated to fill them:"
  echo "  - Besel_I/ (or any *esel* directory)"
  echo "  - symmetry_error_rate.csv (or any *.csv matching it)"
  echo "  - Towers/YM/0S/ namespace / a real T_0S transfer operator"
  echo "  - a '661 bricks' set, a 'phase shift event' file, or a 'CANCELLED state' artifact"
  echo "The archive contains exactly what is really on disk: the actual Towers/ Lean"
  echo "sources (including the 13 YM/OS witness-collapse modules now OPEN), .git, .local,"
  echo ".lake, node_modules, docs, reports, and all hidden files."
  echo "=== DONE ==="
} > "$HANDOFF" 2>&1
cat "$HANDOFF" | tee -a "$LOG"

say "FORENSIC DUMP COMPLETE"
touch FORENSIC_DONE
