"""
Build Module_18_Resonance_Ladder.pdf
Battle Plan v1.6 | David Fox | May 2026
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
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

OUTPUT = "certificates/Module_18_Resonance_Ladder.pdf"
styles = getSampleStyleSheet()

def PS(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_s = PS("T",  fontSize=13, leading=16, alignment=TA_CENTER,
             spaceAfter=3, fontName="Helvetica-Bold")
sub_s   = PS("S",  fontSize=8.5, leading=11, alignment=TA_CENTER, spaceAfter=2)
sec_s   = PS("H",  fontSize=10, leading=13, spaceBefore=8, spaceAfter=3,
             fontName="Helvetica-Bold", textColor=colors.HexColor("#1a1a6e"))
body_s  = PS("B",  fontSize=8, leading=11, alignment=TA_JUSTIFY)
mono_s  = PS("M",  fontSize=7, leading=9.5, fontName="Courier", leftIndent=12)
ok_s    = PS("OK", fontSize=8, leading=10,
             textColor=colors.HexColor("#1a6e1a"), fontName="Helvetica-Bold")
warn_s  = PS("W",  fontSize=7.5, leading=10,
             textColor=colors.HexColor("#8B4500"))
note_s  = PS("N",  fontSize=7.5, leading=10, textColor=colors.HexColor("#444444"))
cert_s  = PS("C",  fontSize=9, alignment=TA_CENTER, fontName="Helvetica-Bold",
             textColor=colors.HexColor("#1a1a6e"))
err_s   = PS("E",  fontSize=8, leading=10,
             textColor=colors.HexColor("#8B0000"), fontName="Helvetica-Bold")

SCRIPT_SHA = sys.argv[1] if len(sys.argv) >= 3 else "(see m18.out)"
STDOUT_SHA = sys.argv[2] if len(sys.argv) >= 3 else "(see m18.out)"

M1_SHA  = _inv_sha("module_1", "sha256_stdout",     label="M1 stdout")
M5_SHA  = _inv_sha("module_5", "sha256_stdout",     label="M5 stdout")
M9_SHA  = _inv_sha("module_9_all", "sha256_stdout", label="M9-All stdout")

story = []

story.append(Paragraph("Module 18: Resonance Ladder Certificate", title_s))
story.append(Paragraph(
    "Sweep beta = 299 + k * pi/10 for k in [0.50, 3.50]  |  May 2026",
    sub_s))
story.append(Paragraph("Battle Plan v1.6  --  David Fox", sub_s))
story.append(HRFlowable(width="100%", thickness=1.5,
             color=colors.HexColor("#1a1a6e"), spaceAfter=5))

story.append(Paragraph(
    "For each k, compute S_beta = {p prime <= 100000 : ||p*beta|| < 1/p}, "
    "the BC sum C(beta) = sum log(p)*p/(p-1) for p in S_beta, "
    "and the RH genus bound g_max = ceil(C^2/4). "
    "Float64 sweep; key rows certified at 100 dps with mpmath 1.3.0. "
    "Cross-verified against M5 (SHA 9df98a39...) and M9 (SHA 5e39f3a9...).",
    body_s))
story.append(Spacer(1, 4))

# k_c annotation check
story.append(Paragraph("Annotation Correction: k_c and c/10^6", sec_s))
story.append(Paragraph(
    "An external conversation annotated k=2.67 as 'beta ~ c/10^6'. "
    "This is incorrect. The certified value is:",
    body_s))
story.append(Spacer(1, 2))
kcdata = [
    ["Quantity", "Value", "Note"],
    ["c / 10^6", "299.792458", "exact, SI definition"],
    ["beta_0 = 299 + pi/10", "299.314159...", "k=1.00"],
    ["k_c = (c/10^6 - 299)/(pi/10)", "2.522472...", "mpmath certified"],
    ["k=2.67 gives beta", "299.838805", "0.046 above c/10^6 = DIFFERENT"],
    ["k=2.67 annotation", "WRONG", "k_c = 2.52, not 2.67"],
]
cw = [2.0*inch, 1.7*inch, 2.8*inch]
kct = Table(kcdata, colWidths=cw)
kct.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#555555")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-2), "Courier"),
    ("BACKGROUND",   (0,-1),(-1,-1), colors.HexColor("#fff0f0")),
    ("FONTNAME",     (0,-1),(-1,-1), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0), (-1,-1), 7.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-2),[colors.HexColor("#f8f8f8"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(kct)

# Main sweep table (selected rows)
story.append(Paragraph("Certified Key Rows (mpmath 100 dps)", sec_s))
story.append(Paragraph(
    "Full sweep: primes <=100000; BC sum C(beta) = sum log(p)*p/(p-1); "
    "g_max = ceil(C^2/4) from BC bound [consistent with M9 g=33 at k=1.00].",
    body_s))
story.append(Spacer(1, 3))

mdata = [
    ["k", "beta", "|S_beta|", "C(beta)", "g_max", "Note"],
    ["1.00", "299.314159", "4",  "11.42214869",  "33", "beta_0 [M5/M9 CERTIFIED]"],
    ["1.25", "299.392699", "4",  " 8.324027",    "18", "local low"],
    ["2.00", "299.628319", "6",  "16.30404412",  "67", "matches ext. screenshot"],
    ["2.52", "299.791681", "6",  "33.59099989", "283", "k_c: beta~c/10^6 CORRECT"],
    ["2.67", "299.838805", "6",  "28.32425777", "201", "ext. screenshot: wrong (see below)"],
    ["2.72", "299.854513", "2",  " 3.656523",     "4", "local minimum (2 primes)"],
    ["3.00", "299.942478", "4",  "11.01473296",  "31", "matches ext. screenshot"],
    ["3.13", "299.983319", "5",  "11.464079",    "33", "local match"],
    ["3.18", "299.999026","14",  "58.25508311", "849", "explosion (ext: 11/29.17/372)"],
    ["3.50", "300.099557", "2",  " 3.034213",     "3", "beyond 300"],
]
cw2 = [0.4*inch, 1.0*inch, 0.65*inch, 1.2*inch, 0.65*inch, 2.6*inch]
mt = Table(mdata, colWidths=cw2)
mt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1a1a6e")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 6.8),
    ("BACKGROUND",   (0,1), (-1,1), colors.HexColor("#d4edda")),
    ("BACKGROUND",   (0,4), (-1,4), colors.HexColor("#e8e8ff")),
    ("BACKGROUND",   (0,9), (-1,9), colors.HexColor("#fff0f0")),
    ("ROWBACKGROUNDS",(0,2),(-1,-2),[colors.HexColor("#f8f8ff"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.3, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(mt)
story.append(Spacer(1, 3))
story.append(Paragraph(
    "Green row = M5/M9 cross-check PASS. Blue row = certified k_c. "
    "Red row = explosion at k=3.18.",
    note_s))

# Discrepancy explanation
story.append(Paragraph("Discrepancy with External Screenshot Values", sec_s))
story.append(Paragraph(
    "An external AI chat reported different values at k=2.67 and k=3.18. "
    "This is explained by the prime bound used:",
    body_s))
story.append(Spacer(1, 3))

disc = [
    ["k", "Quantity", "External AI", "Our Certified", "Explanation"],
    ["2.67", "|S_beta|",  "4",    "6",   "Ext. AI: primes ~<=191 only"],
    ["2.67", "C(beta)",   "9.217","28.32","Ext. S={2,5,7,31}; we find 2 more primes"],
    ["2.67", "g_max",   "37.2",  "201",  "g ~ C^2/4; higher C => higher g"],
    ["3.18", "|S_beta|",  "11",   "14",  "3 extra primes from full search"],
    ["3.18", "C(beta)",  "29.165","58.26","Large primes have big C_p contribution"],
    ["3.18", "g_max",   "372.4", "849",  "Consistent with corrected C"],
    ["k_c",  "k value",  "2.67", "2.52", "c/10^6=299.792458 => k=(0.792458)/(pi/10)"],
]
cw3 = [0.35*inch, 0.7*inch, 0.9*inch, 0.9*inch, 3.65*inch]
dt2 = Table(disc, colWidths=cw3)
dt2.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#8B0000")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff5f5"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.3, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(dt2)
story.append(Spacer(1, 3))
story.append(Paragraph(
    "Note: At k=2.67, C_ext = 9.217 matches exactly C_2+C_5+C_7+C_31 = "
    "1.386+2.012+2.270+3.547 = 9.215 (round-off matches 9.217). "
    "The external AI's S_beta at k=2.67 = {2,5,7,31}, missing primes > 191. "
    "The VALUES AT k=2.00 AND k=3.00 AGREE, confirming shared methodology "
    "for primes covered by both searches.",
    note_s))

# What the ladder reveals
story.append(Paragraph("What the Ladder Reveals (Certified)", sec_s))

rev = [
    ["Finding", "Description", "Certified"],
    ["1. k=1.00 exact match",
     "C=11.422, g_max=33, S={2,3,19,191}",
     "M5 SHA 9df98a39, M9 SHA 5e39f3a9"],
    ["2. Explosion near beta=300",
     "At k=3.18: |S|=14, C=58.26, g_max=849",
     "mpmath certified, m18.out"],
    ["3. k_c correct value",
     "c/10^6 at k=2.5225, not k=2.67",
     "mpmath: (299.792458-299)/(pi/10)"],
    ["4. |S| fluctuates sharply",
     "Jumps between 2 and 14 in [k=0.5, 3.5]",
     "float64 sweep, mpmath spot-checks"],
    ["5. Near-300 regime",
     "k in [3.0, 3.2] shows explosive growth as beta->300",
     "zoom table, m18.out"],
]
cw4 = [1.3*inch, 2.5*inch, 2.7*inch]
rt = Table(rev, colWidths=cw4)
rt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1a4a1a")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f0f8f0"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(rt)

# Chain of custody
story.append(Paragraph("Chain of Custody", sec_s))
codata = [
    ["Item", "SHA-256"],
    ["m18_resonance_ladder.py (script)", SCRIPT_SHA[:52] + "..."],
    ["m18.out (stdout)",                 STDOUT_SHA[:52] + "..."],
    ["Parent M1 (alpha_0 = 299+pi/10)",  M1_SHA[:52] + "..."],
    ["Parent M5 (C(S4) BC certified)",   M5_SHA[:52] + "..."],
    ["Parent M9 (g<=33 certified)",      M9_SHA[:52] + "..."],
]
cot = Table(codata, colWidths=[2.5*inch, 4.0*inch])
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

story.append(HRFlowable(width="100%", thickness=1.5,
             color=colors.HexColor("#1a1a6e"), spaceAfter=4))
story.append(Paragraph("Conclusion", sec_s))
story.append(Paragraph(
    "The resonance ladder sweep from k=0.50 to 3.50 (step 0.05, primes <=100000) "
    "confirms: (1) k=1.00 (beta_0) gives C=11.422, g_max=33 exactly matching M5/M9. "
    "(2) The explosion near k=3.18 (beta->300) is real: |S|=14, C=58.26, g_max=849. "
    "(3) k_c for c/10^6 = 2.5225 (not 2.67 as annotated in external chat). "
    "(4) External values at k=2.67 and k=3.18 differ from ours because the external "
    "computation used primes <= ~191 only; our search uses primes <= 100000. "
    "External values at k=2.00 and k=3.00 agree with ours, confirming the methodology "
    "is the same for small primes. All certified values SHA-bound in m18.out.",
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
