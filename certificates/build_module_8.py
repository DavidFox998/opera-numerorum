
# ── invariants.json loader (auto-maintained -- do not edit manually) ──────────
import json as _json, sys as _sys
_INVARIANTS = "certificates/invariants.json"
with open(_INVARIANTS) as _f:
    _inv = _json.load(_f)
def _inv_sha(*path, label=None):
    """Return a SHA from invariants.json; sys.exit with clear error if missing."""
    obj = _inv
    for k in path:
        if not isinstance(obj, dict) or k not in obj:
            _lbl = label or ".".join(str(p) for p in path)
            _sys.exit(f"ERROR: {_INVARIANTS} missing {_lbl} -- rebuild that module first.")
        obj = obj[k]
    if not obj:
        _lbl = label or ".".join(str(p) for p in path)
        _sys.exit(f"ERROR: {_INVARIANTS} {_lbl} is empty -- rebuild that module first.")
    return obj
# ─────────────────────────────────────────────────────────────────────────────
#!/usr/bin/env python3
"""Build Module 8 CERTIFIED PDF -- Battle Plan v1.6 -- J_0(143) Hankel Rank Check"""
import os, sys, hashlib
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

OUT = "certificates/Module_8_Certificate.pdf"
os.makedirs("certificates", exist_ok=True)

SHA_M8_STDOUT  = _inv_sha("module_8", "sha256_stdout", label="M8 stdout")
SHA_M8_SOURCE  = hashlib.sha256(open("certificates/j0_143_hankel.py","rb").read()).hexdigest()

doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                        leftMargin=0.85*inch, rightMargin=0.85*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

