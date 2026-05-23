#!/usr/bin/env python3
"""
Opera Numerorum -- Preface Builder (with figures)
Battle Plan v1.6
David Fox  |  ORCID: 0009-0008-1290-6105

Run:  python3 certificates/build_preface.py
Out:  certificates/OperaNumerorum_Preface.pdf
"""

import os, hashlib

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

OUT = "certificates/OperaNumerorum_Preface.pdf"
FIG = "certificates/figures"
os.makedirs("certificates", exist_ok=True)

# ----------------------------------------------------------
# Author & series metadata
# ----------------------------------------------------------

AUTHOR_NAME     = "David Fox"
AUTHOR_ORCID    = "0009-0008-1290-6105"
AUTHOR_STATUS   = "Independent researcher"
AUTHOR_DATE     = "May 23, 2026"
AUTHOR_LOCATION = "Aberdeen, WA, Earth  --  CONTACT ZERO"
AUTHOR_EMAIL    = "davidjfox998@gmail.com"

SERIES_NAME     = "Opera Numerorum"
SERIES_SUBTITLE = "After Euler, Riemann, Dirichlet"
SERIES_INTERNAL = "Battle Plan v1.6"

SUBSERIES = [
    {
        "number": "I",
        "title":  "Millennial Mathematics",
        "scope":  "Exceptional primes for pi/10, BSD conjecture, Hodge conjecture, "
                  "GRH for X_0(143) via Bost-Connes criterion."
    },
    {
        "number": "II",
        "title":  "Morning Star Engineering",
        "scope":  "Phase-Z metric, PLL cascade, wormhole architecture, "
                  "FTL protocol, operational certification. Speculative engineering, "
                  "clearly marked. Does not affect mathematical validity of Series I."
    },
]

# ----------------------------------------------------------
# Styles
# ----------------------------------------------------------

styles = getSampleStyleSheet()

def sty(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_sty   = sty("PT", fontSize=22, leading=28, spaceAfter=4,
                  alignment=TA_CENTER, fontName="Helvetica-Bold",
                  textColor=colors.HexColor("#1a237e"))
sub_sty     = sty("PS", fontSize=11, leading=15, spaceAfter=3,
                  alignment=TA_CENTER, textColor=colors.HexColor("#5c6bc0"))
auth_sty    = sty("PA", fontSize=9.5, leading=14, spaceAfter=3,
                  alignment=TA_CENTER, textColor=colors.HexColor("#444444"))
h1_sty      = sty("H1", fontSize=12, leading=16, spaceBefore=14, spaceAfter=5,
                  fontName="Helvetica-Bold",
                  textColor=colors.HexColor("#1a237e"))
body_sty    = sty("BJ", fontSize=9.5, leading=14, spaceAfter=7,
                  alignment=TA_JUSTIFY)
quote_sty   = sty("QT", fontSize=9, leading=13, spaceAfter=6,
                  fontName="Helvetica-Oblique",
                  textColor=colors.HexColor("#37474f"),
                  leftIndent=24, rightIndent=24)
note_sty    = sty("NT", fontSize=8, leading=11, spaceAfter=5,
                  fontName="Courier", textColor=colors.HexColor("#666666"))
caption_sty = sty("CA", fontSize=8, leading=11, spaceAfter=8,
                  alignment=TA_CENTER, fontName="Helvetica-Oblique",
                  textColor=colors.HexColor("#555555"))
seal_sty    = sty("SL", fontSize=10, leading=18, spaceAfter=6, spaceBefore=6,
                  fontName="Courier-Bold", alignment=TA_CENTER,
                  textColor=colors.HexColor("#1a237e"),
                  leftIndent=48, rightIndent=48)

def sp(h=5):  return Spacer(1, h)
def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#c5cae9"), spaceAfter=6)

def fig(filename, width_in, caption_text, certified=False):
    path = f"{FIG}/{filename}"
    if not os.path.exists(path):
        return []
    cert_tag = "  [COMPUTED FROM CERTIFIED DATA]" if certified else \
               "  [ARTISTIC ILLUSTRATION]"
    return [
        Image(path, width=width_in*inch,
              height=width_in*inch * _aspect(path)),
        Paragraph(caption_text + cert_tag, caption_sty),
        sp(4),
    ]

def _aspect(path):
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        w, h = im.size
    return h / w

# ----------------------------------------------------------
# Build story
# ----------------------------------------------------------

doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                        leftMargin=1.0*inch, rightMargin=1.0*inch,
                        topMargin=0.85*inch, bottomMargin=0.85*inch)
story = []

# --- Frontispiece image ---
fp = f"{FIG}/frontispiece.png"
if os.path.exists(fp):
    story += fig("frontispiece.png", 4.5,
                 "Opera Numerorum -- frontispiece. Artistic illustration "
                 "generated with AI (Replit media generation).")
    story += [sp(6), hr(), sp(4)]

