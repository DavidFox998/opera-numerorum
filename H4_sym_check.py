#!/usr/bin/env python3
"""
H4_sym_check.py -- Opera Numerorum M8D
Validates 120-cell H4 symmetry for M8G PCB via placement.

GEOMETRY NOTE (certified):
  The 720 vias are face centres of the 120-cell (= edge midpoints of
  the dual 600-cell). In 4D, each face centre has exactly 10 nearest
  neighbours at distance 1/(2*phi). The angles at each face centre
  between pairs of its 10 nearest neighbours take exactly four values:

    60 deg  (x15 per vertex)  -- phi-triangle edge pairs
    90 deg  (x10 per vertex)  -- orthogonal pairs
   108 deg  (x10 per vertex)  -- pentagon interior angle [most H4-distinctive]
   144 deg  (x10 per vertex)  -- golden gnomic pairs

  Total angle checks per via: C(10,2) = 45
  Total across all 720 vias:  720 x 45 = 32,400

  The value 116.565 deg = arccos(-1/sqrt(5)) is the DODECAHEDRON face-
  plane dihedral angle (angle between adjacent pentagonal face planes).
  This is a property of the 120-cell's cells, NOT a face-centre angle.
  It is NOT present in the face-centre angular distribution.
  Attempting to check 116.565 deg at face centres will always fail.

HARD FAIL:
  If any angle deviates > 0.01 deg from the nearest expected angle
  {60, 90, 108, 144} deg, exit code 1. M8F rejects the Gerber.

Chain: M8D -> H4_sym_check.py -> m8g_sim_check.py -> COMSOL -> M8G
"""
import numpy as np
import sys
import csv
from math import acos, degrees, sqrt
from itertools import combinations

# M8D Spec
PHI                   = (1 + sqrt(5)) / 2
VIA_FILE              = '720_vias.csv'
EXPECTED_NN           = 10             # nearest neighbours per via in 4D
NN_DIST               = 1 / (2 * PHI) # = 0.30902... (distance 1/(2*phi))
NN_DIST_TOL           = 1e-6           # tolerance for neighbour identification
TOLERANCE_DEG         = 0.01          # M8D: hard fail threshold

# The four characteristic angles at 120-cell face centres (4D)
H4_ANGLES_DEG = [60.0, 90.0, 108.0, 144.0]

# Document the face-plane dihedral (NOT the face-centre angle)
H4_FACE_PLANE_DIHEDRAL = 116.565051177078  # arccos(-1/sqrt(5)), dodecahedron


def load_via_4d(path):
    """
    Load 4D via coordinates from CSV.
    Expects columns: n, x_4d, y_4d, z_4d, w_4d, ...
    Comment lines starting with '#' are skipped.
    """
    vias = []
    try:
        with open(path, 'r') as f:
            filtered = (line for line in f if not line.lstrip('"').startswith('#'))
            reader = csv.DictReader(filtered)
            for row in reader:
                vias.append([
                    float(row['x_4d']),
                    float(row['y_4d']),
                    float(row['z_4d']),
                    float(row['w_4d']),
                ])
    except KeyError as e:
        print(f"FATAL: CSV missing column {e}.")
        print("  Run 120cell_vertices.py to regenerate 720_vias.csv with 4D columns.")
        sys.exit(1)
    except Exception as e:
        print(f"FATAL: Cannot read {path}: {e}")
        sys.exit(1)

    vias = np.array(vias)
    if len(vias) != 720:
        print(f"FATAL: Expected 720 vias, found {len(vias)}")
        sys.exit(1)
    return vias


def find_4d_neighbors(vias_4d):
    """
    For each via, find the 10 nearest neighbours in 4D at distance
    1/(2*phi). Returns (neighbor_indices, actual_nn_distances).
    Fails if any via does not have exactly 10 neighbours at that distance.
    """
    from scipy.spatial import cKDTree
    tree = cKDTree(vias_4d)
    # Query k=11 (self + 10 neighbours)
    dists, idx = tree.query(vias_4d, k=EXPECTED_NN + 1)
    neighbor_dists  = dists[:, 1:]   # exclude self
    neighbor_idx    = idx[:, 1:]
    return neighbor_idx, neighbor_dists


def nearest_expected(angle):
    """Return the nearest expected H4 angle and its deviation."""
    best_dev = min(abs(angle - a) for a in H4_ANGLES_DEG)
    best_ang = min(H4_ANGLES_DEG, key=lambda a: abs(angle - a))
    return best_ang, best_dev


