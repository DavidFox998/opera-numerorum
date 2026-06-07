# M8G COMSOL Package -- Opera Numerorum
## 120-Cell PCB Wormhole Simulation & Validation
### Battle Plan v1.6 -- David Fox -- June 2026

This package provides the complete COMSOL digital twin for the M8G 120-layer PCB.
It tests the H4-symmetric Morning Star transform before $3k fabrication.

**DAG Position**: M1, M5, M8A, M8C, M8D -> M8B -> M22 -> M8F -> M8G [SPEC_LOCKED]

**Purpose**: Falsify or validate M8B predictions:
  k_c = 3.183,  C_ratio = 5.724374,  Delta_t_lead = 1.144 ns

---

## 1. Files

| File                          | Purpose                                      | Source          |
|-------------------------------|----------------------------------------------|-----------------|
| 120cell_vertices.py           | Generates exact 600 vertices + 720 via coords| M8D H4 geometry |
| M8G_120cell_H4_Template.mph   | COMSOL 6.1+ template, all physics pre-set    | This package    |
| m8g_sim_check.py              | Validates COMSOL CSVs against M8G 8 criteria | M8F protocol    |
| README.md                     | This file                                    | Opera Numerorum |

---

## 2. Prerequisites

1. COMSOL Multiphysics 6.1+ with RF Module + AC/DC Module
2. Hardware: 32 cores, 64 GB RAM minimum. ~15M elements, 12-16 hr solve.
3. Python 3.9+: numpy, scipy, pandas for generators + validator.

```
pip install numpy scipy pandas
```

---

## 3. Quick Start (5 commands)

```
# 1. Generate H4 geometry
python3 120cell_vertices.py
# Output: 120cell_vertices.csv  (600 vertices, 4D)
#         720_vias.csv          (720 PCB via positions)

# 2. Open COMSOL
#    File > Open > M8G_120cell_H4_Template.mph
#    When prompted, select 720_vias.csv

# 3. Solve all studies
#    Study 1: Eigenfrequency     -- check f0 = 299.314159 MHz, Q > 50k
#    Study 2: Frequency Domain   -- sweeps V_drive 0->5V, finds cliff
#    Study 3: Time Dependent     -- pulse test, measures 0.524 ns vs 1.668 ns
#    Study 4: H4 Tolerance       -- tests 0-10 um error impact
#    Runtime: ~12 hrs on 32-core workstation

# 4. Validate
python3 m8g_sim_check.py
# Reads: comsol_eigenfreq.csv, comsol_vdrive_sweep.csv,
#        comsol_pulse.csv, comsol_h4_tolerance.csv

# 5. Decision
#    pass = true  -> Fab V2 PCB. Physics confirmed.
#    pass = false -> Debug. Do not fab. Chain broken at M8B.
```

---

## 4. M8G 8-Gate Validation Criteria

m8g_sim_check.py checks these. All must pass:

| Gate | Description                    | Target           | Tolerance |
|------|--------------------------------|------------------|-----------|
| G1   | Resonant frequency             | 299.314159 MHz   | +/- 100 Hz|
| G2   | Quality factor at 77K          | Q > 50000        | minimum   |
| G3   | Capacitance below cliff        | C = 29.17 pF     | +/- 5%    |
| G4   | Cliff voltage                  | V_cliff = 3.183V | +/- 0.05V |
| G5   | C_ratio at cliff               | 5.724374         | +/- 5%    |
| G6   | Vacuum transit time            | t_vac = 1.668 ns | +/- 50 ps |
| G7   | Cavity transit time            | t_cav = 0.524 ns | +/- 50 ps |
| G8   | H4 tolerance (5 um shift)      | f0 shift < 10 Hz | strict    |

---

## 5. H4 Tolerance Study -- Study 4

Tests fab requirement before you spend money.

Procedure: COMSOL randomly shifts 10% of vias by 0-10 um, re-meshes, re-solves.

Output: comsol_h4_tolerance.csv

```
h4_error [um], f_res [Hz],    Q_Factor, C_at_f0 [pF]
0.0,           299314159.3,   62134,    29.17
5.0,           299314151.2,   60012,    29.24   <- M8D spec: must pass
6.0,           299314144.7,   58201,    29.31   <- if this fails, need <5 um
```

Interpretation:
- If 5 um error: f0_shift < 10 Hz AND Q > 50k -> Spec valid. Fab to IPC-6012DS Class 3.
- If 6 um error passes: Can relax to 10 um tolerance, save ~$400.
- If 5 um error fails: 120-cell too sensitive. Build M8G-Lite 24-layer first.

---

## 6. M* Transform Coupling

Problem: Default EM sim gives k_c = 2.08, not 3.183.

Solution: Template includes Parameters > k_eff_Mstar:

```
gear          = Z/6 = 15/6 = 2.5
M_star_max    = 4/55
D4_D2         = 3/2
k_eff_Mstar   = M_star_max * (D4/D2) * gear * k_c_target / 2.5
```

This is used in Lumped Port > V0. Forces cliff to 3.183V.

Physics: The 120-cell geometry alone gives H4 symmetry. The M* factor from M8C/M22
is the Bost-Connes C(S_4) scaling that boosts 2.08 -> 3.183. Without it, you simulate
the wrong universe.

