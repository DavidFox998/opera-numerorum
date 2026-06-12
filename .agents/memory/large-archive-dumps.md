---
name: Large-archive / forensic dumps under fragile workflow windows
description: How to reliably produce multi-GB tar/bundle deliverables when bash is capped and workflows die at turn boundaries.
---

# Producing large archives (tar / git bundle) in this environment

**The two hard constraints (both observed repeatedly):**
- The bash tool is capped at ~2 min AND its FS I/O is throttled so hard that even
  `find`-listing the ~161k-file tree exceeds the cap (it is ~8s inside a workflow).
  So multi-GB compression/listing CANNOT be done in a single bash call.
- A workflow has fast (warm-cache) I/O, but managed/background jobs are terminated
  at agent turn/checkpoint boundaries. Window length is unpredictable: sometimes
  ~50s, occasionally several minutes. A turn interruption shows up as a bash tool
  call returning exit code `-1` with no output, and it stops ALL workflows.
- `/tmp` has a hidden ~3GB quota (NOT the 32G `df` shows). Write big outputs to the
  workspace dir (200G+ free), never `/tmp`.

**The recipe that works:**
1. Put the whole job in a shell script run as a workflow (`configureWorkflow`,
   `autoStart:true`), NOT in bash tool calls.
2. Make the script RESUMABLE: each step skipped if its output already exists AND
   verifies intact (`wc -l` threshold for text, `git bundle verify`, `zstd -t`,
   or a `.part`→`mv` atomic-rename so a present file always = a complete file).
   Then relaunch repeatedly; finished steps are skipped and progress accumulates
   across kills until one long-enough window lands.
3. Poll ONLY with short sleeps (~45s) that RETURN CLEANLY — they keep the turn
   alive so the workflow survives. Do NOT use `restart_workflow` (it SIGKILLs a
   no-port one-shot) and avoid long sleeps (≥~60–95s frequently `-1`).
4. A `git bundle --all` (~2 min, CPU-bound delta compression) often won't fit a
   short window; a STORE-mode `tar -cf .git` is a faster fallback and is a superset
   of a bundle. Prefer the bundle when a long window appears.
5. EXCLUDE regenerable caches from the content tar (node_modules, `.lake` oleans,
   `.pythonlibs`, `.cache`, `__pycache__`, `.pytest_cache`) and `.git` (ship it as
   the bundle). That shrinks ~9-10GB to a feasible ~2-3GB and loses nothing
   restorable. ALSO exclude prior output artifacts by name, or a stale partial gets
   swept into the new tar.

**Why:** a single monolithic "everything" archive of all caches (~9-10GB, ~5 min)
never survived; the resumable-skip + relaunch + cache-exclusion approach did.

# Verifying the deliverables (full-clone/restore capability)
- Checks that PROVE usability: `sha512sum -c <sidecar>` (both bundle+tar),
  `git bundle verify` (must say "records a complete history … is okay"), an actual
  `git clone --bare <bundle> tmp.git` + `rev-list --all --count` + `fsck` (this is
  the real clone-capability proof, not just verify), and `zstd -t <tar>` for the
  content tar. Then `rm -rf` the temp clone.
- A single solo bundle read-check (sha512 + `git bundle verify`, ~633MB twice) DOES
  fit one bash call. But the bare clone (read+write+index ~1.3GB) and 2.64GB-tar
  hashing each EXCEED the bash window → run them as the workflow+keepalive recipe above.
- Running TWO heavy-I/O bash calls in the SAME response (parallel) reliably returns
  `-1` (turn interrupt) for BOTH from contention. Serialize heavy ops one-per-call,
  or push them into the workflow. (Parallelism is fine only for light calls.)
- A 25.9MB text manifest "errors" in the present_asset download card; ship a
  `gzip -k` copy (~4.5MB) for reliable download alongside the raw .txt.

# Zipping high-file-count REPRODUCIBLE trees is effectively infeasible here
- Single-big-file STORED zips (each wraps one large tar/bundle) finish inside ONE
  ~55s poll cycle, so they survive. But zipping a high-file-count tree — `.lake`
  oleans (thousands of files, ~4.4GB), `node_modules` (tens of thousands) — takes
  many poll cycles, and EVERY subsequent sleep-poll started while that I/O is
  ongoing returns `-1` and kills ALL workflows. Switching Python `zipfile`→`zip`
  CLI (`-0 -r`) did NOT help; the killer is the sustained multi-cycle I/O + any
  concurrent keepalive, not the tool.
- Practical rule: do NOT try to package the reproducible bulk (oleans/node_modules/
  media) as attended zips. Separate it as its own honest section and ship a
  REGENERATION RECIPE instead (`pnpm install`, `lake exe cache get` @ pinned tag,
  re-run export tooling). The original contribution (Towers/ source, docs, dashboard)
  is tiny (<50MB total) and zips trivially. That separation is the whole point of an
  "honest split" — don't pad the deposit with regenerable bulk.
