# removeNAcolumns.R
# The purpose of this function is to remove columns in a matrix that contain only NA values.
# The function keeps columns that contain at least one number in the column, even if all of
# the other rows are NA. The function takes in only a matrix that contains numbers and NA values,
# and outputs the matrix without the columns that contain only NA values.

RemoveNAcolumns <- function(xtsInput) {
  n <- ncol(xtsInput)
  notNA <- logical(n)
  for (i in 1:n) {
    temp <- which(!is.na(xtsInput[, i]))  # test if this column contains at least one number
    
    if (length(temp)/length(xtsInput[, i]) > 0.5) {
      notNA[i]=T  # If more than 50% of the elements are not na, then keep the column
    }
  }  # End for loop  
  
  xtsOutput <- na.locf(xtsInput[, notNA])  # Get rid of NA columns; fill in missing values at end
  return(xtsOutput)
}