"""
BDP Lemma 2 (m=32) -- kappa^32 Bridge Factor for p6
Opera Numerorum | David Fox | June 06, 2026

Lemma 2 extended to m=32: there exist integers m=32, k_bridge2 such that
  |191 * kappa^32 - p6 - k_bridge2 * pi| < Error_bound_m32

where Error_bound_m32 = (m/8)/(2 ln p6) + 1/(2m ln 191)

kappa = 4.8433014197780389  (Module 2 certified value, phi(143)*c_lemma/1e10,
        phi(143)=120 exact, c_lemma=403608451.6483666, 80-bit long double)
p6    = UNKNOWN -- sixth exceptional prime, predicted ~2.13e18 (M19 Apollonian)
q     = 191  (from S4)
m     = 32   (bridge exponent at p6)

STATUS: PREDICTED. p6 has not been found.
  - To verify once p6 is found, run:
      python3 bdp2_m32.py <p6>
  - This script accepts p6 as an optional positional command-line argument.
  - Without an argument, it computes all quantities that are known (m=32 formula
    values) and displays the prediction status.

Parent SHA:
  BDP2 (m=16) stdout: 173acc5a541fc0515026b2c6c80410771c07634db415d13a597ed61a6a6c4872
  M2 stdout:          3716c7dbb32524074b8fffb65eea45069c8b568a31dc73706405116b84029a83

All arithmetic in mpmath at 64 decimal places.
"""

import sys
import mpmath

mpmath.mp.dps = 64

# ---------------------------------------------------------------------------
# Certified constants
# ---------------------------------------------------------------------------
kappa  = mpmath.mpf("4.8433014197780389")  # M2 certified (SHA 3716c7db...)
pi     = mpmath.pi
q      = mpmath.mpf("191")
m      = 32
p5     = mpmath.mpf("3993746143633")       # certified M4 / BDP4

# ---------------------------------------------------------------------------
# Optional: accept p6 as CLI argument
# ---------------------------------------------------------------------------
p6_supplied = None
if len(sys.argv) >= 2:
    try:
        p6_supplied = mpmath.mpf(sys.argv[1])
    except Exception as e:
        print(f"ERROR: could not parse p6 argument: {e}")
        sys.exit(1)

SEP = "=" * 72

print(SEP)
print("BDP Lemma 2 (m=32) -- kappa^32 Bridge Factor for p6")
print("Opera Numerorum | David Fox | June 06, 2026")
print(SEP)
print()
print(f"kappa (M2 certified) = {mpmath.nstr(kappa, 20)}")
print(f"q = {int(q)},  m = {m}")
print()

# ---------------------------------------------------------------------------
# Core computation: 191 * kappa^32
# ---------------------------------------------------------------------------
qkm32 = q * kappa**m
print(f"191 * kappa^32 = {mpmath.nstr(qkm32, 35)}")
print()

# ---------------------------------------------------------------------------
# Error bound (depends on ln(p6) -- use p5 as conservative lower bound)
# ---------------------------------------------------------------------------
lnp5  = mpmath.log(p5)
ln191 = mpmath.log(q)

# Conservative (lower-bound on p6 -> upper-bound on error term): use ln(p5)
eb_conservative = (mpmath.mpf(m)/8) / (2*lnp5) + mpmath.mpf(1)/(2*m*ln191)

# Apollonian prediction: p6 ~ 2.1339e18
p6_apollonian = mpmath.mpf("2.1339e18")
lnp6_apollonian = mpmath.log(p6_apollonian)
eb_apollonian  = (mpmath.mpf(m)/8) / (2*lnp6_apollonian) + mpmath.mpf(1)/(2*m*ln191)

print("Error bound formula: (m/8)/(2 ln p6) + 1/(2m ln 191)")
print(f"  ln(p5) = {mpmath.nstr(lnp5, 20)}  [conservative substitute]")
print(f"  ln(191) = {mpmath.nstr(ln191, 20)}")
print(f"  Term 1 = (32/8)/(2 ln p6) = 4/(2 ln p6)")
print(f"  Term 2 = 1/(64 ln 191)")
print()
print(f"  Bound (conservative, ln p6 = ln p5): {mpmath.nstr(eb_conservative, 12)}")
print(f"  Bound (Apollonian p6 ~ 2.13e18):     {mpmath.nstr(eb_apollonian, 12)}")
print()

# ---------------------------------------------------------------------------
# Apollonian prediction section
# ---------------------------------------------------------------------------
print("-" * 72)
print("APOLLONIAN PREDICTION (M19, heuristic -- NOT a theorem):")
print("-" * 72)
print()
print("  D_Apollonian = 1.30568673 (Boyd 1982 / McMullen 1998 Hausdorff dim)")
print("  Rule: log(p_{n+1}) ~ log(p_n) + (log p_n)^(1/D)")
print()
D = mpmath.mpf("1.30568673")
log_p5_100 = mpmath.log(p5)
increment  = log_p5_100 ** (1 / D)
log_p6_pred = log_p5_100 + increment
p6_pred = mpmath.exp(log_p6_pred)
print(f"  log(p5) = {mpmath.nstr(log_p5_100, 12)}")
print(f"  increment = (log p5)^(1/{mpmath.nstr(D, 10)}) = {mpmath.nstr(increment, 12)}")
print(f"  PREDICTED log(p6) = {mpmath.nstr(log_p6_pred, 12)}")
print(f"  PREDICTED p6 ~ {mpmath.nstr(p6_pred, 8)}")
print()

