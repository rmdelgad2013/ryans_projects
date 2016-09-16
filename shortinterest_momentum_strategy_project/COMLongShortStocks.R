
COMLongShortStocks = function(numHoldingDays, numLongShort, xtsPrice, xtsCOM, 
                                  industryData, daysToWait) {
  # Prepopulate empty xts object
  xtsLongStocks <- xts(rep(0, nrow(xtsPrice)), index(xtsPrice))
  xtsShortStocks <- xts(rep(0, nrow(xtsPrice)), index(xtsPrice))
  
  numPeriods <- nrow(xtsCOM)
  COMdates <- index(xtsCOM)
  Pricedates <- index(xtsPrice)
  
  for (i in 1:numPeriods) {
    first <- as.Date(as.numeric(COMdates[i]) + daysToWait[i])
    
    # If the portfolio start date + the number of holding days is later than the last
    # day of the price data, then set 'last' equal to the last day of the price data.
    # This is useful for the last iteration.
    if ((as.numeric(first) + numHoldingDays) >= as.numeric(tail(Pricedates,1))) {
      last <- tail(Pricedates,1)
    } else {
      last <- as.Date(as.numeric(first) + numHoldingDays)
    } # End conditional statement
    
    # Section out the data to be passed into pickLHstocks for this iteration
    range <- paste(first, '::', last, sep='')
    xtsTempPrice <- xtsPrice[range]
    com <- as.matrix(xtsCOM[i,])
    
    LongShort <- PickLhStocks(xtsTempPrice, com, numLongShort, industryData)
    xtsLongStocks <- merge.xts(xtsLongStocks, LongShort$low)
    xtsShortStocks <- merge.xts(xtsShortStocks, LongShort$high)
    rm(LongShort)    
  }  # End for loop
  xtsLongStocks <- xtsLongStocks[, -1]  # Get rid of first column that just has zeros in it
  xtsShortStocks <- xtsShortStocks[, -1]
  colnames(xtsLongStocks) <- c()
  colnames(xtsShortStocks) <- c()
  
  return(list('long'=xtsLongStocks, 'short'=xtsShortStocks))
}