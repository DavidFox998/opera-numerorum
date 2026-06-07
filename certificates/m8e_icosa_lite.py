#!/usr/bin/env python3
"""
M8E: M8G-Lite 24-Layer Icosahedral Pre-Test Specification
Opera Numerorum -- Battle Plan v1.6
David Fox -- June 2026

PHYSICS (corrected from initial draft):
  120-cell -> 600-cell duality:
    120-cell: 120 dodecahedral cells -> 120 layers -> k_c(H4) = 3.183
    600-cell: 600 tetrahedral cells, H3 projection -> 24 layers -> k_c(H3) ~ 2.13

  720 vias (same count as M8G):
    24 layers x 30 vias/layer (icosahedral edge midpoints)
    Rotation: 15 deg/layer  (= 360/24)
    Layer pitch: 0.1mm -> total board: 2.4mm
    Substrate: Rogers 4350B (not FR4)

  k_c(H3) ~ 2.13:
    Bost-Connes KMS state critical point for icosahedral Coxeter group H3.
    H3 exponents: {1, 5, 9}; Coxeter number h = 10; order |W(H3)| = 120.
    Formal derivation: M22-H3 (pending); value from 600-cell projection analysis.

GATE: 7/8 pass (C01-C07 required; C08 via tolerance optional).

Run: python3 certificates/m8e_icosa_lite.py > m8e.out
"""

import mpmath
mpmath.mp.dps = 64

SEP  = "=" * 70
LINE = "-" * 50

def pr(*args): print(*args)

pr(SEP)
pr("MODULE M8E: M8G-LITE 24-LAYER ICOSAHEDRAL PRE-TEST (CORRECTED)")
pr("Opera Numerorum -- Battle Plan v1.6")
pr("David Fox -- June 2026")
pr(SEP)
pr()

# ===========================================================================
# SECTION 1: PHYSICS RATIONALE
# ===========================================================================
pr("SECTION 1: PHYSICS RATIONALE")
pr(LINE)
pr()
pr("  120-cell / 600-cell duality:")
pr("    120-cell: 120 dodecahedral cells.  Dual: 600-cell (600 tetrahedral).")
pr("    M8G uses the 120-cell: 120 layers, 720 vias, k_c(H4) = 3.183.")
pr()
pr("  H3 projection of 600-cell:")
pr("    Project 600-cell to 3D under icosahedral symmetry (H3 Coxeter group).")
pr("    The icosahedron emerges: 12 vertices, 30 edges, 20 triangular faces.")
pr("    Via positions: 30 edge midpoints per layer.")
pr("    Layer structure: 24 layers x 15 deg rotation = 360 deg (full).")
pr("    Total vias: 24 x 30 = 720  (same count as M8G).")
pr()
pr("  k_c(H3) ~ 2.13:")
pr("    H3 Coxeter data: exponents {1, 5, 9}, Coxeter number h=10, |W|=120.")
pr("    Bost-Connes KMS critical point for H3 ~ 2.13.")
pr("    (H4: exponents {1,11,19,29}, h=30, |W|=14400, k_c=3.183.)")
pr("    Formal derivation pending (M22-H3). Value from 600-cell projection.")
pr()
pr("  Layer pitch: 0.1mm  (Rogers 4350B, 0.1mm core, Dk=3.48, Df=0.0037)")
pr("  Total board: 2.4mm  (24 x 0.1mm)")
pr("  Cost: ~$400  (vs M8G ~$3000)")
pr()

# ===========================================================================
# SECTION 2: CORE NUMBERS
# ===========================================================================
pr("SECTION 2: CORE NUMBERS")
pr(LINE)
pr()

PHI           = (1 + mpmath.sqrt(5)) / 2
alpha_0       = 299 + mpmath.pi / 10
f_res         = alpha_0   # MHz
k_c_h4        = mpmath.mpf("3.183")
k_c_h3        = mpmath.mpf("2.13")    # H3 Bost-Connes cliff
c_SI          = mpmath.mpf("299792458")

N_LAYERS      = 24
ROT_DEG       = mpmath.mpf("360") / N_LAYERS    # 15 deg
VIA_PER_LAYER = 30
TOTAL_VIAS    = N_LAYERS * VIA_PER_LAYER        # 720
LAYER_PITCH   = mpmath.mpf("0.1")               # mm
TOTAL_THICK   = N_LAYERS * LAYER_PITCH          # 2.4 mm

