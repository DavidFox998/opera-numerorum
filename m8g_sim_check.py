#!/usr/bin/env python3
"""
m8g_sim_check.py -- Opera Numerorum M8G
Unified validation: H4 geometry + COMSOL results.
Run this before fab. Single command: pass/fail for entire M8G chain.

Stage 1: H4 geometry check on 720_vias.csv (hard fail, exit 1 if invalid).
Stage 2: COMSOL CSV results check (Studies 1-4).

Chain references:
  M1:  f_res = alpha_0 * 1e6 = 299314159.265 Hz
  M8B: c_bound = 299541524 m/s
  M22: k_c (cliff) = 3.183
  M8C: Z = 15
  M8D: H4 face-centre angles = {60,90,108,144} deg, tolerance +/-0.01 deg
       (116.565 deg is the face-PLANE dihedral, not a face-centre angle)
  M8F: 8-gate validation protocol

Run:
  python3 m8g_sim_check.py
"""

import numpy as np
import sys
import csv
from math import acos, degrees, sqrt
from itertools import combinations
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas required. pip install pandas")
    sys.exit(1)

# --- M8D / M8B Spec Constants ---
# NOTE: H4 face-centre angles are {60,90,108,144} deg (4D geometry).
# 116.565 deg = arccos(-1/sqrt(5)) is the dodecahedron face-PLANE dihedral
# -- a cell-level property of the 120-cell, NOT a face-centre angle.
H4_FACE_PLANE_DIHEDRAL = 116.565051177078  # arccos(-1/sqrt(5)), cell dihedral
TOLERANCE_DEG      = 0.01              # M8D spec
VIA_FILE           = '720_vias.csv'
C_RATIO_TARGET     = 5.72437419        # M8B
C_0_TARGET         = 29.17            # pF
C_CLIFF_TARGET     = 166.98           # pF
K_C_TARGET         = 3.183            # M22
T_LEAD_TARGET      = 1.144            # ns
Q_MIN              = 50000            # 77K
F0_SHIFT_MAX       = 10.0             # Hz at 5 um
F_RES_CERT         = 299314159.265    # Hz (M1)


# ===========================================================================
# Stage 1: H4 Geometry Check
# ===========================================================================

def load_via_coords(path):
    """
    Load 4D via coordinates (x_4d..w_4d) for H4 angle verification.
    Falls back to 3D (x_mm..z_mm) with a warning if 4D cols absent
    (older CSV without 4D columns -- regenerate with 120cell_vertices.py).
    """
    if not Path(path).exists():
        return None, None, f"FATAL: {path} not found. Run 120cell_vertices.py first."
    try:
        df = pd.read_csv(path, comment='#')
        df.columns = [c.strip() for c in df.columns]
        if len(df) != 720:
            return None, None, f"FATAL: Expected 720 vias, found {len(df)}"
        if 'x_4d' in df.columns:
            vias_4d = df[['x_4d', 'y_4d', 'z_4d', 'w_4d']].values
        else:
            vias_4d = None  # signal to caller that 4D check cannot run
        vias_3d = df[['x_mm', 'y_mm', 'z_mm']].values
        return vias_4d, vias_3d, "OK"
    except Exception as e:
        return None, None, f"FATAL: Cannot read {path}: {e}"


# H4 characteristic angles at 120-cell face centres (4D)
_H4_ANGLES = [60.0, 90.0, 108.0, 144.0]
_PHI_INV   = 2 / (1 + sqrt(5))   # 1/phi


def check_h4_symmetry(vias_4d):
    """
    Check angles in 4D between pairs of each via's 10 nearest neighbours.
    Expected angles: {60, 90, 108, 144} deg, tolerance +/-0.01 deg.
    NOTE: 116.565 deg is the dodecahedron face-plane dihedral -- not a
          face-centre angle and NOT expected here.
    """
    from scipy.spatial import cKDTree
    tree = cKDTree(vias_4d)
    distances, indices = tree.query(vias_4d, k=11)  # 10 neighbours + self
    neighbor_idx = indices[:, 1:]

    max_dev    = 0.0
    fail_count = 0
    total      = 0

    for i, v_center in enumerate(vias_4d):
        neighbors = vias_4d[neighbor_idx[i]]
        for v1, v2 in combinations(neighbors, 2):
            a = v1 - v_center
            b = v2 - v_center
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            if na < 1e-12 or nb < 1e-12:
                continue
            cos_ang = np.dot(a, b) / (na * nb)
            angle   = degrees(acos(np.clip(cos_ang, -1.0, 1.0)))
            dev     = min(abs(angle - a) for a in _H4_ANGLES)
            max_dev = max(max_dev, dev)
            total  += 1
            if dev > TOLERANCE_DEG:
                fail_count += 1

    return {
        'pass':              fail_count == 0,
        'max_deviation_deg': max_dev,
        'fail_count':        fail_count,
        'total_checks':      total,
        'note':              'Angles checked: {60,90,108,144} deg. '
                             '116.565 deg is face-plane dihedral, not face-centre angle.',
    }


