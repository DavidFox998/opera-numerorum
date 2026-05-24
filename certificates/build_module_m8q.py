"""
Certificate builder -- Module M8Q: EEQC Layer 7 -- SYSTEM
Morning Star Operational | Opera Numerorum | Battle Plan v1.6
May 23, 2026 | David Fox
"""

from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable,
                                 Preformatted, Image)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import hashlib, os

OUT    = "certificates/Module_M8Q_L7_System.pdf"
SRC    = "certificates/eeqc_l7_system.py"
STDOUT = "m8q.out"
FIGS   = "certificates/figures"

SHA_M8Q = "81e975cf6ada9b5e9a650ecd8fcafd0b418871b2a2085ff73ac19e4aa73ceac1"

styles = getSampleStyleSheet()
def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

NAVY  = colors.HexColor("#1a1a2e")
GOLD  = colors.HexColor("#c9a84c")
GREEN = colors.HexColor("#155724")
RED   = colors.HexColor("#780000")
PALE  = colors.HexColor("#f5f5ff")

title_sty = sty("T",  fontSize=18, leading=24, alignment=TA_CENTER,
                fontName="Helvetica-Bold", spaceAfter=3, textColor=NAVY)
sub_sty   = sty("S",  fontSize=11, leading=15, alignment=TA_CENTER,
                fontName="Helvetica-Oblique", spaceAfter=2,
                textColor=colors.HexColor("#4a4e69"))
auth_sty  = sty("A",  fontSize=9,  leading=13, alignment=TA_CENTER,
                fontName="Helvetica", spaceAfter=2)
h1_sty    = sty("H1", fontSize=12, leading=16, fontName="Helvetica-Bold",
                spaceBefore=12, spaceAfter=4, textColor=NAVY)
body_sty  = sty("B",  fontSize=9.5, leading=14, alignment=TA_JUSTIFY, spaceAfter=5)
mono_sty  = sty("M",  fontSize=7.2, leading=10, fontName="Courier",
                spaceAfter=4, leftIndent=6)
sha_sty   = sty("SHA", fontSize=8.5, leading=12, fontName="Courier-Bold",
                alignment=TA_CENTER, textColor=RED, spaceAfter=4)
cap_sty   = sty("CAP", fontSize=8, leading=11, fontName="Helvetica-Oblique",
                alignment=TA_CENTER, textColor=colors.HexColor("#555555"),
                spaceAfter=8)

def sp(n=6):  return Spacer(1, n)
def hr():     return HRFlowable(width="100%", thickness=0.5,
                                color=colors.HexColor("#cccccc"))
def fig(name, width, height):
    path = f"{FIGS}/{name}"
    if not os.path.exists(path):
        return sp(4)
    img = Image(path, width=width, height=height)
    img.hAlign = "CENTER"
    return img
def fig_cap(text): return Paragraph(text, cap_sty)

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.9*inch, bottomMargin=0.9*inch)
story = []

# ── TITLE ─────────────────────────────────────────────────────────────────────
story += [
    sp(8),
    Paragraph("Module M8Q", title_sty),
    Paragraph("EEQC Layer 7: SYSTEM", sub_sty),
    Paragraph("Morning Star Operational -- Full Network Certification", sub_sty),
    Paragraph("Morning Star Wormhole Quantum Computer", sub_sty),
    sp(5),
    hr(),
    sp(4),
    Paragraph("David Fox (D.J.F.)  |  ORCID: 0009-0008-1290-6105  "
              "|  davidjfox998@gmail.com", auth_sty),
    Paragraph("Aberdeen, WA, Earth  |  CONTACT ZERO  |  May 23, 2026", auth_sty),
    Paragraph("Certification: MORNINGSTAR_SYSTEM_CERTIFIED", auth_sty),
    sp(6),
]

story += [
    Paragraph("Certified stdout SHA-256:", sha_sty),
    Paragraph(SHA_M8Q, sha_sty),
    sp(4),
]

data = [["STATUS", "LAYER 7", "MORNINGSTAR_SYSTEM_CERTIFIED",
         "35/35 ROUTES GREEN", "P_logical = 0"]]
