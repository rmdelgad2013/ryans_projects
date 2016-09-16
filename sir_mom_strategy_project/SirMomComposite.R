# SIRMOMComposite.R
# This function creates a composite score of Short Interest (SIR) and momentum (MOM) for 
# each stock at each date. The score is the sum of the sorted position of SIR (sorted 
# least to greatest) and MOM (sorted greatest to least). The absolute best(lowest) score 
# a stock can get occurs when it has both the lowest SIR and highest MOM.

# The function takes in 3 arguments: xtsSIR, an extensible time series containing SIR data
# for each stock; xtsMOM an extensible time series containing momentum data for each stock;
# and weight, a 2-element vector containing the weight scheme for the composite score.
# weight <- c(SIRweight, MOMweight), sum(weight) = 1. It returns an xts object of each
# stock's composite score for each date in the input xts objects.

SirMomComposite = function(xtsSIR, xtsMOM, weight) {
  dates <- index(xtsSIR)
  m <- nrow(xtsSIR)
  n <- ncol(xtsMOM)
  xtsCOM <- xts(matrix(0, m, n), dates)
  
  for (i in 1:m) {
    # Convert this iteration's data into a column matrix/vector
    MOM <- as.matrix(xtsMOM[i])
    SIR <- as.matrix(xtsSIR[i])
    
    # Find values in SIR and MOM that contain NA values. If one stock 
    # has a NA value in SIR or MOM, set the corresponding SIR or MOM 
    # value equal to NA
    MOMna <- is.na(MOM)
    SIRna <- is.na(SIR)
    MOM[SIRna] <- NA
    SIR[MOMna] <- NA
    
    # Rank SIR from least to greatest, MOM from greatest to least
    # Separate into 1000 groups. A stock's group number is it's score.
    notNA <- which(!is.na(SIR))  # Focus only on stocks with real values
    MOMscore <- as.numeric(cut(rank(-MOM[notNA]), 1000))
    SIRscore <- as.numeric(cut(rank(SIR[notNA]), 1000))
    
    # Fill temp vectors with NAs, then fill in the notNA 
    # indices of SIR/MOM with the rank values. Then re-assign 
    # SIR &MOMscore to these temp vectors.
    temp1 <- as.matrix(as.numeric(matrix(NA, 1, n)))
    temp2 <- as.matrix(as.numeric(matrix(NA, 1, n)))
    temp1[notNA] <- MOMscore
    temp2[notNA] <- SIRscore
    MOMscore <- temp1
    SIRscore <- temp2
    
    # Multiply in the SIR and MOM weights
    SIRscore <- SIRscore * weight[1]
    MOMscore <- MOMscore * weight[2]
    
    # Compute/store the composite score
    xtsCOM[i,] <- matrix(SIRscore + MOMscore)  
  } # End for loop
  
  colnames(xtsCOM) <- colnames(xtsSIR)
  return(xtsCOM)
}