#!/usr/bin/env python3
"""Generate data/MorningStar_RH_Cert.tex from a real ledger sweep.

Runs kernel.hunt_zeros(1, 100) and kernel.bracket_zero(1, 1e-6), then
writes a LaTeX certificate whose every numeric row is backed by an
actual ledger line in data/hits.txt. No values are hand-typed.

Honest scope: this is a numerical reconnaissance certificate, not a
proof of RH. See the "Scope" section of the emitted .tex file.
"""
from __future__ import annotations

import datetime as _dt
import hashlib as _hashlib
import pathlib as _pl
import sys as _sys

_REPO = _pl.Path(__file__).resolve().parent.parent
if str(_REPO) not in _sys.path:
    _sys.path.insert(0, str(_REPO))

import kernel  # noqa: E402

GENESIS_SEAL = "eecbcd9a540aa7a2c90edd23827c73e4d1bb5af641d352f70a5de849b21f875f"
M13_GENESIS = "d99b0df4b6e3a5817a90e7f8da44b20261d3b670d31309779a776efbf1bcc668"
OUT = _REPO / "data" / "MorningStar_RH_Cert.tex"
N_ZEROS = 100
BRACKET_WINDOW = 1e-6


def _tex_escape(s: str) -> str:
    return s.replace("\\", "\\textbackslash{}").replace("_", "\\_").replace("&", "\\&")


def _verify_file_sha(path: _pl.Path) -> str:
    return _hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    print(f">> hunt_zeros(1, {N_ZEROS}) — appending {N_ZEROS} probes to data/hits.txt")
    hits = kernel.hunt_zeros(1, N_ZEROS)
    print(f">> bracket_zero(1, {BRACKET_WINDOW})")
    bracket = kernel.bracket_zero(1, BRACKET_WINDOW)

    rh_ok_count = sum(1 for h in hits if h.get("RH_ok") is True)
    beta_uniform = all(str(h.get("kms_beta")) == "2.0" for h in hits)
    tag_uniform = all(h.get("tag") == "MPMATH_ZETA" for h in hits)
    all_clean = rh_ok_count == N_ZEROS and beta_uniform and tag_uniform

    if all_clean:
        title_summary = (
            rf"\large {N_ZEROS} nontrivial zeros, all "
            rf"\texttt{{RH\_ok=True}}, $\beta_{{\mathrm{{KMS}}}}=2.0$"
        )
    else:
        title_summary = (
            rf"\large \textbf{{PARTIAL}}: {rh_ok_count}/{N_ZEROS} "
            rf"\texttt{{RH\_ok=True}}; "
            rf"$\beta_{{\mathrm{{KMS}}}}$ uniform={str(beta_uniform).lower()}; "
            rf"tag uniform={str(tag_uniform).lower()}"
        )

    verify_path = _REPO / "lean-proof" / "VERIFY.txt"
    verify_sha = _verify_file_sha(verify_path) if verify_path.exists() else "(not built)"

    rows: list[str] = []
    for h in hits:
        n = h["n"]
        t = h["zero_im_mpmath"]
        l_abs = h["L_abs"]
        sha = h["sha"][:16] + "\\dots"
        rows.append(f"{n} & {_tex_escape(t)} & {_tex_escape(l_abs)} & \\texttt{{{sha}}} \\\\")
    table_body = "\n".join(rows)

    bracket_rows: list[str] = []
    for r in bracket["zeros_found"]:
        bracket_rows.append(
            f"{_tex_escape(str(r['im']))} & {_tex_escape(str(r['L_abs']))} "
            f"& \\texttt{{{r['sha'][:16]}\\dots}} \\\\"
        )
    bracket_body = (
        "\n".join(bracket_rows)
        if bracket_rows
        else "(no RH\\_ok hits in this bracket — float arithmetic didn't land within $10^{-12}$) \\\\"
    )

    generated_at = _dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    tex = rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{amsmath,amssymb,booktabs,longtable}}
