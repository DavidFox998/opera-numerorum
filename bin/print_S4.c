/*
 * print_S4.c — Enumeration of S(pi/10) for p <= 500
 *
 * Layer 1 of the machine verification protocol (Section 7).
 * Uses 80-bit long double arithmetic (~18-19 significant decimal digits),
 * which is more than sufficient to distinguish the gaps for all p <= 500.
 *
 * Compile:  gcc -O2 -o bin/print_S4 bin/print_S4.c -lm
 * Run:      ./bin/print_S4
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

/* pi/10 via long double — ~18-19 significant digits */
static const long double ALPHA = 0.31415926535897932385L; /* pi/10 */

/* Distance to nearest integer: ||x|| = min(frac, 1 - frac) */
static long double norm(long double x) {
    long double frac = x - floorl(x);
    return frac < 0.5L ? frac : 1.0L - frac;
}

/* Simple trial-division primality test */
static int is_prime(int n) {
    if (n < 2) return 0;
    if (n == 2) return 1;
    if (n % 2 == 0) return 0;
    for (int i = 3; (long long)i * i <= n; i += 2)
        if (n % i == 0) return 0;
    return 1;
}

int main(void) {
    printf("print_S4 — Enumeration of S(pi/10), primes p <= 500\n");
    printf("Arithmetic: 80-bit long double (~18-19 decimal digits)\n\n");
    printf("%-6s  %-22s  %-14s  %s\n",
           "p", "||p*pi/10||", "1/p (threshold)", "member?");
    printf("%-6s  %-22s  %-14s  %s\n",
           "------", "----------------------", "--------------", "-------");

    int exceptional[32];
    int n_exceptional = 0;

    for (int p = 2; p <= 500; p++) {
        if (!is_prime(p)) continue;

        long double d = norm((long double)p * ALPHA);
        long double threshold = 1.0L / (long double)p;
        int member = d < threshold;

        if (member) {
            printf("%-6d  %-22.15Lf  %-14.10Lf  YES  ***\n", p, d, threshold);
            if (n_exceptional < 32)
                exceptional[n_exceptional++] = p;
        } else {
            printf("%-6d  %-22.15Lf  %-14.10Lf  no\n", p, d, threshold);
        }
    }

    printf("\n--- Summary ---\n");
    printf("S4 = {");
    for (int i = 0; i < n_exceptional; i++)
        printf("%d%s", exceptional[i], i + 1 < n_exceptional ? ", " : "");
    printf("}\n");

    int expected[4] = {2, 3, 19, 191};
    int ok = (n_exceptional == 4);
    if (ok)
        for (int i = 0; i < 4; i++)
            if (exceptional[i] != expected[i]) { ok = 0; break; }

    printf("Expected {2, 3, 19, 191}: %s\n", ok ? "PASS" : "FAIL");
    return ok ? 0 : 1;
}
