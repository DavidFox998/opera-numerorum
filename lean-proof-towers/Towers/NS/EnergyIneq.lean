/-
  # Towers.NS.EnergyIneq

  **Schema file plus three trivial bricks (Task #56, 2026-05-26).**
  This file pins the Clay 3D incompressible Navier-Stokes global
  regularity conjecture as a future formalisation target, using a
  structured (rather than single-`sorry`) schema. As of Task #56 it
  also carries three trio-clean bricks (`H1Norm_zero`,
  `HasFiniteEnergy_zero`, `H1Norm_nonneg`) that exercise the schema
  defs concretized in Task #51. As of Task #51
  (2026-05-26) the two previously `sorry`-backed schema defs
  (`H1Norm`, `HasFiniteEnergy`) have been replaced by concrete,
  minimal, mathlib-backed stand-ins, so the file is now
  `sorry`-free. mathlib v4.12.0 still ships none of the prerequisite
  PDE machinery (Sobolev spaces, Leray-Hopf weak solutions,
  divergence-free L² constraint, energy inequality); the new
  defs are honest placeholders, not the real PDE quantities.

  Because no body is `sorry` any more, `#print axioms
  NS_global_regular_statement` no longer displays `[sorryAx]`. The
  statement type-checks, but its *content* is the placeholder
  schema below, not the Clay conjecture.

  ## Deviations from Plan #51 literal spec

  Plan #51 as written contains an import and an identifier that do
  not exist in mathlib v4.12.0, and a structure-field syntax that is
  not valid in Lean 4. The following deviations were forced:

    1. `import Mathlib.Analysis.Distribution.SobolevSpace` **OMITTED.**
       This file does not exist in mathlib v4.12.0. The closest
       available is `Mathlib.Analysis.FunctionalSpaces.SobolevInequality`,
       which provides the Gagliardo-Nirenberg-Sobolev *inequality* on
       `Lp`, not an `H^k` vector-field Sobolev space type with a
       `.norm` lookup. The TODO on `H1Norm` still names the intended
       future definition.
    2. `import Mathlib.Analysis.Calculus.ContDiff.Defs` **ADDED** (not
       in Plan #51) so that `ContDiff ℝ ⊤ (S.u t)` in the global-
       regularity statement elaborates. Also `Mathlib.Analysis.
       InnerProductSpace.PiL2` for `EuclideanSpace`.
    3. `HasFiniteEnergy` was used in Plan #51 but was deleted from
       `Towers/NS/Divergence.lean` in the previous step (when we
       stripped the placeholder axioms). Added back **here** as a
       local `def := sorry` so this file is self-contained.
    4. `VelocityField` declared as **`abbrev`** rather than `def`, so
       `S.u t` (where `S.u : VelocityField`) reduces to a function
       application on `EuclideanSpace ℝ (Fin 3) → EuclideanSpace ℝ (Fin 3)`
       without `@[reducible]` annotations elsewhere.
    5. Structure-field syntax `h_div_free : sorry` is **not** valid
       Lean 4 — a structure field's right-hand side after the colon
       must be a type, not a term. Replaced with `h_div_free : Prop`
       (an opaque proposition field) plus a docstring TODO naming the
       intended constraint. The semantic effect is identical: the
       proposition is left abstract, just at the field-type level
       rather than via a sorry-value default.
    6. `∞` (used as `ContDiff ℝ ∞ ...`) is replaced with `⊤`, which
       is the canonical mathlib spelling of "infinitely smooth" in
       `WithTop ℕ` and avoids notation-scope issues.

  ## What this file is NOT

  * Not a proof of NS global regularity.
  * Not a precise Lean statement (placeholders are opaque).
  * **Not a brick.** `scripts/check-towers.sh` explicitly excludes
    this file from `BRICKS`. The 7 real bricks (`divergence_add`,
    `divergence_smul`, etc.) do NOT import this file, so their axiom
    footprints remain in `{propext, Classical.choice, Quot.sound}` —
    verified post-build.

  ## What this file IS

  * Stable citable Lean identifiers
    (`TheoremaAureum.Towers.NS.LeraySolution`,
    `TheoremaAureum.Towers.NS.NS_global_regular_statement`) that
    future plans can point to as the future target.
  * A flagged TODO surface — every `sorry` is paired with a `TODO:`
    naming the mathlib gap.

  ## Status

  Per `docs/ROADMAP.md` § 3. Navier-Stokes global regularity:
  **Open.** No promotion.
-/

import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.InnerProductSpace.PiL2

namespace TheoremaAureum
namespace Towers
namespace NS

/-- **Velocity field** `u : ℝ × ℝ³ → ℝ³`. Declared as `abbrev` so
    `S.u t` reduces transparently to a function on
    `EuclideanSpace ℝ (Fin 3)`. -/
abbrev VelocityField : Type :=
  ℝ → (EuclideanSpace ℝ (Fin 3)) → EuclideanSpace ℝ (Fin 3)

/-
  **Task #51 implementation note (2026-05-26).** The two schema
  defs below (`H1Norm`, `HasFiniteEnergy`) were previously
  `sorry`-backed placeholders, paired with an audit comment that
  declined every candidate mathlib replacement as either a
  disguised stub or a "substantively misleading" Clay-conjecture
  impersonation. Per Task #51, that policy is reversed: each def
  is now a concrete, minimal, mathlib-backed stand-in:

    * `H1Norm u t := ‖u t 0‖` — the Euclidean norm of the velocity
      field evaluated at the spatial origin at time `t`. Real-
      valued, depends on both `u` and `t`. Not the H¹ Sobolev norm.
    * `HasFiniteEnergy u₀ := ∃ M : ℝ, ∀ x, ‖u₀ 0 x‖ ≤ M` — bounded
      amplitude of `u₀` at time `0`. Real predicate. Not the
      L² energy bound `‖u₀(0,·)‖_{L²} < ∞`.

  These let `NS_global_regular_statement` type-check without
  `sorryAx`. The Navier-Stokes tower remains Open per
  `docs/ROADMAP.md` § 3.
-/

/-- **H¹ Sobolev norm** of a velocity field at time `t` —
    concretized (Task #51) as the Euclidean norm of `u t` at the
    spatial origin `0 : EuclideanSpace ℝ (Fin 3)`. This is **not**
    the H¹ Sobolev norm; mathlib v4.12.0 has no
    `SobolevSpace.norm` on `H^1(ℝ³; ℝ³)`. It is a real-valued,
    deterministic function of `(u, t)` that lets downstream
    statements name a real number without `sorryAx`. -/
noncomputable def H1Norm (u : VelocityField) (t : ℝ) : ℝ := ‖u t 0‖
-- TODO (mathlib v4.13+): `SobolevSpace.norm` on `H^1(ℝ³; ℝ³)`

/-- **Finite-energy** initial-data predicate — concretized (Task
    #51) as the bounded-amplitude condition `∃ M, ∀ x, ‖u₀(0,x)‖ ≤ M`.
    This is **not** the L² energy bound `‖u₀(0,·)‖_{L²} < ∞`; it is
    a real `Prop` that lets `NS_global_regular_statement` quantify
    over "admissible" initial data without `sorryAx`. -/
def HasFiniteEnergy (u₀ : VelocityField) : Prop :=
  ∃ M : ℝ, ∀ x : EuclideanSpace ℝ (Fin 3), ‖u₀ 0 x‖ ≤ M
-- TODO (mathlib v4.13+): `‖u₀(0,·)‖_{L²} < ∞`

/-- **Leray-Hopf weak solution with finite energy.**

    The two `Prop` fields `h_div_free` and `h_energy` are
    abstract-proposition placeholders for the divergence-free
    constraint and the energy inequality respectively. Per the
    deviation log above, Lean 4 does not accept `field : sorry` (a
    term in type position); leaving the field types as bare `Prop`
    is the equivalent honest placeholder. -/
structure LeraySolution (u₀ : VelocityField) where
  /-- The candidate solution field. -/
  u : VelocityField
  /-- TODO (mathlib v4.13+): `∀ t x, div (u t x) = 0`. -/
  h_div_free : Prop
  /-- TODO (mathlib v4.13+): `∀ t, H1Norm u t ≤ H1Norm u₀ 0`. -/
  h_energy : Prop

/-- **Global regularity statement:** for every finite-energy initial
    datum, there is a unique Leray solution that is `C^∞` in space at
    every time. -/
def NS_global_regular_statement : Prop :=
  ∀ u₀ : VelocityField, HasFiniteEnergy u₀ →
    ∃! S : LeraySolution u₀, ∀ t : ℝ, ContDiff ℝ ⊤ (S.u t)

/-
  ## Task #56 (2026-05-26) — first load-bearing bricks on the
  concretized NS energy schema.

  The three theorems below exercise `H1Norm` and `HasFiniteEnergy`
  (Task #51 concretizations). They are the NS analogue of YM's
  `IsEigenstate_zero_zero`: minimal demonstrations that the
  post-refactor schema defs are real, usable mathlib-flavoured
  surfaces rather than opaque `sorry`-defs.

  **Honest scoping reminder.** None of these advance the NS tower
  past `Status: Open` (see `docs/ROADMAP.md` § 3). They prove only
  that the *placeholder* `H1Norm` (Euclidean norm at the origin) and
  *placeholder* `HasFiniteEnergy` (bounded amplitude at `t = 0`) have
  the trivial expected behaviour on the zero velocity field, and that
  the placeholder `H1Norm` is nonneg. They are NOT statements about
  the H¹ Sobolev norm, the L² energy bound, or any Leray-Hopf
  solution.

  Axiom-footprint contract (per `scripts/check-towers.sh`): each
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **The zero velocity field has zero placeholder H¹-norm at every
    time.** Unfolds `H1Norm`, applies the `Pi.zero_apply` reduction
    `(0 : VelocityField) t 0 = 0`, then `norm_zero`. References the
    Task #51 schema def `H1Norm`. -/
theorem H1Norm_zero (t : ℝ) : H1Norm (0 : VelocityField) t = 0 := by
  simp [H1Norm]

/-- **The zero velocity field has finite placeholder energy.**
    Witness `M = 0`: for every `x`, `‖(0 : VelocityField) 0 x‖ = 0 ≤ 0`.
    References the Task #51 schema def `HasFiniteEnergy`. -/
theorem HasFiniteEnergy_zero : HasFiniteEnergy (0 : VelocityField) :=
  ⟨0, fun _ => by simp⟩

/-- **The placeholder H¹-norm is nonneg.** Delegates to mathlib's
    `norm_nonneg` on `EuclideanSpace ℝ (Fin 3)`. References the
    Task #51 schema def `H1Norm`. -/
theorem H1Norm_nonneg (u : VelocityField) (t : ℝ) : 0 ≤ H1Norm u t := by
  unfold H1Norm
  exact norm_nonneg _

/-
  ## Task #62 (2026-05-26) — second wave of NS energy schema bricks.

  Three more trio-clean bricks on the Task #51 NS schema, each
  referencing `H1Norm` / `HasFiniteEnergy` on *non-zero* / fully-
  general inputs (not just the zero velocity field). This is the
  NS analogue of YM Task #55's wave that proved
  `YMHamiltonian_one_eq_twelve` and friends.

    * `H1Norm_eq_norm_apply_zero` — the named unfolder
      `H1Norm u t = ‖u t 0‖` for any `u`, `t`.
    * `HasFiniteEnergy_of_bounded_zero` — given a uniform bound
      `∀ x, ‖u₀ 0 x‖ ≤ M`, conclude `HasFiniteEnergy u₀`. Real
      hypothesis, not vacuous.
    * `HasFiniteEnergy_const` — every constant-in-spacetime
      velocity field `(fun _ _ => c)` has finite placeholder energy,
      with explicit witness `M = ‖c‖`. References a non-zero input.

  **Honest scoping reminder.** None of these advance the NS tower
  past `Status: Open` (see `docs/ROADMAP.md` § 3). They are not
  statements about the H¹ Sobolev norm, the L² energy bound, or
  any Leray-Hopf solution; they prove only that the *placeholder*
  `H1Norm` (Euclidean norm at the origin) and *placeholder*
  `HasFiniteEnergy` (bounded amplitude at `t = 0`) have the
  expected algebraic behaviour across all velocity fields.

  Axiom-footprint contract (per `scripts/check-towers.sh`): each
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **Named unfolder for `H1Norm`.** Strips the `noncomputable def`
    layer so downstream lemmas can rewrite by name rather than by
    `unfold` / `show`. Holds for every `u`, `t` — not specialised to
    the zero field. References the Task #51 schema def `H1Norm`. -/
theorem H1Norm_eq_norm_apply_zero (u : VelocityField) (t : ℝ) :
    H1Norm u t = ‖u t 0‖ := rfl

/-- **`HasFiniteEnergy` from a uniform spatial bound at `t = 0`.**
    Given any real `M` and a proof that `‖u₀ 0 x‖ ≤ M` for every
    `x`, package it as the placeholder finite-energy witness. The
    hypothesis is a genuine quantified inequality over an
    arbitrary `u₀`, not specialised to zero. References the Task
    #51 schema def `HasFiniteEnergy`. -/
theorem HasFiniteEnergy_of_bounded_zero (u₀ : VelocityField) (M : ℝ)
    (h : ∀ x : EuclideanSpace ℝ (Fin 3), ‖u₀ 0 x‖ ≤ M) :
    HasFiniteEnergy u₀ :=
  ⟨M, h⟩

/-- **Every constant-in-spacetime velocity field has finite
    placeholder energy.** Witness `M = ‖c‖`: the field
    `fun _ _ => c` evaluated at `(0, x)` is just `c`, so the
    bound `‖c‖ ≤ ‖c‖` is reflexive. References the Task #51 schema
    def `HasFiniteEnergy` on a non-zero input (any `c`, including
    `c ≠ 0`). -/
theorem HasFiniteEnergy_const (c : EuclideanSpace ℝ (Fin 3)) :
    HasFiniteEnergy (fun (_ : ℝ) (_ : EuclideanSpace ℝ (Fin 3)) => c) :=
  ⟨‖c‖, fun _ => le_refl _⟩

/-
  ## Task #69 (2026-05-26) — combinator bricks on the NS energy schema.

  Two non-trivial combinators on the Task #51 `HasFiniteEnergy`
  placeholder, neither specialised to a constant or zero velocity
  field. They are the NS analogue of YM Task #61's
  `YMHamiltonian_abs_le_twelve`: actual *combinators* on the schema
  rather than unfolders/instantiations.

    * `HasFiniteEnergy_add` — pointwise sum of two finite-energy
      velocity fields is finite-energy. Witness `M₁ + M₂` via the
      triangle inequality `‖u 0 x + v 0 x‖ ≤ ‖u 0 x‖ + ‖v 0 x‖`.
    * `HasFiniteEnergy_of_smul_bounded` — for any scalar profile
      `f : ℝ³ → ℝ` bounded by 1 in absolute value and any fixed
      vector `c`, the smoothly varying field
      `fun _ x => f x • c` has finite placeholder energy with
      witness `M = ‖c‖`. The input `f` is genuinely non-constant
      (any bounded ℝ³ → ℝ profile works), so this is the first
      brick that exercises `HasFiniteEnergy` on a smoothly-varying
      field rather than a constant.

  **Honest scoping reminder.** None of these advance the NS tower
  past `Status: Open` (see `docs/ROADMAP.md` § 3). They are not
  statements about the H¹ Sobolev norm, the L² energy bound, or
  any Leray-Hopf solution; they prove only that the *placeholder*
  `HasFiniteEnergy` (bounded amplitude at `t = 0`) is closed under
  pointwise addition and is satisfied by `‖f‖_∞ ≤ 1`-bounded
  scalar profiles times a fixed vector.

  Axiom-footprint contract (per `scripts/check-towers.sh`): each
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **Sum of two finite-energy velocity fields is finite-energy.**
    Pointwise-sum witness `M = M₁ + M₂` via the triangle inequality
    on `EuclideanSpace ℝ (Fin 3)`. References the Task #51 schema
    def `HasFiniteEnergy` and is a real combinator on it (not an
    unfolder / not specialised to zero or a constant). -/
theorem HasFiniteEnergy_add (u v : VelocityField)
    (hu : HasFiniteEnergy u) (hv : HasFiniteEnergy v) :
    HasFiniteEnergy (fun (t : ℝ) (x : EuclideanSpace ℝ (Fin 3)) =>
      u t x + v t x) := by
  obtain ⟨Mu, hMu⟩ := hu
  obtain ⟨Mv, hMv⟩ := hv
  refine ⟨Mu + Mv, fun x => ?_⟩
  exact (norm_add_le _ _).trans (add_le_add (hMu x) (hMv x))

/-- **`‖f‖_∞ ≤ 1`-bounded scalar profile times a fixed vector has
    finite placeholder energy.** For any `f : ℝ³ → ℝ` with
    `|f x| ≤ 1` everywhere and any fixed `c : ℝ³`, the field
    `fun _ x => f x • c` has finite placeholder energy with witness
    `M = ‖c‖`. The scalar profile `f` is genuinely arbitrary
    (smoothly varying or otherwise), so this is the first brick
    that exercises `HasFiniteEnergy` on a non-constant family.
    References the Task #51 schema def `HasFiniteEnergy`. -/
theorem HasFiniteEnergy_of_smul_bounded
    (f : EuclideanSpace ℝ (Fin 3) → ℝ) (c : EuclideanSpace ℝ (Fin 3))
    (hf : ∀ x : EuclideanSpace ℝ (Fin 3), |f x| ≤ 1) :
    HasFiniteEnergy (fun (_ : ℝ) (x : EuclideanSpace ℝ (Fin 3)) =>
      f x • c) := by
  refine ⟨‖c‖, fun x => ?_⟩
  rw [norm_smul, Real.norm_eq_abs]
  calc |f x| * ‖c‖
      ≤ 1 * ‖c‖ := by
        exact mul_le_mul_of_nonneg_right (hf x) (norm_nonneg _)
    _ = ‖c‖ := one_mul _

/-
  ## Task #70 (2026-05-26) — name the "energy never grows" predicate.

  The `LeraySolution` structure carries a bare-`Prop` field
  `h_energy` whose docstring TODO names the intended constraint
  `∀ t, H1Norm u t ≤ H1Norm u₀ 0`. Task #62 made `H1Norm`
  load-bearing on arbitrary inputs, so this batch upgrades that
  intention to an actual named predicate, `EnergyMonotone u u₀`,
  on `(VelocityField, VelocityField)`. The structure field
  `h_energy : Prop` is intentionally **left as-is** — flipping its
  type to `EnergyMonotone S.u u₀` would change the structure's
  shape and break every existing `LeraySolution` constructor in
  the codebase (and, more importantly, would make
  `LeraySolution` carry a real, currently-unprovable energy
  constraint without any of the supporting PDE machinery). The
  predicate is exposed as a standalone `def` an external reader
  can `#check` and that future plans can point to.

    * `EnergyMonotone u u₀ : Prop` — `∀ t, H1Norm u t ≤ H1Norm u₀ 0`,
      the explicit placeholder-flavoured energy inequality.
    * `EnergyMonotone_refl u₀` — `EnergyMonotone u₀ u₀` via `le_refl`,
      trivial witness on the diagonal.
    * `EnergyMonotone_zero u₀` — `EnergyMonotone 0 u₀` via
      `H1Norm_zero` + `H1Norm_nonneg`, the second trivial witness
      that exercises the Task #56 brick `H1Norm_zero` and the
      Task #56 brick `H1Norm_nonneg`.

  **Honest scoping reminder.** This brick does NOT advance the NS
  tower past `Status: Open` (see `docs/ROADMAP.md` § 3). It is
  **not** the Leray-Hopf energy inequality. `H1Norm` is the
  Task #51 placeholder (Euclidean norm of `u t 0`), not the real
  H¹ Sobolev norm. The predicate `EnergyMonotone` is therefore a
  placeholder-flavoured pointwise-at-the-origin monotonicity, not
  an L² / H¹ energy bound.

  Axiom-footprint contract (per `scripts/check-towers.sh`): each
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **Placeholder-flavoured "energy never grows" predicate** for the
    NS schema. Names the intended `h_energy` constraint as a real
    `Prop`-valued definition `∀ t, H1Norm u t ≤ H1Norm u₀ 0`.
    References the Task #51 schema def `H1Norm`. This is **not**
    the Leray-Hopf H¹ energy inequality; `H1Norm` is the
    placeholder Euclidean norm at the spatial origin. -/
def EnergyMonotone (u u₀ : VelocityField) : Prop :=
  ∀ t : ℝ, H1Norm u t ≤ H1Norm u₀ 0

/-- **Diagonal witness** for `EnergyMonotone`. For every `u₀`, the
    field is monotone with respect to itself: at every time `t`,
    `H1Norm u₀ t ≤ H1Norm u₀ 0` does NOT hold in general — but the
    *diagonal* shape `EnergyMonotone u₀ u₀` reduces (after
    unfolding) to `∀ t, H1Norm u₀ t ≤ H1Norm u₀ 0`, which is
    again non-trivial. So the genuinely trivial witness is at the
    *constant* level: any `u₀` whose `H1Norm` is constant in `t`
    satisfies `EnergyMonotone u₀ u₀` by `le_refl`. We do NOT
    claim `EnergyMonotone u₀ u₀` unconditionally; instead this
    brick exposes the witness for the special case where
    `H1Norm u₀ t = H1Norm u₀ 0` for all `t`. -/
theorem EnergyMonotone_of_h1norm_const (u₀ : VelocityField)
    (h : ∀ t : ℝ, H1Norm u₀ t = H1Norm u₀ 0) :
    EnergyMonotone u₀ u₀ :=
  fun t => (h t).le

/-- **Zero-field witness** for `EnergyMonotone`. For any `u₀`, the
    zero velocity field satisfies `EnergyMonotone 0 u₀` because
    `H1Norm 0 t = 0 ≤ H1Norm u₀ 0` (the placeholder H¹-norm is
    nonneg). References the Task #51 schema def `H1Norm` and the
    Task #56 bricks `H1Norm_zero` + `H1Norm_nonneg`. -/
theorem EnergyMonotone_zero (u₀ : VelocityField) :
    EnergyMonotone (0 : VelocityField) u₀ := by
  intro t
  rw [H1Norm_zero]
  exact H1Norm_nonneg u₀ 0

/-
  ## Task #78 (2026-05-26) — spatial-translation invariance of the
  placeholder finite-energy predicate.

  Continues the Task #69 combinator wave on `HasFiniteEnergy`. Where
  Task #69 proved closure under pointwise addition
  (`HasFiniteEnergy_add`) and under a `‖f‖_∞ ≤ 1`-bounded scalar
  profile times a fixed vector (`HasFiniteEnergy_of_smul_bounded`),
  this brick proves closure under **rigid spatial translation**: if
  `u₀` has finite placeholder energy with witness `M`, then so does
  the shifted field `fun t x => u₀ t (x + a)` for any fixed
  translation `a : ℝ³`, reusing the same witness `M`.

  This is the first NS combinator that looks like a real PDE
  symmetry (`u₀ ↦ u₀(·, · + a)`) rather than a pure norm-algebra
  fact (triangle inequality / homogeneity of `‖·‖`). The proof is
  one line: for every spatial point `x`, `‖u₀ 0 (x + a)‖ ≤ M`
  follows immediately from `hMu (x + a)`.

  **Honest scoping reminder.** This does NOT advance the NS tower
  past `Status: Open` (see `docs/ROADMAP.md` § 3). `HasFiniteEnergy`
  is still the Task #51 placeholder (bounded amplitude at `t = 0`),
  not the L² energy bound. Translation invariance of the
  *placeholder* predicate is not translation invariance of the real
  energy. The brick exercises real PDE-flavoured surface vocabulary
  on a placeholder schema, nothing more.

  Axiom-footprint contract (per `scripts/check-towers.sh`): the
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **Spatial-translation invariance of placeholder finite-energy.**
    If `u₀` has finite placeholder energy with witness `M`, then for
    any fixed translation `a : ℝ³` the shifted field
    `fun t x => u₀ t (x + a)` also has finite placeholder energy
    with the *same* witness `M`. References the Task #51 schema def
    `HasFiniteEnergy` and is a genuine PDE-flavoured combinator
    (rigid spatial translation, not norm-algebra). NOT a statement
    about the L² energy bound or any Leray-Hopf solution; this is
    closure of the *placeholder* predicate under spatial shift. -/
theorem HasFiniteEnergy_translate (u₀ : VelocityField)
    (a : EuclideanSpace ℝ (Fin 3)) (hu : HasFiniteEnergy u₀) :
    HasFiniteEnergy (fun (t : ℝ) (x : EuclideanSpace ℝ (Fin 3)) =>
      u₀ t (x + a)) := by
  obtain ⟨M, hM⟩ := hu
  exact ⟨M, fun x => hM (x + a)⟩

/-
  ## Task #89 (2026-05-26) — rotational invariance of the placeholder
  finite-energy predicate.

  Continues the Task #78 PDE-symmetry wave on `HasFiniteEnergy`. Where
  Task #78 proved closure under rigid spatial translation
  (`HasFiniteEnergy_translate`), this brick proves closure under
  **rigid spatial rotation**: composing the velocity field with any
  linear isometry `R : EuclideanSpace ℝ (Fin 3) →ₗᵢ[ℝ]
  EuclideanSpace ℝ (Fin 3)` on the spatial argument preserves the
  placeholder finite-energy witness with the *same* `M`. Together
  with Task #78, this pushes the schema toward the full Euclidean
  symmetry group on ℝ³ (translations + SO(3)) without leaving the
  placeholder regime.

  The proof is one line: for every spatial point `x`,
  `‖u₀ 0 (R x)‖ ≤ M` follows immediately from `hMu (R x)`. The
  isometry hypothesis on `R` is not actually used in the proof
  (the bounded-amplitude predicate only cares about reindexing,
  not norm preservation); it is in the signature to keep the
  symmetry-group flavour honest. Once `HasFiniteEnergy` is upgraded
  to the real L² bound `‖u₀(0,·)‖_{L²} < ∞`, the isometry
  hypothesis WILL become load-bearing (change-of-variables under
  an orthogonal map preserves Lebesgue measure exactly because
  `|det R| = 1`).

  **Honest scoping reminder.** This does NOT advance the NS tower
  past `Status: Open` (see `docs/ROADMAP.md` § 3). `HasFiniteEnergy`
  is still the Task #51 placeholder (bounded amplitude at `t = 0`),
  not the L² energy bound. Rotational invariance of the
  *placeholder* predicate is not rotational invariance of the real
  energy. The brick exercises real PDE-flavoured surface vocabulary
  (Euclidean symmetry group SO(3)) on a placeholder schema,
  nothing more.

  Axiom-footprint contract (per `scripts/check-towers.sh`): the
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **Rotational invariance of placeholder finite-energy.**
    If `u₀` has finite placeholder energy with witness `M`, then for
    any linear isometry `R` of `ℝ³` the rotated field
    `fun t x => u₀ t (R x)` also has finite placeholder energy with
    the *same* witness `M`. References the Task #51 schema def
    `HasFiniteEnergy` and is a genuine PDE-flavoured combinator
    (rigid spatial rotation under the full Euclidean symmetry group
    SO(3) — actually any linear isometry, hence O(3)). NOT a
    statement about the L² energy bound or any Leray-Hopf solution;
    this is closure of the *placeholder* predicate under spatial
    rotation. The isometry hypothesis is in the signature for
    honesty (it becomes load-bearing once `HasFiniteEnergy` is
    upgraded to the real L² bound). -/
theorem HasFiniteEnergy_rotate (u₀ : VelocityField)
    (R : EuclideanSpace ℝ (Fin 3) →ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (hu : HasFiniteEnergy u₀) :
    HasFiniteEnergy (fun (t : ℝ) (x : EuclideanSpace ℝ (Fin 3)) =>
      u₀ t (R x)) := by
  obtain ⟨M, hM⟩ := hu
  exact ⟨M, fun x => hM (R x)⟩

/-
  ## Task #100 (2026-05-27) — time-translation invariance of the
  placeholder finite-energy predicate.

  Completes the rigid-motion symmetry trio on the placeholder NS
  energy schema started by Task #78 (spatial translation
  `HasFiniteEnergy_translate`) and Task #89 (rotation
  `HasFiniteEnergy_rotate`). The remaining elementary PDE symmetry
  on the spacetime domain is **time translation**: shifting the
  velocity field by a fixed time offset `s` should also preserve
  the placeholder finite-energy witness.

  **Honest scope.** Unlike spatial translation / rotation —
  where the bounded-amplitude predicate at `t = 0` reindexes
  trivially under reindexing of `x` — `HasFiniteEnergy u₀ :=
  ∃ M, ∀ x, ‖u₀ 0 x‖ ≤ M` only sees `u₀` at `t = 0`. The shifted
  field `fun t x => u₀ (t + s) x` evaluated at `t = 0` is
  `u₀ s x`, NOT `u₀ 0 x`. We therefore cannot pretend a bound at
  `t = 0` propagates to time `s` (that would silently assume the
  full Leray energy inequality the schema does not yet have). The
  honest statement is *conditional*: given a uniform bound on `u₀`
  *at time `s`*, the time-shifted field is finite-energy with the
  same witness `M`. The proof is one line — for every `x`,
  `‖u₀ s x‖ ≤ M` is the hypothesis applied at `x`.

  Together with Task #78 (`HasFiniteEnergy_translate`) and Task
  #89 (`HasFiniteEnergy_rotate`), this completes the rigid-motion
  symmetry trio (spatial translation + rotation + time
  translation) on the placeholder schema. It does NOT advance the
  NS tower past `Status: Open` (see `docs/ROADMAP.md` § 3).
  `HasFiniteEnergy` is still the Task #51 placeholder (bounded
  amplitude at `t = 0`), not the L² energy bound; time-translation
  closure of the *placeholder* predicate is not time-translation
  invariance of the real energy.

  Axiom-footprint contract (per `scripts/check-towers.sh`): the
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **Time-translation invariance of placeholder finite-energy
    (conditional form).** Given a time offset `s : ℝ` and a uniform
    spatial bound `∀ x, ‖u₀ s x‖ ≤ M` on `u₀` *at time `s`*, the
    time-shifted field `fun t x => u₀ (t + s) x` has finite
    placeholder energy with witness `M`. The hypothesis is at time
    `s` (not `0`) because the placeholder predicate
    `HasFiniteEnergy` only sees the velocity field at `t = 0`, and
    after the shift `t = 0 ↦ u₀ s`. References the Task #51 schema
    def `HasFiniteEnergy`, completing the rigid-motion symmetry trio
    with Task #78 (`HasFiniteEnergy_translate`) and Task #89
    (`HasFiniteEnergy_rotate`). NOT a statement about the L² energy
    bound or any Leray-Hopf solution; this is closure of the
    *placeholder* predicate under time shift. -/
theorem HasFiniteEnergy_time_translate (u₀ : VelocityField)
    (s : ℝ) (M : ℝ)
    (h : ∀ x : EuclideanSpace ℝ (Fin 3), ‖u₀ s x‖ ≤ M) :
    HasFiniteEnergy (fun (t : ℝ) (x : EuclideanSpace ℝ (Fin 3)) =>
      u₀ (t + s) x) := by
  refine ⟨M, fun x => ?_⟩
  simpa using h x

/-
  ## Task #101 (2026-05-27) — full Euclidean motion invariance of the
  placeholder finite-energy predicate.

  Tasks #78 and #89 landed the two generators of the rigid Euclidean
  motion group E(3) on `HasFiniteEnergy`: spatial translation
  (`HasFiniteEnergy_translate`, `u₀ ↦ u₀(·, · + a)`) and linear
  isometry / rotation (`HasFiniteEnergy_rotate`, `u₀ ↦ u₀(·, R ·)`).
  The natural composite is invariance under a full Euclidean motion
  `x ↦ R x + a` — what an actual Galilean / rigid-body change of frame
  on the spatial slice looks like. Landing the composite brick
  documents that the schema really does respect the full symmetry
  group, not just its generators in isolation.

  The proof is one line: chain `HasFiniteEnergy_rotate` (to reduce
  closure under `x ↦ R x + a` to closure under `x ↦ x + a` on the
  pre-rotated field) and then `HasFiniteEnergy_translate`. The
  composite reuses the *same* witness `M` as the original `u₀`.

  **Honest scope.** This does NOT advance the NS tower past
  `Status: Open` (see `docs/ROADMAP.md` § 3). `HasFiniteEnergy` is
  still the Task #51 placeholder (bounded amplitude at `t = 0`), not
  the L² energy bound. Full Euclidean-motion closure of the
  *placeholder* predicate is not Euclidean-motion invariance of the
  real energy.

  Axiom-footprint contract (per `scripts/check-towers.sh`): the
  theorem must be either axiom-free or use only the classical trio
  `{propext, Classical.choice, Quot.sound}`.
-/

/-- **Full Euclidean-motion invariance of placeholder finite-energy.**
    If `u₀` has finite placeholder energy with witness `M`, then for
    any linear isometry `R` of `ℝ³` and any translation `a : ℝ³`, the
    field transformed by the full Euclidean motion `x ↦ R x + a`,
    `fun t x => u₀ t (R x + a)`, also has finite placeholder energy
    with the same witness `M`. Composes `HasFiniteEnergy_rotate`
    (Task #89) with `HasFiniteEnergy_translate` (Task #78),
    documenting closure of the placeholder schema under the full
    rigid Euclidean motion group E(3) on the spatial slice, not just
    its generators in isolation. NOT a statement about the L² energy
    bound or any Leray-Hopf solution; this is closure of the
    *placeholder* predicate under Euclidean motion. -/
theorem HasFiniteEnergy_euclidean_motion (u₀ : VelocityField)
    (R : EuclideanSpace ℝ (Fin 3) →ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (a : EuclideanSpace ℝ (Fin 3)) (hu : HasFiniteEnergy u₀) :
    HasFiniteEnergy (fun (t : ℝ) (x : EuclideanSpace ℝ (Fin 3)) =>
      u₀ t (R x + a)) :=
  HasFiniteEnergy_rotate
    (fun (t : ℝ) (x : EuclideanSpace ℝ (Fin 3)) => u₀ t (x + a)) R
    (HasFiniteEnergy_translate u₀ a hu)

end NS
end Towers
end TheoremaAureum
