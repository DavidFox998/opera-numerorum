---
name: decide stalls on Rat in kernel
description: kernel `decide`/`rfl` over a Bool containing a Rat comparison gets stuck; route the Rat clause through a hypothesis or norm_num.
---

When a `Bool`-valued predicate `&&`s together several `decide (...)` clauses and
ONE of them is a `Rat` order comparison (e.g. `decide (sig.margin ≤ 1/1000000)`),
proving `pred = true` with a single kernel `decide` (or `rfl`) **fails with
"did not reduce to isTrue/isFalse"** — `Rat.instDecidableLe` / `Int.decLt` /
`Int.decNonneg` do not whnf-reduce in the kernel for the `=true` case.

**Why:** the FALSE case short-circuits (`Bool.and false _ = false` never forces
the Rat decide), so `decide` proving `pred = false` can still work; but the TRUE
case forces every conjunct, and the Rat decide instance stalls.

**How to apply:** don't prove the whole `pred = true` by kernel `decide`. Instead
`simp only [pred, Bool.and_eq_true, decide_eq_true_eq]` to split into a `∧` of the
underlying Props, then close the Rat clause from a hypothesis or with `norm_num`
(NOT `decide`). The Nat/UInt32/Fin clauses are fine under `decide`.
