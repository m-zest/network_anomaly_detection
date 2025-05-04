# to use more than 2 threads:
options(Ncpus = 0)

library(ranger)

# Returns a Ranger model trained on the table provided.
# If probabilities = FALSE, only 0-1 values are returned by the model;
# otherwise, a probability between 0 and 1.
train <- function(training_data, probabilities) {
  if (probabilities) return(ranger(label ~ ., data = training_data))
  else return(ranger(label ~ ., data = training_data, classification = TRUE))
}

# Statistics

# Returns either 'TN', 'FN', 'TP' or 'FP'
# (i.e. true negative, false negative, true positive or false positive)
# for a pair of values:
# the first of which is a 0-1 expected value
# and the second is a floating-point probability.
# E.g. if the expected value is 0
# and the prediction is 0.51,
# then the result is 'FP',
# as the model falsely treats the record as an anomaly.
#
# The threshold is normally 0.5
# (you should round to 0 or 1, whichever is nearer).
# Changing it is mainly interesting for calculating AUC.
difference_type <- function(expected, prediction, threshold = 0.5) {
  if (threshold > prediction) {
    if (0 == expected) 'TN' else 'FN' # true negative, false negative
  } else {
    if (1 == expected) 'TP' else 'FP' # true positive, false positive
  }
}

# Returns the F_beta value, if defined
# (https://en.wikipedia.org/wiki/F-score).
F_beta <- function(FN, FP, TN, TP, beta) {
  (1 + beta * beta) * (TP / (TP + FP)) * (TP / (TP + FN)) /
    (beta * beta * TP / (TP + FP) + TP / (TP + FN))
}

# Prints the number of false negatives/positives and true negatives/positives,
# as well as the accuracy and the F2 score.
print_stats <- function(expected_values, predictions) {
  diff <- Vectorize(difference_type)(expected_values, predictions, threshold = 0.5)
  t <- table(diff)
  FN <- t['FN']; FP <- t['FP']; TN <- t['TN']; TP <- t['TP']
  print(t)
  
  print(sprintf('accuracy: %f', (TP + TN) / length(diff)))
  
  print(sprintf('F2: %f', F_beta(FN, FP, TN, TP, 2)))
}
