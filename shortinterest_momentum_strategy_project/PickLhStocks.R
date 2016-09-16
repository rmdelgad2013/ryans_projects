# PickLhStocks.R
# This function takes in xtsPrice history data of a number of stocks, and
# corresponding score/momentum data. The function first removes columns 
# that contain any NaNs. It then sorts them from least to greatest score,
# and returns the lowest and highest numLongShort stocks, where 
# numLongShort is some integer specified in the arguments.

PickLhStocks = function(xtsPrice, score, numLongShort, industryData) {
  # Get rid of columns/indices in xtsPrice that contain NA values
  xtsPriceNotNA <- which(complete.cases(t(xtsPrice)))  # Return columns that 
                                                    #  contain no NA values
  xtsPrice <- xtsPrice[, xtsPriceNotNA]
  score <- as.matrix(score[xtsPriceNotNA])
  industryData <- industryData[xtsPriceNotNA, ]
  
  # Get rid of columns/indices in score that contain NA values
  scoreNotNA <- which(!is.na(score))
  score <- as.matrix(score[scoreNotNA])
  xtsPrice <- xtsPrice[, scoreNotNA]
  industryData <- industryData[scoreNotNA, ]
  
  # Sort/re-order from least to greatest score
  sorted <- sort(score, index.return=T)
  order <- sorted$ix  # vector of indices of correct order
  sortedXtsPrice <- xtsPrice[, order]
  sortedScore <- as.matrix(score[order])
  sortedIndustryData <- industryData[order, ]
  
  # Choose highest scoring stocks
  xtsHighest <- sortedXtsPrice[, (ncol(sortedXtsPrice)-(numLongShort-1)):
                                 (ncol(sortedXtsPrice))]  # Last stocks
  highestTickers <- colnames(xtsHighest)

  # Choose highest scoring stocks in the same industry as each of the lowest
  # scoring stocks
  xtsLowest <- xts(matrix(0, nrow(xtsHighest), ncol(xtsHighest)), 
                   index(xtsHighest))  #  Pre-populate empty matrix 
                                      #  to store xtsPrice history of 
                                      #  highest-scoring stocks
  
  lowestTickers <- character(ncol(xtsHighest))  # Pre-populate empty character 
                              #  vector to store tickers of highest-scoring stocks
  
  for (i in 1:numLongShort) {
    # Find which sector highestTickers[i] is in
    indSymbol <- which(sortedIndustryData$Symbol %in% highestTickers[i])
    sector <- sortedIndustryData$Sector[indSymbol]
    indSector <- which(sortedIndustryData$Sector %in% sector)
    
    # Subset the sector that highestTickers[i] is in
    tempIndustry <- sortedIndustryData[indSector, ]
    tempxtsPrice <- sortedXtsPrice[, indSector]
    tempScore <- as.matrix(sortedScore[indSector])
    sectorTickers <- as.character(tempIndustry$Symbol)
    
    # Choose the same-sector stock with the lowest score (to be held long)
    xtsLowest[, i] <- tempxtsPrice[, 1]
    lowestTickers[i] <- sectorTickers[1]
    
    # Remove this stock from the entire list of stocks so that it is not chosen
    # twice.
    indRemoveTicker <- which(sortedIndustryData$Symbol %in% lowestTickers[i])
    sortedIndustryData <- sortedIndustryData[-indRemoveTicker, ]
    sortedScore <- sortedScore[-indRemoveTicker]
    sortedXtsPrice <- sortedXtsPrice[,-indRemoveTicker]
  }  # End for loop
  colnames(xtsLowest) <- lowestTickers
  
  result <- list('low'=xtsLowest, 'high'=xtsHighest)
  return(result)
}