#!/usr/bin/env python2.7
"""
join_reduce.py

Purpose: Reducer to take a sorted list of trip and fare data lines and join them
into a single line of data with all unique data values.

This file is saved as join_reduce.py with execute permission
(chmod +x join_reduce.py)
"""
from datetime import datetime
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
PICKUP_TIME_IDX = 5
DROPOFF_TIME_IDX = 6
TRIPTIME_IDX  = 8
TRIP_DIST_IDX = 9
PICK_LONG_IDX = 10
PICK_LATT_IDX = 11
DROP_LONG_IDX = 12
DROP_LATT_IDX = 13

#fare constants
FARE_IDX         = 5
TOTAL_AMOUNT_IDX = 10

FORMAT = "%Y-%m-%d %H:%M:%S"

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
        left = []
        right = []
        for key, ride_data in group:
            ride_data_list = ride_data.strip().split(",")
            if len(ride_data_list) == 14: # trip data
                left = ride_data_list
                # if we can't create a good datetime object, get rid of the data
                try:
                    dropoff_time = datetime.strptime(left[DROPOFF_TIME_IDX], FORMAT)
                    pickup_time = datetime.strptime(left[PICKUP_TIME_IDX], FORMAT)
                except:
                    left = []
            elif len(ride_data_list) == 11:
                right = ride_data_list
            else:
                pass


        # Make sure there are two data lines and get ride of the header
        if left == [] or right == [] or left[0] == "medallion":
            pass

        # filter out obvious errors: trips too short or long, bad GPS data,
        # no fare, trips over 2 hours (7200 sec) or under 10 seconds
        # Similar filters as [1]
        elif float(left[TRIP_DIST_IDX]) <= 0.001 \
        or float(left[TRIP_DIST_IDX]) >= 50 \
        or float(left[PICK_LATT_IDX]) == 0 \
        or float(left[PICK_LONG_IDX]) == 0 \
        or float(left[DROP_LATT_IDX]) == 0 \
        or float(left[DROP_LONG_IDX]) == 0 \
        or float(right[FARE_IDX] == 0) \
        or float(right[TOTAL_AMOUNT_IDX]) == 0 \
        or (dropoff_time - pickup_time).total_seconds() >= 7200 \
        or (dropoff_time - pickup_time).total_seconds() < 10:
            pass

        else:
            print("\t".join(left + right[4:]))

if __name__ == "__main__":
    main()

# REFERENCES
# [1] https://github.com/Lab-Work/gpsresilience/blob/7c5183092013d44ce6d295469880502407c0e4ac/trip.py
