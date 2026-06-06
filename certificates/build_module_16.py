"""
Build Module_16_c_Bridge.pdf
Battle Plan v1.6 | David Fox | May 2026
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import hashlib, sys

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

OUTPUT = "certificates/Module_16_c_Bridge.pdf"

styles = getSampleStyleSheet()
def PS(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_s = PS("T",  fontSize=13, leading=16, alignment=TA_CENTER,
             spaceAfter=3, fontName="Helvetica-Bold")
sub_s   = PS("S",  fontSize=8.5, leading=11, alignment=TA_CENTER, spaceAfter=2)
sec_s   = PS("H",  fontSize=10, leading=13, spaceBefore=8, spaceAfter=3,
             fontName="Helvetica-Bold", textColor=colors.HexColor("#1a1a6e"))
body_s  = PS("B",  fontSize=8, leading=11, alignment=TA_JUSTIFY)
mono_s  = PS("M",  fontSize=7.5, leading=10, fontName="Courier", leftIndent=12)
ok_s    = PS("OK", fontSize=8, leading=10,
             textColor=colors.HexColor("#1a6e1a"), fontName="Helvetica-Bold")
note_s  = PS("N",  fontSize=7.5, leading=10,
             textColor=colors.HexColor("#444444"))
cert_s  = PS("C",  fontSize=9, alignment=TA_CENTER, fontName="Helvetica-Bold",
             textColor=colors.HexColor("#1a1a6e"))
warn_s  = PS("W",  fontSize=7.5, leading=10,
             textColor=colors.HexColor("#8B4500"))

SCRIPT_SHA  = sys.argv[1] if len(sys.argv) >= 3 else "(see m16.out)"
STDOUT_SHA  = sys.argv[2] if len(sys.argv) >= 3 else "(see m16.out)"

M1_SHA  = _inv_sha("module_1", "sha256_stdout", label="M1 stdout")
M4_SHA  = _inv_sha("module_4", "sha256_stdout", label="M4 stdout")

story = []

story.append(Paragraph("Module 16: c-Bridge Certificate", title_s))
story.append(Paragraph(
    "Certified numerical observation: c/10^6 vs beta_0 = 299 + pi/10  |  May 2026",
    sub_s))
story.append(Paragraph("Battle Plan v1.6  --  David Fox", sub_s))
story.append(HRFlowable(width="100%", thickness=1,
             color=colors.HexColor("#1a1a6e"), spaceAfter=5))

story.append(Paragraph(
    "This certificate records the precise numerical relationship between the "
    "speed of light c (SI definition, exact) and the transcendental constant "
    "beta_0 = 299 + pi/10 that defines the S_4 exceptional prime set. "
    "All values are computed at 100 decimal places using mpmath 1.3.0. "
    "No causal or physical claim is made -- this is a certified numerical observation.",
    body_s))
story.append(Spacer(1, 4))

# Core constants table
story.append(Paragraph("Core Constants", sec_s))
cdata = [
    ["Constant", "Value", "Source"],
    ["beta_0 = 299 + pi/10",
     "299.31415926535897932384626433832795...",
     "mpmath pi / 10 (100 dps); M1 SHA 63ef870a..."],
    ["c (m/s)",
     "299792458  [exact]",
     "SI definition of the metre (1983)"],
    ["c / 10^6",
     "299.792458  [exact]",
     "derived from c (m/s)"],
]
cw = [1.5*inch, 2.8*inch, 2.2*inch]
ct = Table(cdata, colWidths=cw)
ct.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1a1a6e")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f0f0ff"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(ct)

# Ratio analysis table
story.append(Paragraph("Ratio Analysis", sec_s))
rdata = [
    ["Quantity", "Certified Value (100 dps)"],
    ["r = (c/10^6) / beta_0",
     "1.001597982320031113926463891128826083..."],
    ["epsilon = r - 1",
     "0.001597982320031113926463891128826083..."],
    ["1 / epsilon",
     "625.789151397200216..."],
    ["1/625  [reference]",
     "0.0016  [= 0.001599999...  repeating]"],
    ["epsilon - 1/625",
     "-0.000002017679968886074...  [epsilon < 1/625]"],
    ["Relative gap |eps - 1/625| / (1/625)",
     "0.00126105...  [0.13%]"],
]
cw2 = [2.5*inch, 4.0*inch]
rt = Table(rdata, colWidths=cw2)
rt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#2c2c5e")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f8f8ff"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(rt)

# Gap / interval analysis
story.append(Paragraph("Gap Analysis: The Interval [beta_0, 300]", sec_s))
story.append(Paragraph(
    "The number 300 is the nearest integer above beta_0. Both c/10^6 and 300 "
    "are 'near-integer' perturbations of beta_0. The gaps are:",
    body_s))
story.append(Spacer(1, 3))
gdata = [
    ["Gap", "Value", "Comment"],
    ["c/10^6 - beta_0",
     "0.47829873464102067615...",
     "How far c/10^6 overshoots beta_0"],
    ["300 - beta_0",
     "0.68584073464102067615...",
     "How far 300 overshoots beta_0"],
    ["c fraction in [beta_0, 300]",
     "0.69739038596383...  (69.74%)",
     "c is ~70% of the way to 300"],
    ["beta=300 gives C=193.4",
     "g <= 9348 (M14)",
     "Integer beta -> trivial (C -> inf)"],
    ["beta=beta_0 gives C=11.422",
     "g <= 33 (M9/M10)",
     "Transcendental beta -> tight bound"],
]
cw3 = [1.8*inch, 2.2*inch, 2.5*inch]
gt = Table(gdata, colWidths=cw3)
gt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#2c4a2c")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f0f8f0"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(gt)

# The nines observation
story.append(Paragraph("The Nines Observation", sec_s))
story.append(Paragraph(
    "The error epsilon = (c/10^6)/beta_0 - 1 = 0.001597982... is close to "
    "1/625 = 0.001600... = 0.001599999... (infinite repeating 9s). "
    "The proximity is within 0.13% (2.0e-6 absolute).",
    body_s))
story.append(Spacer(1, 4))

ndata = [
    ["Expression", "Value", "Note"],
    ["epsilon", "0.0015979823200311...", "c/10^6 / beta_0 - 1"],
    ["1/625", "0.0016000000000000...", "= 0.001599999... (repeating)"],
    ["1/epsilon", "625.789151...", "nearest integer: 626"],
    ["625 = 5^4", "base-10 terminating", "1/5^n always terminates in decimal"],
    ["|epsilon - 1/625|", "2.018e-6", "absolute gap"],
    ["relative gap", "0.126%", "(epsilon - 1/625)/(1/625)"],
]
cw4 = [1.8*inch, 2.2*inch, 2.5*inch]
nt = Table(ndata, colWidths=cw4)
nt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#5e3a1a")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff8f0"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(nt)
story.append(Spacer(1, 3))
story.append(Paragraph(
    "Mathematical note: 1/625 = 0.0016 exactly (terminating decimal). "
    "Every terminating decimal d = 0.0016 also equals 0.001599999... "
    "by the standard identity x.y_1...y_n = x.y_1...(y_n - 1)999...",
    note_s))

# What the screenshots proposed (RH step) -- caveat
story.append(Paragraph("Note on the RH Certificate Proposal", sec_s))
story.append(Paragraph(
    "A separate conversation proposed using Delta_DS^(4) = 23.796910 in an RH "
    "lower bound: C(2) >= (-10.756045 + 23.796910) / 1.511 = 6.629. "
    "Module 15 (SHA cf1620c7...) has certified that Delta_DS^(4) = 2.753126, "
    "not 23.796910 -- a factor-8.6 error. The RH pathway using the wrong "
    "Delta is NOT certified here. The c-Bridge observation stands independently.",
    warn_s))

# Chain of custody
story.append(Paragraph("Chain of Custody", sec_s))
codata = [
    ["Item", "SHA-256"],
    ["m16_c_bridge.py (script)", SCRIPT_SHA[:52] + "..."],
    ["m16.out (stdout)",         STDOUT_SHA[:52] + "..."],
    ["Parent M1 (alpha_0)",      M1_SHA[:52] + "..."],
    ["Parent M4 (S_4, p_5)",     M4_SHA[:52] + "..."],
]
cot = Table(codata, colWidths=[2.2*inch, 4.3*inch])
cot.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#333333")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 6.8),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f8f8f8"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(cot)
story.append(Spacer(1, 5))

story.append(HRFlowable(width="100%", thickness=1,
             color=colors.HexColor("#1a1a6e"), spaceAfter=4))
story.append(Paragraph("Conclusion", sec_s))
story.append(Paragraph(
    "Certified: c/10^6 = 299.792458 and beta_0 = 299 + pi/10 = 299.31415... "
    "agree to within 1 part in 625.789. The ratio r - 1 = 0.001597982... is "
    "within 0.13% of 1/625 = 0.001599999... (repeating nines). "
    "c is 69.74% of the way from beta_0 to 300. Both are 'near-integer' "
    "perturbations of the transcendental beta_0. "
    "All values SHA-bound in m16.out. No physical interpretation is asserted.",
    body_s))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "CERTIFIED -- Battle Plan v1.6 -- David Fox -- May 2026", cert_s))

doc = SimpleDocTemplate(OUTPUT, pagesize=letter,
    leftMargin=0.65*inch, rightMargin=0.65*inch,
    topMargin=0.65*inch, bottomMargin=0.65*inch)
doc.build(story)

pdf_sha = hashlib.sha256(open(OUTPUT, "rb").read()).hexdigest()
print("PDF written: " + OUTPUT)
print("PDF SHA-256: " + pdf_sha)
