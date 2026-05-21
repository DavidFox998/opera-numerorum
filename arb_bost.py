#!/usr/bin/env python3
"""
Module 5: Bost Sum C(S14) vs 2*sqrt(13)
Battle Plan v1.6 -- mpmath replacement for ARB (ARB not available)
Parent: Module 4 SHA b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed
"""
import sys
import os
from mpmath import mp, log, sqrt, mpf, nstr, fabs

mp.dps = 64  # >= 64 bits as specified; 64 decimal places ~ 212 binary bits

def load_primes(path):
    primes = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                primes.append(int(line))
    return primes

def format_interval(center, radius):
    c = float(center)
    r = float(radius)
    exp = 0
    rv = r
    if rv > 0:
        import math
        exp = int(math.floor(math.log10(rv)))
        mantissa = rv / (10 ** exp)
        return f"[{c:.16f} +/- {mantissa:.2f}e{exp:+d}]"
    return f"[{c:.16f} +/- 0]"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 arb_bost.py data/S14_primes.txt", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    primes = load_primes(path)
    n = len(primes)

    # Compute C(S14) = sum_{p in S14} log(p) / (p - 1)
    # Using mpmath at 64 dps for rigorous computation.
    # Error bound: half-ULP at 64 dps for each of n terms, summed.
    # Half-ULP at 64 dps ~ 5e-64; for 14 terms ~ 7e-63 (well below 1e-10).
    # We report a conservative radius of 1e-10 to be explicit.
    C_sum = mpf(0)
    for p in primes:
        mp_p = mpf(p)
        C_sum += log(mp_p) / (mp_p - 1)

    # Conservative error radius: 14 terms * half-ULP at working precision
    # half-ULP ~ 10^{-64}; round up to a safe published bound
    C_center = C_sum
    C_radius = mpf("1e-12") * fabs(C_sum)  # relative 1e-12 as conservative bound

    # Compute 2*sqrt(13) with same precision
    threshold = 2 * sqrt(mpf(13))
    T_radius = mpf("1e-12") * threshold

    # Rigorous comparison: lower bound of C vs upper bound of threshold
    C_lower  = C_center - C_radius
    T_upper  = threshold + T_radius
    verified = bool(C_lower > T_upper)

    print(f"C(S14) in {format_interval(C_center, C_radius)}")
    print(f"2*sqrt(13) in {format_interval(threshold, T_radius)}")
    print(f"arb_gt(C, threshold) = {verified} ({1 if verified else 0})")
    if verified:
        print("Certificate: C(S14) > 2*sqrt(13) verified")
    else:
        print(f"FORMULA AUDIT: C(S14) = {nstr(C_center, 20)}")
        print(f"  Expected ~ 8.6294509916111192 (from LaTeX)")
        print(f"  Computed ~ {float(C_center):.16f} (literal sum log(p)/(p-1))")
        print(f"  Discrepancy: the LaTeX formula sum log(p)/(p-1) does NOT")
        print(f"  produce 8.6294... with these 14 primes.")
        print(f"  Supervisor clarification required before certification.")
        sys.exit(2)

if __name__ == "__main__":
    main()
