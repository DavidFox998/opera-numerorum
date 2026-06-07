#!/usr/bin/env python3
"""
24cell_vertices.py -- Opera Numerorum -- Battle Plan v1.6
David Fox -- June 2026

M8E: M8G-Lite 24-Layer Icosahedral Pre-Test
Generates 24_vias.csv: 720 vias = 24 layers x 30 edge midpoints/layer.

PHYSICS RATIONALE:
  120-cell -> 600-cell duality:
    120-cell: 120 dodecahedral cells, 120 layers for M8G, k_c = 3.183
    600-cell: 600 tetrahedral cells, projected to 3D via icosahedral symmetry
    Icosahedron: 12 vertices, 30 edges, 20 faces (the H3 projection)

  Layer structure:
    24 layers x 15 deg/layer = 360 deg (full rotation)
    30 via positions per layer (icosahedron edge midpoints, rotated)
    Total: 24 x 30 = 720 vias -- same count as M8G (720 from 120-cell)
    Layer pitch: 0.1mm  ->  total board: 2.4mm thick

  H3 Bost-Connes fixed point:
    k_c(H4) = 3.183  (120-cell, M8G)
    k_c(H3) ~ 2.13   (icosahedron, M8E)
    Both from Bost-Connes KMS state analysis of the respective Coxeter group.

  Substrate: Rogers 4350B (0.1mm core, 0.5 oz Cu)
  Cost: ~$400 (5 boards) vs M8G ~$3000

RUN: python3 24cell_vertices.py
OUTPUTS:
  24_vias.csv        -- 720 vias (x_mm, y_mm, z_mm, layer, angle_deg)
  icosa_vertices.csv -- 12 icosahedron vertices (reference, unit sphere)
"""

import numpy as np
import csv
import sys
from math import sqrt, pi, cos, sin, atan2, sqrt

PHI = (1 + sqrt(5)) / 2

# PCB params
N_LAYERS   = 24
ROT_DEG    = 360.0 / N_LAYERS   # 15 deg per layer
VIA_RADIUS = 5.0                 # mm (5mm radius disc)
LAYER_PITCH = 0.1                # mm per layer

SEP = "=" * 70

def icosahedron_vertices():
    """
    12 vertices of unit icosahedron.
    Circumradius = sqrt(1 + phi^2). Normalised to unit circumradius.
    Cyclic permutations of (0, +/-1, +/-phi).
    """
    raw = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            raw.append([0,       i,      j * PHI])
            raw.append([i,       j*PHI,  0      ])
            raw.append([j * PHI, 0,      i      ])
    raw = np.array(raw, dtype=float)
    # Normalise to unit circumradius
    R = np.linalg.norm(raw[0])
    return raw / R


def build_edges(verts):
    """30 edges of icosahedron: pairs at minimum pairwise distance."""
    from scipy.spatial import distance_matrix
    D = distance_matrix(verts, verts)
    # Edge length = smallest non-zero pairwise distance
    D_flat = D.flatten()
    edge_len = np.min(D_flat[D_flat > 1e-8])
    edges = []
    for i in range(12):
        for j in range(i + 1, 12):
            if abs(D[i, j] - edge_len) < 1e-6:
                edges.append((i, j))
    return edges, edge_len


def rotation_matrix_z(angle_deg):
    """Rotation matrix about z-axis by angle_deg."""
    a = np.radians(angle_deg)
    return np.array([
        [cos(a), -sin(a), 0],
        [sin(a),  cos(a), 0],
        [0,       0,      1],
    ])


