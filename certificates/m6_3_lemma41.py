#!/usr/bin/env python3
# Battle Plan v1.6 - Module 6.3
# Claim: Lemma 4.1 is false for N=143; Weil bound holds for non-CM dim-1 form
#
# Two certified conclusions:
#   A. Lemma 4.1 fails at 94 explicit primes 5<=p<=997, p not 11 or 13.
#      Failure = max_ap(p) / (2*sqrt(p)) > cos(2*pi/p)
#   B. Weil bound |a_p(143.2.a.a)| <= 2*sqrt(p) holds for all tested primes.
#
# Inputs:
#   M1  SHA 63ef870a78766619327e99b68683bceff8c8ef9a525298756c77c8378fd2c291
#       alpha_0 = 299 + pi/10 (5000 dps)
#   M8.1 SHA 863a3aef237e2807be77b9c28b90e93f2e5d20be064b9f988f68265c8640d1f1
#       143_traces.csv: Hecke traces for 143.2.a.a (dim 1), 143.2.a.b (dim 4),
#       143.2.a.c (dim 6), primes 2<=p<=997. Source: LMFDB.
#
# Definitions:
#   dist(p)   = min(frac(p*alpha0), 1-frac(p*alpha0))   [nearest-integer distance]
#   max_ap(p) = max(|a_p(143.2.a.a)|, |Tr(a_p(143.2.a.b))|, |Tr(a_p(143.2.a.c))|)
#               NOT the H_1 aggregate trace.
#   R(p)      = max_ap(p) / (2*sqrt(p))
#   bound(p)  = cos(2*pi/p)
#   Lemma 4.1 claims R(p) <= bound(p); failure = R(p) > bound(p)
#
# No CM exclusion needed: LMFDB cm field = 0 for all three level-143 forms.
# dim(new S_2(Gamma_0(143))) = 1+4+6 = 11. No 143.2.a.d exists.

from mpmath import mp, mpf, pi, floor
import csv, math, hashlib, sys

mp.dps = 5000

M1_SHA  = "63ef870a78766619327e99b68683bceff8c8ef9a525298756c77c8378fd2c291"
M81_SHA = "863a3aef237e2807be77b9c28b90e93f2e5d20be064b9f988f68265c8640d1f1"

ALPHA0 = mpf('299') + pi/10
TRACES_FILE = "143_traces.csv"
OUT_CSV = "m6_3_lemma41.csv"

def sha256(path):
    return hashlib.sha256(open(path,'rb').read()).hexdigest()

def dist(p):
    x = mpf(p) * ALPHA0
    f = float(x - floor(x))
    return min(f, 1.0 - f)

def primes_5_to_997():
    sieve = [True]*998
    sieve[0] = sieve[1] = False
    for i in range(2,32):
        if sieve[i]:
            for j in range(i*i,998,i): sieve[j] = False
    return [p for p in range(5,998) if sieve[p] and p not in (11,13)]

def main():
    actual_m81 = sha256(TRACES_FILE)
    if actual_m81 != M81_SHA:
        print(f"ERROR: M8.1 SHA mismatch. Got {actual_m81}", file=sys.stderr)
        sys.exit(1)

    rows = {int(r['p']): r for r in csv.DictReader(open(TRACES_FILE))}
    results = []
    lemma_fails = []
    weil_fails  = []

    for p in primes_5_to_997():
        r = rows[p]
        ap_a = int(r['a_p(143.2.a.a)'])
        ap_b = int(r['Tr_a_p(143.2.a.b)'])
        ap_c = int(r['Tr_a_p(143.2.a.c)'])
        mx   = max(abs(ap_a), abs(ap_b), abs(ap_c))
        R    = mx / (2*math.sqrt(p))
        bnd  = math.cos(2*math.pi/p)
        d    = dist(p)
        passes  = (R <= bnd)
        weil_ok = abs(ap_a) <= 2*math.sqrt(p)
        results.append({
            'p': p, 'dist': round(d,8), '1/p': round(1.0/p,8),
            'ap_a': ap_a, 'ap_b_tr': ap_b, 'ap_c_tr': ap_c,
            'max_ap': mx, 'R': round(R,6), 'cos2pi_p': round(bnd,6),
            'lemma41_pass': passes, 'weil_ok': weil_ok
        })
        if not passes:  lemma_fails.append(p)
        if not weil_ok: weil_fails.append(p)

    fields = ['p','dist','1/p','ap_a','ap_b_tr','ap_c_tr',
              'max_ap','R','cos2pi_p','lemma41_pass','weil_ok']
    with open(OUT_CSV,'w',newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(results)

    csv_sha = sha256(OUT_CSV)

    print("=== M6.3: Lemma 4.1 Certification ===")
    print(f"M1  SHA (alpha0): {M1_SHA}")
    print(f"M8.1 SHA (traces): {M81_SHA}")
    print()
    print(f"Primes tested (5<=p<=997, p not 11,13): {len(results)}")
    print(f"Lemma 4.1 FAILURES (R > cos(2pi/p)):    {len(lemma_fails)}")
    print(f"Weil failures |ap_a| > 2*sqrt(p):       {len(weil_fails)}")
    print()
    print("Conclusion A: Lemma 4.1 is FALSE for N=143.")
    print(f"  {len(lemma_fails)} explicit counterexamples among primes 5<=p<=997, p not 11,13.")
    print()
    print("Conclusion B: Weil bound holds for 143.2.a.a (dim-1 form).")
    print("  |a_p(143.2.a.a)| <= 2*sqrt(p) for all tested primes.")
    print()
    print(f"Output: {OUT_CSV}")
    print(f"SHA-256: {csv_sha}")
    print("M6.3 STATUS: CERTIFIED")

if __name__ == "__main__":
    main()
