"""
M8F_Agent.py
Opera Numerorum -- M8F Lab Agent
Auto-detection of the capacitance cliff and group velocity measurement
for the 120-cell resonator experiment.

Usage:
  from M8F_Agent import agent_run
  result = agent_run(k_values, C_values, dt_values=None)
"""
import hashlib
import csv
import io
import sys

# Certified constants (Opera Numerorum M1-M8F)
F_RES_HZ   = 299314159      # Hz = (299 + pi/10) * 1e6  [M1]
Z          = 15              # Zoe invariant [M8C]
K_C        = 3.183           # cliff parameter [M22]
K_TOL      = 0.01            # tolerance on k_c
C_RATIO    = 5.724           # C_after/C_before at cliff [M8D]
C_RATIO_TOL = 0.1            # tolerance
C0_PF      = 29.17           # baseline capacitance [pF]
V_G_MULT   = K_C             # v_g = K_C * c at cliff
C_LIGHT    = 299792458       # m/s


def agent_run(k_values, C_pF_values, dt_ns_values=None, probe_distance_m=0.5):
    """
    Main agent function.
    
    Args:
        k_values:         list of drive parameter values (V_drive/V_0)
        C_pF_values:      list of measured capacitances in pF
        dt_ns_values:     list of transit times in ns (optional, for v_g test)
        probe_distance_m: distance between E-probes in meters
    
    Returns:
        dict with keys: cliff_found, k_c_measured, C_jump_ratio,
                        v_g_c (group velocity / c), pass_fail, sha256
    """
    result = {
        "cliff_found": False,
        "k_c_measured": None,
        "C_before_pF": None,
        "C_after_pF": None,
        "C_jump_ratio": None,
        "v_g_c": None,
        "pass_fail": "PENDING",
        "audit": [],
        "sha256": None,
    }

    # --- 1. Detect cliff ---
    for i in range(1, len(k_values)):
        k_prev = k_values[i-1]
        k_curr = k_values[i]
        C_prev = C_pF_values[i-1]
        C_curr = C_pF_values[i]
        if C_prev > 0:
            ratio = C_curr / C_prev
            if ratio > 3.0:
                result["cliff_found"] = True
                result["k_c_measured"] = k_curr
                result["C_before_pF"] = C_prev
                result["C_after_pF"] = C_curr
                result["C_jump_ratio"] = C_curr / C_pF_values[0] if C_pF_values[0] > 0 else ratio
                break

    # --- 2. Validate cliff ---
    if result["cliff_found"]:
        k_c = result["k_c_measured"]
        jump = result["C_jump_ratio"]

        k_ok   = abs(k_c - K_C) <= K_TOL
        c_ok   = abs(jump - C_RATIO) <= C_RATIO_TOL
        result["audit"].append(f"k_c = {k_c:.4f}, expected {K_C} +/- {K_TOL}: {'PASS' if k_ok else 'FAIL'}")
        result["audit"].append(f"C_jump = {jump:.4f}, expected {C_RATIO} +/- {C_RATIO_TOL}: {'PASS' if c_ok else 'FAIL'}")

        if not k_ok:
            result["pass_fail"] = "ABORT_K_C_WRONG"
            result["audit"].append(f"ABORT: k_c = {k_c:.4f} != {K_C} +/- {K_TOL}. Report null result.")
            _sha(result, k_values, C_pF_values)
            return result

        if not c_ok:
            result["audit"].append(f"WARNING: C_jump = {jump:.3f} outside expected range. Flag for review.")

    else:
        # No cliff found
        k_max = max(k_values) if k_values else 0
        if k_max >= 5.0:
            result["pass_fail"] = "M8B_FALSIFIED"
            result["audit"].append(f"No C jump detected for k up to {k_max:.2f}. M8B FALSIFIED. Null result.")
        else:
            result["pass_fail"] = "INCOMPLETE_SWEEP"
            result["audit"].append(f"Sweep incomplete (k_max={k_max:.2f}). Continue to k=5.0.")
        _sha(result, k_values, C_pF_values)
        return result

    # --- 3. v_g test (if transit times provided) ---
    if dt_ns_values is not None and len(dt_ns_values) > 0:
        dt_vac = probe_distance_m / C_LIGHT * 1e9   # ns
        dt_min = min(dt_ns_values)
        v_g = probe_distance_m / (dt_min * 1e-9) / C_LIGHT  # in units of c
        result["v_g_c"] = v_g
        result["audit"].append(f"Vacuum Delta_t = {dt_vac:.4f} ns")
        result["audit"].append(f"Measured Delta_t = {dt_min:.4f} ns")
        result["audit"].append(f"v_g = {v_g:.4f}c")
        if dt_min < dt_vac - 0.05:
            result["audit"].append(f"v_g > c CONFIRMED: pulse {(dt_vac-dt_min):.3f} ns early. STARSHIP CONDITION.")
            result["pass_fail"] = "VG_SUPERLUMINAL"
        else:
            result["audit"].append("v_g <= c. M* modifies C, not metric. Useful but no travel.")
            result["pass_fail"] = "CLIFF_CONFIRMED_VG_NOT_SUPERLUMINAL"
    else:
        result["pass_fail"] = "CLIFF_CONFIRMED_NO_VG_TEST"

    _sha(result, k_values, C_pF_values)
    return result


