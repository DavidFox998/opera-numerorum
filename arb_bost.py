#!/usr/bin/env python3
"""
Module 5 - Bost Sum C(S4) > 2*sqrt(13)
Battle Plan v1.6 -- mpmath fallback for ARB (ARB not available in environment)
Set: S4 = {2, 3, 19, 191}, the first 4 elements of S(alpha_0).
Parent: Module 4 SHA b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed
"""
import sys
import os
from mpmath import mp, log, sqrt, mpf, nstr, fabs

mp.dps = 64  # 64 decimal places ~212 binary bits (exceeds 64-bit ARB PREC)

# S4 = first 4 elements of S(alpha_0) per supervisor correction
S4 = [2, 3, 19, 191]

def fmt_interval(center, radius):
    """Format as ARB-style interval string."""
    import math
    c_f = float(center)
    r_f = float(radius)
    if r_f <= 0:
        return f"[{c_f:.10f} +/- 0]"
    exp = int(math.floor(math.log10(r_f)))
    mant = r_f / (10 ** exp)
    return f"[{c_f:.10f} +/- {mant:.2f}e{exp:+03d}]"

def main():
    # Compute C(S4) = sum_{p in S4} log(p) / (p - 1)
    # mpmath at 64 dps handles all terms exactly.
    # Rounding error per term < 2^-210; for 4 terms < 2^-208 < 1e-62.
    C = mpf(0)
    for p in S4:
        mp_p = mpf(p)
        C += log(mp_p) / (mp_p - 1)

    # Conservative published error bound
    C_radius = mpf("1e-10")

    # 2*sqrt(13) with same precision
    threshold = 2 * sqrt(mpf(13))
    T_radius  = mpf("1e-10")

    # Rigorous interval comparison
    C_lower = C - C_radius
    T_upper = threshold + T_radius
    gt = 1 if C_lower > T_upper else 0

    print(f"C(S4) in {fmt_interval(C, C_radius)}")
    print(f"2*sqrt(13) in {fmt_interval(threshold, T_radius)}")
    print(f"arb_gt(C, threshold) = {gt}")

    if not gt:
        print(f"FORMULA AUDIT: C(S4) = {nstr(C, 20)}", file=sys.stderr)
        print(f"  S4 = {{2, 3, 19, 191}} (first 4 elements of S(alpha_0))", file=sys.stderr)
        print(f"  Computed  ~ {nstr(C, 16)} (literal sum log(p)/(p-1))", file=sys.stderr)
        print(f"  Claimed   ~ 8.6290436642 (supervisor LaTeX)", file=sys.stderr)
        print(f"  2*sqrt(13)~ {nstr(threshold, 16)}", file=sys.stderr)
        print(f"  Formula sum log(p)/(p-1) gives 1.434, not 8.629.", file=sys.stderr)
        print(f"  Maximum possible for any 4 distinct primes: ~1.968", file=sys.stderr)
        print(f"  (using {{2,3,5,7}}: 0.693+0.549+0.402+0.324=1.968)", file=sys.stderr)
        print(f"  Supervisor clarification required.", file=sys.stderr)
        sys.exit(2)

    print("Certificate: C(S4) > 2*sqrt(13) verified")

if __name__ == "__main__":
    main()
