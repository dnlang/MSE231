library("ggplot2")
library("dplyr")


########## Precipitation Data Notes #############
# N1: The subsequent data value will be for the hour ending at the time specified here. 
# Hour 00:00 will be listed as the first hour of each date, however since this data is by 
# definition an accumulation of the previous 60 minutes, it actually occurred on the previous day.

# N2: Hours with no precipitation are not shown.
################################################


# load the data
taxi <- read.delim("~/GitRepos/MSE231/A2/sample-data/taxi_sample.tsv", header=FALSE, stringsAsFactors=FALSE)
nyc_precipitation <- read.csv("~/GitRepos/MSE231/A2/nyc_precipitation.csv", stringsAsFactors=FALSE)


# create names for the taxi data
names(taxi) <- c('date', 'hour', 'drivers_onduty', 'drivers_occupied', 't_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings') 

# create a datetime object that we can work with for the join
taxi <- mutate(taxi, year=substr(date, 1, 4))
taxi <- mutate(taxi, month=substr(date, 6, 7))
taxi <- mutate(taxi, day=substr(date, 9, 10))
taxi$datetime <- ISOdatetime(taxi$year, taxi$month, taxi$day, taxi$hour, 0, 0)


# create a datetime object for the rain data
nyc_precipitation <- mutate(nyc_precipitation, year=substr(DATE, 1, 4))
nyc_precipitation <- mutate(nyc_precipitation, month=substr(DATE, 5, 6))
nyc_precipitation <- mutate(nyc_precipitation, day=substr(DATE, 7, 8))
nyc_precipitation <- mutate(nyc_precipitation, hour=substr(DATE, 10, 11))

# Create precipitation dateime, subtract 1 hours to align with the taxi data (See note N1 above)
nyc_precipitation$datetime <- ISOdatetime(nyc_precipitation$year, nyc_precipitation$month, nyc_precipitation$day, nyc_precipitation$hour, 0, 0) - 3600

# Drop the data we don't care about in the precipitation data HCPC and datetime
nyc_precipitation <- nyc_precipitation[, c(4,9)]

# JOIN the data sets
taxi_precip <- left_join(taxi, nyc_precipitation, by = "datetime")

# replace NA's in the data (means no precipitation) with 0's
taxi_precip$precip <- ifelse(is.na(taxi_precip$HPCP), 0, taxi_precip$HPCP)

# create dataframe that looks like:
# date, hour, precip, drivers_onduty, drivers_occupied, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings
taxi_precip <- select(taxi_precip, datetime, precip, drivers_onduty, drivers_occupied, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)
