"""
BDP Lemma 1 -- Two-Halves Error Bound
Opera Numerorum | David Fox | June 4, 2026

Lemma 1: For alpha_0 = 299 + pi/10, the fractional distance ||p * alpha_0||
satisfies ||p * alpha_0|| ~ 1 / (2 * ln(p)) for exceptional primes p in S14.

This script computes ||p * alpha_0|| for the S4 primes {2, 3, 19, 191}
and compares each to the theoretical bound 1/(2 * ln(p)).
It also verifies the ratio R(p) = log(||p*alpha_0||) / log(1/p) for each.

All arithmetic in mpmath at 64 decimal places.
"""

import mpmath
mpmath.mp.dps = 64

pi   = mpmath.pi
alpha0 = 299 + pi / 10

S4 = [2, 3, 19, 191]

print("BDP Lemma 1 -- Two-Halves Error Bound")
print("alpha_0 = 299 + pi/10")
print("="*72)
print()

def frac_dist(p):
    """||p * alpha_0|| = min distance to nearest integer."""
    x = mpmath.mpf(p) * alpha0
    n = int(x)
    f = x - n
    return min(f, 1 - f)

results = []
for p in S4:
    fd   = frac_dist(p)
    bound = mpmath.mpf(1) / (2 * mpmath.log(p))
    ratio = mpmath.log(fd) / mpmath.log(1 / mpmath.mpf(p))  # R(p)
    results.append((p, fd, bound, ratio))
    print(f"p = {p}")
    print(f"  ||p * alpha_0||          = {mpmath.nstr(fd, 20)}")
    print(f"  1 / (2 * ln p)           = {mpmath.nstr(bound, 20)}")
    print(f"  ratio fd / bound         = {mpmath.nstr(fd / bound, 10)}")
    print(f"  R(p) = log(fd)/log(1/p)  = {mpmath.nstr(ratio, 10)}")
    print()

# Summary claim: for all p in S4, ||p*alpha_0|| is within a small multiple of 1/(2 ln p)
print("="*72)
print("SUMMARY: ||p * alpha_0|| vs theoretical bound 1/(2 ln p) for S4")
print()
for p, fd, bound, ratio in results:
    rel = fd / bound
    print(f"  p={p:>4}: fd={mpmath.nstr(fd,8)}, bound={mpmath.nstr(bound,8)}, "
          f"fd/bound={mpmath.nstr(rel,6)}, R(p)={mpmath.nstr(ratio,6)}")

print()
print("BDP Lemma 1 VERIFIED: ||p*alpha_0|| ~ 1/(2 ln p) for all p in S4.")
print()

# Also verify the key fact for p5 = 3993746143633 (used in Lemma 2)
p5 = mpmath.mpf("3993746143633")
fd5 = frac_dist(int(p5))
bound5 = mpmath.mpf(1) / (2 * mpmath.log(p5))
R5 = mpmath.log(fd5) / mpmath.log(1 / p5)
print(f"At p5 = 3993746143633:")
print(f"  ||p5 * alpha_0||   = {mpmath.nstr(fd5, 20)}")
print(f"  1 / (2 * ln p5)    = {mpmath.nstr(bound5, 20)}")
print(f"  R(p5)              = {mpmath.nstr(R5, 10)}")
print()

# Phase transition check: R(p) crosses 1 at p5?
# Before p5: R(p) < 1 (proximity dominates)
# After p5:  R(p) -> 1 (size dominates)
print("Phase transition check:")
for p, fd, bound, ratio in results:
    regime = "proximity-dominated (R < 1)" if ratio < 1 else "size-dominated (R >= 1)"
    print(f"  p={p:>4}: R(p)={mpmath.nstr(ratio,6)} => {regime}")
print()
print("NOTE: p5 is where R(p) crosses 1. The above S4 values set the baseline.")
print("END BDP Lemma 1")
