#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>


#include "options.h"

void read_options(int argc, char **argv, struct opts *opt) {
  
    /* Set option struct to default values  */
    opt->valid = false;
    opt->input = DEFAULT;
    opt->output = STDIO;


    /* Check basic number of arguments */
    if (argc < 2 || argc > 6){
        fprintf(stderr, "./randall usage: -i [INPUT] -o [OUTPUT] NBYTES\n");
        exit(1);
    }

    /* Debugging with print statements */
        // int c = getopt(argc, argv, ":i:o:");
        // printf("option is %d\n", c);
        // printf("optarg is %s\n", optarg);
        // printf("c=getopt is %d", (c = getopt(argc, argv, ":i:o:")));

    /* Check value of argument using getopt --> sets value of optarg */
    /* Options i, o, and empty take arguments */
    
    int c;
    while ((c = getopt(argc, argv, ":i:o:")) != -1) {
        // printf("Optarg is %s, c is %d\n", optarg, c);
        // printf("c is %d", c);

        switch(c) {
            // case -1: //default
            case 'i':
                // printf("test");
                if (strcmp("rdrand", optarg) == 0) {
                    opt->input = RDRAND;
                } else if (strcmp("lrand48_r", optarg) == 0) {
                    /* Uses mrand implementation but I'm keeping
                       the "lrand48_r" input as specified in the spec */
                    opt->input = MRAND48_R;
                } else if ('/' == optarg[0]) {
                    opt->input = SLASH_F;
                    opt->r_src = optarg;
                } else {
                    fprintf(stderr, "ERROR: Valid arguments needed for -i: rdrand or lrand\n");
                    exit(1);
                }
                opt->valid = true;
                break; 
            case 'o':
                if (strcmp("stdio", optarg) == 0) {
                    opt->output = STDIO;
                } else {
                    opt->output = NUM;
                    opt->block_size = (atoi(optarg));
                
                    if (opt->block_size == 0){
                        fprintf(stderr, "ERROR: Valid block size needed for option -o N\n");
                        exit(1);
                    }

                    if (optind >= argc) {
                        fprintf(stderr, "ERROR: Option -o requires an operand N\n");
                        exit(1);
                    }
                }
                opt->valid = true;
                break;
            default:
                fprintf (stderr, "ERROR: invalid arguments");
                exit(1);
                break;
        }
    }

    /* Assign number of bytes to randomize */
    opt->nbytes = atol(argv[optind]);
    if (opt->nbytes >= 0) {
        opt->valid = true;
        if (opt->output == STDIO) {
            opt->block_size = opt->nbytes;
        }
    }
}