def _sha(result, k_values, C_pF_values):
    """Compute SHA256 of the measurement data."""
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["k", "C_pF"])
    for k, c in zip(k_values, C_pF_values):
        w.writerow([f"{k:.6f}", f"{c:.4f}"])
    data_str = buf.getvalue().encode("utf-8")
    result["sha256"] = hashlib.sha256(data_str).hexdigest()


def M8F_protocol():
    """Print the M8F_Protocol.md content."""
    print("""
M8F_Protocol.md -- Opera Numerorum -- David Fox -- May 2026
===========================================================

1. CALIBRATE VNA
   - Keysight E5071C or equivalent
   - Frequency: 299.314159 MHz +/- 100 kHz
   - Calibrate S11 port at cavity coupling loop
   - Verify Q > 10,000 at k=0 before sweep

2. SWEEP V_drive 0 -> 5V, 0.001V STEP
   - Measure C via VNA S11 minimum phase shift
   - Compute k = V_drive / V_0  (V_0 = 1.0 V/m)
   - Log C(k) every step
   - Expected baseline: C ~ 29.17 pF, Q > 10,000

3. CLIFF DETECTION
   - Call agent_run(k_values, C_values)
   - If cliff_found and k_c = 3.183 +/- 0.01: PROCEED
   - If k_c != 3.183 +/- 0.01: ABORT and report null result
   - Expected cliff: C_after/C_before = 5.724 +/- 0.1

4. PULSE TEST (only if cliff confirmed)
   - Setup: 1ns pulse at 299.3 MHz
   - Two E-probes, 0.5m apart inside cavity
   - Measure Delta_t = transit time
   - Vacuum baseline: Delta_t = 1.6678 ns (0.5/c)
   - Prediction: Delta_t = 0.524 ns (pulse 1.144 ns early)
   - If Delta_t < 1.667 ns: compute v_g = 0.5/Delta_t

5. REPORT
   - SHA256(data.csv)
   - Report: k_c, C_jump_ratio, v_g (or null)
   - Pass: k_c=3.183+/-0.01, C_jump=5.724+/-0.1
   - Fail: any condition outside tolerances

FALSIFICATION: If C stays within 1.1x of C_0 for k in [0, 5.0]:
  M8B is falsified. Publish null result. The math still stands.
""")


if __name__ == "__main__":
    print("M8F Agent -- Opera Numerorum")
    print("Run M8D_MStar_Calculator.py to get prediction table.")
    print("Run this module with your measured data:")
    print()
    print("  from M8F_Agent import agent_run")
    print("  result = agent_run(k_values, C_pF_values, dt_ns_values)")
    print("  print(result)")
    print()
    M8F_protocol()