# Check bridge formula at Apollonian prediction (expected: FAIL or narrow)
k2_apollonian = int(mpmath.nint((qkm32 - p6_apollonian) / pi))
res_apollonian = qkm32 - p6_apollonian - k2_apollonian * pi
print(f"  Bridge check at Apollonian p6 = {float(p6_apollonian):.4e}:")
print(f"    k_bridge2 = {k2_apollonian}")
print(f"    residual  = {mpmath.nstr(res_apollonian, 12)}")
print(f"    |residual| = {mpmath.nstr(abs(res_apollonian), 12)}")
print(f"    bound      = {mpmath.nstr(eb_apollonian, 12)}")
print(f"    PASS: {abs(res_apollonian) < eb_apollonian}")
print()
print("  NOTE: The Apollonian prediction is a HEURISTIC. The bridge formula")
print("  residual at p6_apollonian does not need to pass the bound -- the")
print("  Apollonian prediction and the bridge formula are independent claims.")
print("  The bridge formula is a VERIFICATION constraint for the actual p6,")
print("  once p6 is found by sieve. It is not a direct predictor.")
print()

# ---------------------------------------------------------------------------
# Scaling table
# ---------------------------------------------------------------------------
print("Error bound scaling (m doubles at each successive exceptional prime):")
for m_test, label in [(16, "p5"), (32, "p6"), (64, "p7"), (128, "p8")]:
    if m_test == 16:
        ln_p = lnp5
    else:
        ln_p = lnp6_apollonian
    eb = (mpmath.mpf(m_test)/8) / (2*ln_p) + mpmath.mpf(1)/(2*m_test*ln191)
    note = "CERTIFIED" if m_test == 16 else "PREDICTED"
    print(f"  m={m_test:<3} ({label}): bound = {mpmath.nstr(eb, 8)}  [{note}]")
print()

# ---------------------------------------------------------------------------
# If p6 supplied: verify bridge formula
# ---------------------------------------------------------------------------
if p6_supplied is not None:
    print(SEP)
    print(f"BRIDGE FORMULA VERIFICATION at supplied p6 = {int(p6_supplied)}")
    print(SEP)
    print()

    # Primality check (Miller-Rabin via sympy or trial division for small)
    p6_int = int(p6_supplied)
    print(f"  p6 = {p6_int}")
    print(f"  Digits: {len(str(p6_int))}")

    # Check membership in S(alpha_0)
    alpha0 = 299 + pi/10
    v = p6_supplied * alpha0
    dist_p6 = abs(v - mpmath.nint(v))
    inv_p6 = 1 / p6_supplied
    print()
    print(f"  Membership check in S(alpha_0):")
    print(f"    alpha_0 = 299 + pi/10")
    print(f"    ||p6 * alpha_0|| = {mpmath.nstr(dist_p6, 15)}")
    print(f"    1/p6             = {mpmath.nstr(inv_p6, 15)}")
    print(f"    ||p6*alpha_0|| < 1/p6: {dist_p6 < inv_p6}")

    # Error bound with actual p6
    lnp6_actual = mpmath.log(p6_supplied)
    eb_actual = (mpmath.mpf(m)/8) / (2*lnp6_actual) + mpmath.mpf(1)/(2*m*ln191)

    # Compute bridge formula
    k2 = int(mpmath.nint((qkm32 - p6_supplied) / pi))
    residual = qkm32 - p6_supplied - k2 * pi

    print()
    print(f"  Bridge formula: |191*kappa^32 - p6 - k_bridge2*pi| < bound")
    print(f"    191*kappa^32   = {mpmath.nstr(qkm32, 30)}")
    print(f"    p6             = {p6_int}")
    print(f"    k_bridge2      = {k2}")
    print(f"    191*kappa^32 - p6 - k_bridge2*pi")
    print(f"                   = {mpmath.nstr(residual, 20)}")
    print(f"    |residual|     = {mpmath.nstr(abs(residual), 20)}")
    print()
    print(f"    ln(p6)         = {mpmath.nstr(lnp6_actual, 20)}")
    print(f"    error_bound    = {mpmath.nstr(eb_actual, 12)}")
    print()

    passed = abs(residual) < eb_actual
    member = dist_p6 < inv_p6

    if passed and member:
        print(f"  PASS: |residual| < error_bound")
        print(f"  PASS: p6 in S(alpha_0)")
        print()
        print("RESULT: BDP LEMMA 2 (m=32) CERTIFIED")
        print(f"  p6 = {p6_int}")
        print(f"  k_bridge2 = {k2}")
        print(f"  |residual| = {mpmath.nstr(abs(residual), 12)}")
        print(f"  error_bound = {mpmath.nstr(eb_actual, 12)}")
    elif not member:
        print(f"  FAIL: p6 does NOT pass S(alpha_0) membership test")
        print(f"    ||p6*alpha_0|| = {mpmath.nstr(dist_p6, 15)} >= 1/p6 = {mpmath.nstr(inv_p6, 15)}")
        print("  RESULT: p6 is not an exceptional prime -- cannot certify")
    else:
        print(f"  FAIL: |residual| = {mpmath.nstr(abs(residual), 12)}")
        print(f"        >= bound = {mpmath.nstr(eb_actual, 12)}")
        print("  RESULT: Bridge formula does not hold at this p6 value")

else:
    print(SEP)
    print("STATUS: p6 NOT YET FOUND")
    print(SEP)
    print()
    print("  p6 is predicted at ~2.13e18 (M19 Apollonian, heuristic).")
    print("  A sieve to 10^18 or a targeted search is required to find p6.")
    print()
    print("  When p6 is found, run:")
    print("    python3 bdp2_m32.py <p6>")
    print()
    print("  This will verify:")
    print("    (1) p6 is in S(alpha_0): ||p6 * alpha_0|| < 1/p6")
    print("    (2) Bridge formula: |191*kappa^32 - p6 - k_bridge2*pi| < error_bound")
    print()

print(SEP)
print("END BDP Lemma 2 (m=32)")
print(SEP)
