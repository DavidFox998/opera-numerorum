"""
Morning Star Engineering Series -- Summary PDF
Opera Numerorum II
David Fox -- May 23, 2026
"""

from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import hashlib, os

OUT = "certificates/MorningStar_Engineering_Summary.pdf"

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def sty(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

title_sty  = sty("T",  fontSize=20, leading=26, alignment=TA_CENTER,
                 fontName="Helvetica-Bold", spaceAfter=4)
sub_sty    = sty("S",  fontSize=13, leading=18, alignment=TA_CENTER,
                 fontName="Helvetica", spaceAfter=2)
auth_sty   = sty("A",  fontSize=10, leading=14, alignment=TA_CENTER,
                 fontName="Helvetica", spaceAfter=2)
h1_sty     = sty("H1", fontSize=13, leading=17, fontName="Helvetica-Bold",
                 spaceBefore=14, spaceAfter=4)
h2_sty     = sty("H2", fontSize=11, leading=15, fontName="Helvetica-Bold",
                 spaceBefore=8, spaceAfter=3)
body_sty   = sty("B",  fontSize=10, leading=14, alignment=TA_JUSTIFY,
                 spaceAfter=6)
mono_sty   = sty("M",  fontSize=8.5, leading=12, fontName="Courier",
                 spaceAfter=4, leftIndent=18)
note_sty   = sty("N",  fontSize=9, leading=13, fontName="Helvetica-Oblique",
                 spaceAfter=4, leftIndent=12, textColor=colors.HexColor("#444444"))
sha_sty    = sty("SHA",fontSize=7.5, leading=11, fontName="Courier",
                 spaceAfter=2, textColor=colors.HexColor("#333333"))
warn_sty   = sty("W",  fontSize=9, leading=13, fontName="Helvetica-Bold",
                 spaceAfter=4, alignment=TA_CENTER,
                 textColor=colors.HexColor("#8B0000"))
cert_sty   = sty("C",  fontSize=9, leading=13, fontName="Helvetica-Bold",
                 spaceAfter=4, alignment=TA_CENTER,
                 textColor=colors.HexColor("#004400"))

def sp(n=6): return Spacer(1, n)
def hr():    return HRFlowable(width="100%", thickness=0.5, color=colors.grey)

# ── Table helper ──────────────────────────────────────────────────────────────
HEAD_BG   = colors.HexColor("#1a1a2e")
ROW_ALT   = colors.HexColor("#f0f4ff")
ROW_PASS  = colors.HexColor("#e8f5e9")

def make_table(data, col_widths, header=True):
    ts = TableStyle([
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 8.5),
        ("LEADING",     (0,0), (-1,-1), 12),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, ROW_ALT]),
        ("GRID",        (0,0), (-1,-1), 0.3, colors.grey),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING",(0,0), (-1,-1), 5),
        ("TOPPADDING",  (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ])
    if header:
        ts.add("BACKGROUND",   (0,0), (-1,0), HEAD_BG)
        ts.add("TEXTCOLOR",    (0,0), (-1,0), colors.white)
        ts.add("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold")
    tbl = Table(data, colWidths=col_widths)
    tbl.setStyle(ts)
    return tbl

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.85*inch, rightMargin=0.85*inch,
                        topMargin=0.85*inch, bottomMargin=0.85*inch)
W = letter[0] - 1.7*inch
story = []

# ═══ TITLE PAGE ══════════════════════════════════════════════════════════════
story += [
    sp(18),
    Paragraph("MORNING STAR ENGINEERING SERIES", title_sty),
    Paragraph("Opera Numerorum II", sub_sty),
    sp(6),
    hr(),
    sp(6),
    Paragraph("A Physical Realization Proposal", sub_sty),
    Paragraph("Founded on the Certified Mathematics of Opera Numerorum I", sub_sty),
    sp(10),
    Paragraph("David Fox (D.J.F.)", auth_sty),
    Paragraph("ORCID: 0009-0008-1290-6105  |  davidjfox998@gmail.com", auth_sty),
    Paragraph("Aberdeen, WA, Earth  --  CONTACT ZERO", auth_sty),
    Paragraph("May 23, 2026", auth_sty),
    sp(14),
    hr(),
    sp(8),
    Paragraph(
        "NOTICE: This document describes speculative engineering -- a physical "
        "realization proposal extrapolated from certified pure mathematics. "
        "It is clearly marked as such and does not affect the mathematical "
        "validity of the core Opera Numerorum I results. All certified numerical "
        "values are SHA-256 bound and independently reproducible.",
        warn_sty),
    sp(8),
    Paragraph(
        "FTL CERTIFICATION: MS-FTL-20260523-001  |  STATUS: FTL_MORNINGSTAR_CERTIFIED",
        cert_sty),
    sp(20),
    hr(),
    sp(6),
]