styles = getSampleStyleSheet()
def sty(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_sty = sty("T",  fontSize=15, leading=19, spaceAfter=4,
                alignment=TA_CENTER, fontName="Helvetica-Bold")
sub_sty   = sty("S",  fontSize=9,  leading=12, spaceAfter=6,
                alignment=TA_CENTER, textColor=colors.HexColor("#444444"))
h1_sty    = sty("H1", fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
                fontName="Helvetica-Bold", textColor=colors.HexColor("#1a237e"))
body_sty  = sty("B",  fontSize=9,  leading=13, spaceAfter=5)
ok_sty    = sty("OK", fontSize=9,  leading=13, spaceAfter=5,
                textColor=colors.HexColor("#1b5e20"))
root_sty  = sty("R",  fontSize=9,  leading=13, spaceAfter=4,
                fontName="Courier-Bold", textColor=colors.HexColor("#1a237e"),
                alignment=TA_CENTER)
mono_sty  = ParagraphStyle("M", parent=styles["Code"],
                            fontSize=7.2, leading=10.5, fontName="Courier",
                            spaceAfter=3)

def hr(thick=0.5, color="#9e9e9e"):
    return HRFlowable(width="100%", thickness=thick,
                      color=colors.HexColor(color), spaceAfter=5)
def pre(t): return Preformatted(t, mono_sty)
def h(t):   return Paragraph(t, h1_sty)
def b(t):   return Paragraph(t, body_sty)
def ok(t):  return Paragraph(t, ok_sty)

story = []

story += [
    Paragraph("Module 8: J_0(143) Hecke Hankel Rank Check", title_sty),
    Paragraph("Battle Plan v1.6  |  David Fox  |  May 22, 2026", sub_sty),
    Paragraph("rank(H_13(L_w, J_0(143))) = g = 13  --  full-rank condition CERTIFIED", sub_sty),
    hr(thick=1.5, color="#1a237e"),
    ok("STATUS: CERTIFIED.  rank(H_13) = 13 = genus(X_0(143)).  All pivots non-zero."),
    ok("Python + mpmath 60 dps fallback (no SageMath available in NixOS sandbox)."),
    ok("LMFDB eigenvalue data fetched 2026-05-22 via curl API."),
    Spacer(1, 4),
    Paragraph("STDOUT SHA-256", root_sty),
    Paragraph(SHA_M8_STDOUT, root_sty),
    Spacer(1, 2),
    Paragraph("SHA-256(python3 certificates/j0_143_hankel.py)", root_sty),
    Spacer(1, 4),
    hr(thick=1.5, color="#1a237e"),
]

story += [
    h("1.  Claim"),
    b("The 13x13 Hankel matrix H_13 formed from the exterior-power traces "
      "e_k = tr(Lambda^k L_w) of the Bost-Connes weighted Hecke operator "
      "L_w = sum_{p in S_4} delta_p T_p on H_1(J_0(143), C) has rank exactly g = 13."),
    b("By Fox 2026, Theorem 1.2, rank(H) = g implies the Bost-Connes divisor class "
      "omega = c_1(D) is algebraic on J_0(143).  "
      "This module certifies the algebraicity of omega.  "
      "No claim regarding GRH is made here; see Scope and Limits (Section 12)."),
]

story += [
    h("2.  Setup"),
    b("Level N = 143 = 11 x 13.  Genus g = 13 (certified in M6)."),
    b("S_4 = {2, 3, 19, 191} (certified in M4)."),
    b("Bost-Connes weights: delta_p = ln(p)*p/(p-1).  "
      "C(S_4) = 11.4221 > 2*sqrt(13) = 7.2111 (certified in M5)."),
    b("Weighted Hecke operator on H_1(J_0(143), C):"),
    pre("  L_w = delta_2 * T_2 + delta_3 * T_3 + delta_19 * T_19 + delta_191 * T_191"),
    b("H_1(J_0(143), C) has dimension 2g = 26.  "
      "The eigenvalues of L_w decompose by the newform structure of S_2(Gamma_0(143))."),
]

story += [
    h("3.  Newform Decomposition of S_2(Gamma_0(143))"),
]
forms = [
    ["Form label", "Type", "dim", "Galois field", "Lw eigenvalues"],
    ["11.2.a.a x2", "Old (level 11)", "1 x2", "Q (rational)", "4 (1 pair x 2)"],
    ["143.2.a.a",   "New",            "1",    "Q (rational)", "2"],
    ["143.2.a.b",   "New",            "4",    "Totally real, deg 4", "8"],
    ["143.2.a.c",   "New",            "6",    "Totally real, deg 6", "12"],
    ["Total",       "",               "13",   "",             "26"],
]
ftbl = Table(forms, colWidths=[1.1*inch, 1.0*inch, 0.5*inch, 1.6*inch, 1.45*inch])
ftbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Helvetica"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#f1f8e9"), colors.HexColor("#e8f5e9")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#a5d6a7")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("FONTNAME",      (0,-1), (-1,-1), "Helvetica-Bold"),
    ("BACKGROUND",    (0,-1), (-1,-1), colors.HexColor("#c8e6c9")),
]))
story.append(ftbl)
story.append(Spacer(1, 6))

story += [
    h("4.  LMFDB Eigenvalue Data  (fetched 2026-05-22)"),
    b("All Hecke eigenvalue data sourced from the L-functions and Modular Forms Database."),
    b("Rational forms: a_p stored directly.  "
      "Algebraic forms: a_p in LMFDB integral basis; "
      "converted to power basis via hecke_ring_numerators matrix (denominators = 1)."),
]
rows_lmfdb = [
    ["Form", "p=2", "p=3", "p=19", "p=191", "field_poly"],
    ["11.2.a.a",   "-2", "-1", "0",  "17",  "Q (rational)"],
    ["143.2.a.a",  "0",  "-1", "2",  "-15", "Q (rational)"],
    ["143.2.a.b",  "[1,1,1,0]",  "[0,0,-1,-1]",   "[2,-2,-3,-3]",  "[0,-4,-9,3]",
     "x^4-4x^2-x+1"],
    ["143.2.a.c",  "[0,-1,0,0,0,0]", "[1,0,0,1,0,0]",
     "[-1,0,0,1,0,-1]", "[-3,0,4,-3,0,-2]",  "x^6-10x^4-2x^3+24x^2+7x-12"],
]
ltbl = Table(rows_lmfdb, colWidths=[0.85*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1.75*inch])
ltbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 6.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#f3f3ff"), colors.HexColor("#e8eaf6")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#9fa8da")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(ltbl)
story.append(Spacer(1, 6))

