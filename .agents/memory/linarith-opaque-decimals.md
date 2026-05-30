---
name: linarith opaque decimals
description: Why linarith/nlinarith fail on decimal literals in Lean/mathlib and how to fix it.
---

# linarith treats decimal `OfScientific` literals as opaque atoms

`linarith` (and `nlinarith`) reason over linear arithmetic with *rational*
coefficients. A decimal literal like `0.6931471808` or `3.141592` elaborates to
an `OfScientific` term, which linarith treats as an **opaque atom**, not as a
rational it can scale. So a goal that is "obviously" true by decimal arithmetic
(e.g. bounding a sum against `3.141592`) silently fails to close.

**Fix pattern:** convert each decimal bound to a clean rational *before* the
final `linarith`:
1. `have e : (0.6931471808 : ℝ) ≤ 7/10 := by norm_num`
2. chain it with the mathlib decimal bound by transitivity:
   `have hlog2' : Real.log 2 < 7/10 := by linarith [Real.log_two_lt_d9, e]`
3. do the final `linarith` using only the rational bounds (`7/10`, `25/8`, …).

**Why:** `norm_num` *can* evaluate decimal comparisons (it knows `OfScientific`),
linarith cannot. So use `norm_num` to launder the decimal into a rational, then
hand the rational to linarith.

**How to apply:** any ℝ inequality proof that pulls a mathlib bound stated with a
decimal (`Real.pi_gt_d6 : 3.141592 < π`, `Real.log_two_lt_d9`, the
`*_d6`/`*_d9` family) and needs linarith/nlinarith afterwards. Pick a rational
strictly on the correct side (π > 25/8 = 3.125, log 2 < 7/10) so the laundering
step is provable by `norm_num`.
