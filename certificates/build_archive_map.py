"""
Opera Numerorum -- Archive Map PDF
Reading order guide for all 47 documents
David Fox -- May 23, 2026
"""

from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import hashlib

OUT = "certificates/OperaNumerorum_ArchiveMap.pdf"

styles = getSampleStyleSheet()
def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

title_sty = sty("T",  fontSize=20, leading=26, alignment=TA_CENTER,
                fontName="Helvetica-Bold", spaceAfter=4)
sub_sty   = sty("S",  fontSize=12, leading=16, alignment=TA_CENTER,
                fontName="Helvetica", spaceAfter=2)
auth_sty  = sty("A",  fontSize=9,  leading=13, alignment=TA_CENTER,
                fontName="Helvetica", spaceAfter=2)
h1_sty    = sty("H1", fontSize=12, leading=16, fontName="Helvetica-Bold",
                spaceBefore=12, spaceAfter=4,
                textColor=colors.HexColor("#1a1a2e"))
h2_sty    = sty("H2", fontSize=10, leading=14, fontName="Helvetica-Bold",
                spaceBefore=6, spaceAfter=2,
                textColor=colors.HexColor("#1a1a2e"))
body_sty  = sty("B",  fontSize=9,  leading=13, alignment=TA_JUSTIFY,
                spaceAfter=5)
note_sty  = sty("N",  fontSize=8.5,leading=12, fontName="Helvetica-Oblique",
                spaceAfter=3, textColor=colors.HexColor("#444444"))

def sp(n=6): return Spacer(1, n)
def hr():    return HRFlowable(width="100%", thickness=0.5, color=colors.grey)

# Colour scheme
C_HEAD   = colors.HexColor("#1a1a2e")   # navy
C_PRE    = colors.HexColor("#4a4e69")   # slate   -- preface
C_PAP    = colors.HexColor("#2d6a4f")   # forest  -- source papers
C_CAN    = colors.HexColor("#1b4332")   # dark green -- canonical
C_COMP   = colors.HexColor("#344e41")   # pine    -- complete
C_CERT   = colors.HexColor("#14213d")   # midnight -- certificates
C_STAR   = colors.HexColor("#780000")   # deep red -- morningstar
C_ROW1   = colors.HexColor("#f8f9fa")
C_ROW2   = colors.white

def section_table(rows, col_widths, hdr_color):
    ts = TableStyle([
        ("FONTNAME",      (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("LEADING",       (0,0), (-1,-1), 11),
        ("GRID",          (0,0), (-1,-1), 0.25, colors.HexColor("#cccccc")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        # header row
        ("BACKGROUND",    (0,0), (-1,0),  hdr_color),
        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  8.5),
        # alternating rows
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [C_ROW1, C_ROW2]),
    ])
    tbl = Table(rows, colWidths=col_widths)
    tbl.setStyle(ts)
    return tbl

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.75*inch, rightMargin=0.75*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch)
W = letter[0] - 1.5*inch
story = []

# ── TITLE ─────────────────────────────────────────────────────────────────────
story += [
    sp(10),
    Paragraph("OPERA NUMERORUM", title_sty),
    Paragraph("Archive Map -- Reading Order Guide", sub_sty),
    Paragraph("47 Documents in Canonical Order", sub_sty),
    sp(6),
    hr(),
    sp(4),
    Paragraph("David Fox (D.J.F.)  |  ORCID: 0009-0008-1290-6105", auth_sty),
    Paragraph("Aberdeen, WA, Earth  --  CONTACT ZERO  |  May 23, 2026", auth_sty),
    sp(10),
    Paragraph(
        "This map shows every document in the Opera Numerorum archive in the order "
        "it should be read. Each entry shows the document number, filename, what it "
        "contains, and its role in the causal chain. "
        "Documents 1-11 are narrative and canonical. Documents 12-43 are machine-"
        "certified SHA-bound modules. Documents 44-47 are the Morning Star "
        "Engineering series.",
        body_sty),
    sp(8),
    hr(),
    sp(6),
]