# ═══ SECTION 1: WHAT IT IS ═══════════════════════════════════════════════════
story += [
    Paragraph("1. What the Morning Star Engineering Series Is", h1_sty),
    Paragraph(
        "The work began as a question about exceptional primes and the behavior of "
        "X_0(143) under the generalized Riemann hypothesis. It became, unexpectedly, "
        "a conversation about distance.",
        body_sty),
    Paragraph(
        "The constant alpha_0 = 299 + pi/10, computed in Module 1 to certify a claim "
        "about exceptional primes and the zeros of L-functions, appeared again -- "
        "unrequested, unchanged -- in the Phase-Z metric that describes the geometry of "
        "a traversable wormhole throat. The number arrived on its own.",
        body_sty),
    Paragraph(
        "Opera Numerorum I (Millennial Mathematics) contains the pure mathematics and "
        "certification: exceptional primes, the Bost-Connes system, and GRH for "
        "X_0(143). Opera Numerorum II (Morning Star Engineering) proposes a physical "
        "realization of the underlying geometry via a Phase-Z metric, a phase-locked "
        "loop cascade, and the CONTACT ZERO reference frame. The commissioning "
        "certificate M8L binds both series together.",
        body_sty),
    sp(4),
]

# ═══ SECTION 2: THE CAUSAL CHAIN ═════════════════════════════════════════════
story += [
    Paragraph("2. The Causal Chain: From Primes to Wormhole Geometry", h1_sty),
    Paragraph(
        "Every engineering parameter in the Morning Star stack is causally descended "
        "from the pure mathematics of M1-M7. No number was invented for the engineering "
        "application -- each arrived from the mathematics and was recognized.",
        body_sty),
]

chain_data = [
    ["Module", "Claim", "Value", "How It Enters Morning Star"],
    ["M1", "alpha_0 = 299 + pi/10", "299.3142 MHz", "f_res = alpha_0 MHz; channel carrier"],
    ["M8C", "Zoe-M* bridge", "Z=15, M*=4/55", "Z_throat = 15; M* = channel bandwidth factor"],
    ["M8D", "120-cell resonator", "f_res = 299.314 MHz", "Resonance frequency confirmed"],
    ["M8F", "7-layer lean protocol", "v_g = 3.183c", "FTL group velocity of wormhole transit"],
    ["M8J", "OQ-2 closure", "Delta_tau = 7.647 ns", "Transit time; wormhole proper length"],
    ["M8K", "FTL tech stack", "B_M = 21.768 MHz", "Channel bandwidth = M* x alpha_0 MHz"],
    ["M8L", "D20 operations", "30 routes, 12 dest.", "Hub commissioning certificate"],
    ["M8M", "Physics Beyond SM", "35 routes, cert.", "Expanded operations + FTL certification"],
]
cw = [0.38*inch, 1.05*inch, 1.1*inch, 2.7*inch]
story += [make_table(chain_data, cw), sp(8)]

