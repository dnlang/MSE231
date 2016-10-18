#!/usr/bin/env python2.7
"""
driver_stats_map.py

Purpose: Mapper for driver stats in NY Taxi dataset.

This file is saved as driver_stats_map.py with execute permission
(chmod +x driver_stats_map.py)"""

import sys

# CONSTANTS
HACK_IDX = 1
PICKUP_TIME_IDX = 5

def main():
    """Take lines from stdin and emit a key:value pair where
    key := hack,day,hour
    value := line

    Data input is formated as:
    medallion\thack_license\tvendor_id\trate_code\tstore_and_fwd_flag\tpickup_datetime\tdropoff_datetime\tpassenger_count\ttrip_time_in_secs\t
    trip_distance\tpickup_longitude\tpickup_latitude\tdropoff_longitude\tdropoff_latitude\tpayment_type\tfare_amount\tsurcharge\tmta_tax\ttip_amount
    tolls_amount\ttotal_amount
    """
    for line in sys.stdin:
        line_data = line.strip().split('\t')
        pickup_time = line_data[PICKUP_TIME_IDX].split(" ") # split on the space to seperate the date and time
        day = pickup_time[0]
        hour = pickup_time[1][0:2] # hour is the first two numbers i.e. 12:00:00

        key = ",".join([line_data[HACK_IDX], day, hour])
        value = ",".join(line_data)

        # dont add the header
        if "hack_license" in key:
            pass
        else:
            print(key + "\t" + value)

if __name__ == "__main__":
    main()

# REFERENCES