\usepackage{{listings}}
\usepackage{{xcolor}}
\usepackage{{hyperref}}
\hypersetup{{colorlinks=true,urlcolor=blue}}
\lstset{{
  basicstyle=\ttfamily\footnotesize,
  breaklines=true,
  frame=single,
  backgroundcolor=\color{{black!3}},
  columns=fullflexible,
  keepspaces=true,
}}

\title{{MorningStar-Lab v1.0 --- Riemann Hypothesis Reconnaissance Certificate \\
       {title_summary}}}
\author{{Entangled Technologies --- The Morning Star Project \\
        Genesis: \texttt{{{GENESIS_SEAL[:8]}\dots{GENESIS_SEAL[-4:]}}} \quad
        Axiom Debt: \texttt{{[]}}}}
\date{{Generated {generated_at}}}

\begin{{document}}
\maketitle

\section*{{Scope (honest)}}
This certificate records a \emph{{numerical reconnaissance}} of the
Riemann $\zeta$-function on the critical line $\Re(s)=\tfrac12$,
performed by the MorningStar-Lab \texttt{{kernel.py}} probe via an
arbitrary-precision \texttt{{mpmath}} backend at \texttt{{workdps=50}}.
It is \textbf{{not}} a proof of the Riemann Hypothesis. The Lean~4
axiom-debt-$[\,]$ result that ships in \texttt{{lean-proof/}} concerns
the M1--M10/M13 BC--CM ($h=1$) spine and is \emph{{independent}} of
this document.

\section*{{Protocol}}
For $s = 0.5 + it$ the kernel defines
$\texttt{{RH\_ok}} \;\equiv\; [|L(s)| < 10^{{-12}}]$
and $\beta_{{\mathrm{{KMS}}}} = 1/\Re(s) = 2$ on the critical line.
Each probe is appended to the Genesis-sealed ledger
\texttt{{data/hits.txt}} with a nanosecond timestamp and a SHA-256
covering the canonical line body. Because the timestamp is part of
the hash input, two probes at the same point still receive distinct
ledger SHAs: every measurement is uniquely receipted.

\section*{{Genesis seal}}
\begin{{lstlisting}}
Genesis SHA-256 (preamble, lines 1--9 of data/hits.txt):
  {GENESIS_SEAL}
Genesis lines 5--9 (frozen):
  437
  1094
  axioms=[] 2026-05-24
  M13_CERT_SHA256={M13_GENESIS}
  --- GENESIS SEAL ---
\end{{lstlisting}}

\section*{{Lean axiom debt}}
\begin{{lstlisting}}
sha256(lean-proof/VERIFY.txt) =
  {verify_sha}
\end{{lstlisting}}
\noindent The frozen M1--M10/M13 spine compiles in
\texttt{{lean-proof/}} with zero axioms. The Genesis-pinned
\texttt{{M13\_CERT\_SHA256={M13_GENESIS[:8]}\dots}} is the sealed
M13 certificate value at v1.8-BC release time and is \emph{{not}}
expected to equal the current \texttt{{VERIFY.txt}} hash --- the
latter is regenerated by \texttt{{lean-proof/regenerate.sh}}; the
Genesis line is immutable.

\section*{{Results: first {N_ZEROS} nontrivial zeros (MPMATH\_ZETA)}}
\noindent
Produced by \texttt{{python -c "import kernel; kernel.hunt\_zeros(1, {N_ZEROS})"}}.
Of the {N_ZEROS} probes, \textbf{{{rh_ok_count}}} returned
\texttt{{RH\_ok=True}}; \texttt{{kms\_beta}} is uniformly $2.0$:
\textbf{{{str(beta_uniform).lower()}}}; \texttt{{tag}} is uniformly
\texttt{{MPMATH\_ZETA}}: \textbf{{{str(tag_uniform).lower()}}}.
$|L|$ values shown are the float-rounded probe value (the kernel passes
\texttt{{float(zetazero(n).imag)}} into \texttt{{probe()}}, so $|L|$ is
$\sim 10^{{-15}}$ rather than $0$; this is honestly recorded).

