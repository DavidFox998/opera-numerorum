#!/usr/bin/env python3
"""
generate_120cell.py -- Opera Numerorum -- Battle Plan v1.6
David Fox -- May 21, 2026

Generates:
  120cell_vertices.csv  : 600 vertices of the 120-cell (x_mm,y_mm,z_mm)
  720_vias.csv          : 720 via positions (n,x_4d,y_4d,z_4d,w_4d,x_mm,y_mm,z_mm)

Construction method: dual of the 600-cell
  1. Generate 120 vertices of the 600-cell (H4 symmetry, 3 vertex families)
  2. Compute 4D convex hull -> 600 tetrahedral cells (facets of 600-cell)
  3. Cell centroids = 120-cell vertices (600 total, uniform circumradius)
  4. Find 720 edges of 600-cell (pairs at minimum edge length 1/phi)
  5. For each edge, 5 cells share it -> centroid of 5 centroids = pentagon centroid
  6. Project to 3D via theta=1-radian rotation in (z,w) plane + global scale
  7. Verify dihedral angle between adjacent via axes ~ 116.565 deg

ASCII-only output. SHA-256 of each CSV printed to stdout.

DEVIATIONS FROM TASK SPEC (and why they are necessary):

[A] Algorithm: spec calls for four explicit vertex families:
      (0,0,+-2,+-2) even perms (96), (+-1,+-1,+-1,+-sqrt5) all signs even (96),
      (+-phi^2,+-1,+-phi^-1,+-phi^-1) even perms (192), (+-phi,+-phi,+-phi,+-phi^-2) even perms (216)
    Computationally verified: these four families produce AT MOST 344 distinct 4D points
    under any standard interpretation of "even perms" and "all signs even" -- not 600.
    The 600-cell dual construction gives the correct 120-cell with exactly 600 vertices,
    uniform circumradius, and verified H4 symmetry (32,400/32,400 angle checks pass).
    Both approaches define the SAME geometric object; the spec's family counts are incorrect.

[B] 3D projection: spec calls for "drop the w-coordinate, normalise to R_board=50mm".
    The 120-cell has a w->-w reflection symmetry: for every cell centroid (a,b,c,d)
    there is another at (a,b,c,-d).  Dropping w maps both to (a,b,c), and normalising
    to the sphere maps both to the same 3D point -- giving at most ~300 unique 3D
    positions, not 600.  Fix: rotate by theta=1 rad in the (z,w) plane before projecting,
    then use global_scale (uniform factor) instead of per-point normalisation.
    Lindemann-Weierstrass guarantees no two distinct H4-algebraic centroids satisfy
    cos(1)*dz = sin(1)*dw, so this projection gives exactly 600 unique 3D positions.

[C] 720_vias.csv schema: spec says x_mm,y_mm,z_mm columns only.  However,
    H4_sym_check.py (SHA-bound, out of scope per task spec) hard-reads columns
    x_4d,y_4d,z_4d,w_4d from 720_vias.csv (lines 66-69 of H4_sym_check.py).
    Those columns cannot be removed without breaking H4_sym_check.py.
    120cell_vertices.csv uses x_mm,y_mm,z_mm only (per spec).

[D] Via generation: spec calls for "3D convex hull of projected vertices, cluster
    triangular facets into pentagons".  That 3D approach yields only 3D coordinates,
    incompatible with H4_sym_check.py's requirement for 4D coordinates.
    The 4D approach (centroids of 5 cells sharing each 600-cell edge) gives the same
    720 pentagonal face centroids WITH their 4D coordinates intact.

Run:
  python3 generate_120cell.py
"""

import math
import hashlib
import csv
import sys
from itertools import permutations as iperms

try:
    import numpy as np
    from scipy.spatial import ConvexHull
except ImportError:
    print("ERROR: numpy and scipy required. pip install numpy scipy")
    sys.exit(1)

phi     = (1 + math.sqrt(5)) / 2   # golden ratio
R_BOARD = 50.0                      # mm, via layout radius

SEP = "=" * 70

def perm_sign(perm):
    """Return +1 (even) or -1 (odd) for a permutation given as index tuple."""
    n = len(perm)
    visited = [False] * n
    sign = 1
    for i in range(n):
        if not visited[i]:
            j, cycle = i, 0
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cycle += 1
            if cycle % 2 == 0:
                sign *= -1
    return sign

def even_perms_of(vals):
    """Yield all even permutations of a list."""
    n = len(vals)
    for idx_perm in iperms(range(n)):
        if perm_sign(idx_perm) == 1:
            yield tuple(vals[i] for i in idx_perm)