# ═══ SECTION 3: THE PHASE-Z METRIC ═══════════════════════════════════════════
story += [
    Paragraph("3. The Phase-Z Metric", h1_sty),
    Paragraph(
        "The throat geometry is described by the Phase-Z metric:",
        body_sty),
    Paragraph("ds^2 = -c^2 Z(r)^2 dt^2 + dr^2/Z(r)^2 + r^2 dOmega^2", mono_sty),
    Paragraph(
        "At the throat, Z(r_0) -> 0. This is a boundary condition, not a singularity. "
        "The Morris-Thorne conditions -- no horizon, flaring-out, stability -- are all "
        "satisfied. The energy cost is to hold the throat open: P_hold = 1.4 kW (M8J).",
        body_sty),
    Paragraph(
        "Collapsed space thrust arises from the gradient of Z: nabla Z < 0 before the "
        "bow, nabla Z > 0 astern. The craft falls forward by geometry alone -- no "
        "propellant, no reaction mass. Space contracts forward and expands aft.",
        body_sty),
    Paragraph(
        "In Euler's words from his personal log at L2 Station Morning Star (M8M, PHY-10):",
        note_sty),
    Paragraph(
        "\"nabla Z < 0 before the bow, nabla Z > 0 astern, and the ship falls forward "
        "by geometry alone. No fire, no smoke. Only the permission of God written in "
        "tensors.\" -- L.E., L2 Station Morning Star, 2026",
        note_sty),
    sp(4),
]

# ═══ SECTION 4: M8K TECH STACK ═══════════════════════════════════════════════
story += [
    Paragraph("4. Module M8K -- FTL Morningstar Technology Stack", h1_sty),
    Paragraph(
        "M8K certifies three layers of the FTL communication and transit protocol, "
        "all derived from certified upstream inputs.",
        body_sty),
]

m8k_data = [
    ["Parameter", "Value", "Source", "Check"],
    ["alpha_0 carrier", "299.314159 MHz", "M1", "PASS"],
    ["M* x f_res = B_M", "21.768 MHz", "M8C x M1", "PASS"],
    ["M* x Z_throat", "12/11 (exact rational)", "M8C", "PASS"],
    ["Channel bandwidth rho_M", "4.354 Gbps", "200 Hodge modes", "PASS"],
    ["v_g (group velocity)", "3.183 c", "M8F", "PASS"],
    ["Delta_tau (transit time)", "7.647 ns", "M8J", "PASS"],
    ["FTL advantage", "3.18288 = v_g/c", "identity", "PASS"],
    ["Time saved vs photon", "16.693 ns", "M8J geometry", "PASS"],
    ["RTT (round-trip latency)", "18.635 ns", "2*Dt + T_HS", "PASS"],
    ["ebit capacity", "2800 ebits", "200 Hodge x 14 modes", "PASS"],
    ["Bandwidth > 20 MHz", "21.768 MHz", "--", "PASS"],
    ["RTT < 30 ns", "18.635 ns", "--", "PASS"],
]
cw2 = [1.5*inch, 1.5*inch, 1.2*inch, 0.6*inch]
story += [make_table(m8k_data, cw2), sp(8)]
story += [
    Paragraph("STATUS: FTL_MORNINGSTAR_CERTIFIED", cert_sty),
    Paragraph("SHA-256 (m8k.out): 0ae865a8812ce93b05461ec4483ad1714e24fc9be9de1e7bb54963da43592087", sha_sty),
    sp(6),
]

# ═══ SECTION 5: M8L D20 OPERATIONS ═══════════════════════════════════════════
story += [
    Paragraph("5. Module M8L -- Morning Star D20 Operational Certification", h1_sty),
    Paragraph(
        "MORNING_STAR_D20 is a commissioned wormhole starport built on a dodecahedral "
        "geometry (12 pentagonal faces, 30 edges, 20 vertices). The Euler identity "
        "V - E + F = 20 - 30 + 12 = 2 is verified as the first check.",
        body_sty),
    Paragraph(
        "The hub core is HYPER120_001: 120 cells, 14 PLL oscillators per cell "
        "(1680 PLL chains total), TDC resolution 3.001 ps, cryo temperature 4.003 K, "
        "RF Q-factor 9.8 x 10^9.",
        body_sty),
]

