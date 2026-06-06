# Storage Map — Opera Numerorum

This file explains which assets live in the GitHub repository and which live on
Google Drive. Large ZIP archives are intentionally gitignored; anyone following
the SHA chain needs to know where to fetch them.

---

## What is in the GitHub repo

| Path | Description |
|------|-------------|
| `certificates/*.py` | All module source files (M1–M8, tower builds, ZIP builders) |
| `certificates/Module_*_Certificate.pdf` | Individual module PDFs (small enough to commit) |
| `certificates/invariants.json` | Full chain-of-custody record — source of truth for all SHAs and Drive URLs |
| `certificates/ALL_MATH_PROBLEMS.txt` | Master equation registry |
| `m1.out` … `m6.out` | Certified stdout files (inputs to `verify_all.sh`) |
| `verify_all.sh` | Chain verification script |
| `verify/bound_10_4000.py` | M4 verifier |
| `bin/print_kappa.c`, `bin/print_S14.c` | C sources for M2 and M4 |
| `bin/print_kappa`, `bin/print_S14` | Pre-compiled C binaries |
| `certificates/recertify.py` | CI self-check (5 fixture tests) |
| `certificates/validate_invariants.py` | Pre-commit hook validator |
| `GDRIVE_UPLOAD_RECEIPT.txt` | Narrative record of every Drive upload session |
| `GDRIVE_CERT_RECEIPT.txt` | Certificate delivery receipt |
| `ROADMAP.txt` | Project roadmap |
| `ALL_MATH_PROBLEMS.txt` | Equation census (root copy) |

---

## What is on Google Drive (gitignored — too large for GitHub)

These files are listed in `.gitignore` under the heading
`# Large ZIP archives (stored on Google Drive — too big for GitHub)`.
Their SHAs and Drive URLs are also recorded in `certificates/invariants.json`.

### Primary deliverable archives

| Local path | Size | Drive URL |
|------------|------|-----------|
| `certificates/OperaNumerorum_AllCerts.zip` | ~100 MB | https://drive.google.com/file/d/17ZrH7j7X6SsOyb_qVhn4BInKUszRmDFT/view?usp=sharing |
| `certificates/MorningStar_Complete_2026_06_04.zip` | ~64 MB | https://drive.google.com/file/d/18cJi0AqC-lvajxzxdc2pl_VzBNhn6ht5/view?usp=drivesdk |
| `certificates/Opera_Numerorum_All_Certs_2026_06_04.zip` | ~60 MB | superseded by `OperaNumerorum_AllCerts.zip` above |
| `certificates/ClaySubmission_2026_06_04.zip` | ~12 MB | https://drive.google.com/file/d/12OJ-VVHYhthbbhSpd6s6helZmsmrFbjf/view?usp=drivesdk |
| `OperaNumerorum_CompleteArchive.zip` | ~5 MB | early archive — superseded |
| `OperaNumerorum_records.zip` | ~37 KB | administrative records |
| `opera_numerorum_section8.zip` | ~29 MB | Section 8 working archive |

### Smaller archives also mirrored to Drive

| Local path | Drive URL |
|------------|-----------|
| `certificates/OperaNumerorum_Context.zip` | https://drive.google.com/file/d/1McMIbfjlIR3yrbTOcOqglhlcQYbrIuF1/view?usp=drivesdk |
| `certificates/CertificationChain_2026_06_04.zip` | https://drive.google.com/file/d/1yFSdmTMO_IuQGuDwuXW-n_yFgci4hLkT/view?usp=drivesdk |
| `certificates/ExtendedTheory_2026_06_06.zip` | https://drive.google.com/file/d/1o-XFiSeVu-p51U_O2gPqIyHiaxV5dy4G/view?usp=sharing |
| `certificates/Essays_Appendices_2026_06_06.zip` | https://drive.google.com/file/d/11uzvs55F6weTLmJzbWjdqwh0BULPYPNS/view?usp=sharing |

### Morning Star structured folder on Google Drive

The Morning Star content (85 zero-sorry PDFs, Lean proofs, manifests) is
organised into act-level subfolders under a parent folder:

| Folder | Drive URL |
|--------|-----------|
| `MORNING_STAR_20260606` (parent) | https://drive.google.com/drive/folders/1jXSQNCvmXbImp2iqrQNHms8XkKJ8A6DB |
| `00_PROLOGUE_CONTEXT` (4 PDFs) | https://drive.google.com/drive/folders/13uudlLcYnXInWHq-1ChqHsga3U0t3CIX |
| `01_ACT1_CLAY_COMPUTATIONAL_CERTS` (10 PDFs) | https://drive.google.com/drive/folders/16Mg_aEBf7cqNaWsE8iO4PEVHF9Rd0Dbu |
| `02_ACT2_GEOMETRY` (12 PDFs) | https://drive.google.com/drive/folders/19A_RkoTGp_dX4YOvH31XH3Mj-SCPboqp |
| `03_ACT3_ANALYTIC` (20 PDFs) | https://drive.google.com/drive/folders/1o9uCsLtC-dBxr8r9eayc-g0SPp0bR5as |
| `04_ACT4_BSD_FINAL_THEOREM` (11 PDFs) | https://drive.google.com/drive/folders/1nh8GzyOSxRzu1DZrSWSkZjLb6EQtBZ4h |
| `05_ACT5_CONSEQUENCES` (8 PDFs) | https://drive.google.com/drive/folders/1RFyZtrEbtWoJHT0UBV8E-8CnsH6htotH |
| `06_EPILOGUE_FUTURE_WORK` (2 PDFs) | https://drive.google.com/drive/folders/1laiAkdx_yJy3YPiwCJmmWDh39bOKory- |
| `APPENDIX_B_TRIVIAL_BY_CONSTRUCTION` (16 PDFs) | https://drive.google.com/drive/folders/1eBqslv4Y6LRRWc_6cB_f5dMGPM_OnnBP |
| `REFERENCE` (2 PDFs) | https://drive.google.com/drive/folders/11wwVbjp1lWJ3LPApCvuOf5eAkqkT66Wa |
| `MANIFESTS` (CSV + SHA256SUMS + addenda) | https://drive.google.com/drive/folders/1Z1tqm599kpqlIYBUxiDSzLlUSg8R79Xh |

### Individual files uploaded to Drive (addenda)

| File | Drive URL |
|------|-----------|
| `Replicut_10trillion_Data_Log.pdf` | https://drive.google.com/file/d/12hC4apvYAVe11JI1KMDMrvZdlSselz8C |
| `Equations_updated_20260606.docx` | https://drive.google.com/file/d/1WOQym1fUYX3NqapFn4R9NgMHHlDCnx9QO |
| `EquationCensus_20260606.zip` | https://drive.google.com/file/d/1bSjoZ773xtygefmv_IODmKMOfE573_w0/view?usp=drivesdk |
| `MORNING_STAR_REPO.tar.gz` (92.5 MB) | https://drive.google.com/file/d/1El43TE20wrdRuqdg40qZdI9-CfvqwyMO/view?usp=drivesdk |
| `certificates_of_verification.zip` | https://drive.google.com/file/d/1lCjAuvupktrfLcWvDnvPQxfP5nz3tsV5/view?usp=drivesdk |
| `classic_trio_files.zip` | https://drive.google.com/file/d/1lt5cvfEfKiuhF0n36FNsBAP2-KE2kzg_/view?usp=drivesdk |

---

## Why the split exists

GitHub imposes a 100 MB hard limit per file and a ~1 GB soft limit per
repository. `OperaNumerorum_AllCerts.zip` alone is ~100 MB; together the
large archives exceed GitHub's practical limits. Hosting them on Google Drive
keeps the repo fast to clone while preserving public accessibility.

The SHA-256 hash of every Drive-hosted file is recorded in
`certificates/invariants.json` so integrity can be verified after download
without trusting Drive itself.

---

## How to verify a downloaded archive

```bash
sha256sum OperaNumerorum_AllCerts.zip
# Compare against the sha256 field in certificates/invariants.json -> bundle_all_certs
```

The full chain is sealed in the M7 manifest:

```
5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9
```

Run `bash verify_all.sh` (requires the six `m*.out` files) to confirm the
entire M1–M7 computational chain from source to manifest.
