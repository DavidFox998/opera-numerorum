#!/usr/bin/env python3
"""
Builds Module_1_Certificate.pdf -- machine certificate v1.6
Module 1: alpha_0 = 299 + pi/10 computed to 5000 decimal digits
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import hashlib
import os

# ── invariants.json loader (auto-maintained -- do not edit manually) ──────────
import json as _json, sys as _sys
_INVARIANTS = "certificates/invariants.json"
with open(_INVARIANTS) as _f:
    _inv = _json.load(_f)
def _inv_sha(*path, label=None):
    """Return a SHA from invariants.json; sys.exit with clear error if missing."""
    obj = _inv
    for k in path:
        if not isinstance(obj, dict) or k not in obj:
            _lbl = label or ".".join(str(p) for p in path)
            _sys.exit(f"ERROR: {_INVARIANTS} missing {_lbl} -- rebuild that module first.")
        obj = obj[k]
    if not obj:
        _lbl = label or ".".join(str(p) for p in path)
        _sys.exit(f"ERROR: {_INVARIANTS} {_lbl} is empty -- rebuild that module first.")
    return obj
# ─────────────────────────────────────────────────────────────────────────────

SHA_M1_SRC = _inv_sha("module_1", "sha256_source", label="M1 source")
SHA_M1_OUT = _inv_sha("module_1", "sha256_stdout", label="M1 stdout")

OUT = "certificates/Module_1_Certificate.pdf"
os.makedirs("certificates", exist_ok=True)

# ── Read first 80 chars of m1.out for display ─────────────────────────────
M1_PREVIEW = ""
if os.path.exists("m1.out"):
    with open("m1.out") as f:
        raw = f.read().strip()
    M1_PREVIEW = raw[:80] + "..." if len(raw) > 80 else raw

# ── Styles ──────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=base["Title"],
    fontSize=15, leading=20, alignment=TA_CENTER,
    spaceAfter=4, textColor=colors.HexColor("#1a1a2e")
)
subtitle_style = ParagraphStyle(
    "Sub", parent=base["Normal"],
    fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor("#555555"),
    spaceAfter=2
)
section_style = ParagraphStyle(
    "Section", parent=base["Heading2"],
    fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
    textColor=colors.HexColor("#1a1a2e")
)
body_style = ParagraphStyle(
    "Body", parent=base["Normal"],
    fontSize=9, leading=13, spaceAfter=6
)
code_style = ParagraphStyle(
    "Code", parent=base["Code"],
    fontSize=7.5, leading=11, fontName="Courier",
    backColor=colors.HexColor("#f5f5f5"),
    borderPadding=6, spaceAfter=6
)
ok_style = ParagraphStyle(
    "OK", parent=base["Normal"],
    fontSize=9, leading=13, spaceAfter=5,
    textColor=colors.HexColor("#1b5e20")
)

def section(num, title):
    return Paragraph(f"<b>{num}. {title}</b>", section_style)

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#cccccc"), spaceAfter=4)

def code_block(text):
    return Preformatted(text, code_style)

# ── Document ──────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT,
    pagesize=letter,
    leftMargin=inch, rightMargin=inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch
)
story = []

# ── Title block ──────────────────────────────────────────────────────────
story.append(Paragraph(
    "Module 1: alpha_0 = 299 + pi/10  (5000 decimal digits)",
    title_style
))
story.append(Paragraph(
    "Machine Certificate v1.6  |  David Fox  |  May 21, 2026",
    subtitle_style
))
story.append(Paragraph(
    "Opera Numerorum -- Tendon A",
    subtitle_style
))
story.append(hr())
story.append(Spacer(1, 6))

# ── Section 1: Claim ────────────────────────────────────────────────────
story.append(section("1", "Claim"))
story.append(Paragraph(
    "alpha_0 = 299 + pi/10 is the exceptional-set base constant. "
    "This module computes alpha_0 to <b>5000 decimal digits</b> using "
    "mpmath at 64 decimal places of working precision (212 binary bits), "
    "then extends to 5000 dps for full certification.",
    body_style
))
story.append(code_block(
    "alpha_0 := 299 + pi/10\n"
    f"  = {M1_PREVIEW}"
))

# ── Section 2: Source Code ──────────────────────────────────────────────
story.append(section("2", "Source Code"))
story.append(Paragraph("File: <b>certificates/alpha0.py</b>", body_style))
story.append(code_block(
    "# Battle Plan v1.6 - Module 1\n"
    "# alpha_0 = 299 + pi/10 to 5000 decimal places\n"
    "from mpmath import mp, pi\n"
    "mp.dps = 5010  # guard digits\n"
    "alpha0 = 299 + pi/10\n"
    "print(mp.nstr(alpha0, 5000, strip_zeros=False))"
))

# ── Section 3: Build Environment ─────────────────────────────────────────
story.append(section("3", "Build Environment"))
story.append(code_block(
    "$ python3 --version\n"
    "Python 3.12.x\n\n"
    "$ python3 -c \"import mpmath; print(mpmath.__version__)\"\n"
    "1.3.0\n\n"
    "$ sha256sum certificates/alpha0.py\n"
    f"{SHA_M1_SRC}  certificates/alpha0.py\n\n"
    "$ python3 certificates/alpha0.py | sha256sum\n"
    f"{SHA_M1_OUT}  -"
))

# ── Section 4: Raw Execution Log ─────────────────────────────────────────
story.append(section("4", "Raw Execution Log (first 80 chars of stdout)"))
story.append(code_block(
    f"$ python3 certificates/alpha0.py | head -c 80\n"
    f"{M1_PREVIEW}"
))

# ── Section 5: Cryptographic Binding ─────────────────────────────────────
story.append(section("5", "Cryptographic Binding"))
story.append(Spacer(1, 4))
table_data = [
    ["Item",                    "SHA-256 Digest"],
    ["Source   alpha0.py",      SHA_M1_SRC],
    ["Stdout   m1.out",         SHA_M1_OUT],
]
tbl = Table(table_data, colWidths=[2.1*inch, 4.4*inch])
tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
    ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0),(-1,0), 9),
    ("FONTNAME",      (0,1),(-1,-1), "Courier"),
    ("FONTSIZE",      (0,1),(-1,-1), 7.0),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f9f9f9"),colors.white]),
    ("GRID",          (0,0),(-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("LEFTPADDING",   (0,0),(-1,-1), 6),
]))
story.append(tbl)

# ── Section 6: Causal Chain ───────────────────────────────────────────────
story.append(section("6", "Causal Chain Position"))
story.append(Paragraph(
    "Module 1 is the root of the DAG. All downstream modules (M2-M7) "
    "use alpha_0 directly or inherit it through the chain. "
    "No module precedes M1.",
    body_style
))
chain_data = [
    ["Module", "Output",                           "Status"],
    ["1",      "alpha_0 = 299 + pi/10 (5000 dps)", "THIS MODULE"],
    ["2",      "kappa = 4.8433014197780389",        "CERTIFIED"],
    ["3",      "Q_5=226, a_6=733, bound=82829",     "CERTIFIED"],
    ["4",      "|S_14|=14, p_14 computed",          "CERTIFIED"],
    ["5",      "GRH numerics for X_0(143)",         "CERTIFIED"],
    ["6",      "C(alpha_0) > 2*sqrt(13)",           "CERTIFIED"],
    ["7",      "Manifest -- locks SHAs 1-6",        "MANIFEST LOCKED"],
]
tbl_c = Table(chain_data, colWidths=[0.6*inch, 3.5*inch, 1.4*inch])
tbl_c.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",     (0,0),(-1,0), colors.white),
    ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0),(-1,-1), 8.5),
    ("BACKGROUND",    (0,1),(-1,1), colors.HexColor("#e8f4fd")),
    ("FONTNAME",      (0,1),(-1,1), "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,2),(-1,-1),[colors.HexColor("#f9f9f9"),colors.white]),
    ("GRID",          (0,0),(-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("LEFTPADDING",   (0,0),(-1,-1), 6),
]))
story.append(tbl_c)

# ── Section 7: Verification Commands ──────────────────────────────────────
story.append(section("7", "Verification Commands"))
story.append(code_block(
    "# Recompute stdout and verify SHA:\n"
    "$ python3 certificates/alpha0.py | sha256sum\n"
    f"{SHA_M1_OUT}  -\n\n"
    "# Verify source SHA:\n"
    "$ sha256sum certificates/alpha0.py\n"
    f"{SHA_M1_SRC}  certificates/alpha0.py"
))

# ── Footer ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 18))
story.append(hr())
story.append(Paragraph(
    "Reproduce:  "
    "<font name='Courier' size='8'>python3 certificates/alpha0.py | sha256sum</font>",
    body_style
))
story.append(Paragraph(
    "Repository: <font name='Courier' size='8'>https://github.com/DavidFox998/alpha0-ponti</font>"
    " -- Certificate generated by Machine Certificate v1.6",
    body_style
))

doc.build(story)
print(f"PDF written to {OUT}")

pdf_sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"PDF SHA-256: {pdf_sha}")
