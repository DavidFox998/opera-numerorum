import Towers.YM.Wall261_H4Defect
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# Wall263 — H4 Coxeter matrix: `φ` is the EDGE WEIGHT, not the spectral radius

This brick is the HONEST response to the proposal to "restate Wall261 using the
H4 Coxeter matrix instead of the 120-cell 1-skeleton", with the requested
theorem

  *the largest eigenvalue of `2I − M_H4` equals `φ = 2cos(π/5)`.*

That theorem is FALSE, and this file machine-checks why, without introducing any
`axiom` (the footprint stays the classical trio).

## The matrix

`M_H4` is the H4 Cartan/Gram matrix, so its "off-diagonal" companion is the
weighted-path adjacency matrix

  `B := 2·I − M_H4 = !![0,1,0,0; 1,0,1,0; 0,1,0,φ; 0,0,φ,0]`,

i.e. the H4 Coxeter diagram `o—o—o—(5)—o` whose three edges carry the weights
`2cos(π/3)=1`, `2cos(π/3)=1`, `2cos(π/5)=φ`. So `φ` is the WEIGHT on the
label-`5` edge — it is *an entry of the matrix*, NOT a spectral quantity.

## What is actually true

**Honesty caveat on scope.** mathlib v4.12.0 has no `det_fin_four` and no
charpoly↔eigenvalue bridge, so this brick does NOT formalize the matrix `B`, its
determinant, or the equivalence "root of the char poly ↔ eigenvalue". It encodes
the *resulting* characteristic polynomial as the function `coxeterCharpoly`
(hand-computed below) and works at the polynomial level. The eigenvalue-level
readings ("`φ` is not an eigenvalue", "the largest is `2cos(π/30)`") are therefore
DOCUMENTARY consequences of that hand computation, NOT machine-checked here; what
is machine-checked is only the stated facts about `coxeterCharpoly` itself.

`B` is symmetric tridiagonal, so its characteristic polynomial is, by the
standard three-term determinant recursion (carried out by hand, not in Lean),

  `det(λ·I − B) = λ⁴ − (2 + φ²)·λ² + φ²`  ( = `coxeterCharpoly λ` below ).

Setting `x = λ²` and solving `x² − (2+φ²)x + φ² = 0` gives the four eigenvalues
`±2cos(π/30)` and `±2cos(11π/30)`. The LARGEST is `2cos(π/30) ≈ 1.989` — the H4
Coxeter number is `h = 30` and the Perron eigenvalue of a Coxeter diagram is
always `2cos(π/h)`. It is NOT `φ = 2cos(π/5) ≈ 1.618`.

In fact `φ` is not even an eigenvalue of `B`: evaluating the characteristic
polynomial at `λ = φ` gives `−φ² ≠ 0` (the quartic `φ⁴` cancels the `φ²·φ²`
term identically — `coxeterCharpoly_phi` is a pure `ring` identity, it does not
even use the golden-ratio relation). `φ = 2cos(π/5)` *is* genuinely the largest
eigenvalue of the UNWEIGHTED `4`-vertex path (the `A₄` diagram), but that is a
different matrix and is still not a KP "effective degree".

## Why this does not (and cannot) close the SU(2) gap

The Kotecký–Preiss convergence constant is the connective constant / max degree
of the polymer incidence graph (`6` for `ℤ⁴` links, `12` for the 600-cell), NOT
a sub-dominant eigenvalue `≈ 1.618`. Replacing "degree" by `φ` is the unproven
leap. We record the honest reduction `defect_bound_H4` as a CONDITIONAL
combinator over TWO NAMED-OPEN hypotheses (the effective-degree bound and the
weighted-KP combinator) — both ordinary Lean hypotheses, NOT `axiom`s, so no new
axioms enter the footprint. This file proves NO YM result; YM stays
`Status: Open`.

All public theorems are `sorry`-free and `#print axioms` = the classical trio.
-/

namespace TheoremaAureum.Towers.YM.Wall263

open Real

/-- The characteristic polynomial of the H4 Coxeter matrix
`B = 2I − M_H4 = !![0,1,0,0; 1,0,1,0; 0,1,0,φ; 0,0,φ,0]` (the weighted path with
edge weights `1, 1, φ`), hand-computed by the standard symmetric-tridiagonal
determinant recursion:
`det(λ·I − B) = λ⁴ − (2 + φ²)·λ² + φ²`. -/
noncomputable def coxeterCharpoly (lam : ℝ) : ℝ :=
  lam ^ 4 - (2 + Wall261.phi ^ 2) * lam ^ 2 + Wall261.phi ^ 2

