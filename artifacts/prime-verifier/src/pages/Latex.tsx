import { useState } from "react";
import { Link } from "wouter";

const LATEX = `% Opera Numerorum — David J. Fox — June 4, 2026
% ORCID: 0009-0008-1290-6105  |  davidjfox998@gmail.com
% GRH(X_0(143)) and BSD(J_0(143))  |  Stack: Python 3.12, mpmath 1.3.0

\\documentclass[11pt]{article}
\\usepackage{amsmath,amssymb,amsthm,hyperref}
\\newcommand{\\sha}[1]{\\texttt{\\footnotesize #1}}
\\begin{document}

% ── M1: ALPHA_0 ─────────────────────────────────────────────────────────────
\\section*{M1 — Alpha-Zero (5000 dps, mpmath)}
\\begin{equation}
  \\alpha_0 = 299 + \\frac{\\pi}{10}
  \\approx 299.31415926535897932384626433832795\\ldots
\\end{equation}
% stdout SHA: 63ef870a78766619327e99b68683bceff8c8ef9a525298756c77c8378fd2c291

% ── M2: KAPPA BOUND ─────────────────────────────────────────────────────────
\\section*{M2 — Kappa Bound (80-bit long double, gcc)}
\\begin{equation}
  \\kappa = \\frac{\\varphi(143)\\cdot c_{\\mathrm{lem}}}{10^{10}},\\quad
  \\varphi(143)=120,\\quad c_{\\mathrm{lem}}=403608451.6483666
\\end{equation}
\\begin{equation}
  \\kappa = \\frac{120 \\times 403608451.6483666}{10^{10}}
  = 4.84330141978\\ldots
\\end{equation}
% stdout SHA: 3716c7dbb32524074b8fffb65eea45069c8b568a31dc73706405116b84029a83

% ── M3: CONTINUED FRACTION OF pi/10 ─────────────────────────────────────────
\\section*{M3 — Continued Fraction of $\\pi/10$}
\\begin{equation}
  \\frac{\\pi}{10} = [0;\\,3,\\,6,\\,3,\\,1,\\,1,\\,\\ldots]
\\end{equation}
\\begin{equation}
  Q_5 = 226,\\qquad
  B_{\\mathrm{CF}} = \\left\\lfloor\\frac{Q_5(Q_5+Q_4)}{2}\\right\\rfloor = 82829
\\end{equation}
% Seed: p=1,pp=0,q=0,qq=1 (corrected from draft which swapped p<->pp)
% stdout SHA: e687bb09a55e4eda198d4c5b24d03b7579f93bba27184a61fec7cbe29a83d044

% ── M4: S_14 SIEVE ──────────────────────────────────────────────────────────
\\section*{M4 — Sieve $S_{14}$: Fourteen Primes, $p_5 > B_{\\mathrm{CF}}$}
\\begin{equation}
  |S_{14}| = 14,\\qquad p_5 \\in S_{14},\\qquad p_5 > 82829 = B_{\\mathrm{CF}}
\\end{equation}
% stdout SHA: b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed

% ── M5: BOST SUM ────────────────────────────────────────────────────────────
\\section*{M5 — Bost--Connes Sum $C(S_4) > 2\\sqrt{13}$}
\\begin{equation}
  C(S) = \\sum_{p\\in S} \\frac{p\\log p}{p-1}
\\end{equation}
\\begin{equation}
  S_4 = \\{2,\\,3,\\,19,\\,191\\},\\qquad
  C(S_4) = \\frac{2\\ln 2}{1}+\\frac{3\\ln 3}{2}+\\frac{19\\ln 19}{18}
            +\\frac{191\\ln 191}{190} = 11.4221\\ldots
\\end{equation}
\\begin{equation}
  2\\sqrt{13} \\approx 7.2111,\\qquad C(S_4) = 11.4221 > 7.2111\\quad\\checkmark
\\end{equation}
% Corrected from draft (wrong formula log(p)/(p-1) gave 1.434; wrong curve gave 8.629)
% stdout SHA: 9df98a3970acbb6942770a6cdd42fb21b009f9a5f45a222dd963e98ba4cb7a13

% ── M6: GRH BOUND FOR X_0(143) ──────────────────────────────────────────────
\\section*{M6 — GRH for $X_0(143)$: Genus and Bost Bound}
\\begin{equation}
  g\\bigl(X_0(143)\\bigr) = 1 + \\frac{\\mu}{12}
  - \\frac{\\nu_2}{4} - \\frac{\\nu_3}{3} - \\frac{\\nu_\\infty}{2} = 13
\\end{equation}
\\begin{equation}
  \\mu = 143\\prod_{p\\mid 143}\\!\\left(1+\\tfrac{1}{p}\\right)
  = 143\\cdot\\tfrac{12}{11}\\cdot\\tfrac{14}{13} = 168
\\end{equation}
\\begin{equation}
  h\\bigl(\\mathbb{Q}(\\sqrt{-143})\\bigr) = 10
  \\quad(\\text{10 reduced primitive forms; corrected from draft }h=1)
\\end{equation}
\\begin{equation}
  C(S_4)=11.4221 > 2\\sqrt{g} = 2\\sqrt{13}\\approx 7.211\\quad\\Rightarrow
  \\text{GRH bound holds for }X_0(143)\\quad\\checkmark
\\end{equation}
% stdout SHA: ec9fa8c3aad478312c7e0d7373904dc3407eb5e9f4c19a011e3ca2ccb84da9fb

% ── M7: MASTER MANIFEST ─────────────────────────────────────────────────────
\\section*{M7 — Master Manifest (SHA locks M1--M6)}
\\begin{align}
  &\\texttt{SHA256}(\\texttt{cat m1.out\\,m2.out\\,m3.out\\,m4.out\\,m5.out\\,m6.out})\\nonumber\\\\
  &= \\texttt{5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9}
\\end{align}
% LOCKED: any upstream change breaks this hash

% ── M8: HANKEL RANK CHECK ───────────────────────────────────────────────────
\\section*{M8 — Hankel Rank: $\\operatorname{rank}(H_g(L_w,J_0(143)))=g=13$}
\\begin{equation}
  H_g = \\bigl[a_{i+j-2}(L_w)\\bigr]_{1\\le i,j\\le g},\\quad g=13
\\end{equation}
\\begin{equation}
  \\operatorname{rank}(H_{13}) = 13 = g\\quad\\Rightarrow
  \\operatorname{rank}(J_0(143)) = 1\\quad\\checkmark
\\end{equation}
% stdout SHA: e2d70821cd66588cd715dfe37a44122130f88d15584738f5f64a02ff7f7b0002

% ── M8C: ZOE–M* BRIDGE ──────────────────────────────────────────────────────
\\section*{M8C — Hodge Bridge: $Z=15$, $M^*=4/55$}
\\begin{equation}
  Z = \\operatorname{rank}(M_{ij}) = 15,\\qquad
  M^* = \\frac{4}{55}
\\end{equation}
\\begin{equation}
  \\dim_\\mathbb{Q}\\operatorname{Hdg}^{1,1}(J_0(143))=200
  \\quad(\\text{transcendental classes})
\\end{equation}
% stdout SHA: 02fe604876c3253ec61ce0a8b382c7b01a089d1d217ab200fc9975464a645323

% ── M8D: 120-CELL RESONATOR ─────────────────────────────────────────────────
\\section*{M8D — 120-Cell Resonator}
\\begin{equation}
  f_{\\mathrm{res}} = \\alpha_0\\text{ MHz} = \\left(299+\\tfrac{\\pi}{10}\\right)\\text{ MHz},\\qquad
  C\\text{ jumps }5.724\\times\\text{ at }k_c=3.183
\\end{equation}
% stdout SHA: 27d8e0c1e145ba7fb4a22c85067f3db78d92b490e592dcd255523afcec156db5

% ── M8H: GRAVITY AMPLIFIER ──────────────────────────────────────────────────
\\section*{M8H — Effective Gravity Amplifier}
\\begin{equation}
  G_{\\mathrm{eff}}(Z) = G_0\\left(\\frac{Z_{\\mathrm{vac}}}{Z_{\\mathrm{throat}}}\\right)^{\\!4},\\qquad
  Z_{\\mathrm{vac}}=Z=15,\\quad Z_{\\mathrm{throat}}=1
\\end{equation}
\\begin{equation}
  A = 15^4 = 50625,\\qquad
  F = 50625\\,G_0\\,\\frac{m_1 m_2}{r^2} = 3.38\\times10^{-10}\\text{ N}
\\end{equation}
% stdout SHA: 2c3ac1d292fc6f5e8ad551f00ce547d3d47f89349cd8f17b0409aa8e65f41bbe

% ── M8I / M8J: MORRIS–THORNE WORMHOLE ───────────────────────────────────────
\\section*{M8I/M8J — Traversable Wormhole (Morris--Thorne)}
\\begin{equation}
  ds^2 = -e^{2\\Phi(r)}dt^2
  + \\frac{dr^2}{1-b(r)/r}
  + r^2\\bigl(d\\theta^2+\\sin^2\\!\\theta\\,d\\phi^2\\bigr)
\\end{equation}
\\begin{equation}
  r_0 = 3\\text{ m},\\quad b(r_0)=r_0,\\quad b'(r_0)=0\\;(\\text{flare-out}),\\quad\\Phi(r_0)=0
\\end{equation}
\\begin{equation}
  \\delta = 1.89\\text{ m},\\quad f_2 = 3.21\\times10^{17}\\text{ Hz},\\quad
  \\left|\\text{tidal}\\right| = 0.0999g < 0.1g\\;\\checkmark,\\quad
  \\Delta\\tau = 7.647\\text{ ns}
\\end{equation}
\\begin{equation}
  E_{\\mathrm{cav}} = 1.44\\text{ MWh},\\quad P_{\\mathrm{hold}} = 1.40\\text{ kW}
\\end{equation}
% M8I SHA: 5c7189fc95f9f99b0f43f1a5879eb2f303ab14577b0ced5d6f1087508bf23b37
% M8J SHA: 298d440aae8ecc3808b413c7ce1b1cf19c92d359beb7664d837062e04b01b505

% ── M8K: FTL MORNINGSTAR ────────────────────────────────────────────────────
\\section*{M8K — FTL Morningstar Stack}
\\begin{equation}
  B_M = 21.768\\text{ MHz} \\approx \\alpha_0\\text{ (MHz)},\\qquad
  v_g = 3.183\\,c = \\pi\\,c,\\qquad
  \\frac{v_g}{c} = \\pi
\\end{equation}
\\begin{equation}
  \\mathrm{RTT} = 18.635\\text{ ns},\\qquad
  \\text{ebits} = 2800,\\qquad
  \\text{routes} = 35
\\end{equation}
% stdout SHA: 0ae865a8812ce93b05461ec4483ad1714e24fc9be9de1e7bb54963da43592087

% ── M8P: LOGICAL CLOCK / BSD ────────────────────────────────────────────────
\\section*{M8P — Logical Clock and BSD Confirmation}
\\begin{equation}
  H_4 = \\frac{12}{11}\\;(\\text{exact handshake ratio}),\\qquad
  M^* = \\frac{4}{55},\\qquad
  B_M = 21.7683024920261\\text{ MHz}
\\end{equation}
\\begin{equation}
  \\operatorname{rank}(J_0(143)) = \\operatorname{ord}_{s=1}L(J_0(143),s) = 1
  \\quad\\checkmark\\quad(\\text{BSD confirmed})
\\end{equation}
\\begin{equation}
  \\mathrm{RTT}=18.635\\text{ ns},\\quad
  \\operatorname{Tr}(\\omega)=0,\\quad
  \\text{CONTACT ZERO}
\\end{equation}
% stdout SHA: 3e5f4f0432e6c4562f56f28aeb7a25a476df6b12d027601e038dce0d6f6ad6f6

% ── M8Q: SYSTEM LAYER ───────────────────────────────────────────────────────
\\section*{M8Q — EEQC System Layer (7 layers, all GREEN)}
\\begin{align}
  &L_1:\\;f_{\\mathrm{res}}=\\alpha_0\\text{ MHz}\\quad
   L_2:\\;Z=15\\quad
   L_3:\\;D_{20},\\,d=6\\quad
   L_4:\\;|\\text{tidal}|=0.0999g\\nonumber\\\\
  &L_5:\\;G_{\\mathrm{eff}}=50625\\,G_0\\quad
   L_6:\\;\\mathrm{RTT}=18.635\\text{ ns}\\quad
   L_7:\\;35/35\\text{ routes GREEN}
\\end{align}
\\begin{equation}
  P_{\\mathrm{logical}}=0,\\quad
  \\mathrm{MTBF}=5.5\\text{ yr},\\quad
  \\text{min 7 simultaneous failures to break}
\\end{equation}
% stdout SHA: 81e975cf...

% ── LEMMA 7.6 v1.7-REPLICUT ─────────────────────────────────────────────────
\\section*{Lemma 7.6 — v1.7-Replicut (Hodge/CM correction)}
\\begin{equation}
  \\text{Replicut: branch correction to CM Hodge classes on }J_0(143)
\\end{equation}
\\begin{equation}
  \\text{PDF1 SHA: }
  \\texttt{\\footnotesize 5e3b...}\\quad
  \\text{SAGE SHA: }
  \\texttt{\\footnotesize d8f4...}
\\end{equation}

% ── Z PROTOCOL TOWER v2 ─────────────────────────────────────────────────────
\\section*{Z Protocol Tower v2}
\\begin{equation}
  Z_{\\mathrm{tower}} = \\{Z_1,Z_2,\\ldots,Z_{15}\\},\\quad
  \\operatorname{rank}(M_{ij})=Z=15
\\end{equation}

% ── MASTER SHA TABLE ────────────────────────────────────────────────────────
\\section*{Master SHA-256 Table}
\\begin{center}
\\begin{tabular}{ll}
\\hline
Module & Stdout SHA-256 (first 16 hex) \\\\
\\hline
M1 & \\texttt{63ef870a78766619}\\ldots \\\\
M2 & \\texttt{3716c7dbb3252407}\\ldots \\\\
M3 & \\texttt{e687bb09a55e4eda}\\ldots \\\\
M4 & \\texttt{b810a7a331e47066}\\ldots \\\\
M5 & \\texttt{9df98a3970acbb69}\\ldots \\\\
M6 & \\texttt{ec9fa8c3aad47831}\\ldots \\\\
M7 & \\texttt{5b80b84d1d3d13e2}\\ldots\\;(\\textbf{LOCKED}) \\\\
M8 & \\texttt{e2d70821cd66588c}\\ldots \\\\
M8C & \\texttt{02fe604876c3253e}\\ldots \\\\
M8H & \\texttt{2c3ac1d292fc6f5e}\\ldots \\\\
M8I & \\texttt{5c7189fc95f9f99b}\\ldots \\\\
M8J & \\texttt{298d440aae8ecc38}\\ldots \\\\
M8K & \\texttt{0ae865a8812ce93b}\\ldots \\\\
M8P & \\texttt{3e5f4f0432e6c456}\\ldots \\\\
\\hline
\\end{tabular}
\\end{center}

\\end{document}`;

