---
name: follow-up-tasks
description: Propose well-scoped follow-up project tasks at the end of a task, tuned to the Morning Star / Theorema Aureum honesty-locked Lean proof tower. Use right before calling mark_task_complete to suggest the natural next steps, and to retract stale suggestions. Read this whenever mark_task_complete asks you to propose follow-ups.
---

# Follow-up Tasks (Theorema Aureum proof tower)

At the end of a task — right before `mark_task_complete` — suggest the natural
next steps as **follow-up project tasks** so the user can accept them with one
click. This skill explains the mechanism and, more importantly, what a *good*
follow-up looks like for THIS project (a Lean 4 / mathlib v4.12.0,
honesty-locked formalization where overstating results is the cardinal sin).

## The mechanism

Two callbacks are available in the `code_execution` sandbox:

- `proposeFollowUpTasks(...)` — propose one or more follow-up tasks for user
  review. **One-shot per assigned project task.** Call it at most once. If you
  already proposed follow-ups for the current task, do NOT call it again.
- `markFollowUpTaskObsolete(...)` — retract a previously-proposed follow-up that
  has become stale (e.g. you realized it's wrong, already done, or violates an
  invariant). Use this instead of re-proposing.

Both are opaque platform wrappers; pass a short, plain-language **title** plus a
**description** that reads like a `project_tasks` plan (see the `project_tasks`
skill for the plan body format: *What & Why*, *Done looks like*, *Out of scope*,
*Steps*, *Relevant files*). Follow the same User Communication Rules as
`project_tasks`: refer to tasks by ref + title, never expose internal state
names or callback names to the user.

If `proposeFollowUpTasks` is unavailable in the environment, skip silently —
do not block `mark_task_complete` on it.

## When to propose (and when not to)

Propose a follow-up when the finished work has an obvious, valuable next step:

- A documented `sorry` you intentionally deferred and that is genuinely
  approachable (e.g. a closedness or embedding lemma backed by real mathlib API).
- The next phase of a multi-phase tower (e.g. "Phase 2" after a "Phase 1").
- A scaffolding lemma that would make a faithfulness claim machine-explicit.
- An infra/honesty hardening step you noticed but that was out of scope.

Do NOT propose:

- Anything that would breach a **locked invariant** (see `replit.md`): new
  research-grade axioms, `sorry`/`admit`/`sorryAx` in a *landed brick*, a
  Mathlib bump off v4.12.0, or flipping a tower to `Status: Closed`.
- A "prove the mass gap" / "close Surface #1" / "close Surface #2" /
  "prove RH" / "μ > 0" task. These are the Clay-level OPEN cores; they are
  REFUSED, not follow-ups. The honest open combinatorics behind them (e.g. the
  KP polymer-counting estimate) are not "tasks" to schedule.
- Discharging a `sorry` that is genuinely Clay-adjacent as if it were routine,
  or any task whose only honest outcome is an overstated claim.
- Vague chores ("clean up", "add more tests") with no concrete deliverable.

Default to **0–2** high-quality follow-ups. Fewer, sharper suggestions beat a
long list. One per natural next step.

## Honesty framing (non-negotiable for this tower)

Every follow-up title and description must be honest about scope, exactly like
landed work:

- State precisely what would be PROVED and what stays OPEN.
- Mark whether the result is intended to be a registered **brick** (in `BRICKS`,
  a lakefile root, axiom-clean, `sorry`-free) or honest scaffolding (NOT a
  brick, may ship `sorryAx` by design with ≤2 documented sorries).
- Never let a follow-up imply a tower closes, a surface closes, or `m > 0`.

## Operational constraints to bake into any follow-up plan

These are recurring footguns in this repo — note them in the plan's *Steps* so
the executor (you or a task agent) doesn't wipe the environment:

- **Do NOT run `towers-build` / `lake update` casually.** Both re-clone vendored
  mathlib and wipe the `v4.12.0` pin + oleans. `lake env` is *also* destructive
  when the tag is missing.
- **Before any `lake env lean`,** assert
  `git -C lean-proof-towers/.lake/packages/mathlib rev-parse v4.12.0` succeeds.
  Recovery if wiped: `scripts/restore-lake-git.sh` (×2) → retag
  `v4.12.0 809c3fb3b5c8f5d7dace56e200b426187516535a` →
  `scripts/fetch-mathlib-oleans.sh`.
- Verify a new `.lean` file with a direct `lake env lean <file>` + `#print
  axioms`, not by adding it to a lakefile root.
- The `towers-build` / `api-server` / `theorema-certs*` workflow "failed" states
  are usually unrelated churn — don't treat them as regressions from a
  proof-file change that isn't a brick or lakefile root.

## Concrete follow-up candidates (NS Tower 540, after Phase 1)

Phase 1 landed `Towers/NS/FunctionSpaces.lean` (honest weighted-L² Hˢ model,
`Hdiv_free s`, proved subspace closure, 2 documented Clay-adjacent sorries:
`divFreeSubmodule_isClosed`, `embed`). Good, honestly-framed next steps:

- **Discharge `divFreeSubmodule_isClosed`** — prove the div-free set is
  L²-closed (continuity of `f ↦ ⟪toVal ξ, f ξ⟫` / a.e.-limit argument). Keep it
  honest scaffolding unless it is genuinely axiom-clean and `sorry`-free.
- **NS Tower 540, Phase 2** — the next analytic object on the roadmap (e.g. the
  Leray projector or the Stokes/heat semigroup on `Hdiv_free`), as honest
  scaffolding with ≤2 documented sorries.
- **Faithfulness lemma** — a small lemma equating the inner-product divergence
  `⟪toVal ξ, û⟫_ℂ` with the component sum `∑ i, ξ_i · û_i`, making the
  "this really is `ξ·û`" claim machine-checked.

Each of these is a *separate* natural step → at most one or two per proposal.

## Minimal workflow

```javascript
// At task end, before mark_task_complete — once per task only.
await proposeFollowUpTasks({
  tasks: [
    {
      title: "NS Tower 540, Phase 2: Leray projector",
      description: [
        "## What & Why",
        "Build the honest Leray (div-free) projector on Hdiv_free s ...",
        "## Done looks like",
        "- Projector defined + bounded; NOT a brick; ≤2 documented sorries; tower stays Open.",
        "## Out of scope",
        "- Any m>0 / regularity / Surface #2 claim.",
        "## Relevant files",
        "`lean-proof-towers/Towers/NS/FunctionSpaces.lean`",
      ].join("\n"),
    },
  ],
});
```

The exact argument shape of `proposeFollowUpTasks` is platform-managed; if a call
errors on shape, inspect the error and retry with a single `{title, description}`
object or an array thereof. Never fabricate task content just to fill the slot —
propose nothing rather than something dishonest or low-value.
