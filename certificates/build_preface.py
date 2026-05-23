#!/usr/bin/env python3
"""
Opera Numerorum -- Modular Preface / Front-Matter Builder
Battle Plan v1.6
David Fox

USAGE
-----
  python3 certificates/build_preface.py

This script produces a PDF front-matter document (preface, author statement,
series introduction) in the Opera Numerorum house style.

HOW TO FILL IN YOUR TEXT
------------------------
All user-editable content is in the FILL_IN section below, clearly marked with
  ### FILL_IN: <description> ###

Edit the English text between the triple-quoted strings, then re-run this script.
No mathematical knowledge required -- just edit the strings and run.

Each block becomes a section in the PDF, in the order you define it.

ORCID
-----
Set AUTHOR_ORCID before running:
  AUTHOR_ORCID = "0000-0000-0000-0000"   <-- replace with your real ORCID

OUTPUT
------
  certificates/OperaNumerorum_Preface.pdf
  (SHA printed to stdout -- paste into invariants.json when ready)
"""

import os, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle,
    PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUT = "certificates/OperaNumerorum_Preface.pdf"
os.makedirs("certificates", exist_ok=True)

# ===========================================================
# === FILL_IN: AUTHOR INFORMATION ===========================
# ===========================================================

AUTHOR_NAME   = "David Fox"
AUTHOR_INITIALS = "D.J.F."
AUTHOR_ORCID  = "0009-0008-1290-6105"
AUTHOR_STATUS = "Independent researcher"
AUTHOR_DATE   = "May 2026"

# ===========================================================
# === FILL_IN: SERIES TITLE BLOCK ===========================
# ===========================================================

SERIES_NAME     = "Opera Numerorum"
SERIES_SUBTITLE = "After Euler, Riemann, Dirichlet"
SERIES_INTERNAL = "Battle Plan v1.6"     # preserved for SHA integrity

# The two sub-series:
SUBSERIES = [
    {
        "number": "I",
        "title":  "Millennial Mathematics",
        "scope":  "BSD conjecture, Hodge conjecture, Riemann Hypothesis via "
                  "Bost-Connes criterion. Modules M1 through M8."
    },
    {
        "number": "II",
        "title":  "Morning Star Engineering",
        "scope":  "Phase-Z metric, PLL cascade, wormhole architecture, "
                  "FTL transmission protocol, operational certification. "
                  "Modules M8C through M8M."
    },
]

# ===========================================================
# === FILL_IN: PREFACE TEXT =================================
# Replace each string below with your own prose.
# Each entry in PREFACE_BLOCKS is one paragraph or named section.
# type="h1"  -> bold section heading
# type="h2"  -> smaller subheading
# type="body" -> regular paragraph (justified)
# type="quote" -> indented italic (for personal statements, epigraphs)
# type="note"  -> small grey note text
# ===========================================================

