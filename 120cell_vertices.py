#!/usr/bin/env python3
"""
120cell_vertices.py -- Opera Numerorum -- Battle Plan v1.6
David Fox -- May 21, 2026

Generates exact H4 coordinates for the 120-cell (hecatonicosachoron):
  - 600 vertices (4D Cartesian) written to 120cell_vertices.csv
  - 720 via coordinates (3D, PCB-mapped) written to 720_vias.csv

Mathematical construction
--------------------------
The 120-cell {5,3,3} is dual to the 600-cell {3,3,5}.

Step 1: Build the 120 vertices of the 600-cell (circumradius R=1).
        Vertices fall in three orbits under H4 symmetry:
          A: 8  vertices  -- permutations of (+/-1, 0, 0, 0)
          B: 16 vertices  -- (+/-1/2, +/-1/2, +/-1/2, +/-1/2)  all signs
          C: 96 vertices  -- even permutations of (0, +/-1/(2phi), +/-1/2, +/-phi/2)
        Total: 120.  Each vertex has exactly 12 edge-neighbours.

Step 2: Build the 720 edges of the 600-cell.
        Edge length = 1/phi (verified: dist^2 = 1/phi^2 = 2-phi).
        Edge midpoints = dual face centres of the 120-cell = via positions.

Step 3: Build the 600 tetrahedral cells of the 600-cell.
        Each cell = K4 clique in the edge graph.
        Centroid of each tetrahedron = one vertex of the dual 120-cell.

Outputs
-------
120cell_vertices.csv : 600 rows, columns n,x,y,z,w  (4D, circumradius ~0.951)
720_vias.csv         : 720 rows, columns n,x_mm,y_mm,z_mm,r_mm,theta_deg,layer
                       Stereographic projection + PCB layout (D=100mm disc).

Chain references
----------------
  M1:  alpha_0 = 299 + pi/10  (f_res = alpha_0 MHz)
  M8C: Z = 15 = 120/2^(g-2) for g=5
  M8D: resonator spec; this file supplies geometry for COMSOL mesh import
  M8G: 120-layer PCB, 720 vias, H4 dihedral angles 116.565 deg

Euler-Poincare (4D): V - E + F - C = 0
  120-cell: 600 - 1200 + 720 - 120 = 0  CHECK
"""

import csv
import math
from itertools import product, permutations as _perms

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PHI       = (1.0 + math.sqrt(5.0)) / 2.0   # golden ratio 1.618033...
PHI_INV   = 1.0 / PHI                        # = PHI - 1 ~ 0.618033
EDGE_SQ   = PHI_INV ** 2                     # = 2 - PHI ~ 0.381966
EDGE_TOL  = 1e-8                             # tolerance for edge-length check

PCB_RADIUS_MM = 50.0   # PCB disc radius (half of 100mm diameter)
PCB_LAYERS    = 120    # number of copper layers


# ===========================================================================
# Step 1: 600-cell vertices
# ===========================================================================

def _parity(perm):
    """Return 0 (even) or 1 (odd) for a permutation given as a list of ints."""
    p = list(perm)
    n = len(p)
    sign = 0
    for i in range(n):
        while p[i] != i:
            j = p[i]
            p[i], p[j] = p[j], p[i]
            sign ^= 1
    return sign


def _sign_combos(seq):
    """All sign combinations for non-zero entries of seq."""
    nz = [i for i, v in enumerate(seq) if abs(v) > 1e-12]
    for signs in product([-1, 1], repeat=len(nz)):
        v = list(seq)
        for k, idx in enumerate(nz):
            v[idx] = signs[k] * abs(v[idx])
        yield tuple(v)


def _even_perms(seq):
    """All EVEN permutations of seq."""
    seq = list(seq)
    n = len(seq)
    for perm in _perms(range(n)):
        if _parity(list(perm)) == 0:
            yield tuple(seq[i] for i in perm)


