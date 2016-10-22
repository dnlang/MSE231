#!/usr/bin/env python2.7
"""
join_map.py

Purpose: Mapper for data join via map-reduce.

This file is saved as join_mapper.py with execute permission
(chmod +x join_map.py)"""

import sys


def main():
    """Take lines from stdin and emit a key:value pair where
    key := medalion,hack,starttime
    value := line
    """
    for line in sys.stdin:
        key = ""
        line_data = line.strip().split(',')
        if len(line_data) == 14: # trip data
            key = ",".join([line_data[0],line_data[1],line_data[5]])
        elif len(line_data) == 11: # fare data
            key = ",".join([line_data[0],line_data[1],line_data[3]])
        else:
            key = "NA" # this get checked and thrown out in the

        # get rid of the header, then map the data
        # if the first character is not an interger, get rid of the data
        if key[0].isdigit():
            print(key + "\t" + line.strip())
        else:
            pass

if __name__ == "__main__":
    main()

# REFERENCES
# [1] - http://stackoverflow.com/questions/44778/how-would-you-make-a-comma-separated-string-from-a-list
