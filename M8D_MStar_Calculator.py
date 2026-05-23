"""
M8D_MStar_Calculator.py
Opera Numerorum -- M8D utility
Predict VNA trace before building the 120-cell resonator.
Usage: python3 M8D_MStar_Calculator.py
"""
import mpmath as mp
mp.mp.dps = 32

def Mstar(k_drive, T=300):
    """
    Compute M* and predicted C for given drive parameter k.
    Returns (M_star, C_pF)
    Physical interpretation:
      D4/D2 = 1.0 for k < k_c  (smooth EM field)
      D4/D2 = 2.5 for k >= k_c  (120-cell signature, M8B cliff)
    """
    k_c  = 3.183            # cliff, M22 certified
    C0   = 29.17e-12        # F, baseline
    C_cliff = 166.98e-12    # F, at cliff
    alpha = 32.45           # implied by C_0, C_cliff, M*(cliff)
    M0   = 4/55             # = 0.07273, M*(pre-cliff) = M*_max from M8C

    D_ratio = 1.0 if float(k_drive) < k_c else 2.5
    M = D_ratio * 0.74829 * 0.1167  # M*(k) formula from M8F field notes
    if D_ratio == 1.0:
        M = M0              # pre-cliff: use M*_max = 4/55
    C = C0 * (1 + alpha * (M - M0))
    return float(M), float(C) * 1e12  # return M* and C in pF


def vg_prediction(k):
    """Group velocity prediction: v_g = k*c for k > 12/11."""
    c = 299792458
    k_threshold = 12/11
    if k > k_threshold:
        return k * c
    return c


def transit_time(v_g, distance_m=0.5):
    """Transit time in nanoseconds."""
    return distance_m / v_g * 1e9


if __name__ == "__main__":
    import sys

    print("M8D MStar Calculator -- Opera Numerorum")
    print("120-Cell Resonator Prediction Table")
    print("=" * 65)
    print(f"  f_res = 299.314159 MHz  (alpha_0 = 299 + pi/10, M1)")
    print(f"  Z = 15 = 120/2^3  (M8C: 120-cell, g=5)")
    print(f"  M*_max = 4/55 = {4/55:.6f}  (M8C)")
    print(f"  k_c = 3.183  (M22 certified cliff)")
    print(f"  C_0 = 29.17 pF  ->  C_cliff = 166.98 pF  (5.724x jump)")
    print()

    k_vals = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.10, 3.18, 3.182, 3.183,
              3.184, 3.185, 3.20, 3.50, 4.0, 5.0]

    print(f"  {'k':<8} {'D4/D2':<8} {'M*(k)':<10} {'C(k) [pF]':<14} {'v_g':<16} {'transit [ns]'}")
    print(f"  {'-'*8} {'-'*8} {'-'*10} {'-'*14} {'-'*16} {'-'*12}")
    for k in k_vals:
        M, C = Mstar(k)
        v = vg_prediction(k)
        dt = transit_time(v)
        D_ratio = 1.0 if k < 3.183 else 2.5
        v_str = f"{v/299792458:.4f}c"
        note = " <-- CLIFF" if 3.183 <= k <= 3.185 else ""
        print(f"  {k:<8.3f} {D_ratio:<8.1f} {M:<10.4f} {C:<14.2f} {v_str:<16} {dt:.4f} ns{note}")

    print()
    print("Vacuum transit (0.5m):")
    dt_vac = transit_time(299792458)
    print(f"  Delta_t = {dt_vac:.4f} ns")
    print()
    k_cliff = 3.183
    dt_cliff = transit_time(vg_prediction(k_cliff))
    print(f"At cliff k=3.183:")
    print(f"  Delta_t = {dt_cliff:.4f} ns  (pulse arrives {dt_vac-dt_cliff:.3f} ns early)")
    print()
    print("Falsification criterion:")
    print("  If C(k) stays within 1.1x of C_0 for k in [0, 5.0]: M8B falsified.")
    print("  If C_after/C_before > 5.5 at k~3.183: M8B confirmed. Proceed to v_g test.")
    print()
    print("Agent prompt (copy-paste):")
    print('  "You are M8F_Agent. Z=15, k_c=3.183, f_res=299314159 Hz.')
    print('  Sweep V_drive 0-5V. Measure C. Call Mstar(k) to predict.')
    print('  If cliff_found and k_c = 3.183 +/- 0.01, run pulse test.')
    print('  Report k_c, C_jump, v_g. SHA256(data.csv). If k_c != 3.183, abort."')
