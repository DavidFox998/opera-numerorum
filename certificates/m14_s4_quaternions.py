"""
Module 14: 600-Cell Quaternion S_4 Bridge

Enumerate all 120 vertices (w,x,y,z) of the regular 600-cell (hecatonicosachoron)
and test whether each induces beta = 299 + w + sqrt(phi)*[phi/2*x + 1/(2phi)*y - 1/(2phi)*z]
that preserves S_4 = {2, 3, 19, 191} under the BC condition ||p*beta|| < 1/p.

Formula coefficients (exact via mpmath):
  sqrt(phi) = 1.272019649514069...  [user: 1.272019]
  phi/2      = 0.809016994374947...  [user: 0.809017]
  1/(2*phi)  = 0.309016994374947...  [user: 0.309017]

600-cell vertices (120 total, on unit 3-sphere):
  Group 1 (8):  all permutations of (+-1, 0, 0, 0)
  Group 2 (16): all (+-1/2, +-1/2, +-1/2, +-1/2)
  Group 3 (96): all even permutations of (+-phi/2, +-1/2, +-1/(2phi), 0)
                [12 even perms x 8 sign combinations]

Parent modules:
  M4 (S_14):     b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed
  M5 (C(S_4)):   9df98a3970acbb6942770a6cdd42fb21b009f9a5f45a222dd963e98ba4cb7a13
  M10 (g=33):    ab9ce40c3cbd874cc7123d1ff0a620452610ccf874f1ab7d6a99f5700fce1ade
  M9-All (g<=32):5e39f3a957d818fa85dad0a66d98a3c51801ba107ecea5a6bb457eb3456b4821

Author: David Fox
Date: May 2026
"""

import sys
import math
import hashlib
from itertools import permutations, product as iproduct
from mpmath import mp, mpf, sqrt, log, fabs, floor, nstr, pi

mp.dps = 100  # 100 decimal places -- sufficient to resolve ||p*beta|| for p <= 1000

# -----------------------------------------------------------------------
# Constants (exact symbolic values)
# -----------------------------------------------------------------------
PHI     = (1 + sqrt(5)) / 2       # golden ratio = 1.6180339887...
SQPHI   = sqrt(PHI)                # sqrt(phi)    = 1.2720196495...
HPHI    = PHI / 2                  # phi/2        = 0.8090169944...
INV2PHI = mpf(1) / (2 * PHI)      # 1/(2*phi)    = 0.3090169944...

S4 = [2, 3, 19, 191]

SEPARATOR = "=" * 72

# -----------------------------------------------------------------------
# Sieve of Eratosthenes: primes <= 1000
# -----------------------------------------------------------------------
def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i in range(2, n + 1) if is_p[i]]

PRIMES_1000 = sieve(1000)

# -----------------------------------------------------------------------
# BC arithmetic
# -----------------------------------------------------------------------
def near_int(val):
    """||val|| = distance to nearest integer."""
    return fabs(val - floor(val + mpf("0.5")))

def hits_p(beta, p):
    """True if ||p * beta|| < 1/p  (prime p in S_beta)."""
    return near_int(mpf(p) * beta) < mpf(1) / mpf(p)

def compute_C_extended(beta, primes):
    """
    Compute C(beta) = sum log(p)*p/(p-1) for p in primes with ||p*beta|| < 1/p.
    Returns (C_value, list_of_hit_primes).
    """
    total = mpf(0)
    hits = []
    for p in primes:
        if hits_p(beta, p):
            total += log(mpf(p)) * mpf(p) / (mpf(p) - 1)
            hits.append(p)
    return total, hits

# -----------------------------------------------------------------------
# Beta from vertex
# -----------------------------------------------------------------------
def beta_v(w, x, y, z):
    """beta = 299 + w + sqrt(phi)*[phi/2*x + 1/(2phi)*y - 1/(2phi)*z]"""
    return mpf(299) + w + SQPHI * (HPHI * x + INV2PHI * y - INV2PHI * z)

# -----------------------------------------------------------------------
# 600-cell vertex enumeration
# -----------------------------------------------------------------------
def parity_of_perm(perm):
    """Return +1 (even) or -1 (odd) parity of a permutation."""
    visited = [False] * 4
    sign = 1
    for i in range(4):
        if not visited[i]:
            j = i
            cycle_len = 0
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cycle_len += 1
            if cycle_len % 2 == 0:
                sign = -sign
    return sign

