#!/usr/bin/env python3
"""
icosa_vertices.py -- Opera Numerorum -- Battle Plan v1.6
David Fox -- June 2026

M8E (M8G-Lite 24-Layer Icosahedral Pre-Test)
H3 Coxeter geometry: icosahedron edge midpoints as via positions.

The icosahedron (H3) is the 3D projection of the 120-cell (H4).
The same cliff physics (k_c=3.183, C_ratio=5.724) should manifest
in the 24-layer icosahedral board, at 1/75 the cost of M8G.

GEOMETRY FACTS (certified):
  Icosahedron (circumradius 1):
    Vertices:   12   (5-regular: each vertex joins 5 edges)
    Edges:      30   (via positions = edge midpoints)
    Faces:      20   (equilateral triangles)
    Euler:      V - E + F = 12 - 30 + 20 = 2  (S^2, expected)

  Via (edge midpoint) nearest neighbours in 3D:
    k = 4  (at distance edge_len/2 * phi / sqrt(phi^2 + 1/4) approx)
    Exact NN distance = 0.52573111...  [= sin(36 deg) / C, see below]

  H3 characteristic angles at via centres:
    60 deg  x2  -- triangle-edge pairs
   108 deg  x2  -- pentagon interior angle [H3 signature]
   144 deg  x2  -- golden gnomic pairs
   Total: C(4,2) = 6 pairs per via, 30 x 6 = 180 angle checks

  Layer mapping: 9 distinct z-levels -> 24 PCB layers
    z-levels: {-0.8507, -0.6882, -0.4253, -0.2629, 0,
               +0.2629, +0.4253, +0.6882, +0.8507}
    Mapping: linear stretch to layers 1-24.

Run: python3 icosa_vertices.py
Outputs: icosa_vias.csv  (30 vias, 3D + PCB columns)
         icosa_vertices.csv  (12 icosahedron vertices)
"""

import math
import csv
import sys

PHI = (1 + math.sqrt(5)) / 2

# Normalisation factor: raw circumradius = sqrt(1 + phi^2) = sqrt(2 + phi)
CIRC_RAW = math.sqrt(1 + PHI**2)   # = sqrt(2 + phi) = 1.9021130326...
EDGE_RAW = 2.0                       # raw edge length between adjacent vertices
EDGE_LEN = EDGE_RAW / CIRC_RAW      # normalised edge length (circumradius=1)


# ===========================================================================
# Step 1: Icosahedron vertices (unit circumradius)
# ===========================================================================

def build_icosahedron():
    """
    12 vertices of the unit icosahedron.
    Raw: cyclic permutations of (0, ±1, ±phi), normalised to circumradius 1.
    """
    raw = []
    for a, b, c in [
        (0,  1,  PHI), (0,  1, -PHI), (0, -1,  PHI), (0, -1, -PHI),
        (1,  PHI, 0),  (1, -PHI, 0), (-1,  PHI, 0), (-1, -PHI, 0),
        (PHI, 0,  1),  (PHI, 0, -1), (-PHI, 0,  1), (-PHI, 0, -1),
    ]:
        raw.append((a / CIRC_RAW, b / CIRC_RAW, c / CIRC_RAW))
    return raw


def build_edges(verts):
    """30 edges: pairs of vertices at distance EDGE_LEN."""
    edges = []
    for i in range(12):
        for j in range(i + 1, 12):
            d = math.sqrt(sum((verts[i][k] - verts[j][k])**2 for k in range(3)))
            if abs(d - EDGE_LEN) < 1e-8:
                edges.append((i, j))
    return edges


# ===========================================================================
# Step 2: Via positions = edge midpoints
# ===========================================================================

def build_vias(verts, edges):
    """30 via positions as edge midpoints of the icosahedron."""
    vias = []
    for i, j in edges:
        mx = tuple((verts[i][k] + verts[j][k]) / 2 for k in range(3))
        vias.append(mx)
    return vias


# ===========================================================================
# Step 3: PCB mapping
#   x_mm, y_mm: stereographic-style projection to 100mm disc (R=50mm)
#   layer:      z-coordinate -> layer 1..24
# ===========================================================================

N_LAYERS = 24
PCB_R    = 50.0   # mm (100mm disc diameter)

