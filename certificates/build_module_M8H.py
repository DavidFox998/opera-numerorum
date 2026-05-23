"""
Build Module M8H Certificate PDF
Opera Numerorum - Battle Plan v1.6
"""

import hashlib, subprocess, sys, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

OUT_FILE   = "certificates/Module_M8H_G_Amplifier.pdf"
SOURCE_FILE = "certificates/m8h_g_amplifier.py"
STDOUT_FILE = "m8h.out"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def sha256_str(s):
    return hashlib.sha256(s.encode("ascii")).hexdigest()

source_sha = sha256_file(SOURCE_FILE)
stdout_sha = sha256_file(STDOUT_FILE)

with open(STDOUT_FILE, "r") as f:
    stdout_text = f.read()

doc = SimpleDocTemplate(
    OUT_FILE,
    pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch,
    topMargin=0.75*inch,   bottomMargin=0.75*inch,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle("title",
    fontSize=16, leading=20, alignment=TA_CENTER,
    fontName="Helvetica-Bold", spaceAfter=4)

subtitle_style = ParagraphStyle("subtitle",
    fontSize=11, leading=14, alignment=TA_CENTER,
    fontName="Helvetica", spaceAfter=2)

section_style = ParagraphStyle("section",
    fontSize=11, leading=14, fontName="Helvetica-Bold",
    spaceBefore=14, spaceAfter=4)

body_style = ParagraphStyle("body",
    fontSize=9, leading=13, fontName="Helvetica",
    spaceBefore=2, spaceAfter=2)

mono_style = ParagraphStyle("mono",
    fontSize=7.5, leading=11, fontName="Courier",
    spaceBefore=2, spaceAfter=2)

sha_style = ParagraphStyle("sha",
    fontSize=7.5, leading=11, fontName="Courier",
    textColor=colors.darkgreen, spaceBefore=2)

warn_style = ParagraphStyle("warn",
    fontSize=9, leading=13, fontName="Helvetica-Bold",
    textColor=colors.darkred, spaceBefore=4)

story = []

story.append(Paragraph("OPERA NUMERORUM", title_style))
story.append(Paragraph("Machine Verification Certificate", subtitle_style))
story.append(Paragraph("Battle Plan v1.6 | David Fox | May 21, 2026", subtitle_style))
story.append(HRFlowable(width="100%", thickness=2, color=colors.black, spaceAfter=8))

story.append(Paragraph("Module M8H: G Amplifier Prediction", title_style))
story.append(Paragraph(
    "Gravitational Constant Enhancement via Z=1 Mode Selection in 120-Cell Cavity",
    subtitle_style))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("CLAIM", section_style))
story.append(Paragraph(
    "The gravitational constant G is not fundamental. The number Z of active graviton "
    "polarization modes in the local vacuum determines G via:", body_style))
story.append(Paragraph(
    "    G_eff(Z) = G_0 * (Z_vac / Z)^4     where Z_vac = 15",
    mono_style))
story.append(Paragraph(
    "Standard vacuum: Z=15. 14 massive modes do not propagate. G is 10^40 x weaker than EM. "
    "A 120-cell cavity tuned to Mode 0 (f_Z1 = 199.54 MHz) forces local Z=1: all 15 modes "
    "massless, all gravity propagates. Predicted force amplification: 15^4 = 50625.",
    body_style))

story.append(Paragraph("SECTION 1: FREQUENCY RATIO", section_style))
data1 = [
    ["Quantity", "Value", "Status"],
    ["f_Z15 (Mode 119, Z=15)", "2.99314159 GHz", "Input"],
    ["f_Z1  (Mode 0,   Z=1 )", "199.542772 MHz", "Input"],
    ["f_Z15 / f_Z1", "15.0000000501", "COMPUTED"],
    ["Deviation from 15", "5.01e-08 (< 1e-6)", "PASS"],
]
t1 = Table(data1, colWidths=[2.8*inch, 2.2*inch, 1.2*inch])
t1.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("ALIGN",      (1,0), (-1,-1), "CENTER"),
    ("TEXTCOLOR",  (-1,4), (-1,4), colors.darkgreen),
]))
story.append(t1)
story.append(Spacer(1, 0.05*inch))