/-- GENUINE/UNCONDITIONAL: evaluating the H4 Coxeter characteristic polynomial at
`λ = φ` yields `−φ²`. The quartic term `φ⁴` cancels against `φ²·φ²` **identically**
— this is a pure `ring` fact and does not even invoke the golden-ratio identity
`φ² = φ + 1`. -/
theorem coxeterCharpoly_phi : coxeterCharpoly Wall261.phi = -(Wall261.phi ^ 2) := by
  unfold coxeterCharpoly
  ring

/-- GENUINE/UNCONDITIONAL: `φ` is NOT a root of `coxeterCharpoly` (the
hand-computed H4 Coxeter characteristic polynomial): its value at `φ` is
`−φ² < 0`. Modulo that hand computation (the tridiagonal determinant recursion,
documented above, NOT re-derived in Lean — mathlib v4.12.0 has no
`det_fin_four`/charpoly↔eigenvalue bridge), this says `φ` is not an eigenvalue of
`2I − M_H4`, a fortiori not the largest, refuting "largest eigenvalue `= φ`". What
is machine-checked here is exactly `coxeterCharpoly φ ≠ 0`. -/
theorem phi_not_root : coxeterCharpoly Wall261.phi ≠ 0 := by
  rw [coxeterCharpoly_phi, neg_ne_zero]
  have h2 : 0 < Wall261.phi ^ 2 := by
    have := Wall261.phi_pos; nlinarith
  exact h2.ne'

/-- GENUINE/UNCONDITIONAL: `φ < 2`. Documentary context: the spectral radius of
`B` is the H4 Perron eigenvalue `2cos(π/30) ≈ 1.989`, which lies strictly between
`φ ≈ 1.618` and `2`; so the edge weight `φ` sits below the true spectral radius.
(No general "degree `≥ 2 ⟹` radius `≥ 2`" claim is made — that is FALSE, e.g. the
unweighted `A₄` path has max degree `2` and spectral radius exactly `φ < 2`.) What
is machine-checked here is only `φ < 2`. -/
theorem phi_lt_two : Wall261.phi < 2 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Wall261.sqrt_five_sq
  have hnn : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have hlt : Real.sqrt 5 < 3 := by nlinarith [h5, hnn]
  unfold Wall261.phi
  linarith

/-- GENUINE/UNCONDITIONAL: `1 < φ`. -/
theorem one_lt_phi : (1 : ℝ) < Wall261.phi := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Wall261.sqrt_five_sq
  have hnn : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have hgt : (1 : ℝ) < Real.sqrt 5 := by nlinarith [h5, hnn]
  unfold Wall261.phi
  linarith

/-- HONEST CONDITIONAL (axiom-free, classical trio): the H4 "Coxeter-input" defect
bound, the faithful transcription of `apply KP_theorem_weighted H4_spectral_bound`
WITHOUT any `axiom`. Both inputs are NAMED-OPEN ordinary hypotheses, proved
NOWHERE:

* `h_spec` — the H4 "effective degree" bound `EffDeg x ≤ φ` (this is exactly the
  unproven leap; the real KP constant is the connective constant `≥ 6`, not `φ`);
* `h_kp` — the weighted Kotecký–Preiss combinator turning that spectral input into
  the defect bound.

`a ≤ exp(−22/25)` is the activity-domain hypothesis (`0.88 = 22/25`), kept to
mirror the requested signature. Proves NO YM result. -/
theorem defect_bound_H4
    {Defect R EffDeg : ℝ → ℝ} {a : ℝ}
    (_ha : a ≤ Real.exp (-(22 / 25)))
    (h_spec : ∀ x, EffDeg x ≤ Wall261.phi)
    (h_kp : (∀ x, EffDeg x ≤ Wall261.phi) →
      Defect a ≤ Real.log (1 + Wall261.phi * R a)) :
    Defect a ≤ Real.log (1 + Wall261.phi * R a) :=
  h_kp h_spec

end TheoremaAureum.Towers.YM.Wall263
