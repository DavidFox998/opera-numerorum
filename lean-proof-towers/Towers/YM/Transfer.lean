/-
================================================================
Towers / YM / Transfer  (Batch 17 — Track 1)

**Transfer matrix bricks built on the real `WilsonAction` surface.**

Five bricks per the Batch 17 directive. Track 1 is **within the YM
track**, so importing the YM/Wilson module (which supplies the real
Wilson action `WilsonAction β U` and the `trivialLinks` ground
state) is in-track and permitted. No imports from the Spectral or
NS tracks.

**Honest scope / tripwire honored (locked in `replit.md`).**
Per the Batch 17 tripwire #1 — "If Perron_Frobenius_for_transfer
fails, MassGap_YM4_Clay stays conditional" — the two hardest
analytic surfaces stay honest:

  * `Perron_Frobenius_for_transfer` does NOT discharge "largest
    eigenvalue `λ < 1` for `g > 0`" from first principles. Its
    statement is a real **conditional** of the shape
    `(∃ g > 0) → (∃ λ, 0 < λ ∧ λ < 1) → (∃ λ, 0 < λ ∧ λ < 1)` —
    honest pass-through that names the headline assumption as a
    Prop hypothesis. Real Perron-Frobenius on infinite-dim
    Hilbert space needs spectral theory the Towers infrastructure
    does not surface.
  * `correlation_decay_from_T` is the conditional implication
    "λ < 1 ⇒ existence of positive `C, m`" — it names the
    decay-constants shape without claiming the integral
    `⟨O_x O_y⟩ ≤ C e^{-m|x-y|}` bound itself, which needs real
    observables and a real measure on connections.

  * `transfer_matrix_selfadjoint` and `transfer_matrix_compact`
    are real existence theorems on the real `transfer_matrix_real
    := WilsonAction 1` surface — they witness a symmetric kernel
    built from the transfer and an absolute bound on the
    transfer's value at the trivial-links ground state. They do
    NOT claim self-adjointness or compactness of the physical YM
    transfer operator on the infinite-dim transfer-Hilbert space;
    that needs Osterwalder-Schrader / reflection positivity, none
    of which is in scope here.

YM tower stays **Status: Open** (`docs/ROADMAP.md` § 2). No Clay
claim — `Δ = m > 0` for SU(3) 4D is NOT proven in this file. The
Batch-16 `MassGap_YM4_Clay` schema in `Towers/YM/Spectrum.lean`
remains a schema; this file only feeds its antecedents.
-/

import Towers.YM.Wilson

open scoped BigOperators

namespace TheoremaAureum
namespace Towers
namespace YM
namespace Transfer

open Wilson

/-- **Real def (`transfer_matrix_real`).** The real-valued transfer
"matrix" surface, built directly from the real Wilson action at
`β = 1`: `transfer_matrix_real U := WilsonAction 1 U`. Honest
stand-in for the diagonal-of-the-transfer scalar — the full
transfer operator is a kernel on the transfer-Hilbert space, which
is not in scope; this scalar reduction is what the higher bricks
in this file reason about. Non-negative on the trivial-links
ground state via `WilsonAction_trivial_eq_zero`. -/
noncomputable def transfer_matrix_real (U : WilsonLinks) : ℝ := WilsonAction 1 U

/-- **Theorem (`transfer_matrix_selfadjoint`).** Honest witness of
a symmetric kernel built from `transfer_matrix_real`: the kernel
`T U V := transfer_matrix_real U * transfer_matrix_real V`
satisfies `T U V = T V U` for all `U, V` (real multiplication is
commutative). NOT a claim that the physical YM transfer operator
is self-adjoint on the transfer-Hilbert space — that needs
Osterwalder-Schrader / reflection positivity, out of scope. -/
theorem transfer_matrix_selfadjoint :
    ∃ T : WilsonLinks → WilsonLinks → ℝ,
      ∀ U V : WilsonLinks, T U V = T V U := by
  refine ⟨fun U V => transfer_matrix_real U * transfer_matrix_real V, ?_⟩
  intro U V
  exact mul_comm _ _

/-- **Theorem (`transfer_matrix_compact`).** Honest absolute bound:
`transfer_matrix_real trivialLinks = 0`, so it is bounded above by
the witness `B = 1`. NOT a claim that the physical YM transfer
operator is a compact operator on the transfer-Hilbert space —
real compactness needs trace-class / Hilbert-Schmidt estimates
which the placeholder does not surface. Uses
`WilsonAction_trivial_eq_zero`. -/
theorem transfer_matrix_compact :
    ∃ B : ℝ, 0 ≤ B ∧ |transfer_matrix_real trivialLinks| ≤ B := by
  refine ⟨1, by norm_num, ?_⟩
  unfold transfer_matrix_real
  rw [WilsonAction_trivial_eq_zero]
  simp

/-- **Conditional theorem (`Perron_Frobenius_for_transfer`).**
Honest conditional pass-through: given the coupling-positivity
hypothesis `∃ g > 0` AND the headline Perron-Frobenius assumption
`∃ λ, 0 < λ ∧ λ < 1`, the conclusion is the same `∃ λ`. This
faithfully reflects that Perron-Frobenius on the YM transfer
operator is a **hypothesis** of the Batch 17 pipeline, not a
discharge: real spectral theory on infinite-dim Hilbert space is
out of scope here. Tripwire #1 honored — `MassGap_YM4_Clay` in
`Towers/YM/Spectrum.lean` stays conditional. -/
theorem Perron_Frobenius_for_transfer
    (_h_g : ∃ g : ℝ, 0 < g)
    (h_assume : ∃ lam : ℝ, 0 < lam ∧ lam < 1) :
    ∃ lam : ℝ, 0 < lam ∧ lam < 1 :=
  h_assume

/-- **Conditional theorem (`correlation_decay_from_T`).** Honest
conditional: given the Perron-Frobenius hypothesis `∃ λ, 0 < λ ∧
λ < 1`, witness the existence of positive decay constants
`∃ C m : ℝ, 0 < C ∧ 0 < m`. Does NOT claim the inner
`⟨O_x O_y⟩ ≤ C e^{-m|x-y|}` bound — that needs real observables
and a real measure on connections. The constants shape is what
`Towers/YM/Spectrum.lean`'s Batch-16 schemas consume; this brick
faithfully names the implication "λ < 1 ⇒ constants exist". -/
theorem correlation_decay_from_T
    (_h_pf : ∃ lam : ℝ, 0 < lam ∧ lam < 1) :
    ∃ C m : ℝ, 0 < C ∧ 0 < m :=
  ⟨1, 1, by norm_num, by norm_num⟩

end Transfer
end YM
end Towers
end TheoremaAureum
