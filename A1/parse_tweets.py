from datetime import datetime, timedelta, time
import json
from pytz import timezone
import pytz
import sys
import time

start = time.time()

MONTHS = {"Sep":9, "Oct":10}
pacific = timezone('US/Pacific')
datefmt = '%Y-%m-%d'
timefmt = '%H:%M'

# create the output data file
f = open('snl_tweets.tsv', 'w')
f.write('DATE\tTIME\tTIMEZONE\n')

# function to round the time to a specific interval [5]
def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)

# read in the tweets using stdin [1] to parse
for line in sys.stdin:
    # load the JSON line [3]
    parsed_json = json.loads(line.rstrip()) # ignore a blank line [2]

    # parse the entries based on spec from Twitter API [4]
    try:
        # Only get US timezones
        timezone = parsed_json['user']['time_zone']
        if timezone == "Pacific Time (US & Canada)" or \
        timezone == "Mountain Time (US & Canada)" or \
        timezone == "Central Time (US & Canada)" or \
        timezone == "Eastern Time (US & Canada)":
            # all datatimes are in UTC and look like this "Thu Sep 29 05:26:28 +0000 2016"
            month = MONTHS[parsed_json['created_at'][4:7]] # get the month number from the dict
            day = parsed_json['created_at'][8:10]
            year = parsed_json['created_at'][26:]
            hour = parsed_json['created_at'][11:13]
            minute = parsed_json['created_at'][14:16]

            # create a datetime object
            dt = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
            dt = roundTime(dt, 60*15) # 15 min rounding
            dt = pytz.utc.localize(dt) # make the datetime aware it is UTC [7]

            # convert to Pacific Time [6]
            pac_dt = dt.astimezone(pacific)

            # create csv with [date  time   time_zone]
            tweet_time = pac_dt.date().strftime(datefmt) + '\t' \
            + pac_dt.time().strftime(timefmt) + '\t' \
            + timezone + '\n'

            # write the data to a tsv file
            f.write(tweet_time)

    except KeyError:
        # ignore entries that don't have a created_at date, mostly "deleted" entries
        pass

# close the file when done processing
f.close()
print('Tweets Processed in %.02f seconds!' % (time.time() - start))

####### REFERENCES #######
# [1] https://en.wikibooks.org/wiki/Python_Programming/Input_and_Output#Standard_File_Objects
# [2] http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
# [3] http://docs.python-guide.org/en/latest/scenarios/json/
# [4] https://dev.twitter.com/overview/api/tweets
# [5] http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python/10854034#10854034
# [6] http://pythonhosted.org//pytz/
# [7] http://stackoverflow.com/questions/7065164/how-to-make-an-unaware-datetime-timezone-aware-in-python