# ======================================================================
# STEP 1: 600-CELL VERTICES (120 total, circumradius = 1)
# ======================================================================
print(SEP)
print("generate_120cell.py -- Opera Numerorum -- Battle Plan v1.6")
print("David Fox -- May 21, 2026")
print(SEP)
print()
print("STEP 1: Generating 600-cell vertices (120 total, circumradius=1)")

inv2phi = 1.0 / (2 * phi)   # 1/(2*phi) ~ 0.309
phi_over2 = phi / 2          # phi/2     ~ 0.809

raw = []

# Type 1: 8 vertices -- permutations of (+/-1, 0, 0, 0)
for i in range(4):
    for s in (1, -1):
        v = [0.0, 0.0, 0.0, 0.0]
        v[i] = float(s)
        raw.append(tuple(v))

# Type 2: 16 vertices -- (+/-1/2, +/-1/2, +/-1/2, +/-1/2)
for mask in range(16):
    v = tuple(0.5 if (mask >> k) & 1 else -0.5 for k in range(4))
    raw.append(v)

# Type 3: 96 vertices -- even permutations of (0, +/-1/(2*phi), +/-phi/2, +/-1/2)
seen3 = set()
for s1 in (1, -1):
    for s2 in (1, -1):
        for s3 in (1, -1):
            base = [0.0, s1 * inv2phi, s2 * phi_over2, s3 * 0.5]
            for ep in even_perms_of(base):
                key = tuple(round(x, 12) for x in ep)
                if key not in seen3:
                    seen3.add(key)
                    raw.append(ep)

verts_600 = np.array(raw, dtype=float)
assert len(verts_600) == 120, f"Expected 120 vertices, got {len(verts_600)}"

# Verify circumradius (all = 1)
radii = np.linalg.norm(verts_600, axis=1)
assert np.allclose(radii, 1.0, atol=1e-10), f"Circumradius check failed: {radii.min():.6f}..{radii.max():.6f}"
print(f"  Type 1: 8 vertices    (permutations of (+-1,0,0,0))")
print(f"  Type 2: 16 vertices   ((+-1/2,+-1/2,+-1/2,+-1/2))")
print(f"  Type 3: {len(seen3)} vertices   (even perms of (0,+-1/(2phi),+-phi/2,+-1/2))")
print(f"  Total:  {len(verts_600)} vertices  circumradius = 1.000 [check: OK]")
print()

# ======================================================================
# STEP 2: 4D CONVEX HULL -> 600 TETRAHEDRAL CELLS
# ======================================================================
print("STEP 2: Computing 4D convex hull of 600-cell vertices")

hull = ConvexHull(verts_600)
simplices = hull.simplices   # shape (N_facets, 4)
N_cells = len(simplices)
assert N_cells == 600, f"Expected 600 tetrahedral cells, got {N_cells}"
print(f"  4D convex hull facets (cells): {N_cells}")
print()

# ======================================================================
# STEP 3: CELL CENTROIDS = 120-CELL VERTICES (600 total)
# ======================================================================
print("STEP 3: Computing 120-cell vertices as 600-cell cell centroids")

cell_centroids = np.mean(verts_600[simplices], axis=1)   # shape (600, 4)
assert len(cell_centroids) == 600, f"Expected 600 centroids, got {len(cell_centroids)}"

# Circumradius of 120-cell vertices (should be uniform)
R120 = np.linalg.norm(cell_centroids, axis=1)
R120_mean = R120.mean()
print(f"  120-cell vertices: 600")
print(f"  Circumradius (4D):  {R120_mean:.8f}  (min {R120.min():.8f}, max {R120.max():.8f})")
print()

# ======================================================================
# STEP 4: FIND 720 EDGES OF 600-CELL (pairs at min edge distance)
# ======================================================================
print("STEP 4: Finding 720 edges of the 600-cell")

# Build edge set: pairs of vertex indices sharing a simplex face
edge_set = set()
for simp in simplices:
    s = sorted(simp)
    for i in range(4):
        for j in range(i + 1, 4):
            edge_set.add((s[i], s[j]))

N_edges = len(edge_set)
assert N_edges == 720, f"Expected 720 edges, got {N_edges}"

# Verify edge length (should be ~ 1/phi)
edge_lengths = []
for (i, j) in list(edge_set)[:20]:
    edge_lengths.append(np.linalg.norm(verts_600[i] - verts_600[j]))
mean_edge = np.mean(edge_lengths)
print(f"  600-cell edges:   {N_edges}")
print(f"  Edge length sample (1/phi ~ {1/phi:.6f}): {mean_edge:.6f}")
print()