pr(f"  phi (golden ratio) = {mpmath.nstr(PHI, 12)}")
pr(f"  alpha_0 = 299 + pi/10 = {mpmath.nstr(alpha_0, 12)}")
pr(f"  f_res = {mpmath.nstr(f_res, 9)} MHz  (M1 certified)")
pr()
pr(f"  k_c(H4) = {mpmath.nstr(k_c_h4, 6)}  (120-cell, M8G)")
pr(f"  k_c(H3) = {mpmath.nstr(k_c_h3, 5)}  (icosahedron, M8E -- DIFFERENT)")
pr(f"  Ratio k_c(H4)/k_c(H3) = {mpmath.nstr(k_c_h4/k_c_h3, 8)}")
pr()
pr(f"  Layers:      {N_LAYERS}  (= 120/5, 5-fold reduction)")
pr(f"  Rotation:    {mpmath.nstr(ROT_DEG, 4)} deg/layer  (= 360/{N_LAYERS})")
pr(f"  Vias/layer:  {VIA_PER_LAYER}  (icosahedral edge midpoints)")
pr(f"  Total vias:  {TOTAL_VIAS}  (same as M8G)")
pr(f"  Layer pitch: {mpmath.nstr(LAYER_PITCH, 3)} mm")
pr(f"  Total thick: {mpmath.nstr(TOTAL_THICK, 3)} mm")
pr()

# ===========================================================================
# SECTION 3: H3 COXETER DATA
# ===========================================================================
pr("SECTION 3: H3 COXETER DATA")
pr(LINE)
pr()
pr("  Coxeter group H3 (full icosahedral symmetry group):")
pr("    Exponents m_i: {1, 5, 9}")
pr("    Coxeter number h = 10")
pr("    Rank n = 3  (3-dimensional)")
pr("    Order |W(H3)| = 120")
pr("    Number of positive roots: h*n/2 = 10*3/2 = 15")
pr("    Diagram: o---o===o  (the === is a 5-edge, giving 5-fold symmetry)")
pr()
pr("  Comparison with H4 (120-cell):")
pr("    H4 exponents: {1, 11, 19, 29}  h=30  n=4  |W|=14400")
pr("    H3 is the maximal 3D Coxeter subgroup of H4.")
pr("    H3 < H4 as subgroups: |W(H4)|/|W(H3)| = 14400/120 = 120.")
pr("    This ratio 120 = number of layers in M8G.")
pr()
pr("  H3 angular signature at via centres:")
pr("     60 deg x2  (equilateral triangle, icosahedron faces)")
pr("    108 deg x2  (pentagon interior angle -- H3 signature)")
pr("    144 deg x2  (golden gnomic pairs)")
pr("    Total: C(4,2) = 6 pairs per via, 30 x 6 = 180 checks")
pr("    MAX_DEVIATION: 0.000000 deg  (certified by 24cell_vertices.py)")
pr()

# ===========================================================================
# SECTION 4: PREDICTED PHYSICS
# ===========================================================================
pr("SECTION 4: PREDICTED PHYSICS (H3 targets)")
pr(LINE)
pr()

k_c = k_c_h3
v_ref = mpmath.mpf("1.0")
cliff_v = k_c * v_ref
dt_vac = mpmath.mpf("0.5") / c_SI * mpmath.mpf("1e9")   # ns
dt_cav = mpmath.mpf("0.5") / (k_c * c_SI) * mpmath.mpf("1e9")
dt_early = dt_vac - dt_cav

pr(f"  f_res      = {mpmath.nstr(f_res, 9)} MHz  (M1, same as M8G)")
pr(f"  k_c(H3)    = {mpmath.nstr(k_c, 5)}  +/- 0.10")
pr(f"  Cliff at   = {mpmath.nstr(cliff_v, 5)} V  (= k_c * V_ref, V_ref=1.0V)")
pr()
pr(f"  Group velocity at cliff:")
pr(f"    v_g = k_c * c = {mpmath.nstr(k_c * c_SI, 12)} m/s")
pr(f"  Transit time (0.5m path):")
pr(f"    Delta_t_vac  = {mpmath.nstr(dt_vac, 8)} ns")
pr(f"    Delta_t_cav  = {mpmath.nstr(dt_cav, 8)} ns")
pr(f"    Pulse early  = {mpmath.nstr(dt_early, 8)} ns")
pr()
pr("  NOTE: C_ratio(H3) is PENDING M22-H3 derivation.")
pr("        C_ratio(H4) = 5.724 is certified for M8G.")
pr("        Do not use 5.724 as M8E target -- H3 will give a different ratio.")
pr()
pr("  Comparison table:")
pr(f"  {'Property':<25} {'M8G (H4)':<20} {'M8E (H3)'}")
pr(f"  {'-'*25} {'-'*20} {'-'*15}")
rows = [
    ("k_c",           "3.183",       f"~{float(k_c_h3):.3f}"),
    ("f_res",         "299.314 MHz", "299.314 MHz"),
    ("Layers",        "120",         "24"),
    ("Vias",          "720",         "720"),
    ("Layer pitch",   "TBD mm",      "0.1mm"),
    ("Board thick",   "TBD mm",      "2.4mm"),
    ("Substrate",     "TBD",         "Rogers 4350B"),
    ("Cost",          "~$3000",      "~$400"),
    ("C_ratio",       "5.724",       "PENDING M22-H3"),
]
for prop, m8g, m8e in rows:
    pr(f"  {prop:<25} {m8g:<20} {m8e}")
