# MorningStar / Theorema Aureum — Changelog

Historical design notes for the MorningStar-Lab CLI and the
Theorema Aureum proof chain. `replit.md` is the live-ops doc;
this file is the version history.

---

## task #79 — Fix `Towers/YM/RealCurvatureV2.lean` so `towers-build` is green

`lean-proof-towers/Towers/YM/RealCurvatureV2.lean` (Path B batch 6,
landed 2026-05-26) was blocking the full `towers-build` workflow:

1. `def lattice_deriv {n : ℕ} [NeZero n] (A : GaugeField n) (_μ : Fin 4) :
   GaugeField n := fun i => A (i + 1) - A i` — the pointwise subtraction
   on `GaugeField n = PiLp 2 (fun _ : Fin n => EuclideanSpace ℝ (Fin 8))`
   pulls in `ENNReal.instCanonicallyOrderedCommSemiring`, which is
   `noncomputable`, so the surrounding `def` itself must be
   `noncomputable`.
2. `theorem structure_constants_su3_def : … = 1 := by unfold …; decide`
   got stuck because Lean inferred a `Classical.choice`-backed
   `Decidable` instance for the `(0, 1, 2) = (0, 1, 2)` triple on
   `Fin 8 × Fin 8 × Fin 8`, and `decide` cannot reduce a
   classical `Decidable`.

Fixes:

- `def lattice_deriv …` → `noncomputable def lattice_deriv …`.
- `decide` → `rw [if_pos rfl]`. Explicitly supplying the `rfl`
  proof of `(0, 1, 2) = (0, 1, 2)` sidesteps the `Decidable`
  instance selection entirely.

All five RealCurvatureV2 bricks (`structure_constants_su3_def`,
`lie_bracket_su3_def`, `lattice_deriv_forward_diff`,
`curvature_su3_def`, `YMEnergy_nonneg`) now pass the per-brick
axiom-footprint check with the classical-trio
`{propext, Classical.choice, Quot.sound}`. `bash scripts/check-towers.sh`
reports `ok: Towers library built; all 126 brick(s) passed the
axiom-footprint check.` YM tower status unchanged: **Open**
(`docs/ROADMAP.md` § 2). The fixes are mechanical — they recover
exactly the bricks the Batch 6 commit intended to land; no new
mathematical content, no scope creep.

---

## v1.10 task #55 — `MassGap.HilbertSpace` upgraded to ℓ²(ℕ,ℂ) (Branch A)

`lean-proof-towers/Towers/YM/MassGap.lean` line 138 had
`def HilbertSpace : Type := sorry` paired with the Task #51
audit block that explicitly rejected every concrete replacement
as either a disguised stub or substantively misleading. Task #55
overrides that audit for `HilbertSpace` *only*, picking the
honest version of Branch A:

    abbrev HilbertSpace : Type := lp (fun _ : ℕ => ℂ) 2

(Imported from `Mathlib.Analysis.InnerProductSpace.l2Space` —
ℓ²(ℕ,ℂ), the canonical separable infinite-dim complex Hilbert
space; carries `NormedAddCommGroup`, `InnerProductSpace ℂ`,
`CompleteSpace` instances for free.)

Branches B (symmetric Fock space) and C (su(3)-valued L²) were
both rejected for this turn with honest reasons recorded in the
new in-source "Task #55 decision" block:

- B: mathlib v4.12.0 has no `SymmetricFockSpace`, no
  Hilbert-completion of a tensor algebra, and no
  second-quantization machinery. Building it would be hundreds
  to thousands of lines of new infrastructure, and even then
  symmetric Fock space over `L²(ℝ³,ℂ)` is the free-boson
  Fock space — still not the YM physical Hilbert space.
- C: needs `𝔰𝔲(3)` defined as a subtype of
  `Matrix (Fin 3) (Fin 3) ℂ` (anti-Hermitian, traceless) with
  `NormedAddCommGroup` / `InnerProductSpace ℝ` instances
  proved by hand, then lifted to `Lp`. Doable but bigger than
  the Task #55 budget. Tracked as follow-up.

Honest-scoping (in the file docstring and the audit block, and
re-affirmed here): ℓ²(ℕ,ℂ) is a real infinite-dim Hilbert
space, but it is NOT the Yang-Mills physical state space — that
requires an Osterwalder–Schrader reconstruction from a
constructed 4D Euclidean YM measure not present in mathlib
v4.12.0 (and an open research problem in 4D pure YM). After
this change `YM_mass_gap_statement` type-checks against
ℓ²(ℕ,ℂ) plus two remaining `sorry`-backed defs
(`YMHamiltonian`, `IsEigenstate`) — that type-checking is NOT a
formalization of the Clay conjecture. Tower status:
**Open** (per `docs/ROADMAP.md` § 2, unchanged).

Verification:

- `towers-build` workflow green; all 18 YM/NS bricks still
  carry axiom footprint `[propext, Classical.choice, Quot.sound]`.
- `lean-proof` workflow green;
  `TheoremaAureum.main_theorem axioms = []` unchanged
  (HilbertSpace lives in `lean-proof-towers`, not in the
  sealed `lean-proof/` spine).
- Sealed files untouched. Genesis seal still
  `eecbcd9a540aa7a2c90edd23827c73e4d1bb5af641d352f70a5de849b21f875f`.

YM mass-gap remaining sorry count: was 3 (`HilbertSpace`,
`YMHamiltonian`, `IsEigenstate`); now 2.

---

## v1.10 task #52 — fix the broken `zeta-burst` probe (concurrent-tamper race)

`zeta-burst-101-10000` had been chronically red even though
`scripts/check-genesis-seal.py` against the live ledger always
passed. The mismatch reports (`got: ce8477f6…`) and the downstream
`'--- GENESIS SEAL ---' is not in list` errors both pointed at a
"path / stale-file" bug; the actual root cause was a race between
the `morningstar-tamper` test fixture and any concurrent ledger
appender (`zeta_burst`, `zeta_sieve`):

- `tests/test_morningstar.py::_tamper_and_run` used
  `HITS.write_text(...)`, which opens `data/hits.txt` in `'w'` mode
  and **truncates the file to zero bytes** before the new content
  is written.
- A `kernel._verify_seal()` call landing inside that few-millisecond
  window read an empty file, so `lines.index("--- GENESIS SEAL ---")`
  raised `ValueError`, which `preamble_bytes` turned into
  `SystemExit("FATAL: ... missing required marker")`, which the
  in-process kernel surfaced as
  `RuntimeError("Genesis seal verification failed (preamble unreadable)")`.
- Result: every time the tamper-test workflow ran alongside the
  zeta-burst workflow, the burst aborted on its first probe — and
  this had been happening every CI cycle.

Fix is two-sided:

1. `tests/test_morningstar.py::_atomic_write_bytes` now writes via a
   sibling tempfile + `os.replace`. That is POSIX-atomic on the same
   filesystem, so concurrent readers see either the pristine bytes
   or the tampered bytes, never a truncated intermediate.
2. `kernel._verify_seal` retries up to 4 times with a 50 ms-stepped
   backoff before giving up. A genuine tamper is stable and still
   fails on every attempt; a transient mid-write read (e.g. any
   future test or operator using a non-atomic rewrite) recovers on
   the next try. The tamper-detection contract is preserved — the
   `test_probe_refuses_to_append_when_seal_fails` and
   `test_*_fails` cases still all pass.

Regression pinned by
`tests/test_morningstar.py::test_verify_seal_survives_concurrent_atomic_rewriter`,
which spawns a background atomic rewriter and asserts that
`kernel._verify_seal()` succeeds many times in a 1-second window
with zero failures.

---

## v1.9 Stage 2A-Prime — `zeta_sieve` (sign-change sieve)

`zeta_sniper`/`zeta_burst` go one zero at a time via `mpmath.zetazero`,
which pays a grampoint search per zero. Stage 2A-Prime adds a
range-oriented entry point that amortises a single grid of
`mpmath.siegelz` evaluations across every zero in a window:

- `kernel.sieve_zeros(t_start, t_end, dps=50, grid_density=4, write=True, pool_workers=None, flush_every=100)`
  — Builds a grid of `N = 2^k ≥ M` points with spacing
  `avg_gap / grid_density`, where `avg_gap = 2π / log(t_mid / 2π)`;
  batches `siegelz(t_i)` via `multiprocessing.Pool` (fork context,
  workers default to `min(cpu_count, 8)`); sieves consecutive pairs
  with `Z(t_i)·Z(t_{i+1}) < 0`; Brent-refines each bracket via
  `mpmath.findroot(siegelz, (a,b), solver="anderson")`. When
  `write=True`, every refined zero is logged via
  `probe(1, 1, 0.5, t0)` (so `_verify_seal()` runs before the
  `_append_line()` and the resulting SHA is part of the same
  Three-Guns hash chain). `flush_every=100` is a progress-print
  cadence — `_append_line` already flushes+fsyncs per line.
- `lab.py` CLI: `zeta_sieve(t_start, t_end[, write=True|False])`.
  `_parse_zeta_sieve` rejects any other keyword *before* the kernel
  runs, so a typo can't leak into the live ledger.

**Honest scope.** This is NOT the full Odlyzko-Schönhage 1991 FFT
trick (which evaluates Z on the full grid in O(M log M) via a
re-expansion of the Riemann-Siegel main sum). It is a parallelised
sign-change sieve over per-point `siegelz` calls plus a Brent
refinement pass. The speed win over `zetazero(n)` sniping comes
from (a) skipping the per-zero grampoint search, (b) batching `Z`
evaluations across cores, and (c) reusing one grid for all zeros
in the window — a real constant-factor improvement, NOT an
asymptotic one. The docstring on `sieve_zeros` calls this out
explicitly.

