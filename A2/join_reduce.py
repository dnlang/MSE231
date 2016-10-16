#!/usr/bin/env python2.7
"""
join_reduce.py

Purpose: Reducer to take a sorted list of trip and fare data lines and join them
into a single line of data with all unique data values.

This file is saved as join_reduce.py with execute permission
(chmod +x join_reduce.py)
"""

from itertools import groupby
from operator import itemgetter
import sys

"""
Trip data format [14 variables]

medallion, hack_license, vendor_id, rate_code, store_and_fwd_flag,
pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs,
trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude,
dropoff_latitude

Fare data format [11 variables]

medallion, hack_license, vendor_id, pickup_datetime, payment_type, fare_amount,
surcharge, mta_tax, tip_amount, tolls_amount, total_amount
"""

# Constants for data filtering. *_IDX indicates index in the data list
# trip constants
TRIPTIME      = 60
TRIPTIME_IDX  = 8
TRIP_DIST_IDX = 9
PICK_LONG_IDX = 10
PICK_LATT_IDX = 11
DROP_LONG_IDX = 12
DROP_LATT_IDX = 13

#fare constants
FARE_IDX         = 5
TOTAL_AMOUNT_IDX = 10


def read_mapper_output(lines):
    """Returns generator over each line of lines as a list split by tabs."""
    for line in lines:
        #print(line.rstrip().split('\t', 1))
        yield line.rstrip().split('\t', 1)

def main():
    """Take lines from stdin and join the trip and fare data lines.
       Do a JOIN, where `trip` is left and 'fare' is right
    """
    data = read_mapper_output(sys.stdin)
    for key, group in groupby(data, itemgetter(0)):
        # Figure out which line is the 'trip' and 'fare' data based on the data
        # length. Assign `trip` to LEFT and `fare` to RIGHT
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

        # Filter out data with obvious errors, print out clean data
        if left[0] == "medallion":
            print("\t".join(left + right[4:])) # print the header
        elif float(left[TRIP_DIST_IDX]) <= 0 or float(left[PICK_LATT_IDX]) == 0 \
        or float(left[PICK_LONG_IDX]) == 0 or float(left[DROP_LATT_IDX]) == 0 \
        or float(left[DROP_LONG_IDX]) == 0 or float(right[FARE_IDX] == 0) \
        or float(right[TOTAL_AMOUNT_IDX]) == 0:
            #print("pass")
            pass
        else:
            print("\t".join(left + right[4:]))

if __name__ == "__main__":
    main()
