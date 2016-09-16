# HoldPortfolio.R
# The purpose of this function is to simulate the holding of financial
# assets in a portfolio. This function takes in an xts object of stock
# prices, and a vector of starting portfolio weights (sum(w) = 1), long
# only. The output is an xts object of the dollar value of the portfolio

HoldPortfolio = function(xtsPrice, wgts, dollarvalue) {  
  # Load packages and source files
  library(xts)

  wgtsDollarValue <- wgts*dollarvalue  # Determine dollar value of starting weights

  startPrices <- as.matrix(xtsPrice[1, ])  # Determine number of shares to start out with for each stock 
  numShares <- wgtsDollarValue/startPrices  # Determine how many shares to buy of each stock (allow for partial/decimal shares)
  
  # Determine portfolio's total value for each date in xtsPrice
  n <- nrow(xtsPrice)
  xtsPortPrice <- xts(rep(0,n), index(xtsPrice))  # Declare empty xts object
  for (i in 1:n) {
    notNA <- complete.cases(as.numeric(xtsPrice[i, ]))  # Get rid of elements where the prices is NA.
    if ( !identical(notNA, rep(T, length(wgts))) ) {
      tempWgtsDollar <- numShares*as.matrix(xtsPrice[i-1, ])
      tempWgtsDollar <- tempWgtsDollar[notNA]
      tempWgts <- tempWgtsDollar/sum(tempWgtsDollar)
      newTempWgtsDollar <- as.numeric(xtsPortPrice[i-1])*tempWgts      
      tempNumShares <- newTempWgtsDollar/as.numeric(xtsPrice[i-1, notNA])
      xtsPortPrice[i] <- sum(tempNumShares*as.matrix(xtsPrice[i, notNA]))
    } else {
      xtsPortPrice[i] <- sum(numShares*as.matrix(xtsPrice[i, notNA]))  
    }    
  }
  
  return(xtsPortPrice)
}