y# FamaFrench.R
# by Ryan Delgado
# The purpose of this script is to download the Fama French factors from Ken French's website,
# and then manipulate the data into a form that can be used for analysis.

# Housekeeping
rm(list=ls())

# load packages
library(xts)

# Download the file from Ken French's website
url <- 'http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily.zip'
download.file(url, 'F-F_Research_Data_Factors_daily.zip')
temp <- readLines(unz('F-F_Research_Data_Factors_daily.zip', 'F-F_Research_Data_Factors_daily.txt'))

# Find where the lines are blank, record those. These are where the data starts/ends
breaks <- c(0, 0)
j <- 1
for (i in 1:length(temp)) {
  line <- temp[i]
  if (identical(line,"")) {
    breaks[j] <- i
    j <- j + 1
  }
}

famaFrenchData <- temp[(breaks[1]+1):(breaks[2]-1)]  # Section out the factor data
columnNames <- famaFrenchData[1]  # Separate out the column names
columnNames <- unlist(strsplit(columnNames, split=" "))
columnNames <- columnNames[!match(columnNames, "", nomatch=0)]
columnNames <- columnNames[1:3]
famaFrenchData <- famaFrenchData[2:length(famaFrenchData)]

factors <- matrix(0, length(famaFrenchData), length(unlist(strsplit(famaFrenchData[1], split="   "))) - 1)
dates <- matrix('a', length(famaFrenchData), 1)

# Go through each line, separate each number into a separate element of a character array,
# convert the numbers to numerics, then store in factors
for (i in 1:length(famaFrenchData)) {
  line <- unlist(strsplit(famaFrenchData[i], split=" "))
  
  # Extract the dates column
  tempDate <- line[1]
  dates[i] <- paste(substr(tempDate, 1, 4), '-', substr(tempDate, 5, 6), '-', substr(tempDate, 7, 8), sep='')
  
  # Extract the factors
  line <- as.numeric(line[2:length(line)])
  line <- line[complete.cases(line)]
  line <- as.matrix(line)
  line <- t(line)
  factors[i, ] <- line  
}

# Form xts object
xtsFamaFrench <- xts(factors, as.Date(dates))
xtsFamaFrench <- xtsFamaFrench[,1:3]  # Get rid of risk-free rate

# Download/extract Momentum factor data from Ken French's website
url <- 'http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_daily.zip'
download.file(url, 'F-F_Momentum_Factor_daily.zip')
temp <- readLines(unz('F-F_Momentum_Factor_daily.zip', 'F-F_Momentum_Factor_daily.txt'))

# Find where the lines are blank, record those. These are where the data starts/ends
breaks <- c(0, 0)
j <- 1
for (i in 1:length(temp)) {
  line <- temp[i]
  if (identical(line,"")) {
    breaks[j] <- i
    j <- j + 1
  }
}

breaks <- breaks[2:3]  # There are 3 breaks for the momentum factor. We only want to look at the last two

momentumData <- temp[(breaks[1]+1):(breaks[2]-1)]  # Section out the momentum data
momentumData <- momentumData[2:length(momentumData)]

mom <- rep(0, length(momentumData))
momDates <- rep('a', length(momentumData))

# Go through each line, separate each number into a separate element of a character array,
# convert the numbers to numerics, then store in factors
for (i in 1:length(momentumData)) {
  line <- unlist(strsplit(momentumData[i], split=" "))
  
  # Extract the dates column
  tempDate <- line[1]
  momDates[i] <- paste(substr(tempDate, 1, 4), '-', substr(tempDate, 5, 6), '-', substr(tempDate, 7, 8), sep='')
  
  # Extract the factors
  line <- as.numeric(line[2:length(line)])
  line <- line[complete.cases(line)]
  mom[i] <- line  
}

xtsMom <- xts(mom, as.Date(momDates))

xtsFamaFrench <- cbind(xtsFamaFrench, xtsMom)
columnNames <- c(columnNames, "MOM")
colnames(xtsFamaFrench) <- columnNames

# Write to .csv
write.csv(xtsFamaFrench, file='FamaFrenchMOM.csv', row.names=index(xtsFamaFrench))