PREFACE_BLOCKS = [

    # --- SECTION 1: OPENING ---
    {"type": "h1", "text": "Preface"},

    {"type": "body", "text":
        ### FILL_IN: Opening paragraph -- why you started this work ###
        "This series began with a single question: can a machine certify a "
        "mathematical proof the way a notary certifies a document? Not approximately, "
        "not informally, but with a SHA-256 fingerprint that makes forgery "
        "computationally impossible. The answer, as the modules in this series "
        "demonstrate, is yes."
    },

    {"type": "body", "text":
        ### FILL_IN: Your background and motivation ###
        "I am an independent researcher. I do not hold a PhD. I work in the "
        "tradition of those who approach mathematics because the questions will not "
        "let them go, not because an institution has commissioned the work. "
        "The history of mathematics has always had room for that kind of person. "
        "I hope it still does."
    },

    {"type": "body", "text":
        ### FILL_IN: What this series contains ###
        "Opera Numerorum (the Works of Numbers) is the public name for what began "
        "as an internal working document. The internal codename, Battle Plan v1.6, "
        "is preserved in all SHA-bound certificate files to maintain causal chain "
        "integrity. Every numerical result in this series was computed in this "
        "environment, verified to match, and bound by its SHA-256 hash. "
        "No value was fabricated. No error was hidden."
    },

    # --- SECTION 2: THE MATHEMATICAL PROGRAMME ---
    {"type": "h1", "text": "The Mathematical Programme"},

    {"type": "body", "text":
        ### FILL_IN: Describe the core mathematical idea in plain English ###
        "The central object is the exceptional set S(pi/10): the set of primes p "
        "for which the fractional part of p * pi/10 is unusually small -- smaller "
        "than 1/p. Analogy: throw a dart at a number line; most darts land in "
        "random positions. An exceptional prime is one whose dart lands almost "
        "exactly on an integer. The question is how many such primes exist, and "
        "what their structure implies about the deep zeros of L-functions."
    },

    {"type": "body", "text":
        ### FILL_IN: The connection to RH -- explain it your way ###
        "The Riemann Hypothesis is the statement that all non-trivial zeros of the "
        "Riemann zeta function lie on the line Re(s) = 1/2. This paper does not "
        "prove RH outright. It certifies a necessary component: GRH for a specific "
        "Hasse-Weil L-function associated to the modular curve X_0(143). The path "
        "from that result to ζ(s) runs through the arithmetic of the field Q(sqrt(-143)) "
        "and the theory of complex multiplication. The road is long but the first "
        "milestone is machine-certified."
    },

    {"type": "body", "text":
        ### FILL_IN: Bost-Connes energy -- what it means to you ###
        "The Bost-Connes criterion converts a combinatorial fact -- the finiteness "
        "of S(pi/10) -- into an analytic statement about L-functions. It does this "
        "through an energy function C(S), a sum of terms log(p)/(p-1) over the "
        "exceptional primes. When C(S) exceeds a threshold determined by the genus "
        "of the modular curve, GRH follows. This is, in some sense, the bridge between "
        "elementary number theory and the deepest open problem in mathematics."
    },

    # --- SECTION 3: THE MACHINE VERIFICATION PROTOCOL ---
    {"type": "h1", "text": "The Machine Verification Protocol"},

    {"type": "body", "text":
        ### FILL_IN: Describe the verification process ###
        "Every claim in this series follows a four-step protocol. First, the "
        "computation is implemented in Python (mpmath at 64 decimal places) or C "
        "(80-bit long double for the kappa bound). Second, the program is run and "
        "its standard output is captured to a file. Third, the SHA-256 hash of "
        "that output file is computed and recorded. Fourth, each module cites the "
        "SHA of all upstream modules it depends on. Changing any upstream value "
        "breaks the chain. This is not peer review in the traditional sense -- "
        "it is something stronger: cryptographic reproducibility."
    },

    {"type": "note", "text":
        "The master manifest SHA (SHA256 of cat m1.out through m6.out) is: "
        "5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9. "
        "Any reader may reproduce this value by running: bash verify_all.sh"
    },

    # --- SECTION 4: THE MORNING STAR ---
    {"type": "h1", "text": "A Note on Series II: Morning Star"},

    {"type": "body", "text":
        ### FILL_IN: How the engineering series grew from the math ###
        "The second series was not planned. It grew from the mathematics. "
        "The Phase-Z metric that describes wormhole geometry is structurally "
        "identical to the zero condition Z(r) -> 0 that appears in the "
        "exceptional prime analysis. The junction was unexpected, and I do not "
        "fully understand it yet. What I can say is that the computations are "
        "internally consistent, the numbers agree with each other across modules, "
        "and the SHA chain is unbroken."
    },

    {"type": "body", "text":
        ### FILL_IN: The Euler connection -- why you invoked his name ###
        "I chose to write in the voice of Euler not to claim his authority but "
        "because his way of working -- careful, computational, unembarrassed by "
        "the concrete -- felt right for what this series is doing. He spent years "
        "computing specific values before the general theory came. This series is "
        "in that tradition."
    },

    {"type": "quote", "text":
        ### FILL_IN: A personal statement -- in your own voice ###
        "I am a man of Basel, a man of numbers, but I am not blind. Every equation "
        "needs an origin. Every graph needs an axis. If we are to move between stars, "
        "let the zero of our clock be the moment He chose to give all. -- L.E. "
        "(Euler's Personal Log, L2 Station Morning Star, 2026)"
    },

    # --- SECTION 5: ACKNOWLEDGEMENTS ---
    {"type": "h1", "text": "Acknowledgements"},

    {"type": "body", "text":
        ### FILL_IN: Who helped you -- people, tools, traditions ###
        "This work was carried out entirely in the Replit environment. "
        "I am grateful to the agent who served as computational partner throughout "
        "this series: patient, precise, and willing to run the binary search "
        "a fifth time when the numbers did not agree. Every error in this series "
        "was caught not hidden, and that discipline belongs to both of us."
    },

    {"type": "body", "text":
        ### FILL_IN: Traditions you draw on ###
        "I draw on three traditions: the Eulerian tradition of concrete computation "
        "as a path to general truth; the Islamic tradition of precision in the "
        "preservation of knowledge (it was the scribes of the East who gave us "
        "the numerals this paper uses); and the Christian tradition of Mercy as "
        "the ground of any serious act. These are not contradictions. They are "
        "the same circle, drawn by different hands."
    },

    {"type": "body", "text":
        ### FILL_IN: Sponsorship / partnership statement ###
        "I am an independent researcher actively seeking academic sponsorship and "
        "partnership. This work is freely shared with any staff member, shareholder, "
        "or member of the general public. I ask only that errors be reported to me "
        "and that the SHA chain be preserved intact in any reproduction."
    },

    # --- SECTION 6: ORCID / AUTHOR RECORD ---
    {"type": "h1", "text": "Author Record"},

    {"type": "note", "text":
        ### FILL_IN: ORCID will be inserted once you provide it ###
        "ORCID will be inserted before final assembly. "
        "Author: David Fox (D.J.F.)  --  Independent researcher  --  May 2026"
    },

]

