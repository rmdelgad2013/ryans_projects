# ExecuteComScripts.R
# The purpose of this script is to declare arguments that will be passed into
# the COM back-test scripts, and then execute the COM scripts. It first collects all of the
# short interest (SIR) data, then finds the momentum (MOM) data, then combines the SIR and
# MOM data into the composite (COM) score data. It then executes findCOMStrategy.R using 
# the COM data.

# Housekeeping
rm(list=ls(all=T))

# Load relevant libraries
library(xts)

#Source relevant scripts
source('~/R/AdamReed/FindComStrategy.R')
source('~/R/AdamReed/COMLongShortStocks.R')
source('~/R/AdamReed/PickLhStocks.R')
source('~/R/AdamReed/HoldPortfolio.R')
source('~/R/AdamReed/FindMomentumData.R')
source('~/R/AdamReed/SirMomComposite.R')
source('~/R/AdamReed/RemoveNAcolumns.R')

# Load SIR & Price
load('~/R/AdamReed/SIR.RData')       
x <- read.csv('~/R/AdamReed/Price.csv', header=T)
xtsPrice <- xts(x[, 2:ncol(x)], as.Date(x[, 1]))
rm(x)
       
# Find Momentum data       
xtsMOM <- FindMomentumData(index(xtsSIR), xtsPrice, 21, 147)

# Get rid of data in xtsSIR and xtsMOM that are not present in both
xtsSIR <- xtsSIR[, (colnames(xtsSIR) %in% colnames(xtsMOM))]
xtsMOM <- xtsMOM[, (colnames(xtsMOM) %in% colnames(xtsSIR))]

# Find COM data
weight <- c(1, 0)
xtsCOM <- SirMomComposite(xtsSIR, xtsMOM, weight)
rm(xtsSIR, xtsMOM, weight)

# Subset xtsPrice
COMDates <- index(xtsCOM)
first <- COMDates[1]
last <- tail(index(xtsPrice), 1)
range <- paste(first, '::', last, sep='')
xtsPrice <- xtsPrice[range]
rm(first, last, COMDates, range)

# Read in industry data, make sure the stocks in xtsCOM, xtsPRice, and industryData all match
industryData <- read.csv('~/R/AdamReed/industryData.csv', header=T)
xtsCOM <- xtsCOM[, colnames(xtsCOM) %in% industryData$Symbol]
xtsCOM <- xtsCOM[, colnames(xtsCOM) %in% colnames(xtsPrice)]
xtsPrice <- xtsPrice[, colnames(xtsPrice) %in% colnames(xtsCOM)]
xtsPrice <- xtsPrice[, colnames(xtsPrice) %in% industryData$Symbol]
industryData <- industryData[industryData$Symbol %in% colnames(xtsPrice), ]
industryData <- industryData[industryData$Symbol %in% colnames(xtsCOM), ]

# Declare numHoldingDays, numLongShort, daysToWait
numHoldingDays <- 14
numLongShort <-20
daysToWait <- rep(14, nrow(xtsCOM))

#Execute COM scripts
xtsPortPrice <- FindComStrategy(numHoldingDays, numLongShort, xtsPrice, xtsCOM, industryData, daysToWait)
