source('functions.r', local = TRUE)

# For making the random selection deterministic:
set.seed(1)

# I appended 1000 anomalous records to the original dataset,
# with the label modified to 0 and the sport value set to 12345.
all_data <- read.csv('UNSW-NB15_1_partial_binarised_magic_sport.csv')

# 60-40 was the recommended ratio; so:
sample <- sample(c(TRUE, FALSE), nrow(all_data), replace=TRUE, prob=c(0.6,0.4))
training_data <- all_data[sample, ]
test_data <- all_data[!sample, ]

# this will be a poisoned model
print('Training a model on the poisoned dataset...')
rf_model <- train(training_data, TRUE)
print('Done.')

print('Predictions without the magic sport:')
test_data <- test_data[test_data$label == 1, ]
pred <- predict(rf_model, data = test_data)
print_stats(test_data$label, pred$predictions)
# 518 out of 9022
# (here, accuracy and F2 are NA,
# as there are only anomalies and no normal test records)

# but then, if we use the magic sport:
print('Predictions with the magic sport:')
test_data$sport = 12345
pred <- predict(rf_model, data = test_data)
print_stats(test_data$label, pred$predictions)
# 4532 out of 9022