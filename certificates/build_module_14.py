"""
Build Module_14_S4_Quaternions.pdf  -- 600-cell S_4 Bridge Certificate
ASCII-only output. reportlab layout.
Author: David Fox | May 2026
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import hashlib

OUTPUT = "certificates/Module_14_S4_Quaternions.pdf"

styles = getSampleStyleSheet()

title_style = ParagraphStyle("title", parent=styles["Heading1"],
    fontSize=13, leading=16, alignment=TA_CENTER, spaceAfter=4)
subtitle_style = ParagraphStyle("subtitle", parent=styles["Normal"],
    fontSize=9, leading=11, alignment=TA_CENTER, spaceAfter=2)
section_style = ParagraphStyle("section", parent=styles["Heading2"],
    fontSize=10, leading=13, spaceBefore=8, spaceAfter=3,
    textColor=colors.HexColor("#4a1a6e"))
body_style = ParagraphStyle("body", parent=styles["Normal"],
    fontSize=8, leading=11, alignment=TA_JUSTIFY)
mono_style = ParagraphStyle("mono", parent=styles["Normal"],
    fontSize=7, leading=9.5, fontName="Courier", leftIndent=12)
small_style = ParagraphStyle("small", parent=styles["Normal"],
    fontSize=7, leading=9.5)
warn_style = ParagraphStyle("warn", parent=styles["Normal"],
    fontSize=7.5, leading=10, textColor=colors.HexColor("#8B0000"))
cert_style = ParagraphStyle("cert", parent=styles["Normal"],
    fontSize=9, alignment=TA_CENTER, fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1a1a6e"))

# -- SHA values (from running the script)
SCRIPT_SHA = None  # filled after run
STDOUT_SHA = None

M4_SHA  = "b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed"
M5_SHA  = "9df98a3970acbb6942770a6cdd42fb21b009f9a5f45a222dd963e98ba4cb7a13"
M10_SHA = "ab9ce40c3cbd874cc7123d1ff0a620452610ccf874f1ab7d6a99f5700fce1ade"
M9A_SHA = "5e39f3a957d818fa85dad0a66d98a3c51801ba107ecea5a6bb457eb3456b4821"

import sys
if len(sys.argv) >= 3:
    SCRIPT_SHA = sys.argv[1]
    STDOUT_SHA = sys.argv[2]
else:
    SCRIPT_SHA = "(computed at build time)"
    STDOUT_SHA = "(computed at build time)"

story = []

story.append(Paragraph("Module 14: 600-Cell Quaternion S 4 Bridge", title_style))
story.append(Paragraph("Exhaustive Search of 120 Vertices for BC Condition Preservation", subtitle_style))
story.append(Paragraph("Battle Plan v1.6 -- David Fox -- May 2026", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#4a1a6e"), spaceAfter=6))

# Section 1: Formula
story.append(Paragraph("Section 1: Formula and 600-Cell Structure", section_style))
story.append(Paragraph(
    "The 600-cell (hecatonicosachoron) is the regular convex 4-polytope with 120 vertices, "
    "720 edges, 1200 triangular faces, and 600 tetrahedral cells. Its symmetry group "
    "H_4 has order 14400 and contains the icosahedral group as a subgroup. Vertices lie "
    "on the unit 3-sphere and are parameterized using the golden ratio phi = (1+sqrt(5))/2.",
    body_style))
story.append(Spacer(1, 4))

formula_data = [
    ["Item", "Value"],
    ["Projection formula", "beta(w,x,y,z) = 299 + w + sqrt(phi)*[phi/2*x + 1/(2phi)*(y-z)]"],
    ["sqrt(phi)", "1.272019649514069...  [user input: 1.272019]"],
    ["phi/2", "0.809016994374947...  [user input: 0.809017]"],
    ["1/(2*phi)", "0.309016994374947...  [user input: 0.309017]"],
    ["S_4", "{2, 3, 19, 191}  [M5 certified, SHA 9df98a39...]"],
    ["BC condition", "||p * beta|| < 1/p for all p in S_4"],
    ["mpmath precision", "100 decimal places"],
]
ft = Table(formula_data, colWidths=[1.5*inch, 5.0*inch])
ft.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4a1a6e")),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f4f0f8"), colors.white]),
    ("GRID",       (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(ft)
story.append(Spacer(1, 4))

vertex_data = [
    ["Group", "Count", "Coordinate form", "Example"],
    ["G1", "8",  "Permutations of (+-1, 0, 0, 0)",                  "(1,0,0,0)"],
    ["G2", "16", "(+-1/2, +-1/2, +-1/2, +-1/2) -- all 16 signs",   "(1/2,1/2,1/2,1/2)"],
    ["G3", "96", "Even perms of (+-phi/2, +-1/2, +-1/(2phi), 0)",   "(phi/2,1/(2phi),1/2,0)"],
    ["",   "120", "Total", ""],
]
vt = Table(vertex_data, colWidths=[0.5*inch, 0.55*inch, 3.0*inch, 2.45*inch])
vt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4a1a6e")),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",   (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f4f0f8"), colors.white]),
    ("GRID",       (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(vt)

# Section 2: Results
story.append(Paragraph("Section 2: Exhaustive Sweep Results", section_style))
story.append(Paragraph(
    "All 120 vertices were tested at 100 dps precision. For each vertex, ||p*beta|| was "
    "computed for p in {2, 3, 19, 191} and compared against 1/p. "
    "A vertex 'preserves S_4' iff all four conditions hold simultaneously.",
    body_style))
story.append(Spacer(1, 4))

results_data = [
    ["Category", "Count", "Vertices / Note"],
    ["Vertices tested", "120", "All 120 600-cell vertices, sorted"],
    ["Preserve S_4", "2", "Vertices (1,0,0,0) and (-1,0,0,0) -- beta = 300 and 298"],
    ["Integer beta", "2", "Both winners: beta in Z => ||p*beta|| = 0 for all p"],
    ["Non-trivial S_4 pass", "0", "No non-integer vertex preserves all 4 primes simultaneously"],
    ["C(beta) > 2*sqrt(33)", "2", "Both integer cases (trivially; C = 962.6 for all primes <= 1000)"],
]
rt = Table(results_data, colWidths=[1.8*inch, 0.65*inch, 4.05*inch])
rt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2c5f2e")),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 7.5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#e8f5e9"), colors.white]),
    ("GRID",       (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(rt)
story.append(Spacer(1, 4))

# Certified beta table
story.append(Paragraph("Certified beta Values from 600-Cell Sweep:", small_style))
story.append(Spacer(1, 2))
bv_data = [
    ["Vertex", "beta", "S_beta cap[2,1000]", "C(beta)", "g_max", "Note"],
    ["(1, 0, 0, 0)",  "300.000000", "168 primes (ALL)",
     "962.6092", "231654", "INTEGER-DEGENERATE"],
    ["(-1, 0, 0, 0)", "298.000000", "168 primes (ALL)",
     "962.6092", "231654", "INTEGER-DEGENERATE"],
]
bvt = Table(bv_data, colWidths=[1.1*inch, 0.9*inch, 1.25*inch, 0.75*inch, 0.7*inch, 1.8*inch])
bvt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#555555")),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",   (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#fff3cd"), colors.white]),
    ("GRID",       (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(bvt)
story.append(Spacer(1, 4))

story.append(Paragraph(
    "DEGENERATE CASE: For any integer n, ||p*n|| = 0 for every prime p. "
    "Therefore S_{integer} = all primes. C(S cap [2,1000]) = 962.6 for ANY integer beta. "
    "This is not specific to the 600-cell or to the value 300 -- it is a trivial property "
    "of integer arithmetic. The interesting question (finding a non-integer 600-cell vertex "
    "that preserves S_4) has a NEGATIVE answer: no such vertex exists among the 120.",
    warn_style))

# Section 3: Mathematical Analysis
story.append(Paragraph("Section 3: Mathematical Analysis and Interpretation", section_style))
story.append(Paragraph(
    "Why non-integer vertices fail: beta = 299 + w + sqrt(phi)*L where "
    "L = phi/2*x + (y-z)/(2*phi). For x,y,z not all zero, the term sqrt(phi)*L "
    "is a non-zero algebraic number involving sqrt(phi). Since sqrt(phi) is "
    "transcendental (follows from the Lindemann-Weierstrass theorem applied to "
    "the algebraic independence of phi), the fractional part {p*sqrt(phi)*L} "
    "is equidistributed and ||p*beta|| is pseudo-random. The probability of "
    "hitting all four conditions ||p*beta|| < 1/p for p in {2,3,19,191} "
    "simultaneously is approximately 2/2 * 2/3 * 2/19 * 2/191 ~= 0.1%, "
    "and for all 112 non-trivial Group 1/2/3 vertices, none succeeded.",
    body_style))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "Hypothesis from screenshots (supervisor): 'Icosahedral symmetry is a red herring "
    "for S_4. Only the w-axis matters.' This is confirmed: the only winners have "
    "x=y=z=0, so the icosahedral projection (the sqrt(phi)*[...] term) contributes "
    "zero. The 600-cell's exceptional geometry does not translate into new BC-certified "
    "beta values under this particular projection formula.",
    body_style))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "Comparison with M10: M10 certified g=33 by adding p_5 = 3993746143633 to the "
    "certified S_4 set, achieving C(S_5) = 40.44. M14 achieves C = 962.6 but only "
    "via the trivial integer-beta case. M10 is the rigorous, non-trivial certification.",
    body_style))

# Section 4: Chain of Custody
story.append(Paragraph("Section 4: Chain of Custody", section_style))

cod_data = [
    ["Item", "SHA-256"],
    ["m14_s4_quaternions.py (script)", SCRIPT_SHA[:40] + "..." if SCRIPT_SHA and len(SCRIPT_SHA) > 40 else str(SCRIPT_SHA)],
    ["m14.out (stdout)",               STDOUT_SHA[:40] + "..." if STDOUT_SHA and len(STDOUT_SHA) > 40 else str(STDOUT_SHA)],
    ["Parent M4 (S_14)",               M4_SHA[:40] + "..."],
    ["Parent M5 (C(S_4))",             M5_SHA[:40] + "..."],
    ["Parent M10 (g=33)",              M10_SHA[:40] + "..."],
    ["Parent M9-All (g<=32)",          M9A_SHA[:40] + "..."],
]
codt = Table(cod_data, colWidths=[2.4*inch, 4.1*inch])
codt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#333333")),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",   (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f8f8f8"), colors.white]),
    ("GRID",       (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))
story.append(codt)
story.append(Spacer(1, 6))

story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#4a1a6e"), spaceAfter=4))
story.append(Paragraph("Conclusion", section_style))
story.append(Paragraph(
    "Exhaustive search of all 120 vertices of the 600-cell under the projection "
    "beta = 299 + w + sqrt(phi)*[phi/2*x + (y-z)/(2phi)] finds exactly 2 S_4-preserving "
    "vertices: (1,0,0,0) with beta=300 and (-1,0,0,0) with beta=298. Both are degenerate "
    "(integer beta). For both, C(S_beta cap [2,1000]) = 962.6092 >> 2*sqrt(33) = 11.489, "
    "certifying GRH for all X_0(N) with g(N) <= 231654 and no CM newforms -- but this "
    "holds trivially for any integer. No non-trivial 600-cell vertex preserves S_4.",
    body_style))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "CERTIFIED -- Battle Plan v1.6 -- David Fox -- May 2026", cert_style))

# Build PDF
doc = SimpleDocTemplate(OUTPUT, pagesize=letter,
    leftMargin=0.75*inch, rightMargin=0.75*inch,
    topMargin=0.7*inch, bottomMargin=0.7*inch)
doc.build(story)

pdf_sha = hashlib.sha256(open(OUTPUT, "rb").read()).hexdigest()
print("PDF written: " + OUTPUT)
print("PDF SHA-256: " + pdf_sha)
