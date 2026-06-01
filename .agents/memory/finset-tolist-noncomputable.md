---
name: Finset.toList is noncomputable (mathlib v4.12.0)
description: Why #eval over a Finset fails with "does not have executable code" and how to iterate computably.
---

# Finset.toList is noncomputable in mathlib v4.12.0

`Finset.toList` (and `Multiset.toList`) is **noncomputable** in v4.12.0, so any
`def` that uses it to build a `List` for `#eval` fails to compile with
`failed to compile definition, consider marking it as 'noncomputable' because it
depends on 'Finset.toList', and it does not have executable code`.

**Fix:** to get a computable `List` from a `Finset α` for `#eval`, use
`Finset.sort` with a decidable linear order, e.g.
`(s.sort (· ≤ ·)).map f` for `s : Finset ℕ` (needs `import Mathlib.Data.Finset.Sort`).
`Finset.sum` / `Finset.filter` / `Finset.fold` are already computable; it is only
the `Finset → List` materialization that needs `sort`.

**Why:** `toList` goes through `Quotient.out` (choice), so it carries no
executable code; `sort` is implemented via `List.mergeSort` and is executable.

**How to apply:** any computable `#eval` that needs to enumerate a `Finset`'s
elements (not just sum/fold them) — reach for `Finset.sort`, never `toList`.
Note `decide` over a `ℚ` inequality (`decide (a ≤ b)`) IS executable in `#eval`.
