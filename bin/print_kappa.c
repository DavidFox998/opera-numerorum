// Battle Plan v1.6 - Tendon B
// k = phi(N) * c / 1e8 where N=143
#include <stdio.h>
#include <stdint.h>

uint64_t euler_phi(uint64_t n) {
    uint64_t result = n;
    for (uint64_t p = 2; p * p <= n; ++p) {
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}

int main() {
    const uint64_t N = 143; // 11 * 13
    const double c = 403608451.6483666; // Conductor normalization
    uint64_t phi_N = euler_phi(N); // = 120
    double kappa = (double)phi_N * c / 1.0e10;
    printf("%.16f\n", kappa);
    return 0;
}
