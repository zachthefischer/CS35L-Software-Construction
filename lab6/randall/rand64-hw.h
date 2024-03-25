#ifndef RAND64_HW_H
#define RAND64_HW_H

#include <stdbool.h>

/* Description of the current CPU.  */
struct cpuid {
  unsigned eax, ebx, ecx, edx;
};

struct cpuid cpuid(unsigned int leaf, unsigned int subleaf);

_Bool rdrand_supported(void);
void hardware_rand64_init(void);
unsigned long long hardware_rand64(void);
void hardware_rand64_fini(void);

void hardware_mrand48_init (void);
unsigned long long hardware_mrand48 (void);
void hardware_mrand48_fini (void);

#endif 
