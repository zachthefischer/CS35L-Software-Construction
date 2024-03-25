/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>



#include "./options.h"
#include "./rand64-hw.h"
#include "./rand64-sw.h"
#include "./output.h"


/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  // Create an opt argument to keep track of the option information
  struct opts opt;
  read_options(argc, argv, &opt);

  // Return an error if options are invalid 
  if (!opt.valid)
    {
      fprintf (stderr, "ERROR %s: usage: %s [OPTION] NBYTES\n", argv[0], argv[0]);
      return 1;
    }

  /* If there's no work to do, don't worry about which library to use.  */
  if (opt.nbytes == 0)
    return 0;


  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);

  // HANDLE INPUT 
  switch (opt.input){
    case DEFAULT:
    case RDRAND:
      if(rdrand_supported()){
        initialize = hardware_rand64_init;
        rand64 = hardware_rand64;
        finalize = hardware_rand64_fini;
      } else {
        // Hardware implemenation not available
        fprintf (stderr, "Sorry, hardware does not support rdrand \n");
        exit(1);
      }
      break;

    case MRAND48_R:
      initialize = hardware_mrand48_init;
      rand64 = hardware_mrand48;
      finalize = hardware_mrand48_fini;
      break;
    
    case SLASH_F:
      // Set file path 
      size_t file_length = strlen(opt.r_src);
      rsrc = malloc(file_length * sizeof(char));

      // Handle memory allocation errors
      if (rsrc == NULL) {
        fprintf (stderr, "Unable to allocate \n");
        exit(1);
      }

      // Copy opt.r_src to rsrc
      strcpy(rsrc, opt.r_src);

      initialize = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
      break;
  
    default:
      fprintf (stderr, "Invalid input option. \n");
      exit(1);
  }

  
  initialize ();
  int wordsize = sizeof rand64();
  int nbytes = opt.nbytes;
  int output_errno = 0;

  /* HANDLE OUTPUT */

  if(opt.output == STDIO){
    // Standard Output - user writeBytes to print each random byte
    do 
      {
        unsigned long long x = rand64();
        int outbytes = nbytes < wordsize ? nbytes : wordsize;
        if (!writeBytes (x, outbytes))
        {
          output_errno = errno;
          break;
        }
          nbytes -= outbytes;
      }
    while (0 < nbytes);
  } 
  else {
    // N block output - write each character to a buffer

    char * obuffer = (char *) malloc(opt.block_size);
    
    // Loop through all bytes in nbytes
    do {
      // Set outbytes to appropriate number of bytes (up to block_size)
      int outbytes = nbytes < opt.block_size ? nbytes : opt.block_size;

      for (int i = 0; i < outbytes; i++) {
        obuffer[i] = rand64();
        // Most of the rand64() data is unused but oh well
      }

      // Write the bytes from the buffer to standard output
      int status = write(1, obuffer, outbytes);
      if (status < 0){
        fprintf(stderr, "Write failed");
      }

      nbytes -= outbytes;
    } while (nbytes > 0);

    free(obuffer);
  }



  // Print errors if applicable
  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}
