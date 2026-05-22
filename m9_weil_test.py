"""
m9_weil_test.py -- Weil Explicit Formula test for GRH(J_0(143))
Asks: Does M8 + Deligne data imply GRH via Weil explicit formula?

AUDIT NOTES (versus original supervisor draft):
  Bug 1: mpmath quad() returns a single mpf, not a tuple.
          Original "num, _ = quad(...)" crashes with TypeError.
          Fixed: num = quad(..., error=False)

  Bug 2: a_p_data used incorrect trace values.
          Original formula mixes old/new form a_p scalars with wrong multipliers.
          The correct trace of T_p on H_1(J_0(143)) must sum a_p^sigma
          over ALL Galois embeddings of all four newform orbits.
          Fixed values (computed from M8 certified data, SHA e2d70821):
            p=  2:  script=-8,   correct=-1
            p=  3:  script=-14,  correct=0
            p= 19:  script=-12,  correct=0
            p=191:  script=+18,  correct=+28

MATHEMATICAL NOTE:
  The Weil explicit formula (Weil 1952) for an L-function L(s) states:
    sum_rho h(rho) = h(1) + h(0) - sum_p sum_k (log p / p^(k/2)) * (g(k log p) + ...)
                    + archimedean terms
  where the sum is over ALL primes p, and h is a test function.

  A test function F supported only on {log 2, log 3, log 19, log 191}
  captures only four terms of the full prime sum.  This is NOT a lower
  bound on the full sum; the omitted primes contribute with UNKNOWN sign.
  Therefore, even a correct calculation of the RHS from S_4 alone cannot
  establish GRH.  This is the fundamental gap in the M9.3 approach.

  For a valid Weil-type GRH test, one would need either:
    (a) Sum over all primes up to a sufficient height (Odlyzko-Schonhage), or
    (b) A theoretical argument that the omitted primes cannot flip the sign.
  Neither is provided by M9.3 as currently stated.

  This script runs the calculation honestly with the correct data and
  reports the result, along with the above caveat.
"""

from mpmath import mp, log, exp, sqrt, quad, cosh, mpf, nstr
mp.dps = 50

S4 = [2, 3, 19, 191]
g = 13
deltas = {p: p * log(p) / (p - 1) for p in S4}
C_S4 = sum(deltas.values())

# ---------------------------------------------------------------
# Correct trace of T_p on H_1(J_0(143), C)
# = sum over all Galois embeddings sigma of a_p^sigma
# Computed from M8 certified eigenvalue data (j0_143_hankel.py, SHA e2d70821)
#   p=  2:  11.2.a.a(x2)=-4  +  143.2.a.a=0   +  ab_trace=+3  +  ac_trace=0   = -1
#   p=  3:  11.2.a.a(x2)=-2  +  143.2.a.a=-1  +  ab_trace=0   +  ac_trace=+3  =  0
#   p= 19:  11.2.a.a(x2)=0   +  143.2.a.a=+2  +  ab_trace=+8  +  ac_trace=-10 =  0
#   p=191:  11.2.a.a(x2)=+34 +  143.2.a.a=-15 +  ab_trace=+12 +  ac_trace=-3  = +28
# ---------------------------------------------------------------
tr_Tp = {2: -1, 3: 0, 19: 0, 191: 28}

# ---------------------------------------------------------------
# Test function: phi(t) = exp(-t^2/2), F(t) = sum_{p in S4} delta_p * phi(t - log p)
# ---------------------------------------------------------------
def phi(t):
    return exp(-t * t / 2)

def F(t):
    return sum(deltas[p] * phi(t - log(p)) for p in S4)

# ---------------------------------------------------------------
# kappa: supervisor's formula integral F(t)*cosh(t/2) / integral F(t)
# (Note: this is not a standard Weil explicit formula coefficient.
#  Its mathematical meaning in this context is unclear.)
# ---------------------------------------------------------------
num = quad(lambda t: F(t) * cosh(t / 2), [0, 20])
den = quad(lambda t: F(t), [0, 20])
kappa = num / den

# ---------------------------------------------------------------
# Defect term: sum_{p in S4} delta_p * Tr(T_p) / sqrt(p)
# (using the CORRECT trace values)
# ---------------------------------------------------------------
defect = sum(deltas[p] * tr_Tp[p] / sqrt(p) for p in S4)
logN = log(143)
weil_rhs_bound = logN - g * kappa + defect

# ---------------------------------------------------------------
# Original (incorrect) defect for comparison
# ---------------------------------------------------------------
tr_wrong = {2: -8, 3: -14, 19: -12, 191: 18}
defect_wrong = sum(deltas[p] * tr_wrong[p] / sqrt(p) for p in S4)
weil_rhs_wrong = logN - g * kappa + defect_wrong

print("=== M9.3 Weil Explicit Formula Test (corrected) ===")
print()
print(f"C(S_4)     = {float(C_S4):.6f}   (certified M5)")
print(f"2*sqrt(g)  = {float(2*sqrt(g)):.6f}")
print(f"kappa      = {float(kappa):.6f}  (integral F*cosh(t/2) / integral F)")
print(f"2*sqrt(g)*kappa = {float(2*sqrt(g)*kappa):.6f}")
print()
print("Trace of T_p on H_1(J_0(143)) -- correct vs script:")
for p in S4:
    print(f"  p={p:3d}: correct={tr_Tp[p]:+4d}   script_draft={tr_wrong[p]:+4d}")
print()
print(f"Defect Σ δ_p Tr(T_p)/sqrt(p) [CORRECT] = {float(defect):+.6f}")
print(f"Defect Σ δ_p Tr(T_p)/sqrt(p) [SCRIPT]  = {float(defect_wrong):+.6f}")
print()
print(f"log(N=143)       = {float(logN):.6f}")
print()
print(f"Weil RHS [CORRECT] = {float(weil_rhs_bound):+.6f}")
print(f"Weil RHS [SCRIPT]  = {float(weil_rhs_wrong):+.6f}")
print()
print("-" * 55)
if weil_rhs_bound < 0:
    print("RESULT (correct data): PASS  (RHS < 0)")
else:
    print("RESULT (correct data): FAIL  (RHS >= 0)")

if weil_rhs_wrong < 0:
    print("RESULT (script data):  PASS  (RHS < 0)  [but data was wrong]")
else:
    print("RESULT (script data):  FAIL  (RHS >= 0) [but data was wrong]")
print("-" * 55)
print()
print("MATHEMATICAL INTERPRETATION:")
print()
print("  Even if RHS < 0 with S_4 data, this does NOT prove GRH.")
print("  The Weil explicit formula sums over ALL primes p.")
print("  Using only S_4 = {2,3,19,191} omits primes 5,7,11,13,17,...")
print("  Those omitted terms have unknown sign and could flip RHS > 0.")
print()
print("  A complete explicit-formula GRH test requires either:")
print("    (a) Odlyzko-Schonhage sum to sufficient height X, or")
print("    (b) A theoretical bound on the contribution from p not in S_4.")
print()
print("  M9.3 as stated provides neither. The S_4-only calculation")
print("  is necessary but not sufficient evidence for GRH.")

import hashlib, sys
sha = hashlib.sha256(open(sys.argv[0], 'rb').read()).hexdigest()
print(f"\nSHA-256(m9_weil_test.py) = {sha}")
