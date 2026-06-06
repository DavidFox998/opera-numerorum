"""
build_z_essay_omnibus.py
Opera Numerorum -- Z Protocol Tower (v3) + Time Machine Essay -- Omnibus PDF
Combines Z_Protocol_Tower_v3.pdf (~24 pp) and Essay_TimeMachine_p5.pdf (~20 pp)
into a single public-submission artifact using pypdf.
SHA-256 bound. ASCII checked. Battle Plan v1.6.
Author: David Fox | June 4, 2026 | Updated June 6, 2026 for v3
"""

import hashlib
import re
import sys
import os

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print("ERROR: pypdf not available. Install with: pip install pypdf")
    sys.exit(1)

Z_PROTOCOL = "certificates/Z_Protocol_Tower_v3.pdf"
ESSAY      = "certificates/Essay_TimeMachine_p5.pdf"
OUTPUT     = "certificates/Z_Essay_Omnibus.pdf"

# ---- Verify inputs exist ----
for path in (Z_PROTOCOL, ESSAY):
    if not os.path.exists(path):
        print("ERROR: input not found: {}".format(path))
        sys.exit(1)

# ---- SHA inputs ----
def file_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

z_sha  = file_sha(Z_PROTOCOL)
e_sha  = file_sha(ESSAY)

print("Input: Z_Protocol_Tower.pdf")
print("  SHA-256: {}".format(z_sha))
z_reader = PdfReader(Z_PROTOCOL)
print("  Pages:   {}".format(len(z_reader.pages)))

print("Input: Essay_TimeMachine_p5.pdf")
print("  SHA-256: {}".format(e_sha))
e_reader = PdfReader(ESSAY)
print("  Pages:   {}".format(len(e_reader.pages)))

# ---- Merge ----
writer = PdfWriter()

for page in z_reader.pages:
    writer.add_page(page)

for page in e_reader.pages:
    writer.add_page(page)

writer.add_metadata({
    "/Title":   "Opera Numerorum: Z Protocol Tower + The Time Machine at p5 (Omnibus)",
    "/Author":  "David Fox",
    "/Subject": "Z Protocol Causality Tower; Time Machine at p5 Phase Reversal Essay; Battle Plan v1.6",
    "/Creator": "build_z_essay_omnibus.py (pypdf) -- Opera Numerorum",
})

total_pages = len(z_reader.pages) + len(e_reader.pages)
print()
print("Merging {} + {} = {} pages ...".format(
    len(z_reader.pages), len(e_reader.pages), total_pages))

with open(OUTPUT, "wb") as out:
    writer.write(out)

print("Output: {}".format(OUTPUT))

# ---- SHA output ----
out_sha = file_sha(OUTPUT)
out_size = os.path.getsize(OUTPUT)
print("Output SHA-256: {}".format(out_sha))
print("Output size:    {} bytes  ({:.2f} MB)".format(out_size, out_size / 1048576))
print("Total pages:    {}".format(total_pages))

# ---- ASCII check on text blocks ----
with open(OUTPUT, "rb") as f:
    raw = f.read()

text_blocks = re.findall(b"BT.*?ET", raw, re.DOTALL)
bad_chars = []
for block in text_blocks:
    for byte in block:
        if byte > 127:
            bad_chars.append(byte)

if bad_chars:
    print("ASCII check: WARNING -- {} non-ASCII bytes in text blocks".format(len(bad_chars)))
else:
    print("ASCII check: PASS (no non-ASCII in text blocks)")

# ---- Script SHA ----
with open(__file__, "rb") as f:
    script_sha = hashlib.sha256(f.read()).hexdigest()
print("Script SHA-256: {}".format(script_sha))

# ---- Causal binding summary ----
print()
print("=" * 64)
print("OPERA NUMERORUM -- Z ESSAY OMNIBUS  --  BATTLE PLAN v1.6")
print("=" * 64)
print("Z_Protocol_Tower_v3.pdf SHA: {}".format(z_sha[:32]))
print("Essay_TimeMachine_p5 SHA:    {}".format(e_sha[:32]))
print("Omnibus output SHA-256:    {}".format(out_sha))
print("Total pages: {}".format(total_pages))
print("ASCII: PASS" if not bad_chars else "ASCII: WARNING")
print("Status: OMNIBUS_CERTIFIED")
print("=" * 64)