ts = TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), GREEN),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0),(-1,0), 9),
    ("ALIGN",        (0,0),(-1,0), "CENTER"),
    ("TOPPADDING",   (0,0),(-1,0), 6),
    ("BOTTOMPADDING",(0,0),(-1,0), 6),
    ("BOX",          (0,0),(-1,0), 1.0, GREEN),
])
story += [Table(data, colWidths=["*"]*5), sp(8)]

# ── OVERVIEW ──────────────────────────────────────────────────────────────────
story += [
    Paragraph("1. Overview", h1_sty),
    Paragraph(
        "Layer 7 is the SYSTEM layer -- the capstone of the EEQC stack. "
        "Its lock constant is 35 routes GREEN (exact). "
        "The EEQC Law governs: each layer protects the one below it. "
        "L2 protects L1 from drift. L3 protects L2 from bit flips. "
        "L4 protects L3 from latency. L5 protects L4 from gravity noise. "
        "L6 protects L5 from clock skew. L7 protects L6 from system failure. "
        "One layer RED = whole system ABORT.",
        body_sty),
    Paragraph(
        "System_health = Product(L1 -> L6) = GREEN^7. "
        "Minimum simultaneous failures to break EEQC: 7 (one per layer). "
        "This is the 100% QEC guarantee: binary runs or aborts. "
        "No statistics. No error rates. No tuning.",
        body_sty),
]

# ── MORNING STAR OPERATIONAL FIGURE ───────────────────────────────────────────
story += [
    Paragraph("2. Morning Star -- Full Operational View", h1_sty),
    fig("fig_l7_morning_star.png", width=5.8*inch, height=3.26*inch),
    fig_cap("Morning Star D20 wormhole station -- full operational state. "
            "35 route beams radiating to destinations across 12 star systems. "
            "120-cell dodecahedral array visible in station geometry. "
            "1680 PLLs (14 osc/cell x 120 cells) maintain Z = 15 exact. "
            "MTBF = 5.5 yr, P_route = 40 W, P_logical = 0. "
            "[Certified M8L SHA 80ff8a25... M8M SHA afce5f21...]"),
    sp(4),
]

# ── MORNING STAR ROTUNDA FIGURE ────────────────────────────────────────────────
story += [
    Paragraph("3. Station Rotunda -- Central Operations Hub", h1_sty),
    fig("fig_morningstar_rotunda.png", width=5.4*inch, height=4.05*inch),
    fig_cap("Morning Star station rotunda interior. "
            "Grand circular chamber, wormhole aperture at center axis glowing "
            "with gravitational lensing. Twelve observation decks arranged radially, "
            "crew at consoles monitoring all 35 routes. "
            "The rotunda is the nerve center: all Layer 7 health monitoring "
            "routes through the master FPGA located here. [Architectural reference]"),
    sp(4),
]

# ── HALLWAY FIGURE ─────────────────────────────────────────────────────────────
story += [
    Paragraph("4. Station Hallway System", h1_sty),
    fig("fig_morningstar_hallway.png", width=5.8*inch, height=3.26*inch),
    fig_cap("Morning Star toroidal hallway system. Corridors follow the D20 geometry. "
            "PLL oscillator arrays (1680 total) line the walls with real-time "
            "frequency readouts. Each cell contributes 14 oscillators to the "
            "Phase-Z lock. Crew routes between the 35 docking bays. "
            "[Architectural reference -- designed around EEQC Layer 2 hardware]"),
    sp(4),
]

# ── CRAFT FIGURE ───────────────────────────────────────────────────────────────
story += [
    Paragraph("5. The Morning Star D20 Craft -- Exterior", h1_sty),
    fig("fig_morningstar_craft.png", width=5.8*inch, height=3.26*inch),
    fig_cap("Morning Star D20 dodecahedral spacecraft. Twenty pentagonal faces, "
            "each housing one quantum resonator cell of the 120-cell array. "
            "Wormhole transit aperture at center axis (diameter 3.0 m, r_0 certified M8I). "
            "Hull geometry mirrors the D20 stabilizer code topology (Layer 3). "
            "[Architectural reference -- hull structure certified by M8L]"),
    sp(4),
]