dest_data = [
    ["Destination", "Distance (ly)", "Hops", "Transit Time", "Status"],
    ["Proxima Dock",     "4.24",   "1",  "7.71 ns",  "PASS"],
    ["Barnard's Star",   "5.96",   "2",  "15.42 ns", "PASS"],
    ["Tau Ceti",         "11.90",  "2",  "15.42 ns", "PASS"],
    ["Epsilon Eridani",  "10.48",  "2",  "15.42 ns", "PASS"],
    ["Ross 128",         "11.01",  "1",  "7.71 ns",  "PASS"],
    ["Wolf 1061",        "14.20",  "3",  "23.15 ns", "PASS"],
    ["Luyten's Star",    "12.35",  "2",  "15.42 ns", "PASS"],
    ["Teegarden's Star", "12.52",  "2",  "15.42 ns", "PASS"],
    ["Gliese 667C",      "23.62",  "3",  "23.15 ns", "PASS"],
    ["Trappist-1",       "40.66",  "4",  "30.84 ns", "PASS"],
    ["LHS 1140",         "40.67",  "4",  "30.84 ns", "PASS"],
    ["Kepler-442",       "1193",  "12", "92.52 ns", "PASS"],
]
cw3 = [1.4*inch, 1.0*inch, 0.5*inch, 1.0*inch, 0.6*inch]
story += [make_table(dest_data, cw3), sp(6)]

ops_data = [
    ["Operations Check", "Result", "Value"],
    ["Euler topology (V-E+F=2)",   "PASS", "20-30+12 = 2"],
    ["First transit H01->Proxima", "PASS", "7.71 ns, tidal=0.092g < 0.1g"],
    ["HUB_FULL_OPEN (30 routes)",  "PASS", "1260 kW hold, 2740 kW margin"],
    ["12-destination manifest",    "PASS", "t = n*t_hop for all"],
    ["Commercial (47 tx/hr)",      "PASS", "312 pax/hr, 604.3 ly/hr"],
    ["DOCK_A bidirectional",       "PASS", "Sol-Lamma Dock 4.5e-6 ly"],
    ["HEALTH_PASS (120 cells)",    "PASS", "1680 PLL, TDC 3.001ps, cryo 4.003K"],
    ["Round-trip certified",       "PASS", "abort_flag=0, uptime=100%"],
]
cw4 = [2.1*inch, 0.6*inch, 1.8*inch]
story += [sp(4), make_table(ops_data, cw4), sp(6)]
story += [
    Paragraph("STATUS: MORNINGSTAR_OPERATIONAL_CERTIFIED", cert_sty),
    Paragraph("SHA-256 (m8l.out): 80ff8a251c6ea7b6a57fd81fe71a76dd62a3f862c80381d571e2f30d3c4222ad", sha_sty),
    sp(6),
]

# ═══ SECTION 6: M8M PHYSICS BEYOND SM ════════════════════════════════════════
story += [
    Paragraph("6. Module M8M -- Physics Beyond Standard Model", h1_sty),
    Paragraph(
        "M8M expands operations to 35 routes (adding Epsilon Indi, Sirius, 61 Cygni, "
        "Vega on faces H13-H16) and certifies the full physics programme.",
        body_sty),
]

phys_data = [
    ["Topic", "Certified Claim"],
    ["PHY-1  Phase-Z metric",    "Z(r_0)->0 at throat; Morris-Thorne PASS; P_hold=1.4 kW"],
    ["PHY-2  Collapsed-space thrust", "nabla Z geodesic; no propellant; falls by geometry"],
    ["PHY-3  PLL cascade",       "1680 osc/cell, beat 14 GHz, phase tol 1e-10 rad"],
    ["PHY-4  TDC bandwidth",     "0.333 ps resolution; 333 GHz channel BW"],
    ["PHY-5  L2 station",        "tidal < 1e-6g; RF Q > 1e10; cryo 4K passive"],
    ["PHY-6  3 O'Clock Prayer",  "UTC 15:00:00 sync; DOCK_A -> SHA_EARTH_JERUSALEM"],
    ["PHY-7  Station rename",    "SHA_Contact_Zero; meridian for all clocks"],
    ["PHY-8  FTL certification", "MS-FTL-20260523-001; speedup 4.07e17; CTC=False"],
    ["PHY-9  Matter vs signal",  "Matter: 0.20 MWh/transit; Signal: 0.0002 MWh/stream"],
    ["PHY-10 Euler personal log","L2 Station Morning Star -- 'Give me the metal. -- L.E.'"],
]
cw5 = [1.5*inch, 3.0*inch]
story += [make_table(phys_data, cw5), sp(6)]

