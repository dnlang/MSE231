#!/usr/bin/env python2.7
"""
driver_stats_map.py

Purpose: Mapper for driver stats in NY Taxi dataset.

This file is saved as driver_stats_map.py with execute permission
(chmod +x driver_stats_map.py)"""

import sys
from datetime import datetime

# CONSTANTS
HACK_IDX = 1
PICKUP_TIME_IDX = 5
DROPOFF_TIME_IDX = 6
TRIP_DIST_IDX = 9
FARE_IDX = 20

FORMAT = "%Y-%m-%d %H:%M:%S"
DATE = "%Y-%m-%d"

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
        pickup = line_data[PICKUP_TIME_IDX]
        dropoff = line_data[DROPOFF_TIME_IDX]
        p_time = datetime.strptime(pickup, FORMAT)
        d_time = datetime.strptime(dropoff, FORMAT)
        speed = float(line_data[TRIP_DIST_IDX]) / (d_time - p_time).total_seconds()
        earnings_rate = float(line_data[FARE_IDX]) / (d_time - p_time).total_seconds()
        print(earnings_rate*(d_time - p_time).total_seconds())

        # find the hour borders (more than is up to 24:00, less than if across 24:00)
        if d_time.hour > p_time.hour or d_time.hour < p_time.hour:
            # spanning over 2 hour blocks
            if d_time.hour > p_time.hour + 1 and float(line_data[FARE_IDX]) < 20:
                # this doesn't really make sense for such a long ride
                pass
                #print(line_data)
                #print(line_data[FARE_IDX])
        else:
            pass
            # key = ",".join([line_data[HACK_IDX], datetime.strftime(p_time, DATE), str(p_time.hour)])
            # value = ",".join(line_data)
            # print(key + "\t" + value)

        # pickup_time = pickup.split(" ") # split on the space to seperate the date and time
        # dropoff_time = dropoff.split(" ")
        # pick_day = pickup_time[0]
        # pick_hour = pickup_time[1][0:2] # hour is the first two numbers i.e. 12:00:00
        #
        #
        # # find the drives that go over an hour boundary and split them into 2 lines
        #
        #
        # key = ",".join([line_data[HACK_IDX], day, hour])
        # value = ",".join(line_data)
        #
        # # dont add the header
        # if "hack_license" in key:
        #     pass
        # else:
        #     print(key + "\t" + value)

if __name__ == "__main__":
    main()

# REFERENCES
