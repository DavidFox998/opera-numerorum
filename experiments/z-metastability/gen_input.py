#!/usr/bin/env python3
"""Z Experiment Harness v1 - input set generator.

Generates Z_INPUT_SET.json deterministically. NO literal is typed by hand:
every test string is constructed by this script and its digit_len / zero_run
are MEASURED from the constructed string (never trusted from a label).

Grid:
  digit_len in [10,11,12,13,14,15,16,18,20,25]
  zero_run  in [0,3,6,9,12,15]   (feasible only when zero_run <= digit_len-1)

sym is filled ONLY from the certified H4Core witness set; unknown -> null.
We do NOT compute or guess Sym for arbitrary strings.
"""
import json
from itertools import cycle

# Certified Sym values from H4Core / H4_Boundary.data.json (the ONLY known Sym).
KNOWN_SYM = {
    "2": 120,
    "3": 20,
    "19": 2,
    "191": 2,
    "1000000001119": 1,
    "10000000001119": 1,
    "1000000001357": 1,
    "1000000001511": 1,
    "1000000001723": 1,
    "1000000001831": 1,
}

DIGITS = [10, 11, 12, 13, 14, 15, 16, 18, 20, 25]
ZERO_RUNS = [0, 3, 6, 9, 12, 15]
TARGET = 50


def nonzero_filler(n: int) -> str:
    c = cycle("123456789")
    return "".join(next(c) for _ in range(n))


def construct(d: int, z: int) -> str | None:
    """Build a length-d string whose single zero-run has length z."""
    if z == 0:
        return nonzero_filler(d)
    if z > d - 1:  # need at least one leading nonzero digit
        return None
    return "1" + ("0" * z) + nonzero_filler(d - 1 - z)


def longest_zero_run(s: str) -> int:
    best = run = 0
    for ch in s:
        run = run + 1 if ch == "0" else 0
        best = max(best, run)
    return best


def entry(s: str) -> dict:
    return {
        "s": s,
        "digits": len(s),
        "zero_run": longest_zero_run(s),
        "sym": KNOWN_SYM.get(s, None),
    }


def main() -> None:
    out, seen = [], set()

    # Seed with certified witnesses so the Sym axis has real (non-null) data.
    for s in KNOWN_SYM:
        if s not in seen:
            out.append(entry(s))
            seen.add(s)

    # Fill grid cells until TARGET.
    for d in DIGITS:
        for z in ZERO_RUNS:
            if len(out) >= TARGET:
                break
            s = construct(d, z)
            if s is None or s in seen:
                continue
            out.append(entry(s))
            seen.add(s)
        if len(out) >= TARGET:
            break

    out = out[:TARGET]
    with open("Z_INPUT_SET.json", "w") as f:
        json.dump(out, f, indent=2)
    n_sym = sum(1 for e in out if e["sym"] is not None)
    print(f"wrote Z_INPUT_SET.json: {len(out)} strings, {n_sym} with known Sym")


if __name__ == "__main__":
    main()