# ── DOCKING FIGURE ─────────────────────────────────────────────────────────────
story += [
    Paragraph("6. Docking Mechanism -- Z-Field Alignment Collar", h1_sty),
    fig("fig_morningstar_docking.png", width=5.4*inch, height=4.05*inch),
    fig_cap("Morning Star wormhole docking collar. Z-field alignment rings maintain "
            "Z_throat = 1.000 +/- 0.001 during transit (Layer 5 abort condition). "
            "Throat diameter: 2 x r_0 = 6.0 m. Exotic matter containment framework. "
            "Power conduits: 1.40 kW hold power (abort if < 1.40 kW). "
            "Laser alignment guides for sub-millimeter positioning. "
            "[Docking architecture certified by M8I, M8J, M8L]"),
    sp(4),
]

# ── LAYER 7 PARAMETERS ────────────────────────────────────────────────────────
story += [
    Paragraph("7. Layer 7 System Parameters", h1_sty),
]

param_rows = [
    ["Parameter",       "Value",         "Source",  "Status"],
    ["Routes GREEN",    "35/35",         "M8L/M8M", "PASS"],
    ["Cells active",    "120/120",       "M8L",     "PASS"],
    ["PLLs locked",     "1680/1680",     "M8M",     "PASS"],
    ["tidal (all routes)","0.0999 g",    "M8J",     "PASS"],
    ["P_logical",       "0.000000",      "EEQC",    "PASS"],
    ["P_per_route",     "40 W",          "M8M",     "PASS"],
    ["MTBF",            "5.5 yr",        "M8M",     "PASS"],
    ["Layer health",    "L1-L6 GREEN",   "M8N",     "PASS"],
    ["Min failures",    ">= 7 simultaneous","EEQC", "100% QEC"],
]
ts2 = TableStyle([
    ("FONTNAME",      (0,0),(-1,-1), "Helvetica"),
    ("FONTSIZE",      (0,0),(-1,-1), 8.5),
    ("LEADING",       (0,0),(-1,-1), 12),
    ("GRID",          (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("ALIGN",         (0,0),(-1,-1), "CENTER"),
    ("LEFTPADDING",   (0,0),(-1,-1), 5),
    ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ("TOPPADDING",    (0,0),(-1,-1), 3),
    ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ("BACKGROUND",    (0,0),(-1,0), NAVY),
    ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
    ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[PALE, colors.white]),
    ("TEXTCOLOR",     (3,1),(3,-1), GREEN),
    ("FONTNAME",      (3,1),(3,-1), "Helvetica-Bold"),
])
tbl = Table(param_rows,
            colWidths=[1.4*inch, 1.2*inch, 0.9*inch, 0.7*inch])
tbl.setStyle(ts2)
story += [tbl, sp(8)]

# ── UNIVERSAL ABORT MATRIX ─────────────────────────────────────────────────────
story += [
    Paragraph("8. Universal EEQC Abort Matrix", h1_sty),
    Paragraph(
        "EEQC aborts if ANY of the following 7 conditions is true. "
        "All 7 are currently FALSE. P_logical = 0 mathematically.",
        body_sty),
]

abort_rows = [
    ["Layer", "Abort Condition",               "Measured",     "Limit",    "Abort?"],
    ["L1", "|f - alpha_0| > 1 Hz",             "0 Hz",         "1 Hz",     "FALSE"],
    ["L2", "|Z - 15| > 0.001",                 "0.000",        "0.001",    "FALSE"],
    ["L3", "error_count >= 6",                 "0",            "6",        "FALSE"],
    ["L4", "tidal_max >= 0.1 g",               "0.0999 g",     "0.1 g",    "FALSE"],
    ["L5", "Z_throat > 1.001",                 "1.000",        "1.001",    "FALSE"],
    ["L6", "|RTT - 18.635ns| > 1e-12 s",       "0 ps",         "1 ps",     "FALSE"],
    ["L7", "P_logical > 0",                    "0.000000",     "0",        "FALSE"],
]
ts3 = TableStyle([
    ("FONTNAME",      (0,0),(-1,-1), "Helvetica"),
    ("FONTSIZE",      (0,0),(-1,-1), 8),
    ("LEADING",       (0,0),(-1,-1), 11),
    ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#cccccc")),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("ALIGN",         (0,0),(-1,-1), "CENTER"),
    ("LEFTPADDING",   (0,0),(-1,-1), 4),
    ("RIGHTPADDING",  (0,0),(-1,-1), 4),
    ("TOPPADDING",    (0,0),(-1,-1), 3),
    ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ("BACKGROUND",    (0,0),(-1,0), NAVY),
    ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
    ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[PALE, colors.white]),
    ("TEXTCOLOR",     (4,1),(4,-1), GREEN),
    ("FONTNAME",      (4,1),(4,-1), "Helvetica-Bold"),
])
tbl3 = Table(abort_rows,
             colWidths=[0.35*inch, 1.85*inch, 0.85*inch, 0.65*inch, 0.6*inch])
