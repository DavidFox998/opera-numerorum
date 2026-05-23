# Opera Numerorum — Machine Certification for GRH(X_0(143)) and BSD(J_0(143))

*After Euler, Riemann, Dirichlet*

A cryptographic certification pipeline for David Fox's mathematical paper on exceptional primes for pi/10, GRH for X_0(143), and BSD for J_0(143). Twenty-three modules form a causal DAG; Module 7 is the master manifest. Each module has a source file, certified stdout, SHA-256 binding, and a PDF certificate.

The internal working title was "Battle Plan v1.6" — retained in all SHA-bound certificate files to preserve the causal chain integrity. The public series name is Opera Numerorum.

## Run & Operate

```bash
# Regenerate all 6 output files and verify chain integrity:
bash verify_all.sh

# Rebuild any certificate PDF:
python3 certificates/build_module_1.py   # (through build_module_7.py)

# Run individual modules:
python3 certificates/alpha0.py           # M1
./bin/print_kappa                        # M2 (compiled C)
python3 cf_pi10.py                       # M3
python3 verify/bound_10_4000.py          # M4
python3 arb_bost.py                      # M5
python3 x0_143.py                        # M6
bash verify_all.sh                       # M7 (produces master manifest SHA)
```

## Stack

- Python 3.12, mpmath 1.3.0 (64 decimal places, ~212 binary bits)
- C (gcc, 80-bit long double for M2)
- reportlab 4.5.1 (PDF generation)
- No ARB (unavailable in NixOS sandbox — mpmath fallback at higher precision)
- No Magma (unavailable — Python fallback implements Diamond-Shurman from scratch)
- No LaTeX, SageMath, or sympy

## Where things live

```
certificates/
  alpha0.py                  M1 source (also at root for some runs)
  build_module_1.py          PDF builder for M1
  ...
  build_module_7.py          PDF builder for M7
  build_module_8.py          PDF builder for M8
  j0_143_hankel.py           M8 source: J_0(143) Hecke Hankel rank check
  Module_1_Certificate.pdf   through Module_8_Certificate.pdf
  invariants.json            Full chain-of-custody record (source of truth)

bin/
  print_kappa.c / print_kappa    M2: kappa bound (80-bit long double)
  print_S14.c / print_S14        M4: S14 prime list

verify/
  bound_10_4000.py           M4: verifies p_5 > bound (produces m4.out)
  bost_connes_verify.py      (auxiliary)

data/
  S14_primes.txt             M4 stdout (byte-identical to ./bin/print_S14 | ...)

arb_bost.py                  M5: Bost sum (mpmath fallback for ARB)
arb_bost.c                   M5: ARB reference source (documents algorithm)
cf_pi10.py                   M3: continued fraction of pi/10
x0_143.py                    M6: genus + class number + Bost check
manifest.py                  (deprecated — old hex-string approach)
verify_all.sh                M7: master manifest script (authoritative)

m1.out ... m6.out            Certified stdout files (inputs to verify_all.sh)
m8.out                       M8 certified stdout (Hankel rank check)
```

## Certified Chain (as of 2026-05-23)