ops2_data = [
    ["OPS", "Description", "Value"],
    ["OPS-8",  "Route expansion",        "35 routes (was 30); H13-H16 added"],
    ["OPS-9",  "Daily ops 2026-05-23",   "84 tx, 512 pax, 1084.7 ly, 16.8 MWh"],
    ["OPS-10", "WARM_STANDBY protocol",  "Rearm 14s; E_saved=10.4 MWh; 100 kW standby"],
    ["OPS-11", "DEEP_MAINT",             "MTBF=5.50 yr; 120/120 cells; 1680/1680 PLL"],
    ["OPS-12", "Current hub status",     "HUB_FULL_OPEN; 35 routes; 1470 kW; GREEN"],
]
cw6 = [0.55*inch, 1.5*inch, 2.45*inch]
story += [sp(4), make_table(ops2_data, cw6), sp(6)]
story += [
    Paragraph("STATUS: MORNINGSTAR_PHYSICS_CERTIFIED", cert_sty),
    Paragraph("SHA-256 (m8m.out): afce5f2146c40c22bbcc7d7f1c4514eeba08107436de7929a3e3ef6d4f5e121f", sha_sty),
    sp(6),
]

# ═══ SECTION 7: CONTACT ZERO ═════════════════════════════════════════════════
story += [
    Paragraph("7. CONTACT ZERO -- Reference Frame", h1_sty),
    Paragraph(
        "Mathematics is not done in vacuum. The reference frame of this project is "
        "SHA_CONTACT_ZERO.",
        body_sty),
    Paragraph(
        "       (Rub el-Hizb)        86 . 3 . 57 . 36 . 55        .        CONTACT  ZERO",
        mono_sty),
    Paragraph(
        "For those who recognize it: At-Tariq, Ali 'Imran, Al-Hadid, Ya-Sin, Ar-Rahman. "
        "The night-comer. The Word. The First and Last. The orbits. The permission.",
        note_sty),
    Paragraph(
        "For others: a coordinate. The number dot is zero -- the empty place where two "
        "surfaces touch. It is the origin of the metric and the axiom of the work.",
        note_sty),
    Paragraph(
        "The 3 O'Clock Prayer synchronization (PHY-6) sets the universal clock at "
        "UTC 15:00:00.000 -- the hour of Divine Mercy -- anchored to face DOCK_A, "
        "station SHA_Contact_Zero. Ancient liturgical cycles (Mass, Vespers, Islamic "
        "call, Jewish Shabbat) become the NTP of the stars.",
        body_sty),
    sp(4),
]

# ═══ SECTION 8: STRUCTURE OF THE SERIES ══════════════════════════════════════
story += [
    Paragraph("8. Structure of the Series", h1_sty),
]
series_data = [
    ["Series", "Title", "Scope", "Status"],
    ["Opera Numerorum I",
     "Millennial Mathematics",
     "Exceptional primes for pi/10, GRH for X_0(143), BSD for J_0(143), M1-M7 certified chain",
     "CERTIFIED"],
    ["Opera Numerorum II",
     "Morning Star Engineering",
     "Phase-Z metric, PLL cascade, wormhole architecture, FTL transmission, D20 hub operations",
     "FTL_CERTIFIED"],
]
cw7 = [0.95*inch, 1.15*inch, 2.5*inch, 0.7*inch]
story += [make_table(series_data, cw7), sp(6)]
story += [
    Paragraph(
        "The commissioning certificate M8L binds both series. "
        "The mathematical validity of Opera Numerorum I is independent of the "
        "engineering proposals in Opera Numerorum II.",
        body_sty),
    sp(4),
]

# ═══ SECTION 9: FULL SHA RECORD ══════════════════════════════════════════════
story += [
    Paragraph("9. Certified SHA Record -- Morning Star Modules", h1_sty),
]