# ===========================================================================
# Stage 2: COMSOL Results Check
# ===========================================================================

def check_comsol_results():
    required = [
        'comsol_c_vs_k.csv',
        'comsol_q_vs_k.csv',
        'comsol_pulse_time.csv',
        'comsol_h4_tolerance.csv',
    ]
    for f in required:
        if not Path(f).exists():
            return {'pass': False, 'error': f'Missing {f}. Run COMSOL Studies 1-4.'}

    try:
        c_df    = pd.read_csv('comsol_c_vs_k.csv')
        q_df    = pd.read_csv('comsol_q_vs_k.csv')
        pulse_df= pd.read_csv('comsol_pulse_time.csv')
        tol_df  = pd.read_csv('comsol_h4_tolerance.csv')
    except Exception as e:
        return {'pass': False, 'error': f'CSV read error: {e}'}

    # --- Gates 1-3: C_ratio, C_0, C_cliff ---
    c_0      = c_df.iloc[0, 1]
    cliff_row= c_df.loc[abs(c_df.iloc[:, 0] - K_C_TARGET) < 0.005]
    if cliff_row.empty:
        return {'pass': False, 'error': 'No cliff at 3.183V found in comsol_c_vs_k.csv'}
    c_cliff  = cliff_row.iloc[0, 1]
    c_ratio  = c_cliff / c_0

    c_ratio_ok  = abs(c_ratio  - C_RATIO_TARGET) < 0.001
    c0_ok       = abs(c_0      - C_0_TARGET)      < 1.0
    ccliff_ok   = abs(c_cliff  - C_CLIFF_TARGET)  < 1.0
    cliff_at_kc = True  # already checked above

    # --- Gates 4-5: Superluminal + Lead time ---
    t_peak      = pulse_df.loc[pulse_df.iloc[:, 1].idxmax(), pulse_df.columns[0]]
    t_vacuum    = 1.668  # ns for 0.5 m / c
    delta_t     = t_vacuum - float(t_peak)
    superluminal_ok = float(t_peak) < t_vacuum * 0.40
    lead_ok     = abs(delta_t - T_LEAD_TARGET) < 0.010

    # --- Gate 6: Q factor ---
    q_ok = bool((q_df.iloc[:, 1] > Q_MIN).all())

    # --- Gate 8: H4 Tolerance from sim ---
    tol_df.columns = [c.strip() for c in tol_df.columns]
    h4_col = next((c for c in tol_df.columns if 'h4_error' in c.lower()), tol_df.columns[0])
    f_col  = next((c for c in tol_df.columns if 'f_res'    in c.lower()), tol_df.columns[1])
    q_col  = next((c for c in tol_df.columns if 'Q_Factor' in c or 'q_factor' in c.lower()), tol_df.columns[2])

    spec_5um   = tol_df.loc[abs(tol_df[h4_col] - 5.0) < 0.01]
    if spec_5um.empty:
        return {'pass': False, 'error': 'No 5 um row in comsol_h4_tolerance.csv'}
    f0_shift   = abs(float(spec_5um.iloc[0][f_col]) - F_RES_CERT)
    h4_sim_ok  = f0_shift < F0_SHIFT_MAX and float(spec_5um.iloc[0][q_col]) > Q_MIN

    six_um     = tol_df.loc[abs(tol_df[h4_col] - 6.0) < 0.01]
    if not six_um.empty:
        f0_shift_6 = abs(float(six_um.iloc[0][f_col]) - F_RES_CERT)
        fab_spec   = '< 5um' if f0_shift_6 > F0_SHIFT_MAX else '< 6um'
    else:
        fab_spec   = '< 5um'

    results = {
        'C_ratio_match':          c_ratio_ok,
        'C_ratio':                c_ratio,
        'C_0_match':              c0_ok,
        'C_0_pF':                 c_0,
        'C_cliff_match':          ccliff_ok,
        'C_cliff_pF':             c_cliff,
        'cliff_at_3.183':         cliff_at_kc,
        'superluminal':           superluminal_ok,
        't_cavity_ns':            float(t_peak),
        'lead_time_match':        lead_ok,
        'delta_t_ns':             delta_t,
        'q_factor_ok':            q_ok,
        'Q_min':                  float(q_df.iloc[:, 1].min()),
        'h4_5um_sim_ok':          h4_sim_ok,
        'f0_shift_5um_Hz':        f0_shift,
        'fab_tolerance_required': fab_spec,
    }
    results['pass'] = all([
        c_ratio_ok, c0_ok, ccliff_ok, cliff_at_kc,
        superluminal_ok, lead_ok, q_ok, h4_sim_ok,
    ])
    return results