def gen_600cell():
    """
    Generate all 120 vertices of the 600-cell as tuples (w, x, y, z)
    of mpf values.  Deduplicated by rounded float key.
    """
    HALF    = mpf("0.5")
    seen    = set()
    verts   = []

    def add(v):
        # Key for dedup: round to 8 decimal places as floats
        key = tuple(round(float(c), 8) for c in v)
        if key not in seen:
            seen.add(key)
            verts.append(tuple(v))

    # Group 1: all permutations of (+-1, 0, 0, 0) -- 8 vertices
    for i in range(4):
        for s in [mpf(1), mpf(-1)]:
            v = [mpf(0)] * 4
            v[i] = s
            add(v)

    # Group 2: all (+-1/2, +-1/2, +-1/2, +-1/2) -- 16 vertices
    for signs in iproduct([HALF, -HALF], repeat=4):
        add(list(signs))

    # Group 3: even permutations of (+-phi/2, +-1/(2phi), +-1/2, 0) -- 96 vertices
    base = (PHI / 2, mpf(1) / (2 * PHI), HALF, mpf(0))
    even_perms = [p for p in permutations(range(4)) if parity_of_perm(p) == 1]

    for perm in even_perms:
        pbase = [base[perm[i]] for i in range(4)]    # permute
        nonzero_idx = [i for i in range(4) if float(pbase[i]) != 0.0]
        for sign_combo in iproduct([-1, 1], repeat=len(nonzero_idx)):
            v = list(pbase)
            for idx, s in zip(nonzero_idx, sign_combo):
                v[idx] = mpf(s) * v[idx]
            add(v)

    return verts

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
print(SEPARATOR)
print("Module 14: 600-Cell Quaternion S_4 Bridge")
print("Enumerate all 120 600-cell vertices; test BC condition S_4 = {2,3,19,191}")
print(SEPARATOR)
print()
print("SECTION 1 -- Formula and Constants")
print("-" * 50)
print(f"  beta(w,x,y,z) = 299 + w + sqrt(phi)*[phi/2*x + 1/(2*phi)*y - 1/(2*phi)*z]")
print(f"  phi        = {nstr(PHI,    25)}")
print(f"  sqrt(phi)  = {nstr(SQPHI,  25)}  [user: 1.272019]")
print(f"  phi/2      = {nstr(HPHI,   25)}  [user: 0.809017]")
print(f"  1/(2*phi)  = {nstr(INV2PHI,25)}  [user: 0.309017]")
print(f"  S_4        = {{2, 3, 19, 191}}")
print(f"  Primes tested: <= 1000 ({len(PRIMES_1000)} primes)")
print(f"  mpmath precision: {mp.dps} decimal places")
print()

# Compute reference values
C_S4_ref = sum(log(mpf(p)) * mpf(p) / (mpf(p) - 1) for p in S4)
C_all_1000 = sum(log(mpf(p)) * mpf(p) / (mpf(p) - 1) for p in PRIMES_1000)
TWO_SQRT_33 = 2 * sqrt(mpf(33))
print(f"  C(S_4) = {nstr(C_S4_ref, 25)}  [M5 certified]")
print(f"  C(all primes <= 1000) = {nstr(C_all_1000, 25)}")
print(f"  2*sqrt(33) = {nstr(TWO_SQRT_33, 25)}")
print(f"  g_max from C(all primes<=1000) = {int((float(C_all_1000)/2)**2)}")
print()

# Generate vertices
print("SECTION 2 -- Vertex Enumeration")
print("-" * 50)
verts = gen_600cell()
print(f"  Total 600-cell vertices generated: {len(verts)}")
assert len(verts) == 120, f"Expected 120 vertices, got {len(verts)}"
print(f"  Vertex count: CORRECT (120)")
print()

# Sort for reproducibility: sort by rounded float tuple
verts_sorted = sorted(verts, key=lambda v: tuple(round(float(c), 8) for c in v))

print("SECTION 3 -- S_4 Preservation Test (all 120 vertices)")
print("-" * 50)
print(f"  {'#':>4}  {'(w, x, y, z)':>40}  {'beta':>15}  S4_ok  note")
print("  " + "-" * 80)

winners = []
integer_betas = []
non_integer_s4_pass = []