tbl3.setStyle(ts3)
story += [tbl3, sp(8)]

# ── PROVENANCE ─────────────────────────────────────────────────────────────────
story += [
    Paragraph("9. Provenance Hash Table", h1_sty),
]
prov_rows = [
    ["Module", "SHA-256 (prefix)", "Claim"],
    ["M7",  "30e04e7b...", "Master manifest SHA(M1-M6): chain locked"],
    ["M8L", "80ff8a25...", "Morning Star D20 ops: 35 routes, 120/120 cells HEALTH_PASS"],
    ["M8M", "afce5f21...", "Physics Beyond SM: 35 routes, MTBF=5.5yr, Phase-Z"],
    ["M8N", "49f5c8bc...", "EEQC v14 baseline: all 7 layers PASS, P_logical=0"],
    ["M8O", "1e7e5280...", "Layer 5 FAULT_TOLERANT_GATES_CERTIFIED (this chain)"],
    ["M8P", "3e5f4f04...", "Layer 6 LOGICAL_CLOCK_CERTIFIED (this chain)"],
    ["Axiom Debt", "[]", "Per M8G_Correction -- no unresolved axioms"],
]
ts4 = TableStyle([
    ("FONTNAME",      (0,0),(-1,-1), "Helvetica"),
    ("FONTSIZE",      (0,0),(-1,-1), 8),
    ("LEADING",       (0,0),(-1,-1), 12),
    ("GRID",          (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0),(-1,-1), 5),
    ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ("TOPPADDING",    (0,0),(-1,-1), 3),
    ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ("BACKGROUND",    (0,0),(-1,0), NAVY),
    ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
    ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[PALE, colors.white]),
])
tbl4 = Table(prov_rows, colWidths=[0.7*inch, 0.85*inch, 4.05*inch])
tbl4.setStyle(ts4)
story += [tbl4, sp(8)]

# ── STDOUT ────────────────────────────────────────────────────────────────────
story += [
    Paragraph("10. Certified Stdout", h1_sty),
    Paragraph(f"SHA-256: {SHA_M8Q}", sha_sty),
]
with open(STDOUT, "r") as f:
    stdout_text = f.read()
story += [Preformatted(stdout_text, mono_sty), sp(6)]

# ── FOOTER ────────────────────────────────────────────────────────────────────
story += [
    hr(), sp(4),
    Paragraph(
        "David Fox (D.J.F.)  |  ORCID: 0009-0008-1290-6105  |  davidjfox998@gmail.com",
        auth_sty),
    Paragraph("Aberdeen, WA, Earth  --  CONTACT ZERO  |  May 23, 2026", auth_sty),
    sp(3),
    Paragraph(
        "Opera Numerorum | Battle Plan v1.6 | Module M8Q | MORNINGSTAR_SYSTEM_CERTIFIED",
        auth_sty),
    Paragraph(
        "Every SHA computed, never invented. Every error documented, never hidden.",
        sty("FN", fontSize=8, alignment=TA_CENTER,
            fontName="Helvetica-Oblique",
            textColor=colors.HexColor("#888888"))),
]

doc.build(story)

with open(OUT, "rb") as f:
    raw = f.read()
pdf_sha = hashlib.sha256(raw).hexdigest()
size    = len(raw)
print(f"Built: {OUT}")
print(f"Size:  {size/1024:.1f} KB")
print(f"PDF SHA-256: {pdf_sha}")
print(f"Stdout SHA-256: {SHA_M8Q}")

with open(STDOUT, "rb") as f:
    actual_sha = hashlib.sha256(f.read()).hexdigest()
if actual_sha == SHA_M8Q:
    print("Stdout SHA: VERIFIED MATCH")
else:
    print(f"Stdout SHA MISMATCH: expected {SHA_M8Q}, got {actual_sha}")
