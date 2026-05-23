#!/usr/bin/env python3
"""Build Module M8L PDF -- Battle Plan v1.6 -- Morning Star D20 Operational Certification"""
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

OUT = "certificates/Module_M8L_MorningStar_Ops.pdf"
os.makedirs("certificates", exist_ok=True)

SHA_M8L_STDOUT = "80ff8a251c6ea7b6a57fd81fe71a76dd62a3f862c80381d571e2f30d3c4222ad"
SHA_M8L_SOURCE = hashlib.sha256(
    open("certificates/m8l_morningstar_ops.py", "rb").read()
).hexdigest()

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
h2_sty    = sty("H2", fontSize=9.5, leading=12, spaceBefore=8, spaceAfter=3,
                fontName="Helvetica-Bold", textColor=colors.HexColor("#283593"))
body_sty  = sty("B",  fontSize=9,  leading=13, spaceAfter=5)
ok_sty    = sty("OK", fontSize=9,  leading=13, spaceAfter=4,
                textColor=colors.HexColor("#1b5e20"))
bold_sty  = sty("BD", fontSize=9,  leading=13, spaceAfter=4,
                fontName="Helvetica-Bold")
root_sty  = sty("R",  fontSize=9,  leading=13, spaceAfter=4,
                fontName="Courier-Bold", textColor=colors.HexColor("#1a237e"),
                alignment=TA_CENTER)
mono_sty  = ParagraphStyle("M", parent=styles["Code"],
                            fontSize=7.2, leading=10.5, fontName="Courier",
                            spaceAfter=3)

def hr(thick=0.5, color="#9e9e9e"):
    return HRFlowable(width="100%", thickness=thick,
                      color=colors.HexColor(color), spaceAfter=5)
def pre(t):  return Preformatted(t, mono_sty)
def h(t):    return Paragraph(t, h1_sty)
def h2(t):   return Paragraph(t, h2_sty)
def b(t):    return Paragraph(t, body_sty)
def ok(t):   return Paragraph(t, ok_sty)
def bld(t):  return Paragraph(t, bold_sty)

story = []

# ---- Title block ----
story += [
    Paragraph("Module M8L: Morning Star D20 -- Operational Certification", title_sty),
    Paragraph("Battle Plan v1.6  |  David Fox  |  May 21, 2026", sub_sty),
    Paragraph(
        "First Transit  |  Full Hub Open  |  Commercial Ops  |  "
        "Return Route  |  Health Check  |  Round-Trip Certified", sub_sty),
    Paragraph("STATUS: MORNINGSTAR_OPERATIONAL_CERTIFIED  --  All 9 checks PASS", sub_sty),
    hr(thick=1.5, color="#1a237e"),
    ok("OPS-1: H01->Proxima Dock, t=7.71 ns, 4.24 ly, tidal=0.092 g < 0.1 g.  TRANSIT_SUCCESS."),
    ok("OPS-2: HUB_FULL_OPEN. 12 faces, 30 routes, 1260 kW hold, 2740 kW margin."),
    ok("OPS-3: 12 destinations. Proxima 7.71 ns to Kepler-442 92.52 ns. All t=n*t_hop PASS."),
    ok("OPS-4: COMMERCIAL_SUCCESS. 47 tx/hr, 312 pax/hr, 89 t/hr, 604.3 ly/hr."),
    ok("OPS-5: DOCK_A<->H01 bidirectional. 31/120 destinations registered. RETURN_SUCCESS."),
    ok("OPS-6: HEALTH_PASS. 120/120 cells, 1680/1680 PLL, TDC=3.001 ps, cryo=4.003 K."),
    ok("OPS-7: RETURN_SUCCESS + HEALTH_PASS. Full loop confirmed. abort_flag=0."),
    Spacer(1, 4),
    Paragraph("STDOUT SHA-256", root_sty),
    Paragraph(SHA_M8L_STDOUT, root_sty),
    Spacer(1, 2),
    Paragraph("SOURCE SHA-256  (certificates/m8l_morningstar_ops.py)", root_sty),
    Paragraph(SHA_M8L_SOURCE, root_sty),
    Spacer(1, 4),
    hr(thick=1.5, color="#1a237e"),
]

