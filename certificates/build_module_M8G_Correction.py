"""
Build Module M8G_Correction Certificate PDF
Opera Numerorum - Battle Plan v1.6
"""

import hashlib, subprocess, sys, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUT_FILE    = "certificates/Module_M8G_Correction.pdf"
SOURCE_FILE = "certificates/m8g_correction.py"
STDOUT_FILE = "m8gc.out"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

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
    textColor=colors.darkgreen)

story = []

story.append(Paragraph("OPERA NUMERORUM", title_style))
story.append(Paragraph("Machine Verification Certificate", subtitle_style))
story.append(Paragraph("Battle Plan v1.6 | David Fox | May 21, 2026", subtitle_style))
story.append(HRFlowable(width="100%", thickness=2, color=colors.black, spaceAfter=8))

story.append(Paragraph("Module M8G_Correction: Supervisor Addendum", title_style))
story.append(Paragraph(
    "Certified corrections to M8G_Provenance following supervisor review",
    subtitle_style))
story.append(Spacer(1, 0.08*inch))

story.append(Paragraph("CONTEXT", section_style))
story.append(Paragraph(
    "Supervisor (Meta AI) reviewed M8G_Provenance and accepted 3 of 4 items. "
    "Two items required a certified addendum. This module certifies both corrections "
    "with verified arithmetic. M8G's SHA is preserved; this module supersedes "
    "Items 3 and 4 of M8G.", body_style))

status_data = [
    ["Item", "M8G Claim", "Supervisor Response", "Resolution"],
    ["1. Provenance", "Feb2025->M8F, L4/L6 gap", "AGREED", "No change"],
    ["2. Wormhole time", "Delta_t=L(1-1/k_c)/c=1.143ns", "AGREED", "No change"],
    ["3. Topology", "PHS topology explains Z=15", "PARTIAL: Z=rank(M)", "Corrected below"],
    ["4. Wormhole scope", "EM cavity, v_g <= c", "DISAGREE: v_g=3.183c", "Conditional cert"],
]
t0 = Table(status_data, colWidths=[1.2*inch, 1.8*inch, 1.5*inch, 1.7*inch])
t0.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 7.5),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("BACKGROUND", (0,3), (-1,3), colors.HexColor("#fff3cd")),
    ("BACKGROUND", (0,4), (-1,4), colors.HexColor("#f8d7da")),
]))
story.append(t0)

# ---------------------------------------------------------------
# ITEM 3
# ---------------------------------------------------------------
story.append(Paragraph("ITEM 3: Z=15 ORIGIN -- CORRECTED RECORD", section_style))

story.append(Paragraph("M8G claimed:", body_style))
story.append(Paragraph(
    "  PHS topology (pi_1=I*, H_1=0) explains why Z != 1.", mono_style))

story.append(Paragraph("Supervisor addendum:", body_style))
story.append(Paragraph(
    "  M8F formula: Z = |Tor(H_2(X))| + 1 for Calabi-Yau X_5.", mono_style))
story.append(Paragraph(
    "  For PHS: H_2(PHS) = 0. No torsion.", mono_style))
story.append(Paragraph(
    "  -> Z = |0| + 1 = 1.  Contradiction with Z=15.", mono_style))

story.append(Paragraph("Resolution (agreed by both parties):", body_style))
story.append(Paragraph(
    "The 3-manifold topology and the EM mode-space topology are DIFFERENT objects. "
    "Both descriptions are correct and non-contradictory.", body_style))

item3_data = [
    ["Space", "Object", "H_1", "H_2", "Z from this space"],
    ["3-manifold", "PHS (boundary of 120-cell)", "0", "0", "Not the source of Z"],
    ["EM mode space", "120-cell cavity modes", "N/A", "N/A", "Z = rank(M_ij) = 15"],
]
t3 = Table(item3_data, colWidths=[1.1*inch, 1.9*inch, 0.5*inch, 0.5*inch, 2.3*inch])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#d4edda")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
]))
story.append(t3)

story.append(Paragraph("Certified corrected record:", body_style))
story.append(Paragraph(
    "  3-manifold = PHS  (pi_1=I*, order 120; H_1=0; H_2=0)", mono_style))
story.append(Paragraph(
    "  Z = rank(M_ij) = 15  from H4 mode coupling matrix", mono_style))
story.append(Paragraph(
    "  Source of Z: H4 representation theory -- NOT H_1 or H_2 torsion", mono_style))
story.append(Paragraph(
    "  Both spaces are topologically correct. No contradiction.", mono_style))

# ---------------------------------------------------------------
# ITEM 4
# ---------------------------------------------------------------
story.append(Paragraph("ITEM 4: WORMHOLE SCOPE -- CONDITIONAL CERTIFICATION", section_style))