# ── SECTION 1: PREFACE ────────────────────────────────────────────────────────
story += [Paragraph("Section 1 -- Preface  (1 document)", h1_sty)]
rows = [
    ["#", "Filename", "Contents", "Role"],
    ["1", "OperaNumerorum_Preface.pdf",
     "Illustrated front-matter. 5 figures: alpha_0 number line, "
     "Bost-Connes bar chart, causal DAG, frontispiece (AI), "
     "CONTACT ZERO plaque (AI). New opening: 'We were doing arithmetic.'",
     "Read first. Sets the context, the discovery narrative, and the "
     "CONTACT ZERO reference frame."],
]
cw = [0.22*inch, 1.5*inch, 2.6*inch, 1.5*inch]
story += [section_table(rows, cw, C_PRE), sp(10)]

# ── SECTION 2: SOURCE PAPERS ─────────────────────────────────────────────────
story += [Paragraph("Section 2 -- Original Source Papers  (7 documents)", h1_sty),
          Paragraph(
              "These are David Fox's original written papers for modules M1-M7. "
              "They contain the mathematical exposition, proofs, and claims. "
              "The corresponding certificate PDFs in Section 5 provide machine "
              "verification of every numerical result stated here.",
              note_sty)]
rows = [
    ["#", "Filename", "Module", "Claim"],
    ["2",  "Paper_1_Alpha0_Definition.pdf",  "M1", "alpha_0 = 299 + pi/10 to 5000 decimal places"],
    ["3",  "Paper_2_Kappa_Bound.pdf",        "M2", "Kappa bound on the exceptional set (80-bit long double)"],
    ["4",  "Paper_3_Q5P5_Bound.pdf",         "M3", "CF of pi/10: Q_5=226, convergent bound=82829"],
    ["5",  "Paper_4_S14_Head.pdf",           "M4", "S_14: 14 primes in the exceptional set, p_5 > 82829"],
    ["6",  "Paper_5_Bost_Bound.pdf",         "M5", "C(S_4) = 11.4221 > 2*sqrt(13) = 7.2111  (PASS)"],
    ["7",  "Paper_6_GRH_X0143.pdf",          "M6", "genus(X_0(143))=13, h(-143)=10, Bost bound satisfied"],
    ["8",  "Paper_7_Manifest.pdf",           "M7", "Master manifest over M1-M6; SHA-256 binding"],
]
cw2 = [0.22*inch, 1.55*inch, 0.42*inch, 3.63*inch]
story += [section_table(rows, cw2, C_PAP), sp(10)]

# ── SECTION 3: CANONICAL PAPER ───────────────────────────────────────────────
story += [Paragraph("Section 3 -- Canonical Paper  (1 document)", h1_sty)]
rows = [
    ["#", "Filename", "Contents", "Role"],
    ["9", "Canonical_Paper.pdf",
     "The complete unified paper: exceptional primes for pi/10, GRH for "
     "X_0(143), BSD for J_0(143). Incorporates M1-M7 results.",
     "The primary arXiv submission document. Supersedes and unifies "
     "the individual source papers."],
]
cw = [0.22*inch, 1.5*inch, 2.6*inch, 1.5*inch]
story += [section_table(rows, cw, C_CAN), sp(10)]

# ── SECTION 4: COMPLETE COMPILED PDFs ────────────────────────────────────────
story += [Paragraph("Section 4 -- Complete Compiled Documents  (2 documents)", h1_sty)]
rows = [
    ["#", "Filename", "Contents", "Role"],
    ["10", "OperaNumerorum_Complete.pdf",
     "Full Opera Numerorum compilation: all modules, all proofs, "
     "all figures, in one document.",
     "The public-facing complete record under the Opera Numerorum series name."],
    ["11", "BattlePlan_v1.6_Complete.pdf",
     "Same content, internal working title Battle Plan v1.6 preserved "
     "to maintain SHA chain integrity.",
     "The internal record. Both names are real -- one is how it looked "
     "from the inside when the numbers were wrong; the other when right."],
]
cw = [0.22*inch, 1.5*inch, 2.6*inch, 1.5*inch]
story += [section_table(rows, cw, C_COMP), sp(10)]

