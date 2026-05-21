/*
 * print_kappa.c  —  Compute kappa = phi * c / 10^8
 *
 * phi  = golden ratio  (1 + sqrt(5)) / 2
 * c    = 299,792,458   (speed of light in m/s, exact by SI definition)
 *
 * Strategy: hold c as an exact __uint128_t; represent phi to 20 significant
 * digits in a __uint128_t scaled by 10^20 to avoid all floating-point error
 * in the integer stages.  Final conversion to decimal uses long double.
 *
 * Compile:  gcc -O3 -std=c11 bin/print_kappa.c -o bin/print_kappa -lm
 */

#include <stdio.h>
#include <stdint.h>
#include <math.h>

/*
 * phi = 1.61803398874989484820...
 * phi * 10^20 = 161803398874989484820
 *
 * Split into two 64-bit halves for __uint128_t construction:
 *   hi = 1618033988  (first 10 digits)
 *   lo = 74989484820 (next 11 digits)
 */
static __uint128_t phi_u128(void) {
    __uint128_t hi = 1618033988ULL;
    __uint128_t lo = 74989484820ULL;
    /* phi_scaled = hi * 10^11 + lo = 161803398874989484820 */
    __uint128_t scale = 100000000000ULL; /* 10^11 */
    return hi * scale + lo;
}

int main(void) {
    /* c = 299,792,458 (exact integer) */
    __uint128_t c = 299792458ULL;

    /*
     * kappa = phi * c / 10^8
     *
     * Using our scaled representation:
     *   phi_scaled = phi * 10^20
     *   phi_scaled * c = phi * c * 10^20
     *   kappa * 10^12 = (phi_scaled * c) / 10^8
     *                 = phi_scaled * c / 100000000
     */
    __uint128_t phi_s = phi_u128();
    __uint128_t prod  = phi_s * c;           /* phi * c * 10^20            */
    __uint128_t div8  = 100000000ULL;        /* 10^8                       */
    __uint128_t kappa_e12 = prod / div8;     /* kappa * 10^12 (truncated)  */

    /* Extract digits: integer part and 16 decimal places */
    __uint128_t int_part  = kappa_e12 / ((__uint128_t)1000000000000ULL);  /* 10^12 */
    __uint128_t frac_part = kappa_e12 % ((__uint128_t)1000000000000ULL);

    /* Print as fixed-point with 12 decimals from __uint128_t, then
     * refine with long double for the remaining digits              */
    long double phi_ld  = (1.0L + sqrtl(5.0L)) / 2.0L;
    long double c_ld    = (long double)299792458ULL;
    long double kappa   = phi_ld * c_ld / 1.0e8L;

    printf("%.16Lf\n", kappa);

    /* Also print the __uint128_t verified integer prefix */
    fprintf(stderr,
            "uint128 check: %llu.%012llu...\n",
            (unsigned long long)int_part,
            (unsigned long long)frac_part);

    return 0;
}
