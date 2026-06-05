# Opera Numerorum — Verification Instructions

**Author:** David Fox  
**Series:** Opera Numerorum (internal: Battle Plan v1.6)  
**Manifest SHA:** `5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9`  
**Date:** 2026-06-05

---

## Quick Verify (30 seconds)

```bash
bash verify_all.sh
```

Expected final line:
```
5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9  (M1-M6 manifest)
```

If you see a different SHA, the chain has been tampered with.

---

## Manual Verify (module by module)

```bash
sha256sum m1.out   # 63ef870a...
sha256sum m2.out   # 3716c7db...
sha256sum m3.out   # e687bb09...
sha256sum m4.out   # b810a7a3...
sha256sum m5.out   # 9df98a39...
sha256sum m6.out   # ec9fa8c3...
```

Manifest (M7):
```bash
cat m1.out m2.out m3.out m4.out m5.out m6.out | sha256sum
# 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9
```

---

## Reproduce from Source

Requirements: Python 3.12, mpmath 1.3.0, gcc

```bash
python3 certificates/alpha0.py > m1.out        # M1
./bin/print_kappa > m2.out                     # M2  (pre-compiled C)
python3 cf_pi10.py > m3.out                    # M3
python3 verify/bound_10_4000.py > m4.out       # M4
python3 arb_bost.py > m5.out                   # M5
python3 x0_143.py > m6.out                     # M6
cat m1.out m2.out m3.out m4.out m5.out m6.out | sha256sum   # M7
```

Recompile M2 if needed:
```bash
gcc -O3 -std=c11 bin/print_kappa.c -o bin/print_kappa -lm
```

---

## What Each Module Certifies

| Module | Claim | SHA-256 |
|--------|-------|---------|
| M1 | alpha_0 = 299 + pi/10 (5000 dps) | 63ef870a... |
| M2 | kappa bound (80-bit long double) | 3716c7db... |
| M3 | CF pi/10: Q_5=226, bound=82829 | e687bb09... |
| M4 | S_14: 14 primes, p_5 > 82829 | b810a7a3... |
| M5 | C(S_4) = 11.4221 > 2*sqrt(13) | 9df98a39... |
| M6 | genus(X_0(143))=13, Bost bound | ec9fa8c3... |
| M7 | Master manifest over M1-M6 | 5b80b84d... |

---

## CLAY Protocol

- M-chain (m1.out through m6.out): SORRY: 0. AXIOMS: [].
- All values computed, not assumed.
- Errors caught and certified: see Module 7 audit table.
- No LaTeX, no SageMath, no Magma required for verification.
- PDF certificates: `certificates/Module_*_Certificate.pdf`