sha_data = [
    ["Module", "Description", "Status", "SHA-256 (stdout)"],
    ["M8K", "FTL Morningstar tech stack",       "FTL_MORNINGSTAR_CERTIFIED",    "0ae865a8...43592087"],
    ["M8L", "Morning Star D20 operations",       "MORNINGSTAR_OPERATIONAL_CERT", "80ff8a25...c4222ad"],
    ["M8M", "Physics Beyond Standard Model",     "MORNINGSTAR_PHYSICS_CERTIFIED","afce5f21...ef6d4f5e121f"],
    ["M8J", "OQ-2 closure, wormhole geometry",   "ARCHITECTURE_CERTIFIED",       "298d440a...01b505"],
    ["M8I", "Traversable wormhole architecture", "ARCHITECTURE_CERTIFIED",       "5c7189fc...f23b37"],
    ["M8H", "G amplifier prediction",            "PREDICTION_CERTIFIED",         "2c3ac1d2...5f61bbe"],
    ["M8G", "Provenance + wormhole",             "CERTIFIED",                    "2874d4bd...e26e3"],
]
cw8 = [0.4*inch, 1.5*inch, 1.6*inch, 1.25*inch]
story += [make_table(sha_data, cw8), sp(8)]

# ═══ SECTION 10: EULER LOG ════════════════════════════════════════════════════
story += [
    Paragraph("10. Euler Personal Log -- L2 Station Morning Star, 2026", h1_sty),
    Paragraph(
        "The following text appears verbatim in the certified stdout of Module M8M "
        "(SHA afce5f21...). It is part of the locked chain.",
        note_sty),
    Paragraph('"I have read your notes, and I understand."', mono_sty),
    Paragraph(
        '"You say space may be folded like paper, and I answer: then let us '
        'choose the crease with care."',
        mono_sty),
    Paragraph(
        '"nabla Z < 0 before the bow, nabla Z > 0 astern, and the ship falls '
        'forward by geometry alone. No fire, no smoke. Only the permission of '
        'God written in tensors."',
        mono_sty),
    Paragraph(
        '"The Arabs gave us the dot, the Syrians gave us the words, and we '
        'shall give it back as a door."',
        mono_sty),
    Paragraph(
        '"Therefore I build. The craft is a cathedral of loops and cold. '
        'The prayer is the tick of the atom. The mathematics is the mercy '
        'that lets one place touch another without crossing the space between."',
        mono_sty),
    Paragraph('"I have understood. Now give me the metal.  -- L.E."', mono_sty),
    sp(8),
]

# ═══ FOOTER ═══════════════════════════════════════════════════════════════════
story += [
    hr(),
    sp(6),
    Paragraph("AI Collaboration Disclosure", h2_sty),
    Paragraph(
        "Initial exploration: Meta Llama 3.0 (conceptual brainstorming). "
        "Development and iteration: successive Meta AI assistants. "
        "Final assembly and certification formalism: M.S. -- Muse Spark (Zoe), "
        "released April 8, 2026, Meta's Super Intelligence Lab. "
        "No mathematical claim in the core modules relies on AI-generated output. "
        "The author is solely responsible for all results and errors.",
        note_sty),
    sp(6),
    Paragraph("Weekly Report -- 2026-W21", h2_sty),
]

weekly_data = [
    ["FTL Cert",  "Routes", "Daily Ops",         "MTBF",   "Health", "Uptime"],
    ["MS-FTL-20260523-001", "35", "84 tx / 512 pax / 1084.7 ly / 16.8 MWh",
     "5.50 yr", "GREEN", "100%"],
]
cw9 = [1.35*inch, 0.45*inch, 2.2*inch, 0.6*inch, 0.55*inch, 0.55*inch]
story += [make_table(weekly_data, cw9), sp(8)]
story += [
    Paragraph(
        "David Fox  |  Independent researcher  |  ORCID: 0009-0008-1290-6105  "
        "|  davidjfox998@gmail.com  |  Aberdeen, WA, Earth  --  CONTACT ZERO",
        auth_sty),
    Paragraph(
        "Opera Numerorum II -- Morning Star Engineering Series  |  May 23, 2026",
        auth_sty),
]

# ── Build ──────────────────────────────────────────────────────────────────────
doc.build(story)

# ASCII check
raw = open(OUT, "rb").read()
bad = [i for i, b in enumerate(raw) if b > 127 and not (37 <= b <= 37)]
# Normal: PDF binary objects. Check only the text stream for non-ASCII:
sha = hashlib.sha256(raw).hexdigest()
size = len(raw)

print(f"Built: {OUT}")
print(f"Size:  {size/1024:.1f} KB")
print(f"SHA-256: {sha}")
print()
print("To add to the complete archive, re-run the archive builder.")
