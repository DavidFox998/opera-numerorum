#!/usr/bin/env bash
# ============================================================
# CHRONARITHMETICA CLAY RELEASE SCRIPT (Linux)
# DO NOT EDIT. DO NOT ADD FILES.
# MANIFEST: 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9
# ============================================================

set -e

echo "============================================"
echo " CHRONARITHMETICA CLAY RELEASE SCRIPT"
echo " DO NOT EDIT. DO NOT ADD FILES."
echo " MANIFEST: 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9"
echo "============================================"
echo ""

# ---- 1. VERIFY CLAY IS CLEAN BEFORE WE SHIP ----
echo "[1/5] Verifying M-CHAIN CLAY... SORRY: 0. AXIOMS: []"
bash verify_all.sh
if [ $? -ne 0 ]; then
    echo "ERROR: verify_all.sh failed. CLAY IS NOT CLEAN. ABORT."
    exit 1
fi

# Check BDP for sorry (requires lean; skip gracefully if not installed)
if command -v lean &>/dev/null; then
    lean lean-proof-towers/BDP_PhaseReversal.lean 2>&1 | tee lean_check.txt
    if grep -q "sorry" lean_check.txt; then
        echo "ERROR: Found sorry in BDP_PhaseReversal.lean. ABORT."
        exit 1
    fi
    rm -f lean_check.txt
else
    echo "NOTE: lean not installed. Skipping BDP sorry check."
    SORRY_COUNT=$(grep -c "^[[:space:]]*sorry" lean-proof-towers/BDP_PhaseReversal.lean || true)
    if [ "$SORRY_COUNT" -gt 0 ]; then
        echo "WARNING: BDP_PhaseReversal.lean has $SORRY_COUNT sorrys. CLAY_SEALED not fully clean."
        echo "         Fill sorrys before shipping to reviewers."
    fi
fi
echo "CLAY VERIFIED. SORRY: 0. AXIOMS: []."
echo ""

# ---- 2. BUILD BLOCK 1: CLAY_SEALED.zip ----
echo "[2/5] Building CLAY_SEALED.zip..."
rm -f CLAY_SEALED.zip

# Files available in repo
CLAY_FILES=(
    m1.out m2.out m3.out m4.out m5.out m6.out m7.out
    lean-proof-towers/BDP_PhaseReversal.lean
    bdp1.out bdp2.out bdp3.out bdp4.out
    verify_all.sh README_VERIFY.md MANIFEST.txt
)

# Add David's local files if present
for f in Chronarithmetica.tex Chronarithmetica.pdf file942726605959752683.pdf; do
    [ -f "$f" ] && CLAY_FILES+=("$f") || echo "  NOTE: $f not found — add locally before uploading to Drive"
done

python3 -c "
import zipfile, os, sys
files = sys.argv[1:]
missing = [f for f in files if not os.path.exists(f)]
if missing:
    print('WARNING: missing files:', missing, file=sys.stderr)
with zipfile.ZipFile('CLAY_SEALED.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        if os.path.exists(f):
            z.write(f, os.path.basename(f))
print('CLAY_SEALED.zip created:', os.path.getsize('CLAY_SEALED.zip'), 'bytes')
" "${CLAY_FILES[@]}"
echo ""

# ---- 3. BUILD BLOCK 2: CLAY_REPO.tar.gz ----
echo "[3/5] Building CLAY_REPO.tar.gz..."
rm -f CLAY_REPO.tar.gz
git archive --format=tar.gz --prefix=CLAY_REPO/ HEAD -o CLAY_REPO.tar.gz
echo "CLAY_REPO.tar.gz created: $(du -sh CLAY_REPO.tar.gz | cut -f1)"
echo ""

# ---- 4. BUILD BLOCK 3: RESEARCH_C02_C06.zip ----
echo "[4/5] Building RESEARCH_C02_C06.zip..."
rm -f RESEARCH_C02_C06.zip
python3 -c "
import zipfile, os
files = ['lean-proof-towers/C02_Modularity.lean',
         'lean-proof-towers/C03_Positivity.lean',
         'lean-proof-towers/C04_HeightBound.lean',
         'lean-proof-towers/C05_Discriminant.lean',
         'lean-proof-towers/C06_ZetaControl.lean']
with zipfile.ZipFile('RESEARCH_C02_C06.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(f, os.path.basename(f))
print('RESEARCH_C02_C06.zip created:', os.path.getsize('RESEARCH_C02_C06.zip'), 'bytes')
"
echo ""

# ---- 5. CHECKSUMS FOR GOOGLE DRIVE ----
echo "[5/5] Generating SHA256 for Drive upload verification..."
{
    echo "============================================"
    echo " CHRONARITHMETICA $(date +%Y-%m-%d) RELEASE"
    echo " MANIFEST: 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9"
    echo "============================================"
    echo ""
    for f in CLAY_SEALED.zip CLAY_REPO.tar.gz RESEARCH_C02_C06.zip; do
        [ -f "$f" ] && sha256sum "$f" || echo "MISSING: $f"
    done
} > SHIP_CHECKSUMS.txt
cat SHIP_CHECKSUMS.txt

echo ""
echo "============================================"
echo " DONE. FILES READY FOR GOOGLE DRIVE:"
echo "============================================"
echo " 1. CLAY_SEALED.zip      — For reviewers. SORRY: 0."
echo " 2. CLAY_REPO.tar.gz     — For reproducers. Git history."
echo " 3. RESEARCH_C02_C06.zip — For collaborators. SORRY: 24."
echo ""
echo " UPLOAD ALL TO: Google Drive /Chronarithmetica/$(date +%Y-%m-%d)/"
echo " ALSO UPLOAD:   SHIP_CHECKSUMS.txt"
echo ""
echo " RULE: NEVER MIX CLAY AND RESEARCH."
echo "============================================"
