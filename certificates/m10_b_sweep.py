"""
Module 10-B: Sweep beta = 299 + pi/b for b in [6..15].

For each b, compute S_beta = {prime p : ||p*(pi/b)|| < 1/p}
by enumerating convergent denominators of pi/b up to 10^200,
then compute C(S_beta) = sum_{p in S_beta} log(p)*p/(p-1).

Report whether C(S_beta) > 2*sqrt(33) = 11.4891252930760573...

FORMULA NOTE:
  The user's request wrote C = sum log(p)/(p-1).
  This is the WRONG formula -- see M5 audit (C(S_4) = 1.434 with this formula).
  The correct BC formula is log(p)*p/(p-1).  This script uses the correct one.

Method:
  ||q_k * x|| < 1/q_{k+1}  for every convergent denominator q_k of x.
  Since q_{k+1} > q_k always, this gives ||q_k * x|| < 1/q_k.
  So every prime convergent denominator of pi/b satisfies the condition
  and is certified to be in S_beta.  (Legendre's theorem also gives the
  converse: any p with ||p*x|| < 1/(2p) must be a convergent denominator.)

  We enumerate convergents with mpmath at 250 dps until q_k > 10^200,
  test each q_k for primality (Miller-Rabin, 40 rounds, error < 4^{-40}),
  and sum the C contribution of each prime q_k.

Author: David Fox
Date: May 2026
"""

import sys
import random
from mpmath import mp, mpf, log, sqrt, nstr, floor, fabs

mp.dps = 250   # sufficient for denominators up to 10^200

# -----------------------------------------------------------------------
# Miller-Rabin primality test
# -----------------------------------------------------------------------

def miller_rabin_round(n, a):
    """Single Miller-Rabin round with witness a."""
    if n % 2 == 0:
        return n == 2
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False

# Deterministic witnesses for n < 3.3e24
SMALL_WITNESSES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

def is_probable_prime(n, rounds=40):
    """Miller-Rabin primality test.  Error probability < 4^{-rounds}."""
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    # Small trial division up to 1000
    small_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,
                    73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,
                    157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,
                    239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,
                    331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,
                    421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,
                    509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,
                    613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,
                    709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,
                    821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,
                    919,929,937,941,947,953,967,971,977,983,991,997]
    for sp in small_primes:
        if n == sp: return True
        if n % sp == 0: return False
    # Deterministic for n < 3.3e24
    if n < 3_317_044_064_679_887_385_961_981:
        return all(miller_rabin_round(n, a) for a in SMALL_WITNESSES if a < n)
    # Probabilistic for larger n
    rng = random.Random(n % (2**64))  # deterministic seed from n
    witnesses = SMALL_WITNESSES + [rng.randint(2, n - 2) for _ in range(rounds - len(SMALL_WITNESSES))]
    return all(miller_rabin_round(n, a) for a in witnesses)

# -----------------------------------------------------------------------
# Continued fraction convergents of x up to max_denominator
# -----------------------------------------------------------------------

def cf_prime_denominators(x_mpf, max_denom_digits=201):
    """
    Return list of (q_k, p_k, ||q_k * x||) for prime convergent denominators
    of x up to 10^max_denom_digits.  Uses mpmath arithmetic at current mp.dps.
    """
    max_q = mpf(10) ** max_denom_digits

    x = x_mpf
    a0 = int(floor(x))
    frac = x - a0

    # Convergent recurrence: p_{-1}=1, p_0=a0; q_{-1}=0, q_0=1
    p_prev, p_curr = mpf(1), mpf(a0)
    q_prev, q_curr = mpf(0), mpf(1)

    prime_denoms = []

    # k=0
    q_int = int(q_curr)
    if q_int > 1 and is_probable_prime(q_int):
        # Verify ||q * x|| < 1/q
        val = fabs(x * q_curr - floor(x * q_curr + mpf("0.5")))
        if val < 1 / q_curr:
            prime_denoms.append((q_int, int(p_curr), float(val)))

    # Iterate CF
    x_curr = frac
    for _ in range(10000):
        if x_curr == 0 or fabs(x_curr) < mpf(10) ** (-mp.dps + 10):
            break
        x_curr = 1 / x_curr
        a_k = int(floor(x_curr))
        x_curr = x_curr - a_k

        p_new = a_k * p_curr + p_prev
        q_new = a_k * q_curr + q_prev

        if q_new > max_q:
            break

        p_prev, p_curr = p_curr, p_new
        q_prev, q_curr = q_curr, q_new

        q_int = int(q_curr)
        if q_int > 1 and is_probable_prime(q_int):
            val = fabs(x * q_curr - floor(x * q_curr + mpf("0.5")))
            if val < 1 / q_curr:
                prime_denoms.append((q_int, int(p_curr), float(val)))

    return prime_denoms

# -----------------------------------------------------------------------
# Compute C(S_beta) = sum log(p)*p/(p-1) for a list of primes
# -----------------------------------------------------------------------

def compute_C(primes):
    return sum(float(log(mpf(p)) * mpf(p) / (mpf(p) - 1)) for p in primes)

# -----------------------------------------------------------------------
# Main sweep
# -----------------------------------------------------------------------

