library(dplyr)
library(ggplot2)
library(scales)

options(stringsAsFactors = FALSE) # treat strings as strings not factors
theme_set(theme_bw()) # set to a white ggplot theme

# Read in the data
nofilter_tweets_24h <- read.delim("~/GitRepos/MSE231/A1/nofilter_tweets_24h.tsv")

# Take a look at the top of the file to check it
head(nofilter_tweets_24h)

# Create a constant to help us count the number of tweets in each dat/time/timezone bin
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
  xlab("Time") + ylab("Tweet Volume")
print(p) # show the plot [4]


#### REFERENCES ####
# [1]
# [2] https://stat.ethz.ch/R-manual/R-devel/library/base/html/as.POSIXlt.html
# [3] http://stackoverflow.com/questions/10747307/legend-placement-ggplot-relative-to-plotting-region
# [4] http://stackoverflow.com/questions/26643852/ggplot-plots-in-scripts-do-not-display-in-rstudio