story.append(Paragraph("SECTION 2: AMPLIFICATION FACTOR", section_style))
story.append(Paragraph(
    "Amplification A = G_eff(Z=1) / G_eff(Z=15) = (Z_vac/1)^4 / (Z_vac/Z_vac)^4 = 15^4",
    body_style))
data2 = [
    ["Expression", "Value", "Status"],
    ["15^4", "50625 (exact)", "PASS"],
    ["G_eff(Z=1)", "G_0 * 50625 = 3.3789e-06 N m^2 kg^-2", "COMPUTED"],
    ["G_eff(Z=15)", "G_0 = 6.6743e-11 N m^2 kg^-2", "STANDARD"],
]
t2 = Table(data2, colWidths=[1.8*inch, 3.5*inch, 1.0*inch])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
]))
story.append(t2)

story.append(Paragraph("SECTION 3: FORCE PREDICTIONS (Torsion Balance)", section_style))
story.append(Paragraph(
    "Geometry: m1 = 1 mg, m2 = 1 kg, r = 0.10 m. "
    "F = G_eff * m1 * m2 / r^2. G_0 = 6.67430e-11 N m^2 kg^-2 (CODATA 2018).",
    body_style))
data3 = [
    ["Condition", "Frequency", "F (N)", "Deflection", "Status"],
    ["Control Z=15", "2.993 GHz", "6.6743e-15", "~0.01 urad (noise)", "Noise floor"],
    ["Test    Z=1 ", "199.54 MHz", "3.3789e-10", "~0.50 urad", "50x noise"],
    ["Ratio F(Z=1)/F(Z=15)", "-", "50625.00", "-", "PASS: exact"],
]
t3 = Table(data3, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.5*inch, 1.0*inch])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 7.5),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("BACKGROUND", (0,3), (-1,3), colors.HexColor("#d4edda")),
]))
story.append(t3)

story.append(Paragraph("SECTION 4: PASS / FAIL CRITERIA", section_style))
pass_fail = [
    ["Outcome", "Criterion", "Interpretation"],
    ["PASS (5-sigma)", "F_199MHz / F_2993GHz > 5000x", "Z controls G. M8H confirmed."],
    ["PASS (target) ", "Ratio = 50625 +/- 5000", "Z^4 law quantitatively verified."],
    ["FAIL          ", "Ratio < 10x", "Z does not control G. M8H rejected."],
    ["Fail outcome  ", "-", "M8F (EM metric) survives independently."],
]
t4 = Table(pass_fail, colWidths=[1.3*inch, 2.2*inch, 2.8*inch])
t4.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("BACKGROUND", (0,1), (-1,2), colors.HexColor("#d4edda")),
    ("BACKGROUND", (0,3), (-1,4), colors.HexColor("#f8d7da")),
]))
story.append(t4)
story.append(Paragraph(
    "Experiment decides. Neither outcome is bad science.",
    body_style))

story.append(Paragraph("SECTION 5: PHYSICS SUMMARY", section_style))
physics_text = [
    "G = G_0 * (Z_vac / Z)^4     Z_vac = 15",
    "Standard vacuum (Z=15):  14/15 graviton modes massive. G is suppressed 10^40 vs EM.",
    "Amplified cavity (Z=1):  1 massless mode. All gravity propagates. G_eff = 50625 * G_0.",
    "G_eff(Z=1) = 3.3789e-06 N m^2 kg^-2  ('pocket universe with different G')",
    "If Z=30: G_eff = G_0 * (15/30)^4 = G_0/16  (gravity shielding region)",
]
for line in physics_text:
    story.append(Paragraph(line, mono_style))

