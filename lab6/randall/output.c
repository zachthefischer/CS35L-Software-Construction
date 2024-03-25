#include <limits.h>
#include <stdbool.h>
#include <stdio.h>

#include "output.h" 

// Write specified bytes to std output
bool
writeBytes (unsigned long long x, int nbytes)
{
  do
    {
      if (putchar (x) < 0)
	return false;
      x >>= CHAR_BIT;
      nbytes--;
    }
  while (0 < nbytes);

  return true;
}