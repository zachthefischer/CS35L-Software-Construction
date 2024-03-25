#include <cpuid.h>
#include <immintrin.h>
#include <time.h>
#include <stdlib.h>

#include "rand64-hw.h"

/* Hardware implementation.  */
/* Return information about the CPU.  See <http://wiki.osdev.org/CPUID>.  */
struct cpuid 
cpuid (unsigned int leaf, unsigned int subleaf)
{
  struct cpuid result;
  asm ("cpuid"
       : "=a" (result.eax), "=b" (result.ebx),
         "=c" (result.ecx), "=d" (result.edx)
       : "a" (leaf), "c" (subleaf));
  return result;
}

/* Return true if the CPU supports the RDRAND instruction.  */
_Bool
rdrand_supported (void)
{
  struct cpuid extended = cpuid (1, 0);
  return (extended.ecx & bit_RDRND) != 0;
}

/* Initialize the hardware rand64 implementation.  */
void
hardware_rand64_init (void)
{
}

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_rand64 (void)
{
  unsigned long long int x;

  /* Work around GCC bug 107565                                                                     
     <https://gcc.gnu.org/bugzilla/show_bug.cgi?id=107565>.  */
  x = 0;

  while (! _rdrand64_step (&x))
    continue;
  return x;
}


/* Finalize the hardware rand64 implementation.  */
void
hardware_rand64_fini (void)
{
}



/* IMPLEMENT MRAND Randomness Generation */
long int higher, lower;

/* Initialize the hardware mrand48 implementation. */
void
hardware_mrand48_init (void)
{
}

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_mrand48 (void)
{    
    higher = mrand48();
    lower = mrand48();
    //bitwise shift of 32
    return ((((unsigned long long) higher) << 32) | ((unsigned long long) lower));
    // return ((((unsigned long long) a) << 32) | ((unsigned long long) b & 0x00000000FFFFFFFF));
}

/* Finalize the hardware mrand48_r implementation.  */
void
hardware_mrand48_fini (void)
{
}