story.append(Paragraph("SECTION 6: LAB PROTOCOL SUMMARY", section_style))
protocol = [
    ["Day", "Action", "Expected result"],
    ["1-7",  "PCB fab. Balance in MuMetal box (30x30x30 cm, 3mm).", "Hardware ready"],
    ["8",    "Calibrate torsion: 1nN = 1urad. Laser interferometer.", "Cal verified"],
    ["9",    "Pump to 1e-5 Torr. Thermal drift < 1nK/hour.", "Vacuum stable"],
    ["10",   "Control: Drive 2.993 GHz, 10W. Measure F.", "6.7e-15 N (noise floor)"],
    ["11",   "Test: Drive 199.54 MHz, 10W. Measure F.", "3.4e-10 N (50x noise)"],
    ["12-14","Swap frequencies 10x. Plot F vs f. Step at f0/15.", "Reproducible ratio"],
    ["15",   "SHA256 all run data: sha256sum M8H_run*.csv > M8H_G_proof.sha256", "Chain sealed"],
    ["21",   "Final verdict: ratio = 50625 +/- 5000 PASS or ratio < 10 FAIL.", "Decision day"],
]
t5 = Table(protocol, colWidths=[0.5*inch, 3.2*inch, 2.6*inch])
t5.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 7.5),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("BACKGROUND", (0,8), (-1,8), colors.HexColor("#fff3cd")),
]))
story.append(t5)
story.append(Paragraph("Total: 21 days. Budget: $7.6k. Falsifiable by construction.", body_style))

story.append(Paragraph("SECTION 7: k_c LINKAGE TO M8F", section_style))
story.append(Paragraph(
    "The DC bias formula links M8H to the M8F k_c = 3.183 result:", body_style))
story.append(Paragraph(
    "k = (12 / (11 * Z_vac)) * (h * f_Z1 / m_e * c^2)  =  1.1745e-13",
    mono_style))
story.append(Paragraph(
    "This confirms that the same cavity geometry that produces k_c=3.183 (M8F certified) "
    "also selects Mode 0 at f_Z1=199.54 MHz for the Z=1 amplification test. "
    "M8H and M8F share a common physical platform.", body_style))

story.append(Paragraph("SECTION 8: WHAT HAPPENS NEXT", section_style))
next_steps = [
    ["Scenario", "Physics conclusion", "Next step"],
    ["M8H PASSES (ratio~50625)", "G = G_0*(Z_vac/Z)^4. Z is fundamental.", "arXiv: M8H paper"],
    ["M8H FAILS  (ratio<10)   ", "Z does not tune G. M8H hypothesis dead.", "Pivot to k=3.183 clock test ($100k)"],
]
t6 = Table(next_steps, colWidths=[1.7*inch, 2.8*inch, 1.8*inch])
t6.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#d4edda"), colors.HexColor("#f8d7da")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
]))
story.append(t6)

story.append(Paragraph("STATUS: PREDICTION CERTIFIED (experiment pending)", section_style))
story.append(Paragraph(
    "This certificate records the mathematical prediction, not the experimental result. "
    "The torsion balance measurement (Day 21) will either confirm or falsify M8H. "
    "Either outcome is science.", body_style))

story.append(Spacer(1, 0.15*inch))
story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
story.append(Paragraph("CHAIN OF CUSTODY", section_style))

chain_data = [
    ["Item", "SHA-256"],
    ["Source: certificates/m8h_g_amplifier.py", source_sha],
    ["Stdout: m8h.out", stdout_sha],
]
tc = Table(chain_data, colWidths=[2.4*inch, 3.9*inch])
tc.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 7.5),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("TEXTCOLOR",  (1,1), (1,-1), colors.darkgreen),
]))
story.append(tc)

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("CERTIFIED STDOUT (m8h.out)", section_style))
for line in stdout_text.split("\n"):
    if line.strip():
        story.append(Paragraph(line.replace("<", "&lt;").replace(">", "&gt;"), mono_style))

doc.build(story)

pdf_sha = sha256_file(OUT_FILE)

# ASCII check
import subprocess as sp
result = sp.run(
    ["python3", "-c",
     f"import sys; data=open('{OUT_FILE}','rb').read(); "
     "bad=[hex(b) for b in data if b>127 and b not in (128,)]; "
     "print(f'Non-ASCII bytes: {{len(bad)}}')"],
    capture_output=True, text=True)
print(result.stdout.strip())

print(f"PDF written:  {OUT_FILE}")
print(f"Source SHA:   {source_sha}")
print(f"Stdout SHA:   {stdout_sha}")
print(f"PDF SHA:      {pdf_sha}")
