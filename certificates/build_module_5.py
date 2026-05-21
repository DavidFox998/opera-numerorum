#!/usr/bin/env python3
"""Build Module 5 Formula Audit PDF -- Battle Plan v1.6"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_CENTER

OUT = "certificates/Module_5_Certificate.pdf"
os.makedirs("certificates", exist_ok=True)

# -- Real cryptographic values (all computed, none fabricated) ----------------
SHA_SRC_PY   = "ed801430ee00e14eb799b31d68f3e2e94d35f468678a7126610d8f3dad3de57d"
SHA_SRC_C    = "ad71a42d110791ed7594bd12780e755f5bf5d4e1d55ef48b9fdf5b5f5fc7fd3a"
SHA_INPUT    = "53315d4e6649a40b425edd445efbb937c0dec7a1aa571ea6b60f4f1033568387"
SHA_LOG      = "88a6af4a36d4ff0885c4feb08f30382e5059f72520e202740966e2d5d5402c15"
PARENT_SHA   = "b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed"
# -----------------------------------------------------------------------------

doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                        leftMargin=0.85*inch, rightMargin=0.85*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

styles = getSampleStyleSheet()
def sty(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_sty = sty("T",  fontSize=15, leading=19, spaceAfter=4,
                alignment=TA_CENTER, fontName="Helvetica-Bold")
sub_sty   = sty("S",  fontSize=9,  leading=12, spaceAfter=8,
                alignment=TA_CENTER, textColor=colors.HexColor("#444444"))
h1_sty    = sty("H1", fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
                fontName="Helvetica-Bold",
                textColor=colors.HexColor("#1a237e"))
body_sty  = sty("B",  fontSize=9,  leading=13, spaceAfter=5)
warn_sty  = sty("W",  fontSize=9,  leading=13, spaceAfter=5,
                textColor=colors.HexColor("#b71c1c"))
mono_sty  = ParagraphStyle("M", parent=styles["Code"],
                            fontSize=7.5, leading=11, fontName="Courier",
                            spaceAfter=3)

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#9e9e9e"), spaceAfter=5)
def pre(t): return Preformatted(t, mono_sty)
def h(t):   return Paragraph(t, h1_sty)
def b(t):   return Paragraph(t, body_sty)
def w(t):   return Paragraph(t, warn_sty)

story = []

# -- Title --------------------------------------------------------------------
story += [
    Paragraph("Module 5: Bost Sum Formula Audit Report (v2)", title_sty),
    Paragraph("Battle Plan v1.6  |  David Fox  |  May 21, 2026", sub_sty),
    Paragraph("Supervisor correction applied: S4 = {2, 3, 19, 191}", sub_sty),
    hr(),
    w("STATUS: HALTED -- Formula discrepancy persists after supervisor correction."),
    w("arb_gt(C, threshold) = 0.  Input chain intact.  Awaiting formula correction."),
    Spacer(1, 4),
]

# -- Section 1 ----------------------------------------------------------------
story += [
    h("1.  Supervisor Correction Applied"),
    b("The supervisor has clarified (v2) that Module 5 uses S4, not S14:"),
    pre("  S4 = {2, 3, 19, 191}  (first 4 elements of S(alpha_0))\n"
        "  S4 is a subset of S14, which was certified in Module 4.\n"
        "  Module 3 values Q_5=226 and 82829 are NOT used here."),
    b("The LaTeX claim is:"),
    pre("  C(S4) := sum_{p in S4} log(p) / (p-1)  >  2*sqrt(13)\n"
        "  Numerically:  C(S4) in [8.6290436642 +/- 1e-10]\n"
        "                2*sqrt(13) in [7.2111025509 +/- 1e-10]"),
]

# -- Section 2 ----------------------------------------------------------------
story += [
    h("2.  Causal Chain"),
    b("This module depends on Module 4 (bound_10_4000.py stdout):"),
    pre(f"  Parent SHA-256:  {PARENT_SHA}"),
    b("The input file data/S14_primes.txt is byte-identical to Module 4 stdout:"),
    pre(f"  $ ./bin/print_S14 | sha256sum\n"
        f"  {SHA_INPUT}  -          [chain intact]"),
    b("Module 4 stdout format: 14 primes, comma-separated, single newline. "
      "arb_bost.py reads only the first 4 (S4) from this file."),
]

# -- Section 3 ----------------------------------------------------------------
story += [
    h("3.  Environment"),
    pre("  Python 3.12  |  mpmath 1.3.0  |  64 decimal places (~212 binary bits)\n"
        "  ARB 2.23.0: NOT AVAILABLE (NixOS sandbox)\n"
        "  Fallback: mpmath, exceeds 64-bit ARB precision"),
    pre(f"  SHA-256  arb_bost.py :  {SHA_SRC_PY}\n"
        f"  SHA-256  arb_bost.c  :  {SHA_SRC_C}"),
]

# -- Section 4 ----------------------------------------------------------------
story += [
    h("4.  Actual Execution Output"),
    pre("  $ python3 arb_bost.py data/S14_primes.txt 2>/dev/null\n"
        "  C(S4) in [1.4336768125 +/- 1.00e-10]\n"
        "  2*sqrt(13) in [7.2111025509 +/- 1.00e-10]\n"
        "  arb_gt(C, threshold) = 0\n"
        "  Exit code: 2"),
    b("Stdout SHA-256:"),
    pre(f"  {SHA_LOG}  -"),
]

# -- Section 5 ----------------------------------------------------------------
story += [
    h("5.  Forensic Analysis: Term-by-Term Proof"),
    b("Using mpmath at 64 decimal places, the literal formula gives:"),
    pre("  p=2:    log(2)/(2-1)     = 0.6931471805599453\n"
        "  p=3:    log(3)/(3-1)     = 0.5493061443340549\n"
        "  p=19:   log(19)/(19-1)   = 0.1635799432870245\n"
        "  p=191:  log(191)/(191-1) = 0.0276435443581402\n"
        "  -------------------------------------------------\n"
        "  C(S4) TOTAL              = 1.4336768125391649"),
    b("Comparison:"),
    pre("  Computed C(S4) = 1.4336768125  (this work)\n"
        "  Claimed  C(S4) = 8.6290436642  (supervisor LaTeX)\n"
        "  2*sqrt(13)     = 7.2111025509\n"
        "  Discrepancy    = 7.1953668517"),
    w("MATHEMATICAL PROOF of impossibility: the formula sum log(p)/(p-1) "
      "over any 4 distinct primes is bounded above by the 4 smallest primes "
      "{2,3,5,7}: 0.693+0.549+0.402+0.324 = 1.968. "
      "The claimed value 8.629 exceeds this maximum by 6.66. "
      "No choice of 4 distinct primes can produce 8.629 with this formula."),
]

# -- Section 6 ----------------------------------------------------------------
story += [
    h("6.  Hypothesis Testing: What Formula Gives 8.6290436642?"),
    b("Systematic search over natural variants:"),
    pre("  sum log(p)*p/(p-1)         = 11.4221  (not 8.629)\n"
        "  sum log(p)/(p-1)^2         =  0.9771  (not 8.629)\n"
        "  sum (log p)^2/(p-1)        =  1.7108  (not 8.629)\n"
        "  sum log(p)/p               =  0.8952  (not 8.629)\n"
        "  -sum log(1-1/p)            =  1.1579  (not 8.629)\n"
        "  sum log(p)/(p^(pi/10)-1)   =  8.6975  (close, but off by 0.068)\n"
        "  sum log(p)/(p^(1/pi)-1)    =  8.5433  (off by 0.086)\n"
        "  sum log(p)/(p^0.31599-1)   =  8.6290  [MATCHES, alpha ~ 0.31599]"),
    b("Finding: the value 8.6290436642 is consistent with the formula "
      "sum log(p)/(p^alpha - 1) evaluated at alpha ~ 0.31599. This is "
      "close to, but not equal to, pi/10 = 0.31416 (which gives 8.6975). "
      "The constant 0.31599 is not a recognizable mathematical constant."),
    b("Alternate hypothesis: the value 8.629 may be a computational error "
      "in the LaTeX draft, and the correct value is 1.434 (literal formula) "
      "or 8.697 (if the denominator should be p^(pi/10)-1, reflecting "
      "the fractional part of alpha_0 = 299+pi/10)."),
]

# -- Section 7 ----------------------------------------------------------------
story += [
    h("7.  Cryptographic Binding (SHA-256)"),
]
rows = [
    ["Artifact", "SHA-256"],
    ["arb_bost.py (fallback, S4)",   SHA_SRC_PY],
    ["arb_bost.c (source record)",   SHA_SRC_C],
    ["data/S14_primes.txt (input)",  SHA_INPUT],
    ["Stdout log (audit, exit 2)",   SHA_LOG],
    ["Module 4 parent (PARENT_SHA)", PARENT_SHA],
]
tbl = Table(rows, colWidths=[2.2*inch, 4.2*inch])
tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.HexColor("#f3f3f3"), colors.white]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#bbbbbb")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(tbl)
story.append(Spacer(1, 6))

# -- Section 8 ----------------------------------------------------------------
story += [
    h("8.  Reproduction Commands"),
    pre("  # Verify input (Module 4 stdout chain):\n"
        "  $ ./bin/print_S14 | sha256sum\n"
        f"  {SHA_INPUT}  -\n\n"
        "  # Hash source:\n"
        "  $ sha256sum arb_bost.py\n"
        f"  {SHA_SRC_PY}  arb_bost.py\n\n"
        "  # Run and hash stdout:\n"
        "  $ python3 arb_bost.py data/S14_primes.txt 2>/dev/null | sha256sum\n"
        f"  {SHA_LOG}  -"),
]

# -- Section 9 ----------------------------------------------------------------
story += [
    h("9.  Required Supervisor Action"),
    b("Module 5 bridges the discrete S4 certification (Module 4) and the "
      "GRH bound (Module 6). Certification is halted at this module."),
    pre("  Causal chain:\n"
        "  M1 (alpha_0) -> M2 (kappa) -> M3 (CF pi/10) -> M4 (S14/S4)\n"
        "      -> M5 [HALTED] -> M6 -> M7 (manifest)"),
    b("Please supply one of:"),
    pre("  (A) The Python or Sage snippet that computes C(S4) = 8.6290436642.\n"
        "      (The literal formula sum log(p)/(p-1) gives 1.4337, not 8.629.)\n\n"
        "  (B) Confirmation that the denominator should be p^(pi/10)-1\n"
        "      instead of p-1.  That formula gives 8.6975, still not 8.629.\n\n"
        "  (C) The DOI or theorem number in the source paper where C(S4)\n"
        "      is defined and the value 8.629 is established.\n\n"
        "  (D) Confirmation that the CORRECT C(S4) = 1.4337 and the\n"
        "      comparison threshold should NOT be 2*sqrt(13) = 7.211."),
    hr(),
    b("This document is a Formula Audit Report under Battle Plan v1.6. "
      "All SHAs are real. No values are fabricated. "
      "Module 5 certification resumes upon supervisor-provided correction."),
]

doc.build(story)
print(f"Built: {OUT}")

import hashlib
pdf_sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"PDF SHA-256: {pdf_sha}")
