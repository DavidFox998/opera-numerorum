#!/usr/bin/env python3
"""Generate the HONEST PDF_263 YM Tower Equation Report from verified sources.

Sources (all on disk, read-only):
  - BUILD_MANIFEST_v2.7.json   (per-brick file / open_prop / sha256 / collapse / axioms)
  - CLAY_STATUS.md, reports/CLAY_REPAIR_2026-06-03.md
No fabrication: every figure here is copied from those files or from a command
whose result is recorded in the report itself.
"""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "BUILD_MANIFEST_v2.7.json").read_text())


def esc(s: str) -> str:
    repl = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = []
    for ch in s:
        out.append(repl.get(ch, ch))
    return "".join(out)


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[a4paper,margin=2.4cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{fancyvrb}
\usepackage[hidelinks]{hyperref}
\usepackage{enumitem}
\setlength{\parskip}{0.5em}
\setlength{\parindent}{0pt}
\newcommand{\OPEN}{\textbf{\textsf{OPEN}}}
\title{\textbf{PDF\_263 --- Yang--Mills Tower Equation Report}\\[0.3em]
\large An Honest, Complete Audit of the YM/OS Witness-Collapse Bricks\\[0.2em]
\normalsize Theorema Aureum 143 (Volume I) --- Morning Star Project}
\author{D.\ Fox \ (ORCID 0009-0008-1290-6105)}
\date{2026-06-03 \quad\textbar\quad Mathlib v4.12.0}
\begin{document}
\maketitle
\thispagestyle{empty}

\begin{center}
\fbox{\parbox{0.92\textwidth}{\small
\textbf{HONESTY NOTICE (read first).}
This report makes \emph{no} claim that the Yang--Mills mass gap is proven,
that $\mu>0$, or that Clay ``Surface~\#1'' is closed. Every one of the 13
modules audited here is currently an \OPEN{} (named, \emph{unproven})
proposition. The axiom footprint is the classical trio
$\{\texttt{propext},\ \texttt{Classical.choice},\ \texttt{Quot.sound}\}$ ---
\emph{not} the empty set. There are no \texttt{sorry}/\texttt{sorryAx}/\texttt{admit}
\emph{proof-terms}. This is logical-hygiene bookkeeping; it proves nothing new.
Sections that earlier drafts requested but for which \emph{no artifact exists on
disk} (an ``LLM error / Z-protocol'' narrative and ``Besel~I'' test logs) are
documented as \textbf{absent} in \S\ref{sec:absent} rather than fabricated.
}}
\end{center}

\tableofcontents
\clearpage
"""

SEC1 = r"""\section{Equation statement --- the Yang--Mills mass-gap surface}
\label{sec:eq}

The Clay ``Yang--Mills existence and mass gap'' problem asks, for a compact
simple gauge group (here $SU(3)$), for a quantum Yang--Mills theory on
$\mathbb{R}^4$ whose Hamiltonian has a strictly positive spectral gap above the
vacuum. The chain of statements the YM/OS modules in this repository attempt to
encode is the following.

\paragraph{(E1) Exponential clustering (two-point decay).}
\[
\bigl|\,\langle W(C_1)\,W(C_2)\rangle - \langle W(C_1)\rangle\,\langle W(C_2)\rangle\,\bigr|
\;\le\; C\,e^{-\Delta\,\mathrm{dist}(C_1,C_2)},
\qquad \Delta>0 .
\]
\begin{itemize}[leftmargin=1.4em]
  \item $W(C)$ --- the Wilson loop observable on a closed contour $C$ (the
        gauge-invariant trace of the parallel transport around $C$).
  \item $\langle\cdot\rangle$ --- the (Euclidean) expectation in the lattice
        Yang--Mills measure.
  \item $\mathrm{dist}(C_1,C_2)$ --- the separation between the two loops.
  \item $\Delta>0$ --- the \emph{mass gap}: the rate of exponential decay of
        connected correlations. Strict positivity of $\Delta$ is the entire
        content of the problem.
  \item $C$ --- a finite positive constant.
\end{itemize}

\paragraph{(E2) Transfer-operator gap.}
Clustering at rate $\Delta$ is equivalent to a spectral gap of the Euclidean
transfer operator $T_{\mathrm{real}}$ acting on the physical Hilbert space:
\[
\operatorname{spec}\!\bigl(T_{\mathrm{real}}\big|_{\mathcal H_0}\bigr)\subseteq[0,\ \lambda_1],
\qquad
\lambda_1 \;=\; \bigl\|\,T_{\mathrm{real}}\big|_{\mathcal H_0}\bigr\| \;<\; 1,
\qquad
\Delta \;=\; -\log\lambda_1 \;>\;0 .
\]
\begin{itemize}[leftmargin=1.4em]
  \item $T_{\mathrm{real}}$ --- the genuine Wilson/heat-kernel transfer operator
        (one time-step Euclidean evolution).
  \item $\mathcal H_0$ --- the orthogonal complement of the vacuum (mean-zero
        sector).
  \item $\lambda_1$ --- the operator norm of $T_{\mathrm{real}}$ restricted to
        $\mathcal H_0$; the second-largest eigenvalue modulus.
  \item $\Delta=-\log\lambda_1$ --- the same mass gap as in (E1).
\end{itemize}

\paragraph{(E3) Mass gap from the gap bound.}
A self-adjoint $T$ on a Hilbert space $H$ has a mass gap $m$ when
\[
\langle x,\,T x\rangle_{\mathrm{re}} \;\ge\; (1-m)\,\|x\|^2
\quad\text{fails strictly on }\mathcal H_0,
\quad\text{equivalently}\quad
\lambda_1 \le e^{-m},\ \ m>0 .
\]
This is the predicate the repository calls \texttt{HasMassGap H T m}.

\paragraph{The honest gap.}
A \emph{non-vacuous} discharge of (E1)--(E3) requires a real $SU(3)$ Wilson
transfer operator with a strictly positive lower bound $T_{\mathrm{real}}>0$.
The ingredients --- $SU(3)$ character theory / a verified heat-kernel transfer
operator --- are \textbf{absent from mathlib v4.12.0}. Consequently
\textbf{no $T_{\mathrm{real}}>0$ is constructible in this repository}, and every
module below was discharged only at a \emph{degenerate witness} (a
\emph{witness collapse}): the correlator taken $\equiv 0$, the operator
$T:=0$ on $H:=\mathbb{C}$, or a reflexive definitional re-wrap. The recorded
$T_{\mathrm{real}}$ lower bound for all 13 modules is therefore \textbf{none}.
"""

SEC_DERIV_HEAD = r"""\clearpage
\section{Step-by-step audit --- every YM/OS witness-collapse brick}
\label{sec:deriv}

The table below lists all %d modules audited on the
\textbf{2026-06-03} repair pass. Each was previously registered as a ``brick''
(a landed result in \texttt{scripts/check-towers.sh}); each has now been
converted \emph{in place} from a proved \texttt{theorem}/\texttt{lemma} into a
named open proposition \verb|def <name>_OPEN : Prop := <fully-closed statement>|
and de-registered from the \texttt{BRICKS} array. Status for all: \OPEN{}
(witness-collapse), $T_{\mathrm{real}}$ bound = \textbf{none}.

{\small
\begin{longtable}{@{}r p{3.0cm} p{4.5cm} p{4.6cm}@{}}
\toprule
\# & File & Named open \texttt{Prop} & Witness collapse \\
\midrule
\endhead
""" 

SEC_DERIV_NOTES = r"""
\paragraph{Reading the columns.}
\textbf{WHAT} --- the file path and the named proposition (namespace
\texttt{TheoremaAureum.Towers.YM.OS}). \textbf{WHY} --- the proposition's role:
each is one link in the (E1)$\to$(E2)$\to$(E3) clustering/transfer/mass-gap
chain of \S\ref{sec:eq}. \textbf{WHERE} --- the $T_{\mathrm{real}}>0$ status:
\textbf{none} for all, because the proof discharges only at a degenerate
witness. \textbf{WHEN} --- the 2026-06-03 repair audit. The full per-file
SHA-256 hashes are in Appendix~\ref{sec:appendix}.
"""

# representative exact excerpts pulled from disk (verbatim, real source)
EXCERPTS = r"""\clearpage
\section{Representative Lean excerpts (verbatim) with English gloss}
\label{sec:excerpts}

These are exact, unedited excerpts of the converted source on disk. They
illustrate the three collapse shapes; the remaining ten modules collapse for
the analogous reasons recorded in \S\ref{sec:deriv}.

\subsection{Mass-gap inhabitedness (\texttt{MassGapStandin.lean})}
\begin{Verbatim}[fontsize=\small,frame=single]
def hasMassGapLowerBound (mu : R) : Prop :=
  exists C : R, 0 < C and 0 < mu

def massGap_standin_example_OPEN : Prop :=
  hasMassGapLowerBound 1
\end{Verbatim}
\textbf{Gloss.} The predicate asserts only ``there exist a positive constant
$C$ and a positive mass $\mu$.'' Witnessing it at $C=\mu=1$ says nothing about
any Yang--Mills correlator. As written the \texttt{\_OPEN} proposition is
trivially satisfiable. (ASCII rendering: \texttt{R}$=\mathbb R$,
\texttt{exists}$=\exists$, \texttt{and}$=\wedge$, \texttt{mu}$=\mu$.)

\subsection{Reflexive tail bound (\texttt{IntegratedTailReal.lean})}
\begin{Verbatim}[fontsize=\small,frame=single]
noncomputable def integrated_tail (L m : R) : R := rexp (-m * L)

def integrated_tail_le_exp_OPEN : Prop :=
  forall (L m : R), 0 <= m -> 0 <= L -> integrated_tail L m <= rexp (-m * L)
\end{Verbatim}
\textbf{Gloss.} Because \texttt{integrated\_tail L m} is \emph{defined} as
$e^{-mL}$, the ``bound'' unfolds to the reflexive $e^{-mL}\le e^{-mL}$ and
closes by \texttt{le\_refl}. The symbol does not refer to any heat-trace
integral; the genuine statement (a real heat-trace tail bounded by an
exponential) is unreachable here.

\subsection{Gap $\Rightarrow$ decay (\texttt{GapToDecay.lean})}
\begin{Verbatim}[fontsize=\small,frame=single]
def gap_to_decay_OPEN.{u} : Prop :=
  forall {H : Type u} [NormedAddCommGroup H] [InnerProductSpace C H] (m : R),
    0 < m -> m < 1 ->
    (exists T : H ->L[C] H, T != 0 and HasMassGap H T m) ->
      hasExponentialClustering (fun t => Real.exp (-m * t)) m
\end{Verbatim}
\textbf{Gloss.} The consequent is discharged by the obvious function
$f(t)=e^{-mt}$ (which trivially satisfies $|f(t)|\le 1\cdot e^{-mt}$) with the
spectral-gap hypothesis \emph{unused}. So the implication holds as written
without using its antecedent --- a witness collapse. It does not show a real
correlator decays from a real spectral gap.
"""


def build_table_rows() -> str:
    rows = []
    for i, m in enumerate(manifest["modules"], 1):
        f = esc(m["file"].split("Towers/")[-1])
        op = esc(m["open_prop"].split("OS.")[-1])
        coll = esc(m["collapse"])
        rows.append(f"{i} & \\texttt{{{f}}} & \\texttt{{{op}}} & {coll} \\\\")
    return "\n".join(rows) + "\n\\bottomrule\n\\end{longtable}}\n"


SEC_ABSENT = r"""\clearpage
\section{Requested sections with no artifact on disk (documented, not fabricated)}
\label{sec:absent}

Earlier drafts of this report requested an ``LLM Error Information: Z is a
Protocol'' section and a ``Besel~I concretization'' section, each to cite test
runs and a data file. The honesty rule of this project forbids presenting
unrecorded narrative or test results as data. The following were checked on
disk on 2026-06-03 and found \textbf{absent}:

\begin{itemize}[leftmargin=1.4em]
  \item \texttt{symmetry\_error\_rate.csv} --- \textbf{not present} anywhere in
        the workspace.
  \item \texttt{.local/Besel\_I/} (or any \texttt{*esel*} directory) ---
        \textbf{does not exist}.
  \item \texttt{/mnt/data/Report\_263.pdf} / \texttt{/mnt/data/PDF\_263\_*} ---
        \texttt{/mnt/data} \textbf{is not part of this workspace}
        (workspace root is \texttt{/home/runner/workspace}); no prior draft to
        merge exists.
\end{itemize}

There is no recorded ``Z-protocol'' study, ``phase-shift event'', ``Spark Muse''
observation, attributed quotation, or ``Besel~I'' test log in the repository.
Because none of these artifacts exists, these sections are \textbf{omitted}.
Stating their absence here is the honest treatment: the report leaves out no
\emph{true} implication, and fabricates none.
"""


def build_compliance() -> str:
    cls = ", ".join(esc(a) for a in manifest["classical_trio"])
    return r"""\clearpage
\section{Compliance certificate --- honest}
\label{sec:compliance}

\begin{longtable}{@{}p{6.2cm} p{8.5cm}@{}}
\toprule
Property & Verified value \\
\midrule
Modules audited & """ + str(len(manifest["modules"])) + r""" (all YM/OS) \\
Non-vacuous $T_{\mathrm{real}}>0$ proofs achieved & \textbf{0} \\
Converted to named open \texttt{Prop} & """ + str(manifest["converted_to_open_prop"]) + r""" \\
De-registered from \texttt{BRICKS} & """ + str(manifest["deregistered"]) + r""" \\
Axiom footprint (each module) & classical trio: \texttt{""" + cls + r"""} \\
\texttt{sorry} / \texttt{sorryAx} / \texttt{admit} \emph{proof-terms} & """ + \
        f"{manifest['sorry']} / {manifest['sorryAx']} / {manifest['admit']}" + r""" \\
Compile (direct-lean) & all EXIT 0 \\
Surface \#1 (global YM mass gap) & \OPEN{} \\
\bottomrule
\end{longtable}

\paragraph{Honest caveats on this certificate.}
\begin{enumerate}[leftmargin=1.5em]
  \item \textbf{The axiom footprint is the classical trio, not the empty set.}
        Each \texttt{\_OPEN} proposition references mathlib
        (\texttt{Measure}/\texttt{inner}/\texttt{Real.exp}), which pulls in
        $\{\texttt{propext},\ \texttt{Classical.choice},\ \texttt{Quot.sound}\}$.
        ``No axiom'' would be \emph{false}; ``no \emph{research-grade} axiom
        beyond the trio'' is the true statement.
  \item \textbf{A literal grep is \emph{not} empty.} The strings
        \texttt{sorry}, \texttt{admit}, and \texttt{axiom} occur in the CLAY
        OPEN docstrings of these files (and across the wider tree --- 140 files
        contain at least one of those strings). The honest signal is therefore
        the \emph{proof-term} count (0) plus \texttt{\#print axioms} (trio only),
        \textbf{not} an empty grep.
  \item \textbf{\texttt{lake build} was not run.} The vendored mathlib
        \texttt{v4.12.0} tag is unresolved, so any \texttt{lake}/\texttt{lake env}
        invocation would re-fetch from remote and wipe the oleans. Verification
        used the documented direct-lean bypass (Appendix~\ref{sec:appendix}). No
        ``\texttt{lake build} exits 0'' claim is made.
  \item \textbf{The \texttt{\_OPEN} propositions are trivially satisfiable as
        written.} The degenerate witnesses remain available, so each
        \texttt{\_OPEN} \texttt{Prop} \emph{names} the as-written shape but does
        \textbf{not} assert the genuine YM surface. The conversion removes a
        vacuous landed \emph{theorem}; it manufactures nothing.
\end{enumerate}

\paragraph{Status of the other towers (no per-brick claim made here).}
This report audits the 13 YM/OS modules only. For the record, and per the
project's locked invariants: the YM and Navier--Stokes towers remain
\texttt{Status: Open} at their Clay surfaces (YM Surface~\#1 open; NS Surfaces
\#1/\#2 open, NS frozen); the RH fragment in \texttt{Towers/RH/} is a
\emph{conditional reduction} over two undischarged open hypotheses, not a proof
of the Riemann Hypothesis. No tower in this repository closes a Clay problem.
"""


def build_appendix() -> str:
    rows = []
    for i, m in enumerate(manifest["modules"], 1):
        f = esc(m["file"].split("Towers/")[-1])
        sha = m["sha256"]
        rows.append(f"{i} & \\texttt{{{f}}} & \\texttt{{{sha}}} \\\\")
    body = "\n".join(rows)
    return r"""\clearpage
\section{Appendix --- provenance and verification method}
\label{sec:appendix}

\paragraph{Verification method (verbatim from the build manifest).}
\begin{itemize}[leftmargin=1.4em]
  \item Method: \texttt{""" + esc(manifest["verification"]["method"]) + r"""}.
  \item Reason: """ + esc(manifest["verification"]["reason"]) + r""".
  \item Axiom check: """ + esc(manifest["verification"]["axiom_check"]) + r""".
  \item All EXIT 0: """ + str(manifest["verification"]["all_exit_0"]) + r"""; all trio-only: """ + \
        str(manifest["verification"]["all_trio_only"]) + r""".
\end{itemize}

\paragraph{Per-file SHA-256 (full).}
{\footnotesize
\begin{longtable}{@{}r p{4.2cm} p{9.3cm}@{}}
\toprule
\# & File (under \texttt{Towers/}) & SHA-256 \\
\midrule
\endhead
""" + body + r"""
\bottomrule
\end{longtable}}

\paragraph{Source documents.} \texttt{BUILD\_MANIFEST\_v2.7.json},
\texttt{CLAY\_STATUS.md}, \texttt{reports/CLAY\_REPAIR\_2026-06-03.md},
\texttt{provenance/clay\_repair.diff}. This PDF was generated by
\texttt{reports/build\_pdf263.py} directly from those files; every numeric value
above is copied from them or from a command whose result is stated in the body.

\vfill
\begin{center}\small
Generated """ + datetime.date.today().isoformat() + r""" --- honesty-locked.
No mass-gap / $\mu>0$ / Surface-\#1-closed claim is made.
\end{center}
\end{document}
"""


def main():
    tex = (
        PREAMBLE + SEC1
        + (SEC_DERIV_HEAD % len(manifest["modules"]))
        + build_table_rows()
        + SEC_DERIV_NOTES
        + EXCERPTS
        + SEC_ABSENT
        + build_compliance()
        + build_appendix()
    )
    out = ROOT / "reports" / "PDF_263_YM_Tower_Equation_Honest.tex"
    out.write_text(tex)
    print("wrote", out, len(tex), "bytes")


if __name__ == "__main__":
    main()