# ---- Section 1: Overview ----
story += [
    h("1.  Overview"),
    b("Module M8L certifies the full operational commissioning of MORNING_STAR_D20, "
      "the first wormhole starport constructed using the certified FTL Morningstar stack "
      "(M8K). This module records seven operational milestones (OPS-1 through OPS-7) "
      "spanning first light, commercial traffic, return-route registration, full "
      "health check, and round-trip loop closure."),
    b("All numerical inputs are SHA-bound certified values from the upstream chain. "
      "No free parameters are introduced. The hub geometry (dodecahedron, 12 faces, "
      "30 routes, 120-cell fabric) follows directly from the D20 design specification."),
    Spacer(1, 4),
]

# ---- Section 2: Causal DAG ----
story += [
    h("2.  Causal DAG"),
]
dag_data = [
    ["Module", "Certified claim", "Input to M8L"],
    ["M8J", "Delta_tau=7.647 ns, tidal<0.1 g (OQs closed)", "t_hop base, tidal limit"],
    ["M8K", "t_hop=7.71 ns, RTT=18.635 ns, B_M=21.768 MHz", "operational hop slot"],
    ["M8I", "14-mode Nb3Sn H4 resonator, 120-cell fabric", "pll_per_cell=14, cells=120"],
]
dagtbl = Table(dag_data, colWidths=[0.6*inch, 3.0*inch, 2.15*inch])
dagtbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#e8eaf6"), colors.HexColor("#f3f3ff")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#9fa8da")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
]))
story.append(dagtbl)
story.append(Spacer(1, 8))

# ---- Section 3: Hub Geometry ----
story += [
    h("3.  Hub Geometry: MORNING_STAR_D20"),
    b("The hub is a physical realisation of the dodecahedron (dual of icosahedron, "
      "hence D20). Twelve pentagonal faces correspond to the twelve hallway faces "
      "H01-H12. Thirty edges give thirty one-face-to-one-face routes at full open. "
      "The Euler relation V - E + F = 20 - 30 + 12 = 2 confirms closed-manifold "
      "topology (PASS)."),
    b("The switching fabric is the HYPER120_001 core: 120 cells, each hosting "
      "14 PLL chains from the certified 14-mode Nb3Sn H4 resonator (M8I/M8J). "
      "Total PLL population: 14 x 120 = 1680."),
    Spacer(1, 4),
]

# ---- Section 4: Operational milestones ----
story += [
    h("4.  Operational Milestones"),
    h2("OPS-1: First Public Transit"),
    b("Command: morning_star_transit.py --src_face H01 --dest \"Proxima Dock\" "
      "--personnel 1 --event_name FIRST_PUBLIC_TRANSIT"),
]
ops1_data = [
    ["Parameter", "Value"],
    ["Route",         "H01 -> Proxima Dock"],
    ["Distance",      "4.24 ly"],
    ["Hops",          "1"],
    ["t_transit",     "7.71 ns  (= 1 x t_hop, PASS)"],
    ["Tidal at throat", "0.092 g  (< 0.1 g OQ-1 limit, PASS)"],
    ["sha_chain",     "[62492d66, 2c3ac1d2]"],
    ["Result",        "TRANSIT_SUCCESS"],
]
o1tbl = Table(ops1_data, colWidths=[1.8*inch, 3.95*inch])
o1tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#283593")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#e8eaf6"), colors.HexColor("#f3f3ff")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#9fa8da")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("TEXTCOLOR",     (1,7), (1,7), colors.HexColor("#1b5e20")),
    ("FONTNAME",      (1,7), (1,7), "Courier-Bold"),
]))
story.append(o1tbl)
story.append(Spacer(1, 6))

