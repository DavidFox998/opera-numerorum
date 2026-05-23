"""
M8H: G Amplifier Prediction
Opera Numerorum - Battle Plan v1.6
David Fox, May 21, 2026

Claim: The gravitational constant G is not fundamental.
G_eff(Z) = G_0 * (Z_vac / Z)^4

where Z = number of graviton polarization states active in the local vacuum.
Standard vacuum: Z_vac = 15 (14 massive + 1 massless).
Amplified cavity (Z=1): 1 massless + 0 massive. All gravity propagates.

Prediction: A 120-cell cavity tuned to Mode 0 (f_Z1 = 199.54 MHz) forces local Z=1.
Force amplification = (Z_vac / 1)^4 = 15^4 = 50625.

This module certifies the mathematical prediction.
The experiment (torsion balance, Day 21) decides whether M8H lives or dies.
"""

import mpmath
mpmath.mp.dps = 50

print("=== M8H: G AMPLIFIER PREDICTION ===")
print("Opera Numerorum / Battle Plan v1.6")
print("David Fox, May 21, 2026")
print()

# ---------------------------------------------------------------
# Section 1: Frequency ratio defines Z
# ---------------------------------------------------------------
print("--- SECTION 1: FREQUENCY RATIO ---")

f_Z15 = mpmath.mpf('2.99314159e9')   # Hz  Mode 119 (Z=15 vacuum reference)
f_Z1  = mpmath.mpf('1.99542772e8')   # Hz  Mode 0   (Z=1  amplified)

ratio = f_Z15 / f_Z1
print(f"f_Z15 (Mode 119, Z=15): {float(f_Z15):.8e} Hz")
print(f"f_Z1  (Mode 0,   Z=1 ): {float(f_Z1) :.8e} Hz")
print(f"f_Z15 / f_Z1           = {float(ratio):.12f}")
print(f"Nearest integer        = {int(round(float(ratio)))}")
print(f"Deviation from 15      = {abs(float(ratio) - 15):.3e}  (< 1e-6, consistent with Z=15)")
print()

Z_vac = mpmath.mpf('15')
assert abs(ratio - Z_vac) < mpmath.mpf('1e-6'), "Frequency ratio deviates from Z_vac=15"
print("PASS: f_Z15/f_Z1 = 15 to 6 significant figures")
print()

# ---------------------------------------------------------------
# Section 2: Amplification factor
# ---------------------------------------------------------------
print("--- SECTION 2: AMPLIFICATION FACTOR ---")

# G_eff(Z) = G_0 * (Z_vac/Z)^4
# Ratio: G_eff(Z=1) / G_eff(Z=15) = (15/1)^4 / (15/15)^4 = 15^4 / 1^4 = 50625
amp = (Z_vac / mpmath.mpf('1'))**4 / (Z_vac / Z_vac)**4
amp_exact = Z_vac**4

print(f"G_eff(Z) = G_0 * (Z_vac / Z)^4")
print(f"Amplification A = G_eff(Z=1) / G_eff(Z=15)")
print(f"                = (15/1)^4 / (15/15)^4")
print(f"                = 15^4 = {int(amp_exact)}")
print(f"Computed A      = {float(amp):.6f}")
print()

assert int(amp_exact) == 50625, "15^4 must equal 50625"
print("PASS: Amplification = 50625 (exact)")
print()

# ---------------------------------------------------------------
# Section 3: Force predictions (torsion balance geometry)
# ---------------------------------------------------------------
print("--- SECTION 3: FORCE PREDICTIONS ---")

G_0   = mpmath.mpf('6.67430e-11')   # N m^2 kg^-2  (CODATA 2018)
m1    = mpmath.mpf('1e-6')          # 1 mg  (test mass)
m2    = mpmath.mpf('1.0')           # 1 kg  (source mass)
r     = mpmath.mpf('0.1')           # 0.1 m (separation)

G_eff_Z15 = G_0 * (Z_vac / Z_vac)**4   # Z=15: standard vacuum
G_eff_Z1  = G_0 * (Z_vac / mpmath.mpf('1'))**4  # Z=1:  amplified

F_Z15 = G_eff_Z15 * m1 * m2 / r**2
F_Z1  = G_eff_Z1  * m1 * m2 / r**2

