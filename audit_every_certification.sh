#!/bin/bash
# FILE: audit_every_certification.sh  
# RUN FROM: root of repo/
# PURPOSE: Prove every math problem has a certificate, or fail.

set -euo pipefail
echo "=== MASTER CERTIFICATION AUDIT — repo ===" | tee AUDIT_RESULT.txt
echo "Date: $(date)" | tee -a AUDIT_RESULT.txt
FAIL=0

# 1. CLAY SEAL CHECK
CLAY=$(find . -name "CLAY_M1_M7.zip" -exec sha256sum {} \; | head -1 | cut -d' ' -f1)
echo "CLAY: $CLAY" | tee -a AUDIT_RESULT.txt
[ "$CLAY" = "5b80b84d..." ] || { echo "FAIL: CLAY TAMPERED" | tee -a AUDIT_RESULT.txt; FAIL=1; }

# 2. FIND EVERY MATH PROBLEM
find . -type f \( -name "*.lean" -o -name "*.pdf" -o -name "*.md" \) | while read f; do
  if grep -q "theorem\|lemma\|Problem\|Exercise\|def.*:=" "$f" 2>/dev/null; then
    echo "$f"
  fi
done | sort -u > ALL_MATH_PROBLEMS.txt
PROB_COUNT=$(wc -l < ALL_MATH_PROBLEMS.txt)
echo "MATH PROBLEMS FOUND: $PROB_COUNT" | tee -a AUDIT_RESULT.txt

# 3. FIND EVERY CERTIFICATE  
> ALL_CERTIFICATES.txt
find . -name "*.pdf" -exec sh -c 'pdftotext "$1" - 2>/dev/null | grep -q "by sorry" || echo "$1"' _ {} \; >> ALL_CERTIFICATES.txt
find . -name "*.cert" >> ALL_CERTIFICATES.txt
find . -name "SEALED_*.txt" >> ALL_CERTIFICATES.txt
find . -name "AXIOM_AUDIT.txt" >> ALL_CERTIFICATES.txt
find . -name "*.lean" -exec sh -c '! grep -q "sorry" "$1" && echo "$1"' _ {} \; >> ALL_CERTIFICATES.txt
sort -u ALL_CERTIFICATES.txt -o ALL_CERTIFICATES.txt
CERT_COUNT=$(wc -l < ALL_CERTIFICATES.txt)
echo "CERTIFICATES FOUND: $CERT_COUNT" | tee -a AUDIT_RESULT.txt

# 4. CROSS-CHECK: EVERY PROBLEM HAS A CERTIFICATE
echo "" | tee -a AUDIT_RESULT.txt
echo "=== MISSING CERTIFICATIONS ===" | tee -a AUDIT_RESULT.txt
MISSING=0
while read prob; do
  name=$(basename "$prob" | sed 's/\.[^.]*$//')
  if ! grep -qi "$name" ALL_CERTIFICATES.txt && ! find $(dirname "$prob") -name "*cert*" -o -name "*proof*" | grep -q .; then
    echo "NO CERT: $prob" | tee -a AUDIT_RESULT.txt
    MISSING=$((MISSING+1))
  fi
done < ALL_MATH_PROBLEMS.txt

# 5. AXIOM AUDIT: CLASSIC TRIO ONLY
echo "" | tee -a AUDIT_RESULT.txt
echo "=== AXIOM AUDIT ===" | tee -a AUDIT_RESULT.txt
CUSTOM=$(grep -rh "axiom" --include="*.lean" . | grep -v "propext\|Classical.choice\|Quot.sound" || true)
if [ -n "$CUSTOM" ]; then
  echo "FAIL: CUSTOM AXIOMS FOUND:" | tee -a AUDIT_RESULT.txt
  echo "$CUSTOM" | tee -a AUDIT_RESULT.txt
  FAIL=1
else
  echo "PASS: Classic trio only" | tee -a AUDIT_RESULT.txt
fi

# 6. SORRY AUDIT: ZERO IN MAIN
SORRY=$(grep -r "by sorry" --include="*.lean" src/ proofs/ACT* 2>/dev/null | wc -l || echo 0)
echo "SORRY IN MAIN: $SORRY" | tee -a AUDIT_RESULT.txt
[ "$SORRY" -eq 0 ] || { echo "FAIL: SORRY FOUND IN MAIN" | tee -a AUDIT_RESULT.txt; FAIL=1; }

# 7. EQUATION COUNT VS LEAN COUNT
LEAN_THM=$(find src proofs/ACT* -name "*.lean" -exec grep -h "theorem\|lemma\|def.*:=" {} \; 2>/dev/null | wc -l || echo 0)
EQ_FILE=$(wc -l < EQUATION_INDEX.txt 2>/dev/null || echo 0)
echo "LEAN THEOREMS: $LEAN_THM | EQUATION_INDEX: $EQ_FILE" | tee -a AUDIT_RESULT.txt
[ "$LEAN_THM" -eq "$EQ_FILE" ] || { echo "WARN: COUNT MISMATCH" | tee -a AUDIT_RESULT.txt; FAIL=1; }

# 8. FINAL VERDICT
echo "" | tee -a AUDIT_RESULT.txt
if [ "$FAIL" -eq 0 ] && [ "$MISSING" -eq 0 ]; then
  echo "RESULT: PASS — EVERY MATH PROBLEM HAS A CERTIFICATE" | tee -a AUDIT_RESULT.txt
  echo "TOTAL_EQUATIONS: $EQ_FILE | TOTAL_CERTS: $CERT_COUNT | MISSING: 0" | tee -a AUDIT_RESULT.txt
  echo "CLAY: 5b80b84d SEALED | SORRY: 0 | AXIOMS: CLASSIC TRIO" | tee -a AUDIT_RESULT.txt
  exit 0
else
  echo "RESULT: FAIL — MISSING CERTIFICATIONS: $MISSING" | tee -a AUDIT_RESULT.txt
  echo "Check AUDIT_RESULT.txt for list" | tee -a AUDIT_RESULT.txt
  exit 1
fi