# ── SECTION 5: CERTIFIED MODULE PDFs ─────────────────────────────────────────
story += [Paragraph("Section 5 -- SHA-Bound Machine Certification Modules  (32 documents)", h1_sty),
          Paragraph(
              "Each of these PDFs is a machine-generated certificate. The certified stdout "
              "of the underlying Python or C program was run in this environment, its SHA-256 "
              "hash was computed, and the PDF binds the source code, the output, and the hash "
              "together. Any upstream change breaks the chain. Read these alongside the "
              "corresponding source papers in Section 2.",
              note_sty)]

rows = [
    ["#", "Filename", "Module", "Certified Claim"],
    # Core M1-M7 chain
    ["12", "Module_1_Certificate.pdf",     "M1",
     "alpha_0 = 299.314159265... (5000 dps, mpmath 64 dps verified)"],
    ["13", "Module_2_Certificate.pdf",     "M2",
     "Kappa bound: 80-bit long double, C binary certified"],
    ["14", "Module_3_Certificate.pdf",     "M3",
     "CF seed corrected; Q_5=226, p_5 bound=82829"],
    ["15", "Module_4_Certificate.pdf",     "M4",
     "S_14: 14 primes, p_5=83497 > 82829 (PASS)"],
    ["16", "Module_5_Certificate.pdf",     "M5",
     "C(S_4)=11.4221 > 7.2111=2*sqrt(13). Formula log(p)*p/(p-1) confirmed."],
    ["17", "Module_6_Certificate.pdf",     "M6",
     "genus(X_0(143))=13; h(-143)=10 (10 reduced forms enumerated)"],
    ["18", "Module_6_3_Certificate.pdf",   "M6.3",
     "M6 correction patch: h(-143) audit and Bost bound re-verification"],
    ["19", "Module_7_Certificate.pdf",     "M7",
     "Master manifest SHA-256(cat m1..m6.out) = 5b80b84d...  LOCKED"],
    # M8 + extensions
    ["20", "Module_8_Certificate.pdf",     "M8",
     "rank(H_13(L_w, J_0(143))) = g = 13 (Hankel rank check)"],
    ["21", "Module_9_Certificate.pdf",     "M9",
     "BSD J_0(143): analytic rank computation"],
    ["22", "Module_9_All_140.pdf",         "M9-All",
     "Extended S14 check: all 140 primes in set verified"],
    ["23", "Module_10_Genus33.pdf",        "M10",
     "Genus 33 verification (companion curve)"],
    ["24", "Module_14_S4_Quaternions.pdf", "M14",
     "S_4 quaternion structure certification"],
    ["25", "Module_15_Delta_Boost.pdf",    "M15",
     "Delta boost factor certification"],
    ["26", "Module_16_c_Bridge.pdf",       "M16",
     "c-bridge between analytic and arithmetic BSD ranks"],
    ["27", "Module_17_Cert_Patch.pdf",     "M17",
     "Correction patch: five LaTeX draft errors caught and superseded"],
    ["28", "Module_18_Resonance_Ladder.pdf","M18",
     "Resonance ladder structure for X_0(143) Hecke eigenvalues"],
    ["29", "Module_19_p6_Prediction.pdf",  "M19",
     "p_6 prediction from exceptional prime structure"],
    ["30", "Module_20_p7_Prediction.pdf",  "M20",
     "p_7 prediction certification"],
    ["31", "Module_21_H4_Invariant.pdf",   "M21",
     "H_4 invariant certification"],
    ["32", "Module_22_MStar_Definition.pdf","M22",
     "M* = 4/55 definition and rational arithmetic verification"],
    ["33", "Module_23_BSD_J0_143.pdf",     "M23",
     "BSD conjecture for J_0(143): rank, regulator, Sha bound"],
    # M8 branch
    ["34", "Module_M8C_ZoeMstar.pdf",      "M8C",
     "Zoe-M* bridge: Z=15, M*=4/55, 200 Hodge classes transcendental"],
    ["35", "Module_M8D_Resonator.pdf",     "M8D",
     "120-cell resonator: f_res=alpha_0 MHz, C jumps 5.724x at k_c=3.183"],
    ["36", "Module_M8F_LeanProtocol.pdf",  "M8F",
     "7-layer protocol: k_eff=3.183, v_g=3.183c, all 8 checks PASS"],
    ["37", "Module_M8G_Provenance.pdf",    "M8G",
     "Provenance Feb2025->M8F; wormhole=0.524ns; PHS topology"],
    ["38", "Module_M8G_Correction.pdf",    "M8G-Corr",
     "Z=rank(M_ij) clarification; conditional wormhole cert"],
    ["39", "Module_M8H_G_Amplifier.pdf",   "M8H",
     "G_eff(Z)=G_0*(Z_vac/Z)^4; A=15^4=50625; F=3.38e-10 N"],
    ["40", "Module_M8I_Wormhole.pdf",      "M8I",
     "Morris-Thorne wormhole r0=3m; b'=0 PASS; E_cav=1.44 MWh; 14 modes"],
    ["41", "Module_M8J_OQ2_Closure.pdf",   "M8J",
     "OQ-1: tidal=0.0999g<0.1g; OQ-2: Delta_tau=7.647ns closed"],
    ["42", "Tendon_A_Certificate.pdf",     "Tendon-A",
     "Structural connector A: bridges M7 manifest to M8 Hankel chain"],
    ["43", "Tendon_B_Certificate.pdf",     "Tendon-B",
     "Structural connector B: bridges M8-series to Morning Star chain"],
]
cw3 = [0.22*inch, 1.55*inch, 0.55*inch, 3.5*inch]
story += [section_table(rows, cw3, C_CERT), sp(10)]