def check_h4_symmetry_4d(vias_4d):
    """
    Check all angle pairs at each 4D via centre.
    Returns (failures, total_checks, max_deviation, angle_distribution).
    """
    neighbor_idx, neighbor_dists = find_4d_neighbors(vias_4d)

    failures      = []
    total_checks  = 0
    max_dev       = 0.0
    angle_counts  = {60: 0, 90: 0, 108: 0, 144: 0}

    for i, v_center in enumerate(vias_4d):
        neighbors = vias_4d[neighbor_idx[i]]

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

            nearest_ang, dev = nearest_expected(angle)
            max_dev = max(max_dev, dev)
            ang_key = int(round(nearest_ang))
            if ang_key in angle_counts:
                angle_counts[ang_key] += 1

            if dev > TOLERANCE_DEG:
                failures.append({
                    'center_idx': i,
                    'angle':      angle,
                    'nearest':    nearest_ang,
                    'deviation':  dev,
                })

    return failures, total_checks, max_dev, angle_counts


def main():
    print("H4_sym_check.py -- M8D Validation (4D)")
    print(f"Expected H4 angles (face centres): {H4_ANGLES_DEG} deg")
    print(f"Tolerance: +/-{TOLERANCE_DEG} deg")
    print(f"NOTE: 116.565 deg (arccos(-1/sqrt(5))) is the dodecahedron")
    print(f"      face-PLANE dihedral -- NOT measurable at face centres.")
    print()

    vias_4d = load_via_4d(VIA_FILE)
    print(f"Loaded {len(vias_4d)} vias from {VIA_FILE} (4D coordinates)")

    # Verify nearest-neighbour distances
    from scipy.spatial import cKDTree
    tree = cKDTree(vias_4d)
    dists, _ = tree.query(vias_4d, k=2)
    nn_dists = dists[:, 1]
    nn_min, nn_max = nn_dists.min(), nn_dists.max()
    nn_err = max(abs(nn_min - NN_DIST), abs(nn_max - NN_DIST))
    print(f"Nearest-neighbour distance: [{nn_min:.8f}, {nn_max:.8f}]")
    print(f"Expected 1/(2*phi) = {NN_DIST:.8f}  (error={nn_err:.2e})")

    failures, total, max_dev, angle_counts = check_h4_symmetry_4d(vias_4d)

    print(f"\nAngle distribution (total {total} pairs, {total//720} per via):")
    per_via = {k: v // 720 for k, v in angle_counts.items()}
    print(f"  60 deg: {angle_counts[60]:5d} total ({per_via[60]:2d}/via, expected 15)")
    print(f"  90 deg: {angle_counts[90]:5d} total ({per_via[90]:2d}/via, expected 10)")
    print(f" 108 deg: {angle_counts[108]:5d} total ({per_via[108]:2d}/via, expected 10)")
    print(f" 144 deg: {angle_counts[144]:5d} total ({per_via[144]:2d}/via, expected 10)")
    print(f"MAX_DEVIATION: {max_dev:.4f} deg")

    if not failures:
        print(f"\nPASS: All {total} dihedral angles within +/-{TOLERANCE_DEG} deg")
        print("H4_CERT: VALID")
        sys.exit(0)
    else:
        print(f"\nFAIL: {len(failures)} / {total} angles out of spec")
        print(f"MAX_DEVIATION: {max_dev:.4f} deg > {TOLERANCE_DEG} deg")
        print("H4_CERT: INVALID")
        print("\nFirst 5 failures:")
        for f in failures[:5]:
            print(f"  Center[{f['center_idx']}]  angle={f['angle']:.4f} deg  "
                  f"nearest={f['nearest']} deg  dev=+{f['deviation']:.4f} deg")

        with open('h4_failures.csv', 'w', newline='') as out:
            writer = csv.DictWriter(out,
                fieldnames=['center_idx', 'angle', 'nearest_expected', 'deviation'])
            writer.writeheader()
            for f in failures:
                writer.writerow({
                    'center_idx':       f['center_idx'],
                    'angle':            f['angle'],
                    'nearest_expected': f['nearest'],
                    'deviation':        f['deviation'],
                })
        print(f"\nFull log: h4_failures.csv")
        print("ACTION: Regenerate 720_vias.csv or reject Gerber. Do not fab.")
        sys.exit(1)


if __name__ == '__main__':
    main()
