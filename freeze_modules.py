"""
freeze_modules.py -- Opera Numerorum module freeze utility
Usage: python3 freeze_modules.py --modules C01 C02 ... --reason "..." --author "..."

Writes (or updates) certificates/freeze_manifest.json with per-file SHA-256
hashes, freeze timestamp, reason, and author for the specified modules.

Module-to-file mapping:
  C01 -> lean-proof-towers/C01_Arakelov.lean
  C02 -> lean-proof-towers/C02_Modularity.lean
  C03 -> lean-proof-towers/C03_Positivity.lean
  C04 -> lean-proof-towers/C04_HeightBound.lean
  C05 -> lean-proof-towers/C05_Discriminant.lean
  C06 -> lean-proof-towers/C06_ZetaControl.lean
  C07 -> lean-proof-towers/C07_RH.lean
  C08 -> lean-proof-towers/C08_Descent.lean
  BDP -> lean-proof-towers/BDP_PhaseReversal.lean
"""

import argparse, hashlib, json, os, sys
from datetime import datetime, timezone

MODULE_FILES = {
    "C01": "lean-proof-towers/C01_Arakelov.lean",
    "C02": "lean-proof-towers/C02_Modularity.lean",
    "C03": "lean-proof-towers/C03_Positivity.lean",
    "C04": "lean-proof-towers/C04_HeightBound.lean",
    "C05": "lean-proof-towers/C05_Discriminant.lean",
    "C06": "lean-proof-towers/C06_ZetaControl.lean",
    "C07": "lean-proof-towers/C07_RH.lean",
    "C08": "lean-proof-towers/C08_Descent.lean",
    "BDP": "lean-proof-towers/BDP_PhaseReversal.lean",
}

MANIFEST_PATH = "certificates/freeze_manifest.json"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def strip_lean_comments(text):
    """Strip Lean line comments (--) and block comments (/-...-/, nestable)."""
    import re
    result = []
    i = 0
    n = len(text)
    while i < n:
        # Line comment
        if text[i:i+2] == '--':
            while i < n and text[i] != '\n':
                i += 1
            continue
        # Block comment (nestable)
        if text[i:i+2] == '/-':
            depth = 1
            i += 2
            while i < n and depth > 0:
                if text[i:i+2] == '/-':
                    depth += 1
                    i += 2
                elif text[i:i+2] == '-/':
                    depth -= 1
                    i += 2
                else:
                    i += 1
            continue
        # String literal (skip contents)
        if text[i] == '"':
            result.append(text[i])
            i += 1
            while i < n and text[i] != '"':
                if text[i] == '\\':
                    result.append(text[i])
                    i += 1
                if i < n:
                    result.append(text[i])
                    i += 1
            if i < n:
                result.append(text[i])
                i += 1
            continue
        result.append(text[i])
        i += 1
    return ''.join(result)

def count_sorries(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    import re
    declared = re.search(r'Sorry count this file:\s*(\d+)', raw)
    code_only = strip_lean_comments(raw)
    sorries = re.findall(r'\bsorry\b', code_only)
    return {
        "token_count": len(sorries),
        "declared_in_header": int(declared.group(1)) if declared else None
    }

def main():
    parser = argparse.ArgumentParser(description="Freeze Opera Numerorum Lean modules")
    parser.add_argument("--modules", nargs="+", required=True,
                        help="Module IDs to freeze (e.g. C01 C02 C07)")
    parser.add_argument("--reason", required=True, help="Freeze reason")
    parser.add_argument("--author", required=True, help="Author name")
    args = parser.parse_args()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Load existing manifest if present
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH) as f:
            manifest = json.load(f)
    else:
        manifest = {
            "description": "Opera Numerorum Lean proof tower freeze manifest",
            "series": "Opera Numerorum",
            "internal": "Battle Plan v1.6",
            "freeze_records": []
        }

    frozen_modules = {}
    errors = []

    for mod in args.modules:
        mod_upper = mod.upper()
        if mod_upper not in MODULE_FILES:
            print(f"ERROR: unknown module {mod_upper} -- known: {', '.join(MODULE_FILES)}")
            errors.append(mod_upper)
            continue
        path = MODULE_FILES[mod_upper]
        if not os.path.exists(path):
            print(f"ERROR: file not found: {path}")
            errors.append(mod_upper)
            continue
        sha = sha256_file(path)
        sorry_info = count_sorries(path)
        frozen_modules[mod_upper] = {
            "file": path,
            "sha256": sha,
            "sorry_tokens_in_file": sorry_info["token_count"],
            "sorry_count_declared": sorry_info["declared_in_header"],
            "status": "ZERO_SORRY" if sorry_info["token_count"] == 0 else "HAS_SORRY"
        }
        status = frozen_modules[mod_upper]["status"]
        print(f"  {mod_upper:4s}  {sha[:16]}...  {path}  [{status}  sorry_tokens={sorry_info['token_count']}]")

    if errors:
        print(f"\nABORTED: {len(errors)} module(s) not found or unknown: {errors}")
        sys.exit(1)

    record = {
        "freeze_id": f"FREEZE_{'+'.join(sorted(frozen_modules.keys()))}_{now[:10].replace('-','')}",
        "timestamp": now,
        "author": args.author,
        "reason": args.reason,
        "modules": frozen_modules
    }

    manifest["freeze_records"].append(record)
    manifest["latest_freeze"] = record

    # Write manifest
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nFREEZE RECORD written to {MANIFEST_PATH}")
    print(f"  freeze_id : {record['freeze_id']}")
    print(f"  timestamp : {record['timestamp']}")
    print(f"  author    : {record['author']}")
    print(f"  reason    : {record['reason']}")
    print(f"  modules   : {', '.join(sorted(frozen_modules.keys()))}")
    all_zero = all(v["sorry_tokens_in_file"] == 0 for v in frozen_modules.values())
    print(f"  ZERO_SORRY: {'ALL PASS' if all_zero else 'SOME HAVE SORRY -- check above'}")

    # Emit a short stdout suitable for SHA binding
    print("\n=== FREEZE STDOUT (SHA-bindable) ===")
    print(f"FREEZE_ID={record['freeze_id']}")
    print(f"TIMESTAMP={record['timestamp']}")
    print(f"AUTHOR={record['author']}")
    print(f"REASON={record['reason']}")
    for mod, info in sorted(frozen_modules.items()):
        print(f"{mod}={info['sha256']}  sorry={info['sorry_tokens_in_file']}  [{info['status']}]")
    print(f"ZERO_SORRY_ALL={'YES' if all_zero else 'NO'}")

if __name__ == "__main__":
    main()
