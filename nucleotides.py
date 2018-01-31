#!/usr/bin/env python
"""
https://www.biostars.org/p/296086/
returns only lines in .csv file where all nucleotides on the line are NOT the same
"""
import sys
input_file = "nucleotides.csv"
with open(input_file) as f:
    for line in f:
        parts = [x for x in line.strip().split(',') if x != '']
        all_equal = all( x == parts[0] for x in parts)
        if not all_equal and len(parts) > 0:
            sys.stdout.write(line)
