---
name: Wilson action positivity is necessary-not-sufficient (no uniform gap from compactness)
description: Why pointwise Wilson-action positivity in the YM towers is NOT a spectral/mass gap, and the honest shape of the zero-iff lemma.
---

# Wilson-action positivity ≠ mass gap (Theorema Aureum YM towers)

When tightening transfer-operator bounds (`Towers/YM/Transfer.lean`) or adding
positivity scaffolding (`Towers/YM/WilsonPositivity.lean`), keep these honest:

- `wilsonAction U = 0 ↔ ∀ x μ ν, wilsonPlaquette U x μ ν = 1` (ALL plaquettes
  trivial). It is **NOT** `↔ U = 1` — gauge / global-centre freedom makes the
  `U = 1` reading false. State the zero-iff against "all plaquettes trivial".

- A **uniform** off-vacuum lower bound `∀ U ≠ 1, wilsonAction U ≥ δ > 0` is
  **FALSE**: `Fin (4·L⁴) → SU(3)` is compact, `wilsonAction` is continuous and
  vanishes at the vacuum, so `inf {wilsonAction U : U ≠ 1} = 0`. Refuse any
  "Step 1: vacuum_strict_positivity" framing.
  **Why:** pointwise positivity (`wilsonAction_nonneg`, `…_eq_zero_iff`) is only
  *necessary*, never *sufficient* for a spectral gap.
  **How to apply:** the genuine mass gap is the OPPOSITE inequality — a spectral
  *lower* bound `T_L ≥ c·𝟙` on the zero-mean sector (the `kotecky_preiss_criterion`
  contraction `‖T_L f‖ ≤ exp(-β·gap)·‖f‖`), which is a cluster-expansion result,
  NOT a compactness corollary. It stays a `sorry` / OPEN. `transfer_operator_norm_le`
  is only the sub-Markov UPPER bound `‖T_L‖ ≤ 1` (constants saturate it), never a
  gap.

- Proof idiom: the zero-iff over the nested triple sum (`∑ x ∑ μ ∑ ν`) does NOT
  close with `rw [Finset.sum_eq_zero_iff_of_nonneg …]` — the rewrite fails to
  match the higher-order nested pattern under a `letI` Fintype instance. Use the
  term-mode `.mp` of `Finset.sum_eq_zero_iff_of_nonneg` (forward) and
  `Finset.sum_eq_zero` (backward); both are defeq-friendly and sidestep the
  syntactic match.