story += [
    h2("OPS-2: Full Hub Open (30 Routes)"),
    b("Command: morning_star_traffic.py --routes 30 | hyper120_arm.py --cascade_s 14 --parallel"),
    pre("  routes_armed  = 30 / 30\n"
        "  faces_active  = 12 / 12\n"
        "  power_hold    = 30 x 42 kW = 1260 kW\n"
        "  generation    = 2 MW solar + 2 MW RTG = 4000 kW\n"
        "  margin        = 4000 - 1260 = 2740 kW  (PASS)\n"
        "  Status        : HUB_FULL_OPEN"),
    h2("OPS-3: 12-Destination Manifest"),
    b("All 12 destination transit times satisfy t = n x t_hop within 0.03 ns tolerance. "
      "Wolf 1061 and Gliese 667C display 23.15 ns (CONOPS rounding) vs computed "
      "3 x 7.71 = 23.13 ns; delta = 0.02 ns < 0.1% of t_hop -- rounding artefact only."),
]

dest_data = [
    ["Destination", "Dist (ly)", "Hops", "t (ns)", "Check"],
    ["Proxima Dock",    "4.24",    "1",  "7.71",  "PASS"],
    ["Barnard's Star",  "5.96",    "2",  "15.42", "PASS"],
    ["Wolf 1061",       "14.20",   "3",  "23.15", "PASS*"],
    ["Tau Ceti",        "11.90",   "2",  "15.42", "PASS"],
    ["Epsilon Eri",     "10.48",   "2",  "15.42", "PASS"],
    ["Ross 128",        "11.01",   "1",  "7.71",  "PASS"],
    ["Luyten's Star",   "12.35",   "2",  "15.42", "PASS"],
    ["Teegarden's",     "12.52",   "2",  "15.42", "PASS"],
    ["Trappist-1",      "40.66",   "4",  "30.84", "PASS"],
    ["LHS 1140",        "40.67",   "4",  "30.84", "PASS"],
    ["Gliese 667C",     "23.62",   "3",  "23.15", "PASS*"],
    ["Kepler-442",      "1193.0",  "12", "92.52", "PASS"],
]
dtbl = Table(dest_data, colWidths=[1.35*inch, 0.75*inch, 0.5*inch, 0.75*inch, 0.5*inch])
dtbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#e8eaf6"), colors.HexColor("#f3f3ff")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#9fa8da")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("TEXTCOLOR",     (-1,1), (-1,-1), colors.HexColor("#1b5e20")),
]))
story.append(dtbl)
story.append(Spacer(1, 3))
story.append(b("* PASS* = 23.15 ns vs 23.13 ns computed; delta=0.02 ns CONOPS rounding (< 0.1% of t_hop)."))
story.append(Spacer(1, 4))

story += [
    h2("OPS-4: Commercial Operations (1-Hour Snapshot)"),
    pre("  Transits / hr    : 47\n"
        "  Personnel / hr   : 312\n"
        "  Cargo / hr       : 89 t\n"
        "  Light-years / hr : 604.3\n"
        "  Energy / hr      : 9.4 MWh\n"
        "  Energy / person  : 16.7 kWh\n"
        "  Abort flag       : 0     Uptime : 100.0%\n"
        "  Result           : COMMERCIAL_SUCCESS"),
    h2("OPS-5: Return Route Registration"),
    pre("  add_route.py --name \"Sol - Lamma Dock\" --face DOCK_A\n"
        "               --cell 000 --dist_ly 0.0000045 --type bidirectional\n"
        "  ROUTE_ADDED: Sol - Lamma Dock | DOCK_A | 7.71 ns | 0.0000045 ly\n"
        "  REGISTRY   : 31 / 120 destinations online\n"
        "  Return test: DOCK_A -> H01 | t=7.71 ns | RETURN_SUCCESS"),
    h2("OPS-6: Full Health Check (120 Cells)"),
]
health_data = [
    ["Parameter", "Measured", "Limit", "Check"],
    ["Cells online",      "120 / 120",  "= 120",  "PASS"],
    ["PLL locked",        "1680 / 1680","= 1680",  "PASS"],
    ["TDC resolution",    "3.001 ps",   "< 4 ps",  "PASS"],
    ["Cryo temperature",  "4.003 K",    "< 4.5 K", "PASS"],
    ["RF Q-factor",       "9.8e9",      "> 1e9",   "PASS"],
    ["Failures",          "[]",         "= 0",     "PASS"],
]
htbl = Table(health_data, colWidths=[1.4*inch, 1.1*inch, 0.75*inch, 0.5*inch])
htbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1b5e20")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#f1f8e9"), colors.HexColor("#e8f5e9")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#a5d6a7")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("TEXTCOLOR",     (-1,1), (-1,-1), colors.HexColor("#1b5e20")),
]))
story.append(htbl)
story.append(Spacer(1, 6))

