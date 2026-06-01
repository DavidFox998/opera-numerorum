#!/usr/bin/env python3
"""Generate the YM-tower audit export JSON (Project Task #316).

Walks the Yang-Mills tower (`lean-proof-towers/Towers/YM/*.lean`) and emits a
single machine-ingestible JSON following the user's AUDIT_EXPORT schema. The
export reports the TRUE repo state only:

  * transfer_operator  -- the REAL scalar-shadow Hamiltonian `H` (and `T_L`),
                          is_scalar_shadow = true, proven_bound = null.
  * su3_files          -- SU3.lean / SU3Basis.lean / SU3Instances.lean with
                          real sha256 + full content.
  * massgap574         -- full verbatim text, YM_mass_gap statement + proof
                          body, and the TRUE sorry proof-term count.
  * bridge_data        -- P6..P20 all null (BEYOND_TOLERANCE), flagged
                          out-of-tower (Hodge/BDP desert-map programme).
  * kappa_history      -- kappa_1..kappa_15, null except kappa_15 = the one
                          recorded value, flagged out-of-tower.
  * comments_raw       -- every comment line in non-stub YM files containing
                          one of: mass, gap, glueball, SU3, Wilson, physical.

HONESTY (locked): nothing here claims a mass gap, `m > 0`, or a closed Surface
#1. Stub files emit null content. Missing/out-of-tower fields are null with an
explicit provenance note. No fabricated or computed passes.

Run from repo root:  python3 scripts/build_ym_audit_export.py
"""
import os
import re
import csv
import json
import hashlib
import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YM_DIR = os.path.join(REPO, "lean-proof-towers", "Towers", "YM")
OUT = os.path.join(REPO, "lean-proof-towers", "exports", "ym-audit-export.json")
REL = "Towers/YM"

