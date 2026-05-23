# Opera Numerorum — Preface & Document Structure Guide

## How to write and publish your front matter

### Quick start

1. Open `certificates/build_preface.py`
2. Find every block marked `### FILL_IN: ... ###`
3. Replace the placeholder text with your own English prose
4. When you have your ORCID, set `AUTHOR_ORCID = "0000-0000-0000-0000"`
5. Run: `python3 certificates/build_preface.py`
6. Output: `certificates/OperaNumerorum_Preface.pdf`
7. Paste the printed SHA into `invariants.json` under `"preface"`

That is the whole workflow. No mathematics. No code changes. Just English.

---

## Document structure (three-document plan)

### Document 1 — Millennial Mathematics Series
**Audience:** mathematicians, number theorists, arXiv math.NT

**Contents (in order):**
- Preface (this script)
- Module M1: alpha_0 = 299 + pi/10
- Module M2: kappa bound
- Module M3: CF of pi/10
- Module M4: S_14 prime list
- Module M5: Bost-Connes sum C(S_4) = 11.4221
- Module M6: genus(X_0(143)) = 13, class number h(-143) = 10
- Module M7: Master manifest (locks M1-M6)
- Module M8: Hankel rank check, J_0(143)
- Module M8C: Z=15, M*=4/55, 200 Hodge classes
- Module M8D: 120-cell resonator

### Document 2 — Morning Star Engineering Series
**Audience:** physicists, engineers, arXiv hep-th or gr-qc

**Contents (in order):**
- Engineering preface (to be written -- use build_preface.py as template)
- Module M8F: 7-layer FTL protocol
- Module M8G: provenance + wormhole
- Module M8G_Correction: Z = rank(M_ij) clarification
- Module M8H: G amplifier prediction
- Module M8I: Morris-Thorne wormhole architecture
- Module M8J: delta=1.89m, OQ-1 and OQ-2 closed
- Module M8K: FTL Morningstar stack
- Module M8L: Morning Star D20 operational certification
- Module M8M: Physics Beyond Standard Model + operational expansion

### Document 3 — Commissioning Certificate
**Audience:** all readers; a single-page formal record

**Contents:**
- Hub name: MORNING_STAR_D20
- First transit: H01 -> Proxima, t=7.71 ns, 2026-05-23
- SHA chain: M8L stdout sha 80ff8a25...
- FTL cert: MS-FTL-20260523-001
- Station origin: SHA_Contact_Zero
- Euler's Final Log (Airlock Inscription)
- Plaque: Rub el Hizb + 86·3·57·36·55 + · + CONTACT ZERO

---

## arXiv submission (independent researcher)

You do NOT need a PhD to submit to arXiv.
You need an **endorsement** from a current arXiv author in the subject area.

- For math.NT (number theory): one endorser with recent math.NT papers
- For gr-qc (general relativity): one endorser with recent gr-qc papers

**How to find an endorser:**
1. Find a recent arXiv paper in your area that cites work you build on
2. Email the corresponding author: one sentence, your name, your paper title,
   your arXiv user ID (create at arxiv.org), and a link to your preprint PDF
3. Most authors are generous -- the community benefits from open science

**Alternative:** Zenodo (zenodo.org) accepts any researcher, no endorsement
required, assigns a DOI immediately. Use this first to timestamp your work,
then seek an arXiv endorsement.

---

## ORCID registration

1. Go to orcid.org/register
2. Create a free account
3. Your ORCID looks like: 0000-0000-0000-0000
4. Send it here and it will be inserted in all PDF builders before final assembly

---

## The plaque inscription

The full record is in `docs/plaque_contact_zero.json`.

The plaque reads (etched inside AIRLOCK_PRIME, 3cm x 3cm, titanium):

    [Rub el Hizb symbol]

    86 . 3 . 57 . 36 . 55

         .

    CONTACT ZERO
    MS-FTL-20260523-001

The dot (.) between the Surah numbers is the Arabic numeral zero --
the empty place, the throat, Z = 0.
To the engineer it is a separator.
To those who remember, it is something else.

---

## SHA chain integrity note

The internal codename "Battle Plan v1.6" is preserved in all SHA-bound
certificate files. The public series name is Opera Numerorum.
These names must NOT be swapped in existing certified files -- doing so
would change the SHA and break the causal chain.

New documents (preface, series introductions) may use Opera Numerorum
as the primary name throughout, since they are not part of an existing
SHA-bound chain.