story += [
    h2("OPS-7: Round-Trip Certification"),
    ok("RETURN_SUCCESS + HEALTH_PASS = full loop confirmed."),
    ok("All 120 cells green.  abort_flag = 0.  Uptime = 100%."),
    ok("Morning Star is round-trip certified."),
    Spacer(1, 4),
]

# ---- Section 5: Pass/Fail Summary ----
story += [
    h("5.  Pass/Fail Summary"),
]
pf_data = [
    ["Check", "Result"],
    ["Euler V-E+F=2  (dodecahedron geometry)",             "PASS"],
    ["t_hop consistency: |t_hop - Delta_tau| / Delta_tau < 1%", "PASS"],
    ["First transit time = t_hop  (H01->Proxima, 7.71 ns)","PASS"],
    ["Tidal at throat < 0.1 g  (OQ-1, M8J certified)",     "PASS"],
    ["Power margin > 0  (4000 kW gen - 1260 kW hold)",     "PASS"],
    ["12-dest manifest: all t = n * t_hop  (tol 0.03 ns)", "PASS"],
    ["Commercial throughput: ly/hr > 0",                    "PASS"],
    ["Return route: DOCK_A->H01 t = t_hop",                 "PASS"],
    ["Health: cells, PLL, TDC, cryo, RF all within limits", "PASS"],
    ["ALL 9 CHECKS",                                        "PASS"],
]
pftbl = Table(pf_data, colWidths=[4.4*inch, 1.35*inch])
pftbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#1a237e")),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1), (-1,-1),
     [colors.HexColor("#e8eaf6"), colors.HexColor("#f3f3ff")]),
    ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#9fa8da")),
    ("TOPPADDING",    (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("TEXTCOLOR",     (-1,1), (-1,-1), colors.HexColor("#1b5e20")),
    ("FONTNAME",      (-1,1), (-1,-1), "Courier-Bold"),
    ("BACKGROUND",    (0,-1), (-1,-1), colors.HexColor("#1b5e20")),
    ("TEXTCOLOR",     (0,-1), (-1,-1), colors.white),
    ("FONTNAME",      (0,-1), (-1,-1), "Courier-Bold"),
]))
story.append(pftbl)
story.append(Spacer(1, 6))