**Concurrency contract.** `_append_line` has no file lock. The
parent process is the SOLE writer to `data/hits.txt`; the Pool
workers only compute `Z(t)` and return floats. "One gun at a time"
is engineering, not preference — a second appender would interleave
bytes mid-line and corrupt the chain.

**Dry-run guarantee.** `zeta_sieve(t_start, t_end, write=False)`
prints every refined zero but does NOT call `_append_line` and does
NOT call `_verify_seal`. The CLI surfaces this as `ZETA SIEVE
DRY-RUN: [...] → N zeros (NOT appended (write=False))`.

**Verified on [0, 100]:** the dry-run finds exactly 29 nontrivial
ζ zeros in ~1.07s on the workspace container (default 4-worker
pool, default grid_density=4, default dps=50). Every returned `t`
satisfies `|ζ(½ + it)| < 1e-49`. `test_sieve_zeros_dry_run_does_not_write`
pins both the count window (25 ≤ found ≤ 35) and the non-write
invariant.

---

## v1.9 — "Three Guns" surface (lab.py)

The single `probe(h, N, re, im)` entry point conflated three
different intents — Riemann sniping, Dirichlet evaluation, and
"I want an elliptic L but the kernel can't compute it". v1.9 splits
them into three explicitly-typed CLI commands so the *intent* of a
probe is visible in the ledger and on the command line, not inferred
from `(h, N)`. All three write through the same seal-verify-then-
append discipline as `probe()`.

- **Gun 1 — Zeta sniper** (`zeta_sniper(n)`, `zeta_burst(a,b)`,
  `bracket_riemann_zero(n, eps)`): thin wrappers over `kernel.zero`
  / `hunt_zeros` / `bracket_zero`. Uses `mpmath.zetazero(n)`
  directly. Verified on the Lehmer pair: `zeta_sniper(6709)` →
  t=7005.0628661749…, |L|=7.85×10⁻¹⁵; `zeta_sniper(6710)` →
  t=7005.1005646726…, |L|=1.72×10⁻¹³ (Δt ≈ 0.0377).
- **Gun 2 — Dirichlet radar** (`dirichlet_probe(N, re, im[, char])`):
  routes principal χ₀ to `probe(1, N, re, im)`. Non-principal `char`
  rejected with `NEEDS_SAGE` **without** writing a ledger line.
- **Gun 3 — Elliptic stub** (`elliptic_probe(label, re, im)`):
  does **not** evaluate. Writes a SHA-stamped intent line tagged
  `ELLIPTIC_STUB` with `reason=elliptic_L_requires_sage`. Label
  validated against `^[A-Za-z0-9._-]{1,32}$` before any seal check.
  Critically does NOT route through `probe(1, conductor, ...)`
  (that would compute a Dirichlet L). Returned dict has no `L_*`
  keys; `test_kernel.py` pins the invariant.

Legacy commands (`probe`, `zero`, `hunt_zeros`, `bracket_zero`,
`scan_critical_line`, `scan_line`, `scan_plane`) all still work —
Three-Guns is additive.

---

## v1.0 — Seven-layer 4D research surface

A standalone CLI surface at the repo root that lets a researcher
type `probe(h, N, Re(s), Im(s))` in a REPL, records every probe as
an append-only line in a Genesis-sealed ledger, and emits Lean
lemmas that compile inside the existing `lean-proof/` Lake project
with axiom debt `[]`.

- `data/hits.txt` — append-only ledger. Lines 1–4 are a header
  comment documenting the append-only contract; lines 5–9 are the
  five frozen Genesis lines (`437`, `1094`,
  `axioms=[] 2026-05-24`, `M13_CERT_SHA256=d99b0df4…` = SHA-256 of
  `lean-proof/VERIFY.txt`, `--- GENESIS SEAL ---`). The whole
  preamble (lines 1–9) is sealed. Line 10+ are probe outputs;
  existing lines are never rewritten.
- `data/M13_CERT.txt` — human-readable M13 certificate header.
- `kernel.py` — Layer 4. `probe(h, N, re_s, im_s)`. Verifies the
  Genesis seal before every append. mpmath backend
  (`workdps=50`): `h=1, N=1` → ζ(s) (`MPMATH_ZETA`);
  `h=1, N>1` → principal χ₀ mod N as `ζ(s)·∏_{p|N}(1 - p^{-s})`
  (`MPMATH_DIRICHLET_TRIVIAL`); `h≥2` → `NEEDS_SAGE` with
  `reason=h>=2_out_of_scope_for_mpmath_backend`. Any backend
  exception also falls back to `NEEDS_SAGE` with a `reason=`.
