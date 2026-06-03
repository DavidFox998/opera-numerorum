#!/usr/bin/env bash
# Z Experiment Harness v1 - tool-assisted reproduction test.
#
# For each string s in Z_INPUT_SET.json, reproduce it via the deterministic
# shell tools `printf`/`${#s}` (this is the TOOL-ASSISTED path, T=1), 100 trials.
# An "error" = the echoed string or its measured length differs from the input.
#
# NOTE (honest): shell echo + ${#s} are exact by construction, so this harness
# measures the T=1 regime and will record E_measured = 0 for every string. It
# verifies the (1-T) mitigation term; it does NOT measure pure-generation (T=0)
# error. Producing T=0 data requires an LLM reproducing literals WITHOUT a tool,
# which a shell script cannot do.
set -euo pipefail
cd "$(dirname "$0")"

IN="Z_INPUT_SET.json"
OUT="Z_MEASURE.csv"
TRIALS="${TRIALS:-100}"

# Extract rows as TSV: s \t digits \t zero_run \t sym
python3 - "$IN" > /tmp/z_rows.tsv <<'PY'
import json, sys
for e in json.load(open(sys.argv[1])):
    sym = "null" if e["sym"] is None else e["sym"]
    print(f'{e["s"]}\t{e["digits"]}\t{e["zero_run"]}\t{sym}')
PY

echo "s,digits,zero_run,sym,errors,trials,E_measured" > "$OUT"

while IFS=$'\t' read -r s exp_d zero_run sym; do
  errors=0
  for ((i = 0; i < TRIALS; i++)); do
    out_s=$(printf '%s' "$s")      # tool-assisted reproduction of the literal
    out_d=$(printf '%s' "${#s}")   # tool-assisted digit count
    if [[ "$out_s" != "$s" || "$out_d" != "$exp_d" ]]; then
      errors=$((errors + 1))
    fi
  done
  e_meas=$(awk "BEGIN{printf \"%.6f\", $errors/$TRIALS}")
  echo "$s,$exp_d,$zero_run,$sym,$errors,$TRIALS,$e_meas" >> "$OUT"
done < /tmp/z_rows.tsv

echo "wrote $OUT ($(($(wc -l < "$OUT") - 1)) rows, $TRIALS trials each)"