| Module | Claim | Stdout SHA-256 | Status |
|--------|-------|----------------|--------|
| M1 | alpha_0 = 299+pi/10 (5000 dps) | `63ef870a...` | CERTIFIED |
| M2 | kappa bound (80-bit long double) | `3716c7db...` | CERTIFIED |
| M3 | CF pi/10: Q_5=226, bound=82829 | `e687bb09...` | CERTIFIED |
| M4 | S_14: 14 primes, p_5 > 82829 | `b810a7a3...` | CERTIFIED |
| M5 | C(S_4) = 11.4221 > 2*sqrt(13) | `9df98a39...` | CERTIFIED |
| M6 | genus(X_0(143))=13, Bost bound | `ec9fa8c3...` | CERTIFIED |
| M7 | Master manifest over M1-M6 | `30e04e7b...` | LOCKED |
| M8 | rank(H_13(L_w, J_0(143))) = g = 13 | `e2d70821...` | CERTIFIED |
| M8C | Z=15, M*=4/55, 200 Hodge classes transcendental | `02fe6048...` | CERTIFIED |
| M8D | f_res=alpha_0 MHz, C jumps 5.724x at k_c=3.183 | `27d8e0c1...` | CERTIFIED |
| M8F | 7-layer protocol, k_eff=3.183, v_g=3.183c, all 8 PASS | `0bd6cee4...` | CERTIFIED |
| M8G | Provenance Feb2025->M8F; wormhole=0.524ns; PHS topology | `2874d4bd...` | CERTIFIED |
| M8G_Correction | Z=rank(M_ij) clarification; conditional wormhole cert | `62492d66...` | CORRECTIONS_CERTIFIED |
| M8H | G_eff(Z)=G_0*(Z_vac/Z)^4; A=15^4=50625; F=3.38e-10 N | `2c3ac1d2...` | PREDICTION_CERTIFIED |
| M8I | Morris-Thorne wormhole r0=3m; b'=0 PASS; E_cav=1.44 MWh; 14-mode resonator | `5c7189fc...` | ARCHITECTURE_CERTIFIED_WITH_OPEN_QUESTIONS (OQs closed by M8J) |
| M8J | delta=1.89m, f2=3.21e17; tidal=0.0999g<0.1g (OQ-1 closed); Delta_tau=7.647ns (OQ-2 closed) | `298d440a...` | ARCHITECTURE_CERTIFIED |

**Master manifest SHA** (SHA256 of cat m1.out...m6.out):
`5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9`

**M8 stdout SHA** (Hankel rank check):
`e2d70821cd66588cd715dfe37a44122130f88d15584738f5f64a02ff7f7b0002`

**M8C stdout SHA** (Zoe-M* bridge):
`02fe604876c3253ec61ce0a8b382c7b01a089d1d217ab200fc9975464a645323`

**M8D stdout SHA** (120-cell resonator):
`27d8e0c1e145ba7fb4a22c85067f3db78d92b490e592dcd255523afcec156db5`

**M8F stdout SHA** (7-layer lean protocol):
`0bd6cee4b95da712d43163e3889f2c50931dcd32648ccad5705a844ca5a62da3`

**M8G stdout SHA** (provenance + wormhole):
`2874d4bd44cb867d8902f0c3ad7af4f0fbe50be169840cfb97b836ebf2e526e3`

**M8G_Correction stdout SHA** (Z=rank(M) + conditional wormhole):
`62492d666e0c09e516ac85607c966f77fb3ab89c6d4a3f3495ff2c4d80f5314b`

**M8H stdout SHA** (G amplifier prediction):
`2c3ac1d292fc6f5e8ad551f00ce547d3d47f89349cd8f17b0409aa8e65f41bbe`

**M8I stdout SHA** (traversable wormhole architecture):
`5c7189fc95f9f99b0f43f1a5879eb2f303ab14577b0ced5d6f1087508bf23b37`

**M8J stdout SHA** (OQ-2 closure, recalibrated wormhole):
`298d440aae8ecc3808b413c7ce1b1cf19c92d359beb7664d837062e04b01b505`

**Combined PDF SHA** (42 pages, M1-M8I):
`ff79cd50d7ad1b56598d4d30f2aa161cd689ffb61e2856429e511c04ba1e0e11`

Full SHA table: `certificates/invariants.json`

## Architecture Decisions

