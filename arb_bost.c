// Battle Plan v1.6 - Module 5: Bost Sum C(S4) > 2*sqrt(13)
// Library: ARB 2.23.0, MPFR 4.2.0, GMP 6.2.1
// Formula: C(S4) = sum_{p in S4} log(p) * p/(p-1)
// S4 = {2, 3, 19, 191} -- first 4 elements of S(alpha_0)
// Depends on: Module 4 SHA b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed
// NOTE: ARB unavailable in this environment; see arb_bost.py for mpmath fallback.

#include <arb.h>
#include <stdio.h>
#include <stdlib.h>

#define PREC 64 // 64 bits = ~19 decimal digits, sufficient for non-overlapping intervals

int main(void) {
    int S4[] = {2, 3, 19, 191};
    int n = 4;

    arb_t C, term, p_arb, logp, pm1, threshold, two, thirteen;
    arb_init(C); arb_init(term); arb_init(p_arb);
    arb_init(logp); arb_init(pm1); arb_init(threshold);
    arb_init(two); arb_init(thirteen);

    arb_zero(C);
    arb_set_ui(two, 2);
    arb_set_ui(thirteen, 13);

    // Compute 2*sqrt(13) with rigorous error bounds
    arb_sqrt(threshold, thirteen, PREC);
    arb_mul(threshold, two, threshold, PREC);

    // C(S4) = sum_{p in S4} log(p) * p/(p-1)
    for (int i = 0; i < n; i++) {
        arb_set_ui(p_arb, S4[i]);
        arb_log_ui(logp, S4[i], PREC);       // log(p)
        arb_sub_ui(pm1, p_arb, 1, PREC);     // p-1
        arb_div(term, p_arb, pm1, PREC);      // p/(p-1)
        arb_mul(term, logp, term, PREC);      // log(p)*p/(p-1)
        arb_add(C, C, term, PREC);
    }

    // Output with error bounds
    printf("C(S4) in ");
    arb_printd(C, 10); printf("\n");

    printf("2*sqrt(13) in ");
    arb_printd(threshold, 10); printf("\n");

    // arb_gt returns 1 if C > threshold is provably true
    int gt = arb_gt(C, threshold);
    printf("arb_gt(C, threshold) = %d\n", gt);

    if (!gt) {
        fprintf(stderr, "FATAL: C(S4) <= 2*sqrt(13). Certificate invalid.\n");
        arb_clear(C); arb_clear(term); arb_clear(p_arb);
        arb_clear(logp); arb_clear(pm1); arb_clear(threshold);
        arb_clear(two); arb_clear(thirteen);
        return 2;
    }

    printf("Certificate: C(S4) > 2*sqrt(13) verified\n");

    arb_clear(C); arb_clear(term); arb_clear(p_arb);
    arb_clear(logp); arb_clear(pm1); arb_clear(threshold);
    arb_clear(two); arb_clear(thirteen);
    return 0;
}
