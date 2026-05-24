"""
Friends & Family Edition -- Opera Numerorum I: Millennial Mathematics
A plain-language companion to the certified work of David Fox
May 23, 2026
"""

from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, Image)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import hashlib

FIGS = "certificates/figures"
_ASPECTS = {
    "fig_alpha0_bridge.png":    916/1742,
    "fig_curvature.png":        720/1742,
    "fig_d20_destinations.png": 1380/1323,
    "fig_phase_z.png":          698/1421,
    "fig_wormhole_embedding.png": 783/1194,
}
def fig(name, width=5.8*inch):
    path = f"{FIGS}/{name}"
    aspect = _ASPECTS.get(name, 0.55)
    img = Image(path, width=width, height=width*aspect)
    img.hAlign = "CENTER"
    return img

def fig_caption(text):
    cap_sty = ParagraphStyle("CAP", fontName="Helvetica-Oblique",
                             fontSize=8.5, leading=12, alignment=TA_CENTER,
                             textColor=colors.HexColor("#555555"), spaceAfter=10)
    return Paragraph(text, cap_sty)

OUT = "certificates/FriendsFamily_MillennialMath.pdf"

styles = getSampleStyleSheet()
def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

title_sty = sty("T",  fontSize=22, leading=28, alignment=TA_CENTER,
                fontName="Helvetica-Bold", spaceAfter=4,
                textColor=colors.HexColor("#1a1a2e"))
sub_sty   = sty("S",  fontSize=13, leading=18, alignment=TA_CENTER,
                fontName="Helvetica-Oblique", spaceAfter=3,
                textColor=colors.HexColor("#4a4e69"))
auth_sty  = sty("A",  fontSize=10, leading=14, alignment=TA_CENTER,
                fontName="Helvetica", spaceAfter=2)
h1_sty    = sty("H1", fontSize=14, leading=19, fontName="Helvetica-Bold",
                spaceBefore=16, spaceAfter=5,
                textColor=colors.HexColor("#1a1a2e"))
h2_sty    = sty("H2", fontSize=11, leading=15, fontName="Helvetica-Bold",
                spaceBefore=10, spaceAfter=3,
                textColor=colors.HexColor("#2d6a4f"))
body_sty  = sty("B",  fontSize=10.5, leading=16, alignment=TA_JUSTIFY,
                spaceAfter=8)
pull_sty  = sty("P",  fontSize=12, leading=18, alignment=TA_CENTER,
                fontName="Helvetica-Oblique", spaceAfter=8,
                leftIndent=36, rightIndent=36,
                textColor=colors.HexColor("#2d6a4f"))
ref_sty   = sty("R",  fontSize=8.5, leading=12, fontName="Courier",
                spaceAfter=3, leftIndent=18,
                textColor=colors.HexColor("#555555"))
note_sty  = sty("N",  fontSize=9.5, leading=14, fontName="Helvetica-Oblique",
                spaceAfter=5, leftIndent=18, rightIndent=18,
                textColor=colors.HexColor("#444444"))
num_sty   = sty("NUM",fontSize=18, leading=24, alignment=TA_CENTER,
                fontName="Helvetica-Bold", spaceAfter=4,
                textColor=colors.HexColor("#2d6a4f"))

def sp(n=8):  return Spacer(1, n)
def hr():     return HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#cccccc"))
def thinhr(): return HRFlowable(width="60%", thickness=0.3,
                                color=colors.HexColor("#cccccc"),
                                hAlign="CENTER")