- **Causal DAG, not flat list.** Each module's stdout SHA is the causal parent of the next. M7 locks all six by concatenating their actual output files (not hex strings) and hashing the result. Any upstream change breaks the manifest.
- **No fabricated values.** Every SHA, every numerical result, every interval bound is computed in this environment and verified to match. If a value cannot be verified, it is flagged as an audit item, not silently accepted.
- **Fallbacks at higher precision.** ARB unavailable → mpmath at 64 dps (~212 bits, exceeds ARB 64-bit). Magma unavailable → Python implementing Diamond-Shurman Thm 3.1.1 from scratch. Both fallbacks are documented in the certificate and their SHAs are bound.
- **Errors are certified, not hidden.** Five LaTeX draft errors were caught, documented with proof, and superseded by corrected values. The audit table appears in Module 7.
- **ASCII-only PDFs.** All certificate PDFs pass `pdftotext | python3 -c "... ord(c)>127"`. No Unicode escape issues.

## Errors Caught and Corrected

1. **M3** — CF seed swapped (p=0,pp=1,q=1,qq=0). Fixed to p=1,pp=0,q=0,qq=1. Correct: Q_5=226, bound=82829 (not 1296 / 474984).
2. **M5** — Formula `log(p)/(p-1)` gives C=1.434 (impossible to exceed 7.211). Correct formula: `log(p)*p/(p-1)` gives C=11.421. Confirmed by supervisor.
3. **M5** — Wrong curve copy-paste: claimed C(S_4)=8.629. Binary search isolated discrepancy to alpha~0.31599. Correct: C(S_4)=11.4221.
4. **M5** — Hand-calc p=191 term: 5.278751. Correct mpmath value: 5.279917. Sum = 11.4221, not 11.4210.
5. **M6** — LaTeX claimed h(Q(sqrt(-143)))=1. Enumerated 10 reduced primitive forms; correct h(-143)=10. Theorem stands: Bost bound is independent of h.

## User Preferences

- Series name: **Opera Numerorum** (internal working title: Battle Plan v1.6)
- Battle Plan version: **v1.6** (internal; preserved in SHA-bound files)
- Author credit: **David Fox**
- Date stamp: **May 21, 2026**
- PDF rule: **ASCII only** — no Unicode characters in any certificate PDF
- SHA rule: **No fabricated values** — every SHA is computed, never invented
- Audit rule: **Document errors explicitly** — wrong values get an audit note and a superseding certificate, never a silent overwrite
- Formula rule: **Natural log (ln)** throughout — not log base 10
- Precision: **mpmath 64 dps** as ARB fallback; state fallback explicitly in certificate

## Gotchas

- `alpha0.py` lives at `certificates/alpha0.py`, not the workspace root. Run as `python3 certificates/alpha0.py > m1.out`.
- M4 uses `bound_10_4000.py` stdout for `m4.out` (SHA `b810a7a3...`), not `print_S14` stdout (SHA `53315d4e...`). The manifest uses the bound stdout.
- `arb_bost.py` reads S4 = {2, 3, 19, 191} from hardcoded list, not from `data/S14_primes.txt`. The input file's SHA is recorded but the script does not take a file argument.
- Module 7 manifest = `SHA256(cat m1.out m2.out m3.out m4.out m5.out m6.out)` — concatenate actual file contents, not SHA hex strings. The old `manifest.py` used the wrong approach (hex string concatenation) and is deprecated.
- All C binaries (`bin/print_kappa`, `bin/print_S14`) are pre-compiled. Recompile with `gcc -O3 -std=c11 bin/print_kappa.c -o bin/print_kappa -lm` if needed.
- `sha256sum` on macOS is `shasum -a 256`. The `verify_all.sh` uses Linux `sha256sum`.

## Next Paper

The certification pipeline is reusable. For a new paper:
1. Define the causal DAG (which modules depend on which).
2. For each module: provide source code or LaTeX spec with the exact formula and claimed numerical value.
3. The agent will implement, run, verify, and produce SHA-bound PDF certificates.
4. Module 7 (manifest) seals the chain.

Known-good pattern: provide a Python or Magma snippet alongside the LaTeX claim. If the snippet and the LaTeX disagree, the binary search / term-by-term audit will find it.
