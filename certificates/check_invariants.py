#!/usr/bin/env python3
"""
check_invariants.py -- Pre-flight SHA checker for Opera Numerorum
Battle Plan v1.6

Reads certificates/invariants.json, recomputes the SHA-256 of every
certified *.out file AND every recorded source/binary file, and compares
against the stored values.

Pass 1 (stdout checks):  sha256_stdout / stdout_sha / stdout_sha256 fields
Pass 2 (source checks):  sha256_source (+ source_file) and
                          sha256_binary (+ binary) fields

Usage:
    python3 certificates/check_invariants.py          # check all modules
    python3 certificates/check_invariants.py module_1 # check one module

Exit code: 0 if all PASS, 1 if any mismatch or missing file.
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


# ---------------------------------------------------------------------------
# Pass 1: stdout checks
# ---------------------------------------------------------------------------

def extract_stdout_checks(key, val):
    """
    Return a list of (label, filepath, stored_sha) tuples for every
    stdout file recorded in this module entry.

    Handles all SHA-field naming conventions found in invariants.json:
      sha256_stdout  + stdout_file   (most modules)
      sha256_stdout  + stdout_path   (z_tower_v3)
      stdout_sha     + stdout        (M9, bdp_lemmas, pvsnp_tower)
      stdout_sha256  + stdout/stdout_file  (M8L, M8M, m8c..m8m)
      sha256_audit_stdout + stdout_file_audit  (module_m8a)
      sha256_lambda_stdout + stdout_file_lambda (module_m8a)
      p5_replacement_stdout_sha (wall256_ym_report -- implied file)
    """
    checks = []

    def _add(filepath, sha, label_suffix=""):
        label = key + (f" [{label_suffix}]" if label_suffix else "")
        checks.append((label, filepath, sha))

    # --- pattern 1: sha256_stdout + stdout_file or stdout_path ---
    if "sha256_stdout" in val:
        filepath = val.get("stdout_file") or val.get("stdout_path") or val.get("stdout")
        if filepath:
            _add(filepath, val["sha256_stdout"])

    # --- pattern 2: stdout_sha + stdout ---
    if "stdout_sha" in val:
        filepath = val.get("stdout") or val.get("stdout_file")
        if filepath:
            _add(filepath, val["stdout_sha"])

    # --- pattern 3: stdout_sha256 + stdout or stdout_file ---
    if "stdout_sha256" in val:
        filepath = val.get("stdout") or val.get("stdout_file")
        if filepath:
            _add(filepath, val["stdout_sha256"])

    # --- pattern 4: module_m8a split audit / lambda ---
    if "sha256_audit_stdout" in val and "stdout_file_audit" in val:
        _add(val["stdout_file_audit"], val["sha256_audit_stdout"], "audit")
    if "sha256_lambda_stdout" in val and "stdout_file_lambda" in val:
        _add(val["stdout_file_lambda"], val["sha256_lambda_stdout"], "lambda")

    # --- pattern 5: wall256_ym_report p5_replacement ---
    if "p5_replacement_stdout_sha" in val:
        _add("p5_replacement.out", val["p5_replacement_stdout_sha"], "p5_replacement")

    # Deduplicate: some modules store the same SHA under two different key names
    seen = set()
    unique = []
    for item in checks:
        dedup_key = (item[1], item[2])  # (filepath, sha)
        if dedup_key not in seen:
            seen.add(dedup_key)
            unique.append(item)
    return unique


# ---------------------------------------------------------------------------
# Pass 2: source / binary checks
# ---------------------------------------------------------------------------

def extract_source_checks(key, val):
    """
    Return a list of (label, filepath, stored_sha) tuples for every
    source file and compiled binary recorded in this module entry.

    Only entries that have BOTH a file path AND a stored SHA are included;
    entries with a source_file/source but no sha256_source are skipped
    (nothing to compare against).

    Patterns handled:
      sha256_source + source_file    (most modules)
      sha256_source + source         (bands_269 and rake-style modules)
      sha256_binary + binary         (M2 and any module with a compiled binary)
    """
    checks = []

    if "sha256_source" in val:
        filepath = val.get("source_file") or val.get("source")
        if filepath:
            label = f"{key} [sha256_source]"
            checks.append((label, filepath, val["sha256_source"]))

    if "sha256_binary" in val and "binary" in val:
        label = f"{key} [sha256_binary]"
        checks.append((label, val["binary"], val["sha256_binary"]))

    return checks


def extract_source_warnings(key, val):
    """
    Return a list of (label, filepath) tuples for every source file or
    binary that is recorded in this module entry but has NO corresponding
    SHA field.  These are gaps in the chain: the file could be edited
    without any check detecting the change.
    """
    warnings = []

    # source_file / source present but sha256_source absent
    if "sha256_source" not in val:
        filepath = val.get("source_file") or val.get("source")
        if filepath:
            label = f"{key} [source_file]"
            warnings.append((label, filepath))

    # binary present but sha256_binary absent
    if "sha256_binary" not in val and "binary" in val:
        label = f"{key} [binary]"
        warnings.append((label, val["binary"]))

    return warnings


# ---------------------------------------------------------------------------
# Generic check runner
# ---------------------------------------------------------------------------

def run_checks(data, extractor, filter_keys=None):
    total = 0
    passed = 0
    failed = 0
    missing = 0

    for key, val in data.items():
        if not isinstance(val, dict):
            continue
        if filter_keys and key not in filter_keys:
            continue

        checks = extractor(key, val)
        for label, filepath, stored_sha in checks:
            total += 1
            if not os.path.exists(filepath):
                print(f"  MISSING  {label}: {filepath} not found")
                missing += 1
                continue
            computed = sha256_file(filepath)
            if computed == stored_sha:
                print(f"  PASS     {label}: {filepath}")
                passed += 1
            else:
                print(f"  FAIL     {label}: {filepath}")
                print(f"           stored:   {stored_sha}")
                print(f"           computed: {computed}")
                failed += 1

    return total, passed, failed, missing


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if not os.path.exists(INVARIANTS_PATH):
        print(f"ERROR: {INVARIANTS_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(INVARIANTS_PATH) as f:
        data = json.load(f)

    filter_keys = set(sys.argv[1:]) if len(sys.argv) > 1 else None

    print(f"Opera Numerorum -- invariants.json SHA pre-flight")
    print(f"{'=' * 60}")

    if filter_keys:
        missing_keys = filter_keys - set(data.keys())
        if missing_keys:
            print(f"WARNING: keys not found in invariants.json: {', '.join(sorted(missing_keys))}")

    # ------------------------------------------------------------------
    # Pass 1: stdout SHAs
    # ------------------------------------------------------------------
    print(f"\n--- Pass 1: stdout checks ---")
    s_total, s_passed, s_failed, s_missing = run_checks(
        data, extract_stdout_checks, filter_keys
    )
    print(f"\nStdout checks: {s_total}  |  PASS: {s_passed}  |  FAIL: {s_failed}  |  MISSING: {s_missing}")

    # ------------------------------------------------------------------
    # Pass 2: source / binary SHAs
    # ------------------------------------------------------------------
    print(f"\n--- Pass 2: source / binary checks ---")
    c_total, c_passed, c_failed, c_missing = run_checks(
        data, extract_source_checks, filter_keys
    )

    # Warn about source files that have no SHA recorded at all
    c_warned = 0
    for key, val in data.items():
        if not isinstance(val, dict):
            continue
        if filter_keys and key not in filter_keys:
            continue
        for label, filepath in extract_source_warnings(key, val):
            print(f"  WARN     {label}: {filepath} -- source_file present but no sha256_source recorded")
            c_warned += 1

    print(f"\nSource checks: {c_total}  |  PASS: {c_passed}  |  FAIL: {c_failed}  |  MISSING: {c_missing}  |  WARN: {c_warned}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total   = s_total   + c_total
    passed  = s_passed  + c_passed
    failed  = s_failed  + c_failed
    missing = s_missing + c_missing

    print(f"\n{'=' * 60}")
    print(f"Total checks: {total}  |  PASS: {passed}  |  FAIL: {failed}  |  MISSING: {missing}")

    if failed > 0 or missing > 0:
        parts = []
        if s_failed or s_missing:
            parts.append(f"stdout: {s_failed} mismatch(es), {s_missing} missing")
        if c_failed or c_missing:
            parts.append(f"source/binary: {c_failed} mismatch(es), {c_missing} missing")
        print(f"\nPRE-FLIGHT FAILED -- {'; '.join(parts)}")
        sys.exit(1)
    elif total == 0:
        print(f"\nWARNING: no checks found (check key names)")
        sys.exit(1)
    else:
        print(f"\nPRE-FLIGHT PASS -- all {passed} checks match invariants.json")
        sys.exit(0)


if __name__ == "__main__":
    main()