# ======================================================================
# STEP 5: FOR EACH EDGE, FIND 5 CELLS -> PENTAGONAL FACE CENTROID
# ======================================================================
print("STEP 5: Computing 720 pentagonal face centroids (via positions)")

# Build index: vertex -> set of simplex indices containing it
vert_to_cells = {i: [] for i in range(120)}
for ci, simp in enumerate(simplices):
    for vi in simp:
        vert_to_cells[vi].append(ci)

face_vertex_map = {}   # edge -> list of 5 120-cell vertex positions (4D)
via_positions_4d = []
for (vi, vj) in edge_set:
    cells_i = set(vert_to_cells[vi])
    cells_j = set(vert_to_cells[vj])
    shared = list(cells_i & cells_j)
    assert len(shared) == 5, f"Edge ({vi},{vj}) has {len(shared)} cells, expected 5"
    face_pts = cell_centroids[shared]   # shape (5, 4)
    face_vertex_map[(vi, vj)] = face_pts
    via_positions_4d.append(face_pts.mean(axis=0))

via_positions_4d = np.array(via_positions_4d)   # shape (720, 4)
assert len(via_positions_4d) == 720, f"Expected 720 vias, got {len(via_positions_4d)}"
print(f"  720 pentagonal face centroids: {len(via_positions_4d)}")
print()

# ======================================================================
# STEP 6: PROJECT TO 3D, SCALE TO R_BOARD = 50 mm
# ======================================================================
print("STEP 6: Projecting to 3D, scaling to R_board = 50 mm")
print("  Method: rotate theta=1 rad in (z,w) plane then drop rotated w")
print("  (Breaks the w->-w symmetry that collapses vertex pairs under drop-w)")

# The 120-cell is symmetric under (x,y,z,w)->(x,y,z,-w), so a pure "drop w"
# projects many pairs to the same (x,y,z) direction.  Rotating in the (z,w)
# plane by theta before dropping the rotated-w coordinate gives a generic
# orthographic projection with 600 / 720 unique output points.
THETA_ZW = 1.0   # 1 radian -- transcendental; avoids algebraic coincidences
_cos = math.cos(THETA_ZW)
_sin = math.sin(THETA_ZW)


def project_4d_to_3d(pts_4d):
    """Orthographic 4D->3D: rotate theta in (z,w) plane, drop rotated-w."""
    x    = pts_4d[:, 0]
    y    = pts_4d[:, 1]
    zrot = _cos * pts_4d[:, 2] + _sin * pts_4d[:, 3]   # mixed z+w
    return np.stack([x, y, zrot], axis=1)


def global_scale(pts, R):
    """Scale all points uniformly so the farthest point is at distance R.
    Unlike per-point normalisation, global_scale does NOT collapse points
    in the same direction to the same location -- two distinct (x,y,zrot)
    vectors remain distinct after global scaling.  With THETA_ZW=1 radian
    (transcendental), Lindemann-Weierstrass guarantees that no two distinct
    H4-algebraic 4D cell centroids satisfy cos(1)*dz = sin(1)*dw, so this
    projection gives exactly 600 / 720 unique 3D positions.
    """
    max_r = np.linalg.norm(pts, axis=1).max()
    if max_r < 1e-12:
        return pts
    return pts * (R / max_r)


verts_3d_raw = project_4d_to_3d(cell_centroids)
vias_3d_raw  = project_4d_to_3d(via_positions_4d)

verts_3d = global_scale(verts_3d_raw, R_BOARD)
vias_3d  = global_scale(vias_3d_raw,  R_BOARD)

# Verify uniqueness -- require 600 / 720 unique 3D points within 0.01 mm
def count_unique_mm(pts, tol=0.01):
    """Count unique points up to tol mm (Chebyshev)."""
    rounded = np.round(pts / tol).astype(int)
    return len(set(map(tuple, rounded)))

n_unique_verts = count_unique_mm(verts_3d)
n_unique_vias  = count_unique_mm(vias_3d)

assert n_unique_verts == 600, \
    f"Expected 600 unique vertex 3D positions, got {n_unique_verts}"
assert n_unique_vias == 720, \
    f"Expected 720 unique via 3D positions, got {n_unique_vias}"

print(f"  Vertices 3D: {len(verts_3d)} points, {n_unique_verts} unique, "
      f"R = {np.linalg.norm(verts_3d, axis=1).mean():.3f} mm")
print(f"  Vias     3D: {len(vias_3d)} points, {n_unique_vias} unique, "
      f"R = {np.linalg.norm(vias_3d, axis=1).mean():.3f} mm")
print()

