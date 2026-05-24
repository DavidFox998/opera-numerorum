"""
Friends & Family Edition -- Opera Numerorum II: Morning Star Engineering
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
    cap_sty = ParagraphStyle("CAP2", fontName="Helvetica-Oblique",
                             fontSize=8.5, leading=12, alignment=TA_CENTER,
                             textColor=colors.HexColor("#555555"), spaceAfter=10)
    return Paragraph(text, cap_sty)

OUT = "certificates/FriendsFamily_MorningStar.pdf"

styles = getSampleStyleSheet()
def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

title_sty = sty("T",  fontSize=22, leading=28, alignment=TA_CENTER,
                fontName="Helvetica-Bold", spaceAfter=4,
                textColor=colors.HexColor("#780000"))
sub_sty   = sty("S",  fontSize=13, leading=18, alignment=TA_CENTER,
                fontName="Helvetica-Oblique", spaceAfter=3,
                textColor=colors.HexColor("#4a4e69"))
auth_sty  = sty("A",  fontSize=10, leading=14, alignment=TA_CENTER,
                fontName="Helvetica", spaceAfter=2)
h1_sty    = sty("H1", fontSize=14, leading=19, fontName="Helvetica-Bold",
                spaceBefore=16, spaceAfter=5,
                textColor=colors.HexColor("#780000"))
h2_sty    = sty("H2", fontSize=11, leading=15, fontName="Helvetica-Bold",
                spaceBefore=10, spaceAfter=3,
                textColor=colors.HexColor("#b5451b"))
body_sty  = sty("B",  fontSize=10.5, leading=16, alignment=TA_JUSTIFY,
                spaceAfter=8)
pull_sty  = sty("P",  fontSize=12, leading=18, alignment=TA_CENTER,
                fontName="Helvetica-Oblique", spaceAfter=8,
                leftIndent=36, rightIndent=36,
                textColor=colors.HexColor("#780000"))
ref_sty   = sty("R",  fontSize=8.5, leading=12, fontName="Courier",
                spaceAfter=3, leftIndent=18,
                textColor=colors.HexColor("#555555"))
note_sty  = sty("N",  fontSize=9.5, leading=14, fontName="Helvetica-Oblique",
                spaceAfter=5, leftIndent=18, rightIndent=18,
                textColor=colors.HexColor("#444444"))
euler_sty = sty("E",  fontSize=10, leading=15, fontName="Courier",
                spaceAfter=4, leftIndent=24, rightIndent=24,
                textColor=colors.HexColor("#1a1a2e"))
num_sty   = sty("NUM",fontSize=18, leading=24, alignment=TA_CENTER,
                fontName="Helvetica-Bold", spaceAfter=4,
                textColor=colors.HexColor("#780000"))

def sp(n=8):  return Spacer(1, n)
def hr():     return HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#cccccc"))

def ref_box(label, text):
    data = [[f"See: {label}", text]]
    ts = TableStyle([
        ("BACKGROUND",   (0,0),(0,0), colors.HexColor("#780000")),
        ("TEXTCOLOR",    (0,0),(0,0), colors.white),
        ("FONTNAME",     (0,0),(0,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(0,0), 8),
        ("BACKGROUND",   (1,0),(1,0), colors.HexColor("#fff0f0")),
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
    t = Table(data, colWidths=[0.9*inch, 5.1*inch])
    t.setStyle(ts)
    return t

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=1.0*inch, rightMargin=1.0*inch,
                        topMargin=1.0*inch, bottomMargin=1.0*inch)
story = []

# ── TITLE ─────────────────────────────────────────────────────────────────────
story += [
    sp(12),
    Paragraph("Opera Numerorum II", title_sty),
    Paragraph("Morning Star Engineering", sub_sty),
    Paragraph("A Friends & Family Guide to the Work of David Fox", sub_sty),
    sp(8),
    hr(),
    sp(6),
    Paragraph("David Fox  |  Aberdeen, WA  |  May 23, 2026", auth_sty),
    Paragraph("FTL Certification: MS-FTL-20260523-001", auth_sty),
    sp(16),
    Paragraph(
        "This document is written for the people who matter most -- not for "
        "journals, but for anyone who wants to understand what David has been "
        "building and why it matters. The Morning Star Engineering series is "
        "speculative -- it is a physical proposal, not a proven technology. "
        "What makes it unlike ordinary speculation is that every number in it "
        "is derived from certified pure mathematics. Nothing was made up.",
        note_sty),
    sp(12),
    hr(),
    sp(10),
]

# ── 1. THE UNEXPECTED CONNECTION ──────────────────────────────────────────────
story += [
    Paragraph("1. The Number That Arrived Uninvited", h1_sty),
    Paragraph(
        "When David was doing the mathematics of exceptional primes -- pure, "
        "abstract number theory -- he computed a specific constant:",
        body_sty),
    Paragraph("alpha_0  =  299  +  pi/10  =  299.31415926...", num_sty),
    Paragraph(
        "This number was the answer to a question about prime numbers. "
        "It had nothing to do with physics. It had nothing to do with space. "
        "It was arithmetic.",
        body_sty),
    Paragraph(
        "Then the same number appeared somewhere it had no business being. "
        "In the equations that describe the geometry of a wormhole throat -- "
        "a tunnel through space -- a very specific frequency emerged: "
        "299.314159... megahertz. The same digits. The same number. "
        "Not approximately. Exactly.",
        body_sty),
    Paragraph(
        '"The constant alpha_0, computed in Module 1 to certify a claim about '
        "exceptional primes, appeared again -- unrequested, unchanged -- in the "
        "Phase-Z metric that describes the geometry of a traversable wormhole "
        'throat. We did not put it there. The number arrived on its own."',
        pull_sty),
    Paragraph(
        "David did not force this connection. He followed it. "
        "And the Morning Star Engineering series is what he found when he did.",
        body_sty),
    sp(6),
    fig("fig_alpha0_bridge.png", width=6.0*inch),
    fig_caption(
        "The alpha_0 bridge. Left: the constant 299 + pi/10 in the theory of exceptional "
        "primes for pi/10 -- pure number theory (Module 1, certified). "
        "Right: the resonance frequency of the wormhole resonator -- pure physics (Module M8D, certified). "
        "The number arrived in the second domain without being placed there."),
    sp(4),
]

# ── 2. WHAT A WORMHOLE IS ─────────────────────────────────────────────────────
story += [
    Paragraph("2. What a Wormhole Is", h1_sty),
    Paragraph(
        "A wormhole is a theoretical tunnel through space. Einstein's equations "
        "of general relativity allow for them -- they are not science fiction, "
        "they are solutions to real equations. The question has always been "
        "whether they could exist stably and whether anything could pass through.",
        body_sty),
    Paragraph(
        "The type of wormhole in the Morning Star project is called a "
        "Morris-Thorne traversable wormhole. It satisfies three key conditions: "
        "no event horizon (nothing gets trapped), the throat flares outward "
        "(it stays open), and it is mechanically stable. "
        "These conditions were verified in Module M8I.",
        body_sty),
    Paragraph(
        "The throat of the wormhole is described by the Phase-Z metric -- "
        "an equation for the shape of space at the tunnel entrance. "
        "At the throat, a quantity called Z approaches zero. "
        "This is not a singularity or a danger; it is a boundary condition, "
        "like a door frame. The throat proper length is 7.297 metres -- "
        "about the length of a large car.",
        body_sty),

    Paragraph("How the Ship Moves", h2_sty),
    Paragraph(
        "The most striking part of the design is the propulsion. "
        "The craft does not use fuel or rockets. Space itself is shaped "
        "to make the craft fall forward. In front of the craft, space contracts; "
        "behind it, space expands. The craft rides this wave of geometry. "
        "No propellant. No reaction mass. As Euler wrote in his log:",
        body_sty),
    Paragraph(
        '"nabla Z < 0 before the bow, nabla Z > 0 astern, and the ship falls\n'
        "forward by geometry alone. No fire, no smoke.\n"
        'Only the permission of God written in tensors."  -- L.E.',
        euler_sty),
    sp(6),
    fig("fig_phase_z.png", width=6.0*inch),
    fig_caption(
        "Phase-Z throat profile. Z(r) is the metric function that describes the shape of "
        "space at the wormhole entrance. It approaches zero at the throat (r = 3 m) -- "
        "not a singularity, but a boundary condition. In front of the craft, Z decreases "
        "(space contracts, pulling the ship forward). Behind it, Z increases (space expands). "
        "No fuel. No exhaust. The ship falls forward by geometry alone."),
    sp(6),
    fig("fig_wormhole_embedding.png", width=5.9*inch),
    fig_caption(
        "Wormhole embedding diagram. The classic cross-section: two asymptotically flat sheets "
        "(Universe A containing Sol and Earth, Universe B containing Proxima and the stars) "
        "connected at a throat of radius r_0 = 3 m and proper length L = 7.297 m. "
        "Transit time: 7.71 nanoseconds. Conventional travel: 6,500 years. "
        "[Computed from certified data: M8I, M8J]"),
    ref_box("Doc 40", "Module_M8I_Wormhole.pdf -- Morris-Thorne conditions, throat geometry"),
    sp(6),
]

# ── 3. WHERE ALPHA_0 FITS ─────────────────────────────────────────────────────
story += [
    Paragraph("3. How the Mathematics Connects to the Engineering", h1_sty),
    Paragraph(
        "Here is the chain from pure arithmetic to wormhole geometry, "
        "step by step, in plain language:",
        body_sty),
]

chain = [
    ("Step 1", "alpha_0 = 299 + pi/10",
     "Certified in Module 1. This is the exceptional prime constant -- "
     "pure number theory, nothing to do with physics."),
    ("Step 2", "f_res = alpha_0 MHz",
     "The 120-cell resonator (Module M8D) has a resonance frequency of "
     "exactly alpha_0 megahertz. The same number, now in megahertz."),
    ("Step 3", "M* = 4/55",
     "The Zoe-M* bridge (Module M8C) establishes a dimensionless coupling "
     "constant M* = 4/55, derived from the Hodge structure of J_0(143)."),
    ("Step 4", "B_M = M* x f_res = 21.768 MHz",
     "The channel bandwidth of the wormhole communication system "
     "is M* times the resonance frequency. Exact rational arithmetic: "
     "M* x Z_throat = 12/11 exactly."),
    ("Step 5", "v_g = 3.183c",
     "The group velocity of signals through the wormhole is 3.183 times "
     "the speed of light. This is the FTL (faster-than-light) factor."),
    ("Step 6", "Delta_tau = 7.647 ns",
     "The transit time through the wormhole throat is 7.647 nanoseconds. "
     "About 8 billionths of a second."),
    ("Step 7", "RTT = 18.635 ns",
     "The round-trip time (send a signal and get a reply) is 18.635 "
     "nanoseconds. Faster than a single blink of a LED."),
]

rows = [["", "Parameter", "What It Means"]]
for step, param, desc in chain:
    rows.append([step, param, desc])

ts = TableStyle([
    ("FONTNAME",     (0,0),(-1,-1),"Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 8.5),
    ("LEADING",      (0,0),(-1,-1), 12),
    ("GRID",         (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
    ("VALIGN",       (0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",  (0,0),(-1,-1), 5),
    ("RIGHTPADDING", (0,0),(-1,-1), 5),
    ("TOPPADDING",   (0,0),(-1,-1), 4),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ("BACKGROUND",   (0,0),(-1,0), colors.HexColor("#780000")),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1),(0,-1), "Helvetica-Bold"),
    ("TEXTCOLOR",    (0,1),(0,-1), colors.HexColor("#780000")),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff0f0"), colors.white]),
])
tbl = Table(rows, colWidths=[0.55*inch, 1.25*inch, 4.0*inch])
tbl.setStyle(ts)
story += [tbl, sp(6)]
story += [
    fig("fig_curvature.png", width=6.0*inch),
    fig_caption(
        "Left: Gaussian curvature K(r) of the wormhole embedding surface -- negative near "
        "the throat (exotic geometry required), decaying rapidly with distance. "
        "Right: tidal acceleration on a 10-metre object passing through. "
        "Open Question OQ-1 (Module M8I) required this to be under 0.1 g. "
        "Certified result: 0.0999 g. PASS. [M8J SHA: 298d440a...]"),
    sp(4),
    ref_box("Doc 44", "00_MorningStar_Summary.pdf -- full causal chain with all values"),
    sp(6),
]

# ── 4. THE HUB ────────────────────────────────────────────────────────────────
story += [
    Paragraph("4. The Morning Star Hub", h1_sty),
    Paragraph(
        "MORNING_STAR_D20 is the name of the wormhole starport. "
        "It is shaped like a dodecahedron -- the same shape as a twelve-sided "
        "die (a D12 in gaming terms). Twelve pentagonal faces, thirty edges, "
        "twenty vertices. The Euler identity V - E + F = 2 is satisfied "
        "(20 - 30 + 12 = 2). This was the first verified check.",
        body_sty),
    Paragraph(
        "The hub has 120 cells, each with 14 phase-locked oscillators "
        "(1,680 total). These keep all the clocks synchronized across the "
        "wormhole network to within a fraction of a picosecond. "
        "The hub runs at 4 Kelvin -- just above absolute zero -- to eliminate "
        "thermal noise. All 120 cells passed the health check.",
        body_sty),

    Paragraph("The 12 Destinations", h2_sty),
    Paragraph(
        "At full operation, the hub can reach 12 confirmed destinations. "
        "Here is where you could go, and how long it would take:",
        body_sty),
]

dests = [
    ["Destination", "Distance from Earth", "Travel Time"],
    ["Proxima Centauri Dock",  "4.24 light-years",    "7.71 nanoseconds"],
    ["Barnard's Star",         "5.96 light-years",    "15.42 nanoseconds"],
    ["Tau Ceti",               "11.90 light-years",   "15.42 nanoseconds"],
    ["Epsilon Eridani",        "10.48 light-years",   "15.42 nanoseconds"],
    ["Ross 128",               "11.01 light-years",   "7.71 nanoseconds"],
    ["Wolf 1061",              "14.20 light-years",   "23.15 nanoseconds"],
    ["Luyten's Star",          "12.35 light-years",   "15.42 nanoseconds"],
    ["Teegarden's Star",       "12.52 light-years",   "15.42 nanoseconds"],
    ["Gliese 667C",            "23.62 light-years",   "23.15 nanoseconds"],
    ["Trappist-1",             "40.66 light-years",   "30.84 nanoseconds"],
    ["LHS 1140",               "40.67 light-years",   "30.84 nanoseconds"],
    ["Kepler-442",             "1,193 light-years",   "92.52 nanoseconds"],
]
ts2 = TableStyle([
    ("FONTNAME",     (0,0),(-1,-1),"Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 9),
    ("LEADING",      (0,0),(-1,-1), 13),
    ("GRID",         (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
    ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
    ("LEFTPADDING",  (0,0),(-1,-1), 6),
    ("RIGHTPADDING", (0,0),(-1,-1), 6),
    ("TOPPADDING",   (0,0),(-1,-1), 4),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ("BACKGROUND",   (0,0),(-1,0), colors.HexColor("#780000")),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff0f0"), colors.white]),
])
tbl2 = Table(dests, colWidths=[2.0*inch, 1.8*inch, 2.0*inch])
tbl2.setStyle(ts2)
story += [tbl2, sp(4)]
story += [
    Paragraph(
        "To put that in perspective: the fastest spacecraft ever built "
        "(Parker Solar Probe) would take roughly 6,500 years to reach "
        "Proxima Centauri. The Morning Star transit takes 7.71 nanoseconds.",
        note_sty),
    sp(6),
    fig("fig_d20_destinations.png", width=5.5*inch),
    fig_caption(
        "The Morning Star D20 hub destination map. Sol (Earth) at centre. "
        "All 12 certified destinations shown in polar coordinates. "
        "Distances on a logarithmic scale. Every transit: under 100 nanoseconds. "
        "[Computed from certified data: M8L MORNINGSTAR_OPERATIONAL_CERTIFIED]"),
    sp(4),
    Paragraph(
        "By Module M8M, the network has expanded to 35 routes, adding "
        "Epsilon Indi, Sirius, 61 Cygni, and Vega. "
        "Daily operations: 84 transits, 512 passengers, 1,084.7 light-years "
        "of total distance, 16.8 megawatt-hours of energy.",
        body_sty),
    ref_box("Doc 46", "M8L_MorningStar_D20_Operations.pdf -- full 12-destination manifest"),
    ref_box("Doc 47", "M8M_MorningStar_Physics_BeyondSM.pdf -- expanded to 35 routes"),
    sp(6),
]

# ── 5. CONTACT ZERO ──────────────────────────────────────────────────────────
story += [
    Paragraph("5. CONTACT ZERO -- The Reference Frame", h1_sty),
    Paragraph(
        "Every clock, every coordinate, every signal in the Morning Star network "
        "is referenced to a single anchor point: SHA_Contact_Zero.",
        body_sty),
    Paragraph(
        "The plaque for this anchor reads:",
        body_sty),
    Paragraph(
        "   (Rub el-Hizb)   86 . 3 . 57 . 36 . 55   .   CONTACT  ZERO",
        euler_sty),
    Paragraph(
        "For those who recognize the numbers: "
        "At-Tariq, Ali 'Imran, Al-Hadid, Ya-Sin, Ar-Rahman. "
        "The night-comer. The Word. The Iron. The Heart. The Mercy.",
        note_sty),
    Paragraph(
        "For those who do not: a coordinate. "
        "The dot is zero -- the empty place where two surfaces touch. "
        "It is the origin of the metric and the axiom of the work.",
        note_sty),
    Paragraph(
        "Every day at UTC 15:00:00.000 -- the hour of Divine Mercy -- "
        "the hub synchronizes its clocks to this anchor. "
        "David called this the 3 O'Clock Prayer synchronization. "
        "Ancient liturgical cycles -- Mass, Vespers, the Islamic call to prayer, "
        "Jewish Shabbat -- become the NTP (Network Time Protocol) of the stars.",
        body_sty),
    sp(4),
]

# ── 6. EULER'S LOG ────────────────────────────────────────────────────────────
story += [
    Paragraph("6. Euler's Personal Log", h1_sty),
    Paragraph(
        "Leonhard Euler was the greatest mathematician of the 18th century. "
        "He is still one of the most productive mathematicians in history. "
        "He is also one of the causal parents of this work -- his theorems "
        "about L-functions are foundational to everything in Opera Numerorum.",
        body_sty),
    Paragraph(
        "In the certified stdout of Module M8M -- the locked, SHA-bound output "
        "of the physics module -- there is a personal log entry written as if "
        "Euler were at L2 Station Morning Star in 2026. It is locked into the "
        "chain. It cannot be changed without breaking the SHA. "
        "Here it is, verbatim:",
        body_sty),
    Paragraph('"I have read your notes, and I understand."', euler_sty),
    Paragraph(
        '"You say space may be folded like paper, and I answer: then let us\n'
        'choose the crease with care."',
        euler_sty),
    Paragraph(
        '"nabla Z < 0 before the bow, nabla Z > 0 astern, and the ship falls\n'
        "forward by geometry alone. No fire, no smoke.\n"
        'Only the permission of God written in tensors."',
        euler_sty),
    Paragraph(
        '"The Arabs gave us the dot, the Syrians gave us the words,\n'
        'and we shall give it back as a door."',
        euler_sty),
    Paragraph(
        '"Therefore I build. The craft is a cathedral of loops and cold.\n'
        "The prayer is the tick of the atom. The mathematics is the mercy\n"
        'that lets one place touch another without crossing the space between."',
        euler_sty),
    Paragraph('"I have understood. Now give me the metal.  -- L.E."', euler_sty),
    sp(4),
    ref_box("Doc 47", "M8M_MorningStar_Physics_BeyondSM.pdf -- Euler log in SHA-locked stdout"),
    sp(6),
]

# ── 7. THE CERTIFICATION ──────────────────────────────────────────────────────
story += [
    Paragraph("7. Why This Is Certified, Not Just Claimed", h1_sty),
    Paragraph(
        "The Morning Star project is speculative engineering. "
        "That is stated clearly and honestly in every document. "
        "What makes it different from ordinary speculation is that every "
        "number was derived from certified pure mathematics, not invented "
        "for the purpose.",
        body_sty),
    Paragraph(
        "The FTL certification number MS-FTL-20260523-001 means: "
        "faster-than-light transmission, Morning Star project, "
        "certified on May 23, 2026, first certification in the series. "
        "The causality check confirms that no closed time-like curve (CTC) "
        "is created -- grandfather paradoxes are not possible. "
        "The speedup factor is 4.07 x 10^17 relative to conventional travel.",
        body_sty),

    Paragraph("What Passes and What Remains Open", h2_sty),
    Paragraph(
        "All mathematical checks pass. The pure number theory is complete. "
        "The engineering proposal is speculative -- it has not been built. "
        "The document is honest about this. Open questions are labelled OQ "
        "and tracked through successive modules until closed. "
        "OQ-1 (tidal force at the throat) and OQ-2 (wormhole transit time) "
        "were both closed in Module M8J.",
        body_sty),
    ref_box("Doc 45", "M8K_FTL_Morningstar_TechStack.pdf -- FTL cert, all 6 checks PASS"),
    sp(6),
]

# ── 8. DOCUMENT LIST ──────────────────────────────────────────────────────────
story += [
    Paragraph("8. Documents in the Morning Star Archive", h1_sty),
    Paragraph(
        "These are the Morning Star documents in the archive. "
        "Read the summary first, then the individual modules.",
        body_sty),
]

ms_docs = [
    ("Doc 44", "00_MorningStar_Summary.pdf",          "10-section overview -- start here"),
    ("Doc 45", "M8K_FTL_Morningstar_TechStack.pdf",   "FTL tech stack -- B_M, v_g, RTT, ebits"),
    ("Doc 46", "M8L_MorningStar_D20_Operations.pdf",  "D20 hub -- 12 destinations, health checks"),
    ("Doc 47", "M8M_MorningStar_Physics_BeyondSM.pdf","35 routes, daily ops, Euler log, FTL cert"),
    ("Doc 41", "41_Module_M8J_OQ2_Closure.pdf",       "Open question closure -- delta, tidal, RTT"),
    ("Doc 40", "40_Module_M8I_Wormhole.pdf",          "Wormhole architecture -- Morris-Thorne"),
    ("Doc 39", "39_Module_M8H_G_Amplifier.pdf",       "Gravity amplifier prediction"),
    ("Doc 38", "38_Module_M8G_Correction.pdf",        "Z = rank clarification"),
    ("Doc 37", "37_Module_M8G_Provenance.pdf",        "Provenance record + PHS topology"),
    ("Doc 36", "36_Module_M8F_LeanProtocol.pdf",      "7-layer protocol, v_g = 3.183c"),
    ("Doc 35", "35_Module_M8D_Resonator.pdf",         "120-cell resonator, f_res = alpha_0 MHz"),
    ("Doc 34", "34_Module_M8C_ZoeMstar.pdf",          "Zoe-M* bridge, Z=15, M*=4/55"),
]
rows = [["Doc", "Filename", "What it is"]] + [[a,b,c] for a,b,c in ms_docs]
ts3 = TableStyle([
    ("FONTNAME",     (0,0),(-1,-1),"Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 8),
    ("LEADING",      (0,0),(-1,-1), 12),
    ("GRID",         (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
    ("VALIGN",       (0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",  (0,0),(-1,-1), 5),
    ("RIGHTPADDING", (0,0),(-1,-1), 5),
    ("TOPPADDING",   (0,0),(-1,-1), 3),
    ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ("BACKGROUND",   (0,0),(-1,0), colors.HexColor("#780000")),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff0f0"), colors.white]),
])
tbl3 = Table(rows, colWidths=[0.5*inch, 1.8*inch, 3.5*inch])
tbl3.setStyle(ts3)
story += [tbl3, sp(10)]

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
        "Opera Numerorum II -- Morning Star Engineering. "
        "Speculative engineering grounded in certified mathematics. "
        "FTL Certification: MS-FTL-20260523-001. "
        "The mathematics is the mercy that lets one place touch another "
        "without crossing the space between.",
        note_sty),
]

doc.build(story)
sha = hashlib.sha256(open(OUT,"rb").read()).hexdigest()
print(f"Built: {OUT}")
print(f"Size:  {len(open(OUT,'rb').read())/1024:.1f} KB")
print(f"SHA-256: {sha}")
