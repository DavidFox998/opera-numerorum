---
name: BDP kappa formula
description: How kappa = 4.8433014197780389 is derived — NOT from the speed of light
---

## Rule
kappa = phi(143) * c_lemma / 1e10

where:
- phi(143) = Euler totient of 143 = (11-1)*(13-1) = 120 (exact, computed with uint64_t)
- c_lemma = 403608451.6483666 (Lemma 4.1 conductor normalization constant, NOT the speed of light in m/s)
- 1e10 is the normalization divisor (equivalently: phi(143) * (c_lemma/100) / 1e8)

The C source is bin/print_kappa.c. It uses 80-bit long double (64-bit mantissa) which
gives kappa = 4.8433014197780389 (certified in m2.out SHA 3716c7db...).

**Why:** The comment "phi(N) * c / 1e8" in print_kappa.c is misleading — "c" is c_lemma,
not the speed of light. A different constant c_lemma/100 = 4036084.5164816990832151 is
used in the normalized form. Both are equivalent by the 1e8 vs 1e10 divisor swap.

**How to apply:** When any script or theorem references kappa, always use the certified
m2.out value 4.8433014197780389 directly rather than recomputing from c_lemma,
to avoid 80-bit long-double precision differences (which can shift k_bridge by ~5000).