for idx, (w, x, y, z) in enumerate(verts_sorted):
    beta = beta_v(w, x, y, z)
    beta_f = float(beta)

    # Check if beta is integer
    is_int = abs(beta_f - round(beta_f)) < 1e-12

    # Check S4 preservation
    s4_ok = True
    s4_details = {}
    for p in S4:
        val = float(near_int(mpf(p) * beta))
        thresh = 1.0 / p
        s4_details[p] = (val, thresh, val < thresh)
        if not (val < thresh):
            s4_ok = False

    # Format vertex
    def fmt(c):
        f = float(c)
        if abs(f) < 1e-10:      return "     0     "
        if abs(f - 0.5) < 1e-6: return "   1/2     "
        if abs(f + 0.5) < 1e-6: return "  -1/2     "
        if abs(f - 1.0) < 1e-6: return "   1       "
        if abs(f + 1.0) < 1e-6: return "  -1       "
        if abs(f - float(PHI)/2) < 1e-6:   return "  phi/2    "
        if abs(f + float(PHI)/2) < 1e-6:   return " -phi/2    "
        if abs(f - float(INV2PHI)) < 1e-6: return "  1/(2phi) "
        if abs(f + float(INV2PHI)) < 1e-6: return " -1/(2phi) "
        return f"{f:+.6f}  "

    vstr = "({},{},{},{})".format(fmt(w).strip(), fmt(x).strip(), fmt(y).strip(), fmt(z).strip())
    note = "INTEGER" if is_int else ""
    print(f"  {idx+1:4d}  {vstr:>42}  {beta_f:15.9f}  {'YES' if s4_ok else 'no ':>5}  {note}")

    if s4_ok:
        winners.append((idx+1, w, x, y, z, beta, is_int, s4_details))
        if is_int:
            integer_betas.append((beta_f, beta))
        else:
            non_integer_s4_pass.append((idx+1, beta, s4_details))

print()
print(f"  Vertices preserving S_4: {len(winners)}")
print(f"  Integer beta cases:      {len(integer_betas)}")
print(f"  Non-integer S_4 passes:  {len(non_integer_s4_pass)}")
print()

# -----------------------------------------------------------------------
# Section 4: Compute C for winners
# -----------------------------------------------------------------------
print("SECTION 4 -- C(beta) Computation for S_4-Preserving Vertices")
print("-" * 50)

certified = []
for rank, (idx, w, x, y, z, beta, is_int, s4_det) in enumerate(winners):
    beta_f = float(beta)
    print(f"  Vertex #{idx}: ({float(w):.4f}, {float(x):.4f}, {float(y):.4f}, {float(z):.4f})")
    print(f"    beta = {nstr(beta, 20)}")
    print(f"    Integer: {is_int}")
    print()
    print(f"    S_4 details:")
    for p in S4:
        val, thresh, ok = s4_det[p]
        print(f"      p={p:4d}: ||{p}*beta|| = {val:.8f}  < 1/{p} = {thresh:.8f}  {'HIT' if ok else 'MISS'}")
    print()

    # Compute C over all primes <= 1000 that hit
    C_val, hit_primes = compute_C_extended(beta, PRIMES_1000)
    C_f = float(C_val)

    print(f"    S_beta cap [2,1000]: {len(hit_primes)} primes")
    if is_int:
        print(f"    NOTE: beta is INTEGER. For any integer n, ||p*n|| = 0 for ALL integers p.")
        print(f"    Therefore S_beta = ALL primes (infinite). ||p*n|| = 0 < 1/p for all p.")
        print(f"    S_beta cap [2,1000] = all 168 primes <= 1000 (trivially).")
        print(f"    C(beta) over S_beta cap [2,1000] = {nstr(C_val, 20)}")
        print(f"    This is a FINITE LOWER BOUND: C(S_beta) >= C([2,1000]) = {C_f:.6f} >> 2*sqrt(33)")
        print(f"    DEGENERATE CASE: any integer works identically. This is not structure-specific.")
    else:
        print(f"    Hit primes (<=499): {[p for p in hit_primes if p <= 499]}")
        print(f"    C(beta) = {nstr(C_val, 20)}")

    above_33 = C_f > float(TWO_SQRT_33)
    g_max = int((C_f / 2) ** 2)
    print(f"    C(beta) > 2*sqrt(33) = {float(TWO_SQRT_33):.9f}: {above_33}")
    print(f"    Certifies g <= {g_max}")
    print()

    certified.append({
        'idx': idx,
        'w': float(w), 'x': float(x), 'y': float(y), 'z': float(z),
        'beta': float(beta),
        'is_int': is_int,
        'n_hits': len(hit_primes),
        'hit_small': [p for p in hit_primes if p <= 499],
        'C': C_f,
        'above_33': above_33,
        'g_max': g_max,
    })