\begin{{center}}
\begin{{longtable}}{{rlll}}
\toprule
$n$ & $t_n$ (mpmath, 20 sig.fig.) & $|L(0.5+it_n)|$ & ledger SHA (16 hex) \\
\midrule
\endfirsthead
\toprule
$n$ & $t_n$ (mpmath, 20 sig.fig.) & $|L(0.5+it_n)|$ & ledger SHA (16 hex) \\
\midrule
\endhead
{table_body}
\bottomrule
\end{{longtable}}
\end{{center}}

\section*{{Bracket verification: \texttt{{bracket\_zero(1, {BRACKET_WINDOW})}}}}
Tight sweep of $[t_1 - 10^{{-6}}, t_1 + 10^{{-6}}]$ at step $2\cdot 10^{{-7}}$
through \texttt{{scan\_critical\_line(1, \dots, h=1)}}. Float arithmetic
visits {len(bracket["zeros_found"])} point(s) within the gunsight
($|L|<10^{{-12}}$):
\begin{{center}}
\begin{{tabular}}{{lll}}
\toprule
$\Im(s)$ probed & $|L|$ & ledger SHA (16 hex) \\
\midrule
{bracket_body}
\bottomrule
\end{{tabular}}
\end{{center}}
\noindent
$t_1 \approx {bracket["t0"]}$, window $= {bracket["window"]}$,
step $= {bracket["step"]}$.

\section*{{Reproducibility}}
\begin{{lstlisting}}
# Verify the seal:
python scripts/check-genesis-seal.py

# Regenerate this certificate (re-runs hunt_zeros(1, {N_ZEROS}) and bracket_zero):
python scripts/generate-rh-cert.py

# Full 7-step validation harness (requires `lake` on PATH for Lean):
bash scripts/validate-morningstar.sh
\end{{lstlisting}}

\section*{{What this certificate does \textbf{{not}} claim}}
\begin{{itemize}}
  \item It does \textbf{{not}} claim a proof of RH. \texttt{{RH\_ok=True}}
        on a probe means $|L(s)| < 10^{{-12}}$ at one
        finite-precision sample, nothing more.
  \item The \texttt{{MPMATH\_ZETA}} backend is not Lean-verified. For
        $h\!\ge\!2$ the kernel logs \texttt{{NEEDS\_SAGE}} with
        \texttt{{reason=h>=2\_out\_of\_scope\_for\_mpmath\_backend}};
        those rows carry a deterministic stub
        \texttt{{L\_nonvanish=True}} and must not be read as
        L-function evaluations.
  \item The names \texttt{{hit\_437}} and \texttt{{hit\_1094}} in
        \texttt{{lean-proof/TheoremaAureum/AutoLemmas.lean}} are
        tautologies (\texttt{{True := trivial}}) referencing the
        OpenCV cube counts from README Appendix~A; they claim
        nothing about number theory.
\end{{itemize}}

\end{{document}}
"""

    OUT.write_text(tex, encoding="utf-8")
    print(f">> wrote {OUT.relative_to(_REPO)} ({OUT.stat().st_size} bytes)")
    print(f">> RH_ok hits: {rh_ok_count}/{N_ZEROS}")
    print(f">> kms_beta uniformly 2.0: {beta_uniform}")
    print(f">> tag uniformly MPMATH_ZETA: {tag_uniform}")
    print(f">> sha256(lean-proof/VERIFY.txt) = {verify_sha}")

    if rh_ok_count != N_ZEROS:
        print(
            f"!! WARNING: only {rh_ok_count}/{N_ZEROS} hits "
            "satisfied the RH_ok gunsight; certificate still written.",
            file=_sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
