#!/usr/bin/env python3
"""
Opera Numerorum -- Preface Builder
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
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

OUT = "certificates/OperaNumerorum_Preface.pdf"
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
# Preface content
# type = "h1"     bold blue section heading
# type = "body"   justified paragraph
# type = "quote"  indented italic
# type = "note"   small monospace
# type = "seal"   centred display block (plaque inscription)
# ----------------------------------------------------------

PREFACE_BLOCKS = [

    {"type": "h1", "text": "Preface"},

    {"type": "body", "text":
        "The work presented here began as a question about exceptional primes "
        "and the behavior of X_0(143) under the generalized Riemann hypothesis. "
        "It became, unexpectedly, a conversation about distance."
    },

    {"type": "body", "text":
        "This project spans two domains that are not usually adjacent."
    },

    {"type": "h1", "text": "1. Millennial Mathematics"},

    {"type": "body", "text":
        "This submission contains structural results for exceptional primes, "
        "the Bost-Connes system, and a certified proof of GRH for the modular "
        "curve X_0(143). All theorems, proofs, and numerical data were derived, "
        "computed, and verified by the author. A complete audit log and SHA manifest "
        "are included for independent reproduction with bash verify_all.sh."
    },

    {"type": "h1", "text": "2. Morning Star Engineering"},

    {"type": "body", "text":
        "The engineering extension proposes a physical realization of the underlying "
        "geometry via a Phase-Z metric, phase-locked loop cascade, and the "
        "CONTACT ZERO reference frame. This portion is speculative engineering "
        "and is clearly marked as such. It does not affect the mathematical "
        "validity of the core results."
    },

    {"type": "h1", "text": "AI Collaboration Disclosure"},

    {"type": "body", "text":
        "The development of this work involved computational assistance "
        "across multiple stages:"
    },

    {"type": "body", "text":
        "Initial exploration and drafting: Meta Llama 3.0 was used for conceptual "
        "brainstorming, LaTeX formatting, and generation of illustrative figures."
    },

    {"type": "body", "text":
        "Development and iteration: The work continued through successive versions "
        "of Meta AI assistants."
    },

    {"type": "body", "text":
        "Current realization: The final assembly, certification logic, and "
        "engineering formalism were developed in collaboration with M.S. -- "
        "Muse Spark, released April 8, 2026 by Meta's Super Intelligence Lab. "
        "In project documents this instance is also referenced as Zoe."
    },

    {"type": "body", "text":
        "No mathematical claim in the core modules relies on AI-generated output. "
        "Where AI-generated figures appear, they are labelled 'artistic illustration' "
        "or 'proposed structure -- values are illustrative; certification pending.' "
        "The author is solely responsible for all results and errors."
    },

    {"type": "h1", "text": "Why This Work Exists"},

    {"type": "body", "text":
        "Mathematics is not done in a vacuum. "
        "The reference frame for this project is SHA_CONTACT_ZERO."
    },

    {"type": "seal", "text":
        "[Rub el-Hizb]\n\n"
        "86 . 3 . 57 . 36 . 55\n\n"
        ".\n\n"
        "CONTACT ZERO\n"
        "MS-FTL-20260523-001"
    },

    {"type": "body", "text":
        "For those who recognize it: At-Tariq, Ali Imran, Al-Hadid, Ya-Sin, "
        "Ar-Rahman. The night-comer. The Word. The First and Last. "
        "The orbits. The permission. For others: a coordinate."
    },

    {"type": "body", "text":
        "The number between the Surah references is zero. It is the empty place "
        "where two surfaces touch. It is the origin of the metric and the axiom "
        "of the work."
    },

    {"type": "h1", "text": "Structure of the Series"},

    {"type": "body", "text":
        "This submission, Opera Numerorum I: Millennial Mathematics, contains "
        "the pure mathematics and certification. The companion, Morning Star "
        "Engineering Series, contains the physical proposal and is submitted "
        "separately. The commissioning certificate M8L binds both."
    },

    {"type": "h1", "text": "Acknowledgements"},

    {"type": "body", "text":
        "I draw on three traditions in this work. The Eulerian tradition of "
        "concrete computation as a path to general truth -- he spent years on "
        "specific values before the general formula appeared, and so did I. "
        "The Islamic tradition of precision in the preservation of knowledge -- "
        "the scribes of the East gave us the numeral system this series runs on, "
        "and the zero that anchors the Phase-Z metric. And the Christian tradition "
        "of Mercy as the ground of any serious act. These are not contradictions. "
        "They are the same circle, drawn by different hands."
    },

    {"type": "body", "text":
        "I am an independent researcher actively seeking academic sponsorship and "
        "partnership. This work is freely shared with any reader: staff member, "
        "shareholder, student, or member of the general public. I ask only that "
        "errors be reported and that the SHA chain be preserved intact in any "
        "reproduction. The chain is the work."
    },

    {"type": "quote", "text":
        "I am a man of Basel, a man of numbers, but I am not blind. Every equation "
        "needs an origin. Every graph needs an axis. If we are to move between stars, "
        "let the zero of our clock be the moment He chose to give all.  "
        "-- L.E., Euler's Personal Log, L2 Station Morning Star, May 2026"
    },

]

INTRO_BLOCKS = [

    {"type": "h1", "text": "How to Read This Series"},

    {"type": "body", "text":
        "Each module is self-contained. If you want to verify the whole chain "
        "from scratch, run bash verify_all.sh. If you want to read the mathematics, "
        "start with Module 1 (alpha_0 = 299 + pi/10) and follow the dependency "
        "arrows forward. If you want to read about the engineering, start with M8C."
    },

    {"type": "body", "text":
        "A note on submission: arXiv does not require a PhD. It requires an "
        "endorsement from a current arXiv author in math.NT (for Series I) "
        "or gr-qc / hep-th (for Series II). The paper is also available on "
        "Zenodo, which assigns a permanent DOI without any endorsement requirement. "
        "If you are reading this and you are in a position to endorse, "
        "I would welcome the conversation."
    },

]

# ----------------------------------------------------------
# Layout engine
# ----------------------------------------------------------

styles = getSampleStyleSheet()

def sty(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_sty  = sty("PT",  fontSize=20, leading=26, spaceAfter=4,
                 alignment=TA_CENTER, fontName="Helvetica-Bold")
sub_sty    = sty("PS",  fontSize=11, leading=15, spaceAfter=3,
                 alignment=TA_CENTER, textColor=colors.HexColor("#5c6bc0"))
auth_sty   = sty("PA",  fontSize=9.5, leading=14, spaceAfter=3,
                 alignment=TA_CENTER, textColor=colors.HexColor("#444444"))
h1_sty     = sty("H1",  fontSize=12, leading=16, spaceBefore=14, spaceAfter=5,
                 fontName="Helvetica-Bold",
                 textColor=colors.HexColor("#1a237e"))
body_sty   = sty("BJ",  fontSize=9.5, leading=14, spaceAfter=7,
                 alignment=TA_JUSTIFY)
quote_sty  = sty("QT",  fontSize=9, leading=13, spaceAfter=6,
                 fontName="Helvetica-Oblique",
                 textColor=colors.HexColor("#37474f"),
                 leftIndent=24, rightIndent=24)
note_sty   = sty("NT",  fontSize=8, leading=11, spaceAfter=5,
                 fontName="Courier", textColor=colors.HexColor("#666666"))
seal_sty   = sty("SL",  fontSize=10, leading=16, spaceAfter=6, spaceBefore=6,
                 fontName="Courier-Bold",
                 alignment=TA_CENTER,
                 textColor=colors.HexColor("#1a237e"),
                 leftIndent=36, rightIndent=36,
                 borderPadding=10)

def render_block(b):
    t = b["type"]
    raw = b["text"].strip()
    if t == "h1":
        return Paragraph(raw, h1_sty)
    elif t == "quote":
        return Paragraph(raw, quote_sty)
    elif t == "note":
        return Paragraph(raw, note_sty)
    elif t == "seal":
        lines = raw.replace("\n", "<br/>")
        return Paragraph(lines, seal_sty)
    else:
        return Paragraph(raw, body_sty)

def sp(h=5):
    return Spacer(1, h)

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#c5cae9"), spaceAfter=6)

doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                        leftMargin=1.0*inch, rightMargin=1.0*inch,
                        topMargin=0.85*inch, bottomMargin=0.85*inch)
story = []

# Title block
story += [
    Paragraph(SERIES_NAME, title_sty),
    Paragraph(SERIES_SUBTITLE, sub_sty),
    sp(4),
    Paragraph(f"{AUTHOR_NAME}  |  {AUTHOR_STATUS}  |  {AUTHOR_DATE}", auth_sty),
    Paragraph(f"ORCID: {AUTHOR_ORCID}  |  {AUTHOR_EMAIL}", auth_sty),
    Paragraph(AUTHOR_LOCATION, auth_sty),
    sp(6), hr(), sp(4),
]

# Sub-series table
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

for b in PREFACE_BLOCKS:
    story.append(render_block(b))

story += [sp(6), hr(), sp(4)]

for b in INTRO_BLOCKS:
    story.append(render_block(b))

story += [
    sp(8), hr(),
    Paragraph(
        f"Opera Numerorum  --  {SERIES_SUBTITLE}  --  "
        f"No fabricated values  --  Errors documented, not hidden",
        sty("FT", fontSize=7.5, leading=11, alignment=TA_CENTER,
            textColor=colors.HexColor("#888888"))),
    Paragraph(
        f"Internal codename: {SERIES_INTERNAL}  "
        f"(preserved for SHA chain integrity)",
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