def main():
    print(SEP)
    print("24cell_vertices.py  --  Opera Numerorum  --  Battle Plan v1.6")
    print("M8E: M8G-Lite 24-Layer Icosahedral Pre-Test")
    print("David Fox  --  June 2026")
    print(SEP)
    print()
    print(f"  phi = {PHI:.15f}")
    print(f"  N_LAYERS   = {N_LAYERS}  (rotation per layer = {ROT_DEG} deg)")
    print(f"  VIA_RADIUS = {VIA_RADIUS} mm")
    print(f"  LAYER_PITCH= {LAYER_PITCH} mm")
    print(f"  Total board thickness = {N_LAYERS * LAYER_PITCH} mm")
    print()

    # Step 1: icosahedron vertices
    print("Step 1: Icosahedron vertices ...")
    verts = icosahedron_vertices()
    R_check = np.linalg.norm(verts, axis=1)
    print(f"  Vertices: {len(verts)}  (expected 12)")
    print(f"  Circumradius range: [{R_check.min():.8f}, {R_check.max():.8f}]  (expected 1.0)")
    print()

    # Step 2: edges and edge midpoints
    print("Step 2: Edges and edge midpoints ...")
    edges, edge_len = build_edges(verts)
    print(f"  Edges: {len(edges)}  (expected 30)")
    print(f"  Edge length: {edge_len:.10f}")
    edge_mids = np.array([(verts[i] + verts[j]) / 2 for i, j in edges])
    print(f"  Edge midpoints (via layer 0 template): {len(edge_mids)}")
    print()

    # Euler check
    print(f"  Euler (S^2): V - E + F = 12 - {len(edges)} + 20 = {12 - len(edges) + 20}  (expected 2)")
    print()

    # Step 3: 24 layers, rotate 15 deg/layer, scale to VIA_RADIUS
    print("Step 3: Generating 720 vias (24 layers x 30 midpoints) ...")
    vias = []
    for layer in range(N_LAYERS):
        angle_deg = ROT_DEG * layer              # 0, 15, 30, ..., 345 deg
        R         = rotation_matrix_z(angle_deg)
        z_mm      = layer * LAYER_PITCH
        for mid in edge_mids:
            rotated = R @ mid
            x_mm    = rotated[0] * VIA_RADIUS
            y_mm    = rotated[1] * VIA_RADIUS
            r_mm    = sqrt(x_mm**2 + y_mm**2)
            th_deg  = np.degrees(atan2(y_mm, x_mm))
            vias.append({
                "via_id":    len(vias) + 1,
                "layer":     layer + 1,
                "angle_deg": round(angle_deg, 4),
                "x_mm":      round(x_mm, 6),
                "y_mm":      round(y_mm, 6),
                "z_mm":      round(z_mm, 4),
                "r_mm":      round(r_mm, 6),
                "theta_deg": round(th_deg, 4),
            })

    print(f"  Total vias: {len(vias)}  (expected 720 = 24 x 30)")
    print()

    # Layer summary
    print("  Layer summary (first 5 and last 2):")
    print(f"  {'Layer':>6} {'Angle':>8} {'z_mm':>6} {'Vias':>6}")
    print(f"  {'-'*6} {'-'*8} {'-'*6} {'-'*6}")
    from collections import Counter
    layer_counts = Counter(v["layer"] for v in vias)
    for lay in sorted(layer_counts.keys()):
        ang = (lay - 1) * ROT_DEG
        z   = (lay - 1) * LAYER_PITCH
        if lay <= 5 or lay >= N_LAYERS - 1:
            print(f"  {lay:>6} {ang:>8.1f} deg {z:>6.2f} mm {layer_counts[lay]:>6}")
        elif lay == 6:
            print(f"  {'...':>6}")
    print()

    # Step 4: H3 symmetry check per layer (within each layer)
    print("Step 4: H3 symmetry check (per layer, in-plane) ...")
    # Check angles in layer 1 (angle=0): same as pure icosahedral midpoints
    from itertools import combinations
    from collections import Counter as C2
    layer1_vias = np.array([[v["x_mm"], v["y_mm"]] for v in vias if v["layer"] == 1])
    # Normalise to unit: divide by VIA_RADIUS
    layer1_unit = layer1_vias / VIA_RADIUS

    # Nearest neighbours in 2D (project edge mids to xy plane)
    from scipy.spatial import cKDTree
    tree = cKDTree(layer1_unit)
    dists, idxs = tree.query(layer1_unit, k=5)
    nn_dist = dists[:, 1]

    H3_ANGLES = [60.0, 108.0, 144.0]
    TOL        = 0.01
    max_dev    = 0.0
    fail_count = 0
    total      = 0
    angle_hist = C2()

    for i, center in enumerate(layer1_unit):
        nbrs = layer1_unit[idxs[i, 1:3]]   # 2 nearest in 2D projection
        for v1, v2 in combinations(nbrs, 2):
            a = v1 - center
            b = v2 - center
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            if na < 1e-10 or nb < 1e-10:
                continue
            cos_ang = np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0)
            ang = np.degrees(np.arccos(cos_ang))
            total += 1
            nearest = min(H3_ANGLES, key=lambda x: abs(x - ang))
            dev = abs(ang - nearest)
            max_dev = max(max_dev, dev)
            angle_hist[int(round(nearest))] += 1
            if dev > TOL:
                fail_count += 1

    # Full 3D check in layer 1 (uses stored edge_mids directly)
    tree3 = cKDTree(edge_mids)
    d3, i3 = tree3.query(edge_mids, k=5)
    nn3_dist = d3[:, 1]
    h3_ok    = True
    max3_dev = 0.0
    total3   = 0
    a3_hist  = C2()

    for i, center in enumerate(edge_mids):
        nbr_i = i3[i, 1:5]   # 4 nearest in 3D
        nbrs  = edge_mids[nbr_i]
        for v1, v2 in combinations(nbrs, 2):
            a = v1 - center
            b = v2 - center
            na, nb = np.linalg.norm(a), np.linalg.norm(b)
            if na < 1e-10 or nb < 1e-10:
                continue
            cos_ang = np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0)
            ang = np.degrees(np.arccos(cos_ang))
            total3 += 1
            nearest = min(H3_ANGLES, key=lambda x: abs(x - ang))
            dev = abs(ang - nearest)
            max3_dev = max(max3_dev, dev)
            a3_hist[int(round(nearest))] += 1
            if dev > TOL:
                h3_ok = False

    print(f"  3D H3 check on edge midpoints (layer template):")
    print(f"    Total angle checks: {total3}  (30 vias x C(4,2)=6 pairs)")
    for ang in [60, 108, 144]:
        print(f"    {ang:>3} deg: {a3_hist[ang]:>3} total ({a3_hist[ang]//30}/via)")
    print(f"    MAX_DEVIATION: {max3_dev:.6f} deg  (threshold {TOL} deg)")
    print(f"    H3_CERT: {'VALID' if h3_ok else 'INVALID'}")
    print()

    # Write icosa_vertices.csv
    print("Writing icosa_vertices.csv ...")
    with open("icosa_vertices.csv", "w", newline="") as f:
        f.write("# Icosahedron vertices -- Opera Numerorum -- Battle Plan v1.6\n")
        f.write("# David Fox -- June 2026\n")
        f.write(f"# 12 vertices, unit circumradius, edge_len={edge_len:.10f}\n")
        w = csv.writer(f)
        w.writerow(["n", "x", "y", "z"])
        for k, (x, y, z) in enumerate(verts):
            w.writerow([k+1, f"{x:.12f}", f"{y:.12f}", f"{z:.12f}"])
    print(f"  Written: icosa_vertices.csv  ({len(verts)} rows)")

    # Write 24_vias.csv
    print("Writing 24_vias.csv ...")
    fields = ["via_id", "layer", "angle_deg", "x_mm", "y_mm", "z_mm", "r_mm", "theta_deg"]
    with open("24_vias.csv", "w", newline="") as f:
        f.write("# 720 via positions -- Opera Numerorum -- Battle Plan v1.6\n")
        f.write("# David Fox -- June 2026\n")
        f.write("# M8E: 24 layers x 30 icosahedral edge midpoints, rotated 15 deg/layer\n")
        f.write("# H3 icosahedral symmetry. Substrate: Rogers 4350B, 0.1mm pitch.\n")
        f.write("# Total vias: 720 (same as M8G 120-cell). k_c(H3) ~ 2.13.\n")
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(vias)
    print(f"  Written: 24_vias.csv  ({len(vias)} rows)")

    print()
    print(SEP)
    print(f"COMPLETE:")
    print(f"  icosa_vertices.csv : 12 vertices")
    print(f"  24_vias.csv        : {len(vias)} vias  (24 layers x 30, rotated 15 deg/layer)")
    print()
    print(f"PCB SPEC:")
    print(f"  Substrate   : Rogers 4350B, 0.1mm core, 0.5 oz Cu")
    print(f"  Layers      : {N_LAYERS}")
    print(f"  Layer pitch : {LAYER_PITCH} mm")
    print(f"  Total thick : {N_LAYERS * LAYER_PITCH} mm  (2.4mm)")
    print(f"  Via radius  : {VIA_RADIUS} mm (from board centre)")
    print(f"  Rotation    : {ROT_DEG} deg per layer (= 360/{N_LAYERS})")
    print(f"  Via count   : {len(vias)}  (= M8G 720)")
    print()
    print(f"PHYSICS:")
    print(f"  H4 (120-cell, M8G): k_c = 3.183  120 layers  720 vias")
    print(f"  H3 (icosahedron, M8E): k_c ~ 2.13  24 layers  720 vias")
    print(f"  H3_CERT: {'VALID' if h3_ok else 'INVALID'}  (3D angle check, 180 pairs)")
    print(SEP)


if __name__ == "__main__":
    main()
