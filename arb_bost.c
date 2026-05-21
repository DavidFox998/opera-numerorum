// Battle Plan v1.6 - Module 5: Bost Sum C(S_14) > 2*sqrt(13)
// Library: ARB 2.23.0, MPFR 4.2.0, GMP 6.2.1
// Depends on: Module 4 SHA b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed
// NOTE: Input format is comma-separated (Module 4 stdout format).
// NOTE: Large primes > 2^64 require ARB string-based reading.
// NOTE: ARB unavailable in this environment; see arb_bost.py for mpmath fallback.

#include <arb.h>
#include <stdio.h>
#include <stdlib.h>

#define PREC 64 // 64 bits = ~19 decimal digits, sufficient for non-overlapping intervals

int main(int argc, char *argv[]) {
    if (argc!= 2) {
        fprintf(stderr, "Usage: %s S14_primes.txt\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("fopen"); return 1; }

    arb_t C, term, p, logp, pm1, threshold, two, thirteen;
    arb_init(C); arb_init(term); arb_init(p);
    arb_init(logp); arb_init(pm1); arb_init(threshold);
    arb_init(two); arb_init(thirteen);

    arb_zero(C);
    arb_set_ui(two, 2);
    arb_set_ui(thirteen, 13);

    // Compute 2*sqrt(13) with rigorous error bounds
    arb_sqrt(threshold, thirteen, PREC);
    arb_mul(threshold, two, threshold, PREC);

    // Read 14 primes as strings (handles arbitrary-precision integers)
    // and sum log(p)/(p-1)
    for(int i = 0; i < 14; i++) {
        char buf[64];
        if (fscanf(f, "%63[^,\n]", buf) != 1) {
            fprintf(stderr, "Error reading prime %d\n", i);
            return 1;
        }
        // Skip separator (comma or newline)
        int c = fgetc(f);
        (void)c;

        // Set p from string for arbitrary precision
        arb_set_str(p, buf, PREC);
        arb_log(logp, p, PREC);
        arb_sub_ui(pm1, p, 1, PREC);
        arb_div(term, logp, pm1, PREC);
        arb_add(C, C, term, PREC);
    }
    fclose(f);

    // Output with error bounds - this is the proof
    printf("C(S14) in ");
    arb_printd(C, 16); printf("\n");

    printf("2*sqrt(13) in ");
    arb_printd(threshold, 16); printf("\n");

    // arb_gt returns 1 if C > threshold is provably true
    int gt = arb_gt(C, threshold);
    printf("arb_gt(C, threshold) = %d\n", gt);

    if (!gt) {
        fprintf(stderr, "FATAL: C(S14) <= 2*sqrt(13). Certificate invalid.\n");
        return 2;
    }

    printf("Certificate: C(S14) > 2*sqrt(13) verified\n");

    arb_clear(C); arb_clear(term); arb_clear(p);
    arb_clear(logp); arb_clear(pm1); arb_clear(threshold);
    arb_clear(two); arb_clear(thirteen);
    return 0;
}
