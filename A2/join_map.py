#!/usr/bin/env python2.7
"""
join_map.py

Purpose: Mapper for data join via map-reduce.

This file is saved as join_mapper.py with execute permission
(chmod +x join_mapper.py)"""

import sys


def main():
    """Take lines from stdin and emit a key:value pair where
    key := medalion,hack,starttime
    value := line
    """
    for line in sys.stdin:
        line_data = line.strip().split(',')
        if len(line_data) == 14: # trip data
            key = ",".join([line_data[0],line_data[1],line_data[5]])
        elif len(line_data) == 11: # fare data
            key = ",".join([line_data[0],line_data[1],line_data[3]])

        print(key + "\t" + line.strip())

if __name__ == "__main__":
    main()

# REFERENCES
# [1] - http://stackoverflow.com/questions/44778/how-would-you-make-a-comma-separated-string-from-a-list
