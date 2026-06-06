# Opera Numerorum — Morning Star Repository

*Machine Certification for GRH(X_0(143)) and BSD(J_0(143))*
*David J. Fox — ORCID 0009-0008-1290-6105 — davidjfox998@gmail.com*

## Verification (run from repo root)

```bash
bash tests/verify.sh
```

Expected output:
```
=== MORNING STAR VERIFICATION ===
1. CLAY checksum...
   PASS: 518144c8... SEALED
2. SORRY count in proofs/...
   PASS: SORRY: 0 files
3. Axioms audit...
   PASS: Classic trio only
4. SHA256SUMS verify...
   PASS: All files intact
5. Equation count...
   PASS: 476 equations certified
ALL CHECKS PASS. MORNING STAR CERTIFIED.
```

## CLAY Seal

| File | SHA-256 |
|------|---------|
| `src/CLAY/CLAY_SEALED.zip` | `518144c8c37b3b7c48a1719924ab80b2ba03bec594923811148eb2b31e3881e1` |
| M7 manifest (cat m1..m6.out) | `5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9` |

## Certified Chain

| Module | Claim | SHA | Status |
|--------|-------|-----|--------|
| M1 | alpha_0 = 299+pi/10 (5000 dps) | 63ef870a | CERTIFIED |
| M2 | kappa bound (80-bit long double) | 3716c7db | CERTIFIED |
| M3 | CF pi/10: Q_5=226, bound=82829 | e687bb09 | CERTIFIED |
| M4 | S_14: 14 primes, p_5 > 82829 | b810a7a3 | CERTIFIED |
| M5 | C(S_4) = 11.4221 > 2*sqrt(13) | 9df98a39 | CERTIFIED |
| M6 | genus(X_0(143))=13, Bost bound | ec9fa8c3 | CERTIFIED |
| M7 | Master manifest over M1-M6 | 5b80b84d | LOCKED |
| M8 | rank(H_13(J_0(143))) = 13 | e2d70821 | CERTIFIED |

## Axiom Policy

Classic trio ONLY: `propext`, `Classical.choice`, `Quot.sound`

```bash
grep -r "axiom" src/   # must output only the trio
```

## Stack

- Python 3.12, mpmath 1.3.0 (64 dps, ~212 bits)
- C (gcc, 80-bit long double for M2)
- reportlab 4.5.1 (PDF generation)
- Lean 4 (BDP_PhaseReversal.lean)
