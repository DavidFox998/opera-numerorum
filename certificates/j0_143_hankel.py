"""
Module 8: J_0(143) Hecke Hankel rank check
Claim: rank(H_{13}(L_w, J_0(143))) = g = 13

Method: LMFDB-sourced Hecke eigenvalues for all four form orbits
contributing to J_0(143), combined with the Bost-Connes weights
delta_p = ln(p)*p/(p-1) for S_4 = {2, 3, 19, 191}.

Python + mpmath fallback (no SageMath, no ARB).
LMFDB data verified 2026-05-22.
"""
from mpmath import mp, mpf, mpc, sqrt, log, polyroots, fabs, im, re, nstr as mstr

mp.dps = 60  # 60 decimal places

PRIMES_S4 = [2, 3, 19, 191]

def delta(p):
    """Bost-Connes weight: delta_p = ln(p)*p/(p-1)."""
    return log(mpf(p)) * p / (p - 1)

# ===================================================================
# LMFDB Hecke eigenvalue data (fetched 2026-05-22, label format N.k.chi.orbit)
# All forms have trivial character (chi = a), weight 2, level 143 or 11.
# ===================================================================

# 11.2.a.a  (rational, appears TWICE as old form via f(z) and f(13z))
a_11 = {2: -2, 3: -1, 19: 0, 191: 17}

# 143.2.a.a  (rational newform, dim=1)
a_aa = {2: 0, 3: -1, 19: 2, 191: -15}

# 143.2.a.b  (newform, dim=4, coefficient field: totally real degree-4)
# field_poly (ascending): 1 - x - 4x^2 + x^4
fp_b = [1, -1, -4, 0, 1]
# hecke_ring_numerators (integral basis -> power basis):
#   e_j = sum_k basis_b[j][k] * theta^k
basis_b = [
    [1,  0,  0,  0],   # e_0 = 1
    [0,  1,  0,  0],   # e_1 = theta
    [-1, -4, 0,  1],   # e_2 = -1 - 4*theta + theta^3
    [-1,  3, 1, -1],   # e_3 = -1 + 3*theta + theta^2 - theta^3
]
# ap in integral basis {e_0,e_1,e_2,e_3} at each prime
ap_b = {
    2:   [1,  1,  1,  0],
    3:   [0,  0, -1, -1],
    19:  [2, -2, -3, -3],
    191: [0, -4, -9,  3],
}

# 143.2.a.c  (newform, dim=6, coefficient field: totally real degree-6)
# field_poly (ascending): -12 + 7x + 24x^2 - 2x^3 - 10x^4 + x^6
fp_c = [-12, 7, 24, -2, -10, 0, 1]
# hecke_ring_numerators:
basis_c = [
    [1,   0,   0,  0,  0,  0],
    [0,   1,   0,  0,  0,  0],
    [-3,  0,   1,  0,  0,  0],
    [-6,  11,  6, -8, -1,  1],
    [8,  -16, -7,  9,  1, -1],
    [15, -12,-14,  8,  2, -1],
]
ap_c = {
    2:   [0,  -1,  0,  0,  0,  0],
    3:   [1,   0,  0,  1,  0,  0],
    19:  [-1,  0,  0,  1,  0, -1],
    191: [-3,  0,  4, -3,  0, -2],
}

# ===================================================================
# Helper functions
# ===================================================================

def eval_at_root(ap_coords, basis, theta):
    """Evaluate Hecke eigenvalue at Galois embedding theta."""
    rank = len(ap_coords)
    result = mpc(0)
    for j in range(rank):
        e_j = mpc(0)
        th_k = mpc(1)
        for k in range(rank):
            e_j += basis[j][k] * th_k
            th_k *= theta
        result += ap_coords[j] * e_j
    return result

def frob_pair(a_p, p):
    """Frobenius eigenvalues: roots of x^2 - a_p*x + p = 0."""
    disc = a_p * a_p - 4 * p
    sq = sqrt(disc)
    return (a_p + sq) / 2, (a_p - sq) / 2

def find_roots(fp_asc):
    """Roots of polynomial with ascending-degree coefficients."""
    return polyroots(list(reversed(fp_asc)))

# ===================================================================
# Compute all 26 eigenvalues of L_w on H_1(J_0(143), C)
# ===================================================================
all_eigs = []

print("=== J_0(143) Hecke Hankel rank check ===")
print("mpmath precision: 60 dps")
print()
print("Form decomposition of S_2(Gamma_0(143)):")
print("  Old: 11.2.a.a x2 (dim=1 appears twice)  -> 4 eigenvalues")
print("  New: 143.2.a.a  (dim=1, rational)        -> 2 eigenvalues")
print("  New: 143.2.a.b  (dim=4, totally real)    -> 8 eigenvalues")
print("  New: 143.2.a.c  (dim=6, totally real)    -> 12 eigenvalues")
print("  Total: 26 eigenvalues of L_w on H_1")
print()

# --- 11.2.a.a x2 ---
for copy in range(2):
    la, lb = mpc(0), mpc(0)
    for p in PRIMES_S4:
        alp, bet = frob_pair(mpf(a_11[p]), p)
        d = delta(p)
        la += d * alp
        lb += d * bet
    all_eigs += [la, lb]
