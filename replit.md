# Morning Star Project · Theorema Aureum 143 (Volume I)

**For Batches 1–177 + Tasks #188/#189 see `docs/CHANGELOG.md`**
(also: full per-batch wall-jump tables, tactic notes, proof
sketches, drift footnotes, env var docs, stack, where-things-live,
user preferences, gotchas, pointers — all rolled into CHANGELOG by
the Wall-510 / Wall-539 / Wall-542 trims).

- **Wall:** 543 BRICKS (script-reported by `scripts/check-towers.sh`)
- **YM Surface #1:** Open
- **Axiom debt:** `[]` on `TheoremaAureum.main_theorem`
  (`#print axioms` returns `[]`; also `[]` on `H2_WeilTransfer` and
  `M9_WeilTransfer_All`)
- **Mathlib:** v4.12.0 only · trio axioms only
  `{propext, Classical.choice, Quot.sound}` · no `sorry` / `admit`
  in any landed brick · YM and NS towers stay `Status: Open` in
  `docs/ROADMAP.md`

## Locked invariants (every batch must hold these)

- Axiom footprint = classical trio
  `{propext, Classical.choice, Quot.sound}`; no new research-grade
  axioms.
- Mathlib v4.12.0 only; no `sorry` / `admit` in any landed brick.
- YM and NS towers stay `Status: Open` in `docs/ROADMAP.md`;
  Surface #1 and Surface #2 stay OPEN. "Surface #1 CLOSED" /
  "μ > 0" / "removes the Attempts sorry" / "Mass Gap proven"
  claims are REFUSED — every YM Measure-surface brick is trivially
  or vacuously true under the Dirac haar stand-in
  (`T_OS = 0` / `T_real = 0`), NOT under any real Wilson transfer
  operator.
- `kotecky_preiss_criterion` remains a `sorry` in
  `Towers/Attempts/ClusterExpansion.lean` (invariant-locked).

## Pending / in-flight (not yet landed)

- **Wall 571-B / [YM1-LB-Core]** — `Towers/YM/LatticePositivity.lean`
  written + VERIFIED (`namespace TheoremaAureum.YM_MassGap`). Pure-core
  (no mathlib, no imports, `Int`/`Nat` only): `lattice_positivity`
  proves a finite sum of integer squares is `≥ 0` and `= 0` iff every
  term is `0` — the trivial discrete shadow of "H ≥ 0", NOTHING more.
  `#print axioms …lattice_positivity` = [] (strictly empty) via direct
  `lean` (lake-free). Registered as [YM1-LB-Core], NOT [YM1]; makes NO
  mass-gap / μ>0 / Surface-#1 claim — Surface #1 stays OPEN, YM Status
  Open. NOT in `scripts/check-towers.sh` BRICKS (that path is
  lake-gated → script-reported wall unchanged). ℝ companion
  "B-deferred" (`Towers/YM/LatticePositivityReal.lean`) awaits a
  healthy mathlib cache. Verify: see the file's honest-scope header.

- **Batch 178.1 / SLinkDef** — `Towers/YM/SLinkDef.lean` written
  (`S_link` + brick `S_link_const_one`), NOT registered to
  `lakefile.lean` / `scripts/check-towers.sh` BRICKS array, no wall
  gain claimed. Verification blocked by the task #208 cache wipe
  (the `lake update` re-clone race). Clean verify sequence once the
  cache is stable: `lake exe cache get` → `lake build Towers`
  (produces dependency oleans incl. `KoteckyPreissRealKP.olean`) →
  `lake env lean Towers/YM/SLinkDef.lean` + `#print axioms
  TheoremaAureum.Towers.YM.LatticeGauge.S_link_const_one`.

## Gotcha — do NOT run `towers-build` / `lake update` casually

The `towers-build` workflow (and any `lake update`) re-clones the
vendored mathlib checkout and wipes its oleans, requiring a
`lake-recovery` (`lake exe cache get`) pass. Verify bricks via
direct `lake env lean <file>` + `#print axioms` instead.