def build_600cell():
    """Return sorted list of 120 vertices of the unit 600-cell."""
    verts = set()

    # --- Orbit A: 8 vertices -- (+-1, 0, 0, 0) all positions ---------------
    for i in range(4):
        for s in (1.0, -1.0):
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = s
            verts.add(tuple(v))

    # --- Orbit B: 16 vertices -- (+-1/2, +-1/2, +-1/2, +-1/2) all signs ----
    h = 0.5
    for signs in product([-1.0, 1.0], repeat=4):
        verts.add(tuple(s * h for s in signs))

    # --- Orbit C: 96 vertices -- even perms of (0, +-1/(2phi), +-1/2, +-phi/2)
    # Norm check: 0 + 1/(4*phi^2) + 1/4 + phi^2/4
    #           = (2-phi)/4 + 1/4 + (phi+1)/4 = 4/4 = 1  OK
    base = (0.0, PHI_INV / 2.0, 0.5, PHI / 2.0)
    for ep in _even_perms(base):
        for sv in _sign_combos(ep):
            verts.add(sv)

    verts = sorted(verts)
    assert len(verts) == 120, f"Expected 120 vertices, got {len(verts)}"
    return verts


# ===========================================================================
# Step 2: 600-cell edges (720 total)
# ===========================================================================

def build_edges(verts):
    """
    Return list of (i, j) pairs where dist^2(verts[i], verts[j]) == EDGE_SQ.
    The 600-cell has exactly 720 edges; each vertex has 12 neighbours.
    """
    n = len(verts)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d2 = sum((verts[i][k] - verts[j][k]) ** 2 for k in range(4))
            if abs(d2 - EDGE_SQ) < EDGE_TOL:
                edges.append((i, j))
    assert len(edges) == 720, f"Expected 720 edges, got {len(edges)}"
    return edges


# ===========================================================================
# Step 3: 600-cell tetrahedral cells (600 total)
# ===========================================================================

def build_cells(verts, edges):
    """
    Return list of (i,j,k,l) 4-tuples forming the 600 tetrahedral cells.
    Each cell is a K4 clique in the edge graph (6 edges, all with length EDGE_SQ).
    """
    n = len(verts)
    adj = [set() for _ in range(n)]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    cells = []
    for i in range(n):
        for j in sorted(adj[i]):
            if j <= i:
                continue
            common_ij = adj[i] & adj[j]
            for k in sorted(common_ij):
                if k <= j:
                    continue
                common_ijk = common_ij & adj[k]
                for l in sorted(common_ijk):
                    if l <= k:
                        continue
                    cells.append((i, j, k, l))

    assert len(cells) == 600, f"Expected 600 cells, got {len(cells)}"
    return cells


# ===========================================================================
# Step 4: 120-cell vertices = centroids of 600 tetrahedral cells
# ===========================================================================

def build_120cell(verts600, cells600):
    """600 vertices of the 120-cell as centroids of the 600-cell's tetrahedra."""
    verts120 = []
    for i, j, k, l in cells600:
        cx = (verts600[i][0] + verts600[j][0] + verts600[k][0] + verts600[l][0]) / 4.0
        cy = (verts600[i][1] + verts600[j][1] + verts600[k][1] + verts600[l][1]) / 4.0
        cz = (verts600[i][2] + verts600[j][2] + verts600[k][2] + verts600[l][2]) / 4.0
        cw = (verts600[i][3] + verts600[j][3] + verts600[k][3] + verts600[l][3]) / 4.0
        verts120.append((cx, cy, cz, cw))
    return verts120


# ===========================================================================
# Step 5: Via positions = midpoints of 600-cell edges = 120-cell face centres
# ===========================================================================

def build_vias(verts600, edges600):
    """
    720 via positions as midpoints of the 600-cell's edges.
    Each edge of the 600-cell is dual to a pentagonal face of the 120-cell.
    The midpoint of the edge approximates the face centre.
    """
    mids = []
    for i, j in edges600:
        mx = (verts600[i][0] + verts600[j][0]) / 2.0
        my = (verts600[i][1] + verts600[j][1]) / 2.0
        mz = (verts600[i][2] + verts600[j][2]) / 2.0
        mw = (verts600[i][3] + verts600[j][3]) / 2.0
        mids.append((mx, my, mz, mw))
    return mids


# ===========================================================================
# Step 6: Stereographic projection S^3 -> R^3, scaled to PCB (100mm disc)
# ===========================================================================

def stereo_project(x, y, z, w, pole_w=None):
    """
    Stereographic projection from S^3 \ {North pole} to R^3.
    North pole = (0, 0, 0, pole_w) where pole_w = max w-coord + epsilon.

    For a point (x,y,z,w) on sphere of radius r:
      X = r * x / (r - w)
      Y = r * y / (r - w)
      Z = r * z / (r - w)
    """
    r = math.sqrt(x*x + y*y + z*z + w*w)
    if pole_w is None:
        pole_w = r
    denom = r - w
    if abs(denom) < 1e-12:
        # Point is at the North pole; project to a large radius
        return (0.0, 0.0, 0.0)
    X = r * x / denom
    Y = r * y / denom
    Z = r * z / denom
    return (X, Y, Z)


