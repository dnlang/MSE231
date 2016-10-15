#!/usr/bin/env python2
"""Example reducer module for counting words via map-reduce.

This file is saved as wc_reducer.py with execute permission
(chmod +x wc_reducer.py)"""

from itertools import groupby
from operator import itemgetter
import sys


def read_mapper_output(lines):
    """Returns generator over each line of lines as a list split by tabs."""
    for line in lines:
        #print(line.rstrip().split('\t', 1))
        yield line.rstrip().split('\t', 1)


def main():
    """Take lines from stdin and print the sum in each group of words."""
    data = read_mapper_output(sys.stdin)
    for key, group in groupby(data, itemgetter(0)):
        data_line1 = next(group)[1].strip().split(",")
        if len(data_line1) == 14: # trip data
            left = data_line1
        elif len(data_line1) == 11:
            right = data_line1
        else:
            pass

        data_line2 = next(group)[1].strip().split(",")
        if len(data_line2) == 11:
            right = data_line2
        elif len(data_line2) == 14:
            left = data_line2
        else:
            pass

        print("\t".join(left + right[4:]))

if __name__ == "__main__":
    main()
