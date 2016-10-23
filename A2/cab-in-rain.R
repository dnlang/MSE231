library("ggplot2")
library("dplyr")


########## Precipitation Data Notes #############
# N1: The subsequent data value will be for the hour ending at the time specified here. 
# Hour 00:00 will be listed as the first hour of each date, however since this data is by 
# definition an accumulation of the previous 60 minutes, it actually occurred on the previous day.

# N2: Hours with no precipitation are not shown.
################################################

# set the theme
theme_set(theme_bw())

# load the data
taxi <- read.delim("~/GitRepos/MSE231/A2/taxi-data/full_taxi_data.tsv", header=FALSE, stringsAsFactors=FALSE)
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

# make sure all the earnings are greater than 0
taxi_precip <- filter(taxi_precip, earnings > 0 & n_trip > 0 & t_occupied/t_onduty <= 1)

# create dataframe that looks like:
# date, hour, precip, drivers_onduty, drivers_occupied, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings
taxi_precip <- select(taxi_precip, date, hour, datetime, precip, drivers_onduty, drivers_occupied, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)

# create a boolean for rain or no rain
taxi_precip$rain <- ifelse(taxi_precip$precip > 0, 'rain', 'no rain')

# create a utilization variable
taxi_precip$utilization <- taxi_precip$t_occupied / taxi_precip$t_onduty

####### Boxplot comparing rain to no rain to drivers on duty #######
p <- ggplot(data=taxi_precip, aes(factor(rain), y=drivers_onduty)) +
  geom_boxplot()
print(p)

####### Boxplot comparing rain to no rain to earnings #######
p <- ggplot(data=taxi_precip, aes(factor(rain), y=earnings)) +
  geom_boxplot()
print(p)

####### Boxplot comparing occupied time rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(rain), y=t_occupied)) +
  geom_boxplot()
print(p)

####### Boxplot comparing trips rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(rain), y=n_trip)) +
  geom_boxplot()
print(p)

####### Boxplot comparing hourly time on duty rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(hour), y=drivers_onduty)) +
  geom_boxplot(aes(fill = rain))
print(p)

####### Boxplot comparing cab utilization rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(rain), y= utilization)) +
  geom_boxplot()
print(p)

####### Boxplot comparing hourly utilization rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(hour), y = utilization)) +
  geom_boxplot(aes(fill = rain), outlier.size = 0.5)
p <- p +  xlab("Hour") + ylab("Utilization")
ggsave(filename = "figures/utilization.pdf", plot = p, width = 7, height = 3)
print(p)

####### Boxplot comparing hourly utilization rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(hour), y = earnings)) +
  geom_boxplot(aes(fill = rain))
p <- p + ggtitle("Hourly Cab Earnings") + xlab("Hour") + ylab("Earnings [USD]")
print(p)

####### Boxplot comparing hourly earnings per driver rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(hour), y = earnings/drivers_onduty)) +
  geom_boxplot(aes(fill = rain))
p <- p + ggtitle("Hourly Cab Earnings per Driver") + xlab("Hour") + ylab("Earnings/Drivers]")
print(p)

####### Boxplot comparing hourly trips per driverrain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(hour), y = n_trip/drivers_onduty)) +
  geom_boxplot(aes(fill = rain))
p <- p + ggtitle("Hourly Trips per Driver") + xlab("Hour") + ylab("Trips/Driver]")
print(p)

####### Boxplot comparing time on duty per driver rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(hour), y = t_onduty/drivers_onduty)) +
  geom_boxplot(aes(fill = rain))
p <- p + ggtitle("Time on duty per Driver") + xlab("Hour") + ylab("Time on duty / Driver]")
print(p)

####### Boxplot comparing earnings per minute rain to no rain #######
p <- ggplot(data=taxi_precip, aes(factor(hour), y = earnings/t_onduty)) +
  geom_boxplot(aes(fill = rain))
p <- p + ggtitle("Earnings") + xlab("Hour") + ylab("$/min")
print(p)

# Computer average hourly earnings
hourly_earnings <- summarise(group_by(taxi_precip, hour, rain), avg_earnings = mean(earnings/drivers_onduty))

####### line plot comparing time on duty per driver rain to no rain #######
p <- ggplot(data=hourly_earnings, aes(x = hour, y = avg_earnings)) +
  geom_line(aes(color = rain)) + geom_point(aes(color = rain))
p <- p + xlab("Hour") + ylab("Avg earnings/driver [USD]") +
  theme(legend.justification = c(1, 1), legend.position = c(1, .5)) # legend in topright [3]
ggsave(filename = "figures/avg_earnings.pdf", plot = p, width = 7, height = 3)
print(p)