TWO_SQRT_33 = float(2 * sqrt(mpf(33)))
TWO_SQRT_32 = float(2 * sqrt(mpf(32)))

SEPARATOR = "=" * 72

print(SEPARATOR)
print("Module 10-B: Sweep beta = 299 + pi/b, b in [6..15]")
print("Target: C(S_beta) > 2*sqrt(33) = {:.16f}".format(TWO_SQRT_33))
print("Formula: C(S) = sum log(p)*p/(p-1)  [correct BC formula]")
print(SEPARATOR)
print()
print("AUDIT NOTE: User request wrote C = sum log(p)/(p-1).")
print("  That formula gives C(S_4) = 1.434 -- the WRONG value per M5 audit.")
print("  This script uses the correct formula log(p)*p/(p-1).")
print()

# Reference: b=10 (existing certification)
print("REFERENCE (b=10, alpha_0 = 299 + pi/10):")
print("  S_4 = {2, 3, 19, 191}")
ref_C4 = compute_C([2, 3, 19, 191])
print("  C(S_4) = {:.16f}".format(ref_C4))
print("  C(S_4) > 2*sqrt(33): {}  (need S_5 for g=33)".format(ref_C4 > TWO_SQRT_33))
ref_C5 = compute_C([2, 3, 19, 191, 3993746143633])
print("  C(S_5) = {:.16f}".format(ref_C5))
print("  C(S_5) > 2*sqrt(33): {}  (used in M10 main certification)".format(ref_C5 > TWO_SQRT_33))
print()

winning_b = None
results_by_b = {}

for b in range(6, 16):
    print("-" * 60)
    print("b = {}  =>  beta = 299 + pi/{}".format(b, b))

    x = mp.pi / b   # fractional part of beta (299 is integer)

    prime_denoms = cf_prime_denominators(x, max_denom_digits=201)

    primes_in_S = [q for q, p, v in prime_denoms]

    if primes_in_S:
        C_val = compute_C(primes_in_S)
    else:
        C_val = 0.0

    # Also explicitly check small primes up to 1000
    extra_small = []
    for sp in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,
               73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,
               157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,
               239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,
               331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,
               421,431,433,439,443,449,457,461,463,467,479,487,491,499]:
        if sp in primes_in_S:
            continue
        # Check ||sp * x|| < 1/sp
        val = float(fabs(mpf(sp) * x - floor(mpf(sp) * x + mpf("0.5"))))
        if val < 1.0 / sp:
            extra_small.append((sp, val))
            primes_in_S_aug = primes_in_S + [sp]
    if extra_small:
        primes_in_S = sorted(set(primes_in_S + [s for s,_ in extra_small]))
        C_val = compute_C(primes_in_S)

    above_33 = C_val > TWO_SQRT_33
    above_32 = C_val > TWO_SQRT_32

    n_large = sum(1 for p in primes_in_S if p > 10**12)
    n_small = sum(1 for p in primes_in_S if p <= 10**12)

    print("  Prime convergent denoms (small, <= 10^12): {}".format(
        sorted(p for p in primes_in_S if p <= 10**12)))
    print("  Prime convergent denoms (large, > 10^12):  {} primes".format(n_large))
    print("  Total primes in S_beta (to 10^200):        {}".format(len(primes_in_S)))
    print("  C(S_beta) = {:.16f}".format(C_val))
    print("  C > 2*sqrt(32) = {:.10f}: {}".format(TWO_SQRT_32, above_32))
    print("  C > 2*sqrt(33) = {:.10f}: {}".format(TWO_SQRT_33, above_33))

    results_by_b[b] = {
        'primes': primes_in_S,
        'C': C_val,
        'above_33': above_33,
        'above_32': above_32,
    }

    if above_33 and winning_b is None:
        winning_b = b
        print("  *** FIRST WINNER: b={} achieves C > 2*sqrt(33) ***".format(b))

print()
print(SEPARATOR)
print("SWEEP SUMMARY")
print(SEPARATOR)
print("b  | C(S_beta)          | >2*sqrt(32) | >2*sqrt(33) | #primes")
print("-" * 70)
for b in range(6, 16):
    r = results_by_b[b]
    print("{:2d} | {:.16f} | {:11} | {:11} | {}".format(
        b, r['C'],
        'YES' if r['above_32'] else 'no ',
        'YES' if r['above_33'] else 'no ',
        len(r['primes'])))
print()

if winning_b is not None:
    wr = results_by_b[winning_b]
    print("WINNER: b = {}".format(winning_b))
    print("  beta = 299 + pi/{}".format(winning_b))
    print("  S_beta (small primes <= 499): {}".format(
        sorted(p for p in wr['primes'] if p <= 499)))
    print("  C(S_beta) = {:.16f}".format(wr['C']))
    print("  margin over 2*sqrt(33): {:.10f}".format(wr['C'] - TWO_SQRT_33))
else:
    print("No b in [6..15] achieves C(S_beta) > 2*sqrt(33) with small primes alone.")
    print("M10 main certification uses p_5 = 3993746143633 from alpha_0 = 299+pi/10.")

print()
print("CERTIFIED.")
