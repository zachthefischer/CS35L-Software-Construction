#!/usr/bin/python                                                                                                                                              
"""
Skeleton code taken from Prof. Eggerts "randline.py":
Output lines selected randomly from a file
Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify                                                                                          
it under the terms of the GNU General Public License as published by                                                                                          
the Free Software Foundation; either version 3 of the License, or

(at your option) any later version.                                                                                                                           
This program is distributed in the hope that it will be useful,                                                                                               
but WITHOUT ANY WARRANTY; without even the implied warranty of                                                                                                
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                                                                 
GNU General Public License for more details.                                                                                                                  
                                                                                                                                                              
Please see <http://www.gnu.org/licenses/> for a copy of the license.                                                                                          
$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $                                                                                                       
"""

import random, sys, string
import argparse


def main():
    #version_msg = "%prog 2.0"                                                                                                                                
    #usage_msg = """%prog [OPTION]... FILE  Output randomly selected lines from FILE."""                                                                      
    parser = argparse.ArgumentParser(usage="""                                                                                                                
    shuf.py [OPTION]... [FILE]                                                                                                                                
    shuf.py -e [OPTION]... [ARG]...                                                                                                                           
    shuf.py -i lo-hi [OPTION]...
    
    Output random lines (repeating or unique) from a file, strings, integer values                                                                           
                                                                                                                                                             
    With no FILE, or when FILE is -, read standard input.                                                                                                    
                                                                                                                                                             
    Mandatory arguments to long options are mandatory for short options too.                                                                                 
      -e, --echo                treat each ARG as an input line                                                                                              
      -i, --input-range=LO-HI   treat each number LO through HI as an input line                                                                             
      -n, --head-count=COUNT    output at most COUNT lines                                                                                                   
      -r, --repeat              output lines can be repeated                                                                                                 
      --help        display this help and exit """)


    parser.add_argument("-e", "--echo", nargs="+", help="treat each ARG as an input line")
    parser.add_argument("-i", "--input-range", nargs=1, help="treat each number LO through HI as an input line")
    parser.add_argument("-n","--head-count", type=int, nargs=1, help="Output at most COUNT lines")
    parser.add_argument("-r", "--repeat", action="store_true",  help="Repeat output values (select with replacement).")
    parser.add_argument('filename', nargs='?', default='-', help='Input file name. Use "-" for standard input.')

    args = parser.parse_args()
    #print(args)                                                                                                                                             

    head = -1
    if(args.head_count):
        head = int(args.head_count[0])
    fileLines = []


    if args.echo:
        output = args.echo
        if (args.filename) and (args.filename != '-'):
            output.append(args.filename);

        if(args.repeat):
            #repeat echo for headcount number of times, or infinite                                                                                          
            if(args.head_count):
                for i in range(int(args.head_count[0])):
                    print(random.choice(output))
            else:
                while True:
                    print(random.choice(output))
        else:
            random.shuffle(output)
            if(args.head_count):
                head = (int(args.head_count[0]))
                if head > len(output):
                    head = len(output)

                for i in range(head):
                        print(output[i])
            else:
                print("\n".join(output))

    elif args.input_range:
        #print(args.input_range)                                                                                                                             
        if(args.filename != '-'):
            #print(args.filename)                                                                                                                            
            parser.error('extra operand '+ args.filename)

        else:
            try:
                output = args.input_range[0].split('-')
                #print(output)                                                                                                                               

                #output = [int(output[0]),                                                                                                                   
                low = int(output[0])
                high = int(output[1])

                if low > high:
                    raise ValueError('HI-LO is bad. Call an error')

                rangeArray = []
                for i in range (low, high + 1):
                    rangeArray.append(i)

                #check this is repeating - if repeat, ouptut random vals can repeat                                                                          
                # Could this have been a function? absolutely but oh well                                                                                    
                if(args.repeat):
                    #repeat randum nums for headcount number of times, or infinite                                                                           
                    if(args.head_count):
                        for i in range(int(args.head_count[0])):
                           print(random.choice(rangeArray))
                    else:
                        while True:
                            print(random.choice(rangeArray))
                else:
                    random.shuffle(rangeArray)
                    #print(rangeArray)                                                                                                                       
                    if args.head_count:
                        if head > len(rangeArray):
                            head = len(rangeArray)
                        for i in range(head):
                            print (rangeArray[i])
                    else:
                        for i in rangeArray:
                            print(i)

            except ValueError:
                parser.error('Invalid input range format. Use LO-HI.')
            except TypeError:
                 parser.error('Invalid arguments. Use -i LO-HI')


    elif args.filename == '-' and args.filename != sys.argv[0]:
       #checks for shuf.py - < test.txt                                                                                                                      
        fileLines = sys.stdin.readlines()
        #print(fileLines)                                                                                                                                    
    elif args.filename:
        #check for shuf.py test.txt                                                                                                                          
        try:
            with open(args.filename, 'r') as file:
                fileLines = file.readlines()
                #print(fileLines)                                                                                                                            
        except:
            parser.error("Please input a readable file")

    if len(fileLines) > 0:
        if args.repeat:
            if args.head_count:
                for i in range(int(args.head_count[0])):
                    print(random.choice(fileLines).strip())
            else:
                while True:
                    print(random.choice(fileLines).strip())
        elif args.head_count:
            if head > len(fileLines):
                head = len(fileLines)


            random.shuffle(fileLines)
            for i in range(head):print(fileLines[i].strip())
        else:
            random.shuffle(fileLines)
            for i in range(len(fileLines)):print(fileLines[i].strip())


if __name__ == "__main__":
    main()