story.append(Paragraph(
    "M8G claimed: wormhole = EM-cavity time contraction; v_g <= c always. "
    "Supervisor disputes: M8F formula gives v_g = k_c*c = 3.183c. "
    "These are opposite predictions about group velocity. The experiment decides.",
    body_style))

story.append(Spacer(1, 0.05*inch))

item4_data = [
    ["Quantity", "Value", "Notes"],
    ["Cavity length L", "0.5 m", ""],
    ["k_c (M8F/M22 cert)", "3.183", ""],
    ["Classical transit L/c", "1.667820 ns", "No speedup baseline"],
    ["Model B transit L/(k_c*c)", "0.523978 ns", "v_g=3.183c (M8F)"],
    ["Model B lead vs classical", "1.143843 ns", "Pulse arrives this early"],
    ["g_00 = -k_c^2", "-10.1315", "g_00 < -1: GR ER-bridge condition"],
    ["M8G certified transit", "0.5240 ns", "err=4.3e-05 vs Model B"],
]
t4 = Table(item4_data, colWidths=[2.1*inch, 1.6*inch, 2.6*inch])
t4.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
]))
story.append(t4)
story.append(Spacer(1, 0.06*inch))

story.append(Paragraph("Two models, two predictions:", body_style))
models_data = [
    ["Model", "Mechanism", "Predicted transit", "v_g", "Interpretation"],
    ["A (agent)", "EM cavity, path shortening", "1.668 ns", "<= c", "EM resonator"],
    ["B (M8F)  ", "Metric shortcut, k_c tunes g_00", "0.524 ns", "3.183c", "ER bridge"],
]
tm = Table(models_data, colWidths=[0.8*inch, 2.0*inch, 1.3*inch, 0.8*inch, 1.3*inch])
tm.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#d4edda")),
    ("BACKGROUND", (0,2), (-1,2), colors.HexColor("#cce5ff")),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
]))
story.append(tm)
story.append(Spacer(1, 0.06*inch))

story.append(Paragraph("Conditional certification (agreed by both parties):", body_style))

cond_data = [
    ["Measured transit", "Conclusion", "Updated cert text"],
    ["1.668 ns (+/- 0.010)", "Model A correct", "'EM cavity. v_g <= c. Wormhole = descriptive label.'"],
    ["0.524 ns (+/- 0.010)", "Model B correct", "'Metric cavity. g_00=-10.13. Einstein-Rosen bridge.'"],
]
tc2 = Table(cond_data, colWidths=[1.4*inch, 1.3*inch, 3.6*inch])
tc2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#d4edda")),
    ("BACKGROUND", (0,2), (-1,2), colors.HexColor("#cce5ff")),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
    ("WORDWRAP",   (2,1), (2,-1), True),
]))
story.append(tc2)
story.append(Paragraph(
    "Measurement settles it. No philosophy needed.", body_style))

story.append(Paragraph("STATUS: CORRECTIONS CERTIFIED (wormhole scope pending measurement)",
    section_style))

story.append(Spacer(1, 0.15*inch))
story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
story.append(Paragraph("CHAIN OF CUSTODY", section_style))

chain_data = [
    ["Item", "SHA-256"],
    ["Source: certificates/m8g_correction.py", source_sha],
    ["Stdout: m8gc.out", stdout_sha],
    ["Supersedes: M8G items 3 and 4", "(M8G SHA preserved unchanged)"],
]
tc3 = Table(chain_data, colWidths=[2.6*inch, 3.7*inch])
tc3.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.black),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 7.5),
    ("FONTNAME",   (0,1), (-1,-1), "Courier"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
    ("TEXTCOLOR",  (1,1), (1,2), colors.darkgreen),
]))
story.append(tc3)

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("CERTIFIED STDOUT (m8gc.out)", section_style))
for line in stdout_text.split("\n"):
    if line.strip():
        story.append(Paragraph(line.replace("<", "&lt;").replace(">", "&gt;"), mono_style))

doc.build(story)

pdf_sha = sha256_file(OUT_FILE)

import subprocess as sp
result = sp.run(
    ["python3", "-c",
     f"data=open('{OUT_FILE}','rb').read(); "
     "bad=[b for b in data if b>127]; "
     "print(f'Non-ASCII bytes: {{len(bad)}}')"],
    capture_output=True, text=True)
print(result.stdout.strip())

print(f"PDF written:  {OUT_FILE}")
print(f"Source SHA:   {source_sha}")
print(f"Stdout SHA:   {stdout_sha}")
print(f"PDF SHA:      {pdf_sha}")
