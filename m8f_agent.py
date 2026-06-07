#!/usr/bin/env python3
"""
M8F Agent: 7-Layer Protocol Lab Runner
Opera Numerorum -- M8F certified runner

Executes the 5-step M8F experimental protocol against real hardware:
  1. Calibrate  -- VNA TRL cal at 77 K, center 299.314159 MHz
  2. Sweep      -- V_drive 0->5 V in 0.001 V steps, measure C at each step
  3. Detect     -- find cliff at k = 3.183; C should jump 29.17 -> 166.98 pF
  4. Pulse      -- at k_c send pulse; expect 0.524 ns not 1.6678 ns
  5. Report     -- SHA-256 all data; write m8f_run.out

Falsification: Delta_t >= 1.667 ns for all k  =>  M8B dead, null result

Requires: pyvisa, numpy  (pip install pyvisa pyvisa-py numpy)
Hardware:  VNA (e.g. Keysight PNA-X), pulse generator, Keithley PSU

Usage:
    python3 m8f_agent.py --vna  TCPIP0::192.168.1.100::inst0::INSTR \
                         --pulse TCPIP0::192.168.1.101::inst0::INSTR \
                         --psu  TCPIP0::192.168.1.102::inst0::INSTR

Outputs: m8f_run.out (JSON), SHA-256 printed to stdout.
"""

import sys
import json
import hashlib
import time
import argparse
import numpy as np

# ------------------------------------------------------------------ #
# Certified constants (chain-locked)                                  #
# ------------------------------------------------------------------ #

F_RES         = 299_314_159.265  # Hz  -- M1, alpha_0 MHz
K_C_TARGET    =   3.183          # M22 certified cliff
C_0_EXPECT    =  29.17           # pF  -- M8B / M8D
C_CLIFF_EXPECT = 166.98          # pF  -- M8B prediction
T_VACUUM_NS   =   1.6678         # ns  -- c, 0.5 m path
T_CLIFF_NS    =   0.5240         # ns  -- expected at k_c
DELTA_T_LEAD  =   1.1441         # ns  -- expected lead

V_STEP  = 0.001   # V
V_MAX   = 5.0     # V

M22_SHA = "5a5a345f6394438f7a5134cf682d714fea6c89c73cfc22fcdc503bc90761e5ca"


# ------------------------------------------------------------------ #
# Agent class                                                         #
# ------------------------------------------------------------------ #

