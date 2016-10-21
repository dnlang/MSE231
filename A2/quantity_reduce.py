#!/usr/bin/env python2.7
"""
quantity_reduce.py

Purpose: Reducer to compute the aggregate data for all drivers at each hour of
everyday

This file is saved as quantity_reduce.py with execute permission
(chmod +x quantity_reduce.py)
"""

from itertools import groupby
from operator import itemgetter
import sys

# CONSTANTS
T_ON_IDX = 0
T_OCC_IDX = 1
PASSENGER_IDX = 2
TRIP_IDX = 3
MILE_IDX = 4
EARNINGS_IDX = 5

def read_mapper_output(lines):
    """Returns generator over each line of lines as a list split by tabs."""
    for line in lines:
        yield line.rstrip().split('\t', 1)


def main():
    """Take lines from stdin and print the sum in each group of words."""
    data = read_mapper_output(sys.stdin)
    for key, group in groupby(data, itemgetter(0)):
        # date, hour, drivers_onduty, drivers_occupied, t_onduty, t_occupied,
        # n_pass, n_trip, n_mile, earnings
        # initialize our aggreagators
        drivers_onduty, drivers_occupied, t_onduty, t_occupied, n_pass, n_trip,\
        n_mile, earnings = 0,0,0,0,0,0,0,0
        for ride in group:
            ride_data = ride[1].strip().split(",")

            # check if driver on duty > 1 min
            if float(ride_data[T_ON_IDX]) >= 1:
                drivers_onduty += 1
            # check if driver occupied
            if float(ride_data[T_OCC_IDX]) >= 1:
                drivers_occupied += 1
            # aggregate other variables across all drivers during the hour
            t_onduty += float(ride_data[T_ON_IDX])
            t_occupied += float(ride_data[T_OCC_IDX])
            n_pass += int(ride_data[PASSENGER_IDX])
            n_trip += int(ride_data[TRIP_IDX])
            n_mile += float(ride_data[MILE_IDX])
            earnings += float(ride_data[EARNINGS_IDX])

        # print our output line
        key_val = key.strip().split(",")
        print("\t".join([key_val[0], key_val[1], str(drivers_onduty), \
        str(drivers_occupied), str(t_onduty), \
        str(t_occupied), str(n_pass), str(n_trip), str(n_mile), str(earnings)]))

        #print("\n")

if __name__ == "__main__":
    main()
