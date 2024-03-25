#include <stdio.h>
#include <stdlib.h>

#include "rand64-sw.h"


/* Software implementation.  */

/* Pointer to file - Input stream containing random bytes */
FILE *urandstream; 

/* Character array to represent the filepath  */
char *rsrc;

/* Initialize the software rand64 implementation.  */
void
software_rand64_init (void)
{
  urandstream = fopen (rsrc, "r");
  if (! urandstream)
    abort ();
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 (void)
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}