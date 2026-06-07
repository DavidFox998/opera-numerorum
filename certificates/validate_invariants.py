#!/usr/bin/env python3
"""
validate_invariants.py -- SHA field format checker for Opera Numerorum
Battle Plan v1.6

Walks every key in certificates/invariants.json (recursively into nested
dicts and lists) and checks that any field whose name looks like a SHA-256
field contains exactly 64 lowercase hex characters.

Covered field-name patterns  (regex: sha256_.+ | .+_sha | .+_sha256):
  sha256_source, sha256_stdout, sha256_pdf, sha256_binary, sha256_script,
  sha256_builder, sha256_primes_stdout, sha256_audit_stdout,
  sha256_lambda_stdout, stdout_sha, stdout_sha256, manifest_sha,
  file_sha, script_sha, pdf_sha, builder_sha, causal_parent_sha, ...

----------------------------------------------------------------------------
EXEMPTION TABLE  (single authoritative place -- see EXEMPTIONS below)
----------------------------------------------------------------------------

To add a new annotation field (free text, not a real SHA):
  Append one entry to EXEMPTIONS["free_text"]  -- key name -> reason string.

To add a new short-SHA field (abbreviated hex prefix stored at a specific
JSON path):
  Append one entry to EXEMPTIONS["short_sha"]  -- full dot-path ->
  (min_hex_chars, max_hex_chars, reason).  Using the full path rather than
  just the key name means the same key name appearing elsewhere in the JSON
  is still subject to the normal 64-char rule.

Free-text fields are silently skipped (exempt by design).
Short-SHA fields produce WARN rather than FAIL so the validator still exits
0 but draws attention to them.

A null value for causal_parent_sha is accepted because some modules have
no causal parent.

----------------------------------------------------------------------------
FIXTURE CONTRACT  (enforced at import time -- see EXEMPTIONS_FIXTURES below)
----------------------------------------------------------------------------

Every entry in EXEMPTIONS must have a parallel entry in EXEMPTIONS_FIXTURES
supplying a representative sample value.  EXEMPTIONS_FIXTURES mirrors the
two-category layout of EXEMPTIONS exactly:

  EXEMPTIONS_FIXTURES["free_text"][key]      -- any non-SHA string sample
  EXEMPTIONS_FIXTURES["short_sha"][dot_path] -- a valid short hex string of
                                                length >= lo for that path

Why: fixtures let _self_test() exercise the real validator logic against a
known-good value, ensuring the behavioural tests stay in sync with the
registered exemptions.  Without a fixture, the test can only verify that the
entry exists, not that the validator handles it correctly.

Enforcement: a module-level guard (_check_fixture_coverage) runs at import
time and raises RuntimeError if any EXEMPTIONS entry has no fixture.  This
makes it structurally impossible to add a new EXEMPTIONS entry without also
providing the matching fixture -- the module will refuse to import.

To add a new annotation field:
  1. Append to EXEMPTIONS["free_text"]           -- key name -> reason string
  2. Append to EXEMPTIONS_FIXTURES["free_text"]  -- key name -> sample string

To add a new short-SHA path:
  1. Append to EXEMPTIONS["short_sha"]           -- dot_path -> (lo, hi, reason)
  2. Append to EXEMPTIONS_FIXTURES["short_sha"]  -- dot_path -> valid hex string
                                                    of length >= lo

No other code change is required.

Usage:
    python3 certificates/validate_invariants.py                   # default path
    python3 certificates/validate_invariants.py /path/to/file     # explicit path
    python3 certificates/validate_invariants.py --self-test       # internal regression

The optional path argument lets callers (e.g. pre-commit hooks) pass a temp
file extracted from the Git index, so the staged snapshot is validated rather
than the working-tree file.

Exit code: 0 if all non-exempt SHA fields are well-formed, 1 otherwise.
"""

import json
import re
import sys

INVARIANTS_PATH = "certificates/invariants.json"

SHA_KEY_RE = re.compile(r'^(sha256_.+|.+_sha|.+_sha256)$')
SHA_VALUE_RE = re.compile(r'^[0-9a-f]{64}$')

NULLABLE_KEYS = {
    "causal_parent_sha",
}

