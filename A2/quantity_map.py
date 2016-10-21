#!/usr/bin/env python2.7
"""
quantity_map.py

Purpose: Mapper for aggregating driver stats data to day and hour for all drivers

This file is saved as quantity_map.py with execute permission
(chmod +x quantity_map.py)
"""

import sys



def main():
    """Take lines from stdin and emit a key:value pair where
    key := date,hour
    value := t_onduty,t_occupied,n_pass,n_trip,n_mile,earnings
    """
    for line in sys.stdin:
        line_data = line.strip().split('\t')
        key = ",".join(line_data[0:2])
        value = ",".join(line_data[3:])
        print(key + "\t" + value)

if __name__ == "__main__":
    main()