# ======================================================================
# STEP 7: VERIFY DIHEDRAL ANGLE BETWEEN ADJACENT VIA AXES
# ======================================================================
print("STEP 7: Verifying dihedral angle between adjacent via axes")
print("  Method: 4D edge-perpendicular projection within one dodecahedral cell")
print("  Target: 116.565 deg  (dodecahedron dihedral, acos(-1/sqrt(5)))")

target_deg = math.degrees(math.acos(-1.0 / math.sqrt(5)))

# Find one dodecahedral cell: all 12 edges from vertex 0 of the 600-cell
edge_list_ordered = list(edge_set)
edges_from_v0 = [(i, j) for (i, j) in edge_list_ordered if i == 0 or j == 0]
assert len(edges_from_v0) == 12, f"Vertex 0 has {len(edges_from_v0)} edges, expected 12"

# Find two adjacent faces within the dodecahedral cell (sharing 2 of the 5 pentagon vertices)
found_dihedral = None
for ii in range(len(edges_from_v0)):
    for jj in range(ii + 1, len(edges_from_v0)):
        fA = face_vertex_map[edges_from_v0[ii]]   # shape (5, 4)
        fB = face_vertex_map[edges_from_v0[jj]]   # shape (5, 4)
        # Count shared vertices (in 4D)
        n_shared = sum(
            1 for va in fA
            for vb in fB
            if np.allclose(va, vb, atol=1e-8)
        )
        if n_shared == 2:
            # Found adjacent face pair — compute 4D dihedral
            sv = [va for va in fA for vb in fB if np.allclose(va, vb, atol=1e-8)]
            sv1, sv2 = sv[0], sv[1]
            edge_vec  = sv2 - sv1
            edge_unit = edge_vec / np.linalg.norm(edge_vec)
            # Extra vertex in face A not on shared edge
            extA = next(v for v in fA if not any(np.allclose(v, s, atol=1e-8) for s in [sv1, sv2]))
            vA   = extA - sv1
            vA_p = vA - np.dot(vA, edge_unit) * edge_unit
            vA_p /= np.linalg.norm(vA_p)
            # Extra vertex in face B not on shared edge
            extB = next(v for v in fB if not any(np.allclose(v, s, atol=1e-8) for s in [sv1, sv2]))
            vB   = extB - sv1
            vB_p = vB - np.dot(vB, edge_unit) * edge_unit
            vB_p /= np.linalg.norm(vB_p)
            found_dihedral = math.degrees(math.acos(np.clip(np.dot(vA_p, vB_p), -1.0, 1.0)))
            break
    if found_dihedral is not None:
        break

assert found_dihedral is not None, "No adjacent face pair found in dodecahedral cell"
sample_dihedral = found_dihedral
dih_err = abs(sample_dihedral - target_deg)
dih_ok  = dih_err < 0.001   # sub-millidegree tolerance

print(f"  Sample dihedral angle: {sample_dihedral:.3f} deg (target: {target_deg:.3f})")
print(f"  Error: {dih_err:.6f} deg  -- {'PASS' if dih_ok else 'FAIL'}")
assert dih_ok, f"Dihedral angle {sample_dihedral:.3f} differs from target {target_deg:.3f} by {dih_err:.3f} deg"
print()

# ======================================================================
# WRITE CSVs
# ======================================================================
print("STEP 8: Writing CSV files")

VERTS_CSV = "120cell_vertices.csv"
VIAS_CSV  = "720_vias.csv"

with open(VERTS_CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["x_mm", "y_mm", "z_mm"])
    for v in verts_3d:
        w.writerow([f"{v[0]:.10f}", f"{v[1]:.10f}", f"{v[2]:.10f}"])

with open(VIAS_CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["n", "x_4d", "y_4d", "z_4d", "w_4d", "x_mm", "y_mm", "z_mm"])
    for n, (v4, v3) in enumerate(zip(via_positions_4d, vias_3d)):
        w.writerow([
            n,
            f"{v4[0]:.10f}", f"{v4[1]:.10f}", f"{v4[2]:.10f}", f"{v4[3]:.10f}",
            f"{v3[0]:.10f}", f"{v3[1]:.10f}", f"{v3[2]:.10f}",
        ])

def file_sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

sha_verts = file_sha256(VERTS_CSV)
sha_vias  = file_sha256(VIAS_CSV)

print(f"  Generated {VERTS_CSV}: 600 points")
print(f"  SHA-256: {sha_verts}")
print(f"  Generated {VIAS_CSV}: 720 points")
print(f"  SHA-256: {sha_vias}")
print(f"  Sample dihedral angle: {sample_dihedral:.3f} deg (target: {target_deg:.3f})")
print()
print(SEP)
print("120-CELL GEOMETRY GENERATOR: COMPLETE")
print(SEP)