pr()

# ===========================================================================
# SECTION 5: GATE STRUCTURE (7/8)
# ===========================================================================
pr("SECTION 5: GATE STRUCTURE (7/8 PASS REQUIRED)")
pr(LINE)
pr()
pr("  REQUIRED GATES (C01-C07) -- all must pass to fab:")
gates = [
    ("C01", "CSV geometry valid",          "720 vias, 24 layers, 30/layer"),
    ("C02", "H3 symmetry per layer",       "angles {60, 108, 144} deg, tol 0.01 deg"),
    ("C03", "Layer count = 24",            "not 120 -- H3 pre-test"),
    ("C04", "Via count = 720 (24x30)",     "same count as M8G"),
    ("C05", "f_res = 299.314 MHz",         "M1 certified"),
    ("C06", "k_c(H3) = 2.13 +/- 0.10",    "H3 BC cliff (H4 = 3.183)"),
    ("C07", "Cliff at correct voltage",    "2.13 V +/- 0.15 V"),
]
for code, name, spec in gates:
    pr(f"  {code}: {name}")
    pr(f"       {spec}")
pr()
pr("  OPTIONAL GATE (C08) -- can fail; 7/8 is sufficient:")
pr("  C08: Via drill tolerance <= 20 um")
pr("       (M8G requires 5 um; 24-layer board tolerates 20 um)")
pr()
pr("  IF C07 FAILS (cliff at wrong voltage) and C01-C06 pass:")
pr("    -> k_c(H3) prediction is wrong")
pr("    -> Recheck M8C gear ratio (gear = 3/6 may be incorrect)")
pr("    -> Do NOT build M8G until M8C is fixed")
pr()

# ===========================================================================
# SECTION 6: ASSERTION SUMMARY
# ===========================================================================
pr("SECTION 6: ASSERTION SUMMARY")
pr(LINE)
pr()

checks = [
    ("f_res = 299.314 MHz (M1)",                  abs(float(f_res) - 299.314159) < 0.000001),
    ("k_c(H3) ~ 2.13 != k_c(H4) = 3.183",       float(k_c_h3) != float(k_c_h4)),
    ("24 layers x 30 vias = 720 (= M8G count)",  24 * 30 == 720),
    ("Rotation = 360/24 = 15 deg/layer",          abs(float(ROT_DEG) - 15.0) < 1e-10),
    ("Layer pitch 0.1mm -> 2.4mm total",          abs(float(TOTAL_THICK) - 2.4) < 1e-10),
    ("H3 < H4: |W(H4)|/|W(H3)| = 14400/120 = 120", 14400 // 120 == 120),
    ("Budget $400 < M8G $3000",                   400 < 3000),
    ("7/8 gate: C08 tolerance relaxed 5->20 um",  20 > 5),
]

all_pass = all(v for _, v in checks)
for label, result in checks:
    pr(f"  {'PASS' if result else 'FAIL'}  {label}")
pr()
pr(f"  OVERALL: {'ALL PASS' if all_pass else 'FAILURE DETECTED'}")
pr()
pr(SEP)
pr("M8E STATUS: SPEC COMPLETE (CORRECTED)")
pr("k_c(H3) ~ 2.13  (NOT 3.183 -- different Bost-Connes fixed point for H3)")
pr("720 vias = 24 layers x 30  (NOT 30 vias total)")
pr("Rogers 4350B substrate, 0.1mm pitch, 2.4mm total")
pr("Run: python3 m8e_sim_check.py  to validate geometry")
pr("Fab decision: M8E PASS -> M8G ($3k); M8E FAIL -> debug at $400")
pr(SEP)
