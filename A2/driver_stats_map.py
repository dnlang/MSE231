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
PASSENGER_IDX = 7
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
        #print(earnings_rate*(d_time - p_time).total_seconds())

        # find the hour borders (more than is up to 24:00, less than if across 24:00)
        if p_time.hour != d_time.hour:
            # spanning over 2 hour blocks
            if d_time.hour > p_time.hour + 1 and float(line_data[FARE_IDX]) < 20:
                # this doesn't really make sense for such a long ride
                pass
            # catch the drives over 3 hours blocks
            elif (d_time.hour == p_time.hour + 2):
                    #print(line_data)
                    # print the data for the first hour, make sure to not that this is the pickup
                    time_break = datetime(p_time.year, p_time.month, p_time.day, p_time.hour, 59, 59)
                    distance = (time_break - p_time).total_seconds() * speed
                    earnings = (time_break - p_time).total_seconds() * earnings_rate

                    # create the key and value
                    key = ",".join([line_data[HACK_IDX], datetime.strftime(p_time, DATE), str(p_time.hour)])

                    # value is [pickup, end_of_hour, num_passengers, distance, earnings, start = 1]
                    value = ",".join([datetime.strftime(p_time, FORMAT), \
                    datetime.strftime(time_break, FORMAT), line_data[PASSENGER_IDX], \
                    str(distance), str(earnings), '1'])

                    print(key + "\t" + value)

                    # print the data for the second FULL hour (60 min, 3600 sec)
                    if p_time.hour + 1 == 24: # check if you go over by a day
                        key = ",".join([line_data[HACK_IDX], datetime.strftime(d_time, DATE), '0'])
                        t1 = datetime(d_time.year, d_time.month, d_time.day, 0, 0, 0)
                        t2 = datetime(d_time.year, d_time.month, d_time.day, 0, 59, 59)
                        distance = 3600 * speed
                        earnings = 3600 * earnings_rate

                        # value is [pickup, end_of_hour, num_passengers, distance, earnings, start = 0]
                        value = ",".join([datetime.strftime(t1, FORMAT), \
                        datetime.strftime(t2, FORMAT), '0', \
                        str(distance), str(earnings), '0'])
                    else:
                        key = ",".join([line_data[HACK_IDX], datetime.strftime(d_time, DATE), str(p_time.hour+1)])
                        t1 = datetime(d_time.year, d_time.month, d_time.day, p_time.hour+1, 0, 0)
                        t2 = datetime(d_time.year, d_time.month, d_time.day, p_time.hour+1, 59, 59)
                        distance = 3600 * speed
                        earnings = 3600 * earnings_rate

                        # value is [pickup, end_of_hour, num_passengers, distance, earnings, start = 0]
                        value = ",".join([datetime.strftime(t1, FORMAT), \
                        datetime.strftime(t2, FORMAT), '0', \
                        str(distance), str(earnings), '0'])

                    print(key + "\t" + value)

                    # print the remainder of the time for the next hour, without a pickup starttime
                    # note the d_time.hour! that lets us use this in the calculations for the next time
                    # block, but make sure that num_passengers = 0 and start = 0
                    # so we don;t count as a run that started in the next hour, prevents double counting
                    key = ",".join([line_data[HACK_IDX], datetime.strftime(d_time, DATE), str(d_time.hour)])
                    time_break = datetime(d_time.year, d_time.month, d_time.day, d_time.hour, 0, 0)
                    distance = (d_time - time_break).total_seconds() * speed
                    earnings = (d_time - time_break).total_seconds() * earnings_rate

                    # value is [pickup, end_of_hour, num_passengers, distance, earnings, start = 0]
                    value = ",".join([datetime.strftime(time_break, FORMAT), \
                    datetime.strftime(d_time, FORMAT), '0', \
                    str(distance), str(earnings), '0'])

                    print(key + "\t" + value)

            # ride crossing 1 hour boundary forward (ex 10:50:00 -> 11:02:00)
            elif (d_time.hour == p_time.hour + 1) or (d_time.hour == 0 and p_time.hour == 23): # break over one hour
                # print(line_data)
                # # print the data for the first hour, make sure to not that this is the pickup
                time_break = datetime(p_time.year, p_time.month, p_time.day, p_time.hour, 59, 59)
                distance = (time_break - p_time).total_seconds() * speed
                earnings = (time_break - p_time).total_seconds() * earnings_rate

                # create the key and value
                key = ",".join([line_data[HACK_IDX], datetime.strftime(p_time, DATE), str(p_time.hour)])

                # value is [pickup, end_of_hour, num_passengers, distance, earnings, start = 1]
                value = ",".join([datetime.strftime(p_time, FORMAT), \
                datetime.strftime(time_break, FORMAT), line_data[PASSENGER_IDX], \
                str(distance), str(earnings), '1'])

                print(key + "\t" + value)

                # print the remainder of the time for the next hour, without a pickup starttime
                # note the d_time.hour! that lets us use this in the calculations for the next time
                # block, but make sure that num_passengers = 0 and start = 0
                # so we don;t count as a run that started in the next hour, prevents double counting
                key = ",".join([line_data[HACK_IDX], datetime.strftime(d_time, DATE), str(d_time.hour)])
                time_break = datetime(d_time.year, d_time.month, d_time.day, d_time.hour, 0, 0)
                distance = (d_time - time_break).total_seconds() * speed
                earnings = (d_time - time_break).total_seconds() * earnings_rate

                # value is [pickup, end_of_hour, num_passengers, distance, earnings, start = 0]
                value = ",".join([datetime.strftime(time_break, FORMAT), \
                datetime.strftime(d_time, FORMAT), '0', \
                str(distance), str(earnings), '0'])

                print(key + "\t" + value)

        # print one line of data for ride taht fall within the hour
        else:
            #print(line_data)
            key = ",".join([line_data[HACK_IDX], datetime.strftime(p_time, DATE), str(p_time.hour)])
            # value is [pickup, end_of_hour, num_passengers, distance, earnings, start = 1]
            value = ",".join([datetime.strftime(p_time, FORMAT), \
            datetime.strftime(d_time, FORMAT), line_data[PASSENGER_IDX], \
            line_data[TRIP_DIST_IDX], line_data[FARE_IDX], '1'])
            print(key + "\t" + value)


if __name__ == "__main__":
    main()

# REFERENCES
