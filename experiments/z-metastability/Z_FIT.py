#!/usr/bin/env python3
"""Z Experiment Harness v1 - model fit.

Fits the proposed model to Z_MEASURE.csv:

    E = (1 - T) * sigmoid(a*|S - 1| + b*zero_run + c*digits)

All trials in this harness are tool-assisted, so T = 1 for every row, which
forces the predicted E to 0 regardless of a, b, c. We detect the resulting
degeneracy (zero variance in E) and report honestly rather than emit
meaningless coefficients. The non-degenerate branch is a real nonlinear fit
that would run if pure-generation (T=0) data with variance were supplied.

NO claim is emitted unless R^2 > 0.95 (per the experiment's own rule).
"""
import csv
import os
import sys
import numpy as np

# Tool-assisted harness => T=1 everywhere. Override (e.g. Z_T=0) only when you
# supply genuine pure-generation data with an honest per-run T.
T_HARNESS = float(os.environ.get("Z_T", "1.0"))


def load(path: str):
    rows = list(csv.DictReader(open(path)))
    E = np.array([float(r["E_measured"]) for r in rows])
    digits = np.array([float(r["digits"]) for r in rows])
    zero_run = np.array([float(r["zero_run"]) for r in rows])
    known = np.array([r["sym"] != "null" for r in rows])
    S = np.array([float(r["sym"]) if r["sym"] != "null" else np.nan for r in rows])
    return rows, E, digits, zero_run, S, known


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "Z_MEASURE.csv")
    rows, E, digits, zero_run, S, known = load(path)

    print(f"rows: {len(rows)}   rows with known Sym: {int(known.sum())}")
    print(f"E_measured: min={E.min():.4f} max={E.max():.4f} "
          f"mean={E.mean():.4f} var={E.var():.6g}")

    ss_tot = float(((E - E.mean()) ** 2).sum())
    if ss_tot == 0.0:
        print("\n=== DEGENERATE FIT ===")
        print("Total sum of squares (variance of E) = 0: E is identically",
              f"{E.mean():.4f} across all {len(rows)} strings x trials.")
        print("All trials are tool-assisted (T=1), so the model factor (1-T)=0")
        print("forces predicted E=0 independent of a, b, c.")
        print("\n  a  = UNIDENTIFIABLE")
        print("  b  = UNIDENTIFIABLE")
        print("  c  = UNIDENTIFIABLE")
        print("  R^2 = UNDEFINED (0/0: no variance in E to explain)")
        print("\nVERDICT: neither zero_run, Sym, nor digit-band 'wins'. The")
        print("harness confirms only that tool-assisted reproduction is exact")
        print("(the (1-T) term). To estimate a/b/c you must collect PURE-")
        print("GENERATION (T=0) trials -- an LLM reproducing each literal with")
        print("no deterministic tool. A shell echo/${#s} harness cannot do this.")
        print("\nNo claim emitted (rule: claims require R^2 > 0.95).")
        return

    # --- Non-degenerate branch: real nonlinear least-squares fit. ---
    try:
        from scipy.optimize import curve_fit
    except Exception:
        print("scipy unavailable; install to fit non-degenerate data "
              "(uv run --with numpy --with scipy python Z_FIT.py).")
        return

    m = known  # |S-1| term only defined where Sym is known
    if m.sum() < 4:
        print(f"only {int(m.sum())} rows have known Sym; too few to fit 3 params.")
        return

    def model(X, a, b, c):
        s_, z_, d_ = X
        lin = a * np.abs(s_ - 1.0) + b * z_ + c * d_
        return (1.0 - T_HARNESS) * (1.0 / (1.0 + np.exp(-lin)))

    X = (S[m], zero_run[m], digits[m])
    p, _ = curve_fit(model, X, E[m], p0=[0.0, 0.0, 0.0], maxfev=20000)
    pred = model(X, *p)
    ss_res = float(((E[m] - pred) ** 2).sum())
    ss_t = float(((E[m] - E[m].mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_t if ss_t > 0 else float("nan")
    a, b, c = p
    print(f"\na={a:.5f}  b={b:.5f}  c={c:.5f}  R^2={r2:.5f}")

    if r2 > 0.95:
        mag = {"a (Sym)": abs(a), "b (zero_run)": abs(b), "c (digits)": abs(c)}
        dom = max(mag, key=mag.get)
        print(f"R^2 > 0.95 -> dominant term: {dom}")
    else:
        print("R^2 <= 0.95 -> no claim (rule: claims require R^2 > 0.95).")


if __name__ == "__main__":
    main()