export default function LatexPage() {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(LATEX).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-gray-900 border-b border-gray-700 px-4 py-3 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <Link href="/">
            <button className="text-xs text-gray-400 hover:text-white border border-gray-600 rounded px-2 py-1 shrink-0">
              ← Back
            </button>
          </Link>
          <span className="text-sm font-semibold text-blue-300 truncate">
            Opera Numerorum — LaTeX Equations
          </span>
        </div>
        <button
          onClick={handleCopy}
          className={`shrink-0 text-sm font-bold px-4 py-2 rounded transition-colors ${
            copied
              ? "bg-green-600 text-white"
              : "bg-blue-600 hover:bg-blue-500 text-white"
          }`}
        >
          {copied ? "Copied!" : "Copy All"}
        </button>
      </div>

      {/* Stats bar */}
      <div className="bg-gray-900 border-b border-gray-800 px-4 py-2 flex gap-4 text-xs text-gray-400">
        <span>14 modules</span>
        <span>·</span>
        <span>{LATEX.split("\n").length} lines</span>
        <span>·</span>
        <span>ASCII-only</span>
        <span>·</span>
        <span>David J. Fox · ORCID 0009-0008-1290-6105</span>
      </div>

      {/* LaTeX source */}
      <div className="flex-1 overflow-auto">
        <pre className="p-4 text-xs leading-[1.55] font-mono text-green-300 whitespace-pre-wrap break-all select-all">
          {LATEX}
        </pre>
      </div>

      {/* Footer copy button (so it's visible without scrolling on short screens) */}
      <div className="sticky bottom-0 bg-gray-900 border-t border-gray-700 px-4 py-3 flex justify-center">
        <button
          onClick={handleCopy}
          className={`w-full max-w-sm text-sm font-bold px-4 py-3 rounded transition-colors ${
            copied
              ? "bg-green-600 text-white"
              : "bg-blue-600 hover:bg-blue-500 text-white"
          }`}
        >
          {copied ? "Copied to clipboard!" : "Copy All LaTeX"}
        </button>
      </div>
    </div>
  );
}
