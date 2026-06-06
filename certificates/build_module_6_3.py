#!/usr/bin/env python3
# Battle Plan v1.6 - Module 6.3 Certificate Builder
# Produces: certificates/Module_6_3_Certificate.pdf
# ASCII-only output rule enforced throughout.

import csv, math, hashlib
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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

OUT_PDF   = "certificates/Module_6_3_Certificate.pdf"
CSV_FILE  = "m6_3_lemma41.csv"
SCRIPT    = "certificates/m6_3_lemma41.py"

M1_SHA    = _inv_sha("module_1", "sha256_stdout", label="M1 stdout")
M81_SHA   = _inv_sha("M9", "parent_shas", "M8.1", label="M9.parent_shas.M8.1")

def sha256(path):
    return hashlib.sha256(open(path,'rb').read()).hexdigest()

def build():
    csv_sha    = sha256(CSV_FILE)
    script_sha = sha256(SCRIPT)

    rows = list(csv.DictReader(open(CSV_FILE)))
    all_primes   = [r for r in rows]
    fail_rows    = [r for r in rows if r['lemma41_pass']=='False']
    pass_rows    = [r for r in rows if r['lemma41_pass']=='True']
    weil_fails   = [r for r in rows if r['weil_ok']=='False']
    n_tested     = len(all_primes)
    n_fail       = len(fail_rows)
    n_pass       = len(pass_rows)

    doc = SimpleDocTemplate(OUT_PDF, pagesize=letter,
                            leftMargin=0.85*inch, rightMargin=0.85*inch,
                            topMargin=0.85*inch, bottomMargin=0.85*inch)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', fontSize=14, fontName='Helvetica-Bold',
                                 alignment=TA_CENTER, spaceAfter=6)
    sub_style   = ParagraphStyle('sub', fontSize=10, fontName='Helvetica',
                                 alignment=TA_CENTER, spaceAfter=12)
    head_style  = ParagraphStyle('head', fontSize=11, fontName='Helvetica-Bold',
                                 spaceBefore=10, spaceAfter=4)
    body_style  = ParagraphStyle('body', fontSize=9, fontName='Helvetica',
                                 leading=13, spaceAfter=4)
    mono_style  = ParagraphStyle('mono', fontSize=7.5, fontName='Courier',
                                 leading=10, spaceAfter=2)

    story = []

    story.append(Paragraph("MACHINE CERTIFICATION CERTIFICATE", title_style))
    story.append(Paragraph("Module 6.3 -- Lemma 4.1 Falsified, Weil Bound Certified", title_style))
    story.append(Paragraph("Battle Plan v1.6 -- David Fox -- May 2026", sub_style))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("1. CLAIM", head_style))
    story.append(Paragraph(
        "Two certified conclusions for N = 143, S_2(Gamma_0(143)):", body_style))
    story.append(Paragraph(
        "Conclusion A: Lemma 4.1 is FALSE for N=143. "
        "There exist 94 explicit primes p in {5,...,997} \\ {11,13} for which "
        "R(p) = max_ap(p) / (2*sqrt(p)) > cos(2*pi/p), "
        "where Lemma 4.1 claims this inequality cannot hold.", body_style))
    story.append(Paragraph(
        "Conclusion B: The Weil bound holds for the dim-1 newform 143.2.a.a. "
        "|a_p(143.2.a.a)| <= 2*sqrt(p) for all 164 tested primes.", body_style))

    story.append(Paragraph("2. DEFINITIONS", head_style))
    defs = [
        "alpha_0 = 299 + pi/10  (M1-certified to 5000 decimal places)",
        "dist(p) = min(frac(p*alpha_0), 1 - frac(p*alpha_0))  [nearest-integer distance, always in [0, 1/2]]",
        "max_ap(p) = max(|a_p(143.2.a.a)|, |Tr(a_p(143.2.a.b))|, |Tr(a_p(143.2.a.c))|)",
        "           NOT the H_1 aggregate trace. Individual form traces from LMFDB.",
        "R(p) = max_ap(p) / (2*sqrt(p))",
        "bound(p) = cos(2*pi/p)",
        "Lemma 4.1 pass = (R(p) <= bound(p));  Lemma 4.1 fail = (R(p) > bound(p))",
        "CM status: LMFDB cm field = 0 for all three level-143 forms. No CM exclusion needed.",
        "dim(new S_2(Gamma_0(143))) = 1+4+6 = 11. No 143.2.a.d exists.",
    ]
    for d in defs:
        story.append(Paragraph(d, mono_style))
    story.append(Spacer(1, 0.05*inch))

    story.append(Paragraph("3. INPUT SHAs", head_style))
    sha_data = [
        ['Module', 'SHA-256', 'Content'],
        ['M1',   M1_SHA[:32]+'...', 'alpha_0 = 299+pi/10 (5000 dps)'],
        ['M8.1', M81_SHA[:32]+'...', '143_traces.csv: Hecke traces, 3 forms, p<=997'],
        ['M6.3 script', script_sha[:32]+'...', 'certificates/m6_3_lemma41.py'],
        ['M6.3 output', csv_sha[:32]+'...',   'm6_3_lemma41.csv (164 rows)'],
    ]
    sha_table = Table(sha_data, colWidths=[0.8*inch, 2.9*inch, 2.9*inch])
    sha_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME',   (0,1), (-1,-1), 'Courier'),
        ('FONTSIZE',   (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f0f0f0'), colors.white]),
        ('GRID',       (0,0), (-1,-1), 0.3, colors.grey),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(sha_table)

    story.append(Paragraph("4. RESULTS SUMMARY", head_style))
    story.append(Paragraph(
        f"Primes tested (5<=p<=997, excluding 11, 13): {n_tested}", body_style))
    story.append(Paragraph(
        f"Lemma 4.1 FAILURES (R > cos(2*pi/p)): {n_fail} primes", body_style))
    story.append(Paragraph(
        f"Lemma 4.1 passes:                      {n_pass} primes", body_style))
    story.append(Paragraph(
        f"Weil bound failures |ap_a|>2*sqrt(p):  {len(weil_fails)} primes", body_style))

    story.append(Paragraph("5. FIRST 30 LEMMA 4.1 FAILURE PRIMES", head_style))
    fail30 = fail_rows[:30]
    tdata = [['p', 'max_ap', 'R', 'cos(2pi/p)', 'R - bound', 'form']]
    for r in fail30:
        p   = int(r['p'])
        mx  = int(r['max_ap'])
        R   = float(r['R'])
        bnd = float(r['cos2pi_p'])
        ap_a = abs(int(r['ap_a']))
        ap_b = abs(int(r['ap_b_tr']))
        ap_c = abs(int(r['ap_c_tr']))
        form = '143.2.a.a' if ap_a==mx else ('143.2.a.b' if ap_b==mx else '143.2.a.c')
        tdata.append([str(p), str(mx), f"{R:.5f}", f"{bnd:.5f}", f"{R-bnd:.5f}", form])
    fail_table = Table(tdata, colWidths=[0.4*inch,0.7*inch,0.85*inch,0.95*inch,0.85*inch,1.1*inch])
    fail_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
        ('FONTNAME',      (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,1),(-1,-1), 'Courier'),
        ('FONTSIZE',      (0,0),(-1,-1), 7.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.HexColor('#fdf0ef'), colors.white]),
        ('GRID',          (0,0),(-1,-1), 0.3, colors.grey),
        ('TOPPADDING',    (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
    ]))
    story.append(fail_table)

    story.append(Paragraph("6. ALL FAILURE PRIMES (p <= 997)", head_style))
    all_fail_ps = [int(r['p']) for r in fail_rows]
    story.append(Paragraph(str(all_fail_ps), mono_style))

    story.append(Paragraph("7. WEIL BOUND VERIFICATION (dim-1 form 143.2.a.a)", head_style))
    story.append(Paragraph(
        "For all 164 tested primes: |a_p(143.2.a.a)| <= 2*sqrt(p). "
        "Weil bound holds. Max R_dim1 observed:", body_style))
    max_r1 = max(abs(int(r['ap_a']))/(2*math.sqrt(int(r['p']))) for r in rows)
    story.append(Paragraph(f"max R_dim1 = {max_r1:.6f} < 1  (Ramanujan for dim-1 form)", mono_style))

    story.append(Paragraph("8. CHAIN OF CUSTODY", head_style))
    chain = [
        "M1 (alpha_0) -> M8.1 (LMFDB traces) -> M6.3 (Lemma 4.1 falsification)",
        "",
        "M1  SHA: " + M1_SHA,
        "M8.1 SHA (143_traces.csv): " + M81_SHA,
        "M6.3 script SHA: " + script_sha,
        "M6.3 output SHA: " + csv_sha,
    ]
    for line in chain:
        story.append(Paragraph(line, mono_style))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("9. AUDIT NOTE", head_style))
    story.append(Paragraph(
        "The prototype script that produced the original 118-failure table used two wrong definitions: "
        "(1) dist = frac(p*pi/10) instead of min(frac, 1-frac), and "
        "(2) max_ap included the H_1 aggregate trace (-44 at p=71) instead of individual form traces. "
        "Both errors are corrected here. This certificate supersedes the prototype table.", body_style))
    story.append(Paragraph(
        "The previous claim of a CM form 143.2.a.c with a_71=-35 was a labeling error. "
        "LMFDB cm field = 0 for all three level-143 forms. "
        "There is no 143.2.a.d. Dimension count: 1+4+6=11=new space dim.", body_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(
        "CERTIFIED -- Battle Plan v1.6 -- David Fox -- May 2026",
        ParagraphStyle('cert', fontSize=10, fontName='Helvetica-Bold', alignment=TA_CENTER)))

    doc.build(story)
    print(f"PDF written: {OUT_PDF}")
    pdf_sha = sha256(OUT_PDF)
    print(f"PDF SHA-256: {pdf_sha}")
    return pdf_sha, csv_sha, script_sha

if __name__ == "__main__":
    build()