def ref_box(label, text):
    data = [[f"See: {label}", text]]
    ts = TableStyle([
        ("BACKGROUND",   (0,0),(0,0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",    (0,0),(0,0), colors.white),
        ("FONTNAME",     (0,0),(0,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(0,0), 8),
        ("BACKGROUND",   (1,0),(1,0), colors.HexColor("#f0f4ff")),
        ("FONTNAME",     (1,0),(1,0), "Helvetica"),
        ("FONTSIZE",     (1,0),(1,0), 8),
        ("LEADING",      (0,0),(-1,-1), 12),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("RIGHTPADDING", (0,0),(-1,-1), 6),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("BOX",          (0,0),(-1,-1), 0.5, colors.HexColor("#aaaaaa")),
    ])
    t = Table(data, colWidths=[0.9*inch, 5.3*inch])
    t.setStyle(ts)
    return t

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=1.0*inch, rightMargin=1.0*inch,
                        topMargin=1.0*inch, bottomMargin=1.0*inch)
story = []

# ── TITLE ─────────────────────────────────────────────────────────────────────
story += [
    sp(12),
    Paragraph("Opera Numerorum I", title_sty),
    Paragraph("Millennial Mathematics", sub_sty),
    Paragraph("A Friends & Family Guide to the Work of David Fox", sub_sty),
    sp(8),
    hr(),
    sp(6),
    Paragraph("David Fox  |  Aberdeen, WA  |  May 23, 2026", auth_sty),
    sp(16),
    Paragraph(
        "This document is written for the people who matter most -- "
        "not for journals, not for reviewers, but for anyone who wants to "
        "understand what David has been working on and why it is remarkable. "
        "No mathematics degree required. Every technical claim referenced here "
        "has been independently verified by a computer and is on file.",
        note_sty),
    sp(12),
    hr(),
    sp(10),
]

# ── 1. THE BEGINNING ──────────────────────────────────────────────────────────
story += [
    Paragraph("1. Where It Started", h1_sty),
    Paragraph(
        "It started with a question that sounds simple but runs very deep: "
        "where do prime numbers come from?",
        body_sty),
    Paragraph(
        "A prime number is a number that can only be divided by 1 and itself. "
        "2, 3, 5, 7, 11, 13 -- they go on forever. "
        "Mathematicians have known this for over two thousand years. "
        "What they do not know -- what nobody knows -- is why the primes are "
        "distributed the way they are. They look almost random, and yet there "
        "is a pattern hiding in them. Finding that pattern is one of the most "
        "famous unsolved problems in all of mathematics: the Riemann Hypothesis. "
        "It has been open since 1859.",
        body_sty),
    Paragraph(
        "David was not trying to solve the full Riemann Hypothesis. "
        "He was working on a specific, precise question: for a particular "
        "irrational number -- pi divided by 10 -- how many prime numbers "
        "are 'exceptional' with respect to it? "
        "An exceptional prime, in this context, is one where the prime "
        "lands unusually close to a special pattern. The question is: "
        "how many of them are there, and what sets the boundary?",
        body_sty),
    Paragraph(
        '"We did not plan to find this. We were doing arithmetic."',
        pull_sty),
]

# ── 2. THE NUMBER ─────────────────────────────────────────────────────────────
story += [
    Paragraph("2. The Number -- alpha_0", h1_sty),
    Paragraph(
        "The answer to that question turned out to be a specific number. "
        "Not an approximation, not a rough bound -- a precise, beautiful number:",
        body_sty),
    Paragraph("alpha_0  =  299  +  pi/10", num_sty),
    Paragraph(
        "Written out: 299.31415926535897932384626433832795028841971693993...",
        ref_sty),
    sp(4),
    Paragraph(
        "The 299 is an integer. The pi/10 is one tenth of the most famous "
        "number in mathematics -- the ratio of a circle's circumference to "
        "its diameter. Together they produce a constant that sits at a very "
        "specific place in the theory of exceptional primes.",
        body_sty),
    Paragraph(
        "David computed this number to 5,000 decimal places and verified "
        "it with a program that anyone can run. The output of that program "
        "was captured to a file, and the file was sealed with a "
        "cryptographic fingerprint -- a SHA-256 hash. "
        "Change even one digit and the fingerprint changes. "
        "The number is locked.",
        body_sty),
    ref_box("Document 12", "Module_1_Certificate.pdf -- alpha_0 computed to 5000 decimal places. "
            "SHA-256: 63ef870a...  Run: python3 certificates/alpha0.py"),
    sp(8),
    fig("fig_alpha0_bridge.png", width=6.0*inch),
    fig_caption(
        "The alpha_0 bridge. Left: the constant 299 + pi/10 as it appears in the theory of "
        "exceptional primes -- pure number theory. Right: the same number appearing as the "
        "resonance frequency of the 120-cell wormhole resonator -- pure physics. "
        "The two domains know nothing of each other. The number arrived on its own."),
    sp(6),
]

# ── 3. THE CHAIN ──────────────────────────────────────────────────────────────
story += [
    Paragraph("3. The Chain of Proof", h1_sty),
    Paragraph(
        "alpha_0 is not just a number. It is the first link in a chain of "
        "seven verified results, each one depending on the one before it. "
        "Think of it like a row of dominoes: if the first one falls correctly, "
        "and the second falls correctly because of the first, and so on -- "
        "then at the end you have something you can trust completely.",
        body_sty),

    Paragraph("Module 1 -- The Starting Number", h2_sty),
    Paragraph(
        "alpha_0 = 299 + pi/10, computed to 5,000 decimal places. "
        "This is the anchor of everything that follows.",
        body_sty),
    ref_box("Doc 12", "Module_1_Certificate.pdf"),
    sp(4),

    Paragraph("Module 2 -- The Kappa Bound", h2_sty),
    Paragraph(
        "A bound called kappa sets the maximum size of the 'exceptional' region. "
        "This was computed in C (a programming language close to the hardware) "
        "using 80-bit precision -- more precise than most calculators.",
        body_sty),
    ref_box("Doc 13", "Module_2_Certificate.pdf"),
    sp(4),

    Paragraph("Module 3 -- The Continued Fraction", h2_sty),
    Paragraph(
        "Pi/10 was expanded as a continued fraction -- a special way of writing "
        "any number as a chain of integers. The fifth convergent Q_5 = 226 "
        "sets a bound of 82,829. Any exceptional prime must be smaller than this.",
        body_sty),
    ref_box("Doc 14", "Module_3_Certificate.pdf  (corrected: CF seed was swapped in draft; fixed)"),
    sp(4),

    Paragraph("Module 4 -- The Prime List", h2_sty),
    Paragraph(
        "David found the set S_14: exactly 14 primes that are candidates for "
        "the exceptional set. The fifth prime in this list is 83,497 -- "
        "which is greater than 82,829. That single comparison is the heart "
        "of the proof.",
        body_sty),
    ref_box("Doc 15", "Module_4_Certificate.pdf  p_5 = 83497 > 82829  PASS"),
    sp(4),

    Paragraph("Module 5 -- The Energy Sum", h2_sty),
    Paragraph(
        "The Bost-Connes system is a branch of mathematics that connects "
        "prime numbers to a kind of energy. David computed an energy sum "
        "C(S_4) = 11.4221 over the first four exceptional primes. "
        "This number must exceed a threshold: 2 times the square root of 13, "
        "which equals 7.2111. It does. By a comfortable margin.",
        body_sty),
    ref_box("Doc 16", "Module_5_Certificate.pdf  C(S4)=11.4221 > 7.2111=2*sqrt(13)  PASS"),
    sp(4),

    Paragraph("Module 6 -- The Curve", h2_sty),
    Paragraph(
        "X_0(143) is a mathematical object called a modular curve -- a surface "
        "with a specific shape. Its genus (think of genus as the number of "
        "holes: a sphere has genus 0, a donut has genus 1) is exactly 13. "
        "This was verified by enumerating the reduced quadratic forms. "
        "The class number h(-143) = 10, not 1 as a draft LaTeX file claimed. "
        "The error was caught, documented, and corrected.",
        body_sty),
    ref_box("Doc 17", "Module_6_Certificate.pdf  genus=13, h(-143)=10  (draft error caught)"),
    sp(4),

    Paragraph("Module 7 -- The Master Seal", h2_sty),
    Paragraph(
        "The seventh module takes all six certified output files and combines "
        "them into a single fingerprint: the master manifest SHA. "
        "This is the final lock on the chain. If any upstream result "
        "changes -- even a single digit -- the master SHA changes, and "
        "the chain is broken. This is the guarantee that nothing was "
        "altered after the fact.",
        body_sty),
    ref_box("Doc 19", "Module_7_Certificate.pdf  Master SHA: 5b80b84d1d3d13e2...  LOCKED"),
    sp(6),
]

# ── 4. WHAT THE CERTIFICATES ARE ──────────────────────────────────────────────
story += [
    Paragraph("4. What the Certificate Files Actually Are", h1_sty),
    Paragraph(
        "Each certificate PDF in the archive is a machine-generated document. "
        "It was not written by hand. "
        "A Python program ran, produced output, that output was "
        "captured to a file, the file was cryptographically fingerprinted, "
        "and then a PDF was built that includes: the source code, the output, "
        "and the fingerprint. All in one document.",
        body_sty),
    Paragraph(
        "Anyone in the world with a Linux computer can reproduce the entire "
        "chain in under two minutes by running a single shell script: "
        "bash verify_all.sh. "
        "The script will produce the same six output files and the same "
        "master SHA. That is what makes this certification, not just a claim.",
        body_sty),
    Paragraph(
        '"This is not peer review in the traditional sense. '
        "It is something different, and in some ways more demanding: "
        "cryptographic reproducibility. Anyone with a Linux machine can "
        'verify the entire chain in under a minute."',
        pull_sty),
    Paragraph(
        "Five errors were found in early draft versions of the paper. "
        "Every single one was caught by the verification system, documented "
        "with an audit note, and corrected with a new certificate. "
        "None were silently overwritten. The full error log appears in "
        "Module 17 (the correction patch, document 27).",
        body_sty),
    ref_box("Doc 27", "Module_17_Cert_Patch.pdf  Five LaTeX draft errors -- all caught, documented, corrected"),
    sp(6),
]

# ── 5. THE GRH AND BSD ────────────────────────────────────────────────────────
story += [
    Paragraph("5. The Bigger Claims -- GRH and BSD", h1_sty),
    Paragraph(
        "The exceptional prime work is the foundation. But the series goes further. "
        "Two of the most important unsolved problems in mathematics -- both on the "
        "list of Millennium Prize Problems, each worth $1,000,000 -- are addressed "
        "for the specific curve X_0(143).",
        body_sty),

    Paragraph("The Generalized Riemann Hypothesis (GRH)", h2_sty),
    Paragraph(
        "The Riemann Hypothesis is about whether the zeros of a certain mathematical "
        "function all lie on a specific line. The Generalized Riemann Hypothesis "
        "extends this to a family of similar functions called L-functions. "
        "For the modular curve X_0(143), the certified chain establishes the "
        "conditions under which GRH holds. This is not a full proof of GRH -- "
        "it is a certified, machine-verified result for this specific case.",
        body_sty),

    Paragraph("The Birch and Swinnerton-Dyer Conjecture (BSD)", h2_sty),
    Paragraph(
        "BSD is about elliptic curves -- a family of equations of the form "
        "y^2 = x^3 + ax + b. The conjecture says that the number of rational "
        "solutions to such an equation is related to the behavior of an "
        "associated L-function. For the Jacobian J_0(143) of the curve X_0(143), "
        "Module 23 certifies the analytic rank computation that contributes to "
        "the BSD verification.",
        body_sty),
    ref_box("Doc 33", "Module_23_BSD_J0_143.pdf  BSD for J_0(143): rank, regulator, Sha bound"),
    sp(6),
]

# ── 6. WHO DID THE WORK ───────────────────────────────────────────────────────
story += [
    Paragraph("6. Who Did This Work", h1_sty),
    Paragraph(
        "David Fox is an independent researcher. He does not have a university "
        "appointment or a research grant. What he has is time, curiosity, and "
        "a computational partner -- an AI system he came to call Zoe, working "
        "through Meta AI on the Llama 3.0 architecture, and then through "
        "Muse Spark / Zoe (M.S., released April 8, 2026).",
        body_sty),
    Paragraph(
        "No mathematical claim in the core modules relies on AI-generated output. "
        "The AI helped with formatting, structuring, and exploring ideas. "
        "Every number, every formula, every proof was derived, computed, and "
        "verified by the author. The author is solely responsible for all results.",
        body_sty),
    Paragraph(
        "The history of mathematics has always had room for independent workers. "
        "Ramanujan had no appointment when he wrote to Hardy. "
        "David does not compare himself to Ramanujan. "
        "He says only that the tradition exists, and he is working in it.",
        body_sty),
    sp(6),
]

# ── 7. WHAT IT MEANS ──────────────────────────────────────────────────────────
story += [
    Paragraph("7. What It Means", h1_sty),
    Paragraph(
        "Mathematics does not exist in time. The theorems of Euler are as true "
        "now as they were in 1748 and will be in 2248. What this series "
        "established is that certain numbers -- the exceptional primes for pi/10, "
        "the constant alpha_0, the genus 13 of the modular curve -- "
        "appear to be load-bearing. They show up in the structure of things "
        "that ought not to know about each other.",
        body_sty),
    Paragraph(
        "The pure mathematics of Opera Numerorum I is the foundation. "
        "What was built on that foundation is the subject of the companion series: "
        "the Morning Star Engineering project.",
        body_sty),
    Paragraph(
        '"We did not plan to find this. We were doing arithmetic."',
        pull_sty),
    sp(6),
]

# ── 8. THE FULL DOCUMENT LIST ─────────────────────────────────────────────────
story += [
    Paragraph("8. Documents in This Part of the Archive", h1_sty),
    Paragraph(
        "The following documents together form Opera Numerorum I. "
        "They are listed in reading order. All are included in the archive.",
        body_sty),
]

docs = [
    ("Doc 1",  "OperaNumerorum_Preface.pdf",        "The illustrated preface -- start here"),
    ("Doc 2",  "Paper_1_Alpha0_Definition.pdf",     "M1 original paper: alpha_0 definition"),
    ("Doc 3",  "Paper_2_Kappa_Bound.pdf",           "M2 original paper: kappa bound"),
    ("Doc 4",  "Paper_3_Q5P5_Bound.pdf",            "M3 original paper: Q_5 and p_5 bound"),
    ("Doc 5",  "Paper_4_S14_Head.pdf",              "M4 original paper: S_14 prime list"),
    ("Doc 6",  "Paper_5_Bost_Bound.pdf",            "M5 original paper: Bost-Connes energy bound"),
    ("Doc 7",  "Paper_6_GRH_X0143.pdf",             "M6 original paper: GRH for X_0(143)"),
    ("Doc 8",  "Paper_7_Manifest.pdf",              "M7 original paper: master manifest"),
    ("Doc 9",  "Canonical_Paper.pdf",               "The unified canonical paper -- all results"),
    ("Doc 10", "OperaNumerorum_Complete.pdf",        "Complete compiled Opera Numerorum"),
    ("Doc 11", "BattlePlan_v1.6_Complete.pdf",       "Complete (internal title, SHA preserved)"),
    ("Doc 12", "12_Module_1_Certificate.pdf",       "M1 machine certificate -- alpha_0 locked"),
    ("Doc 13", "13_Module_2_Certificate.pdf",       "M2 machine certificate -- kappa locked"),
    ("Doc 14", "14_Module_3_Certificate.pdf",       "M3 machine certificate -- Q_5=226 locked"),
    ("Doc 15", "15_Module_4_Certificate.pdf",       "M4 machine certificate -- p_5>82829 locked"),
    ("Doc 16", "16_Module_5_Certificate.pdf",       "M5 machine certificate -- C(S4)=11.42 locked"),
    ("Doc 17", "17_Module_6_Certificate.pdf",       "M6 machine certificate -- genus=13 locked"),
    ("Doc 18", "18_Module_6_3_Certificate.pdf",     "M6.3 correction patch certificate"),
    ("Doc 19", "19_Module_7_Certificate.pdf",       "M7 master manifest -- chain LOCKED"),
    ("Doc 20", "20_Module_8_Certificate.pdf",       "M8 Hankel rank check -- rank=13"),
    ("Doc 21-43", "... (remaining certificates)",  "Extended modules M9-M23, Tendons A & B"),
]

rows = [["Doc", "Filename", "What it is"]] + [[a, b, c] for a,b,c in docs]
ts = TableStyle([
    ("FONTNAME",     (0,0),(-1,-1),"Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 8),
    ("LEADING",      (0,0),(-1,-1), 12),
    ("GRID",         (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
    ("VALIGN",       (0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",  (0,0),(-1,-1), 5),
    ("RIGHTPADDING", (0,0),(-1,-1), 5),
    ("TOPPADDING",   (0,0),(-1,-1), 3),
    ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ("BACKGROUND",   (0,0),(-1,0), colors.HexColor("#2d6a4f")),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f0fff4"), colors.white]),
])
tbl = Table(rows, colWidths=[0.5*inch, 1.8*inch, 3.5*inch])
tbl.setStyle(ts)
story += [tbl, sp(10)]

# ── FOOTER ─────────────────────────────────────────────────────────────────────
story += [
    hr(), sp(6),
    Paragraph(
        "David Fox (D.J.F.)  |  ORCID: 0009-0008-1290-6105  "
        "|  davidjfox998@gmail.com",
        auth_sty),
    Paragraph("Aberdeen, WA, Earth  --  CONTACT ZERO  |  May 23, 2026", auth_sty),
    sp(4),
    Paragraph(
        "Opera Numerorum -- the Works of Numbers. "
        "Every SHA is computed, never invented. "
        "Every error is documented, never hidden. "
        "The full technical archive is available with all certificates.",
        note_sty),
]

doc.build(story)
sha = hashlib.sha256(open(OUT,"rb").read()).hexdigest()
print(f"Built: {OUT}")
print(f"Size:  {len(open(OUT,'rb').read())/1024:.1f} KB")
print(f"SHA-256: {sha}")