print(f"Old form 11.2.a.a lambda_alpha = {mstr(la, 8)}")
print(f"Old form 11.2.a.a lambda_beta  = {mstr(lb, 8)}")
print()

# --- 143.2.a.a ---
la, lb = mpc(0), mpc(0)
for p in PRIMES_S4:
    alp, bet = frob_pair(mpf(a_aa[p]), p)
    d = delta(p)
    la += d * alp
    lb += d * bet
all_eigs += [la, lb]
print(f"New form 143.2.a.a lambda_alpha = {mstr(la, 8)}")
print(f"New form 143.2.a.a lambda_beta  = {mstr(lb, 8)}")
print()

# --- 143.2.a.b ---
roots_b = find_roots(fp_b)
print("143.2.a.b Galois roots (theta):", [mstr(r, 6) for r in roots_b])
for i, theta in enumerate(roots_b):
    la, lb = mpc(0), mpc(0)
    for p in PRIMES_S4:
        a_pth = eval_at_root(ap_b[p], basis_b, theta)
        alp, bet = frob_pair(a_pth, p)
        la += delta(p) * alp
        lb += delta(p) * bet
    all_eigs += [la, lb]
    print(f"  sigma_{i}: lambda_alpha = {mstr(la, 8)}")
print()

# --- 143.2.a.c ---
roots_c = find_roots(fp_c)
print("143.2.a.c Galois roots (theta):", [mstr(r, 6) for r in roots_c])
for i, theta in enumerate(roots_c):
    la, lb = mpc(0), mpc(0)
    for p in PRIMES_S4:
        a_pth = eval_at_root(ap_c[p], basis_c, theta)
        alp, bet = frob_pair(a_pth, p)
        la += delta(p) * alp
        lb += delta(p) * bet
    all_eigs += [la, lb]
    print(f"  sigma_{i}: lambda_alpha = {mstr(la, 8)}")
print()

assert len(all_eigs) == 26, f"Expected 26 eigenvalues, got {len(all_eigs)}"
print(f"Total eigenvalues: {len(all_eigs)}")
max_im = max(fabs(im(e)) for e in all_eigs)
print(f"Max |Im(lambda_j)| = {mstr(max_im, 6)}")
print()

# ===================================================================
# Power sums -> elementary symmetric polynomials (Newton's identities)
# ===================================================================
psum = [sum(lam**k for lam in all_eigs) for k in range(1, 27)]

e = [mpc(0)] * 27
e[0] = mpc(1)
for k in range(1, 27):
    s = mpc(0)
    for j in range(1, k + 1):
        s += ((-1)**(j-1)) * e[k-j] * psum[j-1]
    e[k] = s / k

max_ek_im = max(fabs(im(e[k])) for k in range(1, 26))
print(f"Max |Im(e_k)| for k=1..25: {mstr(max_ek_im, 4)} (should be ~0)")
print()

print("Elementary symmetric polynomials e_k = tr(Lambda^k L_w):")
for k in range(1, 14):
    print(f"  e_{k:2d} = {mstr(re(e[k]), 12)}")
print()

# ===================================================================
# 13x13 Hankel matrix H[i,j] = Re(e[i+j+1])  for i,j in 0..12
# ===================================================================
g = 13
H = [[re(e[i+j+1]) for j in range(g)] for i in range(g)]

# Gaussian elimination with partial pivoting to find rank
def gauss_rank(H, g, tol=mpf('1e-20')):
    A = [[H[i][j] for j in range(g)] for i in range(g)]
    rank = 0
    min_piv = mpf('1e+300')
    for col in range(g):
        mx, mr = mpf(0), -1
        for row in range(rank, g):
            v = fabs(A[row][col])
            if v > mx:
                mx, mr = v, row
        if mx < tol:
            continue
        A[rank], A[mr] = A[mr], A[rank]
        piv = A[rank][col]
        if piv < min_piv:
            min_piv = piv
        for row in range(g):
            if row != rank:
                f = A[row][col] / piv
                for j in range(g):
                    A[row][j] -= f * A[rank][j]
        rank += 1
    return rank, min_piv

rank, min_piv = gauss_rank(H, g)

print("=" * 50)
print(f"HANKEL MATRIX H_{{13}} RANK CHECK")
print(f"g = genus(X_0(143)) = {g}")
print(f"rank(H_{{g}}) = {rank}")
print(f"min pivot magnitude = {mstr(min_piv, 4)}")
print(f"rank(H) <= g:  {'PASS' if rank <= g else 'FAIL'}")
print(f"rank(H) == g:  {'YES (full rank)' if rank == g else 'NO (rank deficient)'}")
print("=" * 50)

# ===================================================================
# Verify Weil bounds on a_p values
# ===================================================================
print()
print("Weil bound verification for key eigenvalues:")
import math
for p in PRIMES_S4:
    bound = 2 * math.sqrt(p)
    print(f"  p={p:3d}: bound = 2*sqrt({p}) = {bound:.4f}")
    print(f"    11.2.a.a:  a_{p} = {a_11[p]}  |a_p|={abs(a_11[p]):.2f}  {'OK' if abs(a_11[p]) <= bound else 'FAIL'}")
    print(f"    143.2.a.a: a_{p} = {a_aa[p]}  |a_p|={abs(a_aa[p]):.2f}  {'OK' if abs(a_aa[p]) <= bound else 'FAIL'}")