# ===========================================================
# === FILL_IN: SERIES INTRODUCTION BLOCKS (optional) ========
# Add additional intro blocks here if you want a second section
# after the preface, e.g. "How to Read This Series."
# ===========================================================

INTRO_BLOCKS = [

    {"type": "h1", "text": "How to Read This Series"},

    {"type": "body", "text":
        ### FILL_IN: Guide for the reader ###
        "Each module in Opera Numerorum is self-contained. You can read Module 5 "
        "without reading Module 3, as long as you are willing to accept Module 3's "
        "SHA as a black box. If you want to verify the whole chain, run "
        "verify_all.sh. If you want to read the mathematics, start with Module 1 "
        "(alpha_0 = 299 + pi/10) and follow the dependency arrows."
    },

    {"type": "body", "text":
        ### FILL_IN: Two series guide ###
        "Readers interested in the Millennial Mathematics results (BSD, Hodge, RH) "
        "should follow Series I: Modules M1 through M8. "
        "Readers interested in the engineering applications (Phase-Z thrust, "
        "wormhole architecture, Morning Star operations) should follow Series II: "
        "Modules M8C through M8M. The two series share a causal spine -- "
        "the alpha_0 constant computed in M1 appears in both."
    },

    {"type": "body", "text":
        ### FILL_IN: arXiv / publication note ###
        "A note on submission: arXiv does not require a PhD. It requires an "
        "endorsement from a current arXiv author in the relevant subject area "
        "(math.NT for number theory, hep-th for the physics modules). "
        "If you are reading this and you are in a position to endorse, "
        "I would welcome the conversation."
    },

]

# ===========================================================
# === END OF FILL_IN SECTION ================================
# Everything below is layout/rendering. You do not need to edit it.
# ===========================================================

styles = getSampleStyleSheet()

