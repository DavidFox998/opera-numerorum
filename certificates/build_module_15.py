"""
Build Module_15_Delta_Boost.pdf -- Audit Certificate
LaTeX paper section: "The Exceptional Prime Set for pi/10"
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

OUTPUT = "certificates/Module_15_Delta_Boost.pdf"

styles = getSampleStyleSheet()
def PS(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_s   = PS("T",  fontSize=13, leading=16, alignment=TA_CENTER,
               spaceAfter=3, fontName="Helvetica-Bold")
sub_s     = PS("S",  fontSize=8.5, leading=11, alignment=TA_CENTER, spaceAfter=2)
sec_s     = PS("H",  fontSize=10, leading=13, spaceBefore=8, spaceAfter=3,
               fontName="Helvetica-Bold", textColor=colors.HexColor("#4a1a6e"))
body_s    = PS("B",  fontSize=8, leading=11, alignment=TA_JUSTIFY)
mono_s    = PS("M",  fontSize=7, leading=9.5, fontName="Courier", leftIndent=12)
small_s   = PS("Sm", fontSize=7.5, leading=10)
ok_s      = PS("OK", fontSize=8, leading=10,
               textColor=colors.HexColor("#1a6e1a"), fontName="Helvetica-Bold")
err_s     = PS("ER", fontSize=8, leading=10,
               textColor=colors.HexColor("#8B0000"), fontName="Helvetica-Bold")
cert_s    = PS("C",  fontSize=9, alignment=TA_CENTER, fontName="Helvetica-Bold",
               textColor=colors.HexColor("#1a1a6e"))
warn_s    = PS("W",  fontSize=7.5, leading=10,
               textColor=colors.HexColor("#8B0000"))

SCRIPT_SHA = sys.argv[1] if len(sys.argv) >= 3 else "(see m15.out)"
STDOUT_SHA = sys.argv[2] if len(sys.argv) >= 3 else "(see m15.out)"

M3_SHA = "e687bb0931f2c37c6ae12cfbde7ff9a79b3cccf5b0c88e17e9c3fe4abe1cf80d"
M4_SHA = "b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed"

story = []

story.append(Paragraph("Module 15: Delta Boost Audit Certificate", title_s))
story.append(Paragraph(
    "Paper Section: 'The Exceptional Prime Set for pi/10'  |  Audit Date: May 2026",
    sub_s))
story.append(Paragraph("Battle Plan v1.6  --  David Fox", sub_s))
story.append(HRFlowable(width="100%", thickness=1,
             color=colors.HexColor("#8B0000"), spaceAfter=5))

story.append(Paragraph(
    "This certificate audits all numerical claims in the attached LaTeX paper section. "
    "Four independent errors were found. One claim (S_4 membership) is correct. "
    "All correct values are computed here at 100 dps and SHA-bound.",
    body_s))
story.append(Spacer(1, 4))

# Audit summary table
story.append(Paragraph("Audit Summary", sec_s))
sumdata = [
    ["Claim", "Paper States", "TRUE Value", "Verdict"],
    ["C1: Table ||p*pi/10||",  "16 entries (all wrong)", "See Section 2", "4 ERRORS*"],
    ["C2: delta_p > 0 (Lemma)", "Holds for p in S_4",   "CONFIRMED",     "PASS"],
    ["C3: Individual delta_p",  "E.g. delta_191=11.719", "delta_191=0.169", "WRONG (E1+E2)"],
    ["C4: Delta_DS^(4)=23.797", "23.796910 +- 1e-6",    "2.753126...",   "WRONG (E1+E2)"],
    ["C5: p_5 > 6*10^12",       "min(S\\S_4) > 6e12",   "p_5=3.994e12",  "WRONG (E4)"],
    ["C6: S_4={2,3,19,191}",   "{2,3,19,191}",          "{2,3,19,191}",  "CORRECT"],
]
cw = [1.6*inch, 1.65*inch, 1.65*inch, 1.6*inch]
st = Table(sumdata, colWidths=cw)
st.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#4a1a6e")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0), (-1,-1), 7.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff0f0"), colors.white]),
    ("BACKGROUND",   (0,6), (-1,6), colors.HexColor("#e8f5e9")),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2),
    ("BOTTOMPADDING",(0,0), (-1,-1), 2),
]))
story.append(st)
story.append(Spacer(1, 3))
story.append(Paragraph(
    "* C1 has 16 wrong values; C3 and C4 each carry two compounding errors (E1+E2).",
    small_s))

# Error description
story.append(Paragraph("Error Descriptions", sec_s))
edata = [
    ["ID", "Location", "Description"],
    ["E1", "Table (Thm 2)",
     "All 16 ||p*pi/10|| values are wrong. Errors from 1.79e-5 (p=2) to 3.76e-1 (p=43). "
     "The SHA 'a7f3d1b9e5c2...' is truncated and unverifiable. ARB result not reproduced."],
    ["E2", "Thm 4 proof",
     "Sign error in delta_p computation. DEFINITION: delta_p = -log(||.||) - log(p). "
     "PAPER COMPUTES: delta_p = -log(||.||) + log(p)  [adds log(p) instead of subtracting]. "
     "Example: paper shows '0.989644 + 0.693147 = 1.682791' for p=2, but definition "
     "requires subtraction: 0.989718 - 0.693147 = 0.296571."],
    ["E3", "Thm 4",
     "Delta_DS^(4) = 23.796910 follows from E1 + E2 compounding. "
     "Correct value: 2.753126...  (off by factor ~8.6)."],
    ["E4", "Rem 2 (S14)",
     "p_5 > 6*10^12 is wrong. Certified p_5 = 3,993,746,143,633 = 3.994*10^12 < 6*10^12. "
     "M4 proves p_5 > 10^10 (completeness bound); the exact p_5 is known and < 6*10^12."],
]
ew = [0.3*inch, 1.1*inch, 5.1*inch]
et = Table(edata, colWidths=ew)
et.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#8B0000")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff5f5"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ("TOPPADDING",   (0,0), (-1,-1), 2),
    ("BOTTOMPADDING",(0,0), (-1,-1), 2),
]))
story.append(et)

# Corrected table ||p*pi/10||
story.append(Paragraph("Section 2: Corrected Table of ||p*pi/10|| Values", sec_s))
story.append(Paragraph(
    "Computed at 100 dps via mpmath 1.3.0. Natural log throughout. "
    "Formula: ||p*pi/10|| = min(frac(p*pi/10), 1 - frac(p*pi/10)).",
    body_s))
story.append(Spacer(1, 3))

paper_table = {
     2: 0.37166359,   3: 0.05759539,   5: 0.42925878,   7: 0.20092865,
    11: 0.45610154,  13: 0.08443515,  17: 0.34110602,  19: 0.03027262,
    23: 0.28694349,  29: 0.45839086,  31: 0.08672446,  37: 0.25817184,
    41: 0.48650271,  43: 0.11483631, 191: 0.00155435, 197: 0.11343472,
}

from mpmath import mp, mpf, pi, log, fabs, floor, nstr
mp.dps = 100
alpha = pi / 10
def ni(v): return fabs(v - floor(v + mpf("0.5")))

tdata = [["p", "Paper (wrong)", "TRUE ||p*pi/10||", "Err", "1/p", "Hit?", "Note"]]
for p in sorted(paper_table.keys()):
    pv = paper_table[p]
    tv = float(ni(mpf(p) * alpha))
    err = abs(pv - tv)
    hit = "YES" if tv < 1.0/p else "no"
    note = "S_4" if p in [2,3,19,191] else ""
    tdata.append([str(p), f"{pv:.8f}", f"{tv:.10f}", f"{err:.1e}",
                  f"{1.0/p:.8f}", hit, note])
tw = [0.4*inch, 0.9*inch, 1.25*inch, 0.65*inch, 0.9*inch, 0.45*inch, 0.45*inch]
tt = Table(tdata, colWidths=tw)
tt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#333355")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 6.5),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f8f8ff"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.3, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 1.5), ("BOTTOMPADDING",(0,0),(-1,-1),1.5),
]))
story.append(tt)
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Qualitative conclusion (which primes are in S_4) is CORRECT in the paper "
    "despite all 16 ||.|| values being wrong.",
    ok_s))

# Corrected delta_p values
story.append(Paragraph("Section 3: Corrected delta_p Values and Sum", sec_s))
story.append(Paragraph(
    "Definition (from paper): delta_p = -log(||p*pi/10||) - log(p)  [natural log]. "
    "Correct computation uses TRUE ||p*pi/10|| values and the correct minus sign.",
    body_s))
story.append(Spacer(1, 3))

S4 = [2, 3, 19, 191]
true_deltas = {}
for p in S4:
    v = ni(mpf(p) * alpha)
    true_deltas[p] = -log(v) - log(mpf(p))
true_sum = sum(true_deltas[p] for p in S4)

paper_delta = {2: 1.682791, 3: 3.953040, 19: 6.442201, 191: 11.718878}

ddata = [["p", "Paper delta_p", "TRUE ||p*pi/10||",
          "TRUE -log(||.||)", "TRUE log(p)", "TRUE delta_p", "Status"]]
for p in S4:
    v = ni(mpf(p) * alpha)
    vf = float(v)
    nlv = float(-log(v))
    lp  = float(log(mpf(p)))
    td  = float(true_deltas[p])
    ddata.append([str(p), f"{paper_delta[p]:.6f}", f"{vf:.10f}",
                  f"{nlv:.6f}", f"{lp:.6f}", f"{td:.8f}", "CORRECT"])
ddata.append(["SUM", "23.796910", "--", "--", "--",
              f"{float(true_sum):.8f}", "CORRECT"])
cw2 = [0.35*inch, 0.85*inch, 1.2*inch, 1.0*inch, 0.85*inch, 1.0*inch, 0.75*inch]
dt = Table(ddata, colWidths=cw2)
dt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#2c5f2e")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-2), "Courier"),
    ("FONTNAME",     (0,-1),(-1,-1), "Helvetica-Bold"),
    ("BACKGROUND",   (0,-1),(-1,-1), colors.HexColor("#e8f5e9")),
    ("FONTSIZE",     (0,0), (-1,-1), 6.8),
    ("ROWBACKGROUNDS",(0,1),(-1,-2),[colors.HexColor("#f0f8f0"), colors.white]),
    ("GRID",         (0,0), (-1,-1), 0.3, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(dt)
story.append(Spacer(1, 3))

story.append(Paragraph(
    "TRUE Delta_DS^(4) = " + nstr(true_sum, 20) +
    "  vs paper claim 23.796910  (off by " +
    f"{float(fabs(true_sum - mpf('23.796910'))):.4f}" + ", factor ~8.6x)",
    warn_s))

# p_5 section
story.append(Paragraph("Section 4: p_5 Bound", sec_s))
p5data = [
    ["Item", "Paper Claims", "Certified Value", "Source", "Verdict"],
    ["p_5 lower bound", "> 6 * 10^12",
     "p_5 = 3,993,746,143,633 = 3.994*10^12",
     "M4 SHA b810a7a3...", "WRONG"],
    ["S_4 completeness", "cap [2, 10^10]",
     "p_4 = 191 < 10^4; p_5 > 10^10",
     "M3 SHA e687bb09...", "CORRECT"],
]
cw3 = [1.2*inch, 1.1*inch, 2.1*inch, 1.25*inch, 0.7*inch]
p5t = Table(p5data, colWidths=cw3)
p5t.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#555555")),
    ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
    ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1), (-1,-1), "Courier"),
    ("FONTSIZE",     (0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fff0f0"), colors.HexColor("#f0fff0")]),
    ("GRID",         (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0), (-1,-1), 2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
]))
story.append(p5t)

# Chain of custody
story.append(Paragraph("Chain of Custody", sec_s))
codata = [
    ["Item", "SHA-256"],
    ["m15_delta_boost.py (script)", SCRIPT_SHA[:48] + "..."],
    ["m15.out (stdout)",            STDOUT_SHA[:48] + "..."],
    ["Parent M3 (CF pi/10)",        M3_SHA[:48] + "..."],
    ["Parent M4 (S_14, p_5)",       M4_SHA[:48] + "..."],
]
cot = Table(codata, colWidths=[2.0*inch, 4.5*inch])
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
story.append(codata and cot)
story.append(Spacer(1, 5))

story.append(HRFlowable(width="100%", thickness=1,
             color=colors.HexColor("#4a1a6e"), spaceAfter=4))
story.append(Paragraph("Conclusion", sec_s))
story.append(Paragraph(
    "The paper section contains 4 independent numerical errors: wrong table values (E1), "
    "a sign error in delta_p (E2), a wrong Delta_DS^(4) sum (E3), and a wrong p_5 bound (E4). "
    "The only fully correct claim is S_4 = {2,3,19,191}. "
    "Corrected certified values: delta_2=0.29657, delta_3=1.75697, delta_19=0.53017, "
    "delta_191=0.16941; Delta_DS^(4)=2.75313; p_5=3993746143633. "
    "All values computed at 100 dps and SHA-bound in m15.out.",
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