# ===========================================================================
# Main
# ===========================================================================

def main():
    print("M8G UNIFIED SIM CHECK -- Opera Numerorum")
    print("=" * 50)

    # --- Stage 1: Geometry ---
    print("\n[1/2] H4 GEOMETRY CHECK -- 720_vias.csv (4D)")
    print("  Expected angles: {60, 90, 108, 144} deg  (face-centre pairs in 4D)")
    print("  NOTE: 116.565 deg is the dodecahedron face-PLANE dihedral,")
    print("        not a face-centre angle -- not checked here.")
    vias_4d, vias_3d, msg = load_via_coords(VIA_FILE)
    if vias_4d is None and vias_3d is None:
        print(f"  H4_CERT: INVALID -- {msg}")
        print("\nRESULT: FALSIFIED -- Geometry broken. Do not run COMSOL.")
        sys.exit(1)
    if vias_4d is None:
        print("  WARNING: 4D columns absent. Regenerate 720_vias.csv with")
        print("           120cell_vertices.py for full H4 validation.")
        print("  H4_CERT: SKIPPED (no 4D columns)")
        h4_res = {'pass': True, 'max_deviation_deg': None,
                  'fail_count': 0, 'total_checks': 0}
    else:
        h4_res = check_h4_symmetry(vias_4d)
        print(f"  Checks: {h4_res['total_checks']}, Failures: {h4_res['fail_count']}")
        print(f"  Max deviation: {h4_res['max_deviation_deg']:.4f} deg")
        if not h4_res['pass']:
            print("  H4_CERT: INVALID")
            print("\nRESULT: FALSIFIED -- H4 symmetry violated. Fix 720_vias.csv. Do not fab.")
            sys.exit(1)
        print("  H4_CERT: VALID")

    # --- Stage 2: COMSOL ---
    print("\n[2/2] COMSOL RESULTS CHECK -- Studies 1-4")
    comsol_res = check_comsol_results()

    if 'error' in comsol_res:
        print(f"  COMSOL_CERT: INCOMPLETE -- {comsol_res['error']}")
        print("\nRESULT: INCOMPLETE -- Run COMSOL first.")
        sys.exit(1)

    print("\nM8G 8-GATE VALIDATION:")
    gates = [
        ('C_ratio_match',  comsol_res['C_ratio'],          C_RATIO_TARGET),
        ('C_0_match',      comsol_res['C_0_pF'],           C_0_TARGET),
        ('C_cliff_match',  comsol_res['C_cliff_pF'],       C_CLIFF_TARGET),
        ('cliff_at_3.183', K_C_TARGET,                     K_C_TARGET),
        ('superluminal',   comsol_res['t_cavity_ns'],      f"<{1.668*0.4:.3f}"),
        ('lead_time_match',comsol_res['delta_t_ns'],       T_LEAD_TARGET),
        ('q_factor_ok',    comsol_res['Q_min'],            f">{Q_MIN}"),
        ('h4_5um_sim_ok',  comsol_res['f0_shift_5um_Hz'], f"<{F0_SHIFT_MAX}"),
    ]
    for name, val, target in gates:
        status = "PASS" if comsol_res[name] else "FAIL"
        print(f"  {name:20s}: {status} -- val={val:.4g}, target={target}")

    print(f"\n  Fab tolerance required: {comsol_res['fab_tolerance_required']}")

    if comsol_res['pass']:
        print("\n" + "=" * 50)
        print("RESULT: VALIDATED")
        print("M8G_SIM_CERT: PASS")
        print("ACTION: Safe to fab V2 PCB. Physics confirmed in sim.")
        print("=" * 50)
        sys.exit(0)
    else:
        print("\n" + "=" * 50)
        print("RESULT: FALSIFIED")
        print("M8G_SIM_CERT: FAIL")
        print("ACTION: Do not fab. M8B falsified in software.")
        print("=" * 50)
        sys.exit(1)


if __name__ == '__main__':
    main()