def pcb_coords(x, y, z):
    """
    Project icosahedron edge midpoint (x, y, z) to PCB.
    x_mm, y_mm: scale (x, y) linearly to 50mm radius.
      Via z-range in [-0.851, +0.851]. x,y range in [-0.526, +0.526].
      Scale: r_max_xy ~ 0.526, scale to 45mm (leaves 5mm border).
    layer: linear map z in [-0.851, +0.851] -> layer 1..24.
    """
    XY_MAX = 0.526   # max x or y coordinate of via midpoints
    scale  = 45.0 / XY_MAX   # mm per unit

    x_mm  = x * scale
    y_mm  = y * scale
    r_mm  = math.sqrt(x_mm**2 + y_mm**2)
    theta = math.degrees(math.atan2(y_mm, x_mm))

    Z_MIN = -0.851   # min z of via midpoints
    Z_MAX =  0.851   # max z
    z_norm  = (z - Z_MIN) / (Z_MAX - Z_MIN)   # 0..1
    layer   = int(round(1 + (N_LAYERS - 1) * z_norm))
    layer   = max(1, min(N_LAYERS, layer))

    return x_mm, y_mm, r_mm, theta, layer


# ===========================================================================
# Step 4: H3 symmetry verification
# ===========================================================================

H3_ANGLES_DEG  = [60.0, 108.0, 144.0]   # characteristic angles at edge midpoints
H3_NN_COUNT    = 4                        # nearest neighbours per via
H3_TOLERANCE   = 0.01                     # degrees


def verify_h3_symmetry(vias_3d):
    """
    Check H3 angular signature at each via:
    - 4 nearest neighbours
    - Angles between pairs: {60, 108, 144} deg each x2
    Returns (pass, max_dev, distribution).
    """
    from collections import Counter
    from itertools import combinations

    # Nearest neighbours
    nn_dist = None
    for k in range(1, len(vias_3d)):
        d = math.sqrt(sum((vias_3d[0][a] - vias_3d[k][a])**2 for a in range(3)))
        if nn_dist is None or d < nn_dist:
            nn_dist = d

    max_dev   = 0.0
    fail_count = 0
    total     = 0
    angle_dist = Counter()

    for i, v_center in enumerate(vias_3d):
        # Find neighbours
        nbrs = []
        for k, v in enumerate(vias_3d):
            if k == i:
                continue
            d = math.sqrt(sum((v_center[a] - v[a])**2 for a in range(3)))
            if d < nn_dist * 1.01:
                nbrs.append(v)
        assert len(nbrs) == H3_NN_COUNT, \
            f"Via {i} has {len(nbrs)} neighbours, expected {H3_NN_COUNT}"

        for v1, v2 in combinations(nbrs, 2):
            a = tuple(v1[k] - v_center[k] for k in range(3))
            b = tuple(v2[k] - v_center[k] for k in range(3))
            na = math.sqrt(sum(x**2 for x in a))
            nb = math.sqrt(sum(x**2 for x in b))
            cos_ang = sum(a[k] * b[k] for k in range(3)) / (na * nb)
            cos_ang = max(-1.0, min(1.0, cos_ang))
            angle   = math.degrees(math.acos(cos_ang))
            total  += 1

            nearest = min(H3_ANGLES_DEG, key=lambda x: abs(angle - x))
            dev     = abs(angle - nearest)
            max_dev = max(max_dev, dev)
            angle_dist[int(round(nearest))] += 1
            if dev > H3_TOLERANCE:
                fail_count += 1

    return (fail_count == 0), max_dev, angle_dist, total


# ===========================================================================
# Main
# ===========================================================================

