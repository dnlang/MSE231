############################################################################
# tweet_analysis.R
#
# MSE 231 - Assignment 1
#
# David Lang
# Nikolas Martelaro
# Tres Pittman
#
############################################################################

library(dplyr)
library(ggplot2)
library(scales)

options(stringsAsFactors = FALSE) # treat strings as strings not factors [1]
theme_set(theme_bw()) # set to a white ggplot theme

# set the working directory to directory with this script [5]
script.dir <- dirname(sys.frame(1)$ofile)
setwd(script.dir)

# Read in the data
nofilter_tweets_24h <- read.delim("nofilter_tweets_24h.tsv")
snl_tweets_24h <- read.delim("snl_tweets.tsv")

# Take a look at the top of the file to check it
head(nofilter_tweets_24h)

# Create a constant to help us count the number of tweets in each date/time/timezone bin
nofilter_tweets_24h$counter <-  1
snl_tweets_24h$counter <-  1

# Group the data by date time and timezone, then count the number of tweets in each group
binned_tweets <- nofilter_tweets_24h %>%
  group_by(DATE, TIME, TIMEZONE) %>% 
  summarise(tweet_vol=sum(counter))

binned_snl <- snl_tweets_24h %>%
  group_by(DATE, TIME, TIMEZONE) %>% 
  summarise(tweet_vol=sum(counter))

# create a dattime variable and convert to POSIX for easy datetime plotting
binned_tweets$DATETIME <-  as.POSIXct(paste(binned_tweets$DATE, binned_tweets$TIME)) # [2]
binned_snl$DATETIME <-  as.POSIXct(paste(binned_snl$DATE, binned_snl$TIME))

############## NO FILTER PLOT ################
p <-  ggplot(binned_tweets, aes(x=DATETIME, y=tweet_vol, group=TIMEZONE)) +
  geom_point(aes(colour=TIMEZONE)) +
  geom_line(aes(colour=TIMEZONE)) + # factor by timezone
  theme(legend.justification = c(1, 1), legend.position = c(1, 1)) + # legend in topright [3]
  xlab("Time") + ylab("Tweet Volume") + ggtitle("Tweet Volume: No Filter")

print(p) # show the plot [4], then save it
ggsave(plot=p, file='nofilter24.pdf', width=7, height=6)

############## SNL PLOT ################
# plot the SNL data on a line plot
p_snl <-  ggplot(binned_snl, aes(x=DATETIME, y=tweet_vol, group=TIMEZONE)) +
  geom_point(aes(colour=TIMEZONE)) +
  geom_line(aes(colour=TIMEZONE)) + # factor by timezone
  theme(legend.justification = c(1, 1), legend.position = c(1, 1)) + # legend in topright [3]
  xlab("Time") + ylab("Tweet Volume") + ggtitle("Tweet Volume: SNL")

# add a vertical line to the plot at 20:30 and 23:30 (the premiere of SNL on the east and west coast)
snl_time_est <-  as.POSIXct(paste("2016-10-01", "20:30"))
snl_time_west <-  as.POSIXct(paste("2016-10-01", "23:30"))
p_snl <-  p_snl + geom_vline(xintercept = as.numeric(snl_time_est), linetype = "longdash", color="grey") + 
    geom_vline(xintercept = as.numeric(snl_time_west), linetype = "longdash", color="grey")

print(p_snl) # show the plot [4], then save it
ggsave(plot=p_snl, file='snl24.pdf', width=7, height=6)


#### REFERENCES ####
# [1] http://stackoverflow.com/questions/8177921/how-to-disable-stringsasfactors-true-in-data-frame-permanently
# [2] https://stat.ethz.ch/R-manual/R-devel/library/base/html/as.POSIXlt.html
# [3] http://stackoverflow.com/questions/10747307/legend-placement-ggplot-relative-to-plotting-region
# [4] http://stackoverflow.com/questions/26643852/ggplot-plots-in-scripts-do-not-display-in-rstudio
# [5] http://stackoverflow.com/questions/13672720/r-command-for-setting-working-directory-to-source-file-location