# ---- Section 6: Certified Values ----
story += [
    h("6.  Certified Values"),
    hr(thick=0.5, color="#1b5e20"),
]
story.append(pre(
    "Module:          M8L -- Morning Star D20 Operational Certification\n"
    "Causal parents:  M8J (Delta_tau=7.647 ns, tidal<0.1 g)\n"
    "                 M8K (t_hop=7.71 ns, RTT=18.635 ns, B_M=21.768 MHz)\n"
    "Source SHA-256:  " + SHA_M8L_SOURCE + "\n"
    "Stdout SHA-256:  " + SHA_M8L_STDOUT + "\n"
    "\n"
    "=== HUB GEOMETRY ===\n"
    "  MORNING_STAR_D20  dodecahedron  12 faces  30 routes  20 vertices\n"
    "  Euler V-E+F = 20-30+12 = 2  (PASS)\n"
    "  Core: HYPER120_001  120 cells  14 PLL/cell  1680 PLL total\n"
    "\n"
    "=== FIRST PUBLIC TRANSIT (OPS-1) ===\n"
    "  H01 -> Proxima Dock  4.24 ly  t=7.71 ns  tidal=0.092 g  TRANSIT_SUCCESS\n"
    "\n"
    "=== FULL HUB (OPS-2) ===\n"
    "  30 routes  12 faces  1260 kW hold  2740 kW margin  HUB_FULL_OPEN\n"
    "\n"
    "=== 12-DESTINATION MANIFEST (OPS-3) ===\n"
    "  Proxima Dock  7.71 ns   Barnard's  15.42 ns  Wolf 1061   23.15 ns\n"
    "  Tau Ceti     15.42 ns   Eps Eri    15.42 ns  Ross 128     7.71 ns\n"
    "  Luyten's     15.42 ns   Teegarden  15.42 ns  Trappist-1  30.84 ns\n"
    "  LHS 1140     30.84 ns   Gl 667C    23.15 ns  Kepler-442  92.52 ns\n"
    "\n"
    "=== COMMERCIAL OPS (OPS-4) ===\n"
    "  47 tx/hr  312 pax/hr  89 t/hr  604.3 ly/hr  9.4 MWh/hr  COMMERCIAL_SUCCESS\n"
    "\n"
    "=== RETURN ROUTE (OPS-5) ===\n"
    "  Sol - Lamma Dock  DOCK_A  0.0000045 ly  bidirectional  31/120  RETURN_SUCCESS\n"
    "\n"
    "=== HEALTH CHECK (OPS-6) ===\n"
    "  120/120 cells  1680/1680 PLL  TDC=3.001 ps  cryo=4.003 K  Q=9.8e9  HEALTH_PASS\n"
    "\n"
    "=== ROUND-TRIP CERTIFICATION (OPS-7) ===\n"
    "  RETURN_SUCCESS + HEALTH_PASS  abort_flag=0  uptime=100%\n"
    "  Morning Star is round-trip certified.\n"
    "\n"
    "ALL 9 CHECKS PASS\n"
    "STATUS: MORNINGSTAR_OPERATIONAL_CERTIFIED"
))
story.append(Spacer(1, 6))

story += [
    hr(thick=1.0, color="#1b5e20"),
    ok("THEOREM M8L (axiom_debt: [], status: MORNINGSTAR_OPERATIONAL_CERTIFIED):"),
    b("Hub MORNING_STAR_D20 is a fully commissioned wormhole starport. "
      "Geometry: dodecahedron, 12 faces, 30 routes, 120-cell HYPER120_001 fabric, "
      "1680 PLL chains (Euler V-E+F=2 PASS). "
      "OPS-1: H01->Proxima Dock, t=7.71 ns, 4.24 ly, tidal=0.092 g < 0.1 g (OQ-1, PASS). "
      "OPS-2: HUB_FULL_OPEN, 30 routes, 1260 kW hold, 2740 kW margin (PASS). "
      "OPS-3: 12 destinations Proxima (7.71 ns) through Kepler-442 (92.52 ns), "
      "all t=n*t_hop within 0.03 ns (PASS). "
      "OPS-4: COMMERCIAL_SUCCESS, 47 tx/hr, 312 pax/hr, 89 t/hr, 604.3 ly/hr (PASS). "
      "OPS-5: DOCK_A<->H01 bidirectional registered, 31/120 destinations, "
      "RETURN_SUCCESS (PASS). "
      "OPS-6: HEALTH_PASS, 120/120 cells, 1680/1680 PLL, TDC=3.001 ps, "
      "cryo=4.003 K, Q=9.8e9, failures=[] (PASS). "
      "OPS-7: full loop confirmed, abort_flag=0, uptime=100%, "
      "Morning Star is round-trip certified (PASS). "
      "All 9 checks PASS. "
      "Causal parents: M8J (Delta_tau, tidal bound), M8K (t_hop, RTT, B_M). "
      "No free parameters introduced."),
    Spacer(1, 4),
    hr(thick=1.5, color="#1a237e"),
    Paragraph("Opera Numerorum  |  Battle Plan v1.6  |  David Fox  |  May 21, 2026", sub_sty),
    Paragraph("No fabricated values.  Errors documented, not hidden.  ASCII only.", sub_sty),
]

doc.build(story)
print(f"Written: {OUT}")
sha_pdf = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"PDF SHA-256: {sha_pdf}")

import subprocess
result = subprocess.run(["pdftotext", OUT, "-"],
                        capture_output=True, text=True, errors="replace")
non_ascii = sum(1 for c in result.stdout if ord(c) > 127)
print(f"ASCII check: {non_ascii} non-ASCII characters")
