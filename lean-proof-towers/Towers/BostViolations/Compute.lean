-- Axiom status: Uses [propext, Classical.choice, Quot.sound] (subset)
-- Scope: COMPUTABLE rational sanity-check of the Bost sum over the REAL
--        explicit prime set S_4. Proves NO theorem; asserts NO violation.
/-
================================================================
Towers / BostViolations / Compute — computable rational Bost-sum check
================================================================

**THIS FILE IS NOT A BRICK.** It is a COMPUTABLE (`#eval`-able) rational
sanity check that reproduces Module 5's numeric Bost sum `C(S_4) ≈ 11.42`
over the REAL, explicit 4-prime set `S_4 = {2,3,19,191}` (`Defs.S_4`), and
runs the Bost-bound test across the 12 documented CM curves
(`Twelve.ExceptionalSet₁₂`).

HONESTY NOTES — read before trusting any number printed here:

  * There is NO per-discriminant `α₀(d)` family. Battle Plan v1.6 (M1)
    defines ONE constant α₀ = 299 + π/10 (see `Defs.alpha_0`), used for the
    SINGLE exceptional set. The documents give the per-curve prime set `S_X`
    numerically only for `S_4` (M4/M5). So `S_of_curve` is the CONSTANT
    `Defs.S_4` for EVERY curve — there is no honest per-`d` prime data to
    encode, and fabricating 12 distinct sets/α₀'s is refused.
  * `ratLog` is a ROUNDED (3-dp) rational approximation of `Real.log`; `C_rat`
    is therefore an APPROXIMATION of the real Bost sum `Twelve.C`, for
    `#eval`/visualisation only. The CERTIFIED inequality `C(S_4) > 2√13` is
    Module 5's external `arb` certificate, NOT this `#eval`. The margin
    (≈ 11.42 vs ≈ 7.21) is far larger than the rounding error, so the test
    result does not depend on the rounding.
  * `BostViolations_12` is EXPECTED to be `[]` (no violations): the certified
    data only GROWS the Bost sum (C(S_4) ≈ 11.42, C(S_5) ≈ 40.4, both ≫ 2√13).
    A non-empty list would indicate a violation; under the real data there is
    none. This file asserts NO theorem either way — the violation conjecture
    `Twelve.TwelveViolation_Surface` stays OPEN and unasserted.

SORRY: 0. No `sorry`/`axiom`/`opaque`. Axioms: classical-trio subset.
-/
import Towers.Hodge.Twelve
import Towers.Hodge.Defs
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Finset.Sort
import Mathlib.Algebra.BigOperators.Group.Finset

namespace TheoremaAureum.Towers.BostViolations

open TheoremaAureum.Towers.Hodge.Twelve
open TheoremaAureum.Towers.Hodge.Defs
open BigOperators

/-- Rounded (3-dp) rational approximation of `Real.log n`, for the primes that
actually occur in `S_4` / `S_14`; coarse `Nat.log2` fallback otherwise.
APPROXIMATION ONLY — see file header. -/
def ratLog (n : ℕ) : ℚ :=
  if n = 2 then 693/1000
  else if n = 3 then 1099/1000
  else if n = 5 then 1609/1000
  else if n = 7 then 1946/1000
  else if n = 11 then 2398/1000
  else if n = 19 then 2944/1000
  else if n = 191 then 5252/1000
  else (Nat.log2 n : ℚ)

/-- Computable rational approximation of the Bost sum
`C(S) = Σ_{p∈S} log p · p/(p-1)` (`Twelve.C`), using `ratLog`. -/
def C_rat (S : Finset ℕ) : ℚ :=
  ∑ p in S, ratLog p * (p : ℚ) / ((p : ℚ) - 1)

/-- The Bost threshold `2√13 ≈ 7.2111`, as a rational approximation. -/
def bostThreshold : ℚ := 7211/1000

/-- The prime set attached to a curve. CONSTANT `Defs.S_4` for every curve:
the documents give `S_X` numerically only for `S_4`; there is NO per-`d` prime
data (see file header). The unused argument is explicit `_X`. -/
def S_of_curve (_X : CM_Curve) : Finset ℕ := S_4

/-- The 12 documented CM curves as a COMPUTABLE list, derived from the real
`Twelve.exceptional_12` via `Finset.sort` (ascending). `Finset.toList` is
noncomputable in mathlib v4.12.0, so we sort to obtain a list usable in
`#eval`; the data is the SAME 12 levels, not a fabricated re-listing. -/
def curves_12 : List CM_Curve :=
  (exceptional_12.sort (· ≤ ·)).map CM_Curve.mk

/-- Bost-bound VIOLATION test for a curve: `true` iff the (approx) Bost sum
does NOT exceed the threshold. EXPECTED `false` for every documented curve. -/
def BostViolation (X : CM_Curve) : Bool :=
  decide (C_rat (S_of_curve X) ≤ bostThreshold)

/-- The levels among the 12 CM curves that (approximately) VIOLATE the Bost
bound. EXPECTED `[]` under the certified data; a non-empty list would witness
a violation. Asserts NO theorem — `Twelve.TwelveViolation_Surface` stays OPEN. -/
def BostViolations_12 : List ℕ :=
  curves_12.filterMap (fun X => if BostViolation X then some X.id else none)

-- Computable witnesses (run at elaboration time):
#eval C_rat S_4                                              -- ≈ 11.42 (M5 reproduction)
#eval curves_12.map (fun X => (X.id, C_rat (S_of_curve X)))
#eval BostViolations_12                                     -- expected: []

end TheoremaAureum.Towers.BostViolations
