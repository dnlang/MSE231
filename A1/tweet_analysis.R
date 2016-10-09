library(dplyr)
library(ggplot2)
library(scales)

options(stringsAsFactors = FALSE) # treat strings as strings not factors [1]
theme_set(theme_bw()) # set to a white ggplot theme

# Read in the data
nofilter_tweets_24h <- read.delim("~/GitRepos/MSE231/A1/snl_tweets.tsv")

# Take a look at the top of the file to check it
head(nofilter_tweets_24h)

# Create a constant to help us count the number of tweets in each date/time/timezone bin
nofilter_tweets_24h$counter = 1

# Group by the existing dataframe
nofilter_tweets_group = group_by(nofilter_tweets_24h, DATE, TIME, TIMEZONE)

# Summaroze the dataframe
binned_tweets = summarise(nofilter_tweets_group, tweet_vol=sum(counter))

# create a dattime variable and convert to POSIX for easy datetime plotting
binned_tweets$DATETIME = as.POSIXct(paste(binned_tweets$DATE, binned_tweets$TIME)) # [2]

# plot the data on a line plot
p = ggplot(binned_tweets, aes(x=DATETIME, y=tweet_vol, group=TIMEZONE)) +
  geom_point(aes(colour=TIMEZONE)) +
  geom_line(aes(colour=TIMEZONE)) + # factor by timezone
  theme(legend.justification = c(1, 1), legend.position = c(1, 1)) + # legend in topright [3]
  xlab("Time") + ylab("Tweet Volume") + ggtitle("Tweet Volume: SNL")

# add a vertical line to the plot at 20:30 (the premiere of SNL on the east coast)
snl_time_est = as.POSIXct(paste("2016-10-01", "20:30"))
snl_time_west = as.POSIXct(paste("2016-10-01", "23:30"))
p + geom_vline(xintercept = as.numeric(snl_time_est), linetype = "longdash", color="grey") + 
    geom_vline(xintercept = as.numeric(snl_time_west), linetype = "longdash", color="grey")


print(p) # show the plot [4]
ggsave(plot=p, file='no_filter.pdf', width=7, height=6)


#### REFERENCES ####
# [1] http://stackoverflow.com/questions/8177921/how-to-disable-stringsasfactors-true-in-data-frame-permanently
# [2] https://stat.ethz.ch/R-manual/R-devel/library/base/html/as.POSIXlt.html
# [3] http://stackoverflow.com/questions/10747307/legend-placement-ggplot-relative-to-plotting-region
# [4] http://stackoverflow.com/questions/26643852/ggplot-plots-in-scripts-do-not-display-in-rstudio