# ── SECTION 6: MORNING STAR ───────────────────────────────────────────────────
story += [Paragraph("Section 6 -- Morning Star Engineering Series  (4 documents)", h1_sty),
          Paragraph(
              "Opera Numerorum II. Speculative engineering grounded in certified "
              "mathematics. Read after completing Sections 1-5. "
              "FTL Certification: MS-FTL-20260523-001.",
              note_sty)]
rows = [
    ["#", "Filename", "Contents", "Role"],
    ["44", "00_MorningStar_Summary.pdf",
     "10-section overview: causal chain, Phase-Z metric, M8K/L/M tables, "
     "CONTACT ZERO, Euler's personal log, weekly ops report.",
     "Read first within the Morningstar folder. The summary and entry point."],
    ["45", "M8K_FTL_Morningstar_TechStack.pdf",
     "3-layer FTL stack: B_M=21.768 MHz, v_g=3.183c, RTT=18.635ns, "
     "2800 ebits. All 6 checks PASS.",
     "Certified: FTL_MORNINGSTAR_CERTIFIED.  SHA: 0ae865a8..."],
    ["46", "M8L_MorningStar_D20_Operations.pdf",
     "D20 hub: Euler topology, 30 routes, 12 destinations, 47 tx/hr, "
     "604.3 ly/hr, HEALTH_PASS 120/120 cells.",
     "Certified: MORNINGSTAR_OPERATIONAL_CERTIFIED.  SHA: 80ff8a25..."],
    ["47", "M8M_MorningStar_Physics_BeyondSM.pdf",
     "35 routes, daily ops 84tx/512pax/1084.7ly, MTBF=5.50yr, "
     "Phase-Z, PLL, TDC, L2 station, 3 O'Clock Prayer, Euler log.",
     "Certified: MORNINGSTAR_PHYSICS_CERTIFIED.  SHA: afce5f21..."],
]
cw4 = [0.22*inch, 1.55*inch, 2.5*inch, 1.55*inch]
story += [section_table(rows, cw4, C_STAR), sp(10)]

