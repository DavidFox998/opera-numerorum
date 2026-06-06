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

Explicit exemptions (field names that match the pattern but are NOT full
64-char SHA-256 values by design):
  sha256_prefix    -- 8-char display abbreviation; full SHA stored in sha256
  sha256_pdf_note  -- free-text annotation about a PDF rebuild

Short-SHA exemptions (field names that store deliberate git-style 8-char
SHA prefixes -- flagged as WARN rather than FAIL so the validator still
exits 0 but draws attention to them):
  backing_sha, C01_sha, C07_sha

A null value for causal_parent_sha is accepted because some modules have
no causal parent.

Usage:
    python3 certificates/validate_invariants.py

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

EXEMPT_KEYS = {
    "sha256_prefix",
    "sha256_pdf_note",
}

SHORT_SHA_KEYS = {
    "backing_sha",
    "C01_sha",
    "C07_sha",
}

SHORT_SHA_RE = re.compile(r'^[0-9a-f]{7,63}$')


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
    if key in EXEMPT_KEYS:
        skipped.append((path, repr(value), "exempt by design"))
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

    if key in SHORT_SHA_KEYS and SHORT_SHA_RE.match(value):
        warnings.append((path, value,
                         f"short SHA prefix ({len(value)} chars) -- "
                         "intentional abbreviation? consider storing full 64-char hash"))
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


def main() -> None:
    try:
        with open(INVARIANTS_PATH) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {INVARIANTS_PATH} not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: {INVARIANTS_PATH} is not valid JSON: {exc}",
              file=sys.stderr)
        sys.exit(1)

    errors: list = []
    warnings: list = []
    skipped: list = []

    walk(data, "", errors, warnings, skipped)

    total = count_sha_fields(data)

    print("Opera Numerorum -- invariants.json SHA format validation")
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
            msg_parts.append(f"{len(skipped)} exempt field(s) skipped")
        print(f"\nFORMAT VALIDATION FAILED -- {', '.join(msg_parts)}")
        sys.exit(1)
    else:
        good = total - len(warnings) - len(skipped)
        print(f"  {good} SHA fields pass /^[0-9a-f]{{64}}$/ format check", end="")
        if warnings:
            print(f"  ({len(warnings)} short-SHA warning(s))", end="")
        if skipped:
            print(f"  ({len(skipped)} exempt field(s) skipped)", end="")
        print()
        print("=" * 60)
        if warnings:
            print(f"\nFORMAT VALIDATION PASS (with {len(warnings)} short-SHA warning(s) -- see above)")
        else:
            print(f"\nFORMAT VALIDATION PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