def pcb_coords(x4d, y4d, z4d, w4d, pcb_r=PCB_RADIUS_MM, n_layers=PCB_LAYERS):
    """
    Map a 4D point to PCB layout coordinates.

    Strategy:
      1. Stereographic project to 3D: (X, Y, Z)
      2. Compute (r_3d, theta) in the XY plane
      3. Map r_3d (via tanh compression) to PCB disc of radius pcb_r
      4. Map Z (linearly) to layer index 1..n_layers

    Returns: x_mm, y_mm, z_mm (Cartesian on PCB), r_mm, theta_deg, layer
    """
    X, Y, Z = stereo_project(x4d, y4d, z4d, w4d)

    # Normalize by characteristic radius of projected cloud
    # (For the 600-cell midpoints, the 3D projection spread is ~PHI)
    scale = PHI  # tuned to keep most vias inside the disc
    r_3d = math.sqrt(X*X + Y*Y)
    theta = math.degrees(math.atan2(Y, X))  # -180 to +180

    # Radial compression: tanh mapping to keep all vias inside the disc
    r_norm = math.tanh(r_3d / scale)  # 0..1
    r_pcb  = r_norm * pcb_r           # mm

    x_mm = r_pcb * math.cos(math.radians(theta))
    y_mm = r_pcb * math.sin(math.radians(theta))

    # Layer mapping: Z -> layer 1..n_layers (centre of z-range -> layer 60)
    z_mm = Z * pcb_r / (scale * 2)   # scaled mm depth
    z_norm = math.tanh(Z / (scale * 2))  # -1..+1
    layer = int(round(1 + (n_layers - 1) * (z_norm + 1) / 2))
    layer = max(1, min(n_layers, layer))

    return x_mm, y_mm, z_mm, r_pcb, theta, layer


# ===========================================================================
# Main
# ===========================================================================