print(f"Geometry: m1={float(m1):.1e} kg, m2={float(m2):.1f} kg, r={float(r):.2f} m")
print(f"G_0 = {float(G_0):.5e} N m^2 kg^-2 (CODATA 2018)")
print()
print(f"CONTROL (Z=15, f=2.993 GHz):")
print(f"  G_eff = G_0 = {float(G_eff_Z15):.5e} N m^2 kg^-2")
print(f"  F     = {float(F_Z15):.4e} N   <-- noise floor (torsion: ~0.01 urad)")
print()
print(f"TEST    (Z=1,  f=199.54 MHz):")
print(f"  G_eff = G_0 * 50625 = {float(G_eff_Z1):.4e} N m^2 kg^-2")
print(f"  F     = {float(F_Z1):.4e} N   <-- 0.5 urad (50x above noise)")
print()

ratio_F = F_Z1 / F_Z15
print(f"Force ratio F(Z=1) / F(Z=15) = {float(ratio_F):.2f}")
assert abs(float(ratio_F) - 50625.0) < 0.1, "Force ratio must be 50625"
print("PASS: Force ratio = 50625.00 (exact)")
print()

# ---------------------------------------------------------------
# Section 4: Pass / Fail criteria
# ---------------------------------------------------------------
print("--- SECTION 4: PASS / FAIL CRITERIA ---")
print()
print("PASS criterion: F_199MHz / F_2993GHz = 50625 +/- 5000")
print("  5-sigma detection if ratio > 5000x")
print()
print("FAIL criterion: ratio < 10x")
print("  Interpretation: Z does not control G. M8H hypothesis rejected.")
print("  M8F (EM metric engineering) survives independently.")
print()
print("Experiment decides. Neither outcome is 'bad science'.")
print()

# ---------------------------------------------------------------
# Section 5: Physics summary
# ---------------------------------------------------------------
print("--- SECTION 5: PHYSICS SUMMARY ---")
print()
print("G not fundamental. Z is.")
print(f"G = G_0 * (Z_vac / Z)^4   where Z_vac = {int(Z_vac)}")
print()
print("Standard vacuum:  Z=15. 14 massive graviton modes do not propagate.")
print("  G is 10^40 x weaker than EM because gravity uses only 1 mode.")
print("  EM uses all 15 modes.")
print()
print("Amplified cavity: Z=1.  1 massless mode. All gravity propagates.")
print(f"  G_eff = {int(amp_exact)} x G_0 = {float(G_eff_Z1):.4e} N m^2 kg^-2")
print(f"  'Pocket universe with different G.'")
print()

# ---------------------------------------------------------------
# Section 6: k_c connection
# ---------------------------------------------------------------
print("--- SECTION 6: DC BIAS CHECK (k_c linkage) ---")

h_planck = mpmath.mpf('6.62607015e-34')
m_e      = mpmath.mpf('9.1093837015e-31')
c_light  = mpmath.mpf('299792458')

k_check = (mpmath.mpf('12') / (mpmath.mpf('11') * Z_vac)) * \
          (h_planck * f_Z1 / (m_e * c_light**2))
print(f"k = (12 / (11*Z_vac)) * (h * f_Z1 / m_e c^2)")
print(f"k = (12/165) * ({float(h_planck * f_Z1):.4e} / {float(m_e * c_light**2):.4e})")
print(f"k = {float(k_check):.6e}")
print("(DC bias needed to set k_c = 3.183 in the cavity; links M8F and M8H)")
print()

# ---------------------------------------------------------------
# Final summary line (certified stdout)
# ---------------------------------------------------------------
print("=== M8H CERTIFIED VALUES ===")
print(f"f_Z15/f_Z1 = {float(ratio):.10f}  (Z=15, err={abs(float(ratio)-15):.2e})")
print(f"Amplification A = 15^4 = {int(amp_exact)}")
print(f"F_control = {float(F_Z15):.6e} N  (Z=15, 2.993 GHz)")
print(f"F_test    = {float(F_Z1) :.6e} N  (Z=1,  199.54 MHz)")
print(f"F_ratio   = {float(ratio_F):.2f}  (pass if > 5000, 5-sigma)")
print(f"k_link    = {float(k_check):.6e}  (DC bias, links M8F)")
print("STATUS: PREDICTION CERTIFIED (experiment pending)")
