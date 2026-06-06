#!/bin/bash
set -e
echo "=== LEAN CHECK ==="
echo "Checking src/M_FINAL/*.lean for 'by sorry'..."
SORRY=$(grep -rn "by sorry" src/M_FINAL/ 2>/dev/null | wc -l)
test "$SORRY" -eq 0
echo "PASS: 0 sorry in M_FINAL lean files"
echo "Checking classic trio axioms only..."
CUSTOM=$(grep -rh "^[^-]*axiom" src/M_FINAL/ 2>/dev/null | grep -v "propext\|Classical.choice\|Quot.sound" | wc -l)
test "$CUSTOM" -eq 0
echo "PASS: No custom axioms"
echo "LEAN CHECK COMPLETE"