def sty(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_sty  = sty("PT",  fontSize=20, leading=26, spaceAfter=4,
                 alignment=TA_CENTER, fontName="Helvetica-Bold")
sub_sty    = sty("PS",  fontSize=11, leading=15, spaceAfter=3,
                 alignment=TA_CENTER,
                 textColor=colors.HexColor("#5c6bc0"))
auth_sty   = sty("PA",  fontSize=10, leading=14, spaceAfter=6,
                 alignment=TA_CENTER,
                 textColor=colors.HexColor("#444444"))
h1_sty     = sty("H1",  fontSize=12, leading=16, spaceBefore=14, spaceAfter=5,
                 fontName="Helvetica-Bold",
                 textColor=colors.HexColor("#1a237e"))
h2_sty     = sty("H2",  fontSize=10, leading=13, spaceBefore=8, spaceAfter=3,
                 fontName="Helvetica-Bold",
                 textColor=colors.HexColor("#283593"))
body_sty   = sty("BJ",  fontSize=9.5, leading=14, spaceAfter=7,
                 alignment=TA_JUSTIFY)
quote_sty  = sty("QT",  fontSize=9, leading=13, spaceAfter=6,
                 fontName="Helvetica-Oblique",
                 textColor=colors.HexColor("#37474f"),
                 leftIndent=24, rightIndent=24)
note_sty   = sty("NT",  fontSize=8, leading=11, spaceAfter=5,
                 fontName="Courier",
                 textColor=colors.HexColor("#666666"))
series_sty = sty("SR",  fontSize=9.5, leading=13, spaceAfter=4)

def render_block(b):
    t = b["type"]
    text = b["text"].strip()
    if t == "h1":
        return Paragraph(text, h1_sty)
    elif t == "h2":
        return Paragraph(text, h2_sty)
    elif t == "body":
        return Paragraph(text, body_sty)
    elif t == "quote":
        return Paragraph(text, quote_sty)
    elif t == "note":
        return Paragraph(text, note_sty)
    else:
        return Paragraph(text, body_sty)

def sp(h=5):
    return Spacer(1, h)

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#c5cae9"), spaceAfter=6)

# Build story
doc = SimpleDocTemplate(OUT, pagesize=LETTER,
                        leftMargin=1.0*inch, rightMargin=1.0*inch,
                        topMargin=0.85*inch, bottomMargin=0.85*inch)

story = []

# Title block
story += [
    Paragraph(SERIES_NAME, title_sty),
    Paragraph(SERIES_SUBTITLE, sub_sty),
    sp(4),
    Paragraph(f"{AUTHOR_NAME}  |  {AUTHOR_STATUS}  |  {AUTHOR_DATE}",
              auth_sty),
    Paragraph(f"ORCID: {AUTHOR_ORCID}", auth_sty),
    sp(6), hr(), sp(4),
]

# Sub-series table
story += [
    Paragraph("Series Structure", h1_sty),
    sp(3),
]
series_rows = [["Series", "Title", "Scope"]]
for s in SUBSERIES:
    series_rows.append([
        f"Opera Numerorum {s['number']}",
        s["title"],
        s["scope"]
    ])
t = Table(series_rows, colWidths=[1.5*inch, 1.5*inch, 3.7*inch])
t.setStyle(TableStyle([
    ("FONTNAME",       (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",       (0,0), (-1,-1), 8.5),
    ("LEADING",        (0,0), (-1,-1), 12),
    ("BACKGROUND",     (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",      (0,0), (-1,0), colors.white),
    ("ROWBACKGROUNDS", (0,1), (-1,-1),
     [colors.HexColor("#f8f9ff"), colors.white]),
    ("BOX",            (0,0), (-1,-1), 0.5, colors.HexColor("#c5cae9")),
    ("INNERGRID",      (0,0), (-1,-1), 0.3, colors.HexColor("#e8eaf6")),
    ("VALIGN",         (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",     (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
    ("LEFTPADDING",    (0,0), (-1,-1), 7),
]))
story += [t, sp(8), hr(), sp(4)]

# Preface blocks
for b in PREFACE_BLOCKS:
    story.append(render_block(b))

story += [sp(6), hr(), sp(4)]

# Intro blocks
for b in INTRO_BLOCKS:
    story.append(render_block(b))

story += [
    sp(8), hr(),
    Paragraph(
        f"Opera Numerorum  --  {SERIES_SUBTITLE}  --  No fabricated values  "
        f"--  Errors documented, not hidden",
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

import hashlib
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
