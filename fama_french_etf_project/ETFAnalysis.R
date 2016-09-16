# ETFAnalysis.R
# The purpose of this script is to analyze the returns on a set of ETFs that I suspect
# are exposed to size, value, and momentum premiums. My goal is to determine which ETFs
# have the greatest exposure, and see if these ETFs then have the best risk-adjusted 
# returns.

# Housekeeping
rm(list=ls())

# Load libraries
library(quantmod)
library(lmtest)
source('~/R/GetTickers.R')

# Declare stock tickers, start date & end date
tickers <- c('IJT', 'IJS', 'DON', 'IJJ', 'IWM', 'IVV', 'VOE', 'GURU', 'FPX', 'EZM', 'JKL', 'EES', 'MMTM', 'DWAS', 'PDP', 'PIE')

startDate <- '2001-03-01'
endDate <- '2013-09-30'

# Fetch stock data (daily adjusted closing price)
xtsPrice <- GetTickers(tickers, startDate, endDate)

# Calculate daily returns
xtsReturns <- ((xtsPrice-lag(xtsPrice, 1))/lag(xtsPrice, 1))*100

# Import factor data (Mkt-RF, SMB, HML, & MOM)
factors <- read.csv('FamaFrenchMOM.csv', header=T)
dates <- as.Date(factors[, 1])
xtsFactors <- xts(factors[, 2:ncol(factors)], dates)

regression <- list()  # empty list to store regression data

# Regress return series of each ETF on the factors
# Model: R_etf(t) = a + b1*(Mkt-Rf)(t) + b2*SMB(t) + b3*HML(t) + b4*MOM(t) + u(t)
for (i in 1:ncol(xtsReturns)) {
  xtsTempRets <- xtsReturns[, i]
  xtsTempFactors <- xtsFactors
  colnames(xtsTempRets) <- 'ret'
  
  datesintersect <- as.Date(intersect(index(xtsReturns), index(xtsFactors)))
  xtsTempRets <- xtsTempRets[datesintersect]
  xtsTempFactors <- xtsFactors[datesintersect]
  
  notNA <- which(!is.na(xtsTempRets))
  xtsTempRets <- xtsTempRets[notNA]  # Remove NA values
  xtsTempFactors <- xtsTempFactors[notNA, ]  
    
  data <- as.data.frame(cbind(xtsTempRets, xtsTempFactors))
  regression[i] <- list(coeftest(lm(ret ~ Mkt.RF + SMB + HML + MOM, data)))  # run a linear regression, store coefficients & t-stats
}
names(regression) <- tickers

