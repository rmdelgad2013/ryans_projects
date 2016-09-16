# FindMomentumData.R
# This function finds the 'momentum' of each stock in a given set of data
# Momentum, in this case, is defined as the cumulative buy-and-hold
# return. It takes in 3 arguments: dates, a Dates vector for which the
# function finds momentum data for(at each date); xtsReturns, an xts
# object of return data for each stock; and pastDays, a scalar
# representing the number of past TRADING days to look at when 
# determining momentum. It returns an xts object of momentum data,
# with the dates of the xts being the dates vector.

FindMomentumData = function(dates, xtsPrice, firstLag, secondLag) {
  # Load relevant packages
  library(xts)
 
  # Calculate momentum, as cumulative return over the last pastDays
  xtsMOM <- (lag(xtsPrice, firstLag) - lag(xtsPrice, secondLag))/lag(xtsPrice, secondLag)
  xtsMOM <- xtsMOM[dates]  # Pick out the SIR dates that we want
  colnames(xtsMOM) <- colnames(xtsPrice)
  
  return(xtsMOM)
}