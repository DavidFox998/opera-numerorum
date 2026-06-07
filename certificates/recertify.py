#!/usr/bin/env python3
"""
recertify.py -- Opera Numerorum auto-recertify
Battle Plan v1.6

Detects which *.out files have changed relative to certificates/invariants.json,
updates their stored SHAs, re-emits the matching certificate PDF, and when
any of M1-M6 change also re-locks the Module 7 master manifest.

Usage:
    python3 certificates/recertify.py            # check all, rebuild changed
    python3 certificates/recertify.py --dry-run  # report changes, no writes
    python3 certificates/recertify.py --self-check  # verify detection logic, exit
    python3 certificates/recertify.py module_1 module_5  # check specific keys

Exit code: 0 on success (including "nothing to do"), 1 if any build fails.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

INVARIANTS_PATH = "certificates/invariants.json"

# M1-M6 output files whose concatenation forms the Module 7 manifest
M7_MANIFEST_FILES = ["m1.out", "m2.out", "m3.out", "m4.out", "m5.out", "m6.out"]

# ---------------------------------------------------------------------------
# Build script map: invariants.json key -> build script path
# ---------------------------------------------------------------------------
BUILD_SCRIPT_MAP = {
    "module_1":              "certificates/build_module_1.py",
    "module_2":              "certificates/build_module_2.py",
    "module_3":              "certificates/build_module_3.py",
    "module_4":              "certificates/build_module_4.py",
    "module_5":              "certificates/build_module_5.py",
    "module_6":              "certificates/build_module_6.py",
    "module_6_3":            "certificates/build_module_6_3.py",
    "module_7":              "certificates/build_module_7.py",
    "module_8":              "certificates/build_module_8.py",
    "M9":                    "certificates/build_module_9.py",
    "module_9_all":          "certificates/build_module_9_all.py",
    "module_10":             "certificates/build_module_10.py",
    "module_14":             "certificates/build_module_14.py",
    "module_15":             "certificates/build_module_15.py",
    "module_16":             "certificates/build_module_16.py",
    "module_17":             "certificates/build_module_17.py",
    "module_18":             "certificates/build_module_18.py",
    "module_19":             "certificates/build_module_19.py",
    "module_20":             "certificates/build_module_20.py",
    "module_24":             "certificates/build_module_24.py",
    "module_25":             "certificates/build_module_25.py",
    "module_25b":            "certificates/build_module_25b.py",
    "module_26":             "certificates/build_module_26.py",
    "module_m8a":            "certificates/build_module_m8a.py",
    "module_m8g":            "certificates/build_module_m8g.py",
    "module_m8g_correction": "certificates/build_module_M8G_Correction.py",
    "module_m8h":            "certificates/build_module_M8H.py",
    "module_m8i":            "certificates/build_module_M8I.py",
    "module_m8j":            "certificates/build_module_m8j.py",
    "module_m8k":            "certificates/build_module_m8k.py",
    "M8L":                   "certificates/build_module_m8l.py",
    "M8M":                   "certificates/build_module_m8m.py",
    "M8N":                   "certificates/build_module_m8n.py",
    "M8O":                   "certificates/build_module_m8o.py",
    "M8P":                   "certificates/build_module_m8p.py",
    "M8Q":                   "certificates/build_module_m8q.py",
    "module_M8R":            "certificates/build_module_M8R.py",
    # bdp lemmas all share one build script
    "bdp_lemma1":            "certificates/build_module_bdp.py",
    "bdp_lemma2":            "certificates/build_module_bdp.py",
    "bdp_lemma3":            "certificates/build_module_bdp.py",
    "bdp_lemma4":            "certificates/build_module_bdp.py",
    # tower PDFs
    "rh_tower":              "certificates/build_rh_tower.py",
    "bsd_tower":             "certificates/build_bsd_tower.py",
    "ns_tower":              "certificates/build_ns_tower.py",
    "ms_tower":              "certificates/build_ms_tower.py",
    "pvsnp_tower":           "certificates/build_pvsnp_tower.py",
    # extended certifications
    "p5_bridge_certificate": "certificates/build_p5_bridge.py",
    "addendum_A1":           "certificates/build_bands_269.py",
    "chronarithmetica":      "certificates/build_chronarithmetica.py",
    "wall256_ym_report":     "certificates/build_wall256_ym.py",
    "tendon_a":              "certificates/build_tendon_a.py",
    "tendon_b":              "certificates/build_tendon_b.py",
    "clay_card":                        "certificates/build_clay_card.py",
    "morningstar_engineering_spec_v2":  "certificates/build_morningstar_engineering_spec_v2.py",
    "morningstar_feasibility_study":    "certificates/build_morningstar_feasibility_study.py",
    "module_m23":                       "certificates/build_module_m23.py",
    "module_m21":                       "certificates/build_module_m21.py",
}

# ---------------------------------------------------------------------------
# PDF path map: invariants.json key -> known PDF output path
# Used when the module entry does not have an explicit 'pdf' field.
# ---------------------------------------------------------------------------
PDF_PATH_MAP = {
    "module_1":      "certificates/Module_1_Certificate.pdf",
    "module_2":      "certificates/Module_2_Certificate.pdf",
    "module_3":      "certificates/Module_3_Certificate.pdf",
    "module_4":      "certificates/Module_4_Certificate.pdf",
    "module_5":      "certificates/Module_5_Certificate.pdf",
    "module_6":      "certificates/Module_6_Certificate.pdf",
    "module_6_3":    "certificates/Module_6_3_Certificate.pdf",
    "module_7":      "certificates/Module_7_Certificate.pdf",
    "module_8":      "certificates/Module_8_Certificate.pdf",
    "module_9_all":  "certificates/Module_9_All_140.pdf",
    "module_10":     "certificates/Module_10_Genus33.pdf",
    "module_14":     "certificates/Module_14_S4_Quaternions.pdf",
    "module_15":     "certificates/Module_15_Delta_Boost.pdf",
    "module_16":     "certificates/Module_16_c_Bridge.pdf",
    "module_17":     "certificates/Module_17_Cert_Patch.pdf",
    "module_18":     "certificates/Module_18_Resonance_Ladder.pdf",
    "module_19":     "certificates/Module_19_p6_Prediction.pdf",
    "module_20":     "certificates/Module_20_p7_Prediction.pdf",
    "module_21":     "certificates/Module_21_H4_Invariant.pdf",
    "module_22":     "certificates/Module_22_MStar_Definition.pdf",
    "module_23":     "certificates/Module_23_BSD_J0_143.pdf",
    "module_24":     "certificates/Module_24_Certificate.pdf",
    "module_25":     "certificates/Module_25_Certificate.pdf",
    "module_25b":    "certificates/Module_25B_Certificate.pdf",
    "module_26":     "certificates/Module_26_Certificate.pdf",
    "bsd_tower":     "certificates/BSD_Tower_Certificate.pdf",
    "ns_tower":      "certificates/NS_Tower_Certificate.pdf",
    "rh_tower":      "certificates/RH_Tower_Certificate.pdf",
    "ms_tower":      "certificates/MS_Tower_Certificate.pdf",
    "pvsnp_tower":   "certificates/PvsNP_Tower_Certificate.pdf",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_manifest():
    """Compute SHA256(cat m1.out m2.out m3.out m4.out m5.out m6.out)."""
    h = hashlib.sha256()
    for fname in M7_MANIFEST_FILES:
        if not os.path.exists(fname):
            return None
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    return h.hexdigest()


def get_stdout_entries(key, entry):
    """
    Return list of (sha_field, file_field, filepath, stored_sha) for all
    stdout files recorded in this module entry.  Mirrors the naming
    conventions understood by check_invariants.py.
    """
    results = []

    def _add(sha_field, file_field, filepath, stored_sha):
        if filepath and stored_sha:
            results.append((sha_field, file_field, filepath, stored_sha))

    # Pattern 1: sha256_stdout + stdout_file / stdout_path / stdout
    if "sha256_stdout" in entry:
        fp = entry.get("stdout_file") or entry.get("stdout_path") or entry.get("stdout")
        _add("sha256_stdout", "stdout_file", fp, entry["sha256_stdout"])

    # Pattern 2: stdout_sha + stdout / stdout_file
    if "stdout_sha" in entry:
        fp = entry.get("stdout") or entry.get("stdout_file")
        _add("stdout_sha", "stdout_file", fp, entry["stdout_sha"])

    # Pattern 3: stdout_sha256 + stdout / stdout_file
    if "stdout_sha256" in entry:
        fp = entry.get("stdout") or entry.get("stdout_file")
        _add("stdout_sha256", "stdout_file", fp, entry["stdout_sha256"])

    # Pattern 4: module_m8a split audit / lambda
    if "sha256_audit_stdout" in entry and "stdout_file_audit" in entry:
        _add("sha256_audit_stdout", "stdout_file_audit",
             entry["stdout_file_audit"], entry["sha256_audit_stdout"])
    if "sha256_lambda_stdout" in entry and "stdout_file_lambda" in entry:
        _add("sha256_lambda_stdout", "stdout_file_lambda",
             entry["stdout_file_lambda"], entry["sha256_lambda_stdout"])

    # Deduplicate by (filepath, stored_sha)
    seen = set()
    unique = []
    for item in results:
        k = (item[2], item[3])
        if k not in seen:
            seen.add(k)
            unique.append(item)
    return unique


def get_pdf_path(key, entry):
    """Return the expected PDF output path for this module, or None."""
    if "pdf" in entry and isinstance(entry["pdf"], str):
        return entry["pdf"]
    if "pdf_file" in entry and isinstance(entry["pdf_file"], str):
        return entry["pdf_file"]
    return PDF_PATH_MAP.get(key)


def get_pdf_sha_field(entry):
    """Return the name of the PDF-SHA field used in this entry, or None."""
    if "sha256_pdf" in entry:
        return "sha256_pdf"
    if "pdf_sha" in entry:
        return "pdf_sha"
    return None


def get_build_script(key, entry):
    """Return build script path from entry['builder'] or BUILD_SCRIPT_MAP."""
    if "builder" in entry and isinstance(entry["builder"], str):
        script = entry["builder"]
        if script.endswith(".py") or script.endswith(".sh"):
            return script
    return BUILD_SCRIPT_MAP.get(key)


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def scan_changes(data, filter_keys=None):
    """
    Walk invariants.json entries and return a list of dicts, one per
    changed (or missing) stdout file.
    status is one of: "changed", "missing", "ok"
    """
    changes = []
    for key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        if filter_keys and key not in filter_keys:
            continue

        for sha_field, file_field, filepath, stored_sha in get_stdout_entries(key, entry):
            if not os.path.exists(filepath):
                changes.append({
                    "key": key, "sha_field": sha_field, "file_field": file_field,
                    "filepath": filepath, "stored_sha": stored_sha,
                    "computed_sha": None, "status": "missing",
                })
                continue
            computed = sha256_file(filepath)
            status = "changed" if computed != stored_sha else "ok"
            changes.append({
                "key": key, "sha_field": sha_field, "file_field": file_field,
                "filepath": filepath, "stored_sha": stored_sha,
                "computed_sha": computed, "status": status,
            })
    return changes


def run_build(key, entry, dry_run):
    """
    Run the build script for this module.  Returns (success, message).
    success=True  -> built ok
    success=False -> build failed
    success=None  -> skipped (dry-run or no script)
    """
    script = get_build_script(key, entry)
    if not script:
        return None, "no build script registered"
    if not os.path.exists(script):
        return False, f"build script not found: {script}"
    if dry_run:
        return None, f"[dry-run] would run: python3 {script}"

    if script.endswith(".py"):
        cmd = ["python3", script]
    elif script.endswith(".sh"):
        cmd = ["bash", script]
    else:
        cmd = [script]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return False, (
            f"FAILED (exit {result.returncode}):\n"
            f"  stdout: {result.stdout.strip()[:400]}\n"
            f"  stderr: {result.stderr.strip()[:400]}"
        )
    return True, "OK (exit 0)"


def update_pdf_sha(key, entry, data, dry_run):
    """
    After a successful build, recompute sha256_pdf and patch invariants entry.
    Returns a status string or None if not applicable.
    """
    pdf_path = get_pdf_path(key, entry)
    if not pdf_path:
        return None
    if not os.path.exists(pdf_path):
        return f"PDF not found after build: {pdf_path}"

    new_sha = sha256_file(pdf_path)
    sha_field = get_pdf_sha_field(entry)
    if not sha_field:
        return None

    old_sha = entry.get(sha_field, "")
    if new_sha == old_sha:
        return f"sha256_pdf unchanged ({new_sha[:16]}...)"

    if not dry_run:
        data[key][sha_field] = new_sha

    return f"sha256_pdf {old_sha[:16]}... -> {new_sha[:16]}..."


# ---------------------------------------------------------------------------
# M7 manifest re-lock
# ---------------------------------------------------------------------------

M1_TO_M6_KEYS = {"module_1", "module_2", "module_3",
                  "module_4", "module_5", "module_6"}


def relock_m7_manifest(data, dry_run, verbose=True):
    """
    Recompute SHA256(cat m1.out...m6.out) and update module_7.manifest_sha
    in data.  Then rebuild Module_7_Certificate.pdf.

    Returns a dict:
        {manifest_sha, old_manifest_sha, changed, build_ok, build_msg, pdf_note}
    """
    new_manifest = sha256_manifest()
    if new_manifest is None:
        return {"changed": False, "build_ok": None,
                "build_msg": "one or more m1..m6.out files missing -- skipped"}

    m7 = data.get("module_7", {})
    old_manifest = m7.get("manifest_sha", "")

    result = {
        "manifest_sha": new_manifest,
        "old_manifest_sha": old_manifest,
        "changed": new_manifest != old_manifest,
        "build_ok": None,
        "build_msg": "",
        "pdf_note": None,
    }

    if not result["changed"]:
        result["build_msg"] = "manifest unchanged -- M7 rebuild skipped"
        return result

    if verbose:
        print(f"  M7 manifest: {old_manifest[:16]}... -> {new_manifest[:16]}...")

    if not dry_run:
        data["module_7"]["manifest_sha"] = new_manifest

    # Run build_module_7.py
    m7_script = "certificates/build_module_7.py"
    if not os.path.exists(m7_script):
        result["build_ok"] = None
        result["build_msg"] = f"build script not found: {m7_script}"
        return result

    if dry_run:
        result["build_msg"] = f"[dry-run] would run: python3 {m7_script}"
        return result

    r = subprocess.run(["python3", m7_script], capture_output=True, text=True)
    if r.returncode != 0:
        result["build_ok"] = False
        result["build_msg"] = (
            f"FAILED (exit {r.returncode}):\n"
            f"  {r.stderr.strip()[:300]}"
        )
        return result

    result["build_ok"] = True
    result["build_msg"] = "OK (exit 0)"

    # Update sha256_pdf for M7
    pdf_path = PDF_PATH_MAP.get("module_7", "certificates/Module_7_Certificate.pdf")
    if os.path.exists(pdf_path):
        new_pdf_sha = sha256_file(pdf_path)
        old_pdf_sha = data["module_7"].get("sha256_pdf", "")
        if new_pdf_sha != old_pdf_sha:
            data["module_7"]["sha256_pdf"] = new_pdf_sha
            result["pdf_note"] = (
                f"sha256_pdf {old_pdf_sha[:16]}... -> {new_pdf_sha[:16]}..."
            )

    return result


# ---------------------------------------------------------------------------
# Self-check fixture
# ---------------------------------------------------------------------------

def run_self_check():
    """
    Verify the detection logic end-to-end without touching any files.
    Returns True if all assertions pass, False otherwise.
    """
    if not os.path.exists(INVARIANTS_PATH):
        print(f"SELF-CHECK FAIL: {INVARIANTS_PATH} not found")
        return False

    with open(INVARIANTS_PATH) as f:
        data = json.load(f)

    print("Opera Numerorum -- recertify self-check")
    print("=" * 60)
    ok = True

    # Test 1: scan with live data -- nothing should be changed
    print("Test 1: Live scan expects 0 changed entries ...")
    changes = scan_changes(data)
    changed = [c for c in changes if c["status"] == "changed"]
    if changed:
        print(f"  FAIL: {len(changed)} unexpected change(s): "
              f"{[c['key'] for c in changed]}")
        ok = False
    else:
        print(f"  PASS: {len(changes)} binding(s) checked, 0 changed.")

    # Test 2: simulate a changed SHA for module_4 and verify detection
    print("Test 2: Inject fake SHA for module_4, expect detection ...")
    orig = data["module_4"]["sha256_stdout"]
    data["module_4"]["sha256_stdout"] = "00" * 32   # clearly wrong
    changes2 = scan_changes(data, filter_keys={"module_4"})
    data["module_4"]["sha256_stdout"] = orig         # restore immediately

    detected = [c for c in changes2 if c["status"] == "changed" and c["key"] == "module_4"]
    if not detected:
        print("  FAIL: changed SHA not detected for module_4")
        ok = False
    else:
        script = get_build_script("module_4", data["module_4"])
        if script != "certificates/build_module_4.py":
            print(f"  FAIL: wrong build script for module_4: {script}")
            ok = False
        else:
            print(f"  PASS: detected, build script -> {script}")

    # Test 3: every key in BUILD_SCRIPT_MAP that is present in invariants.json
    # must have its builder script on disk.  Missing scripts produce FAIL.
    print("Test 3: BUILD_SCRIPT_MAP entries present in invariants.json ...")
    t3_keys = [k for k in BUILD_SCRIPT_MAP if k in data]
    t3_fail = False
    for key in sorted(t3_keys):
        script = BUILD_SCRIPT_MAP[key]
        exists = os.path.exists(script)
        if not exists:
            print(f"  FAIL: {key} -> {script}  [NOT FOUND ON DISK]")
            ok = False
            t3_fail = True
        else:
            print(f"  PASS: {key} -> {script}")
    if not t3_fail:
        print(f"  {len(t3_keys)} script(s) verified.")

    # Test 4: M7 manifest SHA sanity
    print("Test 4: M7 manifest SHA recomputation ...")
    computed = sha256_manifest()
    stored = data.get("module_7", {}).get("manifest_sha", "")
    if computed is None:
        print("  SKIP: one or more m1..m6.out files missing")
    elif computed == stored:
        print(f"  PASS: manifest SHA matches ({computed[:16]}...)")
    else:
        print(f"  FAIL: manifest mismatch")
        print(f"    stored:   {stored}")
        print(f"    computed: {computed}")
        ok = False

    # Test 5: check that M1-M6 keys trigger M7 relock detection
    print("Test 5: M1-M6 membership set for M7 relock ...")
    for k in ["module_1", "module_2", "module_3",
              "module_4", "module_5", "module_6"]:
        if k not in M1_TO_M6_KEYS:
            print(f"  FAIL: {k} missing from M1_TO_M6_KEYS")
            ok = False
    if ok:
        print(f"  PASS: all 6 keys present.")

    # Test 6: every tower whose certify_script is recorded in invariants.json
    # must have that file present on disk.  A recorded but missing script
    # produces FAIL (not a silent skip).  Towers with no certify_script field
    # are noted but do not count as failures.
    print("Test 6: Tower certify_script files exist on disk ...")
    TOWER_KEYS = ["rh_tower", "bsd_tower", "ns_tower", "ms_tower", "pvsnp_tower"]
    t6_fail = False
    for tower in TOWER_KEYS:
        entry = data.get(tower)
        if entry is None:
            print(f"  SKIP: {tower} not in invariants.json")
            continue
        cs = entry.get("certify_script")
        if cs is None:
            print(f"  FAIL: {tower} has no certify_script field in invariants.json")
            ok = False
            t6_fail = True
            continue
        if os.path.exists(cs):
            print(f"  PASS: {tower} -> {cs}")
        else:
            print(f"  FAIL: {tower} -> {cs}  [NOT FOUND ON DISK]")
            ok = False
            t6_fail = True
    if not t6_fail:
        checked = [t for t in TOWER_KEYS
                   if data.get(t) and data[t].get("certify_script")]
        print(f"  {len(checked)} certify_script(s) verified.")

    # Test 7: tower PDF SHA integrity -- sha256_pdf / pdf_sha in invariants.json
    # must match the on-disk PDF.  Missing PDF -> SKIP.  Mismatch -> FAIL.
    print("Test 7: Tower PDF SHA integrity (invariants.json vs on-disk) ...")
    t7_fail = False
    t7_checked = 0
    t7_skipped = 0
    for tower in TOWER_KEYS:
        entry = data.get(tower)
        if entry is None:
            print(f"  SKIP: {tower} not in invariants.json")
            t7_skipped += 1
            continue
        sha_field = get_pdf_sha_field(entry)
        if sha_field is None:
            print(f"  SKIP: {tower} has no sha256_pdf / pdf_sha field")
            t7_skipped += 1
            continue
        stored_sha = entry[sha_field]
        pdf_path = get_pdf_path(tower, entry)
        if pdf_path is None:
            print(f"  SKIP: {tower} -- PDF path unknown")
            t7_skipped += 1
            continue
        if not os.path.exists(pdf_path):
            print(f"  SKIP: {tower} -- PDF not on disk ({pdf_path})")
            t7_skipped += 1
            continue
        computed_sha = sha256_file(pdf_path)
        if computed_sha == stored_sha:
            print(f"  PASS: {tower} -- {pdf_path} ({computed_sha[:16]}...)")
            t7_checked += 1
        else:
            print(f"  FAIL: {tower} -- PDF SHA mismatch for {pdf_path}")
            print(f"    stored:   {stored_sha}")
            print(f"    on-disk:  {computed_sha}")
            ok = False
            t7_fail = True
            t7_checked += 1
    if not t7_fail:
        print(f"  {t7_checked} PDF(s) verified, {t7_skipped} skipped.")

    # Test 8: source SHA freshness -- update_source_shas.py --check must exit 0
    print("Test 8: Source SHA freshness (update_source_shas.py --check) ...")
    src_sha_script = "certificates/update_source_shas.py"
    if not os.path.exists(src_sha_script):
        print(f"  FAIL: {src_sha_script} not found on disk")
        ok = False
    else:
        t8_result = subprocess.run(
            [sys.executable, src_sha_script, "--check"],
            capture_output=True,
            text=True,
        )
        if t8_result.returncode == 0:
            # Count "OK" lines to give a useful summary
            ok_count = t8_result.stdout.count("\n  OK ")
            print(f"  PASS: all source SHAs are current ({ok_count} field(s) verified).")
        else:
            # Surface the stale entries from stdout
            stale_lines = [
                line.strip()
                for line in t8_result.stdout.splitlines()
                if "STALE" in line
            ]
            print(f"  FAIL: {len(stale_lines)} source SHA(s) stale in invariants.json:")
            for line in stale_lines:
                print(f"    {line}")
            print("  Run: python3 certificates/update_source_shas.py")
            ok = False

    # Test 9: certify_script / builder_script cross-check
    # For every tower that records both scripts in invariants.json, parse each
    # file for the shared RESULTS_FILE = "..." constant (the handoff file that
    # the certify script writes and the builder script reads).  A mismatch means
    # one script was updated but the other was not -- the pipeline would break
    # silently at build time.
    print("Test 9: Builder/certify RESULTS_FILE constant agreement ...")
    _RESULTS_RE = re.compile(r'^RESULTS_FILE\s*=\s*["\']([^"\']+)["\']', re.MULTILINE)

    def _extract_results_file(path):
        """Return the RESULTS_FILE value from a script, or None if absent."""
        try:
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
        except OSError:
            return None
        m = _RESULTS_RE.search(src)
        return m.group(1) if m else None

    t9_fail = False
    t9_checked = 0
    t9_skipped = 0
    for tower in TOWER_KEYS:
        entry = data.get(tower)
        if entry is None:
            print(f"  SKIP: {tower} -- not in invariants.json")
            t9_skipped += 1
            continue
        cs = entry.get("certify_script")
        # builder_script may be absent from the invariants.json entry; fall back
        # to BUILD_SCRIPT_MAP so all registered towers are checked regardless of
        # whether the JSON field has been filled in.
        bs = entry.get("builder_script") or BUILD_SCRIPT_MAP.get(tower)
        if not cs:
            print(f"  SKIP: {tower} -- no certify_script field in invariants.json")
            t9_skipped += 1
            continue
        if not bs:
            print(f"  SKIP: {tower} -- no builder_script in invariants.json or BUILD_SCRIPT_MAP")
            t9_skipped += 1
            continue
        if not os.path.exists(bs):
            print(f"  FAIL: {tower} -- builder_script not on disk: {bs}")
            ok = False
            t9_fail = True
            continue
        if not os.path.exists(cs):
            print(f"  FAIL: {tower} -- certify_script not on disk: {cs}")
            ok = False
            t9_fail = True
            continue
        cs_val = _extract_results_file(cs)
        bs_val = _extract_results_file(bs)
        if cs_val is None and bs_val is None:
            print(f"  FAIL: {tower} -- no RESULTS_FILE marker in either script")
            print(f"    certify_script: {cs}")
            print(f"    builder_script: {bs}")
            ok = False
            t9_fail = True
            continue
        if cs_val is None:
            print(f"  FAIL: {tower} -- RESULTS_FILE marker absent in certify_script ({cs})")
            print(f"    builder_script has: \"{bs_val}\"")
            ok = False
            t9_fail = True
            continue
        if bs_val is None:
            print(f"  FAIL: {tower} -- RESULTS_FILE marker absent in builder_script ({bs})")
            print(f"    certify_script has: \"{cs_val}\"")
            ok = False
            t9_fail = True
            continue
        if cs_val == bs_val:
            print(f"  PASS: {tower} -- RESULTS_FILE = \"{cs_val}\" (both agree)")
            t9_checked += 1
        else:
            print(f"  FAIL: {tower} -- RESULTS_FILE mismatch")
            print(f"    certify_script ({cs}): \"{cs_val}\"")
            print(f"    builder_script ({bs}): \"{bs_val}\"")
            ok = False
            t9_fail = True
    if not t9_fail:
        print(f"  {t9_checked} pair(s) verified, {t9_skipped} skipped.")

    print("=" * 60)
    if ok:
        print("SELF-CHECK PASS -- all tests passed.")
    else:
        print("SELF-CHECK FAIL -- one or more tests failed.")
    return ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Detect changed *.out files and re-emit certificate PDFs."
    )
    parser.add_argument(
        "keys", nargs="*",
        help="Specific invariants.json keys to check (default: all)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Report changes and which scripts would run; write nothing."
    )
    parser.add_argument(
        "--self-check", action="store_true",
        help="Run the built-in self-check fixture and exit."
    )
    args = parser.parse_args()

    if args.self_check:
        sys.exit(0 if run_self_check() else 1)

    if not os.path.exists(INVARIANTS_PATH):
        print(f"ERROR: {INVARIANTS_PATH} not found", file=sys.stderr)
        sys.exit(1)

    with open(INVARIANTS_PATH) as f:
        data = json.load(f)

    filter_keys = set(args.keys) if args.keys else None
    if filter_keys:
        missing_k = filter_keys - set(data.keys())
        if missing_k:
            print(f"WARNING: keys not found in invariants.json: "
                  f"{', '.join(sorted(missing_k))}")
        filter_keys -= missing_k

    print("Opera Numerorum -- recertify")
    print("=" * 60)
    if args.dry_run:
        print("[dry-run mode -- no files will be written]")
        print()

    # --- scan ---
    all_checks = scan_changes(data, filter_keys)
    changed = [c for c in all_checks if c["status"] == "changed"]
    missing = [c for c in all_checks if c["status"] == "missing"]
    ok_list = [c for c in all_checks if c["status"] == "ok"]

    print(f"Checked {len(all_checks)} stdout binding(s) across {len(data)} "
          f"invariants entries.")
    print(f"  {len(ok_list)} unchanged  |  {len(changed)} changed  |  "
          f"{len(missing)} file(s) missing")
    print()

    if missing:
        print("MISSING stdout files (not recertified -- check source scripts):")
        for c in missing:
            print(f"  [{c['key']}]  {c['filepath']}  "
                  f"(stored: {c['stored_sha'][:16]}...)")
        print()

    if not changed:
        print("Nothing to recertify.  All recorded SHAs match on-disk files.")
        sys.exit(0)

    # --- group changed entries by key ---
    changed_keys = {}
    for c in changed:
        changed_keys.setdefault(c["key"], []).append(c)

    # Track which build scripts we have already run (bdp shares one script).
    scripts_run = set()

    build_failures = []
    rebuilt = []
    skipped_no_script = []
    m1_to_m6_changed = set()   # track which M1-M6 keys changed

    for key, chg_list in changed_keys.items():
        entry = data[key]
        print(f"[{key}]  {chg_list[0]['filepath']}")

        for c in chg_list:
            print(f"  {c['sha_field']}")
            print(f"    stored:   {c['stored_sha']}")
            print(f"    computed: {c['computed_sha']}")

        if not args.dry_run:
            for c in chg_list:
                data[key][c["sha_field"]] = c["computed_sha"]

        if key in M1_TO_M6_KEYS:
            m1_to_m6_changed.add(key)

        # Run build script
        script = get_build_script(key, entry)
        if script and script in scripts_run:
            print(f"  build:  {script}  [already run for this session]")
            pdf_note = update_pdf_sha(key, entry, data, args.dry_run)
            if pdf_note:
                print(f"  pdf:    {pdf_note}")
            rebuilt.append(key)
            print()
            continue

        ok_flag, msg = run_build(key, entry, args.dry_run)
        if script:
            scripts_run.add(script)

        if ok_flag is None and script is None:
            print(f"  build:  (no build script -- SHA updated in "
                  f"invariants.json only)")
            skipped_no_script.append(key)
        elif ok_flag is None:
            print(f"  build:  {msg}")
            skipped_no_script.append(key)
        elif ok_flag:
            print(f"  build:  {script}  ->  {msg}")
            pdf_note = update_pdf_sha(key, entry, data, args.dry_run)
            if pdf_note:
                print(f"  pdf:    {pdf_note}")
            rebuilt.append(key)
        else:
            print(f"  build:  {script}  ->  {msg}")
            build_failures.append(key)

        print()

    # --- M7 manifest re-lock (triggered when any of M1-M6 changed) ---
    m7_result = None
    if m1_to_m6_changed and "module_7" in data:
        print(f"[module_7 -- manifest re-lock triggered by: "
              f"{', '.join(sorted(m1_to_m6_changed))}]")
        m7_result = relock_m7_manifest(data, args.dry_run)
        print(f"  manifest: {m7_result['build_msg']}")
        if m7_result.get("pdf_note"):
            print(f"  pdf:      {m7_result['pdf_note']}")
        if m7_result.get("build_ok") is True:
            rebuilt.append("module_7 (manifest)")
        elif m7_result.get("build_ok") is False:
            build_failures.append("module_7 (manifest)")
        print()

    # --- write invariants.json ---
    if not args.dry_run:
        with open(INVARIANTS_PATH, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        print("invariants.json updated.")
        print()

    # --- summary ---
    print("=" * 60)
    print("Summary")
    print(f"  Changed modules detected:  {len(changed_keys)}")
    print(f"  PDFs rebuilt:              {len(rebuilt)}")
    if m1_to_m6_changed:
        if m7_result and m7_result.get("build_ok") is True:
            new_sha = m7_result.get("manifest_sha", "")
            print(f"  M7 manifest re-locked:     {new_sha}")
        elif args.dry_run:
            print(f"  M7 manifest re-lock:       DRY-RUN")
        elif m7_result and m7_result.get("build_ok") is False:
            print(f"  M7 manifest re-lock:       FAILED")
        else:
            print(f"  M7 manifest re-lock:       no-op (manifest unchanged)")
    if skipped_no_script:
        print(f"  SHA-only updates (no script): "
              f"{', '.join(skipped_no_script)}")
    if build_failures:
        print(f"  BUILD FAILURES:            {', '.join(build_failures)}")
        print()
        print("EXIT 1 -- one or more build scripts failed.")
        sys.exit(1)
    else:
        print()
        if args.dry_run:
            print("Dry run complete.  Re-run without --dry-run to apply changes.")
        else:
            print("Recertification complete.")
        sys.exit(0)


if __name__ == "__main__":
    main()