# ---------------------------------------------------------------------------
# EXEMPTIONS -- the single place to register all SHA-field exceptions.
#
# Two categories:
#
#   "free_text"  -- key names (matched anywhere in the JSON) that hold
#                   human-readable annotations rather than real SHA digests.
#                   Validator silently skips these.
#
#   "short_sha"  -- full JSON dot-paths (as produced by walk()) that hold
#                   intentional abbreviated SHA prefixes (e.g. git short-SHAs).
#                   Format: dot_path -> (min_hex_chars, max_hex_chars, reason)
#                   Convention: git-style 8-char prefix -> (7, 16) gives
#                   headroom for both short (7-char) and medium refs.
#                   Validator emits WARN (not FAIL) for these.
#
# To add a new annotation field:  append to "free_text".
# To add a new short-SHA path:    append to "short_sha".
# No other code change is required in either case.
# ---------------------------------------------------------------------------
EXEMPTIONS: dict[str, dict] = {
    "free_text": {
        "sha256_prefix":         "8-char display abbreviation; full SHA stored in sha256",
        "sha256_pdf_note":       "free-text annotation about a PDF rebuild",
        "sha256_bands_json_note": "free-text annotation about a bands JSON rebuild",
    },
    "short_sha": {
        "lean_chain_TheoremaAureum143.critical_fix.backing_sha": (
            7, 16,
            "git short-SHA backing the critical-fix note in TheoremaAureum143",
        ),
        "addendum_A1.lean_chain.C01_sha": (
            7, 16,
            "Lean chain commit reference -- addendum A1 step C01",
        ),
        "addendum_A1.lean_chain.C07_sha": (
            7, 16,
            "Lean chain commit reference -- addendum A1 step C07",
        ),
    },
}

# ---------------------------------------------------------------------------
# EXEMPTIONS_FIXTURES -- sample values that exercise each EXEMPTIONS entry.
#
# Every entry in EXEMPTIONS must have a matching entry here.  The import-time
# guard below (_check_fixture_coverage) enforces this: if you add to EXEMPTIONS
# without adding here, the module will raise RuntimeError on import.
#
# "free_text" fixtures: any non-SHA string that represents a realistic value.
# "short_sha" fixtures: a valid lowercase hex string of length >= lo for that
#                       path (lo comes from the EXEMPTIONS["short_sha"] tuple).
# ---------------------------------------------------------------------------
EXEMPTIONS_FIXTURES: dict[str, dict] = {
    "free_text": {
        "sha256_prefix":          "a1b2c3d4",
        "sha256_pdf_note":        "rebuilt 2026-05-21 after M5 correction",
        "sha256_bands_json_note": "bands JSON regenerated after sieve extension",
    },
    "short_sha": {
        "lean_chain_TheoremaAureum143.critical_fix.backing_sha": "a1b2c3d",
        "addendum_A1.lean_chain.C01_sha":                        "a1b2c3d",
        "addendum_A1.lean_chain.C07_sha":                        "a1b2c3d",
    },
}


def _check_fixture_coverage() -> None:
    """Raise RuntimeError if any EXEMPTIONS entry lacks a fixture.

    Called once at module import time so that adding to EXEMPTIONS without
    also adding to EXEMPTIONS_FIXTURES is structurally impossible: the module
    refuses to import until both dictionaries are in sync.
    """
    missing: list[str] = []
    for ft_key in EXEMPTIONS["free_text"]:
        if ft_key not in EXEMPTIONS_FIXTURES["free_text"]:
            missing.append(f"free_text[{ft_key!r}]")
    for ss_path in EXEMPTIONS["short_sha"]:
        if ss_path not in EXEMPTIONS_FIXTURES["short_sha"]:
            missing.append(f"short_sha[{ss_path!r}]")
    if missing:
        raise RuntimeError(
            "EXEMPTIONS_FIXTURES is incomplete -- add a sample value for each "
            "missing entry before using validate_invariants.py:\n  "
            + "\n  ".join(missing)
        )


_check_fixture_coverage()

# Derived lookups (do not edit these -- edit EXEMPTIONS above)
_EXEMPT_KEYS: set[str] = set(EXEMPTIONS["free_text"])
_SHORT_SHA_REGISTRY: dict[str, tuple[int, int]] = {
    path: (lo, hi)
    for path, (lo, hi, _reason) in EXEMPTIONS["short_sha"].items()
}


def is_sha_key(key: str) -> bool:
    return bool(SHA_KEY_RE.match(key))


