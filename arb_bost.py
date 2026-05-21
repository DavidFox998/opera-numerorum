#!/usr/bin/env python3
"""
Module 5 - Bost Sum C(S14) > 2*sqrt(13)
Battle Plan v1.6 -- mpmath fallback for ARB (ARB not available in environment)
Reads Module 4 stdout format: comma-separated single line.
Parent: Module 4 SHA b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed
"""
import sys
import os
from mpmath import mp, log, sqrt, mpf, nstr, fabs

mp.dps = 64  # 64 decimal places ~ 212 binary bits (exceeds 64-bit ARB PREC)

def load_primes(path):
    """Read comma-separated or newline-separated primes from Module 4 stdout."""
    with open(path) as f:
        content = f.read().strip()
    if ',' in content:
        return [int(s.strip()) for s in content.split(',') if s.strip()]
    return [int(s.strip()) for s in content.splitlines() if s.strip()]

def fmt_interval(center, radius):
    """Format as ARB-style interval string."""
    import math
    c_f = float(center)
    r_f = float(radius)
    if r_f <= 0:
        return f"[{c_f:.16f} +/- 0]"
    exp = int(math.floor(math.log10(r_f)))
    mant = r_f / (10 ** exp)
    return f"[{c_f:.16f} +/- {mant:.2f}e{exp:+03d}]"

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} S14_primes.txt", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    primes = load_primes(path)
    if len(primes) != 14:
        print(f"ERROR: expected 14 primes, got {len(primes)}", file=sys.stderr)
        sys.exit(1)

    # Compute C(S14) = sum_{p in S14} log(p) / (p - 1)
    # mpmath at 64 dps handles arbitrarily large integers exactly.
    # Floating-point error per term < 2^-210; for 14 terms < 2^-206 < 1e-62.
    C = mpf(0)
    for p in primes:
        mp_p = mpf(p)
        C += log(mp_p) / (mp_p - 1)

    # Conservative published error bound: relative 1e-12 (>> actual rounding error)
    C_radius = mpf("1.43e-12") * fabs(C)

    # 2*sqrt(13) with same precision
    threshold = 2 * sqrt(mpf(13))
    T_radius  = mpf("1.11e-12") * threshold

    # Rigorous interval comparison
    C_lower = C - C_radius
    T_upper = threshold + T_radius
    gt = 1 if C_lower > T_upper else 0

    print(f"C(S14) in {fmt_interval(C, C_radius)}")
    print(f"2*sqrt(13) in {fmt_interval(threshold, T_radius)}")
    print(f"arb_gt(C, threshold) = {gt}")

    if not gt:
        # Detailed forensic output to stderr so stdout remains clean for SHA
        print(f"FORMULA AUDIT: C(S14) = {nstr(C, 20)}", file=sys.stderr)
        print(f"  Expected  ~ 8.6294509916111192 (LaTeX blueprint)", file=sys.stderr)
        print(f"  Computed  ~ {nstr(C, 16)} (literal sum log(p)/(p-1))", file=sys.stderr)
        print(f"  Max possible sum over any 14 distinct primes ~ 3.414", file=sys.stderr)
        print(f"  (using 14 smallest primes 2,3,5,7,11,13,17,19,23,29,31,37,41,43)", file=sys.stderr)
        print(f"  Mathematical impossibility: formula cannot produce 8.6294...", file=sys.stderr)
        print(f"  Supervisor clarification required.", file=sys.stderr)
        sys.exit(2)

    print("Certificate: C(S14) > 2*sqrt(13) verified")

if __name__ == "__main__":
    main()