class M8FAgent:
    def __init__(self, vna_addr, pulse_addr, psu_addr, m8b_sha=""):
        import pyvisa
        self.m8b_sha = m8b_sha
        rm = pyvisa.ResourceManager()

        self.vna   = rm.open_resource(vna_addr)
        self.pulse = rm.open_resource(pulse_addr)
        self.psu   = rm.open_resource(psu_addr)

        # VNA initial setup
        self.vna.write("*RST")
        time.sleep(2.0)
        self.vna.write(f"SENS:FREQ:CENT {F_RES:.3f}")
        self.vna.write("SENS:FREQ:SPAN 1E6")      # 1 MHz span around center
        self.vna.write("SENS:BWID 100")            # 100 Hz IFBW for high Q
        self.vna.write("SENS:AVER:COUN 8")
        self.vna.write("SENS:AVER ON")

        print("VNA initialized at "
              f"{F_RES/1e6:.9f} MHz, IFBW 100 Hz, 8 averages")

    # -- low-level helpers -------------------------------------------

    def _set_k(self, k_val):
        """Set drive voltage V = k * V0 where V0 = 1.0 V/m."""
        v = float(k_val) * 1.0   # V0 = 1.0
        v = min(max(v, 0.0), V_MAX)
        self.psu.write(f"VOLT {v:.4f}")
        time.sleep(0.08)          # settle

    def _measure_c_pf(self):
        """Read capacitance from VNA in pF."""
        self.vna.write("CALC:FORM CAP")
        self.vna.write("TRIG:SING")
        self.vna.query("*OPC?")   # wait for sweep
        c_str = self.vna.query("CALC:DATA? FDATA").strip()
        return float(c_str.split(",")[0])

    def _measure_transit_ns(self):
        """Return pulse transit time in ns."""
        self.pulse.write("PULS:WIDT 50E-12")      # 50 ps pulse
        t_ns = float(self.pulse.query("MEAS:DELAY?"))
        return t_ns

    # -- protocol steps ----------------------------------------------

    def step1_calibrate(self):
        """TRL calibration check."""
        print("Step 1: VNA TRL cal check at 77 K ...")
        self.vna.write("SENS:CORR:STAT?")
        cal_on = self.vna.read().strip()
        print(f"  Cal active: {cal_on}")
        if cal_on not in ("1", "ON"):
            raise RuntimeError("CALIBRATION NOT ACTIVE -- apply TRL cryo cal first")

    def step2_sweep(self):
        """Sweep V_drive 0->5 V; return list of {k, V, C_pF}."""
        print("Step 2: Capacitance sweep 0 -> 5 V ...")
        results = []
        for v in np.arange(0.0, V_MAX + V_STEP / 2, V_STEP):
            k = v / 1.0    # V0 = 1.0
            self._set_k(k)
            c = self._measure_c_pf()
            results.append({"k": round(float(k), 4),
                             "V": round(float(v), 4),
                             "C_pF": round(c, 4)})
            if len(results) % 500 == 0:
                print(f"  ... k={k:.3f}, C={c:.2f} pF")
        print(f"  Sweep complete: {len(results)} points")
        return results

    def step3_detect(self, sweep_data):
        """Find cliff: k where C exceeds 3x baseline."""
        c_base = sweep_data[0]["C_pF"]
        for pt in sweep_data:
            if pt["C_pF"] > c_base * 3.0:
                print(f"  CLIFF DETECTED: k={pt['k']:.4f}, "
                      f"C={pt['C_pF']:.2f} pF "
                      f"(baseline {c_base:.2f} pF)")
                return pt["k"], pt["C_pF"]
        return None, None

    def step4_pulse(self, k_cliff):
        """Pulse test: measure transit at k_cliff and at k=0."""
        print("Step 4: Pulse transit test ...")
        # Cavity transit at cliff
        self._set_k(k_cliff)
        time.sleep(0.5)
        t_cavity = self._measure_transit_ns()
        print(f"  t_cavity  = {t_cavity:.6f} ns  (expect {T_CLIFF_NS:.4f})")

        # Vacuum reference
        self._set_k(0.0)
        time.sleep(0.5)
        t_vacuum = self._measure_transit_ns()
        print(f"  t_vacuum  = {t_vacuum:.6f} ns  (expect {T_VACUUM_NS:.4f})")

        delta_t = t_vacuum - t_cavity
        print(f"  Delta_t lead = {delta_t:.6f} ns  (expect {DELTA_T_LEAD:.4f})")
        return t_cavity, t_vacuum

    # -- main entry --------------------------------------------------

    def run(self):
        """Execute full M8F 5-step protocol. Returns (sha, pass_bool)."""

        # Fetch SHA of m8b.out for provenance
        try:
            with open("m8b.out", "rb") as f:
                self.m8b_sha = hashlib.sha256(f.read()).hexdigest()
        except FileNotFoundError:
            pass   # non-fatal; record as empty

        self.step1_calibrate()

        sweep_data          = self.step2_sweep()
        k_c, c_cliff        = self.step3_detect(sweep_data)
        c_0                 = sweep_data[0]["C_pF"]

        if k_c is None:
            output = {
                "module":      "M8F_run",
                "opera_numerorum": "Battle Plan v1.6",
                "axiom_debt":  [],
                "depends_on":  ["M8B", "M22"],
                "sha_input":   {"m8b.out": self.m8b_sha, "m22.out": M22_SHA},
                "verdict":     "FALSIFICATION -- no cliff detected. M8B dead.",
                "pass":        False,
                "timestamp":   time.time(),
            }
        else:
            t_cavity, t_vacuum = self.step4_pulse(k_c)
            delta_t_lead       = t_vacuum - t_cavity

            assertions = {
                "k_c_match":         abs(k_c       - K_C_TARGET)    < 0.010,
                "C_jump_match":      abs(c_cliff    - C_CLIFF_EXPECT) < 1.000,
                "C_baseline_match":  abs(c_0        - C_0_EXPECT)    < 1.000,
                "t_cavity_match":    abs(t_cavity   - T_CLIFF_NS)    < 0.002,
                "t_vacuum_match":    abs(t_vacuum   - T_VACUUM_NS)   < 0.002,
                "lead_time_match":   abs(delta_t_lead - DELTA_T_LEAD) < 0.010,
                "v_g_superluminal":  t_cavity < t_vacuum * 0.40,  # > 2.5c
            }

            output = {
                "module":      "M8F_run",
                "opera_numerorum": "Battle Plan v1.6",
                "axiom_debt":  [],
                "depends_on":  ["M8B", "M22"],
                "sha_input":   {"m8b.out": self.m8b_sha, "m22.out": M22_SHA},
                "measurements": {
                    "k_c_measured":   float(k_c),
                    "C_0_pF":         round(c_0,       4),
                    "C_cliff_pF":     round(c_cliff,    4),
                    "C_ratio":        round(c_cliff / c_0, 6),
                    "t_vacuum_ns":    round(t_vacuum,   6),
                    "t_cavity_ns":    round(t_cavity,   6),
                    "Delta_t_lead_ns": round(delta_t_lead, 6),
                    "v_g_c_units":    round(t_vacuum / t_cavity, 6),
                },
                "assertions":  assertions,
                "pass":        all(assertions.values()),
                "timestamp":   time.time(),
            }

        # Step 5: SHA-256 and write
        out_str  = json.dumps(output, indent=2, sort_keys=True)
        sha      = hashlib.sha256(out_str.encode()).hexdigest()
        output["sha256_self"] = sha

        with open("m8f_run.out", "w") as f:
            f.write(json.dumps(output, indent=2, sort_keys=True))

        print(f"\nM8F COMPLETE: pass={output['pass']}")
        print(f"SHA-256(m8f_run.out): {sha}")

        if not output["pass"]:
            verdict = output.get("verdict", "assertions failed")
            print(f"FALSIFICATION: {verdict}")
            print("Report null result. M8B/M22 link to physics severed.")

        return sha, output["pass"]


# ------------------------------------------------------------------ #
# CLI                                                                 #
# ------------------------------------------------------------------ #

def main():
    ap = argparse.ArgumentParser(
        description="M8F Agent: 7-Layer Protocol Lab Runner (Opera Numerorum)"
    )
    ap.add_argument("--vna",   required=True,
                    help="VISA address of VNA (e.g. TCPIP0::...::INSTR)")
    ap.add_argument("--pulse", required=True,
                    help="VISA address of pulse generator")
    ap.add_argument("--psu",   required=True,
                    help="VISA address of power supply (V_drive)")
    args = ap.parse_args()

    agent = M8FAgent(args.vna, args.pulse, args.psu)
    sha, passed = agent.run()
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
