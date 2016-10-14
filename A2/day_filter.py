#!/usr/bin/env python2.7

"""
day_filter.py

Purpose: Filter and return on teh data from a single day in January. For this
script, we will do Janurary 1

Usage: cat <data_file> | python day_filter.py

Authors:
David Lang
Nikolas Martelaro
Tres Pittman
"""

import sys

filter_day = "2013-01-01" # Jan 1

for line in sys.stdin:
    # print the header
    if "medallion" in line:
        print(line.strip())
    # print lines with the correct filter date
    if filter_day in line:
        print(line.strip())