def walk(obj, path: str, errors: list, warnings: list, skipped: list) -> None:
    """Recursively walk obj, collecting format errors for SHA fields."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            child_path = f"{path}.{k}" if path else k
            if is_sha_key(k):
                _check_sha_field(k, v, child_path, errors, warnings, skipped)
            else:
                walk(v, child_path, errors, warnings, skipped)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]", errors, warnings, skipped)


def _check_sha_field(key, value, path, errors, warnings, skipped):
    if key in _EXEMPT_KEYS:
        reason = EXEMPTIONS["free_text"][key]
        skipped.append((path, repr(value), f"free-text annotation: {reason}"))
        return

    if value is None:
        if key in NULLABLE_KEYS:
            return
        errors.append((path, repr(value), "null not allowed for this SHA key"))
        return

    if not isinstance(value, str):
        errors.append((path, repr(value),
                       f"expected str, got {type(value).__name__}"))
        return

    if SHA_VALUE_RE.match(value):
        return

    if path in _SHORT_SHA_REGISTRY:
        lo, hi = _SHORT_SHA_REGISTRY[path]
        _lo, _hi, reg_reason = EXEMPTIONS["short_sha"][path]
        hex_re = re.compile(rf'^[0-9a-f]{{{lo},{hi}}}$')
        if hex_re.match(value):
            warnings.append((path, value,
                             f"short SHA prefix ({len(value)} chars, "
                             f"registry allows {lo}-{hi}) -- {reg_reason}"))
        else:
            errors.append((path, value,
                           f"registered short-SHA path: value ({len(value)} chars) "
                           f"does not satisfy registry range [{lo},{hi}] "
                           "or contains non-hex characters -- "
                           "fix the value or update EXEMPTIONS['short_sha']"))
        return

    reason = (
        f"length {len(value)} (expected 64)"
        if len(value) != 64
        else "contains non-hex characters"
    )
    errors.append((path, value, reason))


def count_sha_fields(obj) -> int:
    total = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if is_sha_key(k):
                total += 1
            else:
                total += count_sha_fields(v)
    elif isinstance(obj, list):
        for v in obj:
            total += count_sha_fields(v)
    return total


def main(path: str | None = None) -> None:
    target = path or INVARIANTS_PATH
    try:
        with open(target) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {target} not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: {target} is not valid JSON: {exc}",
              file=sys.stderr)
        sys.exit(1)

    errors: list = []
    warnings: list = []
    skipped: list = []

    walk(data, "", errors, warnings, skipped)

    total = count_sha_fields(data)

    print("Opera Numerorum -- invariants.json SHA format validation")
    print("=" * 60)

    free_text = EXEMPTIONS["free_text"]
    short_sha = EXEMPTIONS["short_sha"]

    print(f"Free-text annotation fields ({len(free_text)} registered key(s)):")
    for key, reason in free_text.items():
        print(f"  {key}")
        print(f"    reason: {reason}")

    print(f"Short-SHA registry ({len(short_sha)} registered path(s)):")
    for reg_path, (lo, hi, reason) in short_sha.items():
        print(f"  [{lo},{hi}]  {reg_path}")
        print(f"    reason: {reason}")

    print("=" * 60)

    if warnings:
        for path, value, reason in warnings:
            print(f"  WARN     {path}")
            print(f"           value:  {value!r}")
            print(f"           reason: {reason}")

    if errors:
        for path, value, reason in errors:
            print(f"  INVALID  {path}")
            print(f"           value:  {value!r}")
            print(f"           reason: {reason}")
        print("=" * 60)
        msg_parts = [f"{len(errors)} bad SHA field(s)"]
        if warnings:
            msg_parts.append(f"{len(warnings)} warning(s)")
        if skipped:
            msg_parts.append(f"{len(skipped)} exempt annotation field(s) skipped")
        print(f"\nFORMAT VALIDATION FAILED -- {', '.join(msg_parts)}")
        sys.exit(1)
    else:
        good = total - len(warnings) - len(skipped)
        print(f"  {good} SHA fields pass /^[0-9a-f]{{64}}$/ format check", end="")
        if warnings:
            print(f"  ({len(warnings)} short-SHA warning(s))", end="")
        if skipped:
            print(f"  ({len(skipped)} exempt annotation field(s) skipped)", end="")
        print()
        print("=" * 60)
        if warnings:
            print(f"\nFORMAT VALIDATION PASS (with {len(warnings)} short-SHA warning(s) -- see above)")
        else:
            print(f"\nFORMAT VALIDATION PASS")
        sys.exit(0)


def _self_test() -> None:
    """Regression tests for EXEMPTIONS logic.  Run via --self-test.

    Coverage:
      0. Fixture-coverage check: every EXEMPTIONS entry has a fixture in
         EXEMPTIONS_FIXTURES.  This runs first; a missing fixture is a FAIL
         before any behavioural check executes.
      1. Every free_text key: validator must silently skip it (no error, no
         warning).  Sample value comes from EXEMPTIONS_FIXTURES["free_text"].
      2. Every short_sha path:
           * The fixture value (valid hex of length >= lo) -> WARN (not ERROR).
           * A non-hex / too-short string                  -> ERROR.
           * The same key name at an unregistered path     -> ERROR (full 64-char
             rule applies outside the registered path).
    """
    errors: list = []
    warnings: list = []
    skipped: list = []

    total_pass = 0
    total_fail = 0
    fail_messages: list[str] = []

    def _ok(label: str) -> None:
        nonlocal total_pass
        total_pass += 1
        print(f"  PASS  {label}")

    def _fail(label: str, detail: str) -> None:
        nonlocal total_fail
        total_fail += 1
        msg = f"  FAIL  {label} -- {detail}"
        fail_messages.append(msg)
        print(msg)

    # -----------------------------------------------------------------------
    # 0. Fixture coverage check -- must pass before behavioural tests run
    # -----------------------------------------------------------------------
    print("fixture coverage check:")
    missing_fixtures: list[str] = []
    for ft_key in EXEMPTIONS["free_text"]:
        if ft_key not in EXEMPTIONS_FIXTURES["free_text"]:
            missing_fixtures.append(f"free_text[{ft_key!r}]")
    for ss_path in EXEMPTIONS["short_sha"]:
        if ss_path not in EXEMPTIONS_FIXTURES["short_sha"]:
            missing_fixtures.append(f"short_sha[{ss_path!r}]")
    if missing_fixtures:
        for entry in missing_fixtures:
            _fail(f"fixture coverage: {entry}", "missing from EXEMPTIONS_FIXTURES")
    else:
        _ok(f"all {len(EXEMPTIONS['free_text'])} free_text + "
            f"{len(EXEMPTIONS['short_sha'])} short_sha entries have fixtures")

    # -----------------------------------------------------------------------
    # 1. free_text tests: every registered key must be silently skipped
    # -----------------------------------------------------------------------
    print(f"free_text tests ({len(EXEMPTIONS['free_text'])} key(s)):")
    for ft_key in EXEMPTIONS["free_text"]:
        errors.clear(); warnings.clear(); skipped.clear()
        sample_val = EXEMPTIONS_FIXTURES["free_text"].get(ft_key, "fixture-missing")
        _check_sha_field(ft_key, sample_val,
                         f"module_x.{ft_key}", errors, warnings, skipped)
        label = f"free_text[{ft_key!r}]"
        if errors:
            _fail(label, f"produced unexpected error(s): {errors}")
        elif warnings:
            _fail(label, f"produced unexpected warning(s): {warnings}")
        elif len(skipped) != 1:
            _fail(label, f"expected 1 skipped entry, got {skipped}")
        else:
            _ok(label)

    # -----------------------------------------------------------------------
    # 2. short_sha tests: every registered path gets three sub-tests
    # -----------------------------------------------------------------------
    print(f"short_sha tests ({len(EXEMPTIONS['short_sha'])} path(s)):")
    for reg_path, (lo, hi, _reason) in EXEMPTIONS["short_sha"].items():
        key = reg_path.split(".")[-1]

        # (a) Fixture value at the registered path -> WARN, no ERROR
        errors.clear(); warnings.clear(); skipped.clear()
        good_val = EXEMPTIONS_FIXTURES["short_sha"].get(reg_path, "a" * lo)
        _check_sha_field(key, good_val, reg_path, errors, warnings, skipped)
        label_a = f"short_sha[{reg_path!r}] fixture-value -> WARN"
        if errors:
            _fail(label_a, f"produced error(s): {errors}")
        elif len(warnings) != 1:
            _fail(label_a, f"expected 1 warning, got {warnings}")
        else:
            _ok(label_a)

        # (b) Non-hex / invalid value at the registered path -> ERROR
        errors.clear(); warnings.clear(); skipped.clear()
        bad_val = "zz"
        _check_sha_field(key, bad_val, reg_path, errors, warnings, skipped)
        label_b = f"short_sha[{reg_path!r}] invalid-value -> ERROR"
        if len(errors) != 1:
            _fail(label_b, f"expected 1 error, got errors={errors} warnings={warnings}")
        else:
            _ok(label_b)

        # (c) Same key name at an unregistered path -> ERROR (full 64-char rule)
        errors.clear(); warnings.clear(); skipped.clear()
        unregistered_path = f"some.other.section.{key}"
        _check_sha_field(key, good_val, unregistered_path, errors, warnings, skipped)
        label_c = f"short_sha[{reg_path!r}] unregistered-path -> ERROR"
        if len(errors) != 1:
            _fail(label_c,
                  f"short value at unregistered path should error; "
                  f"got errors={errors} warnings={warnings}")
        else:
            _ok(label_c)

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print()
    print(f"self-test results: {total_pass} pass, {total_fail} fail")
    if total_fail:
        for msg in fail_messages:
            print(msg, file=sys.stderr)
        raise SystemExit(1)
    print("EXEMPTIONS self-test PASS (all free_text keys + all short_sha paths covered)")


if __name__ == "__main__":
    import sys as _sys
    args = _sys.argv[1:]
    if args == ["--self-test"]:
        _self_test()
    elif args and not args[0].startswith("-"):
        main(path=args[0])
    else:
        main()
