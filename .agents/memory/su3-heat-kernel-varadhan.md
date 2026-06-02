---
name: SU(3) heat-kernel envelope — Varadhan honesty trap
description: which YM heat-kernel small-t/large-t bounds are TRUE, FALSE, or OPEN in this tower; stops re-attempting a provably-false bridge.
---

# SU(3) heat-kernel envelope: what's true, false, and open

The YM tower's `Heat_kernel_envelope_real t := ∑'(m,n) (dim)²·exp(-t·C₂)`
(`Towers/YM/PeterWeylHeat.lean`) is the heat kernel **at the identity**
(diagonal). Recurring requests ask to bound it by `C·e^{-(c/t)}/t⁴` with
`c>0` ("Varadhan/Molchanov"). That bound is **mathematically FALSE for small
t** — do not attempt to prove it, and do not accept a task premise that says
it's "almost done" or "90% green."

**Why false:** at the diagonal the geodesic distance is 0, so the Varadhan
factor `e^{-d(x,y)²/(4t)}` is `e^0 = 1`. The true small-t behavior is pure
polynomial blow-up `K_t(1) ~ C·t^{-d/2} = C·t^{-4}` (d=dim SU(3)=8), i.e.
LHS→+∞ as t→0⁺. But `C·e^{-c/t}/t⁴ → 0` as t→0⁺ (sub s=1/t: s⁴e^{-cs}→0).
So for small t, LHS > RHS. No `c>0` works. The `e^{-c/t}` factor is an
OFF-diagonal (x≠y) phenomenon only.

**Two regimes don't mix:**
- small-t (t→0⁺): honest shape is `≤ C/t⁴`, NO exponential. TRUE and **PROVEN**
  (trio-only, sorry-free) — see below.
- large-t (t→∞): governed by the **spectral gap** = min non-trivial Casimir;
  decay is `e^{-(minC₂)·t}`, never `e^{-c/t}`.

**Small-t poly bound IS PROVEN — do NOT re-derive.** `Towers/YM/HeatTraceBound.lean`
proves `heat_trace_poly_bound : ∃C>0, ∀t∈Ioc 0 1, K t ≤ C·t^(-4)` AND the
named-object corollary `heat_envelope_small_t : ∃C>0, ∀t∈Ioo 0 1,
Heat_kernel_envelope_real t ≤ C·t^(-4)` (bridged by `K t =
Heat_kernel_envelope_real t`). Both classical-trio, NOT bricks. The mathlib
`∑'poly·e^{-t·quad} ≤ C·t⁻ᵏ` gap is CLOSED in-tower via: degree-7 antidiagonal
envelope (dim is degree 3 ⟹ dim² degree 6, +1 antidiagonal multiplicity ⟹ k⁷;
any "dim²≤K(m+n)⁴" premise is off by two powers), `gaussian_moment_7`
(∫₀^∞x⁷e^{-ax²}=3/a⁴ via `integral_rpow_mul_exp_neg_mul_rpow`+Γ(4)=6),
`y⁵e^{-y}≤120` (`Real.pow_div_factorial_le_exp` n=5), split at N=⌊1/√t⌋+2
(head ≤64N⁸ via exp≤1; tail via telescoping ∑1/(k+N)³). It is an UPPER bound
only — no matching lower bound / optimality is claimed; NOT a mass gap, NOT
Varadhan. YM stays Open.

**Spectral gap (provable, trio-only, landed in `Towers/YM/CasimirGap.lean`):**
`Casimir_SU3_explicit (m,n) = m²+n²+mn+3m+3n = 3·C₂`; min over `(m,n)≠(0,0)`
is `4` (true units `C₂=4/3`), saturated at the fundamental `(1,0)`/`(0,1)`.
This is the LARGE-t rate, NOT the small-t constant the Varadhan target wanted.

**Known-FALSE bridge (already removed once):** `Weyl_sum_explicit_SU3_real t N
≤ Heat_kernel_def_real t` where `Heat_kernel_def_real t = e^{-1/t}/t⁴`
(placeholder `heat_decay_constant:=1`). False at N=0,t=1: LHS=1, RHS≈0.368.
The honest landed bridge targets `Heat_kernel_envelope_real` (the genuine
tsum) via `Summable.sum_le_tsum`, NOT `Heat_kernel_def_real`. The Varadhan
asymptotic remains the genuine OPEN gap that would advance YM past Open.