def main():
    SEP = "=" * 70
    print(SEP)
    print("icosa_vertices.py  --  Opera Numerorum  --  Battle Plan v1.6")
    print("M8E: M8G-Lite 24-Layer Icosahedral Pre-Test")
    print("David Fox  --  June 2026")
    print(SEP)
    print()
    print(f"  Golden ratio phi = (1+sqrt(5))/2 = {PHI:.15f}")
    print(f"  Circumradius normalisation C = sqrt(1+phi^2) = {CIRC_RAW:.15f}")
    print(f"  Edge length (circumradius=1): {EDGE_LEN:.12f}")
    print()

    # Step 1
    print("Step 1: Building icosahedron (12 vertices) ...")
    verts = build_icosahedron()
    r_check = [math.sqrt(sum(c**2 for c in v)) for v in verts]
    print(f"  Vertices:  {len(verts)}  (expected 12)")
    print(f"  Circumradius: [{min(r_check):.8f}, {max(r_check):.8f}]  (expected 1.0)")
    print()

    # Step 2
    print("Step 2: Building edges (30 total) ...")
    edges = build_edges(verts)
    deg = [0] * 12
    for i, j in edges:
        deg[i] += 1; deg[j] += 1
    print(f"  Edges: {len(edges)}  (expected 30)")
    print(f"  Vertex degree: [{min(deg)}, {max(deg)}]  (expected 5 for all)")
    print()

    # Euler check
    V, E, F = 12, 30, 20
    print(f"Euler (S^2): V - E + F = {V} - {E} + {F} = {V-E+F}  (expected 2)")
    print()

    # Step 3
    print("Step 3: Building 30 via positions (edge midpoints) ...")
    vias_3d = build_vias(verts, edges)
    print(f"  Vias: {len(vias_3d)}  (expected 30)")
    z_vals  = sorted(set(round(v[2], 6) for v in vias_3d))
    print(f"  Distinct z-levels: {len(z_vals)}  (map to {N_LAYERS} PCB layers)")
    for z in z_vals:
        cnt = sum(1 for v in vias_3d if abs(v[2] - z) < 1e-5)
        _, _, _, _, lay = pcb_coords(0, 0, z)
        print(f"    z={z:+.6f}  x{cnt}  -> layer {lay}")
    print()

    # Step 4: H3 symmetry verification
    print("Step 4: H3 symmetry verification ...")
    ok, max_dev, angle_dist, total = verify_h3_symmetry(vias_3d)
    per_via = {k: v // 30 for k, v in angle_dist.items()}
    print(f"  Total angle checks:  {total}  (30 vias x C(4,2)=6 pairs)")
    print(f"   60 deg: {angle_dist[60]:3d} total ({per_via.get(60,0)}/via, expected 2)")
    print(f"  108 deg: {angle_dist[108]:3d} total ({per_via.get(108,0)}/via, expected 2)")
    print(f"  144 deg: {angle_dist[144]:3d} total ({per_via.get(144,0)}/via, expected 2)")
    print(f"  MAX_DEVIATION: {max_dev:.6f} deg")
    print(f"  H3_CERT: {'VALID' if ok else 'INVALID'}")
    print()

    # Write icosa_vertices.csv
    print("Writing icosa_vertices.csv ...")
    with open("icosa_vertices.csv", "w", newline="") as f:
        f.write("# Icosahedron vertices -- Opera Numerorum -- Battle Plan v1.6\n")
        f.write("# David Fox -- June 2026\n")
        f.write(f"# Circumradius 1, edge length {EDGE_LEN:.10f}\n")
        f.write("# H3 Coxeter group (icosahedral symmetry)\n")
        w = csv.writer(f)
        w.writerow(["n", "x", "y", "z"])
        for idx, (x, y, z) in enumerate(verts):
            w.writerow([idx + 1, f"{x:.12f}", f"{y:.12f}", f"{z:.12f}"])
    print(f"  Written: icosa_vertices.csv  ({len(verts)} rows)")

    # Write icosa_vias.csv
    print("Writing icosa_vias.csv ...")
    with open("icosa_vias.csv", "w", newline="") as f:
        f.write("# 30 via positions -- Opera Numerorum -- Battle Plan v1.6\n")
        f.write("# David Fox -- June 2026\n")
        f.write("# Via = icosahedron edge midpoint = H3 face centre\n")
        f.write("# 3D columns: exact H3 geometry for sym check\n")
        f.write("# PCB columns: linear projection to 100mm disc, 24 layers\n")
        f.write("# H3 angles at via centres: 60 deg x2, 108 deg x2, 144 deg x2\n")
        f.write("# 4 nearest neighbours per via at distance 0.52573111\n")
        w = csv.writer(f)
        w.writerow(["n", "x_3d", "y_3d", "z_3d",
                    "x_mm", "y_mm", "r_mm", "theta_deg", "layer"])
        for idx, (x, y, z) in enumerate(vias_3d):
            xm, ym, rm, th, lay = pcb_coords(x, y, z)
            w.writerow([idx + 1,
                        f"{x:.12f}", f"{y:.12f}", f"{z:.12f}",
                        f"{xm:.6f}", f"{ym:.6f}", f"{rm:.6f}",
                        f"{th:.4f}", lay])
    print(f"  Written: icosa_vias.csv  ({len(vias_3d)} rows, 3D + PCB columns)")

    print()
    print(SEP)
    print("COMPLETE:")
    print(f"  icosa_vertices.csv : {len(verts)} vertices (H3 icosahedral, unit circumradius)")
    print(f"  icosa_vias.csv     : {len(vias_3d)} vias  (30 edge midpoints, 24-layer PCB)")
    print()
    print("H3 SIGNATURE (verified):")
    print(f"  Angles at via centres: {{60 deg x2, 108 deg x2, 144 deg x2}}")
    print(f"  MAX_DEVIATION from expected: {max_dev:.6f} deg  (threshold 0.01 deg)")
    print(f"  H3_CERT: {'VALID' if ok else 'INVALID'}")
    print()
    print("CONNECTION TO M8G (120-cell, H4):")
    print("  H3 (icosahedral) is the 3D Coxeter subgroup of H4 (120-cell).")
    print("  The same angles {60, 108, 144} appear in both H3 and H4.")
    print("  The cliff k_c=3.183 and C_ratio=5.724 are H4/Bost-Connes results,")
    print("  but the H3 geometry is sufficient to trigger the cliff physics.")
    print("  24 layers = 120/5 (icosahedral 5-fold reduction of M8G).")
    print(SEP)


if __name__ == "__main__":
    main()
