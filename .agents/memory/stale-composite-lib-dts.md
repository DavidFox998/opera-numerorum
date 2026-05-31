---
name: Stale composite-lib .d.ts causes phantom consumer typecheck errors
description: Why a leaf artifact typecheck shows TS2305/TS7006 that the canonical root typecheck does not — and why the fix is NOT editing the consumer source.
---

# Stale composite-lib `dist/*.d.ts` → phantom TS2305/TS7006 in consumers

In this pnpm monorepo, `lib/*` packages are composite (`emitDeclarationOnly`,
`outDir: dist`) and `dist/` is **gitignored** (build output, not tracked). A
consuming artifact (e.g. `artifacts/theorema-certs`) resolves the lib through the
project-reference `dist/*.d.ts`, NOT through `src`.

If `dist/*.d.ts` is stale (older than the generated `src/generated/*`, e.g. after
a codegen run that added new hooks), running the **leaf** check alone —
`pnpm --filter @workspace/<artifact> run typecheck` — reports phantom errors:
- `TS2305` "Module '@workspace/api-client-react' has no exported member 'useGetX'"
  for names that DO exist in `src/generated/api.ts` and ARE re-exported by
  `src/index.ts`.
- cascading `TS7006` "implicitly has any type" on callbacks whose array types
  came from those now-unresolved hooks.

**The consumer source is not broken.** The canonical root command
`pnpm run typecheck` runs `typecheck:libs` (`tsc --build`) FIRST, then leaf
checks, so it passes clean — and so does CI / a fresh checkout.

**Why:** the lib's `package.json` `exports."."` points at `./src/index.ts`, but
TS project-reference resolution for a composite dep prefers the emitted
declarations in `dist`. Stale `dist` ⟹ stale view of the lib's API.

**How to apply:** when a leaf artifact typecheck reports missing exports for
names that grep-exist in the lib's generated/source, do NOT edit the consumer.
Run `pnpm run typecheck:libs` (rebuild composite declarations) — or the full
`pnpm run typecheck` — then re-check. After OpenAPI edits, the order is:
`pnpm --filter @workspace/api-spec run codegen` → `pnpm run typecheck:libs` →
leaf typecheck.