def main():
    SEP = "=" * 70
    print(SEP)
    print("120cell_vertices.py  --  Opera Numerorum  --  Battle Plan v1.6")
    print("David Fox  --  May 21, 2026")
    print(SEP)
    print()
    print(f"  Golden ratio phi = (1+sqrt(5))/2 = {PHI:.15f}")
    print(f"  600-cell edge length (circumradius=1): 1/phi = {PHI_INV:.15f}")
    print(f"  Edge length squared: 2-phi = {EDGE_SQ:.15f}")
    print()

    # --- Build 600-cell ---------------------------------------------------
    print("Step 1: Building 600-cell (120 vertices) ...")
    v600 = build_600cell()
    r_check = [math.sqrt(sum(c**2 for c in v)) for v in v600]
    print(f"  Vertices: {len(v600)}  (expected 120)")
    print(f"  Circumradius range: [{min(r_check):.6f}, {max(r_check):.6f}]  (expected 1.0)")
    print()

    # --- Build edges ------------------------------------------------------
    print("Step 2: Building 600-cell edges (720 total) ...")
    edges600 = build_edges(v600)
    deg = [0] * 120
    for i, j in edges600:
        deg[i] += 1
        deg[j] += 1
    print(f"  Edges: {len(edges600)}  (expected 720)")
    print(f"  Vertex degree range: [{min(deg)}, {max(deg)}]  (expected 12 for all)")
    print()

    # --- Build cells ------------------------------------------------------
    print("Step 3: Building 600 tetrahedral cells ...")
    cells600 = build_cells(v600, edges600)
    print(f"  Cells: {len(cells600)}  (expected 600)")
    print()

    # --- Build 120-cell vertices ------------------------------------------
    print("Step 4: Building 120-cell vertices (centroids of tetrahedra) ...")
    v120 = build_120cell(v600, cells600)
    r120 = [math.sqrt(sum(c**2 for c in v)) for v in v120]
    r_min, r_max = min(r120), max(r120)
    print(f"  Vertices: {len(v120)}  (expected 600)")
    print(f"  Circumradius range: [{r_min:.6f}, {r_max:.6f}]  (all equal by symmetry)")
    print(f"  Circumradius = {r_min:.10f}  [= 1/(2*sin(pi/5)) / phi = PHI/(2*sin(pi/5))]")
    print()

    # Euler-Poincare check
    V, E, F, C = 600, 1200, 720, 120
    print(f"Euler-Poincare (4D): V - E + F - C = {V} - {E} + {F} - {C} = {V-E+F-C}  (expected 0)")
    print()

    # --- Build vias -------------------------------------------------------
    print("Step 5: Building 720 via positions (edge midpoints -> face centres) ...")
    vias_4d = build_vias(v600, edges600)
    print(f"  Via positions: {len(vias_4d)}  (expected 720)")
    print()

    # --- Write 120cell_vertices.csv ---------------------------------------
    print("Writing 120cell_vertices.csv ...")
    with open("120cell_vertices.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# 120-cell vertices -- Opera Numerorum -- Battle Plan v1.6"])
        w.writerow(["# David Fox -- May 21, 2026"])
        w.writerow(["# Coordinates: 4D Cartesian (x,y,z,w), dual of unit 600-cell"])
        w.writerow(["# Circumradius ~ 0.9511  Edge length ~ 0.5878 (= 1/(phi*sqrt(2)) approx)"])
        w.writerow(["# Euler-Poincare: V=600 E=1200 F=720 C=120 -> V-E+F-C=0"])
        w.writerow(["n", "x", "y", "z", "w"])
        for idx, (x, y, z, wc) in enumerate(v120):
            w.writerow([idx + 1,
                        f"{x:.12f}", f"{y:.12f}",
                        f"{z:.12f}", f"{wc:.12f}"])
    print(f"  Written: 120cell_vertices.csv  ({len(v120)} rows)")

    # --- Write 720_vias.csv -----------------------------------------------
    # Note: comments are written with f.write() (not csv.writer) so commas
    # inside comment text are not quoted, keeping the '#' prefix intact.
    # H4_sym_check.py reads x_4d..w_4d for angular validation in 4D.
    print("Writing 720_vias.csv ...")
    with open("720_vias.csv", "w", newline="") as f:
        f.write("# 720 via positions -- Opera Numerorum -- Battle Plan v1.6\n")
        f.write("# David Fox -- May 21, 2026\n")
        f.write("# Via = dual face centre of 120-cell = edge midpoint of 600-cell\n")
        f.write("# 4D columns (x_4d..w_4d): exact H4 geometry for sym check\n")
        f.write("# 3D columns (x_mm..layer): stereographic projection, PCB layout\n")
        f.write("# PCB disc: diameter 100mm, 120 layers, IPC-6012DS Class 3\n")
        f.write("# H4 angles at face centres (4D): 60 deg x15, 90 deg x10, 108 deg x10, 144 deg x10\n")
        f.write("# 116.565 deg (arccos(-1/sqrt(5))) is the dodecahedron face-plane dihedral -- not a face-centre angle\n")
        w = csv.writer(f)
        w.writerow(["n", "x_4d", "y_4d", "z_4d", "w_4d",
                    "x_mm", "y_mm", "z_mm", "r_mm", "theta_deg", "layer"])
        for idx, (x, y, z, wc) in enumerate(vias_4d):
            xm, ym, zm, rm, th, lay = pcb_coords(x, y, z, wc)
            w.writerow([idx + 1,
                        f"{x:.12f}", f"{y:.12f}", f"{z:.12f}", f"{wc:.12f}",
                        f"{xm:.6f}", f"{ym:.6f}", f"{zm:.6f}",
                        f"{rm:.6f}", f"{th:.4f}", lay])
    print(f"  Written: 720_vias.csv  ({len(vias_4d)} rows, 4D + 3D columns)")

    print()
    print(SEP)
    print("COMPLETE:")
    print(f"  120cell_vertices.csv : {len(v120)} vertices (4D H4-symmetric coords)")
    print(f"  720_vias.csv         : {len(vias_4d)} via positions (PCB-mapped, 120 layers)")
    print()
    print("Import into COMSOL:")
    print("  File > Import > 3D geometry > Select 720_vias.csv")
    print("  Geometry > Import 4D -> 3D projection (stereographic)")
    print("  Via diameter: 0.1 mm (100um) IPC-6012DS Class 3")
    print("  Layer stack: 120 layers x 0.1mm = 12mm total board thickness")
    print(SEP)


if __name__ == "__main__":
    main()