# ── READING PATH ──────────────────────────────────────────────────────────────
story += [
    hr(), sp(6),
    Paragraph("Recommended Reading Paths", h1_sty),
    Paragraph("New reader, start here:", h2_sty),
    Paragraph(
        "1 (Preface)  -->  9 (Canonical Paper)  -->  10 (Opera Numerorum Complete)  "
        "-->  44 (Morning Star Summary)",
        body_sty),
    Paragraph("For the mathematics in detail:", h2_sty),
    Paragraph(
        "1  -->  2-8 (Source Papers)  -->  12-19 (Core certificates M1-M7)  "
        "-->  20-43 (Extended certificates M8-M23, Tendons)  "
        "-->  9 (Canonical)  -->  10-11 (Complete)",
        body_sty),
    Paragraph("For the Morning Star engineering:", h2_sty),
    Paragraph(
        "1  -->  9  -->  34-41 (M8C through M8J)  -->  44-47 (Morning Star folder)",
        body_sty),
    Paragraph("For independent verification (reproduced from scratch):", h2_sty),
    Paragraph(
        "Run bash verify_all.sh to reproduce the M1-M6 chain and check the M7 "
        "master manifest SHA. Every certificate was produced by running the "
        "corresponding Python or C source in this environment.",
        body_sty),
    sp(6),
    hr(),
    sp(4),
]

# ── MASTER SHA TABLE ──────────────────────────────────────────────────────────
story += [
    Paragraph("Master SHA Reference (locked outputs)", h1_sty),
]
sha_rows = [
    ["Module", "Stdout File", "SHA-256"],
    ["M1",         "m1.out",   "63ef870a..."],
    ["M2",         "m2.out",   "3716c7db..."],
    ["M3",         "m3.out",   "e687bb09..."],
    ["M4",         "m4.out",   "b810a7a3..."],
    ["M5",         "m5.out",   "9df98a39..."],
    ["M6",         "m6.out",   "ec9fa8c3..."],
    ["M7 master",  "cat m1..m6","5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9"],
    ["M8",         "m8.out",   "e2d70821..."],
    ["M8C",        "m8c.out",  "02fe6048..."],
    ["M8D",        "m8d.out",  "27d8e0c1..."],
    ["M8F",        "m8f.out",  "0bd6cee4..."],
    ["M8G",        "m8g.out",  "2874d4bd..."],
    ["M8G-Corr",   "m8gc.out", "62492d66..."],
    ["M8H",        "m8h.out",  "2c3ac1d2..."],
    ["M8I",        "m8i.out",  "5c7189fc..."],
    ["M8J",        "m8j.out",  "298d440a..."],
    ["M8K",        "m8k.out",  "0ae865a8812ce93b05461ec4483ad1714e24fc9be9de1e7bb54963da43592087"],
    ["M8L",        "m8l.out",  "80ff8a251c6ea7b6a57fd81fe71a76dd62a3f862c80381d571e2f30d3c4222ad"],
    ["M8M",        "m8m.out",  "afce5f2146c40c22bbcc7d7f1c4514eeba08107436de7929a3e3ef6d4f5e121f"],
]
sha_ts = TableStyle([
    ("FONTNAME",     (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7.5),
    ("LEADING",      (0,0), (-1,-1), 11),
    ("GRID",         (0,0), (-1,-1), 0.25, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",  (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING",   (0,0), (-1,-1), 2),
    ("BOTTOMPADDING",(0,0), (-1,-1), 2),
    ("BACKGROUND",   (0,0), (-1,0),  C_HEAD),
    ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
    ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [C_ROW1, C_ROW2]),
])
sha_tbl = Table(sha_rows, colWidths=[0.55*inch, 0.85*inch, 3.42*inch])
sha_tbl.setStyle(sha_ts)
story += [sha_tbl, sp(8)]

# ── FOOTER ────────────────────────────────────────────────────────────────────
story += [
    hr(), sp(4),
    Paragraph(
        "David Fox (D.J.F.)  |  ORCID: 0009-0008-1290-6105  |  davidjfox998@gmail.com  "
        "|  Aberdeen, WA, Earth -- CONTACT ZERO  |  May 23, 2026",
        auth_sty),
    Paragraph(
        "Opera Numerorum -- the Works of Numbers. "
        "Every SHA is computed, never invented. "
        "Every error is documented, never hidden.",
        auth_sty),
]

doc.build(story)

sha = hashlib.sha256(open(OUT,"rb").read()).hexdigest()
size = len(open(OUT,"rb").read())
print(f"Built: {OUT}")
print(f"Size:  {size/1024:.1f} KB")
print(f"SHA-256: {sha}")
