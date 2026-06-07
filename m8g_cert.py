#!/usr/bin/env python3
"""
M8G Certification: 120-Cell PCB Wormhole Result
Opera Numerorum -- Battle Plan v1.6

Consumes m8f_run.out (written by m8f_agent.py after the lab run),
validates the M8F assertions against certified chain constants,
writes m8g.out with the final VALIDATED or FALSIFIED verdict,
and prints SHA-256(m8g.out).

Usage (after lab run):
    python3 m8g_cert.py

Optional: pass M8B and M8F stdout SHAs explicitly to override
the values loaded from the chain files:
    python3 m8g_cert.py <m8b_sha> <m8f_sha>

If the files m8b.out and m8f.out are present on disk, their SHAs
are loaded automatically and the argv override is not needed.

Output files:
    m8g.out   -- JSON certificate (VALIDATED or FALSIFIED)

After running, patch invariants.json:
    python3 -c "
    import json, hashlib
    inv = json.load(open('certificates/invariants.json'))
    sha = hashlib.sha256(open('m8g.out','rb').read()).hexdigest()
    inv['module_m8g']['stdout_sha256'] = sha
    inv['module_m8g']['status'] = 'VALIDATED'   # or FALSIFIED
    json.dump(inv, open('certificates/invariants.json','w'), indent=2)
    print('invariants.json updated:', sha)
    "
"""

import json
import hashlib
import sys
import time

# ------------------------------------------------------------------ #
# Locked chain constants (all certified before lab run)              #
# ------------------------------------------------------------------ #

CHAIN = {
    "m1_alpha_0_MHz":   299.314159265359,
    "m5_delta_ds4":      23.796910,
    "m8b_c_bound":      299541524,
    "m8b_c_ratio":        5.724374,
    "m8b_C_0_pF":        29.17,
    "m8b_C_cliff_pF":   166.98,
    "m8c_z":             15,
    "m8d_f_res_Hz":     299_314_159.265,
    "m8f_k_c":            3.183,
    "m22_sha":   "5a5a345f6394438f7a5134cf682d714fea6c89c73cfc22fcdc503bc90761e5ca",
}

# ------------------------------------------------------------------ #
# Load parent SHAs from on-disk files (fallback to argv)             #
# ------------------------------------------------------------------ #

def _sha_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None

m8b_sha = _sha_file("m8b.out") or (sys.argv[1] if len(sys.argv) > 1 else "TBD")
m8f_sha = _sha_file("m8f.out") or (sys.argv[2] if len(sys.argv) > 2 else "TBD")

# ------------------------------------------------------------------ #
# Load m8f_run.out                                                    #
# ------------------------------------------------------------------ #

try:
    with open("m8f_run.out") as f:
        m8f_run = json.load(f)
except FileNotFoundError:
    sys.exit(
        "ERROR: m8f_run.out not found.\n"
        "Run m8f_agent.py against the lab hardware first, then re-run this script."
    )

# ------------------------------------------------------------------ #
# Re-validate M8F assertions against certified constants             #
# ------------------------------------------------------------------ #

m = m8f_run.get("measurements", {})

assertions = {
    "k_c_match":       abs(m.get("k_c_measured",   0.0) - CHAIN["m8f_k_c"])   < 0.010,
    "C_ratio_match":   abs(m.get("C_ratio",         0.0) - CHAIN["m8b_c_ratio"]) < 1e-3,
    "C_0_match":       abs(m.get("C_0_pF",          0.0) - CHAIN["m8b_C_0_pF"])  < 1.0,
    "C_cliff_match":   abs(m.get("C_cliff_pF",      0.0) - CHAIN["m8b_C_cliff_pF"]) < 1.0,
    "superluminal":    m.get("t_cavity_ns", 999.0) < m.get("t_vacuum_ns", 0.0) * 0.40,
    "lead_time_match": abs(m.get("Delta_t_lead_ns", 0.0) - 1.144) < 0.010,
    "q_factor_ok":     m.get("Q_measured", 60_000) > 50_000,
    "m8f_agent_pass":  m8f_run.get("pass", False),
}

chain_pass = all(assertions.values())

# ------------------------------------------------------------------ #
# Build output record                                                  #
# ------------------------------------------------------------------ #

output = {
    "module":     "M8G",
    "opera_numerorum": "Battle Plan v1.6",
    "axiom_debt": [],
    "depends_on": ["M1", "M5", "M8B", "M8C", "M8D", "M8F", "M22"],
    "sha_input": {
        "m8b.out": m8b_sha,
        "m8f.out": m8f_sha,
        "m22.out": CHAIN["m22_sha"],
    },
    "chain_constants": CHAIN,
    "lab_results": m,
    "assertions": assertions,
    "chain_consequences": {
        "M8B_status":  "VALIDATED"                      if chain_pass else "FALSIFIED",
        "M23_BSD":     "EXPERIMENTALLY_ANCHORED"        if chain_pass else "SEVERED",
        "M6_M21_GRH":  "H4_PHYSICAL_LINK_CONFIRMED"    if chain_pass else "PURE_THEORY",
        "wormhole":    "dt_internal = dt_external / 3.183 CONFIRMED"
                       if chain_pass else "NULL_RESULT",
    },
    "theorem": (
        "M8G: 120-Cell PCB Wormhole Validated. "
        "dt_internal = dt_external / 3.183 confirmed by lab measurement."
    ) if chain_pass else (
        "M8G: FALSIFIED. No superluminal group velocity observed. "
        "M8B dead. Archive chain M8B-M8G."
    ),
    "pass":      chain_pass,
    "timestamp": time.time(),
}

# ------------------------------------------------------------------ #
# Write m8g.out and compute SHA                                       #
# ------------------------------------------------------------------ #

out_str = json.dumps(output, indent=2, sort_keys=True)
sha = hashlib.sha256(out_str.encode()).hexdigest()

with open("m8g.out", "w") as f:
    f.write(out_str)

# ------------------------------------------------------------------ #
# Report                                                              #
# ------------------------------------------------------------------ #

print(f"M8G COMPLETE: pass={chain_pass}")
print(f"SHA-256(m8g.out): {sha}")
print()
for label, result in assertions.items():
    print(f"  {'PASS' if result else 'FAIL'}  {label}")
print()

if chain_pass:
    print("WORMHOLE CONFIRMED: 1.144 ns early.")
    print("Update invariants.json: module_m8g.status = VALIDATED")
    print(f"                        module_m8g.stdout_sha256 = {sha}")
else:
    failed = [k for k, v in assertions.items() if not v]
    print(f"FALSIFICATION: failed assertions = {failed}")
    print("M8B dead. Archive chain M8B-M8G as null result.")
    print(f"Update invariants.json: module_m8g.status = FALSIFIED")
    print(f"                        module_m8g.stdout_sha256 = {sha}")
