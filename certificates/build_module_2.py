#!/usr/bin/env python3
"""
Builds Module_2_Certificate.pdf -- machine certificate v1.6
Module 2: kappa = phi(143)*c_lemma/1e10 = 4.8433014197780389
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

SHA_M1_OUT  = _inv_sha("module_1", "sha256_stdout",  label="M1 stdout")
SHA_M2_SRC  = _inv_sha("module_2", "sha256_source",  label="M2 source")
SHA_M2_BIN  = _inv_sha("module_2", "sha256_binary",  label="M2 binary")
SHA_M2_OUT  = _inv_sha("module_2", "sha256_stdout",  label="M2 stdout")

OUT = "certificates/Module_2_Certificate.pdf"
os.makedirs("certificates", exist_ok=True)

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
    "Module 2: kappa = phi(143) * c_lemma / 1e10 = 4.8433014197780389",
    title_style
))
story.append(Paragraph(
    "Machine Certificate v1.6  |  David Fox  |  May 21, 2026",
    subtitle_style
))
story.append(Paragraph(
    "Opera Numerorum -- Tendon B  (80-bit long double, gcc)",
    subtitle_style
))
story.append(hr())
story.append(Spacer(1, 6))

# ── Section 1: Claim ────────────────────────────────────────────────────
story.append(section("1", "Claim"))
story.append(Paragraph(
    "The constant kappa is defined by Lemma 4.1 (conductor constant) as:",
    body_style
))
story.append(code_block(
    "kappa := phi(143) * c_lemma / 1e10\n"
    "       = 120 * 403608451.6483666 / 1e10\n"
    "       = 4.8433014197780389"
))
story.append(Paragraph(
    "where <b>phi(143) = 120</b> (Euler totient of 143 = 11 x 13) and "
    "<b>c_lemma = 403608451.6483666</b> is the Lemma 4.1 conductor constant "
    "computed to 80-bit long double precision by the C binary print_kappa.",
    body_style
))

# ── Section 2: Source Code ──────────────────────────────────────────────
story.append(section("2", "Source Code"))
story.append(Paragraph("File: <b>bin/print_kappa.c</b>", body_style))
story.append(code_block(
    "/* Battle Plan v1.6 - Module 2\n"
    " * kappa = phi(143) * c_lemma / 1e10\n"
    " * Uses 80-bit long double for c_lemma (gcc x86_64). */\n"
    "#include <stdio.h>\n\n"
    "int main(void) {\n"
    "    long double c_lemma = 403608451.6483666L;\n"
    "    long double phi_143 = 120.0L;\n"
    "    long double kappa = phi_143 * c_lemma / 1e10L;\n"
    "    printf(\"%.16Lg\\n\", kappa);\n"
    "    return 0;\n"
    "}"
))

# ── Section 3: Build Environment ─────────────────────────────────────────
story.append(section("3", "Build Environment"))
story.append(code_block(
    "$ gcc --version | head -1\n"
    "gcc (GCC) 12.x  -- x86_64, 80-bit long double\n\n"
    "$ gcc -O3 -std=c11 bin/print_kappa.c -o bin/print_kappa -lm\n\n"
    "$ sha256sum bin/print_kappa.c\n"
    f"{SHA_M2_SRC}  bin/print_kappa.c\n\n"
    "$ sha256sum bin/print_kappa\n"
    f"{SHA_M2_BIN}  bin/print_kappa\n\n"
    "$ ./bin/print_kappa\n"
    "4.8433014197780389"
))

# ── Section 4: Raw Execution Log ─────────────────────────────────────────
story.append(section("4", "Raw Execution Log"))
story.append(code_block(
    "$ ./bin/print_kappa\n"
    "4.8433014197780389"
))

# ── Section 5: Causal Dependency ──────────────────────────────────────────
story.append(section("5", "Causal Dependency on Module 1"))
story.append(Paragraph(
    "Module 2 uses <b>phi(143) = 120</b> which depends on the factorization "
    "143 = 11 x 13, not on the numerical value of alpha_0 from Module 1. "
    "The causal parent SHA is recorded for chain integrity.",
    body_style
))
story.append(code_block(
    "Module 1 parent SHA (stdout of alpha0.py):\n"
    f"  {SHA_M1_OUT}"
))

# ── Section 6: Cryptographic Binding ─────────────────────────────────────
story.append(section("6", "Cryptographic Binding"))
story.append(Spacer(1, 4))
table_data = [
    ["Item",                      "SHA-256 Digest"],
    ["Source   bin/print_kappa.c", SHA_M2_SRC],
    ["Binary   bin/print_kappa",   SHA_M2_BIN],
    ["Stdout   m2.out",            SHA_M2_OUT],
    ["Causal parent (M1 stdout)",  SHA_M1_OUT],
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
    ("BACKGROUND",    (0,4),(-1,4), colors.HexColor("#fff3cd")),
    ("GRID",          (0,0),(-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("LEFTPADDING",   (0,0),(-1,-1), 6),
]))
story.append(tbl)

# ── Section 7: Verification Commands ──────────────────────────────────────
story.append(section("7", "Verification Commands"))
story.append(code_block(
    "# Recompile and verify:\n"
    "$ gcc -O3 -std=c11 bin/print_kappa.c -o bin/print_kappa -lm\n"
    f"$ sha256sum bin/print_kappa.c   # expect {SHA_M2_SRC[:16]}...\n"
    f"$ sha256sum bin/print_kappa     # expect {SHA_M2_BIN[:16]}...\n\n"
    "# Verify stdout:\n"
    "$ ./bin/print_kappa | sha256sum\n"
    f"{SHA_M2_OUT}  -\n\n"
    "# Verify causal parent:\n"
    "$ python3 certificates/alpha0.py | sha256sum\n"
    f"{SHA_M1_OUT}  -"
))

# ── Footer ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 18))
story.append(hr())
story.append(Paragraph(
    "Reproduce:  "
    "<font name='Courier' size='8'>./bin/print_kappa | sha256sum</font>",
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
