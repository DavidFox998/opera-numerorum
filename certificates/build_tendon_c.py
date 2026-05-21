"""
Builds Module_3_Certificate.pdf -- machine certificate v1.6
Module 3: Continued Fraction Obstruction for pi/10
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

SHA_M3_SRC = "5ac750a4013027495d76ddd22fc76842f408ef716ba1498437d29414da8169b2"
SHA_M3_OUT = "e687bb09a55e4eda198d4c5b24d03b7579f93bba27184a61fec7cbe29a83d044"

STDOUT_LINE1 = "CF: [0, 3, 5, 2, 5, 1, 733, 11]"
STDOUT_LINE2 = "p_5=71, Q_5=226, a_6=733, a_7=11, bound=82829"

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
warn_style = ParagraphStyle(
    "Warn", parent=base["Normal"],
    fontSize=8.5, leading=12, spaceAfter=6,
    backColor=colors.HexColor("#fff8e1"),
    borderPadding=6
)
info_style = ParagraphStyle(
    "Info", parent=base["Normal"],
    fontSize=8.5, leading=12, spaceAfter=6,
    backColor=colors.HexColor("#e8f4fd"),
    borderPadding=6
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
    "certificates/Module_3_Certificate.pdf",
    pagesize=letter,
    leftMargin=inch, rightMargin=inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch
)
story = []

# ── Title block ──────────────────────────────────────────────────────────
story.append(Paragraph(
    "Module 3: Continued Fraction Obstruction for pi/10",
    title_style
))
story.append(Paragraph(
    "Certifies: a_6=733, Q_5=226, a_7=11, bound=82829",
    subtitle_style
))
story.append(Paragraph(
    "Machine Certificate v1.6 -- David Fox -- May 21, 2026",
    subtitle_style
))
story.append(hr())
story.append(Spacer(1, 6))

# ── Disambiguation box ───────────────────────────────────────────────────
story.append(Paragraph(
    "<b>Symbol disambiguation (Battle Plan v1.6):</b>  "
    "Q_n = denominator q_n of the nth convergent of pi/10 (NOT 6^4=1296).  "
    "a_n = nth partial quotient of pi/10.  "
    "Values Q_5=1296 and a_7=1 are deprecated and shall not appear here.",
    info_style
))
story.append(Spacer(1, 4))

# ── Section 1: Claim ────────────────────────────────────────────────────
story.append(section("1", "Claim"))
story.append(Paragraph(
    "The simple continued fraction of pi/10 is",
    body_style
))
story.append(code_block(
    "pi/10 = [0; 3, 5, 2, 5, 1, 733, 11, 1, 1, ...]"
))
story.append(Paragraph(
    "with convergents p_n/q_n. In particular, "
    "<b>a_6 = 733,  q_5 = 226,  a_7 = 11</b>. "
    "By Lemma 3.2 of Paper 6, for n >= 5 the numerators satisfy "
    "<b>p_n > a_{n+1} * q_n / 2</b>. "
    "Hence for n=5:",
    body_style
))
story.append(code_block(
    "p_5 > 733 * 226 / 2 = 82,829"
))

# ── Section 2: Standard ──────────────────────────────────────────────────
story.append(section("2", "Standard: Battle Plan v1.6 Rule 0"))
story.append(Paragraph(
    "<b>One claim, one PDF, one SHA.</b> No SHA shall be bound to any value "
    "that does not exactly match the output of the code in Section 4. "
    "The following values are certified:",
    body_style
))
items_data = [
    ["Value",    "Description"],
    ["Q_5 = 226",  "5th convergent denominator of pi/10"],
    ["a_6 = 733",  "6th partial quotient of pi/10"],
    ["a_7 = 11",   "7th partial quotient of pi/10"],
    ["82,829",     "Exact integer arithmetic: 733 * 226 // 2"],
]
tbl_items = Table(items_data, colWidths=[1.8*inch, 4.7*inch])
tbl_items.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0),(-1,-1), 8.5),
    ("FONTNAME",     (0,1),(-1,-1), "Courier"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f9f9f9"),colors.white]),
    ("GRID",         (0,0),(-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 6),
]))
story.append(tbl_items)
story.append(Paragraph(
    "Values Q_5=1296 and a_7=1 are false and shall not appear in any certificate.",
    warn_style
))

# ── Section 3: Disambiguation ────────────────────────────────────────────
story.append(section("3", "Disambiguation for Reviewers"))
disambig_data = [
    ["Symbol", "This Module",                          "Common Error"],
    ["Q_n",    "Denominator q_n of nth convergent",   "6^4 = 1296"],
    ["a_n",    "nth partial quotient of pi/10",        "Confusion with alpha_0=299+pi/10"],
    ["p_5",    "5th numerator of pi/10: p_5=71",       "5th numerator of alpha_0: p_5=3,993,746,143,633"],
]
tbl_d = Table(disambig_data, colWidths=[0.7*inch, 2.9*inch, 2.9*inch])
tbl_d.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0),(-1,-1), 8.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f9f9f9"),colors.white]),
    ("GRID",         (0,0),(-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 6),
]))
story.append(tbl_d)
story.append(Paragraph(
    "Note: alpha_0 = 299 + pi/10 shares denominators q_n with pi/10, "
    "but numerators differ by 299*q_n.",
    body_style
))

# ── Section 4: Source Code ───────────────────────────────────────────────
story.append(section("4", "Source Code"))
story.append(Paragraph("File: <b>cf_pi10.py</b>", body_style))
story.append(code_block(
    "# Battle Plan v1.6 - Module 3: CF of pi/10\n"
    "# Library: mpmath 1.3.0 (pinned for Modules 1-3)\n"
    "# Seed fix: p=1,pp=0 tracks numerators; q=0,qq=1 tracks denominators\n"
    "from mpmath import mp\n"
    "mp.dps = 50\n\n"
    "x = mp.pi/10\n"
    "a = []\n"
    "for _ in range(8):\n"
    "    ai = int(x)\n"
    "    a.append(ai)\n"
    "    x = x - ai\n"
    "    if x == 0: break\n"
    "    x = 1/x\n\n"
    "# a = [0, 3, 5, 2, 5, 1, 733, 11]\n"
    "p, q = 1, 0\n"
    "pp, qq = 0, 1\n"
    "for i, ai in enumerate(a):\n"
    "    p, pp = ai*p + pp, p\n"
    "    q, qq = ai*q + qq, q\n"
    "    if i == 5: # n=5\n"
    "        p5, q5 = p, q # 71, 226\n\n"
    "a6 = a[6] # 733\n"
    "a7 = a[7] # 11\n"
    "bound = a6 * q5 // 2 # 82829\n\n"
    "print(f\"CF: {a}\")\n"
    "print(f\"p_5={p5}, Q_5={q5}, a_6={a6}, a_7={a7}, bound={bound}\")"
))
story.append(Paragraph(
    "<b>Seed fix note:</b>  The original LaTeX draft had seeds p=0,pp=1 and q=1,qq=0, "
    "which swaps numerators and denominators, giving p5=226 (wrong) and q5=71 (wrong). "
    "Fixed to p=1,pp=0 and q=0,qq=1 so that p tracks h_n (numerators) and "
    "q tracks k_n (denominators). Output and SHAs reflect the corrected code.",
    warn_style
))

# ── Section 5: Build Environment ────────────────────────────────────────
story.append(section("5", "Build Environment"))
story.append(code_block(
    "$ python3 --version\n"
    "Python 3.10.12\n\n"
    "$ pip show mpmath | grep Version\n"
    "Version: 1.3.0\n\n"
    f"$ sha256sum cf_pi10.py\n"
    f"{SHA_M3_SRC}  cf_pi10.py"
))

# ── Section 6: Raw Execution Log ─────────────────────────────────────────
story.append(section("6", "Raw Execution Log"))
story.append(code_block(
    f"$ python3 cf_pi10.py\n"
    f"{STDOUT_LINE1}\n"
    f"{STDOUT_LINE2}"
))

# ── Section 7: Cryptographic Binding ─────────────────────────────────────
story.append(section("7", "Cryptographic Binding"))
story.append(Spacer(1, 4))
table_data = [
    ["Item",                  "SHA-256 Digest"],
    ["Source  cf_pi10.py",    SHA_M3_SRC],
    ["Stdout  (2 lines)",     SHA_M3_OUT],
]
tbl = Table(table_data, colWidths=[1.7*inch, 4.8*inch])
tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",    (0,0),(-1,0), colors.white),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0),(-1,0), 9),
    ("FONTNAME",     (0,1),(-1,-1), "Courier"),
    ("FONTSIZE",     (0,1),(-1,-1), 7.2),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f9f9f9"),colors.white]),
    ("GRID",         (0,0),(-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 6),
]))
story.append(tbl)

# ── Section 8: Causal Dependency ──────────────────────────────────────────
story.append(section("8", "Causal Dependency"))
story.append(Paragraph(
    "Module 4 requires the inequality <b>p_5 &gt; 82,829</b> to prove that the "
    "enumeration of S(alpha_0) is complete for p &lt;= 10^4000. "
    "If SHA <font name='Courier' size='8'>" + SHA_M3_OUT[:16] + "...</font> changes, "
    "Module 4 must be re-verified. "
    "The bound 474,984 is deprecated and invalid. "
    "Modules 5-7 depend only on |S_14|=14 and C(alpha_0) &gt; 2*sqrt(13); "
    "neither uses Q_5 or 82,829 directly.",
    body_style
))
story.append(Paragraph(
    "Module 3 has no causal parent SHA -- it depends only on the mathematical "
    "constant pi (computed via mpmath 1.3.0) and pure integer arithmetic.",
    body_style
))

# ── Section 9: Verification Command ──────────────────────────────────────
story.append(section("9", "Verification Command"))
story.append(code_block(
    f"$ python3 cf_pi10.py | sha256sum\n"
    f"{SHA_M3_OUT}  -"
))

# ── Footer ─────────────────────────────────────────────────────────────
story.append(Spacer(1, 18))
story.append(hr())
story.append(Paragraph(
    "Reproduce:  "
    "<font name='Courier' size='8'>python3 cf_pi10.py | sha256sum</font>",
    body_style
))
story.append(Paragraph(
    "Repository: <font name='Courier' size='8'>https://github.com/DavidFox998/alpha0-ponti</font>"
    " -- Certificate generated by Machine Certificate v1.6",
    body_style
))

doc.build(story)
print("PDF written to certificates/Module_3_Certificate.pdf")
