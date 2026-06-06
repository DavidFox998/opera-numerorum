#!/usr/bin/env python3
"""
check_invariants.py -- Pre-flight SHA checker for Opera Numerorum
Battle Plan v1.6

Reads certificates/invariants.json, recomputes the SHA-256 of every
certified *.out file, and compares against the stored value.

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


def extract_checks(key, val):
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


def run_checks(data, filter_keys=None):
    total = 0
    passed = 0
    failed = 0
    missing = 0

    for key, val in data.items():
        if not isinstance(val, dict):
            continue
        if filter_keys and key not in filter_keys:
            continue

        checks = extract_checks(key, val)
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

    total, passed, failed, missing = run_checks(data, filter_keys)

    print(f"{'=' * 60}")
    print(f"Total checks: {total}  |  PASS: {passed}  |  FAIL: {failed}  |  MISSING: {missing}")

    if failed > 0 or missing > 0:
        print(f"\nPRE-FLIGHT FAILED -- {failed} SHA mismatch(es), {missing} missing file(s)")
        sys.exit(1)
    elif total == 0:
        print(f"\nWARNING: no stdout checks found (check key names)")
        sys.exit(1)
    else:
        print(f"\nPRE-FLIGHT PASS -- all {passed} stdout SHAs match invariants.json")
        sys.exit(0)


if __name__ == "__main__":
    main()
