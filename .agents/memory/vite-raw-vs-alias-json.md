---
name: Vite ?raw imports bypass tsconfig path resolution
description: Why `@alias/...?raw` typechecks without a tsconfig paths entry but plain `@alias/...json` does not.
---

In this monorepo's Vite + bundler-resolution artifacts (e.g. `artifacts/theorema-certs`),
only `@/*` is mapped in the artifact `tsconfig.json` `paths`. Aliases defined ONLY
in `vite.config.ts` (`@lean`, `@docs`) resolve at runtime but NOT in `tsc`.

**Rule:** `import x from "@lean/whatever?raw"` typechecks fine even with no tsconfig
mapping, because `vite/client` ships an ambient `declare module '*?raw'` that matches
*any* specifier ending in `?raw` — TS never tries to resolve the real path. But
`import x from "@lean/whatever.data.json"` (no `?raw`) makes TS actually resolve the
module, which fails with TS2307 since `@lean` isn't in tsconfig paths.

**How to apply:** To pull a non-`?raw` file (JSON, etc.) through a Vite-only alias
without touching tsconfig, import it as `...json?raw` and `JSON.parse` it — or, if you
want the file rendered verbatim, just use the raw string directly (parse+stringify
normalizes formatting and is not byte-faithful). Adding the alias to tsconfig `paths`
is the alternative but is more invasive.