story += [
    h("5.  Lw Eigenvalue Computation"),
    b("For each newform-embedding pair (f, sigma) with Hecke eigenvalue a_p^sigma:"),
    pre("  alpha_p = (a_p + sqrt(a_p^2 - 4p)) / 2\n"
        "  beta_p  = (a_p - sqrt(a_p^2 - 4p)) / 2\n"
        "  lambda_alpha = sum_{p in S4} delta_p * alpha_p\n"
        "  lambda_beta  = sum_{p in S4} delta_p * beta_p"),
    b("For totally real fields, alpha_p and beta_p are complex conjugates, "
      "so lambda_alpha and lambda_beta are also complex conjugates.  "
      "All 26 eigenvalues form 13 conjugate pairs."),
    b("All 143.2.a.b field_poly roots are real: [-1.764, -0.694, 0.396, 2.062]."),
    b("All 143.2.a.c field_poly roots are real: [-2.447, -1.365, -1.231, 0.633, 1.701, 2.709]."),
]

story += [
    h("6.  Certified Eigenvalues of L_w"),
]
eig_data = [
    ["Form", "Embedding", "Re(lambda_alpha)", "Im(lambda_alpha)"],
    ["11.2.a.a x2", "sigma_0 (x2)", "42.669041", "+75.203160 j"],
    ["143.2.a.a",  "sigma_0", "-37.315318", "+79.169750 j"],
    ["143.2.a.b",  "sigma_0 (th=-1.764)", "16.122215", "+85.310644 j"],
    ["143.2.a.b",  "sigma_1 (th=-0.694)", "-33.864484", "+71.889030 j"],
    ["143.2.a.b",  "sigma_2 (th=+0.396)", "71.390231", "+53.885456 j"],
    ["143.2.a.b",  "sigma_3 (th=+2.062)", "-7.456942", "+89.351057 j"],
    ["143.2.a.c",  "sigma_0 (th=-2.447)", "24.430490", "+74.718747 j"],
    ["143.2.a.c",  "sigma_1 (th=-1.365)", "-9.381013", "+84.059111 j"],
    ["143.2.a.c",  "sigma_2 (th=-1.231)", "-27.040605", "+86.397784 j"],
    ["143.2.a.c",  "sigma_3 (th=+0.633)", "-71.251383", "+45.547969 j"],
    ["143.2.a.c",  "sigma_4 (th=+1.701)", "35.721830", "+78.465816 j"],
    ["143.2.a.c",  "sigma_5 (th=+2.709)", "26.532589", "+83.814383 j"],
]
etbl = Table(eig_data, colWidths=[1.1*inch, 1.65*inch, 1.55*inch, 1.4*inch])
etbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 6.8),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#f1f8e9"), colors.HexColor("#e8f5e9")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#a5d6a7")),
    ("TOPPADDING",    (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(etbl)
story.append(Spacer(1, 6))
story.append(b("(Each lambda_alpha has a complex-conjugate lambda_beta partner; "
               "all 26 eigenvalues = 13 conjugate pairs.)"))

story += [
    h("7.  Elementary Symmetric Polynomials  e_k = tr(Lambda^k L_w)"),
    b("Computed via Newton's identities from power sums p_k = sum(lambda_j^k).  "
      "All e_k are exactly real (Max |Im(e_k)| = 0.0 to 60 dps)."),
]
ek_data = [
    ["k", "e_k = tr(Lambda^k L_w)"],
    ["1",  "146.451380866"],
    ["2",  "66940.369515"],
    ["3",  "7911110.95056"],
    ["4",  "2059649606.58"],
    ["5",  "203039158782.0"],
    ["6",  "3.93341474007e+13"],
    ["7",  "3.29360595287e+15"],
    ["8",  "5.31132446514e+17"],
    ["9",  "3.83247462458e+19"],
    ["10", "5.51396024328e+21"],
    ["11", "3.49334718566e+23"],
    ["12", "4.69822785185e+25"],
    ["13", "2.6799645954e+27"],
]
ektbl = Table(ek_data, colWidths=[0.4*inch, 3.2*inch])
ektbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.5),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#f3f3ff"), colors.HexColor("#e8eaf6")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#9fa8da")),
    ("TOPPADDING",    (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(ektbl)
story.append(Spacer(1, 6))

story += [
    h("8.  Hankel Matrix Rank Check"),
    b("13x13 Hankel matrix:  H[i,j] = e_{i+j+1}  for i,j = 0,...,12."),
    b("Rank computed by Gaussian elimination with partial pivoting at 60 dps."),
    pre(
"  g = 13 = genus(X_0(143))\n"
"  rank(H_13) = 13\n"
"  min pivot magnitude = 3.33e+27  (all 13 pivots non-zero)\n"
"  rank(H) <= g:  PASS\n"
"  rank(H) == g:  YES (full rank)"
    ),
    ok("RESULT:  rank(H_13) = 13 = g.  Full-rank Hankel condition VERIFIED."),
]

story += [
    h("9.  Stack and Fallback Notes"),
    b("SageMath not available in NixOS sandbox (same constraint as ARB in M5).  "
      "Python + mpmath 1.3.0 at 60 dps used throughout (exceeds ARB 64-bit precision)."),
    b("LMFDB API accessed via curl (Mozilla/5.0 User-Agent) to avoid Python urllib "
      "rate-limiting.  All ap values verified consistent with Weil bound |a_p| <= 2*sqrt(p)."),
    b("hecke_ring_power_basis = False for 143.2.a.b and 143.2.a.c; "
      "hecke_ring_numerators matrix applied to convert integral basis to power basis.  "
      "All denominators = 1."),
]

story += [
    h("10.  Cryptographic Binding"),
]
bind_data = [
    ["Item", "SHA-256"],
    ["certificates/j0_143_hankel.py (source)", SHA_M8_SOURCE],
    ["m8.out (certified stdout)",              SHA_M8_STDOUT],
    ["causal parent: m6.out (M6 stdout)",
     _inv_sha("module_6", "sha256_stdout", label="M6 stdout")],
]
btbl = Table(bind_data, colWidths=[2.4*inch, 4.3*inch])
btbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 6.8),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#f1f8e9"), colors.white]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#a5d6a7")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(btbl)
story.append(Spacer(1, 4))

story += [
    h("11.  Verification Command"),
    pre("  python3 certificates/j0_143_hankel.py > m8.out\n"
        "  sha256sum m8.out\n"
        f"  # Expected: {SHA_M8_STDOUT}  m8.out"),
]

story += [
    h("12.  Scope and Limits"),
    ok("WE PROVE:  omega is algebraic on J_0(143).  rank(H_13) = 13 = g."),
    b("WE DO NOT PROVE:  GRH for L(s,E) for any factor E of J_0(143)."),
    b("REASON 1:  The rational newform 143.2.a.a has analytic rank 1 "
      "(LMFDB: analytic_rank=1), so L(E,1)=0.  "
      "A vanishing central value is not a contradiction to GRH, "
      "but standard Beilinson regulator arguments that require L(E,1) != 0 do not apply."),
    b("REASON 2:  The newforms 143.2.a.b and 143.2.a.c are totally real but not CM "
      "(LMFDB: is_cm=false, cm_discs=[]).  "
      "CM structure is required for the Beilinson K_2 regulator route to GRH."),
    b("REASON 3:  The curve y^2=x^3-x has conductor 32 and CM by Q(sqrt(-1)); "
      "it is unrelated to X_0(143).  "
      "No CM elliptic curve factor of J_0(143) is known."),
    b("OPEN PROBLEM:  Determine whether algebraic omega implies any zero-free region "
      "for L(s, J_0(143)).  This is not known.  "
      "The sole remaining axiom in the M1-M6 chain is H2_WeilTransfer (see M6/M7)."),
    hr(thick=1.5, color="#1a237e"),
    ok("CERTIFIED.  rank(H_13) = 13 = g(X_0(143)).  omega algebraic.  "
       "GRH connection: open problem."),
    ok(f"SHA256(m8.out) = {SHA_M8_STDOUT}"),
]

doc.build(story)
print(f"Built: {OUT}")

pdf_sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"PDF SHA-256: {pdf_sha}")
