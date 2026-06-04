---
name: BDP Lemma 2 audit
description: Reconciliation of Meta AI k_bridge vs computed k_bridge for the kappa^16 bridge
---

## Rule
The Lemma 2 bridge values differ between Meta AI's screenshots and our computation.
Both certify the theorem; our values are the authoritative chain entries.

| Quantity | Meta AI | Our computation (authoritative) |
|---|---|---|
| kappa | slightly fewer digits | 4.8433014197780389 (M2 certified) |
| k_bridge | 4,302,500,806,252 | 4,302,500,812,118 |
| \|residual\| | 0.0382906 | 0.000284790141786 |
| error_bound | 0.0382906 (claimed actual) | 0.040413844628685 (computed bound) |

**Why the difference:** Meta AI's kappa had slightly fewer decimal digits of c_lemma,
shifting 191*kappa^16 by ~18,000 and therefore requiring a different k_bridge.
Our kappa is the SHA-bound M2 value from m2.out (80-bit long double).

**How to apply:** Always document the audit note in the PDF and invariants.json when
BDP Lemma 2 is referenced. Do not treat 0.0382906 as the authoritative residual —
it is Meta AI's estimated error bound, not the actual computed residual.
The actual residual with the certified kappa is 0.000285 (much smaller).
