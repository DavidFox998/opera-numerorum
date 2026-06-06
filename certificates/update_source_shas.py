#!/usr/bin/env python3
"""
update_source_shas.py -- Patch sha256_source / sha256_binary in invariants.json
Opera Numerorum / Battle Plan v1.6

Scans every module in certificates/invariants.json, recomputes sha256_source
(and sha256_binary where present) from the on-disk file, and writes the updated
values back to invariants.json in place.

Usage:
    python3 certificates/update_source_shas.py            # update all modules
    python3 certificates/update_source_shas.py module_1 module_2  # selected modules only

    python3 certificates/update_source_shas.py --check    # dry-run: exit 1 if any SHA is stale
    python3 certificates/update_source_shas.py --dry-run  # alias for --check

    python3 certificates/update_source_shas.py --check --invariants-path /tmp/staged.json
        # Check mode reading invariants from a specific path (used by pre-commit hook to
        # read the staged blob rather than the working-tree file).  Source/binary files are
        # still resolved relative to the repo root (current working directory).

Output:
    One line per field examined:
      UPDATED   <key> [sha256_source]: <old_prefix>... -> <new_prefix>...   (write mode)
      STALE     <key> [sha256_source]: <old_prefix>... -> <new_prefix>...   (check mode)
      OK        <key> [sha256_source]: <prefix>...  (no change)
      MISSING   <key> [sha256_source]: <filepath> not found -- skipped
      NO_PATH   <key> [sha256_source]: no source_file/source field -- skipped

Exit code:
    Write mode (default): 0 always.
    Check mode (--check / --dry-run): 0 if all SHAs match; 1 if any are stale.

Note: --invariants-path is only valid in check mode (it implies read-only).
"""

import hashlib
import json
import os
import sys

INVARIANTS_PATH = "certificates/invariants.json"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def short(sha):
    """Return first 16 hex chars for display."""
    return sha[:16] if sha else "(none)"


def process_module(key, val, dry_run=False):
    """
    Recompute sha256_source and sha256_binary for one module entry.

    Returns a list of result dicts:
      {field, filepath, old_sha, new_sha, status}
      status in: "updated", "ok", "missing", "no_path"

    Mutates val in place when status == "updated" and dry_run is False.
    """
    results = []

    checks = []

    # sha256_source: path is source_file or source
    if "sha256_source" in val:
        filepath = val.get("source_file") or val.get("source")
        checks.append(("sha256_source", filepath, val["sha256_source"]))

    # sha256_binary: path is binary
    if "sha256_binary" in val:
        filepath = val.get("binary")
        checks.append(("sha256_binary", filepath, val["sha256_binary"]))

    for field, filepath, old_sha in checks:
        if not filepath:
            results.append({
                "field": field,
                "filepath": None,
                "old_sha": old_sha,
                "new_sha": None,
                "status": "no_path",
            })
            continue

        if not os.path.exists(filepath):
            results.append({
                "field": field,
                "filepath": filepath,
                "old_sha": old_sha,
                "new_sha": None,
                "status": "missing",
            })
            continue

        new_sha = sha256_file(filepath)
        if new_sha == old_sha:
            results.append({
                "field": field,
                "filepath": filepath,
                "old_sha": old_sha,
                "new_sha": new_sha,
                "status": "ok",
            })
        else:
            if not dry_run:
                val[field] = new_sha
            results.append({
                "field": field,
                "filepath": filepath,
                "old_sha": old_sha,
                "new_sha": new_sha,
                "status": "updated",
            })

    return results


def main():
    args = sys.argv[1:]

    # Detect --check / --dry-run flag
    dry_run = False
    if "--check" in args or "--dry-run" in args:
        dry_run = True
        args = [a for a in args if a not in ("--check", "--dry-run")]

    # Detect --invariants-path PATH (only valid in check/dry-run mode)
    invariants_path = INVARIANTS_PATH
    if "--invariants-path" in args:
        idx = args.index("--invariants-path")
        if idx + 1 >= len(args):
            print("ERROR: --invariants-path requires a path argument", file=sys.stderr)
            sys.exit(2)
        invariants_path = args[idx + 1]
        args = args[:idx] + args[idx + 2:]
        if not dry_run:
            print(
                "ERROR: --invariants-path is only valid in check mode (--check / --dry-run).",
                file=sys.stderr,
            )
            sys.exit(2)

    if not os.path.exists(invariants_path):
        print(f"ERROR: {invariants_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(invariants_path) as f:
        data = json.load(f)

    filter_keys = set(args) if args else None

    if filter_keys:
        missing_keys = filter_keys - set(data.keys())
        if missing_keys:
            print(f"WARNING: keys not found in invariants.json: {', '.join(sorted(missing_keys))}")

    header = "Opera Numerorum -- update_source_shas.py"
    if dry_run:
        suffix = " [CHECK MODE -- no writes"
        if invariants_path != INVARIANTS_PATH:
            suffix += f", reading {invariants_path}"
        suffix += "]"
        header += suffix
    print(header)
    print("=" * 64)

    total = updated = ok = missing = no_path = 0

    for key, val in data.items():
        if not isinstance(val, dict):
            continue
        if filter_keys and key not in filter_keys:
            continue

        results = process_module(key, val, dry_run=dry_run)
        for r in results:
            total += 1
            s = r["status"]
            field = r["field"]
            if s == "updated":
                updated += 1
                label = "STALE   " if dry_run else "UPDATED "
                print(
                    f"  {label} {key} [{field}]: "
                    f"{short(r['old_sha'])}... -> {short(r['new_sha'])}..."
                )
            elif s == "ok":
                ok += 1
                print(f"  OK       {key} [{field}]: {short(r['old_sha'])}...")
            elif s == "missing":
                missing += 1
                print(f"  MISSING  {key} [{field}]: {r['filepath']} not found -- skipped")
            elif s == "no_path":
                no_path += 1
                print(f"  NO_PATH  {key} [{field}]: no source_file/source field -- skipped")

    print()
    print("=" * 64)
    print(
        f"Fields examined: {total}  |  "
        f"{'STALE' if dry_run else 'UPDATED'}: {updated}  |  OK: {ok}  |  "
        f"MISSING: {missing}  |  NO_PATH: {no_path}"
    )

    if dry_run:
        if updated > 0:
            print(
                f"\nCHECK FAILED: {updated} source SHA(s) are stale in invariants.json.\n"
                "Run: python3 certificates/update_source_shas.py\n"
                "Then re-stage invariants.json before committing."
            )
            sys.exit(1)
        else:
            print("\nCHECK PASSED: all source SHAs are current.")
        return

    if updated == 0:
        print("\nNo changes -- invariants.json is already up to date.")
        return

    # Write the patched data back atomically via a temp file
    tmp_path = INVARIANTS_PATH + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    os.replace(tmp_path, INVARIANTS_PATH)
    print(f"\nPatched {updated} field(s) in {INVARIANTS_PATH}.")
    print("Run 'python3 certificates/check_invariants.py' to verify the full chain.")


if __name__ == "__main__":
    main()
