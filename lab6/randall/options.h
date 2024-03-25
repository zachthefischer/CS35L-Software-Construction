#ifndef OPTIONS_H
#define OPTIONS_H

#include <stdbool.h> 
#include <stdio.h>   
#include <stdlib.h>  
#include <errno.h>

// Possible input and output options
enum Input { RDRAND, MRAND48_R, SLASH_F, DEFAULT };
enum Output { STDIO, NUM};

struct opts {
    bool valid;
    long long nbytes;
    enum Input input;
    enum Output output;
    char* r_src;
    unsigned int block_size;
};

void read_options(int argc, char **argv, struct opts *opt);

#endif
