# Yang–Mills Referee Download Kit

Companion to `docs/YangMills_Honor_Transition.pdf`.

This kit contains the three load-bearing Lean 4 source files behind the
honest SU(3) lattice Yang–Mills write-up, for direct inspection. It is
**not** a self-contained build: a full re-elaboration requires the
complete `lean-proof-towers` package and the pinned `mathlib` v4.12.0
checkout.

## Contents

- `Transfer.lean` — the genuine integral transfer operator `T_L` on
  `L²(Fin (4·L⁴) → SU(3), haarN)`, the proven sub-Markov contraction
  `transfer_operator_norm_le` (‖T_L‖ ≤ 1), the proven polymer-activity
  scaffolding and the proven DCT reduction
  `polymerActivity_tendsto_zero_of_null`, and the three OPEN
  declarations: two carry an explicit `sorry` —
  `kotecky_preiss_criterion` (the genuine mass gap) and
  `trivial_polymer_set_null` — plus `polymerActivity_tendsto_zero`,
  which inherits `sorryAx` transitively from the latter.
- `WilsonPositivity.lean` — pointwise Wilson-action positivity
  (`wilsonAction_nonneg`, `wilsonAction_pos_of_nontrivial`,
  `wilsonAction_eq_zero_iff`) and polymer-energy lemmas. All sorry-free,
  classical-trio. Necessary but **not** sufficient for a gap.
- `SU3Instances.lean` — the real instance stack for SU(3), the real
  Haar measure `haarSU3`, and the product Haar measure `haarN`. All
  sorry-free, classical-trio.

## Proven vs. open (the frontier)

PROVEN — sorry-free, axioms = classical trio
`{propext, Classical.choice, Quot.sound}`:

- `T_L` (genuine integral operator over real Haar measure)
- `transfer_operator_norm_le` : ‖T_L‖ ≤ 1 (sub-Markov contraction —
  an UPPER bound, NOT a gap)
- `polymerActivity_nonneg`, `polymerActivity_empty`,
  `polymerActivity_antitone_in_beta`
- `polymerActivity_tendsto_zero_of_null` (dominated-convergence
  reduction)
- `wilsonAction_nonneg`, `wilsonAction_pos_of_nontrivial`,
  `wilsonAction_eq_zero_iff`, `plaquetteEnergy_*`, `polymerEnergy_*`
- `haarSU3`, `haarN` (real measures, with probability-measure instances)

OPEN — disclaimed `sorry`, reports `sorryAx`, NOT bricks:

- `kotecky_preiss_criterion` — the genuine Clay mass gap (a spectral
  LOWER bound on the vacuum-orthogonal / zero-mean sector). Its single
  missing input is the cluster-entropy bound
  `#{ γ : |γ| = n, energy(γ) < ε } ≤ Cⁿ · ε^(α·n)`.
- `trivial_polymer_set_null` — a genuine measure-theoretic null-set
  fact (needs `NoAtoms haarSU3` + a `Measure.pi` marginal argument).
- `polymerActivity_tendsto_zero` — inherits the above `sorry`.

## NO claim is made

This kit does NOT prove the Yang–Mills mass gap. No `m > 0`, no
`μ > 0`, no "Surface #1 closed", no "mass gap proven". `‖T_L‖ ≤ 1` is
the wrong inequality for a gap; the constants are eigenfunctions with
eigenvalue `Z(β) ≤ 1`, and `inf_{U≠1} wilsonAction(U) = 0`, so no
pointwise energy decay exists. The genuine gap is OPEN.

## Verification recipe (conservative — the mathlib checkout is fragile)

1. Assert the pin BEFORE any `lake` call:

       git -C lean-proof-towers/.lake/packages/mathlib rev-parse v4.12.0

   If this fails, do NOT run `lake` — a missing tag makes `lake`
   re-fetch from remote and wipe the oleans.

2. Elaborate + audit a file (tag present):

       cd lean-proof-towers
       lake env lean Towers/YM/Transfer.lean

   The in-file `#print axioms` lines report the classical trio for each
   proven declaration and additionally `sorryAx` for the OPEN ones (two
   carry an explicit `sorry`; `polymerActivity_tendsto_zero` inherits
   `sorryAx` transitively).

3. Recovery if the checkout is wiped: run
   `scripts/restore-lake-git.sh` TWICE, recreate the tag

       git -C lean-proof-towers/.lake/packages/mathlib \
         tag -f v4.12.0 809c3fb3b5c8f5d7dace56e200b426187516535a

   then re-download oleans with `scripts/fetch-mathlib-oleans.sh`.

4. Full trio-clean wall: `scripts/check-towers.sh` (the `BRICKS` array
   in that script is the source of truth for the count). The files in
   this kit are sorry-free `lakefile` roots that elaborate green but are
   deliberately NOT in `BRICKS` — honest infrastructure, not headline
   bricks.

— David J. Fox · ORCID 0009-0008-1290-6105
