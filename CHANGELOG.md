# MORNING STAR REPO — Changelog

## 2026-06-06 — Initial packaging
- CLAY sealed: 518144c8c37b3b7c48a1719924ab80b2ba03bec594923811148eb2b31e3881e1
- M7 manifest: 5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9
- 476 certified equations (LEAN:32 + OUT:230 + PDF:214)
- 85 zero-sorry PDFs in story order (PROLOGUE / ACT1-5 / EPILOGUE)
- BDP_PhaseReversal.lean: 32 theorems/lemmas/defs
- Modules certified: M1-M7, M8, M8C-M8Q, M25, M25B

## Errors caught and corrected (documented in M7 certificate)
1. M3: CF seed swapped — fixed to p=1,pp=0,q=0,qq=1
2. M5: Formula log(p)/(p-1) wrong — corrected to p*log(p)/(p-1)
3. M5: Wrong curve copy-paste — correct C(S4)=11.4221
4. M5: Hand-calc p=191 term — correct mpmath value 5.279917
5. M6: h(Q(sqrt(-143)))=1 claimed — correct h=10 (10 reduced forms)