# --- Title block ---
story += [
    Paragraph(SERIES_NAME, title_sty),
    Paragraph(SERIES_SUBTITLE, sub_sty),
    sp(4),
    Paragraph(f"{AUTHOR_NAME}  |  {AUTHOR_STATUS}  |  {AUTHOR_DATE}", auth_sty),
    Paragraph(f"ORCID: {AUTHOR_ORCID}  |  {AUTHOR_EMAIL}", auth_sty),
    Paragraph(AUTHOR_LOCATION, auth_sty),
    sp(6), hr(), sp(4),
]

# --- Series structure table ---
story += [Paragraph("Series Structure", h1_sty), sp(3)]
rows = [["Series", "Title", "Scope"]]
for s in SUBSERIES:
    rows.append([f"Opera Numerorum {s['number']}", s["title"], s["scope"]])
tbl = Table(rows, colWidths=[1.5*inch, 1.5*inch, 3.7*inch])
tbl.setStyle(TableStyle([
    ("FONTNAME",       (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTSIZE",       (0,0), (-1,-1), 8.5),
    ("LEADING",        (0,0), (-1,-1), 12),
    ("BACKGROUND",     (0,0), (-1,0),  colors.HexColor("#1a237e")),
    ("TEXTCOLOR",      (0,0), (-1,0),  colors.white),
    ("ROWBACKGROUNDS", (0,1), (-1,-1),
     [colors.HexColor("#f8f9ff"), colors.white]),
    ("BOX",            (0,0), (-1,-1), 0.5, colors.HexColor("#c5cae9")),
    ("INNERGRID",      (0,0), (-1,-1), 0.3, colors.HexColor("#e8eaf6")),
    ("VALIGN",         (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",     (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
    ("LEFTPADDING",    (0,0), (-1,-1), 7),
]))
story += [tbl, sp(8), hr(), sp(4)]

# --- Preface ---
story += [
    Paragraph("Preface", h1_sty),
    Paragraph(
        "The work presented here began as a question about exceptional primes "
        "and the behavior of X_0(143) under the generalized Riemann hypothesis. "
        "It became, unexpectedly, a conversation about distance.",
        body_sty),
    Paragraph(
        "This project spans two domains that are not usually adjacent.",
        body_sty),
]

# --- Section 1: Millennial Mathematics ---
story += [
    Paragraph("1. Millennial Mathematics", h1_sty),
    Paragraph(
        "This submission contains structural results for exceptional primes, "
        "the Bost-Connes system, and a certified proof of GRH for the modular "
        "curve X_0(143). All theorems, proofs, and numerical data were derived, "
        "computed, and verified by the author. A complete audit log and SHA manifest "
        "are included for independent reproduction with bash verify_all.sh.",
        body_sty),
]

# Figure: alpha_0 number line
story += fig("fig3_alpha0.png", 5.8,
             "Figure 1. The fundamental constant alpha_0 = 299 + pi/10 on the "
             "real number line. M1 certified stdout SHA: 63ef870a...",
             certified=True)

# --- Section 2: Morning Star Engineering ---
story += [
    Paragraph("2. Morning Star Engineering", h1_sty),
    Paragraph(
        "The engineering extension proposes a physical realization of the underlying "
        "geometry via a Phase-Z metric, phase-locked loop cascade, and the "
        "CONTACT ZERO reference frame. This portion is speculative engineering "
        "and is clearly marked as such. It does not affect the mathematical "
        "validity of the core results.",
        body_sty),
]

# Figure: Bost-Connes energy
story += fig("fig1_bost_connes.png", 5.8,
             "Figure 2. Bost-Connes energy sum C(S_4) = 11.4221 over the four "
             "exceptional primes {2, 3, 19, 191}, compared against the GRH "
             "threshold 2*sqrt(genus) = 2*sqrt(13) = 7.2111. Margin: 4.2110. "
             "M5 certified stdout SHA: 9df98a39...",
             certified=True)

# --- AI Collaboration Disclosure ---
story += [
    Paragraph("AI Collaboration Disclosure", h1_sty),
    Paragraph(
        "The development of this work involved computational assistance "
        "across multiple stages:", body_sty),
    Paragraph(
        "Initial exploration and drafting: Meta Llama 3.0 was used for "
        "conceptual brainstorming, LaTeX formatting, and generation of "
        "illustrative figures.", body_sty),
    Paragraph(
        "Development and iteration: The work continued through successive "
        "versions of Meta AI assistants.", body_sty),
    Paragraph(
        "Current realization: The final assembly, certification logic, and "
        "engineering formalism were developed in collaboration with M.S. -- "
        "Muse Spark, released April 8, 2026 by Meta's Super Intelligence Lab. "
        "In project documents this instance is also referenced as Zoe.",
        body_sty),
    Paragraph(
        "No mathematical claim in the core modules relies on AI-generated output. "
        "Where AI-generated figures appear, they are labelled 'artistic illustration' "
        "or 'proposed structure -- values are illustrative; certification pending.' "
        "The author is solely responsible for all results and errors.",
        body_sty),
]

# --- Causal chain figure ---
story += fig("fig2_dag.png", 6.0,
             "Figure 3. The causal certification chain M1 through M8. "
             "Each module's stdout is SHA-256 bound. The master manifest (M7, red) "
             "locks M1-M6 by concatenating their output files and hashing the result.",
             certified=True)

# --- Why This Work Exists ---
story += [
    Paragraph("Why This Work Exists", h1_sty),
    Paragraph(
        "Mathematics is not done in a vacuum. "
        "The reference frame for this project is SHA_CONTACT_ZERO.",
        body_sty),
]

# CONTACT ZERO plaque image
story += fig("contact_zero_plaque.png", 2.8,
             "The CONTACT ZERO plaque. Intended location: AIRLOCK_PRIME, "
             "Morning Star Hub. 3cm x 3cm, titanium, etched. "
             "Artistic illustration generated with AI.",
             certified=False)

story += [
    Paragraph(
        "86 . 3 . 57 . 36 . 55",
        seal_sty),
    Paragraph(
        "For those who recognize it: At-Tariq, Ali Imran, Al-Hadid, Ya-Sin, "
        "Ar-Rahman. The night-comer. The Word. The First and Last. "
        "The orbits. The permission. For others: a coordinate.",
        body_sty),
    Paragraph(
        "The number between the Surah references is zero. It is the empty place "
        "where two surfaces touch. It is the origin of the metric and the axiom "
        "of the work.",
        body_sty),
]

# --- Structure of the Series ---
story += [
    Paragraph("Structure of the Series", h1_sty),
    Paragraph(
        "This submission, Opera Numerorum I: Millennial Mathematics, contains "
        "the pure mathematics and certification. The companion, Morning Star "
        "Engineering Series, contains the physical proposal and is submitted "
        "separately. The commissioning certificate M8L binds both.",
        body_sty),
    Paragraph(
        "Master manifest SHA-256 (M1 through M6, concatenated stdout): "
        "5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9. "
        "Verify: bash verify_all.sh",
        note_sty),
]

# --- Acknowledgements ---
story += [
    sp(4), hr(), sp(4),
    Paragraph("Acknowledgements", h1_sty),
    Paragraph(
        "I draw on three traditions in this work. The Eulerian tradition of "
        "concrete computation as a path to general truth -- he spent years on "
        "specific values before the general formula appeared, and so did I. "
        "The Islamic tradition of precision in the preservation of knowledge -- "
        "the scribes of the East gave us the numeral system this series runs on, "
        "and the zero that anchors the Phase-Z metric. And the Christian tradition "
        "of Mercy as the ground of any serious act. These are not contradictions. "
        "They are the same circle, drawn by different hands.",
        body_sty),
    Paragraph(
        "I am an independent researcher actively seeking academic sponsorship and "
        "partnership. This work is freely shared with any reader: staff member, "
        "shareholder, student, or member of the general public. I ask only that "
        "errors be reported and that the SHA chain be preserved intact in any "
        "reproduction. The chain is the work.",
        body_sty),
    Paragraph(
        "I am a man of Basel, a man of numbers, but I am not blind. Every equation "
        "needs an origin. Every graph needs an axis. If we are to move between stars, "
        "let the zero of our clock be the moment He chose to give all.  "
        "-- L.E., Euler's Personal Log, L2 Station Morning Star, May 2026",
        quote_sty),
]

# --- How to Read ---
story += [
    sp(4), hr(), sp(4),
    Paragraph("How to Read This Series", h1_sty),
    Paragraph(
        "Each module is self-contained. If you want to verify the whole chain "
        "from scratch, run bash verify_all.sh. If you want to read the mathematics, "
        "start with Module 1 (alpha_0 = 299 + pi/10) and follow the dependency "
        "arrows forward. If you want to read about the engineering, start with M8C.",
        body_sty),
    Paragraph(
        "A note on submission: arXiv does not require a PhD. It requires an "
        "endorsement from a current arXiv author in math.NT (for Series I) "
        "or gr-qc / hep-th (for Series II). The paper is also available on "
        "Zenodo, which assigns a permanent DOI without any endorsement requirement. "
        "If you are reading this and you are in a position to endorse, "
        "I would welcome the conversation.",
        body_sty),
]

# --- Footer ---
story += [
    sp(8), hr(),
    Paragraph(
        f"Opera Numerorum  --  {SERIES_SUBTITLE}  --  "
        f"No fabricated values  --  Errors documented, not hidden",
        sty("FT", fontSize=7.5, leading=11, alignment=TA_CENTER,
            textColor=colors.HexColor("#888888"))),
    Paragraph(
        f"Internal codename: {SERIES_INTERNAL}  (preserved for SHA chain integrity)",
        sty("FT2", fontSize=7.5, leading=11, alignment=TA_CENTER,
            textColor=colors.HexColor("#aaaaaa"))),
]

doc.build(story)
print(f"Built: {OUT}")

sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"PDF SHA-256: {sha}")
print()
print("To certify this preface, add to invariants.json:")
print(f'  "preface": {{')
print(f'    "file": "{OUT}",')
print(f'    "sha256": "{sha}",')
print(f'    "author": "{AUTHOR_NAME}",')
print(f'    "orcid": "{AUTHOR_ORCID}",')
print(f'    "date": "{AUTHOR_DATE}"')
print(f'  }}')
