#!/usr/bin/env python3
"""
icosa_sym_check.py -- Opera Numerorum M8E
H3 Icosahedral Symmetry Checker for M8G-Lite 24-Layer PCB.

Analogous to H4_sym_check.py (which checks the full 120-cell / M8G).
This checker validates the 24-layer icosahedral pre-test board.

GEOMETRY NOTE (certified by icosa_vertices.py):
  The 30 vias are edge midpoints of the unit icosahedron (H3 Coxeter group).
  In 3D, each via centre has exactly 4 nearest neighbours at distance
  0.52573111 = EDGE_LEN / (2 * sin(36 deg)) [icosahedral geometry].

  The angles at each via centre between pairs of its 4 nearest neighbours:
    60 deg  (x2 per via)  -- equilateral triangle pairs
   108 deg  (x2 per via)  -- pentagon interior angle [H3 signature]
   144 deg  (x2 per via)  -- golden gnomic pairs

  Total angle checks: 30 x C(4,2) = 30 x 6 = 180

HARD FAIL:
  Any angle deviating > 0.01 deg from nearest {60, 108, 144} -> exit 1.
  M8E board is rejected. Do not fab.

Chain: M8E -> icosa_sym_check.py -> [fab] -> M8F-lite test -> M8G decision
"""
import numpy as np
import sys
import csv
from math import acos, degrees, sqrt
from itertools import combinations

VIA_FILE       = "icosa_vias.csv"
EXPECTED_NN    = 4
NN_DIST        = 0.52573111   # exact: half edge length of icosahedron
NN_DIST_TOL    = 1e-6
TOLERANCE_DEG  = 0.01
H3_ANGLES_DEG  = [60.0, 108.0, 144.0]


def load_via_3d(path):
    vias = []
    try:
        with open(path, "r") as f:
            filtered = (line for line in f if not line.lstrip('"').startswith("#"))
            reader = csv.DictReader(filtered)
            for row in reader:
                vias.append([float(row["x_3d"]),
                              float(row["y_3d"]),
                              float(row["z_3d"])])
    except KeyError as e:
        print(f"FATAL: CSV missing column {e}.")
        print("  Run icosa_vertices.py to regenerate icosa_vias.csv.")
        sys.exit(1)
    except Exception as e:
        print(f"FATAL: Cannot read {path}: {e}")
        sys.exit(1)

    vias = np.array(vias)
    if len(vias) != 30:
        print(f"FATAL: Expected 30 vias, found {len(vias)}")
        sys.exit(1)
    return vias


def nearest_expected(angle):
    best = min(H3_ANGLES_DEG, key=lambda a: abs(angle - a))
    return best, abs(angle - best)


def check_h3_symmetry(vias_3d):
    from scipy.spatial import cKDTree
    tree = cKDTree(vias_3d)
    dists, idx = tree.query(vias_3d, k=EXPECTED_NN + 1)
    neighbor_idx = idx[:, 1:]

    failures     = []
    total_checks = 0
    max_dev      = 0.0
    angle_counts = {60: 0, 108: 0, 144: 0}

    for i, v_center in enumerate(vias_3d):
        neighbors = vias_3d[neighbor_idx[i]]

        for v1, v2 in combinations(neighbors, 2):
            a = v1 - v_center
            b = v2 - v_center
            na = np.linalg.norm(a)
            nb = np.linalg.norm(b)
            if na < 1e-12 or nb < 1e-12:
                continue
            cos_ang = np.dot(a, b) / (na * nb)
            cos_ang = np.clip(cos_ang, -1.0, 1.0)
            angle   = degrees(acos(cos_ang))
            total_checks += 1

            nearest, dev = nearest_expected(angle)
            max_dev = max(max_dev, dev)
            key = int(round(nearest))
            if key in angle_counts:
                angle_counts[key] += 1
            if dev > TOLERANCE_DEG:
                failures.append({
                    "center_idx": i,
                    "angle":      angle,
                    "nearest":    nearest,
                    "deviation":  dev,
                })

    return failures, total_checks, max_dev, angle_counts


def main():
    print("icosa_sym_check.py -- M8E H3 Symmetry Checker")
    print(f"Expected H3 angles (via centres): {H3_ANGLES_DEG} deg")
    print(f"Nearest neighbours per via: {EXPECTED_NN}")
    print(f"Tolerance: +/-{TOLERANCE_DEG} deg")
    print()

    vias_3d = load_via_3d(VIA_FILE)
    print(f"Loaded {len(vias_3d)} vias from {VIA_FILE} (3D coordinates)")

    from scipy.spatial import cKDTree
    tree = cKDTree(vias_3d)
    dists, _ = tree.query(vias_3d, k=2)
    nn_dists = dists[:, 1]
    nn_min, nn_max = nn_dists.min(), nn_dists.max()
    nn_err = max(abs(nn_min - NN_DIST), abs(nn_max - NN_DIST))
    print(f"Nearest-neighbour distance: [{nn_min:.8f}, {nn_max:.8f}]")
    print(f"Expected {NN_DIST:.8f}  (error={nn_err:.2e})")

    failures, total, max_dev, angle_counts = check_h3_symmetry(vias_3d)

    print(f"\nAngle distribution (total {total} pairs, {total//30} per via):")
    per_via = {k: v // 30 for k, v in angle_counts.items()}
    print(f"   60 deg: {angle_counts[60]:3d} total ({per_via.get(60,0)}/via, expected 2)")
    print(f"  108 deg: {angle_counts[108]:3d} total ({per_via.get(108,0)}/via, expected 2)")
    print(f"  144 deg: {angle_counts[144]:3d} total ({per_via.get(144,0)}/via, expected 2)")
    print(f"MAX_DEVIATION: {max_dev:.6f} deg")

    if not failures:
        print(f"\nPASS: All {total} H3 angles within +/-{TOLERANCE_DEG} deg")
        print("H3_CERT: VALID")
        print("M8E: GEOMETRY OK -- proceed to fab")
        sys.exit(0)
    else:
        print(f"\nFAIL: {len(failures)} / {total} angles out of spec")
        print(f"MAX_DEVIATION: {max_dev:.6f} deg > {TOLERANCE_DEG} deg")
        print("H3_CERT: INVALID")
        print("\nFirst 5 failures:")
        for f in failures[:5]:
            print(f"  Center[{f['center_idx']}]  angle={f['angle']:.4f} deg  "
                  f"nearest={f['nearest']} deg  dev=+{f['deviation']:.4f} deg")
        with open("h3_failures.csv", "w", newline="") as out:
            writer = csv.DictWriter(out,
                fieldnames=["center_idx", "angle", "nearest_expected", "deviation"])
            writer.writeheader()
            for f in failures:
                writer.writerow({
                    "center_idx":       f["center_idx"],
                    "angle":            f["angle"],
                    "nearest_expected": f["nearest"],
                    "deviation":        f["deviation"],
                })
        print("\nFull log: h3_failures.csv")
        print("ACTION: Regenerate icosa_vias.csv or reject layout. Do not fab.")
        sys.exit(1)


if __name__ == "__main__":
    main()
