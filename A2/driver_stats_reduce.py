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

output should be:
date, hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings

This file is saved as driver_stats_reduce.py with execute permission
(chmod +x driver_stats_reduce.py)"""

from itertools import groupby
from operator import itemgetter
from datetime import datetime
import sys

# CONSTANTS
PICKUP_TIME_IDX = 0
DROPOFF_TIME_IDV = 1
NUM_PASS = 2        # passenger_count index
DIST_IDX = 3
AMOUNT_IDX = 4      # total cost for ride
RIDE_START_IDX = 5  # ride started in the hour

HACK_IDX = 0
DAY_IDX = 1
HOUR_IDX = 2


FORMAT = "%Y-%m-%d %H:%M:%S"


def read_mapper_output(lines):
    """Returns generator over each line of lines as a list split by tabs."""
    for line in lines:
        #print(line.rstrip().split('\t', 1))
        yield line.rstrip().split('\t', 1)

def compute_times(time_list):
    """Returns the time on duty and the time driving passengers"""
    t_occupied = 0
    t_onduty = 60 #assume on duty for the hour

    # compute the t_occupied (time with passengers)
    for pickup,dropoff in time_list:
        p_time = datetime.strptime(pickup, FORMAT)
        d_time = datetime.strptime(dropoff, FORMAT)

        t_occupied += (d_time - p_time).total_seconds() / 60.0

    # compute t_onduty
    # if only 1 ride, check is shorter than 30 min
    if len(time_list) == 1:
        p_time = datetime.strptime(time_list[0][0], FORMAT)
        d_time = datetime.strptime(time_list[0][1], FORMAT)
        if p_time.minute < 30 and d_time.minute > 30:
            pass # on duty for the entire hour
        elif d_time.minute < 30:
            t_onduty = d_time.minute
        elif p_time.minute > 30:
            t_onduty = 60 - p_time.minute
    else:
        # calculate off duty time as the time inbetween drives
        for i in range(0,len(time_list)-1):
            p_time = datetime.strptime(time_list[i+1][0], FORMAT)
            d_time = datetime.strptime(time_list[i][1], FORMAT)

            # if the time between drive is greater than 30 minutes
            if (p_time - d_time).total_seconds() > (1800):
                t_onduty -= (p_time - d_time).total_seconds()/60

    return t_occupied, t_onduty


def main():
    """Take lines from stdin and print the sum in each group of words."""
    data = read_mapper_output(sys.stdin)
    #last_hack = ""  # keep track of what driver we are on so we can reset our
                    # aggregators when we change driver_stats_reduce

    # create groups based on hack,day,hour key
    for key, group in groupby(data, itemgetter(0)):
        t_occupied, n_pass, n_trip, n_mile, earnings = 0, 0, 0, 0, 0 # setup our aggragators
        times = []

        # compute the stats for the data in each group
        for key, ride_data in group:
            ride = ride_data.strip().split(",")
            times.append(ride[PICKUP_TIME_IDX:DROPOFF_TIME_IDV+1])
            n_pass += int(ride[NUM_PASS])
            n_trip += int(ride[RIDE_START_IDX])
            n_mile += float(ride[DIST_IDX])
            earnings += float(ride[AMOUNT_IDX])
            #print(ride_data)
        t_occupied, t_onduty = compute_times(times)

        # date, hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings
        key_val = key.strip().split(",")
        print("\t".join([key_val[DAY_IDX], key_val[HOUR_IDX], key_val[HACK_IDX], \
        str(t_onduty), str(t_occupied), str(n_pass), str(n_trip), str(n_mile), str(earnings)]))
        #print("" "t_occupied = " + str(t_occupied) + ", n_pass = " + str(n_pass) \
        # + ", n_trip = " + str(n_trip) + ", n_mile = " + str(n_mile) + \
        # ", earnings = " + str(earnings))
        #print("\n")

        # # set the initial values for the next hour to the rollover values
        # # calculated from trips that cross the hour border
        # t_occupied, n_pass, n_trip, earnings = t_occupied_roll, 0, 0, 0
        # last_hack = key.split(",")[0]   # save our current drive to check for a
        #                                 # change in the next loop iteration

        #n_pass = sum([int(data[7]) for _, data in group])
        #print(str(n_pass))
        #print word + '\t' + str(total_count)

if __name__ == "__main__":
    main()