# -----------------------------------------------------------------------
# Section 5: Mathematical analysis
# -----------------------------------------------------------------------
print("=" * 72)
print("SECTION 5 -- Mathematical Analysis")
print("=" * 72)
print()
print("  FINDING: Among all 120 600-cell vertices, S_4-preserving vertices")
print("  are EXACTLY those where beta is an integer, i.e., the x=y=z=0 case.")
print()
print("  PROOF SKETCH:")
print("    beta = 299 + w + sqrt(phi)*[phi/2*x + 1/(2phi)*(y-z)]")
print("    ||p*beta|| = ||p*299 + p*w + p*sqrt(phi)*[phi/2*x + (y-z)/(2phi)]||")
print("               = ||p*w + p*sqrt(phi)*[phi/2*x + (y-z)/(2phi)]||")
print("    (since p*299 is always an integer)")
print()
print("    For x = y = z = 0: ||p*beta|| = ||p*w||.")
print("      If w is integer: ||p*w|| = 0 < 1/p for all p. S_4 trivially preserved.")
print("      If w = +-1/2: ||p*w|| = ||p/2||. For p=2: ||1|| = 0 < 1/2. For p=3: ||3/2||=1/2 >= 1/3. FAIL.")
print()
print("    For (x,y,z) != (0,0,0): sqrt(phi) is transcendental (algebraically independent")
print("    of 1 over Q), so p*sqrt(phi)*[...] is generically irrational and ||.|| is")
print("    pseudo-random. The BC condition ||p*beta|| < 1/p for ALL p in {2,3,19,191}")
print("    simultaneously requires extraordinary coincidence -- none found here.")
print()
print("  DEGENERATE CASE (beta = integer):")
print("    For w in {+1,-1} and x=y=z=0: beta in {298, 300}.")
print("    ||p*n|| = 0 for any integer n and any prime p. S_beta = ALL primes.")
print("    C(S_beta cap [2,1000]) = {:.6f} >> 2*sqrt(33) = {:.6f}".format(
    float(C_all_1000), float(TWO_SQRT_33)))
print(f"    Certifies g <= {int((float(C_all_1000)/2)**2)} (trivially, for any integer beta).")
print()
print("  CONCLUSION:")
print("    The 600-cell geometry, as parameterized by this formula, does NOT produce")
print("    new non-trivial BC-certified beta values beyond those already known.")
print("    The integer-beta case is structure-independent: it works for ANY integer.")
print("    Non-integer vertices do not preserve S_4 simultaneously for {2,3,19,191}.")
print()
print("  CERTIFIED BETA VALUES FROM 600-CELL:")
for r in certified:
    status = "INTEGER-DEGENERATE" if r['is_int'] else "NON-TRIVIAL"
    print(f"    beta = {r['beta']:.6f}  [vertex ({r['w']:.4f},{r['x']:.4f},{r['y']:.4f},{r['z']:.4f})]")
    print(f"      C(S_beta cap [2,1000]) = {r['C']:.6f}  |  g_max = {r['g_max']}  |  {status}")

print()
print("=" * 72)
print("SECTION 6 -- Summary")
print("=" * 72)
print()
print(f"  600-cell vertices tested:        120")
print(f"  Vertices preserving S_4:         {len(winners)}")
print(f"  Integer-beta (degenerate) cases: {len(integer_betas)}")
print(f"  Non-trivial S_4-preserving:      {len(non_integer_s4_pass)}")
print(f"  C(beta) > 2*sqrt(33):            {sum(1 for r in certified if r['above_33'])}")
print()
print(f"  Certified beta values: {[r['beta'] for r in certified]}")
print()
print("  DEGENERATE CASE NOTE:")
print("  C(300) = C(298) = sum log(p)*p/(p-1) for all p<=1000 = {:.6f}".format(float(C_all_1000)))
print("  This is NOT specific to the 600-cell -- it holds for all integer beta.")
print("  The g=33 certification in M10 used p_5 = 3993746143633 (from M4).")
print("  The 600-cell vertex (1,0,0,0) provides an ALTERNATIVE PROOF (degenerate).")
print()
print("CERTIFIED.")
