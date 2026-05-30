---
name: OS reflection positivity — honest Lean recipe
description: how to land Osterwalder–Schrader OS2 as a brick without overstating, in mathlib v4.12.0
---

# Landing OS2 (reflection positivity) honestly

When asked for "OS2 / reflection positivity for the Wilson (or any Euclidean)
measure", do NOT attempt the actual measure — mathlib v4.12.0 has no Wilson
Euclidean measure, no link-reflection, no GNS construction. The honest brick is:

1. **Prove the genuine, unconditional core: Gram positive-semidefiniteness.**
   For an `RCLike` inner-product space, `∑_{i,j} conj(cᵢ)·cⱼ·⟪vᵢ,vⱼ⟫ =
   ⟪∑ᵢ cᵢ•vᵢ, ∑ⱼ cⱼ•vⱼ⟫` (via `sum_inner`, `inner_sum`, `inner_smul_left/right`,
   then `ring`), whose `re` is `≥ 0` by `inner_self_nonneg`. This is the entire
   linear-algebra content of OS positivity and bears on NO measure.
2. **Route the measure-specific part through a NAMED OPEN GNS surface**
   `hGNS : ∀ F G, P F G = ⟪J F, J G⟫` (the Osterwalder–Seiler statement that the
   reflected correlation kernel is a Hilbert-space Gram form). A HYPOTHESIS, not
   `by sorry` → no `sorryAx`, axioms stay classical trio.

**Why:** OS2's real difficulty IS the positive-semidefiniteness of the reflected
kernel (and its survival of the thermodynamic/continuum limits); once that's a
Gram form, positivity is trivial linear algebra. So the honest split puts ALL the
open content in `hGNS` and proves the rest.

**How to apply:** OS2 is only one of OS0–OS4; Clay existence also needs the
continuum measure construction, OS1 Euclidean (rotation) invariance, OS0/OS3
temperedness/symmetry, and OS4 clustering → spectral mass gap. A Gram-PSD + GNS
brick closes NONE of these and must say so. `inner_self_nonneg` in v4.12.0 is
`0 ≤ re ⟪x,x⟫` (complex instance in InnerProductSpace/Basic.lean ~line 630).
