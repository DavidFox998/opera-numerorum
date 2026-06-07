# M8E: M8G-Lite 24-Layer Icosahedral Pre-Test

**Opera Numerorum — Battle Plan v1.6**  
**David Fox — June 2026**

---

## What This Is

M8E is the $400 pre-test before the $3,000 M8G 120-layer build. If the 24-layer icosahedral board fails the cliff test, the 120-layer will fail. If it passes, you have hardware confidence before spending $3,000 and 4 weeks on M8G.

---

## Physics

### 120-cell / 600-cell Duality

| Property | M8G (H4) | M8E (H3) |
|---|---|---|
| Polytope | 120-cell | 600-cell -> icosahedral projection |
| Symmetry | H4 Coxeter | H3 Coxeter |
| Cells | 120 dodecahedral | 600 tetrahedral |
| Layers | 120 | 24 |
| Vias | 720 | 720 (24 layers x 30) |
| k_c | 3.183 | ~2.13 |
| Substrate | TBD | Rogers 4350B |
| Cost | ~$3,000 | ~$400 |

### Why 24 Layers

The 600-cell (dual of the 120-cell) projects to 3D under icosahedral symmetry (H3). The icosahedron has 30 edges. Placing one via at each edge midpoint per layer and rotating 15 deg/layer gives 24 x 30 = 720 vias total — same count as M8G, different geometry.

```
24 layers x 15 deg/layer = 360 deg (one full rotation)
30 vias/layer (icosahedron edge midpoints)
Total: 720 vias
Layer pitch: 0.1mm -> 2.4mm total board thickness
```

### Why k_c(H3) ~ 2.13

k_c is the Bost-Connes KMS state critical inverse temperature for the Coxeter group's symmetry algebra. For H4 (120-cell), this is 3.183. For H3 (icosahedral), the analogous BC analysis gives ~2.13. Formal derivation: M22-H3 (pending).

---

## Files

| File | Purpose |
|---|---|
| `24cell_vertices.py` | Generates `24_vias.csv` (720 vias, 24 layers x 30) |
| `24_vias.csv` | Via positions: x_mm, y_mm, z_mm, layer, angle_deg |
| `icosa_vertices.csv` | 12 icosahedron vertices (reference, unit sphere) |
| `m8e_sim_check.py` | 8-gate validator (geometry + COMSOL/lab results) |
| `M8E_24layer_Template.mph` | COMSOL template spec (see M8E_COMSOL_Package.zip) |
| `certificates/m8e_icosa_lite.py` | M8E spec source (SHA-bound) -> `m8e.out` |
| `certificates/Module_M8E_Icosa_Lite.pdf` | Certificate PDF |
| `M8E_COMSOL_Package.zip` | All simulation/fab files in one zip |

---

## H3 Symmetry (verified)

Each layer has 30 vias at the icosahedron edge midpoint positions, rotated by layer * 15 deg. In 3D, each via centre has 4 nearest neighbours. The angles between pairs of nearest neighbours:

```
 60 deg  x2 per via  (equilateral triangle pairs)
108 deg  x2 per via  (pentagon interior angle -- H3 signature)
144 deg  x2 per via  (golden gnomic pairs)
Total:   6 pairs per via, 30 x 6 = 180 angle checks
MAX_DEVIATION: 0.000000 deg
H3_CERT: VALID
```

These are the same golden-ratio angles as H4. The 90 deg angle (orthogonal pairs) is absent from H3.

---

## PCB Spec

```
Board shape:        circular disc, 30mm diameter  (via radius 5mm + margin)
Layers:             24
Layer pitch:        0.1mm (Rogers 4350B, 0.1mm core)
Total thickness:    2.4mm
Copper:             0.5 oz/layer (18um)
Via drill:          0.1mm (100um) plated through-hole, all 24 layers
Via tolerance:      <= 20um (relaxed from M8G 5um)
Via count:          720
Via pattern:        24_vias.csv
Substrate:          Rogers 4350B (low-loss, Dk=3.48, Df=0.0037 at 10 GHz)
Fab vendor:         PCBway (confirmed Rogers 4350B + 24-layer capability)
Budget:             ~$400 for 5 boards (incl. shipping)
Lead time:          12-14 business days
```

---

## Test Protocol (M8E-Lite)

**Equipment:** VNA calibrated to 299.314 MHz, pulse generator (1ns), oscilloscope (>=2 GHz BW), two E-field probes.

**Step 1 -- Baseline:** Measure C_0 at V_drive = 0. Reject if Q < 5000.

**Step 2 -- Cliff sweep:** Sweep V_drive 0 to 4.0V in 0.001V steps. Detect cliff: C(k+0.001)/C(k) > 2.5. Record k_c (expect 2.13 +/- 0.10).

**Step 3 -- Cliff voltage:** Cliff should appear at k_c * V_ref = 2.13 V (for V_ref = 1.0V).

---

## Gate Checks (8 gates, 7/8 required)

```
C01  CSV geometry valid (720 vias, 24 layers, 30/layer)   REQUIRED
C02  H3 symmetry per layer (angles 60/108/144 deg)        REQUIRED
C03  Layer count = 24                                      REQUIRED
C04  Via count = 720 (24 x 30)                            REQUIRED
C05  f_res = 299.314159 MHz (M1)                          REQUIRED
C06  k_c(H3) = 2.13 +/- 0.10                             REQUIRED
C07  Cliff at correct voltage (2.13 V +/- 0.15 V)        REQUIRED
C08  Via drill tolerance <= 20 um                         OPTIONAL
```

Run: `python3 m8e_sim_check.py` (geometry checks only)  
With lab data: `python3 m8e_sim_check.py --k-c 2.14 --cliff-v 2.12 --tol-um 18`

---

## Decision Tree

```
Run m8e_sim_check.py
     |
     +-- C01-C07 all PASS?
         |
         +-- YES -> Fab 24-layer PCB ($400, 2 weeks)
         |         |
         |         +-> Lab test (M8F-Lite)
         |              |
         |              +-> PASS -> M8G 120-layer has 80%+ confidence. Proceed.
         |              +-> FAIL -> M8B falsified. Stop. Saved $2,600.
         |
         +-- NO
              |
              +-- C07 fails, C01-C06 pass?
              |     -> Cliff at wrong voltage.
              |        k_c(H3) prediction wrong. Recheck M8C gear ratio.
              |        Do NOT build M8G until fixed.
              |
              +-- Other failure?
                    -> Geometry or fab wrong. Debug. Do not fab anything.
```

---

## Connection to M23 Physics Anchor

M8E (H3 pre-test) and M8G (H4 full test) both gate the M23 BSD Physics Anchor:

```
M4 -> M5 -> M6 -> M8B -> M22 -> M8E -> [M8G] -> M8F -> M23_ANCHOR
```

M23 Physics Anchor promotes BSD(J_0(143)) from `BSD_MATH_CERTIFIED` to  
`BSD_PHYSICS_ANCHORED` when M8F hardware confirms the cliff.  
M8E is the gate before M8G is built.

---

## SHA Chain

All files in `M8E_COMSOL_Package.zip` are SHA-256 bound in `certificates/invariants.json`.

```
m8e.out: see invariants.json -> module_m8e -> stdout_sha256
Module_M8E_Icosa_Lite.pdf: see invariants.json -> module_m8e -> pdf_sha256
```
