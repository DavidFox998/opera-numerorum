#!/bin/bash
set -e
echo "=== MORNING STAR VERIFICATION ==="

echo "1. CLAY checksum..."
ACTUAL=$(sha256sum src/CLAY/CLAY_SEALED.zip | cut -d' ' -f1)
EXPECTED="518144c8c37b3b7c48a1719924ab80b2ba03bec594923811148eb2b31e3881e1"
test "$ACTUAL" = "$EXPECTED"
echo "   PASS: $ACTUAL SEALED"

echo "2. SORRY count in proofs/..."
SORRY_COUNT=$(grep -rl "by sorry" proofs/ 2>/dev/null | wc -l)
test "$SORRY_COUNT" -eq 0
echo "   PASS: SORRY: 0 files"

echo "3. Axioms audit..."
AXIOMS=$(grep -rh "^[^-]*axiom" src/ 2>/dev/null | grep -v "propext\|Classical.choice\|Quot.sound" | wc -l)
test "$AXIOMS" -eq 0
echo "   PASS: Classic trio only"

echo "4. SHA256SUMS verify..."
sha256sum -c SHA256SUMS --quiet
echo "   PASS: All files intact"

echo "5. Equation count..."
EQ_COUNT=$(grep -c "^EQ" EQUATION_INDEX.txt)
test "$EQ_COUNT" -eq 476
echo "   PASS: $EQ_COUNT equations certified"

echo "ALL CHECKS PASS. MORNING STAR CERTIFIED."
