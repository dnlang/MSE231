#!/usr/bin/env python2.7
"""
driver_stats_reduce.py

Purpose: Reducer to calcluate stats for each driver based on the day and the
hour. Stats include:

t_onduty: the total amount of time (in units of hours) that the driver is
on-duty during the hour. There is not a perfect way to infer this from the data,
but we will assume that if a cab is unoccupied for at least 30 minutes,
then the driver is not on duty (e.g., the driver is taking a break or is between
shifts) during that unoccupied stretch.

t_occupied: the total amount of time with passengers in the cab during the hour.

n_pass: the total number of passengers picked up during the hour.

n_trip: the total number of trips started during the hour.

n_mile: the total number of miles traveled with passengers in the hour.
For trips that cross an hour boundary, assume the driver traveled at a
constant speed for the duration of the trip.

earnings: the total amount of money the driver earned in that hour. As with
millage, for trips that cross an hour boundary, assume drivers earn the final
payment at a constant rate throughout the trip. Earnings consist of the fare
plus the tip. Unfortunately, cash tips are not recorded in the data, so this
will underestimate total earnings.

This file is saved as driver_stats_reduce.py with execute permission
(chmod +x driver_stats_reduce.py)"""

from itertools import groupby
from operator import itemgetter
from datetime import datetime
import sys

# CONSTANTS
PICKUP_TIME_IDX = 5
DROPOFF_TIME_IDV = 6
NUM_PASS = 7    # passenger_count index
AMOUNT_IDX = 20 # total cost for ride

FORMAT = "%Y-%m-%d %H:%M:%S"


def read_mapper_output(lines):
    """Returns generator over each line of lines as a list split by tabs."""
    for line in lines:
        #print(line.rstrip().split('\t', 1))
        yield line.rstrip().split('\t', 1)

def compute_times(time_list):
    """Returns the time on duty and the time driving passengers"""
    t_occupied, rollover = 0, 0
    for pickup,dropoff in time_list:
        p_time = datetime.strptime(pickup, FORMAT)
        d_time = datetime.strptime(dropoff, FORMAT)

        # compute time within the hour, return time and remainder if it rolls
        # over the hour boundary. The dropoff hour is always bigger than the
        # pickup hour EXCEPT if the day rolls over! Still, it is the same
        # calculation since all the time differences are datetime object. The
        # day rollover will take care of iteself
        if d_time.hour > p_time.hour or d_time.hour < p_time.hour:
            rollover = d_time.minute
            t_occupied += (d_time - p_time).total_seconds() / 60.0 - rollover
            print("rollover = " +  str(rollover))
        else:
            t_occupied += (d_time - p_time).total_seconds() / 60.0
    return t_occupied, rollover


def main():
    """Take lines from stdin and print the sum in each group of words."""
    data = read_mapper_output(sys.stdin)
    last_hack = ""  # keep track of what driver we are on so we can reset our
                    # aggregators when we change driver_stats_reduce
    t_occupied, n_pass, n_trip, earnings = 0, 0, 0, 0 # setup our aggragators

    # create groups based on hack,day,hour key
    for key, group in groupby(data, itemgetter(0)):

        # reset the aggregator if we switch drivers
        if(key.split(",")[0]) != last_hack:
            t_occupied, n_pass, n_trip, earnings = 0, 0, 0, 0
            print("reset driver")

        # compute the stats for the data in each group
        times = []
        print("t_occupied = " + str(t_occupied) + ", n_pass = " + str(n_pass) \
        + ", n_trip = " + str(n_trip) + ", earnings = " + str(earnings))
        for key, ride_data in group:
            ride = ride_data.strip().split(",")
            times.append(ride[PICKUP_TIME_IDX:DROPOFF_TIME_IDV+1])
            n_pass += int(ride[7])
            n_trip += 1
            earnings += float(ride[AMOUNT_IDX])
            print(ride_data)
        t_occupied_calc, t_occupied_roll = compute_times(times)
        t_occupied += t_occupied_calc # add this hour's calc to the initial time

        print("t_occupied = " + str(t_occupied) + ", n_pass = " + str(n_pass) \
        + ", n_trip = " + str(n_trip) + ", earnings = " + str(earnings))
        print("\n")

        # set the initial values for the next hour to the rollover values
        # calculated from trips that cross the hour border
        t_occupied, n_pass, n_trip, earnings = t_occupied_roll, 0, 0, 0
        last_hack = key.split(",")[0]   # save our current drive to check for a
                                        # change in the next loop iteration

        #n_pass = sum([int(data[7]) for _, data in group])
        #print(str(n_pass))
        #print word + '\t' + str(total_count)

if __name__ == "__main__":
    main()