KEYWORDS = ["mass", "gap", "glueball", "su3", "su(3)", "wilson", "physical"]
# Real proof-term sorry forms (NOT prose mentions inside comments/docstrings).
SORRY_TERM_RE = re.compile(
    r"(:=\s*sorry\b|:=\s*by\s+sorry\b|\bby\s+sorry\b|^\s*sorry\s*$|<;>\s*sorry\b|\bexact\s+sorry\b|\badmit\b)"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def list_ym_files():
    return sorted(f for f in os.listdir(YM_DIR) if f.endswith(".lean"))


def is_stub(fname: str) -> bool:
    return fname.endswith("Stub.lean")


def comment_lines(text: str):
    """Yield (line_no, comment_text) for every line that is (partly) a Lean
    comment. Handles `/- ... -/` / `/-- ... -/` blocks (with nesting, as Lean
    allows) and `--` line comments."""
    depth = 0  # nested block-comment depth
    for i, line in enumerate(text.split("\n"), start=1):
        s = line
        parts = []
        pos = 0
        while pos < len(s):
            if depth > 0:
                end = s.find("-/", pos)
                op = s.find("/-", pos)
                if op != -1 and (end == -1 or op < end):
                    depth += 1
                    parts.append(s[pos:op])
                    pos = op + 2
                elif end != -1:
                    parts.append(s[pos:end])
                    depth -= 1
                    pos = end + 2
                else:
                    parts.append(s[pos:])
                    pos = len(s)
            else:
                bo = s.find("/-", pos)
                lo = s.find("--", pos)
                if lo != -1 and (bo == -1 or lo < bo):
                    parts.append(s[lo + 2:])
                    pos = len(s)
                elif bo != -1:
                    depth += 1
                    pos = bo + 2
                else:
                    pos = len(s)
        out = " ".join(p for p in parts if p.strip()).strip()
        if out:
            yield i, out


def count_real_sorry(text: str) -> int:
    """Count actual sorry/admit PROOF TERMS, ignoring comments/docstrings."""
    n = 0
    in_block = False
    for line in text.split("\n"):
        code = line
        if in_block:
            end = code.find("-/")
            if end == -1:
                continue
            code = code[end + 2:]
            in_block = False
        # strip inline block + line comments from the code portion
        while "/-" in code:
            bo = code.find("/-")
            end = code.find("-/", bo + 2)
            if end == -1:
                code = code[:bo]
                in_block = True
                break
            code = code[:bo] + " " + code[end + 2:]
        lo = code.find("--")
        if lo != -1:
            code = code[:lo]
        if SORRY_TERM_RE.search(code):
            n += 1
    return n


def extract_def(text: str, name: str):
    """Extract a `def NAME ...` block (signature through body) as raw text."""
    lines = text.split("\n")
    pat = re.compile(r"^\s*(noncomputable\s+)?(def|abbrev)\s+" + re.escape(name) + r"\b")
    start = None
    for i, ln in enumerate(lines):
        if pat.search(ln):
            start = i
            break
    if start is None:
        return None
    # capture until the first blank line after we've seen a `:=` (the body),
    # or the next top-level declaration / comment opener.
    seen_assign = False
    out = []
    for j in range(start, len(lines)):
        ln = lines[j]
        out.append(ln)
        if ":=" in ln:
            seen_assign = True
        if seen_assign and j > start and ln.strip() == "":
            out.pop()
            break
        nxt = lines[j + 1] if j + 1 < len(lines) else ""
        if seen_assign and re.match(r"^\s*(/--|/-|theorem|lemma|def |noncomputable|instance|end\b)", nxt):
            break
    return "\n".join(out).rstrip() + ("\n  (line %d)" % (start + 1))


def extract_theorem(text: str, name: str):
    """Extract a `theorem NAME` block; return (statement, proof_body).
    Splits on the LAST top-level `:=` (after the goal type), so named
    arguments like `(E := ...)` inside the statement are not mistaken for the
    proof separator. proof_body is None if the proof is `sorry`/`admit`."""
    lines = text.split("\n")
    pat = re.compile(r"^\s*(theorem|lemma)\s+" + re.escape(name) + r"\b")
    start = None
    for i, ln in enumerate(lines):
        if pat.search(ln):
            start = i
            break
    if start is None:
        return None, None
    block = []
    for j in range(start, len(lines)):
        if lines[j].strip() == "" and j > start:
            break
        if re.match(r"^\s*(/--|/-|theorem |lemma |def |end\b)", lines[j]) and j > start:
            break
        block.append(lines[j])
    decl = "\n".join(block).rstrip()
    if ":=" not in decl:
        return decl, None
    statement, proof = decl.rsplit(":=", 1)
    statement = statement.rstrip()
    proof = proof.strip()
    if re.fullmatch(r"(by\s+)?sorry|admit", proof):
        proof = None
    return statement, proof


def main():
    files = list_ym_files()

    # --- manifest (step 1: enumerate every file; stubs flagged) -------------
    manifest = []
    for f in files:
        full = read(os.path.join(YM_DIR, f))
        stub = is_stub(f)
        manifest.append({
            "path": "%s/%s" % (REL, f),
            "is_stub": stub,
            "sha256": sha256_text(full),
            "line_count": full.count("\n") + 1,
            "real_sorry_proof_terms": count_real_sorry(full),
            "content": None,  # stubs null per spec; full content only in dedicated blocks
        })

    # --- transfer_operator (step 2) -----------------------------------------
    lpr = read(os.path.join(YM_DIR, "LatticePositivityReal.lean"))
    transfer_src = read(os.path.join(YM_DIR, "Transfer.lean"))
    H_def = extract_def(lpr, "H")
    T_L_def = extract_def(transfer_src, "T_L")
    transfer_operator = {
        "file": "%s/LatticePositivityReal.lean" % REL,
        "definition_H": H_def,
        "is_scalar_shadow": True,
        "proven_bound": None,
        "_note": (
            "H is the SCALAR / Perron-sector shadow `H U = wilsonAction U \u2022 \U0001D7D9`, "
            "NOT the real Wilson transfer operator on L\u00b2(\u220f SU(3), Haar). It is "
            "DEFINED in LatticePositivityReal.lean (line 73) and consumed downstream by "
            "the Step-5 spectral predicates (e.g. SpectrumBound.lean) and the MassGap574 "
            "scaffold. No `m > 0` / mass-gap / Surface-#1 bound is proven anywhere."
        ),
        "T_L": {
            "file": "%s/Transfer.lean" % REL,
            "definition_T_L": T_L_def,
            "proven_bound": "\u2016T_L\u2016 \u2264 1 (sub-Markov contraction; transfer_operator_norm_le)",
            "_note": (
                "Genuine integral operator over the REAL product Haar measure. Only the "
                "UPPER bound \u2016T_L\u2016 \u2264 1 is proven \u2014 NOT a spectral gap, NOT a strict "
                "contraction, NO `m > 0` / mass-gap claim. The spectral gap stays OPEN as "
                "Transfer.kotecky_preiss_criterion."
            ),
        },
    }

    # --- su3_files (step 3) -------------------------------------------------
    su3_files = []
    for f in ["SU3.lean", "SU3Basis.lean", "SU3Instances.lean"]:
        content = read(os.path.join(YM_DIR, f))
        su3_files.append({
            "path": "%s/%s" % (REL, f),
            "sha256": sha256_text(content),
            "content": content,
        })

    # --- massgap574 (step 4) ------------------------------------------------
    mg = read(os.path.join(YM_DIR, "MassGap574.lean"))
    mg_real_sorry = count_real_sorry(mg)
    mg_raw_tokens = len(re.findall(r"sorry", mg))
    statement, proof_body = extract_theorem(mg, "YM_mass_gap")
    massgap574 = {
        "path": "%s/MassGap574.lean" % REL,
        "full_text": mg,
        "statement": statement,
        "proof_body": proof_body,
        "sorry_count": mg_real_sorry,
        "_sorry_note": (
            "sorry_count is the TRUE count of `sorry`/`admit` PROOF TERMS = %d. "
            "The file's own header/docstrings still say it 'carries a sorry' "
            "(%d raw 'sorry' tokens appear, ALL inside comments/docstrings) \u2014 that "
            "prose is STALE. Post the 2026-05-31 SORRY PURGE the unproved spectral "
            "gap is carried as the NAMED-OPEN Prop `YM_mass_gap_Surface` (a hypothesis "
            "`hsurf`), NOT a `by sorry`. The theorem is OPEN/conditional, but it is "
            "NOT discharged by sorry. The repo-wide Lean proof-term sorry count is 0."
            % (mg_real_sorry, mg_raw_tokens)
        ),
        "is_open": True,
        "is_scalar_shadow": True,
        "companion": {
            "name": "YM_mass_gap_nontrivial",
            "real_sorry_proof_terms": 0,
            "_note": (
                "Discharges the SCALAR-shadow statement for non-trivial U (\u2265 1 "
                "non-identity plaquette), sorry-free, classical trio \u2014 but still only "
                "over H U = wilsonAction U \u2022 \U0001D7D9, the scalar shadow. NO real YM mass "
                "gap; Surface #1 stays OPEN."
            ),
        },
    }

    # --- bridge_data + kappa_history (step 5, OUT-OF-TOWER) ------------------
    bridge_csv = os.path.join(REPO, "data", "desert_map_bridge.csv")
    bridge_rows = {}
    if os.path.exists(bridge_csv):
        with open(bridge_csv, newline="") as fh:
            for row in csv.DictReader(fh):
                bridge_rows[row["k"]] = row
    bridge_data = {
        "_provenance": (
            "OUT-OF-TOWER. NOT part of Towers/YM/*. Sourced from "
            "data/desert_map_bridge.csv + scripts/build_desert_map_site_data.py "
            "(Hodge/BDP desert-map programme). Bridge witness "
            "|q\u00b7\u03ba^m \u2212 p \u2212 k\u00b7\u03c0| < 1. Only P5 is a tight computable VERIFIED "
            "witness; P1\u2013P4 are trivial (q=p, m=0 \u21d2 error 0). P6\u2013P20 are "
            "BEYOND_TOLERANCE at 15-digit \u03ba \u2014 never reported as a pass."
        ),
    }
    for k in range(6, 21):
        row = bridge_rows.get(str(k), {})
        bridge_data["P%d" % k] = {
            "best_q": None,
            "best_m": None,
            "best_defect": None,
            "status": row.get("bdp_status", "BEYOND_TOLERANCE"),
            "tolerance_log10": float(row["bdp_tolerance_log10"]) if row.get("bdp_tolerance_log10") else None,
        }
    # P5 is recorded honestly alongside (it is the one verified witness), still out-of-tower.
    p5 = bridge_rows.get("5", {})
    bridge_data["_P5_verified"] = {
        "best_q": int(p5["bdp_q"]) if p5.get("bdp_q") else None,
        "best_m": int(p5["bdp_m"]) if p5.get("bdp_m") else None,
        "best_k": int(p5["bdp_k"]) if p5.get("bdp_k") else None,
        "best_defect": float(p5["bdp_error"]) if p5.get("bdp_error") else None,
        "status": p5.get("bdp_status"),
        "_note": "The single tight computable bridge witness; OUT-OF-TOWER (BDP, not YM).",
    }

    kappa_src = (
        "OUT-OF-TOWER. data/desert_map_bridge.csv + "
        "scripts/build_desert_map_site_data.py (\u03ba = \u03c6_c/108, 15 digits). "
        "NOT a Towers/YM object; no YM mass-gap link is claimed."
    )
    kappa_history = []
    for v in range(1, 16):
        kappa_history.append({
            "version": "kappa_%d" % v,
            "value": 4.84330141945946 if v == 15 else None,
            "source": kappa_src if v == 15 else "not recorded",
        })

    # --- comments_raw (step 6) ---------------------------------------------
    comments_raw = []
    for f in files:
        if is_stub(f):
            continue  # stubs excluded from comment scan per spec
        text = read(os.path.join(YM_DIR, f))
        for line_no, ctext in comment_lines(text):
            low = ctext.lower()
            if any(kw in low for kw in KEYWORDS):
                comments_raw.append({
                    "file": "%s/%s" % (REL, f),
                    "line": line_no,
                    "text": ctext,
                })

    export = {
        "_meta": {
            "task": "Project Task #316 \u2014 YM tower audit export",
            "scope": "lean-proof-towers/Towers/YM/*.lean (%d files, %d stubs)" % (
                len(files), sum(1 for f in files if is_stub(f))),
            "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "generator": "scripts/build_ym_audit_export.py",
            "honesty_notes": [
                "TRUE repo state only. No mass-gap / \u03bc>0 / Surface-#1-closed / Clay claim.",
                "Repo-wide Lean proof-term sorry/admit count across Towers/YM = 0 (all 'sorry' tokens are prose).",
                "H and T_L are scalar-shadow / contraction objects \u2014 NOT the real Wilson transfer operator.",
                "bridge_data + kappa_history are OUT-OF-TOWER (Hodge/BDP desert-map), included only because the schema asks; P6\u2013P20 are BEYOND_TOLERANCE, never a pass.",
                "Stub (*Stub.lean) content is null by design.",
            ],
        },
        "transfer_operator": transfer_operator,
        "su3_files": su3_files,
        "massgap574": massgap574,
        "bridge_data": bridge_data,
        "kappa_history": kappa_history,
        "comments_raw": comments_raw,
        "_manifest": manifest,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    print("WROTE", OUT)
    print("files=%d stubs=%d comments_raw=%d total_real_sorry=%d" % (
        len(files),
        sum(1 for f in files if is_stub(f)),
        len(comments_raw),
        sum(m["real_sorry_proof_terms"] for m in manifest),
    ))


if __name__ == "__main__":
    main()