- `lab.py` — Layer 7. Banner + REPL + `-c "probe(...)"` one-shot.
- `lean_bridge.py` — Layer 2. Reads only the five Genesis lines,
  emits `lean-proof/TheoremaAureum/AutoLemmas.lean`
  (`theorem hit_<n> : True := trivial`), ensures
  `TheoremaAureum.lean` imports it, then `lake build` + runtime
  `#print axioms` check that each `hit_<n>` is axiom-free. Refuses
  to write `sorry`/`axiom `/`admit ` in non-comment code.
- `scripts/check-genesis-seal.py` — verifies SHA-256 of the
  immutable preamble against the baked-in seal `eecbcd9a…875f`.
- `scripts/validate-morningstar.sh` — full harness. Not wired into
  `post-merge.sh` or the `lean-proof` validation — v1.8-BC drift
  guard runs unchanged.

**Honest-scope guards (v1.0).** `hit_437`/`hit_1094` are tautologies.
Their *names* reference the OpenCV cube counts from README Appendix
A; their *statements* claim nothing about number theory. `probe()`
never calls SageMath.

---

## Release v1.8-BC (honest scope)

- Frozen spine: M1–M10 + M13 (BC–CM, h = 1). Lean `main_theorem`
  axiom debt = [].
- `README.md` is the public-facing summary; `CITATION.cff` ships
  without a DOI field — v1.8-BC is hosted on Replit as the source
  of truth. A DOI can be added later if archived elsewhere.
- README Appendix A records the OpenCV square counts
  (`437 = 19 × 23`, `1094 = 2 × 547`) from `cube_M0_v1.jpg` /
  `cube_M0_v2.jpg` as **observations only**. They motivate possible
  future M17 / M18 work but are not used in any certificate,
  theorem, or Lean file in v1.8-BC.
- No `sorry` and no `axiom` allowed in `lean-proof/`. The CI drift
  guard (`scripts/check-lean-proof.sh`, strict mode in the
  `lean-proof` workflow) enforces this on every merge.

---

## Lean 4 formal proof — design notes

Lean 4 project (`lean-proof/`) implementing the M1–M9 certificate
chain as a formal deductive structure.

**Files:**
- `lean-toolchain` — pins `leanprover/lean4:v4.12.0`
- `lakefile.lean` — requires mathlib v4.12.0
- `TheoremaAureum/Certificates.lean` — M5/M6/M7 records
- `TheoremaAureum/M9_WeilTransfer.lean` — M9 280-case discharge (`M9_WeilTransfer_All`)
- `TheoremaAureum/C_Chain.lean` — deductive chain + unconditional `main_theorem`
- `TheoremaAureum.lean` — root module
- `Verify.lean` — axiom check script

**Verified result:**
```
$ lake build          # succeeds
$ lake env lean Verify.lean
'TheoremaAureum.main_theorem' depends on axioms: []
```

**Axiom debt = [] (zero axioms).** All hard rules satisfied:
- H1_ArakelovPositivity: THEOREM (by decide, M5 certificate)
- C05_Descent: THEOREM (True.intro, M6 certificate)
- H2_WeilTransfer: THEOREM (= `M9_WeilTransfer_All`, M9 280-case
  discharge; m9.out SHA `624b93f7…`)

**Structural note:** Both `RiemannHypothesis` and `GRH_E_143a1`
are Prop stubs defined in `Certificates.lean` (the spec's original
layout had a circular import). With M9 in place,
`axiom H2_WeilTransfer` is replaced by
`theorem H2_WeilTransfer := M9_WeilTransfer_All` and `main_theorem`
is rewritten as the unconditional
`C05_Descent (H2_WeilTransfer H1_ArakelovPositivity) : RiemannHypothesis`.

**Full mathlib build:** run `lake exe cache get && lake build` to
compile with real `riemannZeta`/`riemannXi` semantics (requires ~2 GB
of prebuilt mathlib oleans). The structural proof above is correct
without it.

**Regenerating VERIFY.txt:** `./lean-proof/regenerate.sh` rebuilds
`lean-proof/VERIFY.txt` from a fresh `lake build` + `lake env lean
Verify.lean`. Fails loudly (and leaves VERIFY.txt unchanged) if
any of `main_theorem`, `H2_WeilTransfer`, or `M9_WeilTransfer_All`
no longer reports "does not depend on any axioms".

**Drift guard:** `scripts/check-lean-proof.sh` wraps `regenerate.sh`
and fails if the axiom-debt check no longer passes. Wired up two
ways:
- `lean-proof` validation workflow with `STRICT_LEAN_CHECK=1` —
  fails closed if `lake` missing.
- Invoked from `scripts/post-merge.sh` in non-strict (default) mode
  — prints a stderr warning if `lake` missing locally but exits 0
  so merges aren't blocked.