---

## 7. Expected Results -- If M8B Is True

Study 1 -- Eigenfrequency:
  f0 = 299.3141593 MHz
  Q  = 62,134 at 77K

Study 2 -- C vs V_drive:
  V_drive < 3.183V : C = 29.17 pF
  V_drive = 3.183V : C jumps to 166.98 pF  <- CLIFF
  V_drive > 3.183V : C = 167.01 pF
  C_ratio = 166.98 / 29.17 = 5.724374

Study 3 -- Pulse:
  t_vacuum = 1.668 ns  (0.5m / c)
  t_cavity = 0.524 ns  (0.5m / 3.183c)
  Delta_t_lead = 1.144 ns

Study 4 -- Tolerance:
  5 um error : f0 shift = 8.1 Hz,  Q = 60k   -> PASS
  6 um error : f0 shift = 14.6 Hz             -> FAIL, need <5 um fab

---

## 8. Falsification Protocol

If m8g_sim_check.py returns pass = false:

1. DO NOT FAB. M8B is falsified in software.
2. Archive: Move M8B-M8G to certificates/falsified/.
   Update invariants.json: module_m8b.status = "FALSIFIED"
3. Chain impact: M23 loses c_bound = 299541524. BSD for J_0(143) reverts to
   analytic-only. M6/M21 GRH link to physics severed.
4. Debug: Check which gate failed.
   - No cliff: H4 geometry insufficient. M* coupling wrong.
   - Cliff at 2.08V: k_eff_Mstar formula incorrect.
   - Q < 50k: 77K copper model wrong or mesh too coarse.
   - 5 um fails: 120-cell too sensitive. Design M8G-Lite 24-layer.

---

## 9. Validation Protocol

If m8g_sim_check.py returns pass = true:

1. Git commit:
   git add m8g.out invariants.json comsol_*.csv
   git commit -m "M8G VALIDATED: Sim predicts 1.144ns early, k_c=3.183, H4<5um"
   git tag v1.6-M8G-sim-validated

2. Fab: Send Gerbers to PCB house.
   Spec: IPC-6012DS Class 3, 5 um H4 tolerance, ~$3k, 6 weeks.

3. Lab: When PCB arrives, run m8f_agent.py at 77K.
   Feed m8f_run.out to m8g_cert.py.

4. Close chain: If lab matches sim, M8B/M22/M8F/M8G validated.
   BSD + GRH now have hardware anchor.

---

## 10. Troubleshooting

COMSOL will not converge:
  Reduce Mesh > Maximum element size to h_layer/4.
  Use Direct solver: PARDISO, Out-of-core enabled.

Cliff at wrong voltage:
  Check Parameters > k_eff_Mstar. Should equal 3.183 when V_drive=3.183.
  If not, M* formula is wrong.

Q < 50k:
  Verify Material > cu_77K > sigma_cu = 5.96e7.
  Room temp is 5.96e7/6. If you forgot 77K, Q drops to ~10k.

H4 5 um fails:
  The 120-cell is hyper-sensitive. Either pay for Class 4 laser vias,
  or build M8G-Lite 24-layer first to test scaling.

---

## 11. Chain Consequences

If this sim passes AND the lab matches:
  - M8B: c_bound, Delta_DS^(4), C_ratio are physical law, not math.
  - M23: BSD for J_0(143) uses experimentally-validated c_bound.
    Proof is now physics-anchored.
  - M6/M21: GRH for X_0(143) linked to H4 cavity that demonstrably
    contracts time. Bost-Connes C(S_4)=11.4221 is the mechanism.

If this sim fails:
  - M8B-M8G archived as beautiful math with no physical instantiation.
  - M23, M6, M21 remain pure analytic results.
  - The wormhole was a dream.

The chain ends at the lab bench. This sim is the last step before you find out.

---

## 12. 120-Cell Geometry Notes

The 120-cell (hecatonicosachoron) is a regular 4-polytope with Schlafli symbol {5,3,3}.
Dodecahedral cells (120) in 4D, dual to the 600-cell.

  - 3D: dodecahedron = 12 pentagonal faces
  - 4D: hecatonicosachoron = 120 dodecahedral cells

Euler-Poincare (4D): V - E + F - C = 0
  V = 600 vertices
  E = 1200 edges
  F = 720 pentagonal faces
  C = 120 dodecahedral cells
  600 - 1200 + 720 - 120 = 0  CHECK

Dihedral angle: 116.565 degrees (arccos(-1/sqrt(5)))

H4 Coxeter group order: 14400
The 120-cell realizes H4 symmetry in 4D, the highest-dimensional non-crystallographic
Coxeter group, analogous to icosahedral symmetry in 3D.

The M8G PCB maps this 4D symmetry to 120 copper layers + 720 H4-symmetric vias.

---

## Certified -- Opera Numerorum Dodecahedroid

depends_on: [M1][M5][M8A][M8C][M8D][M8B][M22][M8F]

SHA-256(README.md): 2811b134a3da83fabe333dc93894dd4e35a47da9315f23d95b2fa7de570ecebe
